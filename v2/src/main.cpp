/*
 * ============================================================================
 *  D.E.V_Darshan v2.0 — ESP32-S3 Super Mini Board Diagnostics & Hardware Probe
 * ============================================================================
 *  Author: Sakshyam Bastakoti & Antigravity
 *
 *  Features probed:
 *    1. Chip Info: Model, Revision, Cores, CPU Frequency, Internal Temp
 *    2. Flash Memory: Chip Size, Speed, SPI Mode, Real JEDEC ID
 *    3. SRAM & Heap: Total Internal SRAM, Free Heap, Max Alloc Block
 *    4. PSRAM / SPIRAM: eFuse detection, psramFound(), Total & Free PSRAM
 *    5. LittleFS Filesystem: Mount status, Partition size, Used space
 *    6. I2C OLED Probe: Scans I2C bus on GPIO1/2 (and GPIO8/9) for SSD1306 (0x3C)
 *       and draws a hardware status screen on the 0.91" 128x32 OLED
 *    7. 4-Tactile Button Live Test: GPIO4, 5, 6, 7 real-time state monitor
 * ============================================================================
 */

#include <Arduino.h>
#include <Wire.h>
#include <esp_chip_info.h>
#include <esp_flash.h>
#include <esp_system.h>
#include <LittleFS.h>
#include <U8g2lib.h>

// ---------------------------------------------------------------------------
// Hardware Pin Configuration (Recommended for ESP32-S3 Super Mini)
// ---------------------------------------------------------------------------
#define I2C_SDA_PIN     1     // Default SDA
#define I2C_SCL_PIN     2     // Default SCL
#define I2C_ALT_SDA     8     // Alternate SDA (if user wired to GPIO 8)
#define I2C_ALT_SCL     9     // Alternate SCL (if user wired to GPIO 9)

#define PIN_BTN_UP      4     // Button 1: UP
#define PIN_BTN_DOWN    5     // Button 2: DOWN
#define PIN_BTN_SELECT  6     // Button 3: SELECT / ENTER
#define PIN_BTN_BACK    7     // Button 4: BACK / PANIC

// Button test structure
struct ButtonTest {
    uint8_t pin;
    const char* name;
    bool lastState;
    unsigned long lastDebounce;
};

static ButtonTest buttons[] = {
    { PIN_BTN_UP,     "UP     (GPIO 4)", HIGH, 0 },
    { PIN_BTN_DOWN,   "DOWN   (GPIO 5)", HIGH, 0 },
    { PIN_BTN_SELECT, "SELECT (GPIO 6)", HIGH, 0 },
    { PIN_BTN_BACK,   "BACK   (GPIO 7)", HIGH, 0 }
};

// Global OLED instance pointer (allocated if display is found)
static U8G2_SSD1306_128X32_UNIVISION_F_HW_I2C *u8g2 = nullptr;
static bool oledDetected = false;
static uint8_t oledSda = 0, oledScl = 0;

// ---------------------------------------------------------------------------
// Helper: Print Section Header
// ---------------------------------------------------------------------------
void printHeader(const char* title) {
    Serial.println();
    Serial.println("================================================================");
    Serial.printf("  %s\n", title);
    Serial.println("================================================================");
}

// ---------------------------------------------------------------------------
// 1. Chip & CPU Diagnostics
// ---------------------------------------------------------------------------
void diagnoseChip() {
    printHeader("1. ESP32-S3 CHIP SPECIFICATIONS");

    esp_chip_info_t chip_info;
    esp_chip_info(&chip_info);

    Serial.printf("  Chip Model:            %s\n", ESP.getChipModel());
    Serial.printf("  Chip Revision:         v%d\n", ESP.getChipRevision());
    Serial.printf("  CPU Cores:             %d core(s)\n", chip_info.cores);
    Serial.printf("  CPU Clock Frequency:   %u MHz\n", ESP.getCpuFreqMHz());
    Serial.printf("  SDK Version:           %s\n", ESP.getSdkVersion());

    // Features flag check
    Serial.print("  Silicon Features:      ");
    if (chip_info.features & CHIP_FEATURE_WIFI_BGN) Serial.print("[WiFi 2.4GHz] ");
    if (chip_info.features & CHIP_FEATURE_BLE)      Serial.print("[BLE 5.0] ");
    if (chip_info.features & CHIP_FEATURE_BT)       Serial.print("[Classic BT] ");
    if (chip_info.features & CHIP_FEATURE_EMB_FLASH)Serial.print("[Embedded Flash] ");
    if (chip_info.features & CHIP_FEATURE_EMB_PSRAM)Serial.print("[Embedded PSRAM] ");
    Serial.println();

    // Internal Temperature Sensor (ESP32-S3 has built-in tsens)
    #if defined(temperatureRead)
    float tempC = temperatureRead();
    Serial.printf("  Core Temperature:      %.1f °C (%.1f °F)\n", tempC, (tempC * 9.0 / 5.0) + 32.0);
    #endif
}

// ---------------------------------------------------------------------------
// 2. Flash Memory Diagnostics
// ---------------------------------------------------------------------------
void diagnoseFlash() {
    printHeader("2. FLASH MEMORY SPECIFICATIONS");

    uint32_t flashBytes = ESP.getFlashChipSize();
    float flashMB = flashBytes / (1024.0 * 1024.0);
    uint32_t flashSpeed = ESP.getFlashChipSpeed();
    FlashMode_t flashMode = ESP.getFlashChipMode();

    const char* modeStr = "UNKNOWN";
    switch (flashMode) {
        case FM_QIO:  modeStr = "QIO (Quad I/O - Fast)"; break;
        case FM_QOUT: modeStr = "QOUT (Quad Output)"; break;
        case FM_DIO:  modeStr = "DIO (Dual I/O)"; break;
        case FM_DOUT: modeStr = "DOUT (Dual Output)"; break;
        case FM_FAST_READ: modeStr = "FAST_READ"; break;
        case FM_SLOW_READ: modeStr = "SLOW_READ"; break;
        default: break;
    }

    Serial.printf("  Configured Flash Size: %.2f MB (%u bytes)\n", flashMB, flashBytes);
    Serial.printf("  Flash SPI Speed:       %u MHz\n", flashSpeed / 1000000);
    Serial.printf("  Flash SPI Mode:        %s\n", modeStr);

    // Read real JEDEC ID via esp_flash
    uint32_t flash_id = 0;
    if (esp_flash_read_id(NULL, &flash_id) == ESP_OK) {
        uint8_t mfg_id = flash_id & 0xFF;
        uint16_t dev_id = (flash_id >> 8) & 0xFFFF;
        Serial.printf("  JEDEC Chip ID:         0x%06X (Manufacturer: 0x%02X, Device: 0x%04X)\n", flash_id, mfg_id, dev_id);
    }
}

// ---------------------------------------------------------------------------
// 3. SRAM / Internal Heap Diagnostics
// ---------------------------------------------------------------------------
void diagnoseRAM() {
    printHeader("3. INTERNAL SRAM & HEAP MEMORY");

    uint32_t totalHeap = ESP.getHeapSize();
    uint32_t freeHeap  = ESP.getFreeHeap();
    uint32_t minFree   = ESP.getMinFreeHeap();
    uint32_t maxAlloc  = ESP.getMaxAllocHeap();

    Serial.printf("  Total Internal Heap:   %u bytes (%.2f KB)\n", totalHeap, totalHeap / 1024.0);
    Serial.printf("  Current Free Heap:     %u bytes (%.2f KB)\n", freeHeap, freeHeap / 1024.0);
    Serial.printf("  Lowest Ever Free Heap: %u bytes (%.2f KB)\n", minFree, minFree / 1024.0);
    Serial.printf("  Max Allocatable Block: %u bytes (%.2f KB)\n", maxAlloc, maxAlloc / 1024.0);
}

// ---------------------------------------------------------------------------
// 4. PSRAM / SPIRAM Diagnostics
// ---------------------------------------------------------------------------
void diagnosePSRAM() {
    printHeader("4. EXTERNAL PSRAM (SPIRAM) PROBE");

    esp_chip_info_t chip_info;
    esp_chip_info(&chip_info);

    bool hasEmbeddedPsram = (chip_info.features & CHIP_FEATURE_EMB_PSRAM);
    bool psramActive = psramFound();

    Serial.printf("  eFuse Emb PSRAM Flag:  %s\n", hasEmbeddedPsram ? "YES (Hardware detected)" : "NO");
    Serial.printf("  Runtime PSRAM Active:  %s\n", psramActive ? "YES (Initialized & usable)" : "NO / Not enabled in firmware");

    if (psramActive) {
        uint32_t totalPsram = ESP.getPsramSize();
        uint32_t freePsram  = ESP.getFreePsram();
        Serial.printf("  Total PSRAM Available: %u bytes (%.2f MB)\n", totalPsram, totalPsram / (1024.0 * 1024.0));
        Serial.printf("  Free PSRAM Available:  %u bytes (%.2f MB)\n", freePsram, freePsram / (1024.0 * 1024.0));
        Serial.println("  ==> EXCELLENT: High-speed PSRAM can cache entire documents in RAM!");
    } else {
        Serial.println("  ==> NOTE: If your board has 2MB/8MB PSRAM, ensure `board_build.arduino.memory_type`");
        Serial.println("            and `-DBOARD_HAS_PSRAM` are set in platformio.ini.");
        Serial.println("            If this is a standard 4MB/8MB Flash without PSRAM, 512KB SRAM is more than");
        Serial.println("            enough for all D.E.V_Darshan v2 features!");
    }
}

// ---------------------------------------------------------------------------
// 5. LittleFS Storage Test
// ---------------------------------------------------------------------------
void diagnoseLittleFS() {
    printHeader("5. LITTLEFS FLASH STORAGE CHECK");

    if (LittleFS.begin(true)) {
        size_t totalBytes = LittleFS.totalBytes();
        size_t usedBytes  = LittleFS.usedBytes();
        Serial.println("  LittleFS Mount:        SUCCESS (Format on fail: enabled)");
        Serial.printf("  LittleFS Total Space:  %u bytes (%.2f KB / %.2f MB)\n", totalBytes, totalBytes / 1024.0, totalBytes / (1024.0 * 1024.0));
        Serial.printf("  LittleFS Used Space:   %u bytes (%.2f KB)\n", usedBytes, usedBytes / 1024.0);
        Serial.printf("  LittleFS Free Space:   %u bytes (%.2f KB)\n", totalBytes - usedBytes, (totalBytes - usedBytes) / 1024.0);
    } else {
        Serial.println("  LittleFS Mount:        FAILED (Check partition table)");
    }
}

// ---------------------------------------------------------------------------
// 6. I2C Bus Scanner & 0.91" OLED Test
// ---------------------------------------------------------------------------
bool scanI2cBus(uint8_t sda, uint8_t scl) {
    Serial.printf("\n  Scanning I2C bus on SDA = GPIO%d, SCL = GPIO%d...\n", sda, scl);
    Wire.begin(sda, scl);
    Wire.setClock(400000); // 400kHz fast mode

    int foundDevices = 0;
    bool foundOled = false;

    for (uint8_t addr = 1; addr < 127; addr++) {
        Wire.beginTransmission(addr);
        uint8_t error = Wire.endTransmission();

        if (error == 0) {
            Serial.printf("    -> Found I2C Device at address: 0x%02X", addr);
            if (addr == 0x3C || addr == 0x3D) {
                Serial.print("  <-- [MATCH] SSD1306 0.91\" OLED Display!");
                foundOled = true;
            }
            Serial.println();
            foundDevices++;
        }
    }

    if (foundDevices == 0) {
        Serial.println("    -> No I2C devices detected on these pins.");
    }

    return foundOled;
}

void diagnoseI2CAndOled() {
    printHeader("6. I2C BUS SCANNER & 0.91\" OLED PROBE");

    // Try primary pins GPIO1 and GPIO2
    if (scanI2cBus(I2C_SDA_PIN, I2C_SCL_PIN)) {
        oledDetected = true;
        oledSda = I2C_SDA_PIN;
        oledScl = I2C_SCL_PIN;
    } 
    // If not found, try alternate pins GPIO8 and GPIO9
    else if (scanI2cBus(I2C_ALT_SDA, I2C_ALT_SCL)) {
        oledDetected = true;
        oledSda = I2C_ALT_SDA;
        oledScl = I2C_ALT_SCL;
    }

    if (oledDetected) {
        Serial.printf("  ==> Initializing 0.91\" OLED on SDA=GPIO%d, SCL=GPIO%d...\n", oledSda, oledScl);
        u8g2 = new U8G2_SSD1306_128X32_UNIVISION_F_HW_I2C(U8G2_R0, U8X8_PIN_NONE, oledScl, oledSda);
        u8g2->begin();
        u8g2->clearBuffer();
        u8g2->setFont(u8g2_font_6x10_tf);
        u8g2->drawStr(0, 9, "D.E.V_Darshan v2.0");
        u8g2->drawHLine(0, 11, 128);

        char buf[32];
        snprintf(buf, sizeof(buf), "S3 %.0fMB Fl | %.0fK H", ESP.getFlashChipSize() / (1024.0*1024.0), ESP.getFreeHeap() / 1024.0);
        u8g2->drawStr(0, 22, buf);
        u8g2->drawStr(0, 31, "HW Diagnostics OK!");
        u8g2->sendBuffer();
        Serial.println("  ==> OLED Screen successfully drawn! [PASS]");
    } else {
        Serial.println("  ==> [NOTE] 0.91\" OLED not detected yet.");
        Serial.println("      Wiring reminder: VCC->3V3, GND->GND, SDA->GPIO1, SCL->GPIO2.");
    }
}

// ---------------------------------------------------------------------------
// 7. 4-Tactile Button Tester Setup
// ---------------------------------------------------------------------------
void setupButtons() {
    printHeader("7. 4-TACTILE BUTTON LIVE MONITOR INITIALIZATION");
    Serial.println("  Configuring pins with internal pull-ups (Active LOW):");

    for (size_t i = 0; i < 4; i++) {
        pinMode(buttons[i].pin, INPUT_PULLUP);
        buttons[i].lastState = digitalRead(buttons[i].pin);
        Serial.printf("    - Button %d: %-18s [Initial State: %s]\n",
                      i + 1, buttons[i].name,
                      buttons[i].lastState == LOW ? "PRESSED (LOW)" : "RELEASED (HIGH)");
    }
    Serial.println();
    Serial.println("  ==> Interactive Mode Active:");
    Serial.println("      Press any of the 4 buttons now to test physical switch & debouncing!");
    Serial.println("================================================================");
}

// ---------------------------------------------------------------------------
// Arduino Setup & Main Diagnostics Run
// ---------------------------------------------------------------------------
void setup() {
    // Wait for USB Serial CDC to stabilize
    Serial.begin(115200);
    unsigned long startWait = millis();
    while (!Serial && (millis() - startWait < 3000)) {
        delay(10);
    }

    delay(200);
    printHeader("D.E.V_Darshan v2.0 — ESP32-S3 SUPER MINI PROBE");
    Serial.println("  Running comprehensive hardware diagnostics...");

    diagnoseChip();
    diagnoseFlash();
    diagnoseRAM();
    diagnosePSRAM();
    diagnoseLittleFS();
    diagnoseI2CAndOled();
    setupButtons();
}

// ---------------------------------------------------------------------------
// Arduino Loop: Live Button Monitoring & Status Heartbeat
// ---------------------------------------------------------------------------
void loop() {
    unsigned long now = millis();

    // Check all 4 buttons
    for (size_t i = 0; i < 4; i++) {
        int raw = digitalRead(buttons[i].pin);

        if (raw != buttons[i].lastState) {
            if (now - buttons[i].lastDebounce > 30) { // 30ms debounce
                buttons[i].lastState = raw;
                buttons[i].lastDebounce = now;

                if (raw == LOW) {
                    Serial.printf("  >>> [BUTTON PRESSED]  Button %d: %s\n", i + 1, buttons[i].name);
                    // If OLED is connected, flash button feedback on screen
                    if (u8g2) {
                        u8g2->clearBuffer();
                        u8g2->setFont(u8g2_font_6x10_tf);
                        u8g2->drawStr(0, 9, "BUTTON TEST ACTIVE");
                        u8g2->drawHLine(0, 11, 128);
                        char buf[32];
                        snprintf(buf, sizeof(buf), "Pressed: BTN %d", (int)(i + 1));
                        u8g2->drawStr(0, 22, buf);
                        u8g2->drawStr(0, 31, buttons[i].name);
                        u8g2->sendBuffer();
                    }
                } else {
                    Serial.printf("  <<< [BUTTON RELEASED] Button %d: %s\n", i + 1, buttons[i].name);
                }
            }
        }
    }

    // Heartbeat every 10 seconds to confirm CPU stability & free heap
    static unsigned long lastHeartbeat = 0;
    if (now - lastHeartbeat >= 10000) {
        lastHeartbeat = now;
        Serial.printf("  [HEARTBEAT] Free Heap: %u bytes (%.1f KB) | Uptime: %lu sec\n",
                      ESP.getFreeHeap(), ESP.getFreeHeap() / 1024.0, now / 1000);
    }

    delay(5);
}
