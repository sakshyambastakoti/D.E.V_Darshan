import os
import re
import textwrap

OLED_DIR = "d:/D.E.V_Darshan/math_solutions_oled"
os.makedirs(OLED_DIR, exist_ok=True)

def wrap_text(text, width=32, indent=""):
    """Wrap text to max width with optional indent."""
    lines = []
    for paragraph in text.split("\n"):
        stripped = paragraph.strip()
        if not stripped:
            lines.append("")
        elif set(stripped) == {'='} or set(stripped) == {'-'}:
            lines.append(stripped[0] * width)
        else:
            p_indent_len = len(paragraph) - len(paragraph.lstrip())
            total_indent = indent + (" " * min(p_indent_len, 4))
            avail_width = max(10, width - len(total_indent))
            
            wrapped = textwrap.wrap(
                stripped,
                width=avail_width,
                break_long_words=True,
                break_on_hyphens=False
            )
            for w in wrapped:
                lines.append(total_indent + w)
    return lines

def build_oled_set(set_title, group_a, group_b, group_c=None):
    output_lines = []
    
    output_lines.append("=" * 32)
    for h in textwrap.wrap(set_title.upper(), width=32):
        output_lines.append(h.center(32))
    output_lines.append("=" * 32)
    output_lines.append("")

    # GROUP A
    output_lines.append("-" * 32)
    output_lines.append("GROUP 'A' - MCQs [1 Mark Each]".center(32))
    output_lines.append("-" * 32)
    output_lines.append("")

    for q in group_a:
        q_num = q["num"]
        output_lines.append("=" * 32)
        output_lines.append(f"QUESTION {q_num} (1 Mark MCQ)".center(32))
        output_lines.append("=" * 32)
        output_lines.append("")
        
        output_lines.append("Question:")
        output_lines.extend(wrap_text(q["text"], 32, indent="  "))
        output_lines.append("")
        
        output_lines.append("Options:")
        for opt in q["options"]:
            output_lines.extend(wrap_text(opt, 32, indent="  "))
        output_lines.append("")

        output_lines.append("Solution:")
        output_lines.extend(wrap_text(q["solution"], 32, indent="  "))
        output_lines.append("")

        output_lines.append("--------------------------------")
        ans_line = f"CORRECT: {q['correct']}"
        for al in textwrap.wrap(ans_line, width=32):
            output_lines.append(al.center(32))
        output_lines.append("--------------------------------")
        output_lines.append("")
        
        output_lines.append("-" * 32)
        output_lines.append(f"[ END OF QUESTION {q_num} ]".center(32))
        output_lines.append("-" * 32)
        output_lines.append("")

    # GROUP B
    output_lines.append("=" * 32)
    output_lines.append("GROUP 'B' - DESCRIPTIVE".center(32))
    output_lines.append("=" * 32)
    output_lines.append("")

    for q in group_b:
        q_num = q["num"]
        q_marks = q["marks"]
        output_lines.append("=" * 32)
        hdr = f"QUESTION {q_num} ({q_marks})"
        for h in textwrap.wrap(hdr, width=32):
            output_lines.append(h.center(32))
        output_lines.append("=" * 32)
        output_lines.append("")

        output_lines.append("Question:")
        output_lines.extend(wrap_text(q["text"], 32, indent="  "))
        output_lines.append("")

        output_lines.append("Solution:")
        output_lines.extend(wrap_text(q["solution"], 32, indent="  "))
        output_lines.append("")

        output_lines.append("-" * 32)
        output_lines.append(f"[ END OF QUESTION {q_num} ]".center(32))
        output_lines.append("-" * 32)
        output_lines.append("")

    # GROUP C if any
    if group_c:
        output_lines.append("=" * 32)
        output_lines.append("GROUP 'C' - COMPREHENSIVE".center(32))
        output_lines.append("=" * 32)
        output_lines.append("")

        for q in group_c:
            q_num = q["num"]
            q_marks = q["marks"]
            output_lines.append("=" * 32)
            hdr = f"QUESTION {q_num} ({q_marks})"
            for h in textwrap.wrap(hdr, width=32):
                output_lines.append(h.center(32))
            output_lines.append("=" * 32)
            output_lines.append("")

            output_lines.append("Question:")
            output_lines.extend(wrap_text(q["text"], 32, indent="  "))
            output_lines.append("")

            output_lines.append("Solution:")
            output_lines.extend(wrap_text(q["solution"], 32, indent="  "))
            output_lines.append("")

            output_lines.append("-" * 32)
            output_lines.append(f"[ END OF QUESTION {q_num} ]".center(32))
            output_lines.append("-" * 32)
            output_lines.append("")

    full_text = "\n".join(output_lines)
    return re.sub(r"\n{3,}", "\n\n", full_text).strip() + "\n"

# --- DATA DEFINITIONS FOR ALL SETS ---

# SET A MORNING
set_a_morning_ga = [
    {
        "num": "1",
        "text": "If z = 1/(1 - i) then what is the argument of z?",
        "options": ["A) 45°", "B) 135°", "C) 225°", "D) 315°"],
        "solution": "z = (1+i)/[(1-i)(1+i)] = (1+i)/2 = 1/2 + i(1/2).\nBoth x = 1/2 > 0 and y = 1/2 > 0 (1st Quadrant).\ntan(theta) = (1/2)/(1/2) = 1 ==> theta = 45°.",
        "correct": "A) 45°"
    },
    {
        "num": "2",
        "text": "Which one of the following system is Inconsistent and Independent?",
        "options": [
            "A) 2x - y = 6, x - (1/2)y = 3",
            "B) 2x - y = 6, 4x - 2y = 5",
            "C) 2x - y = 6, 3x + 2y = 1",
            "D) 2x - y = 6, 4x - 2y = 12"
        ],
        "solution": "Inconsistent & Independent means parallel distinct lines (no solution): a1/a2 = b1/b2 != c1/c2.\nIn Option B: 2/4 = -1/-2 = 1/2, but 6/5 != 1/2.",
        "correct": "B) 2x - y = 6, 4x - 2y = 5"
    },
    {
        "num": "3",
        "text": "What is the derivative of sinh^(-1)(sqrt(x))?",
        "options": [
            "A) 1 / (1 + x^2)",
            "B) 1 / [2*sqrt(x)*sqrt(1+x)]",
            "C) 1 / (1 + x)",
            "D) 1 / sqrt(1 - x)"
        ],
        "solution": "d/dx[sinh^(-1)(sqrt(x))] = [1/sqrt(1+(sqrt(x))^2)] * d/dx(sqrt(x))\n= [1/sqrt(1+x)] * [1/(2*sqrt(x))]\n= 1 / [2*sqrt(x)*sqrt(1+x)].",
        "correct": "B) 1 / [2*sqrt(x)*sqrt(1+x)]"
    },
    {
        "num": "4",
        "text": "What is the value of 1 + |w| - |w^2|? (w is complex cube root of unity)",
        "options": ["A) 1", "B) 2", "C) 3", "D) 0"],
        "solution": "For complex cube roots of unity, |w| = 1 and |w^2| = 1.\n1 + |w| - |w^2| = 1 + 1 - 1 = 1.",
        "correct": "A) 1"
    },
    {
        "num": "5",
        "text": "Which one of the following is equal to lim (x->0) (1 + x + x^2 - e^x) / x^2?",
        "options": ["A) 1", "B) 0", "C) 1/2", "D) -1/2"],
        "solution": "Using e^x = 1 + x + x^2/2 + x^3/6 + ...\nlim (x->0) [1 + x + x^2 - (1 + x + x^2/2 + ...)] / x^2\n= lim (x->0) [(x^2/2 - x^3/6) / x^2] = 1/2.",
        "correct": "C) 1/2"
    }
]

set_a_morning_gb = [
    {
        "num": "6.a",
        "marks": "2 Marks",
        "text": "By using De-Moivre's Theorem, evaluate [-1/2 + i*sqrt(3)/2]^20.",
        "solution": "z = cos(2pi/3) + i sin(2pi/3).\nz^20 = cos(40pi/3) + i sin(40pi/3).\n40pi/3 = 13pi + pi/3 = 12pi + pi + pi/3.\ncos(13pi + pi/3) = -cos(pi/3) = -1/2.\nsin(13pi + pi/3) = -sin(pi/3) = -sqrt(3)/2.\nResult = -1/2 - i*sqrt(3)/2."
    },
    {
        "num": "6.b",
        "marks": "3 Marks",
        "text": "Under what condition is a system of linear equations in two variables consistent and independent? Justify your answer with an example.",
        "solution": "1. Condition: Has a unique solution, i.e., a1/a2 != b1/b2 (or D != 0).\n2. Geometric: Lines intersect at exactly one point.\n3. Example: 2x + y = 5 and x - y = 1. Ratios: 2/1 != 1/(-1). Unique solution (2, 1)."
    },
    {
        "num": "7.a",
        "marks": "2 Marks",
        "text": "Write one application of derivatives in evaluating limits. Justify your answer with a suitable example.",
        "solution": "1. Application: L'Hopital's Rule for 0/0 or inf/inf indeterminate forms.\n2. Example: lim (x->0) (sin x)/x [Form 0/0] = lim (x->0) (cos x)/1 = cos(0) = 1."
    },
    {
        "num": "7.b",
        "marks": "3 Marks",
        "text": "A ladder 10 metres long rests with one end against a vertical wall, the other on the floor. Lower end moves away from wall at 2 m/min. Find rate at which upper end falls when base is 6 m away.",
        "solution": "x^2 + y^2 = 100. Given dx/dt = 2 m/min, x = 6 m.\nWhen x = 6, y = sqrt(100 - 36) = 8 m.\nDifferentiating: 2x(dx/dt) + 2y(dy/dt) = 0.\n6(2) + 8(dy/dt) = 0 ==> dy/dt = -12/8 = -1.5 m/min.\nUpper end falls at 1.5 m/min."
    },
    {
        "num": "8",
        "marks": "5 Marks",
        "text": "Short Answer Questions (a to e):\na) If z = r(cos theta + i sin theta), arg(z^5)?\nb) What are elementary row operations?\nc) Derivative of cosech^(-1)(x)?\nd) Equation of tangent to y=f(x) at (x1, y1)?\ne) Condition for tangent parallel to X-axis?",
        "solution": "a) arg(z^5) = 5*theta = 5*arg(z).\nb) Row swap (Ri<->Rj), Scalar mult (Ri->kRi), Row add (Ri->Ri+kRj).\nc) -1 / [|x| * sqrt(1 + x^2)].\nd) y - y1 = f'(x1)*(x - x1).\ne) dy/dx = f'(x) = 0."
    },
    {
        "num": "9.a",
        "marks": "2 Marks",
        "text": "Test consistency of x - 2y = 5, 2x - 4y = 4 by Determinant method.",
        "solution": "D = (1)(-4) - (-2)(2) = 0.\nDx = (5)(-4) - (-2)(4) = -12 != 0.\nSince D = 0 and Dx != 0, the system has no solution (Inconsistent)."
    },
    {
        "num": "9.b",
        "marks": "3 Marks",
        "text": "In AX = B, if Det(A) = 0, what conclusion can be drawn from Inverse matrix method? Justify with example.",
        "solution": "1. Conclusion: A^(-1) = (1/Det(A))*adj(A) is undefined. Inverse method FAILS.\n2. Example: x + y = 2, 2x + 2y = 5. Det(A) = 2 - 2 = 0. Lines are parallel, no solution exists."
    },
    {
        "num": "10.a",
        "marks": "2 Marks",
        "text": "Find points in circle x^2 + y^2 = 16 at which tangents are parallel to X-axis.",
        "solution": "2x + 2y(dy/dx) = 0 ==> dy/dx = -x/y.\nFor tangent || X-axis: -x/y = 0 ==> x = 0.\nSubstituting x = 0: y^2 = 16 ==> y = +/- 4.\nPoints: (0, 4) and (0, -4)."
    },
    {
        "num": "10.b",
        "marks": "3 Marks",
        "text": "Find d/dx(y) when y = cosh(ln(x)/x).",
        "solution": "y = cosh(u) where u = ln(x)/x.\ndy/dx = sinh(ln(x)/x) * d/dx[ln(x)/x].\nd/dx[ln(x)/x] = (1 - ln(x)) / x^2.\ndy/dx = [(1 - ln(x))/x^2] * sinh(ln(x)/x)."
    },
    {
        "num": "11.a",
        "marks": "2 Marks",
        "text": "Use row-equivalent matrices to solve: x - 2y = 3, 3x - 5y = 8.",
        "solution": "Augmented [A|B]:\n[ 1 -2 | 3 ]\n[ 3 -5 | 8 ]\nR2 -> R2 - 3R1 ==> [ 0  1 | -1 ] ==> y = -1.\nR1 -> R1 + 2R2 ==> [ 1  0 |  1 ] ==> x = 1.\nSolution: x = 1, y = -1."
    },
    {
        "num": "11.b",
        "marks": "3 Marks",
        "text": "Solve z^4 - 1 = 0 by using De-Moivre's theorem.",
        "solution": "z^4 = cos(2k*pi) + i sin(2k*pi).\nz = cos(k*pi/2) + i sin(k*pi/2) for k = 0, 1, 2, 3.\nk=0: 1; k=1: i; k=2: -1; k=3: -i.\nRoots: 1, -1, i, -i."
    },
    {
        "num": "12.a",
        "marks": "2 Marks",
        "text": "If percentage error in edge of a cube is 1%, find error in volume.",
        "solution": "V = x^3 ==> ln V = 3 ln x.\ndV/V = 3 (dx/x).\nPercentage error in V = 3 * 1% = 3%."
    },
    {
        "num": "12.b",
        "marks": "3 Marks",
        "text": "Show that two curves x^3 - 3xy^2 + 2 = 0 and 3x^2y - y^3 = 2 cut at right angles.",
        "solution": "Curve 1: m1 = dy/dx = (x^2 - y^2)/(2xy).\nCurve 2: m2 = dy/dx = -2xy/(x^2 - y^2).\nm1 * m2 = [(x^2 - y^2)/(2xy)] * [-2xy/(x^2 - y^2)] = -1.\nProduct of slopes is -1 ==> cut orthogonally."
    }
]


# SET B MORNING
set_b_morning_ga = [
    {
        "num": "1",
        "text": "If z = (1 - sqrt(3))i then what is argument of z?",
        "options": ["A) 90°", "B) 270°", "C) 60°", "D) 30°"],
        "solution": "Since sqrt(3) > 1, coefficient (1 - sqrt(3)) < 0.\nz = -k*i where k > 0. Lie on negative Y-axis.\narg(z) = 270° (or -90°).",
        "correct": "B) 270°"
    },
    {
        "num": "2",
        "text": "Which one of the following system is inconsistent?",
        "options": [
            "A) x + 2y = 5, 2x - y = 7",
            "B) x + 2y = 5, 2x + 4y = 10",
            "C) 6x - 3y = 21, 2x - y = 7",
            "D) x + 2y = 5, 2x + 4y = 7"
        ],
        "solution": "Inconsistent means parallel lines (a1/a2 = b1/b2 != c1/c2).\nIn Option D: 1/2 = 2/4 = 1/2 != 5/7.",
        "correct": "D) x + 2y = 5, 2x + 4y = 7"
    },
    {
        "num": "3",
        "text": "What is derivative of tanh^(-1)(sqrt(x))?",
        "options": [
            "A) 1 / (1 - x^2)",
            "B) 1 / (1 - x)",
            "C) 1 / [2*sqrt(x)*(1 - x)]",
            "D) 1 / (1 + x)"
        ],
        "solution": "d/dx[tanh^(-1)(sqrt(x))] = [1/(1 - x)] * [1/(2*sqrt(x))]\n= 1 / [2*sqrt(x)*(1 - x)].",
        "correct": "C) 1 / [2*sqrt(x)*(1 - x)]"
    },
    {
        "num": "4",
        "text": "What is value of (1 + w - w^2)^4 + (1 - w + w^2)^4?",
        "options": ["A) 16", "B) -16", "C) 256", "D) 32"],
        "solution": "1 + w = -w^2 and 1 + w^2 = -w.\n(-2w^2)^4 + (-2w)^4 = 16*w^8 + 16*w^4\n= 16(w^2 + w) = 16(-1) = -16.",
        "correct": "B) -16"
    },
    {
        "num": "5",
        "text": "Which one of the following is equal to lim (x->0+) x * ln(sin x)?",
        "options": ["A) 1", "B) -1", "C) log_e 1", "D) e"],
        "solution": "lim (x->0+) ln(sin x)/(1/x) = lim (x->0+) (cot x)/(-1/x^2)\n= lim (x->0+) -x^2*cos x / sin x = (1) * 0 = 0.\nSince log_e 1 = 0.",
        "correct": "C) log_e 1"
    }
]

set_b_morning_gb = [
    {
        "num": "6",
        "marks": "5 Marks",
        "text": "Short Answer Questions (a to e):\na) Argument of z = sin theta + i cos theta?\nb) Define consistent system of linear equations.\nc) What are elementary row operations?\nd) Two matrix methods to solve linear system.\ne) Two properties of cube roots of unity.",
        "solution": "a) z = cos(pi/2 - theta) + i sin(pi/2 - theta) ==> arg(z) = pi/2 - theta.\nb) A system possessing at least one solution.\nc) Row swap, non-zero scalar mult, row addition.\nd) Inverse Matrix Method, Gauss-Jordan Method.\ne) 1 + w + w^2 = 0 and w^3 = 1."
    },
    {
        "num": "7",
        "marks": "5 Marks",
        "text": "Short Answer Questions (a to e):\na) Geometrical meaning of dy/dx at x = a?\nb) Derivative of tanh^(-1) x?\nc) Equation of normal to y = f(x) at (x1, y1)?\nd) Condition for tangent || Y-axis?\ne) Difference between dy and Delta y?",
        "solution": "a) Slope of tangent line at x = a.\nb) 1 / (1 - x^2) for |x| < 1.\nc) y - y1 = -1/f'(x1) * (x - x1).\nd) dy/dx -> infinity or dx/dy = 0.\ne) Delta y is exact change, dy is differential linear approximation."
    },
    {
        "num": "8.a",
        "marks": "2 Marks",
        "text": "Test consistency of x - 2y = 5, 2x + y = 4 by Determinant method.",
        "solution": "D = (1)(1) - (-2)(2) = 1 - (-4) = 5 != 0.\nSince D != 0, system has unique solution.\nConsistent and Independent."
    },
    {
        "num": "8.b",
        "marks": "3 Marks",
        "text": "In AX = B, if Det(A) = 0, conclusion from Inverse matrix method? Justify with example.",
        "solution": "1. Conclusion: A^(-1) does not exist. Method fails.\n2. Example: x + 2y = 3, 2x + 4y = 6. Det(A) = 4 - 4 = 0. Coincident lines (infinitely many solutions)."
    },
    {
        "num": "9.a",
        "marks": "2 Marks",
        "text": "Under what condition can L'Hopital's Rule be used? Justify.",
        "solution": "1. Condition: Indeterminate form 0/0 or inf/inf with differentiable functions.\n2. Justification: For non-indeterminate lim (x->1) (x+1)/(x+2) = 2/3, L'Hopital gives 1 (wrong)."
    },
    {
        "num": "9.b",
        "marks": "3 Marks",
        "text": "Write one application of polar form of complex number. Justify with example.",
        "solution": "1. Application: High powers/roots using De-Moivre's theorem.\n2. Example: (1 + i)^10 = (sqrt(2) e^(i pi/4))^10 = 32 e^(i 5pi/2) = 32i."
    },
    {
        "num": "10.a",
        "marks": "2 Marks",
        "text": "Find equation of normal to parabola x^2 = 8y at x = 4.",
        "solution": "At x = 4, y = 16/8 = 2. Point (4, 2).\n2x = 8 y' ==> y' = x/4.\nAt (4,2), tangent slope mt = 1 ==> normal slope mn = -1.\ny - 2 = -1(x - 4) ==> x + y = 6."
    },
    {
        "num": "10.b",
        "marks": "3 Marks",
        "text": "Find dy/dx when y = [sinh(x/a)]^(x^2).",
        "solution": "ln y = x^2 ln(sinh(x/a)).\n(1/y) y' = 2x ln(sinh(x/a)) + x^2 coth(x/a) (1/a).\ndy/dx = [sinh(x/a)]^(x^2) [2x ln(sinh(x/a)) + (x^2/a) coth(x/a)]."
    },
    {
        "num": "11.a",
        "marks": "2 Marks",
        "text": "Use row-equivalent matrices to solve: 9x - 2y = 5, 3x - 3y = 11.",
        "solution": "[ 9 -2 | 5 ]\n[ 3 -3 | 11 ]\nR1 -> R1 - 3R2 ==> [ 0  7 | -28 ] ==> y = -4.\nSub into R2: 3x - 3(-4) = 11 ==> 3x = -1 ==> x = -1/3.\nSolution: x = -1/3, y = -4."
    },
    {
        "num": "11.b",
        "marks": "3 Marks",
        "text": "If w is complex cube root of unity, show (p+qw+rw^2)/(pw^2+q+rw) + (p+qw+rw^2)/(pw+qw^2+r) = -1.",
        "solution": "Let N = p + qw + rw^2.\nD1 = w^2 N ==> N/D1 = 1/w^2 = w.\nD2 = w N ==> N/D2 = 1/w = w^2.\nTerm 1 + Term 2 = w + w^2 = -1."
    },
    {
        "num": "12.a",
        "marks": "2 Marks",
        "text": "Show equation of tangent to x^2/a^2 + y^2/b^2 = 2 at (a, b) is x/a + y/b = 2.",
        "solution": "dy/dx = -b^2 x / (a^2 y). At (a, b), slope m = -b/a.\ny - b = (-b/a)(x - a) ==> bx + ay = 2ab ==> x/a + y/b = 2."
    },
    {
        "num": "12.b",
        "marks": "3 Marks",
        "text": "Inverted conical tank: inflow 42 cm^3/sec, height 12 cm, top radius 6 cm. When depth h = 8 cm, rate of level rising?",
        "solution": "r/h = 6/12 = 1/2 ==> r = h/2.\nV = (pi/12) h^3 ==> dV/dt = (pi/4) h^2 (dh/dt).\n42 = (pi/4) (64) (dh/dt) ==> dh/dt = 42/(16pi) = 21/(8pi) cm/sec."
    }
]


# SET A DAY
set_a_day_ga = [
    {
        "num": "1",
        "text": "If w is complex cube root of unity, value of 1 + |w| + |w^2|?",
        "options": ["A) 0", "B) 1", "C) 2", "D) 3"],
        "solution": "|w| = 1 and |w^2| = 1.\n1 + 1 + 1 = 3.",
        "correct": "D) 3"
    },
    {
        "num": "2",
        "text": "The system x + 2y = 0 and -2x - 4y = 0 is:",
        "options": [
            "A) consistent and independent",
            "B) consistent and dependent",
            "C) inconsistent and independent",
            "D) inconsistent and dependent"
        ],
        "solution": "D = -4 - (-4) = 0. Equations are identical.\nInfinitely many solutions ==> Consistent and Dependent.",
        "correct": "B) consistent and dependent"
    },
    {
        "num": "3",
        "text": "If y = x^2 + 5x, x = 2 and Delta x = 0.1, value of Delta y?",
        "options": ["A) 0.9", "B) 0.91", "C) 0.09", "D) none of them"],
        "solution": "Delta y = f(2.1) - f(2) = (4.41 + 10.5) - (4 + 10) = 14.91 - 14 = 0.91.",
        "correct": "B) 0.91"
    },
    {
        "num": "4",
        "text": "Point where tangent to y = e^(2x) at (0, 1) meets X-axis?",
        "options": ["A) (0, 1)", "B) (-1/2, 0)", "C) (2, 0)", "D) (0, -1/2)"],
        "solution": "y' = 2 e^(2x). Slope m = 2. Tangent: y = 2x + 1.\nMeets X-axis when y = 0 ==> x = -1/2. Point (-1/2, 0).",
        "correct": "B) (-1/2, 0)"
    },
    {
        "num": "5",
        "text": "If y = tan(sinh x), then d/dx(y) is:",
        "options": [
            "A) cosh x",
            "B) sec^2(sinh x) cosh x",
            "C) tanh x",
            "D) sinh x"
        ],
        "solution": "d/dx[tan(sinh x)] = sec^2(sinh x) cosh x.",
        "correct": "B) sec^2(sinh x) cosh x"
    }
]

set_a_day_gb = [
    {
        "num": "6",
        "marks": "5 Marks",
        "text": "a) State De-Moivre's theorem.\nb) Use De-Moivre's theorem to find cube roots of unity.\nc) Discuss any two properties of cube roots of unity.",
        "solution": "a) (cos theta + i sin theta)^n = cos(n theta) + i sin(n theta).\nb) 1, -1/2 + i sqrt(3)/2 = w, -1/2 - i sqrt(3)/2 = w^2.\nc) 1 + w + w^2 = 0 and w^3 = 1."
    },
    {
        "num": "7.a",
        "marks": "2 Marks",
        "text": "Use Cramer's rule to solve 3x + 4/y = 10, 2x - 3/y = 1.",
        "solution": "Let u = 1/y. 3x + 4u = 10, 2x - 3u = 1.\nD = -9 - 8 = -17.\nDx = -30 - 4 = -34 ==> x = 2.\nDu = 3 - 20 = -17 ==> u = 1 ==> y = 1.\nSolution: x = 2, y = 1."
    },
    {
        "num": "7.b",
        "marks": "3 Marks",
        "text": "Find d/dx(y) when y = x^[cosh^2(x/a)].",
        "solution": "ln y = cosh^2(x/a) ln x.\n(1/y) y' = (1/a) sinh(2x/a) ln x + (1/x) cosh^2(x/a).\ndy/dx = x^[cosh^2(x/a)] [(1/a) sinh(2x/a) ln x + (1/x) cosh^2(x/a)]."
    },
    {
        "num": "8.a",
        "marks": "2 Marks",
        "text": "Evaluate using L'Hopital's rule: lim (x->1) [x/(x-1) - 1/ln x].",
        "solution": "lim (x->1) [x ln x - (x-1)] / [(x-1) ln x]  [Form 0/0].\n1st L'Hopital: lim (x->1) [ln x] / [ln x + 1 - 1/x]  [Form 0/0].\n2nd L'Hopital: lim (x->1) (1/x) / [1/x + 1/x^2] = 1/2."
    },
    {
        "num": "8.b",
        "marks": "3 Marks",
        "text": "Approximate increase in surface area of cube if edge increases from 10 to 10.01 cm. Percentage error?",
        "solution": "S = 6x^2, x = 10, dx = 0.01.\ndS = 12 x dx = 12(10)(0.01) = 1.2 cm^2.\nPercentage error = (dS/S) 100% = 2(dx/x) 100% = 0.2%."
    },
    {
        "num": "9.a",
        "marks": "3 Marks",
        "text": "If tangent to y^2 = a x^3 + b at (2,3) is y = 4x - 5, find a and b.",
        "solution": "Slope m = 4. 2y y' = 3a x^2 ==> y' = 3a x^2 / (2y).\nAt (2,3): 2a = 4 ==> a = 2.\n3^2 = 2(2^3) + b ==> 9 = 16 + b ==> b = -7."
    },
    {
        "num": "9.b",
        "marks": "2 Marks",
        "text": "Condition for L'Hopital's rule? Justify with example.",
        "solution": "1. Condition: 0/0 or inf/inf indeterminate form.\n2. Example: lim (x->0) (e^x - 1)/x [Form 0/0] = 1."
    },
    {
        "num": "10.a",
        "marks": "3 Marks",
        "text": "Conical tank radius 10 ft, height 24 ft. Outflow 20 ft^3/min. Depth rate when h = 16 ft?",
        "solution": "r = 5h/12. V = (25pi/432) h^3.\ndV/dt = (25pi/144) h^2 (dh/dt).\n-20 = (400pi/9) (dh/dt) ==> dh/dt = -9/(20pi) ft/min."
    },
    {
        "num": "10.b",
        "marks": "2 Marks",
        "text": "Balloon radius rate dr/dt = 10 cm/sec. Rate of surface area increase when r = 15 cm?",
        "solution": "S = 4pi r^2 ==> dS/dt = 8pi r (dr/dt) = 8pi(15)(10) = 1200pi cm^2/sec."
    },
    {
        "num": "11.a",
        "marks": "2 Marks",
        "text": "If alpha, beta are imaginary cube roots of unity, prove alpha^4 + beta^4 + 1/(alpha beta) = 0.",
        "solution": "alpha = w, beta = w^2.\nw^4 + w^8 + 1/(w^3) = w + w^2 + 1 = 0."
    },
    {
        "num": "11.b",
        "marks": "3 Marks",
        "text": "Condition for inconsistent and independent system? Example.",
        "solution": "1. Condition: a1/a2 = b1/b2 != c1/c2.\n2. Example: x + 2y = 4, 2x + 4y = 10 (parallel lines)."
    },
    {
        "num": "12",
        "marks": "5 Marks",
        "text": "Commodity business model: A, B, C transactions:\n3x + 5y - 4z = 600\n2x - 3y + z = 500\n-x + 4y + 6z = 1300\nFind unit prices by Determinant method.",
        "solution": "D = -151.\nDx = -45300 ==> x = 300.\nDy = -15100 ==> y = 100.\nDz = -30200 ==> z = 200.\nPrices: X = Rs. 300, Y = Rs. 100, Z = Rs. 200."
    }
]


# SET B DAY
set_b_day_ga = [
    {
        "num": "1",
        "text": "Value of w(1 - |w| + |w^2|)?",
        "options": ["A) w", "B) w^2", "C) 2w", "D) 0"],
        "solution": "|w| = 1, |w^2| = 1.\nw(1 - 1 + 1) = w.",
        "correct": "A) w"
    },
    {
        "num": "2",
        "text": "Inclination with X-axis of tangent of x^2 + y^2 = 9 at (0, -3)?",
        "options": ["A) 0", "B) pi/2", "C) pi/3", "D) pi/4"],
        "solution": "y' = -x/y = 0. tan(theta) = 0 ==> theta = 0.",
        "correct": "A) 0"
    },
    {
        "num": "3",
        "text": "Value of lim (x->0) ln(x^2) / cot(x^2)?",
        "options": ["A) 0", "B) 1", "C) infinity", "D) -infinity"],
        "solution": "Form [-inf / inf]. L'Hopital gives lim -sin^2(x^2)/x^2 = 0.",
        "correct": "A) 0"
    },
    {
        "num": "4",
        "text": "System x - y + 2 = 0 and y + x = 3 is:",
        "options": [
            "A) consistent and independent",
            "B) inconsistent and independent",
            "C) consistent and dependent",
            "D) inconsistent and dependent"
        ],
        "solution": "D = 2 != 0. Unique solution (1/2, 5/2) ==> Consistent and Independent.",
        "correct": "A) consistent and independent"
    },
    {
        "num": "5",
        "text": "If y = tanh^(-1)(sin x), value of d/dx(y)?",
        "options": ["A) sec x", "B) tan x", "C) cos x", "D) sin x"],
        "solution": "cos x / (1 - sin^2 x) = cos x / cos^2 x = sec x.",
        "correct": "A) sec x"
    }
]

set_b_day_gb = [
    {
        "num": "1",
        "marks": "5 Marks",
        "text": "a) State De-Moivre's theorem.\nb) Solve z^4 - 1 = 0.\nc) Interpret roots geometrically.",
        "solution": "a) (cos theta + i sin theta)^n = cos(n theta) + i sin(n theta).\nb) z = 1, -1, i, -i.\nc) Vertices of a square inscribed in unit circle |z| = 1."
    },
    {
        "num": "2",
        "marks": "5 Marks",
        "text": "a) Derivative of y = x^(cosh x)?\nb) If f, g -> 0 as x->a, value of lim f(x)/g(x)?\nc) Tangent to y = f(x) at (x0, y0) || X-axis?",
        "solution": "a) x^(cosh x) [sinh(x) ln x + cosh(x)/x].\nb) lim f'(x)/g'(x) by L'Hopital.\nc) y = y0."
    },
    {
        "num": "3.a",
        "marks": "2 Marks",
        "text": "Evaluate lim (x->0) ln(1 - x^2) / ln(cos x).",
        "solution": "Form [0/0]. L'Hopital: lim [2 / (1 - x^2)] [x / tan x] = 2."
    },
    {
        "num": "3.b",
        "marks": "3 Marks",
        "text": "Sphere radius changes 3 cm to 3.01 cm, approximate volume increase?",
        "solution": "dV = 4pi r^2 dr = 4pi(9)(0.01) = 0.36pi cm^3."
    },
    {
        "num": "4.a",
        "marks": "3 Marks",
        "text": "Tangent to y^2 = a x^3 + b at (2,3) is y = 4x - 5, find a and b.",
        "solution": "m = 2a = 4 ==> a = 2. 9 = 16 + b ==> b = -7."
    },
    {
        "num": "4.b",
        "marks": "2 Marks",
        "text": "Angle of intersection of y = x^2 and 6y = 7 - x^3 at (1,1)?",
        "solution": "m1 = 2, m2 = -1/2. m1 * m2 = -1 ==> 90° (pi/2)."
    },
    {
        "num": "5",
        "marks": "5 Marks",
        "text": "Expanding cube edge rate 3 cm/sec. Rates of volume & surface area increase at x = 10 cm?",
        "solution": "dV/dt = 3 x^2 (dx/dt) = 900 cm^3/sec.\ndS/dt = 12 x (dx/dt) = 360 cm^2/sec."
    },
    {
        "num": "6.a",
        "marks": "2 Marks",
        "text": "Inverse matrix method to solve x + 2y = 3, 2x + 3y = 5.",
        "solution": "A^(-1) = [ -3 2 ; 2 -1 ]. X = A^(-1) B = [ 1 ; 1 ]. Solution: x = 1, y = 1."
    },
    {
        "num": "6.b",
        "marks": "3 Marks",
        "text": "If w is cube root of unity, prove w^n + w^(2n) = -1 when n not multiple of 3.",
        "solution": "If n=3k+1 or 3k+2, w^n + w^(2n) = w + w^2 = -1."
    },
    {
        "num": "7",
        "marks": "5 Marks",
        "text": "Chemist 100-unit drug mixture equations:\nx + y + z = 100\n3x - y + z = 0\ny - 2z = 0\nSolve by Determinant method.",
        "solution": "D = 10, Dx = 100 ==> x = 10.\nDy = 600 ==> y = 60.\nDz = 300 ==> z = 30.\nUnits: A = 10, B = 60, C = 30."
    }
]


# SET 5 MODEL
set_5_model_ga = [
    {
        "num": "1",
        "text": "Euler's form of complex number?",
        "options": ["A) r * e^(i theta)", "B) e^z", "C) r(cos theta + i sin theta)", "D) e^(i z)"],
        "solution": "Euler's form: z = r e^(i theta).",
        "correct": "A) r * e^(i theta)"
    },
    {
        "num": "2",
        "text": "Linear system has infinitely many solutions if:",
        "options": [
            "A) D = 0, D1 != 0, D2 != 0",
            "B) D = 0, D1 = 0, D2 = 0",
            "C) D != 0, D1 != 0, D2 != 0",
            "D) D != 0, D1 = 0, D2 = 0"
        ],
        "solution": "Infinitely many solutions occur when D = 0 and D1 = D2 = 0.",
        "correct": "B) D = 0, D1 = 0, D2 = 0"
    },
    {
        "num": "3",
        "text": "If x^n - 1 is divisible by x - k for all integer n, value of k?",
        "options": ["A) 1", "B) 2", "C) 3", "D) 4"],
        "solution": "P(k) = k^n - 1 = 0 for all n ==> k = 1.",
        "correct": "A) 1"
    },
    {
        "num": "4",
        "text": "System (i), (ii), (iii) diagonally dominant if order is:",
        "options": [
            "A) (iii), (ii) and (i)",
            "B) (iii), (i) and (ii)",
            "C) (i), (ii) and (iii)",
            "D) (i), (iii) and (ii)"
        ],
        "solution": "Row 1: Eq (iii), Row 2: Eq (i), Row 3: Eq (ii).",
        "correct": "B) (iii), (i) and (ii)"
    }
]

set_5_model_gb = [
    {
        "num": "5",
        "marks": "5 Marks",
        "text": "a) Find cube roots of unity by De-Moivre's theorem.\nb) Interpret roots geometrically.",
        "solution": "a) 1, -1/2 + i sqrt(3)/2 = w, -1/2 - i sqrt(3)/2 = w^2.\nb) Vertices of equilateral triangle on unit circle."
    },
    {
        "num": "6",
        "marks": "5 Marks",
        "text": "Series 1 + 3 + 7 + 13 + 21 + ...\na) nth term (tn)?\nb) Sum of n terms (Sn)?\nc) 15th term & sum of 20 terms?",
        "solution": "a) tn = n^2 - n + 1.\nb) Sn = n(n^2 + 2) / 3.\nc) t15 = 211, S20 = 2680."
    },
    {
        "num": "7.a",
        "marks": "2 Marks",
        "text": "Reason why x + 2y = 5 and 3x + 6y = 12 not solvable by Inverse matrix method.",
        "solution": "Det(A) = 6 - 6 = 0. Matrix is singular, inverse undefined."
    },
    {
        "num": "7.b",
        "marks": "3 Marks",
        "text": "Use inverse matrix method to solve: x - y = 0, x + y - z = 1, y + z = 2.",
        "solution": "Det(A) = 3. adj(A) = [2 1 1 ; -1 1 1 ; 1 -1 2]. X = [1 ; 1 ; 1]."
    },
    {
        "num": "8",
        "marks": "5 Marks",
        "text": "Simplex method: Max Z = 50x + 60y s.t. 3x + 4y <= 36, 9x + 4y <= 60, x, y >= 0.",
        "solution": "Iter 1: Pivot (y, s1, 4).\nIter 2: Pivot (x, s2, 6).\nOptimal: x = 4, y = 6, Max Z = 560."
    }
]

set_5_model_gc = [
    {
        "num": "9.a",
        "marks": "4 Marks",
        "text": "Augmented matrix [ 1 2 -1 | 5 ; 0 0 1 | 3 ; 0 0 r | p ]:\ni) r = 0, p != 0?\nii) r = 0, p = 0?\niii) r = 1, p = 1?",
        "solution": "i) Inconsistent (No Solution).\nii) Consistent (Infinitely Many Solutions).\niii) Inconsistent (No Solution since z=3 and z=1)."
    },
    {
        "num": "9.b",
        "marks": "4 Marks",
        "text": "Solve 3x - 6y + 2z = 23, -4x + y - z = -8, x - 3y + 7z = 17 by Gauss-Seidel method (error < 0.005).",
        "solution": "Diagonally dominant system:\n4x - y + z = 8\n-3x + 6y - 2z = -23\nx - 3y + 7z = 17\nIter 6 converges to x = 1.0001, y = -3.0000, z = 1.0000.\nSolution: x = 1, y = -3, z = 1."
    },
    {
        "num": "10",
        "marks": "8 Marks",
        "text": "a) Show arg(z) + arg(z_bar) = 2pi, verify with z = 1+i.\nc) Prove d/dx(tanh x) = sech^2 x.\nd) Condition for d/dx[tanh^(-1) x] = 1/(1-x^2)?\ne) Derivative of tanh^(-1)(sin 2x)?",
        "solution": "a) arg(z) + arg(z_bar) = theta + (2pi - theta) = 2pi. Verified for 1+i: pi/4 + 7pi/4 = 2pi.\nc) d/dx(sinh x / cosh x) = (cosh^2 x - sinh^2 x)/cosh^2 x = sech^2 x.\nd) |x| < 1.\ne) 2 sec(2x)."
    }
]

# --- MAIN EXECUTION ---
def main():
    sets = [
        ("KATHMANDU MODEL SECONDARY SCHOOL - MORNING SHIFT SET 'A'", set_a_morning_ga, set_a_morning_gb, None, "math_set_a_morning_oled.txt"),
        ("KATHMANDU MODEL SECONDARY SCHOOL - MORNING SHIFT SET 'B'", set_b_morning_ga, set_b_morning_gb, None, "math_set_b_morning_oled.txt"),
        ("KATHMANDU MODEL SECONDARY SCHOOL - DAY SHIFT SET 'A'", set_a_day_ga, set_a_day_gb, None, "math_set_a_day_oled.txt"),
        ("KATHMANDU MODEL SECONDARY SCHOOL - DAY SHIFT SET 'B'", set_b_day_ga, set_b_day_gb, None, "math_set_b_day_oled.txt"),
        ("KATHMANDU MODEL SECONDARY SCHOOL - MODEL SET '5'", set_5_model_ga, set_5_model_gb, set_5_model_gc, "math_set_5_model_oled.txt"),
    ]

    all_oled_parts = [
        "=" * 32,
        "  COMPLETE MASTER MATH SOLUTIONS".center(32),
        "    DEV DARSHAN OLED VERSION    ".center(32),
        "=" * 32,
        ""
    ]

    for title, ga, gb, gc, fname in sets:
        oled_content = build_oled_set(title, ga, gb, gc)
        
        # Save individual OLED file
        fpath = os.path.join(OLED_DIR, fname)
        with open(fpath, "w", encoding="utf-8") as f:
            f.write(oled_content)
        
        all_oled_parts.append(oled_content)

    # Save master combined file
    master_content = "\n\n".join(all_oled_parts).strip() + "\n"
    master_path = os.path.join(OLED_DIR, "all_math_solutions_oled.txt")
    with open(master_path, "w", encoding="utf-8") as f:
        f.write(master_content)

    print("All OLED files generated successfully.")

    # LINE LENGTH VERIFICATION
    total_errors = 0
    for root, _, files in os.walk(OLED_DIR):
        for file in files:
            filepath = os.path.join(root, file)
            with open(filepath, "r", encoding="utf-8") as f:
                lines = f.readlines()
            
            file_errors = 0
            for idx, l in enumerate(lines, 1):
                clean_l = l.rstrip("\r\n")
                if len(clean_l) > 32:
                    print(f"ERROR in {file} L{idx} (len {len(clean_l)}): '{clean_l}'")
                    file_errors += 1
            
            total_errors += file_errors
            print(f"Verified {file}: {len(lines)} lines, Max len: {max(len(l.rstrip('\r\n')) for l in lines)}, Errors: {file_errors}")

    if total_errors == 0:
        print("PERFECT SUCCESS! All OLED files have ZERO line length violations (> 32 chars).")

if __name__ == "__main__":
    main()
