import os
import textwrap

os.makedirs("d:/D.E.V_Darshan/chemistry_solutions_oled", exist_ok=True)
os.makedirs("d:/D.E.V_Darshan/math_topicwise_solutions_oled", exist_ok=True)

raw_text = r"""================================
     CHEMISTRY CORE CONCEPTS
      OLED MASTER COMPLIANCE
================================

--------------------------------
 1. NORMALITY VS MOLARITY
--------------------------------

RELATIONSHIP:
Normality (N) = Molarity (M) * n

DERIVATION:
Molarity (M) = (w / M.wt) / V(L)
Normality (N) = (w / E.wt) / V(L)

We know: E.wt = M.wt / n
(Where n = n-factor: acidity,
basicity, or change in ox. state)

Substituting E.wt in Normality:
N = [w / (M.wt / n)] / V(L)
N = n * [(w / M.wt) / V(L)]
N = M * n

EXAMPLES:
- For H2SO4 (n = 2): N = 2 * M
- For HCl (n = 1): N = 1 * M
- For NaOH (n = 1): N = 1 * M
- For H3PO4 (n = 3): N = 3 * M


--------------------------------
 2. NORMALITY EQUATION
--------------------------------

STATEMENT:
N1 * V1 = N2 * V2

DERIVATION:
By Law of Chemical Equivalence,
during neutralization:
g-eq of Acid = g-eq of Base

g-eq of Acid = (N1 * V1) / 1000
g-eq of Base = (N2 * V2) / 1000

Equating both sides:
(N1 * V1)/1000 = (N2 * V2)/1000
=> N1 * V1 = N2 * V2


--------------------------------
 3. REDOX TITRATION
--------------------------------

DEFINITION:
Volumetric titration based on a
redox (reduction-oxidation)
reaction between analyte and
titrant.

EXAMPLE:
Oxalic acid (H2C2O4) vs KMnO4
in acidic medium (H2SO4):

2 KMnO4 + 3 H2SO4 + 5 H2C2O4
-> K2SO4 + 2 MnSO4 + 8 H2O +
   10 CO2^

Oxidation: C (+3) -> C (+4)
Reduction: Mn (+7) -> Mn (+2)


--------------------------------
 4. EQUIVALENCE VS END POINT
--------------------------------

EQUIVALENCE POINT:
- Theoretical point where
  stoichiometrically equivalent
  amounts of reactants react.
- Exact stoichiometric stage.

END POINT:
- Practical point where indicator
  changes color.
- Signals completion of titration.


--------------------------------
 5. PRIMARY VS SECONDARY STANDARD
--------------------------------

PRIMARY STANDARD SOLUTION:
- Prepared by direct weighing.
- Pure (>99.9%), stable in air.
- Non-hygroscopic, non-reactive.
- Examples: Oxalic acid,
  Anhydrous Na2CO3.

SECONDARY STANDARD SOLUTION:
- Cannot be prepared by direct
  weighing.
- Hygroscopic, unstable in air.
- Standardized against primary.
- Examples: NaOH, HCl, KMnO4.


--------------------------------
 6. ATOMIC WT, EQ WT & VALENCY
--------------------------------

RELATIONSHIP:
Equivalent Weight (E) =
Atomic Weight (A) / Valency (v)

DERIVATION:
By definition, Equivalent Weight
is mass combining with 1 g-atom
of Hydrogen (or 1 equivalent).

1 mole of element = A grams.
1 mole combines with v g-atoms of
Hydrogen (v equivalents).

Mass for v equivalents = A grams
Mass for 1 equivalent = A / v

Therefore: E = A / v


--------------------------------
 7. BLUE VITRIOL (CuSO4.5H2O)
--------------------------------

PREPARATION:
1. 2 Cu + 2 H2SO4 + O2
   -> 2 CuSO4 + 2 H2O
2. CuO + H2SO4 -> CuSO4 + H2O
3. CuCO3 + H2SO4
   -> CuSO4 + CO2^ + H2O

ACTION OF HEAT:
100°C: CuSO4.5H2O -> CuSO4.H2O
230°C: CuSO4.H2O -> CuSO4 (white)
750°C: 2 CuSO4 -> 2 CuO (black)
       + 2 SO2^ + O2^

REACTIONS:
- With NaOH: Cu(OH)2 pale blue ppt
- With excess NH3: [Cu(NH3)4]SO4
  deep blue solution
- With KI: Cu2I2 white ppt + I2


--------------------------------
 8. BESSEMERIZATION & SMELTING
--------------------------------

A) COPPER BESSEMERIZATION:
FeS oxidation & slag formation:
2 FeS + 3 O2 -> 2 FeO + 2 SO2^
FeO + SiO2 -> FeSiO3 (Slag)

Cu2S partial oxidation:
2 Cu2S + 3 O2 -> 2 Cu2O + 2 SO2^

Self-Reduction:
2 Cu2O + Cu2S -> 6 Cu + SO2^
(Yields Blister Copper ~98% pure)

B) IRON SMELTING (BLAST FURNACE):
Combustion: C + O2 -> CO2
Fusion: CO2 + C -> 2 CO
Slag Formation:
CaCO3 -> CaO + CO2^
CaO + SiO2 -> CaSiO3 (Slag)
Reduction:
3 Fe2O3 + CO -> 2 Fe3O4 + CO2^
Fe3O4 + CO -> 3 FeO + CO2^
FeO + CO -> Fe + CO2^
"""

def main():
    lines = raw_text.split("\n")
    output_lines = []
    for l in lines:
        l_str = l.strip("\r")
        if len(l_str) <= 32:
            output_lines.append(l_str)
        else:
            wrapped = textwrap.wrap(l_str, width=32, break_long_words=True, break_on_hyphens=False)
            output_lines.extend(wrapped)
            
    final_text = "\n".join(output_lines)
    errs = sum(1 for line in output_lines if len(line) > 32)
    print(f"Total lines: {len(output_lines)}, Errors >32: {errs}, Max line length: {max(len(l) for l in output_lines)}")
    
    file1 = "d:/D.E.V_Darshan/chemistry_solutions_oled/chemistry_core_topics_oled.txt"
    file2 = "d:/D.E.V_Darshan/math_topicwise_solutions_oled/chemsitry_solutions_oled.txt"
    
    with open(file1, "w", encoding="utf-8") as f:
        f.write(final_text)
        
    with open(file2, "a", encoding="utf-8") as f:
        f.write("\n\n" + final_text)
        
    print(f"Saved to {file1} and appended to {file2}")

if __name__ == "__main__":
    main()
