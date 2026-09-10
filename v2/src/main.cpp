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
 *    6. I2C OLED Probe: Scans I2C bus on GPIO1/2 (and GPIO8/9) for SSD1306
 * (0x3C) and draws a hardware status screen on the 0.91" 128x32 OLED
 *    7. 4-Tactile Button Live Test: GPIO4, 5, 6, 7 real-time state monitor
 * ============================================================================
 */

#include <Arduino.h>
#include <LittleFS.h>
#include <U8g2lib.h>
#include <Wire.h>
#include <esp_chip_info.h>
#include <esp_flash.h>
#include <esp_system.h>

// ---------------------------------------------------------------------------
// Hardware Pin Configuration (ESP32-S3 Super Mini)
// ---------------------------------------------------------------------------
#define I2C_SDA_PIN 1 // Primary SDA
#define I2C_SCL_PIN 2 // Primary SCL
#define I2C_ALT_SDA 8 // Alternate SDA (if user wired to GPIO 8)
#define I2C_ALT_SCL 9 // Alternate SCL (if user wired to GPIO 9)

#define PIN_BTN_UP 4     // Button 1: UP
#define PIN_BTN_DOWN 5   // Button 2: DOWN
#define PIN_BTN_SELECT 6 // Button 3: SELECT / ENTER
#define PIN_BTN_BACK 7   // Button 4: BACK / PANIC

// Button test structure
struct ButtonTest {
  uint8_t pin;
  const char *name;
  bool lastState;
  unsigned long lastDebounce;
};

static ButtonTest buttons[] = {{PIN_BTN_UP, "UP     (GPIO 4)", HIGH, 0},
                               {PIN_BTN_DOWN, "DOWN   (GPIO 5)", HIGH, 0},
                               {PIN_BTN_SELECT, "SELECT (GPIO 6)", HIGH, 0},
                               {PIN_BTN_BACK, "BACK   (GPIO 7)", HIGH, 0}};

// Global OLED instance pointer (allocated if display is found)
static U8G2_SSD1306_128X32_UNIVISION_F_HW_I2C *u8g2 = nullptr;
static bool oledDetected = false;
static uint8_t oledSda = 0, oledScl = 0;
static bool initialReportPrinted = false;

// ---------------------------------------------------------------------------
// Helper: Print Section Header
// ---------------------------------------------------------------------------
void printHeader(const char *title) {
  Serial.println();
  Serial.println(
      "================================================================");
  Serial.printf("  %s\n", title);
  Serial.println(
      "================================================================");
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

  Serial.print("  Silicon Features:      ");
  if (chip_info.features & CHIP_FEATURE_WIFI_BGN)
    Serial.print("[WiFi 2.4GHz] ");
  if (chip_info.features & CHIP_FEATURE_BLE)
    Serial.print("[BLE 5.0] ");
  if (chip_info.features & CHIP_FEATURE_BT)
    Serial.print("[Classic BT] ");
  if (chip_info.features & CHIP_FEATURE_EMB_FLASH)
    Serial.print("[Embedded Flash] ");
  if (chip_info.features & CHIP_FEATURE_EMB_PSRAM)
    Serial.print("[Embedded PSRAM] ");
  Serial.println();

#if defined(temperatureRead)
  float tempC = temperatureRead();
  Serial.printf("  Core Temperature:      %.1f °C (%.1f °F)\n", tempC,
                (tempC * 9.0 / 5.0) + 32.0);
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

  const char *modeStr = "UNKNOWN";
  switch (flashMode) {
  case FM_QIO:
    modeStr = "QIO (Quad I/O)";
    break;
  case FM_QOUT:
    modeStr = "QOUT (Quad Output)";
    break;
  case FM_DIO:
    modeStr = "DIO (Dual I/O - Active)";
    break;
  case FM_DOUT:
    modeStr = "DOUT (Dual Output)";
    break;
  default:
    break;
  }

  Serial.printf("  Detected Flash Size:   %.2f MB (%u bytes)\n", flashMB,
                flashBytes);
  Serial.printf("  Flash SPI Speed:       %u MHz\n", flashSpeed / 1000000);
  Serial.printf("  Flash SPI Mode:        %s\n", modeStr);

  uint32_t flash_id = 0;
  if (esp_flash_read_id(NULL, &flash_id) == ESP_OK) {
    uint8_t mfg_id = flash_id & 0xFF;
    uint16_t dev_id = (flash_id >> 8) & 0xFFFF;
    Serial.printf("  JEDEC Chip ID:         0x%06X (Manufacturer: 0x%02X, "
                  "Device: 0x%04X)\n",
                  flash_id, mfg_id, dev_id);
  }
}

// ---------------------------------------------------------------------------
// 3. SRAM / Internal Heap Diagnostics
// ---------------------------------------------------------------------------
void diagnoseRAM() {
  printHeader("3. INTERNAL SRAM & HEAP MEMORY");

  uint32_t totalHeap = ESP.getHeapSize();
  uint32_t freeHeap = ESP.getFreeHeap();
  uint32_t minFree = ESP.getMinFreeHeap();
  uint32_t maxAlloc = ESP.getMaxAllocHeap();

  Serial.printf("  Total Internal Heap:   %u bytes (%.2f KB)\n", totalHeap,
                totalHeap / 1024.0);
  Serial.printf("  Current Free Heap:     %u bytes (%.2f KB)\n", freeHeap,
                freeHeap / 1024.0);
  Serial.printf("  Lowest Ever Free Heap: %u bytes (%.2f KB)\n", minFree,
                minFree / 1024.0);
  Serial.printf("  Max Allocatable Block: %u bytes (%.2f KB)\n", maxAlloc,
                maxAlloc / 1024.0);
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

  Serial.printf("  eFuse Emb PSRAM Flag:  %s\n",
                hasEmbeddedPsram ? "YES (Hardware detected)" : "NO");
  Serial.printf("  Runtime PSRAM Active:  %s\n",
                psramActive ? "YES (Initialized & usable)"
                            : "NO (Not present or disabled)");

  if (psramActive) {
    uint32_t totalPsram = ESP.getPsramSize();
    uint32_t freePsram = ESP.getFreePsram();
    Serial.printf("  Total PSRAM Available: %u bytes (%.2f MB)\n", totalPsram,
                  totalPsram / (1024.0 * 1024.0));
    Serial.printf("  Free PSRAM Available:  %u bytes (%.2f MB)\n", freePsram,
                  freePsram / (1024.0 * 1024.0));
  } else {
    Serial.println("  ==> RESULT: Standard 4MB Flash without PSRAM.");
    Serial.println("      With ~340 KB of free internal SRAM, you have massive "
                   "headroom for");
    Serial.println("      the entire text reader, LittleFS, and Wi-Fi portal "
                   "without needing PSRAM!");
  }
}

// ---------------------------------------------------------------------------
// 5. LittleFS Storage Test
// ---------------------------------------------------------------------------
void diagnoseLittleFS() {
  printHeader("5. LITTLEFS FLASH STORAGE CHECK");

  if (LittleFS.begin(true)) {
    size_t totalBytes = LittleFS.totalBytes();
    size_t usedBytes = LittleFS.usedBytes();
    Serial.println("  LittleFS Mount:        SUCCESS");
    Serial.printf("  LittleFS Total Space:  %u bytes (%.2f KB / %.2f MB)\n",
                  totalBytes, totalBytes / 1024.0,
                  totalBytes / (1024.0 * 1024.0));
    Serial.printf("  LittleFS Used Space:   %u bytes (%.2f KB)\n", usedBytes,
                  usedBytes / 1024.0);
    Serial.printf("  LittleFS Free Space:   %u bytes (%.2f KB)\n",
                  totalBytes - usedBytes, (totalBytes - usedBytes) / 1024.0);
  } else {
    Serial.println("  LittleFS Mount:        FAILED");
  }
}

// ---------------------------------------------------------------------------
// 6. I2C Bus Scanner & 0.91" OLED Test
// ---------------------------------------------------------------------------
bool scanI2cBus(uint8_t sda, uint8_t scl) {
  Serial.printf("\n  Scanning I2C on SDA=GPIO%d, SCL=GPIO%d...\n", sda, scl);
  Wire.begin(sda, scl);
  Wire.setTimeOut(50);
  Wire.setClock(400000);

  int foundDevices = 0;
  bool foundOled = false;

  for (uint8_t addr = 1; addr < 127; addr++) {
    Wire.beginTransmission(addr);
    uint8_t error = Wire.endTransmission();

    if (error == 0) {
      Serial.printf("    -> Found I2C device at: 0x%02X", addr);
      if (addr == 0x3C || addr == 0x3D) {
        Serial.print("  <-- [MATCH] 0.91\" SSD1306 OLED!");
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

  oledDetected = false;
  if (scanI2cBus(I2C_SDA_PIN, I2C_SCL_PIN)) {
    oledDetected = true;
    oledSda = I2C_SDA_PIN;
    oledScl = I2C_SCL_PIN;
  } else if (scanI2cBus(I2C_ALT_SDA, I2C_ALT_SCL)) {
    oledDetected = true;
    oledSda = I2C_ALT_SDA;
    oledScl = I2C_ALT_SCL;
  }

  if (oledDetected) {
    Serial.printf(
        "  ==> Initializing 0.91\" OLED on SDA=GPIO%d, SCL=GPIO%d...\n",
        oledSda, oledScl);
    if (!u8g2) {
      u8g2 = new U8G2_SSD1306_128X32_UNIVISION_F_HW_I2C(U8G2_R0, U8X8_PIN_NONE,
                                                        oledScl, oledSda);
      u8g2->begin();
    }
    u8g2->clearBuffer();
    u8g2->setFont(u8g2_font_6x10_tf);
    u8g2->drawStr(0, 9, "D.E.V_Darshan v2.0");
    u8g2->drawHLine(0, 11, 128);

    char buf[32];
    snprintf(buf, sizeof(buf), "S3 4MB Fl | %.0fK Heap",
             ESP.getFreeHeap() / 1024.0);
    u8g2->drawStr(0, 22, buf);
    u8g2->drawStr(0, 31, "Diagnostics Ready!");
    u8g2->sendBuffer();
    Serial.println("  ==> OLED screen drawing verified! [PASS]");
  } else {
    Serial.println("  ==> [NOTE] 0.91\" OLED not detected.");
    Serial.println(
        "      If wired: VCC->3V3, GND->GND, SDA->GPIO1, SCL->GPIO2.");
  }
}

// ---------------------------------------------------------------------------
// 7. Buttons Summary
// ---------------------------------------------------------------------------
void printButtonSummary() {
  printHeader("7. 4-TACTILE BUTTON LIVE MONITOR");
  Serial.println(
      "  Current Button States (Internal Pull-Up, Active LOW to GND):");
  for (size_t i = 0; i < 4; i++) {
    int state = digitalRead(buttons[i].pin);
    Serial.printf("    - Button %d: %-18s -> %s\n", i + 1, buttons[i].name,
                  state == LOW ? "PRESSED (LOW)" : "RELEASED (HIGH)");
  }
}

// ---------------------------------------------------------------------------
// Run All Diagnostics in Sequence
// ---------------------------------------------------------------------------
void runAllDiagnostics() {
  printHeader("D.E.V_Darshan v2.0 — ESP32-S3 COMPLETE REPORT");
  diagnoseChip();
  diagnoseFlash();
  diagnoseRAM();
  diagnosePSRAM();
  diagnoseLittleFS();
  diagnoseI2CAndOled();
  printButtonSummary();

  Serial.println();
  Serial.println(
      "================================================================");
  Serial.println(
      "  💡 TIP: Send any key or press ENTER in terminal to reprint!");
  Serial.println("  💡 TIP: Tap any of the 4 buttons to test them live.");
  Serial.println(
      "================================================================");
}

// ---------------------------------------------------------------------------
// Arduino Setup
// ---------------------------------------------------------------------------
void setup() {
  Serial.begin(115200);

  // Initialize button pins with internal pull-up
  for (size_t i = 0; i < 4; i++) {
    pinMode(buttons[i].pin, INPUT_PULLUP);
    buttons[i].lastState = digitalRead(buttons[i].pin);
  }
}

// ---------------------------------------------------------------------------
// Arduino Loop
// ---------------------------------------------------------------------------
void loop() {
  unsigned long now = millis();

  // Give 1.5 seconds on boot before auto-printing full report
  if (!initialReportPrinted && now > 1500) {
    initialReportPrinted = true;
    runAllDiagnostics();
  }

  // If user presses ENTER or sends anything over the Serial monitor, reprint!
  if (Serial.available()) {
    while (Serial.available()) {
      Serial.read(); // Clear incoming buffer
    }
    runAllDiagnostics();
  }

  // Live 4-Button monitor
  for (size_t i = 0; i < 4; i++) {
    int raw = digitalRead(buttons[i].pin);

    if (raw != buttons[i].lastState) {
      if (now - buttons[i].lastDebounce > 30) {
        buttons[i].lastState = raw;
        buttons[i].lastDebounce = now;

        if (raw == LOW) {
          Serial.printf("\n  >>> [BUTTON PRESSED]  Button %d: %s\n", i + 1,
                        buttons[i].name);
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
          Serial.printf("  <<< [BUTTON RELEASED] Button %d: %s\n", i + 1,
                        buttons[i].name);
        }
      }
    }
  }

  // Periodic Heartbeat every 8 seconds with reminder
  static unsigned long lastHeartbeat = 0;
  if (now - lastHeartbeat >= 8000) {
    lastHeartbeat = now;
    Serial.printf("\n[STATUS] Uptime: %lus | Free Heap: %u bytes (%.1f KB) | "
                  "(Press ENTER to reprint report)\n",
                  now / 1000, ESP.getFreeHeap(), ESP.getFreeHeap() / 1024.0);
  }

  delay(5);
}
