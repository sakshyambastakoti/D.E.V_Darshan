# 🔋 D.E.V_Darshan v2.0 — Battery, Charging & Power Optimization Guide

> **Hardware**: ESP32-S3 Super Mini (ESP32-S3FH4R2)  
> **Display**: 0.91" 128×32 I2C OLED (SSD1306)  
> **Storage**: 2MB High-Speed PSRAM Cache + 1.38MB LittleFS  

---

## ⚡ 1. The Onboard Lithium Charging System

Your ESP32-S3 Super Mini features a **built-in single-cell (1S) 3.7V Lithium-Polymer / Lithium-Ion charging circuit**. You do not need any external charging boards (like the TP4056).

```text
              BACK SIDE OF ESP32-S3 SUPER MINI
         ┌────────────────────────────────────────┐
         │                                        │
         │      [ B+ ]                 [ B- ]     │
         │    (Battery+)             (Battery-)   │
         │         │                      │       │
         │         ▼                      ▼       │
         │    [Red Wire]            [Black Wire]  │
         │                                        │
         │             [ BOOST Jumper ]           │
         │             [●]  [●] (Unbridged: 100mA)│
         │             [══════] (Bridged:   300mA)│
         └────────────────────────────────────────┘
```

### How It Works:
1. **USB-C Dual Role**:
   * When plugged into USB-C, the board powers the ESP32-S3 and simultaneously charges the connected LiPo battery.
   * When unplugged from USB-C, the board automatically transitions to battery power with **zero reboot or interruption**.
2. **Onboard Battery Status LED**:
   * Near the top right of the board, an indicator LED illuminates during active charging and turns off / changes color when full (4.20V cut-off).
3. **The `BOOST` Solder Jumper (Crucial Safety Rule!)**:
   * **Default (Unbridged — Recommended)**: Charging current is capped at **100 mA**.
     - Safe for **any battery size** (even small 100mAh–300mAh cells).
     - Standard 1C charge rate for small batteries prevents overheating and swelling.
   * **Bridged (`BOOST` mode)**: Charging current increases to **300 mA**.
     - ⚠️ **ONLY bridge this jumper if your battery capacity is 500 mAh or larger!**
     - Charging a 150mAh or 200mAh battery at 300mA (2C rate) can damage the battery or cause dangerous thermal runaway.

---

## 📦 2. Recommended Batteries for D.E.V_Darshan

To fit inside a scientific calculator (like the Casio fx-991ES, fx-991EX, fx-82MS) or small stealth enclosure, you need a **1S 3.7V Lithium Polymer (LiPo) pouch cell**.

> 💡 **Understanding LiPo Part Numbers**:  
> LiPo model numbers represent dimensions in millimeters: `[Thickness] [Width] [Length]`  
> *Example*: `402030` = **4.0 mm thick**, **20 mm wide**, **30 mm long**.

### Top Recommended Battery Models:

| Model | Dimensions (T × W × L) | Capacity | Fitment / Where to Place | Continuous Reading Life |
| :--- | :--- | :--- | :--- | :--- |
| **402030P** *(400mAh High-Density)* | **4.0 × 20 × 30 mm** | **400 mAh** | **Ideal stealth fit**; certified BIS R-41202096 with built-in PCM | **~13.1 Hours** *(See [402030P Report](BATTERY_402030P_POWER_REPORT.md))* |
| **402030** *(Standard)* | **4.0 × 20 × 30 mm** | **180 – 220 mAh** | Fits perfectly inside standard AAA battery bay or hollowed calculator space | **~7 to 8.5 Hours** |
| **502030** | **5.0 × 20 × 30 mm** | **250 – 300 mAh** | Slightly thicker; fits inside Casio fx-991EX with minor internal rib trimming | **~10 to 12 Hours** |
| **302030** *(Ultra-Thin)* | **3.0 × 20 × 30 mm** | **120 – 150 mAh** | Ultra slim; fits in the tightest calculator shells with zero bulging | **~5 to 6 Hours** |
| **603040** *(Max Endurance)*| **6.0 × 30 × 40 mm** | **600 – 700 mAh** | Large capacity; requires removing internal calculator battery brackets | **~24 to 28 Hours** |

### ⚠️ Mandatory Battery Requirement: Built-in PCM
Always buy LiPo cells labeled with **PCM / Protection Circuit Board** (a small green PCB wrapped under the yellow Kapton tape at the top of the battery). This protects against:
* **Over-discharge** (< 2.8V cutoff)
* **Over-charge** (> 4.25V cutoff)
* **Short-circuit** protection

---

## 📊 3. Power Consumption Breakdown (D.E.V_Darshan v2)

Because D.E.V_Darshan v2 reads files from **2MB PSRAM** rather than an SD card and turns off Wi-Fi during reading, its power draw is dramatically lower than v1:

| Operating Mode | CPU Clock | Wi-Fi State | OLED State | Current Draw @ 3.7V |
| :--- | :--- | :--- | :--- | :--- |
| **Active Reading Mode** | **80 MHz** (Downclocked) | **OFF** | **ON** (~25% pixels lit) | **~24 – 28 mA** |
| **Auto-Dimmed Reading** | **80 MHz** | **OFF** | **Dimmed (10% brightness)** | **~18 – 20 mA** |
| **Light Sleep (Standby)** | CPU Paused | **OFF** | **OFF** (Display sleeping) | **~1.2 – 1.8 mA** |
| **Deep Sleep** | Powered down | **OFF** | **OFF** | **~20 – 35 µA** |
| **Wi-Fi Web Portal (Upload)**| **240 MHz** | **ON** (AP Mode) | **ON** | **~115 – 140 mA** |

---

## ⏱️ 4. Battery Life & Charging Time Estimations

Calculated using real-world efficiency (85% usable battery capacity):

| Battery Capacity | Reading Mode Life (Continuous) | Standby Time (Light Sleep) | Charge Time (Default 100mA) | Charge Time (Boost 300mA) |
| :--- | :--- | :--- | :--- | :--- |
| **150 mAh** (302030) | **5.5 Hours** | ~4 Days | ~1.6 Hours | ❌ Do Not Use Boost |
| **200 mAh** (402030) | **7.5 Hours** | ~6 Days | ~2.2 Hours | ❌ Do Not Use Boost |
| **300 mAh** (502030) | **11.5 Hours** | ~9 Days | ~3.3 Hours | ❌ Do Not Use Boost |
| **400 mAh** (402030P) | **13.1 Hours** | **~9.5 Days** | **~4.8 Hours** | **~1.7 Hours** (Safe at 0.75C) |
| **500 mAh** (503040) | **19.0 Hours** | ~15 Days | ~5.5 Hours | **~1.9 Hours** (Bridged) |
| **700 mAh** (603040) | **26.5 Hours** | ~22 Days | ~7.8 Hours | **~2.6 Hours** (Bridged) |

> 💡 **Typical Student / Daily Usage**:  
> If you read for **1.5 hours per day**, a standard **200 mAh battery** will last **5 full days** on a single charge!

---

## 🪛 5. Stealth Power Switch Options

To prevent the battery from slowly draining when not in use for weeks, install a power cutoff switch on the positive wire:

```text
    LiPo Battery (+) ──────>[ Switch ]──────> B+ Pad on ESP32-S3
    LiPo Battery (-) ───────────────────────> B- Pad on ESP32-S3
```

### Option A: Magnetic Reed Switch (100% Invisible / Stealth)
* Solder a tiny glass reed switch inside the calculator shell.
* To turn the device ON/OFF, simply pass a small magnet (e.g. inside an eraser or pen cap) over that specific spot on the calculator case.
* **Advantage**: Zero visible external switches or holes!

### Option B: Micro Slide Switch
* Mount a miniature 3-pin SPDT slide switch along the seam or battery cover notch of the calculator.

### Option C: Calculator Key Integration
* Tap into the calculator's existing physical ON button using an ultra-low-power latching MOSFET circuit.

---

## 🧠 6. Firmware Power Optimizations in D.E.V_Darshan v2

Our v2 firmware includes several automated power-saving techniques:

1. **PSRAM In-Memory Execution**:
   - The document is loaded into the **2 MB PSRAM** once upon opening.
   - The Flash memory and SPI bus stay asleep during reading, saving up to **15 mA** compared to continuous SD card reads.
2. **Dynamic CPU Frequency Scaling (DFS)**:
   - When in **Reading Mode**, CPU drops from 240 MHz to **80 MHz** (plenty fast for smooth 60fps text scrolling, cutting CPU power in half).
   - When entering **Wi-Fi Portal Mode**, CPU automatically scales up to **240 MHz** for maximum web transfer speed.
3. **Smart OLED Auto-Dim & Sleep**:
   - **After 30 seconds** of button inactivity: Display dims by 50%.
   - **After 3 minutes**: Display turns completely off and enters Light Sleep.
   - **Any Button Press**: Wakes the display instantly (< 5ms).
