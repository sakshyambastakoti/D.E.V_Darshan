# D.E.V_Darshan v2.0 — ESP32-S3 Super Mini Edition

Welcome to **D.E.V_Darshan v2.0**. This edition upgrades the hardware foundation from the legacy ESP32-CAM to the **ESP32-S3 Super Mini**, featuring:
- **Ultra-compact form factor** (~22.5mm × 18mm)
- **Native USB-C CDC / JTAG** (plug-and-play flashing & serial output)
- **0.91" I2C OLED Display (128×32 SSD1306)**
- **4 Tactile Buttons** (UP, DOWN, SELECT, BACK/PANIC)
- **Onboard LittleFS Storage** (eliminates bulky/noisy SD cards)

---

## 📚 Technical Documentation Index

All in-depth hardware, electrical, battery, and storage guides are organized in the [`v2/docs/`](docs/) directory:

| Document | Description |
| :--- | :--- |
| 📋 [**Hardware Configuration & Specs**](docs/BOARD_CONFIG.md) | Verified ESP32-S3FH4R2 chip specs, 2MB PSRAM, 4MB Flash, and locked settings |
| 🔌 [**Circuit Schematic & Pin Mapping**](docs/CIRCUIT_PINOUT.md) | 1:1 physical board diagram, 0.91" OLED wiring, 4-button cluster, and B+/B- pads |
| 🔋 [**Battery, Charging & Power Guide**](docs/BATTERY_AND_POWER_GUIDE.md) | Recommended 3.7V LiPo models, onboard charging, BOOST jumper, and battery life calculations |
| 💾 [**Storage, LittleFS & OTA Guide**](docs/STORAGE_AND_OTA_GUIDE.md) | 4MB partition map, 1.38MB text storage capacity, and dual-slot wireless OTA mechanics |

---

## ⚡ Method 1: Instant 5-Second Hardware Probe (No Compiling Required)

If you have your ESP32-S3 Super Mini plugged into your computer via USB-C, you can instantly query its exact Flash size and chip model using `esptool`:

```powershell
python -m esptool flash_id
```

### What to look for in the output:
- **`Chip is ESP32-S3...`**: Confirms model and chip revision.
- **`Manufacturer / Device`**: Identifies the onboard flash brand (Winbond, GigaDevice, etc.).
- **`Detected flash size: X MB`**: Shows whether you have **4MB, 8MB, or 16MB** flash!

---

## 🛠️ Method 2: Comprehensive Hardware Diagnostics Firmware

We have created an interactive diagnostic sketch inside `v2/src/main.cpp`. It runs a complete hardware health check:
1. **CPU & Silicon Check**: Clock speed (240MHz), cores, silicon feature flags, and internal chip temperature.
2. **Flash Memory**: Real JEDEC ID, configured size, SPI mode (QIO), and bus speed (80MHz).
3. **Internal SRAM**: Total heap, free heap, minimum heap recorded, and largest contiguous allocatable block.
4. **PSRAM (External RAM) Probe**: Checks if eFuse embedded PSRAM is present and verifies `psramFound()`.
5. **LittleFS Filesystem**: Formats/mounts internal flash storage and displays total & usable space.
6. **I2C Bus Scanner**: Scans GPIO 1/2 and GPIO 8/9 to find the 0.91" OLED display (`0x3C`) and draws a diagnostic test card on it.
7. **4-Button Interactive Tester**: Monitors GPIO 4, 5, 6, and 7. When you press any tactile button, it logs the event in real-time and flashes feedback onto the OLED!

### How to Flash with PlatformIO:
```powershell
# From the project root:
& "$HOME\.platformio\penv\Scripts\platformio.exe" run -d v2 -t upload

# Open the serial monitor:
& "$HOME\.platformio\penv\Scripts\platformio.exe" device monitor -b 115200
```

---

## 🔌 Hardware Wiring Diagram

```
                 ESP32-S3 Super Mini
                  ┌──────────────┐
           5V/VBUS│ [ ]      [ ] │GPIO 7  ──> BTN 4: BACK / PANIC (to GND)
               GND│ [ ]      [ ] │GPIO 6  ──> BTN 3: SELECT       (to GND)
              3V3 │ [ ]  ══  [ ] │GPIO 5  ──> BTN 2: DOWN         (to GND)
OLED SDA ──> GPIO 1│ [ ]  USB [ ] │GPIO 4  ──> BTN 1: UP           (to GND)
OLED SCL ──> GPIO 2│ [ ]      [ ] │GPIO 3
            GPIO 8│ [ ]      [ ] │GPIO 10
            GPIO 9│ [ ]      [ ] │GPIO 11
                  └──────────────┘
```

> **Zero External Resistors Required**:
> - All buttons use the ESP32-S3 internal pull-ups (`INPUT_PULLUP`). Wire each button directly between the GPIO pin and any **GND** pin.
> - The 0.91" OLED VCC goes to `3V3`, GND to `GND`, SDA to `GPIO 1`, SCL to `GPIO 2`.

---

## 📦 GitHub Release & Versioning Strategy

To keep both versions organized and clear for your users and portfolio:

### 1. Tag v1.0.0 (ESP32-CAM Edition)
Before publishing v2 changes, tag the original working code:
```bash
git tag -a v1.0.0 -m "Release v1.0.0: Stable ESP32-CAM Edition with SD_MMC and Web Portal"
git push origin v1.0.0
```

### 2. Side-by-Side Coexistence (`src/` vs `v2/`)
By having `v2/` as a dedicated subfolder with its own `platformio.ini`, anyone can build either:
- **v1.0 (ESP32-CAM)**: Uses root `src/` and root `platformio.ini`.
- **v2.0 (ESP32-S3 Super Mini)**: Uses `v2/` independently.

### 3. Create a GitHub Release
On GitHub, draft a release:
- **Tag**: `v1.0.0`
- **Title**: `v1.0.0 - ESP32-CAM Scientific Calculator Edition`
- Keep `main` branch progressing towards `v2.0-beta`.
