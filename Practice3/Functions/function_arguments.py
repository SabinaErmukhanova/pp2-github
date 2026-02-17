# Positional arguments
def multiply(a, b):
    return a * b

# Default argument
def power(number, exponent=2):
    return number ** exponent

# Keyword arguments
def introduce(name, age):
    print("Name:", name)
    print("Age:", age)

# Passing list
def print_list(numbers):
    for n in numbers:
        print(n)

# Test
print("Multiply:", multiply(4, 5))
print("Square:", power(6))
print("Cube:", power(6, 3))
introduce(age=18, name="Tair")
my_list = [1, 2, 3]
print_list(my_list)