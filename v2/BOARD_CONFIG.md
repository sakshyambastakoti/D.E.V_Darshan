# 📋 ESP32-S3 Super Mini — Confirmed Hardware Profile & Architecture Guide

> **Hardware Audit Date**: September 2026  
> **Diagnostic Firmware**: D.E.V_Darshan v2.0 Hardware Probe  
> **Status**: Verified & Confirmed Active

---

## 🎯 Verified Board Identity: **ESP32-S3FH4R2**

Your board is the high-tier **ESP32-S3FH4R2** revision of the Super Mini, featuring **embedded 4MB Flash and 2MB Quad-SPI PSRAM**.

```
                           ESP32-S3 Super Mini
                            ┌──────────────┐
                     5V/VBUS│ [ ]      [ ] │GPIO 7  ──> BTN 4: BACK / PANIC
                         GND│ [ ]      [ ] │GPIO 6  ──> BTN 3: SELECT / ENTER
                        3V3 │ [ ]  ══  [ ] │GPIO 5  ──> BTN 2: DOWN
I2C SDA ──>           GPIO 1│ [ ]  USB [ ] │GPIO 4  ──> BTN 1: UP
I2C SCL ──>           GPIO 2│ [ ]      [ ] │GPIO 3
                      GPIO 8│ [ ]      [ ] │GPIO 10
                      GPIO 9│ [ ]      [ ] │GPIO 11
                            └──────────────┘
```

---

## 📊 Complete Hardware Specifications

| Component | Verified Specification | Details & Impact on D.E.V_Darshan v2 |
| :--- | :--- | :--- |
| **Microcontroller** | **ESP32-S3 (Xtensa LX7)** | Dual-core 32-bit @ **240 MHz**, Revision v2 |
| **Flash Memory** | **4.00 MB** (4,194,304 bytes) | High-speed **DIO mode @ 80 MHz** (JEDEC ID: `0x464016`) |
| **External PSRAM** | **2.00 MB** (2,097,152 bytes) | **ACTIVE & Usable!** Enables caching entire books in RAM |
| **Internal SRAM** | **378.22 KB** Total / **338.6 KB Free** | Massive headroom; zero risk of heap exhaustion during Web Portal use |
| **Total Usable RAM** | **~2.43 MB Total RAM** | 346 KB Internal SRAM + 2,094 KB High-Speed PSRAM |
| **Storage (LittleFS)**| **1.38 MB** (1,441,792 bytes) | Reliable onboard flash storage (holds hundreds of `.txt` documents) |
| **Wireless** | **Wi-Fi 2.4 GHz + BLE 5.0** | High-throughput web portal + potential BLE ring/remote control |
| **Native USB** | **On-chip USB-C CDC / JTAG** | Direct flashing, serial monitoring, and USB Mass Storage |

---

## 🔌 Hardware Wiring & Pin Mapping

### 1. 0.91" I2C OLED Display (128×32 SSD1306)

| OLED Pin | ESP32-S3 Super Mini Pin | Notes |
| :--- | :--- | :--- |
| **VCC** | **3V3** (Pin 3) | 3.3V Logic & Power |
| **GND** | **GND** (Pin 2) | Common Ground |
| **SDA** | **GPIO 1** | Primary Hardware I2C SDA (400 kHz) |
| **SCL** | **GPIO 2** | Primary Hardware I2C SCL (400 kHz) |

> *Tip: If your display module is ever rewired to GPIO 8/9, the firmware automatically scans and supports it.*

### 2. 4-Tactile Button Navigation

All buttons connect directly between the GPIO pin and **GND**.  
**Zero external resistors needed** — the firmware enables internal `INPUT_PULLUP`.

| Button | GPIO Pin | Function in Reading Mode | Function in Menu Mode |
| :--- | :--- | :--- | :--- |
| **BTN 1 (UP)** | **GPIO 4** | Scroll Up / Previous Line | Move cursor Up |
| **BTN 2 (DOWN)** | **GPIO 5** | Scroll Down / Next Line | Move cursor Down |
| **BTN 3 (SELECT)** | **GPIO 6** | Page Forward / Bookmark | Open File / Select Option |
| **BTN 4 (BACK / PANIC)**| **GPIO 7** | **Instant Panic Screen** (Blank/Fake Calc) | Return to File List / Parent Menu |

---

## 🚀 Architectural Advantages for D.E.V_Darshan v2

### 1. 2 MB PSRAM Document Caching (Zero-Lag Paging)
* In v1 (ESP32-CAM), reading from SD card caused micro-stutters and consumed battery power.
* In v2, when you open a `.txt` file from LittleFS, the entire file (even a 500 KB book) is loaded directly into the **2 MB PSRAM buffer**.
* Result: **Instantaneous, zero-latency paging** and line scrolling, with flash memory powered down most of the time to save battery!

### 2. Dual-Core Task Splitting
* **Core 1**: Dedicated to the reading loop, button debouncing (<5ms latency), and U8g2 OLED rendering.
* **Core 0**: Handles the background Wi-Fi Web Portal during file uploads. The UI never freezes or stutters when uploading files!

### 3. Dedicated Stealth / Panic Button (GPIO 7)
* A single press of Button 4 immediately blanks the OLED screen or switches to a realistic fake calculator error screen (`"Syntax ERROR"` or `"Math ERROR"`), ensuring complete discretion.

---

## ⚙️ Locked-In PlatformIO Configuration

This exact configuration in [`v2/platformio.ini`](file:///d:/D.E.V_Darshan/v2/platformio.ini) matches your verified hardware:

```ini
[platformio]
default_envs = esp32s3_supermini

[env:esp32s3_supermini]
platform = espressif32
board = esp32-s3-devkitc-1
framework = arduino
monitor_speed = 115200

; Confirmed Hardware: 4MB Flash DIO + 2MB Quad-SPI PSRAM
board_upload.flash_size = 4MB
board_build.partitions = default.csv
board_build.flash_mode = dio
board_build.f_flash = 80000000L
board_build.arduino.memory_type = dio_qspi

; Native USB-C CDC + PSRAM Flags
build_flags =
    -D ARDUINO_USB_MODE=1
    -D ARDUINO_USB_CDC_ON_BOOT=1
    -D BOARD_HAS_PSRAM
    -D CORE_DEBUG_LEVEL=1

; Filesystem Configuration
board_build.filesystem = littlefs

; Libraries
lib_deps =
    olikraus/U8g2 @ ^2.35.19
```
