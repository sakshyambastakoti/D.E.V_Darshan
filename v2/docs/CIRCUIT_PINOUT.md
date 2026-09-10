# 🔌 D.E.V_Darshan v2.0 — Verified Circuit Schematic & Pin Mapping

> **Hardware Target**: ESP32-S3 Super Mini (Verified Layout from Manufacturer Diagram)  
> **Silicon**: ESP32-S3FH4R2 (4MB Flash, 2MB PSRAM, Onboard LiPo Charger)  
> **Display**: 0.91" 128×32 I2C OLED (SSD1306)  
> **Controls**: 4× Tactile Push Buttons (Active LOW)  

---

## 🗺️ 1:1 Physical Board Pinout & Master Schematic

Based on your exact manufacturer pinout diagram:

```text
                               USB-C PORT (Top)
                               ┌──────────────┐
                    [TX/GP43] [│]            [│] [ 5V ]          <── BATTERY LED
                    [RX/GP44] [│]            [│] [ GND ]         <── Common Ground
    OLED SDA ─────> [  GP1  ] [│]            [│] [3V3(OUT)]      <── OLED VCC (3.3V)
    OLED SCL ─────> [  GP2  ] [│]   ESP32-S3 [│] [ GP13 ]
                    [  GP3  ] [│]   Super    [│] [ GP12 ]
    BTN 1: UP ────> [  GP4  ] [│]    Mini    [│] [ GP11 ]
    BTN 2: DOWN ──> [  GP5  ] [│]            [│] [ GP10 ]
    BTN 3: SELECT > [  GP6  ] [│]            [│] [ GP9  ]
    BTN 4: PANIC ─> [  GP7  ] [│]            [│] [ GP8  ]
                               └──────────────┘
                                [BOOT]  [RESET]
                                (Left)  (Right)

    ────────────────────────── BOTTOM (BACK SIDE) ──────────────────────────
                       [ B+ ]                 [ B- ]       [ BOOST Jumper ]
                     (Battery+)             (Battery-)   (Default: 100mA charge)
                                                         (Bridge for: 300mA)
```

---

## 📋 Exact Component Wiring Table

### 1. 0.91" I2C OLED Display (128×32 SSD1306)

| OLED Pin | ESP32-S3 Super Mini Pin | Header Position | Function / Details |
| :--- | :--- | :--- | :--- |
| **VCC** | **3V3 (OUT)** | **Pin 3 on RIGHT header** | Clean 3.3V power output from onboard LDO |
| **GND** | **GND** | **Pin 2 on RIGHT header** | System ground |
| **SDA** | **GP1** | **Pin 3 on LEFT header** | Hardware I2C Data line (400 kHz Fast Mode) |
| **SCL** | **GP2** | **Pin 4 on LEFT header** | Hardware I2C Clock line (400 kHz Fast Mode) |

---

### 2. 4-Tactile Button Navigation (Consecutive Cluster)

Notice that **GP4, GP5, GP6, and GP7** sit directly next to each other at the bottom of the **LEFT header**.  
All buttons are **Active LOW** using internal pull-ups (`INPUT_PULLUP`). **Zero external resistors needed.**

```text
   LEFT HEADER                                   COMMON GND
   ┌─────────┐
   │ GP4 [●] ├──────── ( Button 1: UP ) ─────────────┐
   │ GP5 [●] ├──────── ( Button 2: DOWN ) ───────────┤
   │ GP6 [●] ├──────── ( Button 3: SELECT ) ─────────┼──> GND (Right Pin 2)
   │ GP7 [●] ├──────── ( Button 4: BACK/PANIC ) ─────┘
   └─────────┘
```

| Button | ESP32-S3 Pin | Header Position | Reading Mode Action | Menu Mode Action | Boot Safety |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **BTN 1 (UP)** | **GP4** | Pin 6 (Left) | Previous Line / Fast Scroll Up | Move Selection Up | ✅ 100% Boot Safe |
| **BTN 2 (DOWN)** | **GP5** | Pin 7 (Left) | Next Line / Fast Scroll Down | Move Selection Down | ✅ 100% Boot Safe |
| **BTN 3 (SELECT)** | **GP6** | Pin 8 (Left) | Page Forward / Bookmark | Open File / Confirm | ✅ 100% Boot Safe |
| **BTN 4 (BACK/PANIC)**| **GP7** | Pin 9 (Left) | **Emergency Cloak / Blank Screen** | Return to Previous Menu | ✅ 100% Boot Safe |

---

## 🔋 Onboard Lithium Battery Charger (Built-in Feature!)

Your board has an **integrated battery charging controller** with solder pads on the back side:

```text
        [ B+ ]                       [ B- ]
     (Battery +)                  (Battery -)
          │                            │
          ▼                            ▼
   [ + Red Wire ]               [ - Black Wire ]
   ┌───────────────────────────────────────────┐
   │       3.7V Rechargeable LiPo Battery      │
   │           (e.g., 150mAh - 500mAh)         │
   └───────────────────────────────────────────┘
```

### Key Advantages for D.E.V_Darshan:
1. **No External TP4056 Module Needed**: Solder your 3.7V LiPo directly to the `B+` and `B-` solder pads on the back.
2. **Automatic USB-C Charging**: Whenever you plug the device into USB-C, it powers the system and charges the LiPo battery automatically.
3. **Charge Status LED**: The board has an onboard `BATTERY LED` near the top-right corner.
4. **BOOST Solder Jumper**:
   - **Default (Unbridged)**: 100 mA charge current (ideal & safe for small 100mAh–400mAh batteries).
   - **Bridged**: 300 mA charge current (only for batteries > 500mAh).

---

## 💡 Onboard WS2812 RGB LED (GP48)

* Your board includes an addressable **WS2812 RGB LED on GP48**.
* **In D.E.V_Darshan v2**:
  - We keep this LED **turned OFF** by default during normal operation to maintain complete stealth inside the calculator and conserve battery.
  - Can be configured to emit a subtle, dim flash (e.g. faint blue) only when Wi-Fi Web Portal mode is actively enabled.

---

## 🛡️ Why This Pinout is 100% Boot-Safe

* **GPIO 0 (BOOT Button)**: Stays on the board's tactile button, untouched by external wiring.
* **GP4, GP5, GP6, GP7**: Have zero strapping dependencies. Even if you press or hold any button while turning on the power, the ESP32-S3 will **never** hang, enter bootloader mode, or brick.
* **Internal Pull-Ups**: The ESP32-S3 enables internal ~45kΩ pull-up resistors on GP4–GP7, ensuring clean, noise-free button presses without external resistors.

---

## 🛠️ Step-by-Step Soldering Sequence

1. **OLED Harness (4 Wires)**:
   - Solder `3V3` and `GND` from the OLED to Pins 3 & 2 on the **Right** header.
   - Solder `SDA` and `SCL` from the OLED to `GP1` (Pin 3) & `GP2` (Pin 4) on the **Left** header.
2. **Button Ground Rail (Daisy Chain)**:
   - Solder a single ground wire to `GND` (Right Pin 2), then daisy-chain it to one leg of all 4 buttons.
3. **Button Signal Wires (4 Adjacent Left Pins)**:
   - Button 1 -> `GP4`
   - Button 2 -> `GP5`
   - Button 3 -> `GP6`
   - Button 4 -> `GP7`
4. **Battery (Optional for Portable Use)**:
   - Solder the LiPo battery (+) to `B+` and (-) to `B-` on the back side of the board.
   - Place a miniature slide switch or magnetic reed switch on the (+) wire to cut power when not in use.
