import os
import re
import textwrap

os.makedirs("d:/D.E.V_Darshan/chemistry_solutions_oled", exist_ok=True)
os.makedirs("d:/D.E.V_Darshan/chemistry_solutions_txt", exist_ok=True)

raw_text = r"""================================
      METALLURGY & COPPER/IRON
      OLED MASTER COMPLIANCE
================================

--------------------------------
 1. ROASTING VS CALCINATION
--------------------------------

ROASTING:
Heating concentrated ore strongly
in EXCESS OF AIR below its
melting point.
Mainly used for Sulphide Ores.

Reactions:
2 ZnS + 3 O2 -> 2 ZnO + 2 SO2^
2 CuFeS2 + O2 -> Cu2S + 2 FeS + SO2^

CALCINATION:
Heating concentrated ore in
ABSENCE OR LIMITED AIR below its
melting point.
Mainly used for Carbonate and
Hydrated Oxide Ores.

Reactions:
CaCO3 -> CaO + CO2^
Fe2O3.3H2O -> Fe2O3 + 3 H2O^
ZnCO3 -> ZnO + CO2^

KEY DIFFERENCES:
--------------------------------
Feature      Roasting  Calcination
--------------------------------
Air          Excess    Absent/Ltd
Ore Type     Sulphide  Carbonate/
                       Hydrated
Gas Evolved  SO2       CO2/H2O
--------------------------------


--------------------------------
 2. SMELTING PROCESS
--------------------------------

Smelting is the process of
extracting molten metal from its
roasted ore at high temperature
using a suitable reducing agent
(Coke/CO) and a flux.

Role of Flux & Slag:
Flux + Gangue -> Slag (Fusible)
Example:
CaO (Basic Flux) + SiO2 (Acidic Gangue)
-> CaSiO3 (Slag)


--------------------------------
 3. BESSEMERIZATION OF COPPER
--------------------------------

Bessemerization is the process of
converting copper matte (Cu2S + FeS)
into blister copper in a Bessemer
Converter.

Process Steps:
1. Molten copper matte mixed with
sand (SiO2) is poured into the
converter.
2. Hot air blast is blown through
tuyeres.

Chemical Reactions:
a) Removal of Iron (as slag):
2 FeS + 3 O2 -> 2 FeO + 2 SO2^
FeO + SiO2 -> FeSiO3 (Slag)

b) Partial Oxidation of Cu2S:
2 Cu2S + 3 O2 -> 2 Cu2O + 2 SO2^

c) Self-Reduction (Auto-Reduction):
2 Cu2O + Cu2S -> 6 Cu + SO2^

Blister Copper:
As molten copper cools, dissolved
SO2 gas escapes, creating blisters
on the surface. It is ~98% pure.


--------------------------------
 4. BESSEMER CONVERTER DIAGRAM
--------------------------------

+------------------------------+
|     BESSEMER CONVERTER       |
|    (For Copper Extraction)   |
+------------------------------+
|       \              /       |
|        \   MOUTH    /        |
|         \          /         |
|          |        |          |
|          |        |          |
|         /          \         |
|        / STEEL SHELL\        |
|       /   REFRACTORY \       |
|      /   BRICK LINING \      |
|     |  MOLTEN COPPER   |     |
|     |     MATTE        |     |
|  ===[TUYERES]  [TUYERES]===  |
|     +------------------+     |
|     |   AIR BLAST IN   |     |
+------------------------------+


--------------------------------
 5. BLUE VITRIOL (CuSO4.5H2O)
--------------------------------

A) PREPARATION:
1. From Copper Metal:
2 Cu + 2 H2SO4 + O2 -> 2 CuSO4 + 2 H2O
Or: Cu + 2 H2SO4(conc) -> CuSO4 + SO2 + 2 H2O

2. From Cupric Oxide (CuO):
CuO + H2SO4 (dil) -> CuSO4 + H2O

3. From Copper Carbonate:
CuCO3 + H2SO4 -> CuSO4 + CO2 + H2O

B) PROPERTIES:
- Blue triclinic crystals.
- Soluble in water.

C) CHEMICAL REACTIONS:
1. Heat Action:
100°C: CuSO4.5H2O -> CuSO4.H2O + 4 H2O
230°C: CuSO4.H2O -> CuSO4 (white) + H2O
750°C: 2 CuSO4 -> 2 CuO (black) + 2 SO2 + O2

2. With NaOH (Caustic Soda):
CuSO4 + 2 NaOH -> Cu(OH)2 (pale blue ppt) + Na2SO4

3. With Aqueous Ammonia (NH4OH):
Dropwise: 2 CuSO4 + 2 NH4OH -> Cu2(OH)2SO4 (pale blue ppt)
Excess: Cu(OH)2 + (NH4)2SO4 + 2 NH3 -> [Cu(NH3)4]SO4 (deep blue solution)

4. With Potassium Iodide (KI):
2 CuSO4 + 4 KI -> Cu2I2 (white ppt) + I2 (brown) + 2 K2SO4


--------------------------------
 6. SMELTING REDUCTION OF IRON
--------------------------------

Smelting of iron is carried out
in a Blast Furnace using charge:
Hematite (Fe2O3) : Coke (C) :
Limestone (CaCO3) in 8 : 4 : 1.


--------------------------------
 7. BLAST FURNACE DIAGRAM (IRON)
--------------------------------

+------------------------------+
|      IRON BLAST FURNACE      |
+------------------------------+
|     (ORE+COKE+LIMESTONE)     |
|              ||              |
|              \/              |
|        /------------\        |
|       /  REDUCTION   \ (400C)|
|      /     ZONE       \(700C)|
|     /------------------\     |
|    /   SLAG FORMATION   \(800C|
|   /        ZONE          \(100|
|  /------------------------\  |
| /       FUSION ZONE        \ |
|/----------------------------\|
|   COMBUSTION ZONE (1500-1600C|
|===TUYERE==          ==TUYERE=|
| (HOT AIR)            (HOT AIR|
|------------------------------|
| [SLAG OUT]     [PIG IRON OUT]|
+------------------------------+


--------------------------------
 8. ZONES IN BLAST FURNACE
--------------------------------

1. COMBUSTION ZONE (1500C-1600C):
Bottom region. Coke burns in hot
air blast:
C + O2 -> CO2 + Heat (Exothermic)

2. FUSION ZONE (1200C-1300C):
Above combustion zone. CO2 reacts
with red hot coke to form CO:
CO2 + C -> 2 CO (Endothermic)

3. SLAG FORMATION ZONE (800C-1000C):
Middle region. Limestone decomposes
and forms fusible slag:
CaCO3 -> CaO + CO2^
CaO + SiO2 -> CaSiO3 (Slag)

4. REDUCTION ZONE (400C-700C):
Top region. CO reduces iron oxide
step-wise to iron metal:
3 Fe2O3 + CO -> 2 Fe3O4 + CO2^
Fe3O4 + CO -> 3 FeO + CO2^
FeO + CO -> Fe + CO2^
"""

def main():
    lines = raw_text.split("\n")
    output_lines = []
    for l in lines:
        if len(l) <= 32:
            output_lines.append(l)
        else:
            wrapped = textwrap.wrap(l, width=32, break_long_words=True, break_on_hyphens=False)
            output_lines.extend(wrapped)
            
    final_text = "\n".join(output_lines)
    
    # Check max line length
    errs = sum(1 for line in output_lines if len(line) > 32)
    print(f"Total lines: {len(output_lines)}, Errors >32: {errs}, Max line length: {max(len(l) for l in output_lines)}")
    
    with open("d:/D.E.V_Darshan/chemistry_solutions_oled/metallurgy_oled.txt", "w", encoding="utf-8") as f:
        f.write(final_text)
    print("Saved to d:/D.E.V_Darshan/chemistry_solutions_oled/metallurgy_oled.txt")

if __name__ == "__main__":
    main()
