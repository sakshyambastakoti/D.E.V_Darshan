/*
 * ============================================================================
 *  D.E.V_Darshan — Simple v1 OLED Text Display
 * ============================================================================
 *  Exact v1 U8g2 display code running on ESP32-S3 Super Mini
 *
 *  Hardware:
 *    OLED SDA -> GPIO 1
 *    OLED SCL -> GPIO 2
 *    BTN 1    -> GPIO 4 (Optional: Tap to switch between v1 screens)
 * ============================================================================
 */

#include <Arduino.h>
#include <Wire.h>
#include <U8g2lib.h>

#define PIN_SDA   1
#define PIN_SCL   2
#define PIN_BTN   4

// Exact v1 U8g2 display instance
static U8G2_SSD1306_128X32_UNIVISION_F_HW_I2C u8g2(U8G2_R0, U8X8_PIN_NONE);

static int screenIndex = 0;

// ── Screen 1: Exact v1 Reading Mode (4 Lines, TomThumb 4x6) ──
void showScreen1() {
    u8g2.clearBuffer();
    u8g2.setFont(u8g2_font_tom_thumb_4x6_mr);
    u8g2.drawStr(0, 7,  "Photosynthesis is a");
    u8g2.drawStr(0, 15, "process plants use to");
    u8g2.drawStr(0, 23, "convert sunlight into");
    u8g2.drawStr(0, 31, "chemical energy (ATP).");
    u8g2.sendBuffer();
    Serial.println("Showing: Screen 1 (v1 Reading Mode - TomThumb)");
}

// ── Screen 2: Exact v1 Menu Mode (4 Lines, 5x7 Font) ──
void showScreen2() {
    u8g2.clearBuffer();
    u8g2.setFont(u8g2_font_5x7_mr);
    u8g2.drawStr(0, 7,  "> 1. Physics.txt");
    u8g2.drawStr(0, 15, "  2. Calculus.txt");
    u8g2.drawStr(0, 23, "  3. Chemistry.txt");
    u8g2.drawStr(0, 31, "  4. Settings");
    u8g2.sendBuffer();
    Serial.println("Showing: Screen 2 (v1 Menu Mode - 5x7)");
}

// ── Screen 3: Exact v1 Boot Screen (6x10 & 5x7) ──
void showScreen3() {
    u8g2.clearBuffer();

    // Line 1: 6x10 font
    u8g2.setFont(u8g2_font_6x10_mr);
    int w1 = u8g2.getStrWidth("D.E.V_Darshan");
    u8g2.drawStr((128 - w1) / 2, 11, "D.E.V_Darshan");

    // Line 2: 5x7 font
    u8g2.setFont(u8g2_font_5x7_mr);
    int w2 = u8g2.getStrWidth("v.1.0");
    u8g2.drawStr((128 - w2) / 2, 21, "v.1.0");

    // Line 3: 5x7 font
    int w3 = u8g2.getStrWidth("Dev: Sakshyam");
    u8g2.drawStr((128 - w3) / 2, 31, "Dev: Sakshyam");

    u8g2.sendBuffer();
    Serial.println("Showing: Screen 3 (v1 Boot Screen)");
}

void setup() {
    Serial.begin(115200);
    pinMode(PIN_BTN, INPUT_PULLUP);

    delay(300);
    Serial.println("\n--- Simple v1 OLED Text Display ---");

    // Initialize I2C on ESP32-S3 Super Mini
    Wire.begin(PIN_SDA, PIN_SCL);
    Wire.setClock(400000);

    // Exact v1 display startup sequence
    u8g2.begin();
    u8g2.setBusClock(400000);
    u8g2.setContrast(180);
    u8g2.enableUTF8Print();

    // Show initial reading screen
    showScreen1();
}

void loop() {
    // Tap BTN 1 (GPIO 4) to switch between screens
    static bool lastState = HIGH;
    int state = digitalRead(PIN_BTN);

    if (state != lastState) {
        delay(30); // debounce
        lastState = state;

        if (state == LOW) {
            screenIndex = (screenIndex + 1) % 3;
            if (screenIndex == 0) showScreen1();
            else if (screenIndex == 1) showScreen2();
            else if (screenIndex == 2) showScreen3();
        }
    }

    // You can also send '1', '2', or '3' in Serial Monitor
    if (Serial.available()) {
        char c = Serial.read();
        if (c == '1') { screenIndex = 0; showScreen1(); }
        else if (c == '2') { screenIndex = 1; showScreen2(); }
        else if (c == '3') { screenIndex = 2; showScreen3(); }
    }

    delay(10);
}
