# 🔌 D.E.V_Darshan v2.0 — Circuit Schematic & Pin Mapping Guide

> **Target Hardware**: ESP32-S3 Super Mini (ESP32-S3FH4R2 — 4MB Flash, 2MB PSRAM)  
> **Display**: 0.91" 128×32 I2C OLED (SSD1306)  
> **Inputs**: 4× Tactile Push Buttons (Active LOW)  
> **Design Philosophy**: Zero External Resistors • 100% Boot-Safe • Ultra-Compact

---

## 🗺️ Master Wiring Schematic (ASCII Diagram)

```text
                               ESP32-S3 Super Mini
                                ┌─────────────────┐
                       [5V/VBUS]│ [1]         [16]│[GPIO 7]  ───┐
                         [ GND ]│ [2]         [15]│[GPIO 6]  ───┼──────────┐
                         [ 3V3 ]│ [3]    USB  [14]│[GPIO 5]  ───┼────────┐ │
       ┌───────────────> [GPIO 1]│ [4]    ══   [13]│[GPIO 4]  ───┼──────┐ │ │
       │ ┌─────────────> [GPIO 2]│ [5]        [12]│[GPIO 3]     │      │ │ │
       │ │               [GPIO 3]│ [6]        [11]│[GPIO 10]    │      │ │ │
       │ │               [GPIO 4]│ [7]        [10]│[GPIO 11]    │      │ │ │
       │ │                      └─────────────────┘             │      │ │ │
       │ │                                                      │      │ │ │
       │ │   0.91" I2C OLED                                     │      │ │ │
       │ │  ┌───────────────┐                                   │      │ │ │
3V3 ───┼─┼──┤ VCC           │                                   │      │ │ │
GND ───┼─┼──┤ GND           │                                   │      │ │ │
SDA ───┘ │  ┤ SDA           │                                   │      │ │ │
SCL ─────┘  ┤ SCL           │                                   │      │ │ │
            └───────────────┘                                   │      │ │ │
                                                                │      │ │ │
     4× Tactile Buttons (Active LOW, Internal Pull-Up)          │      │ │ │
     ┌──────────────────────────────────────────────────────────┘      │ │ │
     │   BTN 1: UP              [Pin] ─── (Button) ───┐                │ │ │
     └────────────────────────────────────────────────┼────────────────┘ │ │
         BTN 2: DOWN            [Pin] ─── (Button) ───┤                  │ │
     ┌────────────────────────────────────────────────┼──────────────────┘ │
     │   BTN 3: SELECT / ENTER  [Pin] ─── (Button) ───┤                    │
     └────────────────────────────────────────────────┼────────────────────┘
         BTN 4: BACK / PANIC    [Pin] ─── (Button) ───┤
                                                      │
                       COMMON GROUND (GND) ───────────┴──> ESP32 GND (Pin 2)
```

---

## 📋 Comprehensive Pin Assignment Table

| Component | Pin Label | ESP32-S3 Pin | Header Pin # | Logic / Signal | Boot Safety Status | Function & Description |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **0.91" OLED** | **VCC** | **3V3** | Pin 3 (Left) | 3.3V Power | Safe | Powers the SSD1306 display driver |
| **0.91" OLED** | **GND** | **GND** | Pin 2 (Left) | Common Ground | Safe | System Ground |
| **0.91" OLED** | **SDA** | **GPIO 1** | Pin 4 (Left) | I2C Data (400kHz) | Safe (Non-strapping) | Serial Data line with internal pull-up |
| **0.91" OLED** | **SCL** | **GPIO 2** | Pin 5 (Left) | I2C Clock (400kHz) | Safe (Non-strapping) | Serial Clock line with internal pull-up |
| **Button 1** | **UP** | **GPIO 4** | Pin 7 (Left) | `INPUT_PULLUP` | Safe (Non-strapping) | Scroll Up / Previous Line / Menu Up |
| **Button 2** | **DOWN** | **GPIO 5** | Pin 14 (Right)| `INPUT_PULLUP` | Safe (Non-strapping) | Scroll Down / Next Line / Menu Down |
| **Button 3** | **SELECT** | **GPIO 6** | Pin 15 (Right)| `INPUT_PULLUP` | Safe (Non-strapping) | Open File / Confirm / Page Forward |
| **Button 4** | **BACK/PANIC**| **GPIO 7** | Pin 16 (Right)| `INPUT_PULLUP` | Safe (Non-strapping) | Back to Folder / **Emergency Cloak** |

---

## 🎯 Why This Pinout is Structurally "Perfect"

### 1. Clustered OLED Connections (No Crossed Wires)
Notice that the OLED requires 4 wires: `3V3`, `GND`, `SDA`, and `SCL`.
On the ESP32-S3 Super Mini, these 4 pins sit **directly next to each other** in sequence:
```
Pin 2: GND
Pin 3: 3V3
Pin 4: GPIO 1 (SDA)
Pin 5: GPIO 2 (SCL)
```
You can use a tidy, straight 4-wire ribbon cable directly from the microcontroller to the display without any wire crossovers or spaghetti routing!

### 2. 100% Zero-Boot-Conflict Guarantee
* On the legacy ESP32-CAM (v1), `GPIO 0` and `GPIO 12` were boot-strapping pins. If you turned on the device while accidentally pressing a button, the chip would freeze or enter download mode.
* On the ESP32-S3 Super Mini:
  * **GPIO 0** (Boot strapping) is **left completely untouched**.
  * **GPIO 4, 5, 6, 7** are pure general-purpose IOs with **zero boot strapping roles**.
  * You can hold down all 4 buttons while switching the device on, and it will still boot normally every single time!

### 3. Zero External Resistors Needed
* Every button uses the internal pull-up resistor built into the ESP32-S3 silicon (`pinMode(pin, INPUT_PULLUP)`).
* When a button is not pressed, the pin reads `HIGH` (3.3V).
* When a button is pressed, it shorts to `GND` and reads `LOW` (0V).
* No pull-up or pull-down resistors are needed on your breadboard or perfboard.

---

## ⚡ Power Supply & Battery Integration

### Power Requirements:
* **Operating Voltage**: 3.3V (Logic level)
* **USB Input**: 5.0V (regulated by onboard LDO to 3.3V)
* **Current Draw**:
  * **Reading Mode (OLED ON, Wi-Fi OFF)**: ~25–35 mA
  * **Auto-Dim / Standby Mode**: ~8–12 mA
  * **Wi-Fi Portal Mode (Uploading Files)**: ~110–140 mA (bursts up to 200mA)

### Power Connection Options:

#### Option A: Bench Testing / Direct USB-C
Simply plug in a standard USB-C cable. The onboard regulator provides stable 3.3V to the chip and OLED.

#### Option B: 3.7V LiPo Battery (Recommended for Stealth Calculator Builds)
```text
  [ 3.7V LiPo Battery ]
     (+) Positive ────> [ Slide Switch / Magnetic Reed Switch ] ────> 5V / VBUS (Pin 1)
     (-) Negative ──────────────────────────────────────────────────> GND (Pin 2)
```
* Connecting the 3.7V LiPo to the **5V/VBUS** pin utilizes the onboard low-dropout (LDO) regulator to deliver a clean, protected 3.3V rail.
* A tiny 150mAh to 300mAh 1S LiPo battery provides **6 to 10 hours of continuous reading time**!

---

## 🪛 Step-by-Step Soldering & Assembly Checklist

1. **Prepare Common Ground**:
   * Solder a black wire from `GND` (Pin 2) to one leg of each of the 4 tactile buttons in a daisy-chain.
2. **Connect OLED Display**:
   * `VCC` -> `3V3` (Pin 3)
   * `GND` -> `GND` (Pin 2)
   * `SDA` -> `GPIO 1` (Pin 4)
   * `SCL` -> `GPIO 2` (Pin 5)
3. **Connect the 4 Control Buttons**:
   * Other leg of Button 1 (UP) -> `GPIO 4`
   * Other leg of Button 2 (DOWN) -> `GPIO 5`
   * Other leg of Button 3 (SELECT) -> `GPIO 6`
   * Other leg of Button 4 (BACK/PANIC) -> `GPIO 7`
4. **Validation Test**:
   * Plug in USB-C and open the PlatformIO Serial Monitor:
     ```powershell
     & "$HOME\.platformio\penv\Scripts\platformio.exe" device monitor -b 115200
     ```
   * Tap each button: You should see live `[BUTTON PRESSED]` events for buttons 1, 2, 3, and 4!
   * The 0.91" OLED will immediately display the `"Diagnostics Ready!"` screen at address `0x3C`.

---

## 🕶️ Stealth Calculator Enclosure Recommendations

If mounting inside a Casio or similar scientific calculator:
1. **OLED Placement**: Mount the 0.91" OLED behind the solar cell window or in the top margin of the primary LCD compartment.
2. **Polarizing Film**: Cover the OLED with a sheet of tinted polarizing film or dark neutral-density gel to make the screen invisible until illuminated.
3. **Button Placement**:
   - Tap into unused calculator rubber dome contacts, OR
   - Mount miniature SMD tactile switches along the side seams of the calculator casing.
4. **Panic Mode**: GPIO 7 is mapped to Button 4. In the v2 firmware, double-tapping Button 4 instantly triggers a fake calculator error screen (`"Syntax ERROR"`) or shuts the display completely black within 20 milliseconds.
