import os
import re
import textwrap

def format_block_to_oled(text, max_width=32):
    lines = text.strip().split('\n')
    output_lines = []
    
    for line in lines:
        stripped = line.strip()
        if not stripped:
            output_lines.append("")
        elif set(stripped) == {'='} or set(stripped) == {'-'}:
            output_lines.append(stripped[0] * max_width)
        else:
            # Preserve leading indentation up to 4 spaces
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
                
    # Collapse 3+ consecutive newlines to max 2 (\n\n)
    full_text = '\n'.join(output_lines)
    single_gap_text = re.sub(r'\n{3,}', '\n\n', full_text)
    
    # Check max line length
    final_lines = single_gap_text.split('\n')
    max_len = max(len(l) for l in final_lines) if final_lines else 0
    oversized = [l for l in final_lines if len(l) > max_width]
    
    return single_gap_text, max_len, oversized

set_1_content = """
================================
 COMPUTER SCIENCE - SET 1
 FULL MODEL SOLUTIONS
================================

--------------------------------
 GROUP A: MCQs (5 x 1 = 5)
--------------------------------

QUESTION 1:
Which of the following is a user-defined function type where no arguments are passed and no return value is expected?
a) NBNA  b) NRYA
c) YRNA  d) YRYA
ANSWER: a) NBNA
Explanation: NBNA stands for No Argument & No Return Value.

QUESTION 2:
In C, what happens to the original value of a variable when passed using "call by value"?
a) It is modified by the function.
b) It remains unchanged.
c) Its memory address is passed.
d) It is deleted.
ANSWER: b) It remains unchanged.
Explanation: Call by value passes a copy of the argument, so the original variable is preserved.

QUESTION 3:
Which storage class has a local scope and its lifetime is limited to the function block where it is declared?
a) auto     b) register
c) static   d) extern
ANSWER: a) auto
Explanation: 'auto' is the default storage class for all local variables.

QUESTION 4:
Which of the following best describes Cloud Computing?
a) Storing data on your personal computer.
b) Delivering computing services-including servers, storage, databases, networking, software, analytics, and intelligence-over the Internet ("the cloud").
c) Only storing files in online drives.
d) Using a single, powerful supercomputer.
ANSWER: b) Delivering computing services over the Internet.

QUESTION 5:
When an entire array is passed to a function, what is actually passed?
a) A copy of the entire array.
b) Only the base address of the array.
c) The size of the array.
d) Individual elements are copied.
ANSWER: b) Only the base address of the array.

--------------------------------
 GROUP B: SHORT ANSWERS (3 x 4 = 12)
--------------------------------

Q1: Differentiate between "call by value" and "call by reference" with a simple example showing their impact on variable values. [4]

ANSWER:
1. Concept:
   - Call by Value: Passes a copy of the actual parameter value to the function.
   - Call by Reference: Passes the memory address (pointer) of the actual parameter to the function.

2. Impact on Original Variable:
   - Call by Value: Modifications inside the function DO NOT affect the original variable.
   - Call by Reference: Modifications inside the function DO affect and modify the original variable.

3. Code Example:
#include <stdio.h>
void val(int x) {
  x = 20;
}
void ref(int *x) {
  *x = 20;
}
int main() {
  int a = 10, b = 10;
  val(a);   // a remains 10
  ref(&b);  // b becomes 20
  printf("a = %d, b = %d\\n", a, b);
  return 0;
}

--------------------------------
Q2: What is Artificial Intelligence (AI)? Mention two real world applications of AI. [2+2]

ANSWER:
1. Definition:
Artificial Intelligence (AI) is a branch of computer science focused on building smart machines capable of performing tasks that typically require human intelligence, such as learning, reasoning, pattern recognition, and decision making.

2. Real-World Applications:
i) Healthcare: AI algorithms assist in analyzing medical scans (X-rays, MRIs) for early disease detection.
ii) Autonomous Systems: Self-driving vehicles (e.g. Tesla) use computer vision and AI for navigation.

--------------------------------
Q2 (OR): Explain the static storage class in C with an example. How does its lifetime differ from an auto variable? [3+1]

ANSWER:
1. Static Storage Class:
Variables declared with the 'static' keyword retain their value across multiple function calls. They are stored in static memory and initialized only once (default value is 0).

2. Lifetime Comparison:
- auto variable: Lifetime is limited to the execution of the block where it is declared. It is destroyed upon function exit.
- static variable: Lifetime persists throughout the entire execution of the program.

3. Code Example:
#include <stdio.h>
void count() {
  static int c = 0;
  c++;
  printf("%d ", c);
}
int main() {
  count(); // Prints 1
  count(); // Prints 2
  count(); // Prints 3
  return 0;
}

--------------------------------
Q3: What is recursive function? Provide a simple C program that uses recursion to print factorial of a number. [1+3]

ANSWER:
1. Recursive Function:
A function that calls itself directly or indirectly to solve a problem until it reaches a base condition that terminates the recursion.

2. C Program (Factorial):
#include <stdio.h>
int fact(int n) {
  if (n <= 1)
    return 1;
  return n * fact(n - 1);
}
int main() {
  int num = 5;
  printf("Factorial of %d = %d\\n",
         num, fact(num));
  return 0;
}

--------------------------------
 GROUP C: LONG ANSWERS (1 x 8 = 8)
--------------------------------

Q1: Define a structure named Product with members id, name, and price. Write a C program to input details of N number of products and display them using structure. [2+6]

ANSWER:
1. Structure Definition:
A structure is a user-defined data type in C that allows grouping together variables of different data types under a single name.

2. C Program:
#include <stdio.h>
struct Product {
  int id;
  char name[30];
  float price;
};

int main() {
  int n, i;
  printf("Enter number of products: ");
  scanf("%d", &n);
  struct Product p[n];

  for(i = 0; i < n; i++) {
    printf("\\nProduct %d ID: ", i+1);
    scanf("%d", &p[i].id);
    printf("Product %d Name: ", i+1);
    scanf("%s", p[i].name);
    printf("Product %d Price: ", i+1);
    scanf("%f", &p[i].price);
  }

  printf("\\n=========================\n");
  printf("    PRODUCT DETAILS\n");
  printf("=========================\n");
  for(i = 0; i < n; i++) {
    printf("ID: %d\\n", p[i].id);
    printf("Name: %s\\n", p[i].name);
    printf("Price: $%.2f\\n", p[i].price);
    printf("-------------------------\\n");
  }
  return 0;
}
"""

set_2_content = """
================================
 COMPUTER SCIENCE - SET 2
 FULL MODEL SOLUTIONS
================================

--------------------------------
 GROUP A: MCQs (5 x 1 = 5)
--------------------------------

QUESTION 1:
When using "call by reference", what is passed to the function, allowing it to modify the original variable?
a) A copy of the value.
b) The memory address of the variable.
c) Only the variable name.
d) Its data type.
ANSWER: b) The memory address of the variable.

QUESTION 2:
Which storage class has a global scope and retains its value even if the control goes out of its scope?
a) auto     b) register
c) extern   d) static
ANSWER: c) extern
Explanation: 'extern' gives global visibility across multiple source files.

QUESTION 3:
Every recursive function must have a condition that stops the recursion. This condition is called the:
a) Termination point
b) Base case
c) Exit condition
d) Loop break
ANSWER: b) Base case

QUESTION 4:
Which of the following is a key characteristic of Big Data?
a) Small volume.  b) High velocity
c) Low veracity   d) Static nature
ANSWER: b) High velocity

QUESTION 5:
What is the output of following C code?
#include<stdio.h>
int main(){
auto int a;
register int b;
static int c;
printf("%d\\t%d\\t%d\\t",a,b,c);
return 0;
}
a) 0 0 1
b) 101
c) Garbage Garbage 0
d) 110
ANSWER: c) Garbage Garbage 0
Explanation: auto and register variables hold garbage values when uninitialized, while static variables are automatically initialized to 0.

--------------------------------
 GROUP B: SHORT ANSWERS (3 x 4 = 12)
--------------------------------

Q1: Write a C program using a user-defined function (NRYA type) to check if a given number is even or odd. [4]

ANSWER:
NRYA: No Return, Yes Argument.
#include <stdio.h>
void checkEvenOdd(int num) {
  if (num % 2 == 0)
    printf("%d is EVEN\\n", num);
  else
    printf("%d is ODD\\n", num);
}

int main() {
  int n;
  printf("Enter an integer: ");
  scanf("%d", &n);
  checkEvenOdd(n);
  return 0;
}

--------------------------------
Q2: What are the characteristics (the "Vs") of Big data? Briefly explain it. [4]

ANSWER:
Big Data is characterized by five key "Vs":
1. Volume: Massive quantity of data generated every second.
2. Velocity: Extreme speed at which data is created, streamed, and processed.
3. Variety: Wide range of data formats (structured, semi-structured, unstructured).
4. Veracity: Quality, truthfulness, and accuracy of data.
5. Value: Ability to turn raw data into meaningful business insights.

--------------------------------
Q2 (OR): Explain the concept of array with functions. Provide a C program to find the sum of elements in an array by passing the array to a function. [1+3]

ANSWER:
1. Concept:
When passing an array to a function in C, only the base memory address (pointer to the first element) is passed. Any modification inside the function directly affects the array.

2. C Program:
#include <stdio.h>
int calculateSum(int arr[], int size) {
  int sum = 0, i;
  for(i = 0; i < size; i++) {
    sum += arr[i];
  }
  return sum;
}

int main() {
  int numbers[5] = {10, 20, 30, 40, 50};
  int total = calculateSum(numbers, 5);
  printf("Sum of array elements = %d\\n", total);
  return 0;
}

--------------------------------
Q3: What are the benefits of recursive function? Write a simple C program that uses recursion to print Fibonacci series up to Nth term. [1+3]

ANSWER:
1. Benefits of Recursion:
- Reduces code complexity and makes code cleaner for naturally recursive problems.
- Ideal for data structures like Trees, Graphs, and algorithms like divide-and-conquer (QuickSort, MergeSort).

2. C Program (Fibonacci Series):
#include <stdio.h>
int fibonacci(int n) {
  if (n <= 0) return 0;
  if (n == 1) return 1;
  return fibonacci(n - 1) + fibonacci(n - 2);
}

int main() {
  int terms, i;
  printf("Enter number of terms: ");
  scanf("%d", &terms);
  printf("Fibonacci Series: ");
  for(i = 0; i < terms; i++) {
    printf("%d ", fibonacci(i));
  }
  printf("\\n");
  return 0;
}

--------------------------------
 GROUP C: LONG ANSWERS (1 x 8 = 8)
--------------------------------

Q1: Define a structure named Employee with members employee id, name, and salary. Write a C program to input details for N number of employees and display the name of the employee with the highest salary using structure. [2+6]

ANSWER:
1. Structure Definition:
A structure allows storing different data types under one named type.

2. C Program:
#include <stdio.h>
struct Employee {
  int id;
  char name[30];
  float salary;
};

int main() {
  int n, i, maxIndex = 0;
  printf("Enter number of employees: ");
  scanf("%d", &n);
  struct Employee emp[n];

  for(i = 0; i < n; i++) {
    printf("\\nEmp %d ID: ", i+1);
    scanf("%d", &emp[i].id);
    printf("Emp %d Name: ", i+1);
    scanf("%s", emp[i].name);
    printf("Emp %d Salary: ", i+1);
    scanf("%f", &emp[i].salary);
  }

  for(i = 1; i < n; i++) {
    if(emp[i].salary > emp[maxIndex].salary) {
      maxIndex = i;
    }
  }

  printf("\\n=========================\n");
  printf(" HIGHEST SALARY EMPLOYEE\n");
  printf("=========================\n");
  printf("ID: %d\\n", emp[maxIndex].id);
  printf("Name: %s\\n", emp[maxIndex].name);
  printf("Salary: $%.2f\\n", emp[maxIndex].salary);
  return 0;
}
"""

set_3_content = """
================================
 COMPUTER SCIENCE - SET 3
 FULL MODEL SOLUTIONS
================================

--------------------------------
 GROUP A: MCQs (5 x 1 = 5)
--------------------------------

QUESTION 1:
What would be the most suitable user-defined function type for a function that takes an array and its size as input, sorts the array, and then prints the sorted array?
a) NRNA  b) YRNA
c) NRYA  d) YRYA
ANSWER: c) NRYA (No Return, Yes Argument)

QUESTION 2:
Which storage class keyword indicates that a variable's value should persist across multiple function calls, even if it's declared inside a function?
a) auto     b) register
c) extern   d) static
ANSWER: d) static

QUESTION 3:
When passing a multi-dimensional array to a function, which dimension must be explicitly specified in the function parameter list?
a) Only the first dimension.
b) Only the last dimension.
c) All dimensions except the first.
d) All dimensions.
ANSWER: c) All dimensions except the first.

QUESTION 4:
Which type of cloud deployment model is built for exclusive use by a single organization, providing the most control and security?
a) Public Cloud.  b) Private Cloud
c) Hybrid Cloud  d) Community Cloud
ANSWER: b) Private Cloud

QUESTION 5:
What is the output of following C program?
#include <stdio.h>
void func();
int main() {
func(); func(); func();
return 0;
}
void func() {
static int count = 0;
count++;
printf("%d\\t", count);
}
a) 1 1 1   b) 1 2 3
c) 0 0 0   d) Compilation error
ANSWER: b) 1 2 3

--------------------------------
 GROUP B: SHORT ANSWERS (3 x 4 = 12)
--------------------------------

Q1: Write a C program to implement user-defined function (YRNA type) that takes no arguments but calculate and returns the factorials of hardcoded number (e.g., 5). [4]

ANSWER:
YRNA: Yes Return, No Argument.
#include <stdio.h>
int calculateFactorial5() {
  int num = 5, fact = 1, i;
  for(i = 1; i <= num; i++) {
    fact *= i;
  }
  return fact;
}

int main() {
  int result = calculateFactorial5();
  printf("Factorial of 5 = %d\\n", result);
  return 0;
}

--------------------------------
Q2: What is cloud computing? List and briefly describe any three types of cloud services. [2+2]

ANSWER:
1. Cloud Computing:
On-demand delivery of IT resources (computing power, database storage, applications) over the Internet with pay-as-you-go pricing.

2. Three Types of Cloud Services:
i) IaaS (Infrastructure as a Service): Rent raw infrastructure like virtual servers, storage, and networking (e.g. AWS EC2).
ii) PaaS (Platform as a Service): Provides hardware & software tools for app development without managing servers (e.g. Heroku).
iii) SaaS (Software as a Service): Delivers complete software applications over the web (e.g. Google Workspace, Office 365).

--------------------------------
Q2 (OR): What is function prototype. Provide a C program to find the greatest number from N number of elements using user define function. [1+3]

ANSWER:
1. Function Prototype:
A function declaration that informs the compiler about the function's name, return type, and parameters before its actual definition.

2. C Program:
#include <stdio.h>
int findGreatest(int arr[], int n);

int main() {
  int n, i;
  printf("Enter N: ");
  scanf("%d", &n);
  int numbers[n];
  for(i = 0; i < n; i++) {
    printf("Element %d: ", i+1);
    scanf("%d", &numbers[i]);
  }
  int greatest = findGreatest(numbers, n);
  printf("Greatest number = %d\\n", greatest);
  return 0;
}

int findGreatest(int arr[], int n) {
  int max = arr[0], i;
  for(i = 1; i < n; i++) {
    if(arr[i] > max) max = arr[i];
  }
  return max;
}

--------------------------------
Q3: What is recursive function? Write a simple C program that uses recursion to print Sum of N natural number. [1+3]

ANSWER:
1. Recursive Function:
A function that calls itself to divide a problem into simpler sub-problems until a base condition stops execution.

2. C Program (Sum of N Natural Numbers):
#include <stdio.h>
int sumNatural(int n) {
  if (n <= 0) return 0;
  return n + sumNatural(n - 1);
}

int main() {
  int n;
  printf("Enter N: ");
  scanf("%d", &n);
  printf("Sum of first %d natural numbers = %d\\n",
         n, sumNatural(n));
  return 0;
}

--------------------------------
 GROUP C: LONG ANSWERS (1 x 8 = 8)
--------------------------------

Q1: Define a structure for Time that stores hours, minutes, and seconds. Write a C program that takes two Time inputs from the user, calculates their sum, and displays the resulting time using structure. [2+6]

ANSWER:
1. Structure Definition:
Represents time using 3 integer members: hours, minutes, and seconds.

2. C Program:
#include <stdio.h>
struct Time {
  int hours;
  int minutes;
  int seconds;
};

int main() {
  struct Time t1, t2, sum;

  printf("Time 1 (hours min sec): ");
  scanf("%d %d %d", &t1.hours, &t1.minutes, &t1.seconds);

  printf("Time 2 (hours min sec): ");
  scanf("%d %d %d", &t2.hours, &t2.minutes, &t2.seconds);

  sum.seconds = t1.seconds + t2.seconds;
  sum.minutes = t1.minutes + t2.minutes + (sum.seconds / 60);
  sum.seconds %= 60;

  sum.hours = t1.hours + t2.hours + (sum.minutes / 60);
  sum.minutes %= 60;

  printf("\\n=========================\n");
  printf("       TOTAL TIME\n");
  printf("=========================\n");
  printf("%02d Hours : %02d Mins : %02d Secs\\n",
         sum.hours, sum.minutes, sum.seconds);
  return 0;
}
"""

set_4_content = """
================================
 COMPUTER SCIENCE - SET 4
 FULL MODEL SOLUTIONS
================================

--------------------------------
 GROUP A: MCQs (5 x 1 = 5)
--------------------------------

QUESTION 1:
You have a function void process(int arr[], int size);. If int myArray[10]; is passed as process(myArray, 10);, how is arr treated inside the process function?
a) As a copy of myArray.
b) As a pointer to the first element of myArray.
c) As an auto variable.
d) As a static variable.
ANSWER: b) As a pointer to the first element of myArray.

QUESTION 2:
Which storage class is intended for variables that are accessed very frequently, potentially speeding up execution?
a) auto     b) register
c) extern   d) static
ANSWER: b) register

QUESTION 3:
What is the correct way to pass an array int matrix[3][3]; to a function void func(int m[][3]);?
a) func(matrix[3][3]);
b) func(matrix);
c) func(&matrix);
d) func(matrix[][]);
ANSWER: b) func(matrix);

QUESTION 4:
Which model of Cloud Computing gives users access to raw computing resources like virtual machines, storage, and networks?
a) IaaS  b) PaaS
c) SaaS  d) None of the above
ANSWER: a) IaaS

QUESTION 5:
What happens if a recursive function in C does not have a base condition?
a) It will execute indefinitely / cause stack overflow.
b) It will return an incorrect result.
c) It will automatically terminate after a certain number of calls.
d) It will cause a compile-time error.
ANSWER: a) It will execute indefinitely / cause stack overflow.

--------------------------------
 GROUP B: SHORT ANSWERS (3 x 4 = 12)
--------------------------------

Q1: Write a C program that uses a user-defined function (YRYA type) to reverse a given integer number and returns the reversed number. [4]

ANSWER:
YRYA: Yes Return, Yes Argument.
#include <stdio.h>
int reverseNumber(int num) {
  int rev = 0, rem;
  while(num != 0) {
    rem = num % 10;
    rev = rev * 10 + rem;
    num /= 10;
  }
  return rev;
}

int main() {
  int n;
  printf("Enter an integer: ");
  scanf("%d", &n);
  int reversed = reverseNumber(n);
  printf("Reversed Number = %d\\n", reversed);
  return 0;
}

--------------------------------
Q2: What is Artificial Intelligence (AI)? Explain how AI differs from traditional programming. List out and shortly define its types. [1 + 1 + 2]

ANSWER:
1. Artificial Intelligence (AI):
Field of computer science devoted to creating systems capable of performing intelligent human-like tasks.

2. Difference from Traditional Programming:
- Traditional: Human writes explicit rules + data -> system produces output.
- AI: Machine uses algorithms + data -> system learns patterns and self-adjusts rules.

3. Types of AI:
i) Narrow AI (Weak AI): Designed for specific single tasks (e.g. Siri, Alexa, Chess AI).
ii) General AI (Strong AI): Theoretical AI with human-level intellect across all domains.
iii) Super AI: Future AI surpassing human intelligence in every cognitive aspect.

--------------------------------
Q2 (OR): Differentiate Between Structure and Array. [4]

ANSWER:
1. Element Data Types:
   - Array: Collection of homogeneous elements (all of the SAME data type).
   - Structure: Collection of heterogeneous elements (can be of DIFFERENT data types).

2. Access Mechanism:
   - Array: Elements are accessed using numerical indices (e.g. arr[0]).
   - Structure: Members are accessed using member names via dot operator (e.g. s.name).

3. Memory Allocation:
   - Array: Contiguous memory chunk for identical data types.
   - Structure: Contiguous memory chunk with padding for mixed member types.

4. Keyword:
   - Array: No special keyword used during declaration.
   - Structure: Declared using the 'struct' keyword.

--------------------------------
Q3: Differentiate between call by value and call by reference with suitable example. [4]

ANSWER:
1. Parameter Passed:
   - Call by Value: Passes value copy.
   - Call by Reference: Passes memory address (pointer).

2. Side Effects:
   - Call by Value: Modifying parameter inside function leaves original variable unchanged.
   - Call by Reference: Modifying parameter inside function alters original variable value directly.

3. Code Example:
#include <stdio.h>
void swapValue(int a, int b) {
  int temp = a; a = b; b = temp;
}
void swapRef(int *a, int *b) {
  int temp = *a; *a = *b; *b = temp;
}
int main() {
  int x = 5, y = 10;
  swapValue(x, y); // x=5, y=10
  swapRef(&x, &y);   // x=10, y=5
  printf("x=%d y=%d\\n", x, y);
  return 0;
}

--------------------------------
 GROUP C: LONG ANSWERS (1 x 8 = 8)
--------------------------------

Q1: Define a structure for Student with members roll_no, name, address and marks. Write a C program to input details for N number of students and then display them using structure. [2+6]

ANSWER:
1. Structure Definition:
Groups student details: roll_no (int), name (string), address (string), marks (float).

2. C Program:
#include <stdio.h>
struct Student {
  int roll_no;
  char name[30];
  char address[50];
  float marks;
};

int main() {
  int n, i;
  printf("Enter number of students: ");
  scanf("%d", &n);
  struct Student std[n];

  for(i = 0; i < n; i++) {
    printf("\\nStudent %d Roll No: ", i+1);
    scanf("%d", &std[i].roll_no);
    printf("Student %d Name: ", i+1);
    scanf("%s", std[i].name);
    printf("Student %d Address: ", i+1);
    scanf("%s", std[i].address);
    printf("Student %d Marks: ", i+1);
    scanf("%f", &std[i].marks);
  }

  printf("\\n=========================\n");
  printf("     STUDENT RECORDS\n");
  printf("=========================\n");
  for(i = 0; i < n; i++) {
    printf("Roll No : %d\\n", std[i].roll_no);
    printf("Name    : %s\\n", std[i].name);
    printf("Address : %s\\n", std[i].address);
    printf("Marks   : %.2f\\n", std[i].marks);
    printf("-------------------------\\n");
  }
  return 0;
}
"""

sets = [
    ("set1", set_1_content),
    ("set2", set_2_content),
    ("set3", set_3_content),
    ("set4", set_4_content)
]

os.makedirs("d:/D.E.V_Darshan/computer_solutions_oled", exist_ok=True)

all_oled_blocks = []

for name, raw_text in sets:
    formatted_text, max_l, overs = format_block_to_oled(raw_text, 32)
    print(f"{name}: max_len={max_l}, overs_count={len(overs)}")
    if overs:
        print(f"Oversized lines in {name}:", overs)
        
    # Write to computer_solutions_oled/set1.txt ...
    sub_path = f"d:/D.E.V_Darshan/computer_solutions_oled/{name}.txt"
    with open(sub_path, "w", encoding="utf-8") as f:
        f.write(formatted_text + "\n")
        
    # Also write to root directory as computer_set1_oled.txt ...
    root_path = f"d:/D.E.V_Darshan/computer_{name}_oled.txt"
    with open(root_path, "w", encoding="utf-8") as f:
        f.write(formatted_text + "\n")
        
    all_oled_blocks.append(formatted_text)

# Write combined all.txt
full_all_text = "\n\n".join(all_oled_blocks)

with open("d:/D.E.V_Darshan/computer_solutions_oled/all.txt", "w", encoding="utf-8") as f:
    f.write(full_all_text + "\n")

with open("d:/D.E.V_Darshan/computer_full_solutions_oled.txt", "w", encoding="utf-8") as f:
    f.write(full_all_text + "\n")

print("All files generated and verified successfully!")
