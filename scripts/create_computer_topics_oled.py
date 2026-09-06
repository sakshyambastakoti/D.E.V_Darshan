import os
import re
import textwrap

def format_text_to_oled(text, max_width=32):
    lines = text.strip().split('\n')
    output_lines = []
    
    for line in lines:
        stripped = line.strip()
        if not stripped:
            output_lines.append("")
        elif set(stripped) == {'='} or set(stripped) == {'-'}:
            output_lines.append(stripped[0] * max_width)
        else:
            indent_len = len(line) - len(line.lstrip())
            indent_str = " " * min(indent_len, 4)
            
            wrapped = textwrap.wrap(
                line.strip(),
                width=max_width - len(indent_str),
                break_long_words=True,
                break_on_hyphens=False
            )
            for w in wrapped:
                output_lines.append(indent_str + w)
                
    full_text = '\n'.join(output_lines)
    single_gap_text = re.sub(r'\n{3,}', '\n\n', full_text)
    
    final_lines = single_gap_text.split('\n')
    max_len = max(len(l) for l in final_lines) if final_lines else 0
    oversized = [l for l in final_lines if len(l) > max_width]
    
    return single_gap_text, max_len, oversized

content = """
================================
 COMPUTER SCIENCE CORE TOPICS
 OLED MASTER COMPLIANCE FILE
================================

--------------------------------
 1. UDF (USER DEFINED FUNCTION)
 TYPES & EXAMPLE PROGRAMS
--------------------------------

User-Defined Functions (UDF) in C are classified into 4 types based on parameters passed and return value:

1. No Return & No Argument (NRNA):
- Neither receives arguments nor returns a value to caller.

#include <stdio.h>
void add() {
  int a = 5, b = 10;
  printf("Sum = %d\\n", a + b);
}
int main() {
  add();
  return 0;
}

2. No Return & Yes Argument (NRYA):
- Accepts arguments from caller but does not return any value.

#include <stdio.h>
void checkEvenOdd(int num) {
  if (num % 2 == 0)
    printf("%d is Even\\n", num);
  else
    printf("%d is Odd\\n", num);
}
int main() {
  checkEvenOdd(7);
  return 0;
}

3. Yes Return & No Argument (YRNA):
- Takes no arguments from caller but returns a value after computation.

#include <stdio.h>
int getSquare() {
  int n = 4;
  return n * n;
}
int main() {
  printf("Square = %d\\n", getSquare());
  return 0;
}

4. Yes Return & Yes Argument (YRYA):
- Accepts arguments from caller AND returns a computed result back.

#include <stdio.h>
int findMax(int a, int b) {
  return (a > b) ? a : b;
}
int main() {
  printf("Max = %d\\n", findMax(12, 25));
  return 0;
}

--------------------------------
 2. STORAGE CLASSES IN C
 (TYPES & EXAMPLES)
--------------------------------

Storage classes define scope, visibility, lifetime, and storage location of variables.

1. Automatic (auto):
- Location: RAM (Stack)
- Default value: Garbage
- Scope: Local to block
- Lifetime: End of block

#include <stdio.h>
void func() {
  auto int a = 10;
  printf("%d\\n", a);
}

2. Register (register):
- Location: CPU Register
- Default value: Garbage
- Scope: Local to block
- Lifetime: End of block

#include <stdio.h>
void fastLoop() {
  register int i;
  for(i=0; i<5; i++) printf("%d ", i);
}

3. Static (static):
- Location: RAM (Data segment)
- Default value: Zero (0)
- Scope: Local to block
- Lifetime: Entire program

#include <stdio.h>
void counter() {
  static int c = 0;
  c++;
  printf("%d ", c);
}
int main() {
  counter(); // 1
  counter(); // 2
  return 0;
}

4. External (extern):
- Location: RAM (Data segment)
- Default value: Zero (0)
- Scope: Global (all files)
- Lifetime: Entire program

#include <stdio.h>
int x = 100; // global
void printX() {
  extern int x;
  printf("x = %d\\n", x);
}

--------------------------------
 3. CALL BY VALUE VS
 CALL BY REFERENCE
--------------------------------

1. Concept:
- Call by Value: Passes copy of actual value.
- Call by Reference: Passes memory address of variable using pointers.

2. Effect on Original Variable:
- Call by Value: Original value REMAINS UNCHANGED.
- Call by Reference: Original value CAN BE MODIFIED directly.

3. Example Code Comparison:

#include <stdio.h>
void val(int x) { x = 99; }
void ref(int *x) { *x = 99; }

int main() {
  int a = 10, b = 10;
  val(a);   // a is still 10
  ref(&b);  // b becomes 99
  printf("a=%d, b=%d\\n", a, b);
  return 0;
}

--------------------------------
 4. LIBRARY FUNCTIONS VS
 USER-DEFINED FUNCTIONS (UDF)
--------------------------------

1. Definition:
- Library Functions: Pre-defined built-in functions provided by standard C header files.
- UDF: Functions created by programmers to solve custom requirements.

2. Declaration & Code:
- Library: Declaration present in header files (stdio.h, math.h, string.h); code pre-compiled.
- UDF: Defined and coded explicitly by programmer in source file.

3. Examples:
- Library: printf(), scanf(), sqrt(), strlen(), pow().
- UDF: main(), calculateSum(), checkPrime(), fact().

--------------------------------
 5. RECURSIVE FUNCTION
 DEFINITION & CONCEPT
--------------------------------

1. Definition:
A recursive function is a function that calls itself repeatedly until a specific condition (Base Case) is met to stop execution.

2. Essential Components:
- Base Case: Condition that terminates recursion to prevent infinite loops / stack overflow.
- Recursive Case: Call to the function itself with smaller inputs.

3. Working Mechanism:
Uses system Call Stack (LIFO - Last In First Out) to store return addresses and local variables during each recursive call.

--------------------------------
 6. RECURSION PROGRAMS
--------------------------------

A) WAP: Sum of Digits using Recursion
#include <stdio.h>
int sumDigits(int n) {
  if (n == 0) return 0;
  return (n % 10) + sumDigits(n / 10);
}
int main() {
  int num = 1234;
  printf("Sum of digits = %d\\n", sumDigits(num));
  return 0;
}

B) WAP: Fibonacci Series up to Nth Term
#include <stdio.h>
int fib(int n) {
  if (n <= 0) return 0;
  if (n == 1) return 1;
  return fib(n - 1) + fib(n - 2);
}
int main() {
  int n = 7, i;
  printf("Fibonacci: ");
  for(i = 0; i < n; i++) {
    printf("%d ", fib(i));
  }
  return 0;
}

C) WAP: Factorial using Recursion
#include <stdio.h>
int fact(int n) {
  if (n <= 1) return 1;
  return n * fact(n - 1);
}
int main() {
  int n = 5;
  printf("Factorial of %d = %d\\n", n, fact(n));
  return 0;
}

D) WAP: Length of String using Recursion
#include <stdio.h>
int strLen(char *str) {
  if (*str == '\\0') return 0;
  return 1 + strLen(str + 1);
}
int main() {
  char text[] = "Computer";
  printf("Length = %d\\n", strLen(text));
  return 0;
}

--------------------------------
 7. POINTERS IN C
--------------------------------

1. Definition:
A pointer is a variable that stores the memory address of another variable of the same data type.

2. Operators Used:
- Address-of Operator (&): Returns memory address of a variable.
- Dereference / Value-at Operator (*): Accesses value stored at the memory address.

3. Code Example:
#include <stdio.h>
int main() {
  int x = 25;
  int *p = &x; // p holds address of x
  printf("Value of x = %d\\n", x);
  printf("Address of x = %p\\n", &x);
  printf("Value via pointer = %d\\n", *p);
  return 0;
}

4. Pointer with Array:
Array name acts as a constant pointer to its 1st element: *(arr + i) == arr[i].

--------------------------------
 8. ARTIFICIAL INTELLIGENCE (AI)
 CONCEPTS
--------------------------------

1. Definition:
Artificial Intelligence (AI) is a domain of computer science that creates intelligent software and hardware capable of mimicking human cognitive functions like learning, reasoning, pattern recognition, and problem solving.

2. Types of AI:
- Narrow AI (Weak AI): Built for specific tasks (e.g. Siri, Alexa, Spam Filters).
- General AI (Strong AI): Theoretical human-level general intelligence across domains.
- Super AI: Hypothetical AI exceeding human intelligence in all areas.

3. Key Subfields:
- Machine Learning (ML): Systems learning from data without explicit programming.
- Deep Learning (DL): ML based on multi-layer Artificial Neural Networks.
- Natural Language Processing (NLP): Computer understanding of human language.

--------------------------------
 9. CLOUD COMPUTING & TYPES
--------------------------------

1. Definition:
Cloud Computing is the on-demand delivery of computing services (servers, storage, databases, networking, software) over the Internet on pay-as-you-go pricing.

2. Cloud Deployment Models:
- Public Cloud: Owned & operated by third-party providers (e.g. AWS, Google Cloud).
- Private Cloud: Infrastructure dedicated exclusively to one single organization.
- Hybrid Cloud: Combines public and private clouds, allowing data sharing between them.
- Community Cloud: Shared by multiple organizations with common compliance/goals.

3. Cloud Service Models:
- IaaS (Infrastructure as a Service): Rent raw VMs, storage, networking (AWS EC2).
- PaaS (Platform as a Service): Rent development platforms and OS tools (Heroku).
- SaaS (Software as a Service): Ready-to-use software applications via web browser (Gmail, Google Docs).

--------------------------------
 10. CONCEPT OF INTERNET OF
 THINGS (IoT)
--------------------------------

1. Definition:
Internet of Things (IoT) refers to a network of physical objects ("things") embedded with sensors, software, actuators, and connectivity that enables them to collect, process, and exchange data over the Internet with minimal human interaction.

2. Key Layers of IoT Architecture:
- Sensing Layer: Sensors and actuators gathering physical environment data (temp, motion).
- Network Layer: Transmits data securely (WiFi, Bluetooth, Cellular, LoRaWAN).
- Data Processing Layer: Analyzes and processes data in Cloud/Edge servers.
- Application Layer: User interface & smart services (Smart Home, Smart Cities, Health trackers).

3. Real-World Applications:
- Smart Home Automation (Smart lights, thermostats)
- Industrial IoT (Predictive equipment maintenance)
- Healthcare (Wearable health monitoring devices)
"""

formatted_text, max_l, overs = format_text_to_oled(content, 32)
print(f"OLED Topics File: max_len={max_l}, overs_count={len(overs)}")

sub_path = "d:/D.E.V_Darshan/computer_solutions_oled/topics.txt"
with open(sub_path, "w", encoding="utf-8") as f:
    f.write(formatted_text + "\n")

root_path = "d:/D.E.V_Darshan/computer_topics_oled.txt"
with open(root_path, "w", encoding="utf-8") as f:
    f.write(formatted_text + "\n")

print("Topics file successfully created!")
