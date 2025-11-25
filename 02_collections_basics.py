"""
Collections basics cheat sheet.

Covers:
- lists (creation, indexing, slicing, mutating, methods, nested lists)
- tuples (creation, unpacking, immutability)
- sets (uniqueness, set operations)
- dictionaries (key–value storage, methods, iteration)
- basic list and dict comprehensions
"""

# ============================================
# 1. Lists
# ============================================

# Creating lists
numbers = [10, 20, 30, 40]
mixed = [1, "two", 3.0, True]

print("numbers:", numbers)
print("mixed:", mixed)

# Indexing and slicing
print("First element:", numbers[0])        # 10
print("Last element:", numbers[-1])       # 40
print("Slice [1:3]:", numbers[1:3])       # [20, 30]

# Updating elements
numbers[0] = 100
print("After update:", numbers)           # [100, 20, 30, 40]

# List methods
numbers.append(50)                        # add at the end
print("After append:", numbers)

numbers.extend([60, 70])                  # extend with another iterable
print("After extend:", numbers)

numbers.insert(1, 15)                     # insert at index 1
print("After insert:", numbers)

numbers.remove(30)                        # remove first occurrence of value
print("After remove(30):", numbers)

last_value = numbers.pop()                # remove and return last element
print("Popped value:", last_value)
print("After pop:", numbers)

# Deleting by index (using del)
del numbers[0]
print("After del numbers[0]:", numbers)

# Membership and length
print("Is 20 in numbers?", 20 in numbers)
print("Is 999 in numbers?", 999 in numbers)
print("Length of numbers:", len(numbers))

# Built-in functions with numeric lists
values = [3, 1, 4, 1, 5, 9]
print("values:", values)
print("min:", min(values))
print("max:", max(values))
print("sum:", sum(values))

# Sorting
values_sorted = sorted(values)            # returns a new sorted list
print("sorted(values):", values_sorted)
print("original values:", values)

values.sort(reverse=True)                 # sorts in place
print("values.sort(reverse=True):", values)

# Nested lists (2D)
matrix = [
    [1, 2, 3],
    [4, 5, 6]
]

print("matrix:", matrix)
print("matrix[0][1]:", matrix[0][1])      # 2


# ============================================
# 2. Tuples
# ============================================

# Creating tuples
point = (3, 4)
single_element_tuple = (5,)  # note the comma

print("point:", point)
print("single_element_tuple:", single_element_tuple)

# Tuple unpacking
x, y = point
print("x:", x, "y:", y)

# Tuples are immutable – this would raise an error:
# point[0] = 10  # TypeError


# ============================================
# 3. Sets
# ============================================

# Creating sets (duplicates are removed automatically)
A = {1, 2, 3, 3, 2}
B = set([3, 4, 5])

print("A:", A)  # {1, 2, 3}
print("B:", B)  # {3, 4, 5}

# Basic operations
A.add(4)
print("A after add(4):", A)

A.discard(2)          # remove element if it exists (no error if missing)
print("A after discard(2):", A)

# Set operations
print("A union B:", A.union(B))
print("A intersection B:", A.intersection(B))
print("A difference B:", A.difference(B))
print("Is {3, 4} subset of B?", {3, 4}.issubset(B))

# Membership
print("Is 3 in A?", 3 in A)
print("Is 99 in A?", 99 in A)


# ============================================
# 4. Dictionaries
# ============================================

# Creating dictionaries
person = {
    "name": "Joanna",
    "age": 35,
    "job": "Data Analyst"
}

print("person:", person)

# Accessing and updating values
print("Name:", person["name"])

person["age"] = 36                   # update existing key
person["city"] = "Charlotte"         # add new key
print("Updated person:", person)

# Safe access with get (no KeyError)
print("Salary (with default):", person.get("salary", "unknown"))

# Deleting keys
del person["job"]
removed_city = person.pop("city", None)  # remove and return value
print("Removed city:", removed_city)
print("After deletions:", person)

# Keys, values, items
print("Keys:", list(person.keys()))
print("Values:", list(person.values()))
print("Items:", list(person.items()))

# Iterating over a dict
for key, value in person.items():
    print(f"{key} -> {value}")


# ============================================
# 5. Iteration over collections
# ============================================

fruits = ["apple", "banana", "orange"]

# Simple for loop
for fruit in fruits:
    print("Fruit:", fruit)

# Index + value using enumerate
for idx, fruit in enumerate(fruits):
    print(f"Fruit #{idx}: {fruit}")

# Iterating over a nested list (matrix)
for row in matrix:
    for value in row:
        print("Matrix value:", value)


# ============================================
# 6. List and dict comprehensions
# ============================================

numbers_range = list(range(1, 6))  # [1, 2, 3, 4, 5]
print("numbers_range:", numbers_range)

# List comprehensions
squared = [n ** 2 for n in numbers_range]
print("squared:", squared)

even_squared = [n ** 2 for n in numbers_range if n % 2 == 0]
print("even_squared:", even_squared)

# Dict comprehension – mapping fruit -> length of its name
fruit_lengths = {fruit: len(fruit) for fruit in fruits}
print("fruit_lengths:", fruit_lengths)
