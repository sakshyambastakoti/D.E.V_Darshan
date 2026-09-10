# 💾 D.E.V_Darshan v2.0 — Flash Partitioning, Storage & Wireless OTA Guide

> **Hardware**: ESP32-S3 Super Mini (ESP32-S3FH4R2)  
> **Total Flash**: 4.00 MB (4,194,304 bytes — DIO Mode @ 80 MHz)  
> **Active Architecture**: Dual-Bank Wireless OTA + 1.38 MB LittleFS Storage  

---

## 🗺️ 1. Complete 4MB Flash Memory Map

Your board uses the verified **`default.csv` 4MB partition table**. The 4,194,304 bytes of Flash are partitioned into distinct, isolated zones:

```text
0x000000 ┌────────────────────────────────────────────────────────┐
         │ Bootloader & System Header (~36 KB)                    │
0x009000 ├────────────────────────────────────────────────────────┤
         │ NVS (Non-Volatile Storage — Wi-Fi settings) (20 KB)    │
0x00E000 ├────────────────────────────────────────────────────────┤
         │ OTA Data (Boot pointer & rollback state) (8 KB)        │
0x010000 ├────────────────────────────────────────────────────────┤
         │                                                        │
         │ App Slot 0 (Active Firmware Binary)                    │
         │ Capacity: 1.25 MB (1,310,720 bytes)                    │
         │ Current Firmware Usage: ~410 KB (~31% used)            │
         │                                                        │
0x150000 ├────────────────────────────────────────────────────────┤
         │                                                        │
         │ App Slot 1 (Over-The-Air Update Target)                │
         │ Capacity: 1.25 MB (1,310,720 bytes)                    │
         │ Standby for Wireless Firmware Updates                  │
         │                                                        │
0x290000 ├────────────────────────────────────────────────────────┤
         │                                                        │
         │ LittleFS Partition (Document Storage)                  │
         │ Capacity: 1.38 MB (1,441,792 bytes)                    │
         │ Dedicated to .txt Notes, Books & Formulas              │
         │                                                        │
0x3F0000 └────────────────────────────────────────────────────────┘
```

---

## 📋 2. Partition Table Specification

| Partition Name | Type | Subtype | Memory Offset | Allocated Size | Purpose & Contents |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **`nvs`** | Data | `nvs` | `0x009000` | **20 KB** (`0x005000`) | Saved Wi-Fi AP settings, last read position, brightness |
| **`otadata`** | Data | `ota` | `0x00E000` | **8 KB** (`0x002000`) | Flags indicating which app slot (`app0` or `app1`) to boot |
| **`app0`** | App | `ota_0` | `0x010000` | **1.25 MB** (`0x140000`)| Currently running D.E.V_Darshan C++ firmware |
| **`app1`** | App | `ota_1` | `0x150000` | **1.25 MB** (`0x140000`)| Backup/Staging slot for new firmware updates |
| **`spiffs` (LittleFS)**| Data | `spiffs`| `0x290000` | **1.38 MB** (`0x160000`)| User text files, notes, formula books |

---

## 🛡️ 3. How the Dual-Slot OTA Update System Works

Having two 1.25 MB application slots (`app0` and `app1`) provides **foolproof brick-protection**:

```text
 1. Normal Running:
    ESP32-S3 boots and runs from [App Slot 0].

 2. You initiate Wireless OTA update from your phone browser:
    New firmware is streamed over Wi-Fi and written into [App Slot 1].
    (If Wi-Fi disconnects or power dies midway, [App Slot 0] is untouched!)

 3. Verification & Reboot:
    The bootloader verifies the cryptographic checksum in [App Slot 1].
    If valid, the 'otadata' pointer is flipped to boot [App Slot 1].

 4. Automatic Rollback Protection:
    If the new firmware crashes upon boot, the ESP32 automatically 
    rolls back to [App Slot 0] safely.
```

---

## 📚 4. LittleFS Document Storage: What 1.38 MB Means in Practice

Because plain text (`.txt`) uses only 1 byte per character, **1.38 MB (1,441,792 bytes)** offers immense storage capacity:

### Real-World Document Capacity:
* **Academic Formula Cheat-Sheet** (500 lines of equations & steps): **~12 KB**
* **Detailed Subject Summary** (10 dense pages of text): **~35 KB**
* **Full Chapter of a Textbook** (30 pages): **~90 KB**
* **Complete English Novel** (*The Great Gatsby*): **~290 KB**

### 📦 Storage Equivalents:
* **~50 to 70 separate detailed subject notes / cheat-sheets**, OR
* **Over 1,440,000 characters** of readable text.
* To read 1.38 MB of text line-by-line on a 0.91" OLED screen would take **over 80 hours of non-stop reading**!

---

## 🔄 5. Document Uploads vs. Firmware Updates

| Feature | What It Does | How You Access It | Affects LittleFS Storage? |
| :--- | :--- | :--- | :--- |
| **Wireless Document Upload** | Uploads or deletes `.txt` files | Private Web Portal on your phone/PC browser | Stored inside the **1.38 MB LittleFS partition** |
| **Wireless Firmware OTA** | Updates the C++ system code (new features, UI changes) | Web Portal -> `/update` page | Written into the **1.25 MB App Slot** (Documents stay 100% safe!) |
| **USB-C Direct Upload** | Fast local flashing or serial debugging | VS Code / PlatformIO via USB-C cable | Writes to active App slot |

---

## ⚙️ 6. PlatformIO Configuration Locking

Your [`v2/platformio.ini`](file:///d:/D.E.V_Darshan/v2/platformio.ini) is configured to build and upload with this exact partition scheme:

```ini
[env:esp32s3_supermini]
platform = espressif32
board = esp32-s3-devkitc-1
framework = arduino
monitor_speed = 115200

; Confirmed 4MB Flash DIO + default.csv Dual-Slot OTA layout
board_upload.flash_size = 4MB
board_build.partitions = default.csv
board_build.flash_mode = dio
board_build.f_flash = 80000000L
board_build.arduino.memory_type = dio_qspi

; Native USB-C CDC + PSRAM enabled
build_flags =
    -D ARDUINO_USB_MODE=1
    -D ARDUINO_USB_CDC_ON_BOOT=1
    -D BOARD_HAS_PSRAM
    -D CORE_DEBUG_LEVEL=1

; Filesystem
board_build.filesystem = littlefs
```
