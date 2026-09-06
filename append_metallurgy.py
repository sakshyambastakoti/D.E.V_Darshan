import os

with open("d:/D.E.V_Darshan/chemistry_solutions_oled/metallurgy_oled.txt", "r", encoding="utf-8") as f:
    metallurgy_content = f.read()

with open("d:/D.E.V_Darshan/math_topicwise_solutions_oled/chemsitry_solutions_oled.txt", "a", encoding="utf-8") as f:
    f.write("\n\n" + metallurgy_content)

with open("d:/D.E.V_Darshan/chemistry_solutions_oled/chemistry_full_solutions_oled.txt", "a", encoding="utf-8") as f:
    f.write("\n\n" + metallurgy_content)

print("Appended metallurgy content to all OLED files.")
