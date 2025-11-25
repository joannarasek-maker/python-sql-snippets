"""
Python basics cheat sheet.

Covers:
- running Python, printing and comments
- data types and variables
- arithmetic, comparison and logical operators
- strings and f-strings
- conditionals (if / elif / else)
- loops (for, while, break, continue, enumerate)
- basic functions and docstrings
"""

# ============================================
# 1. Running Python and basic instructions
# ============================================

# Check Python version (run this in the terminal, not in the script):
# python --version

# Basic print
print("Hello, Python")

# Single-line comment:
# This is a single-line comment.

"""
This is a multi-line comment (docstring).
It can be used to document a module or a function.
"""

# ============================================
# 2. Data types and variables
# ============================================

# Variable assignment
x = 10          # integer (int)
y = 3.14        # floating point number (float)
name = "Joanna" # string (str)
flag = True     # boolean (bool)

# Checking variable types
print(type(x))
print(type(y))
print(type(name))
print(type(flag))

# Type conversions
a = "10"
b = int(a)      # '10' -> 10
c = float(a)    # '10' -> 10.0
d = str(3.14)   # 3.14 -> "3.14"

# ============================================
# 3. Arithmetic and logical operators
# ============================================

a = 7
b = 3

# Arithmetic operators
print(a + b)   # addition -> 10
print(a - b)   # subtraction -> 4
print(a * b)   # multiplication -> 21
print(a / b)   # division (float) -> 2.333...
print(a // b)  # integer division -> 2
print(a % b)   # modulo (remainder) -> 1
print(a ** b)  # exponentiation -> 343

# Comparison operators (result is bool)
print(a == b)  # equal
print(a != b)  # not equal
print(a > b)   # greater than
print(a < b)   # less than
print(a >= b)  # greater or equal
print(a <= b)  # less or equal

# Logical operators
p = True
q = False

print(p and q)  # True if both are True
print(p or q)   # True if at least one is True
print(not p)    # logical negation

# ============================================
# 4. Strings
# ============================================

# Creating a string
text = "Python for Data Science"

# Indexing (0-based)
print(text[0])   # 'P'
print(text[1])   # 'y'

# Slicing
print(text[0:6])   # 'Python'
print(text[7:10])  # 'for'
print(text[-7:])   # 'Science'

# Length of a string
print(len(text))

# String methods
print(text.upper())                # 'PYTHON FOR DATA SCIENCE'
print(text.lower())                # 'python for data science'
print(text.replace("Data", "AI"))  # 'Python for AI Science'

print(text.find("Data"))           # index of substring start or -1
print(text.split(" "))             # split into list of words

# f-strings (formatted strings)
course = "Python"
hours = 40
message = f"Course: {course}, duration: {hours} hours."
print(message)

# ============================================
# 5. Conditionals (if / elif / else)
# ============================================

age = 20

if age < 18:
    print("Underage")
elif age < 65:
    print("Adult")
else:
    print("Senior")

score = 85

if score >= 90:
    grade = "A"
elif score >= 80:
    grade = "B"
else:
    grade = "C"

print("Grade:", grade)

# ============================================
# 6. Loops (for, while, break, continue, enumerate)
# ============================================

fruits = ["apple", "banana", "orange"]

# for over a list
for fruit in fruits:
    print(fruit)

# for with range()
for i in range(5):  # 0,1,2,3,4
    print(i)

# range with start, stop, step
for i in range(2, 10, 2):  # 2,4,6,8
    print(i)

# while loop – runs while the condition is True
count = 0
while count < 3:
    print("Count:", count)
    count += 1

# break and continue
for i in range(10):
    if i == 5:
        break        # stop the loop completely
    if i % 2 == 0:
        continue     # skip the rest of the body and go to next iteration
    print(i)

# enumerate – index + value
for idx, fruit in enumerate(fruits):
    print(idx, fruit)

# ============================================
# 7. Functions
# ============================================

# Simple function
def add(a, b):
    result = a + b
    return result

sum_ab = add(3, 4)
print(sum_ab)

# Default parameter
def power(base, exp=2):
    return base ** exp

print(power(3))    # 3^2 = 9
print(power(3, 3)) # 3^3 = 27

# Function with docstring
def bmi(weight_kg, height_m):
    """
    Calculate BMI based on weight (kg) and height (m).
    Returns a float value.
    """
    return weight_kg / (height_m ** 2)

print(bmi(60, 1.65))

# Lambda function (anonymous function)
square = lambda x: x ** 2
print(square(5))
