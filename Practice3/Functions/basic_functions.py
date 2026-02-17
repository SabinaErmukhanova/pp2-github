# Function that prints text
def say_hello():
    print("Hello!")

# Function with one parameter
def greet(name):
    print("Hi,", name)

# Function that returns a value
def add(a, b):
    return a + b

# Function that checks even number
def is_even(number):
    return number % 2 == 0


# Test the functions
say_hello()
greet("Sabina")

result = add(5, 3)
print("5 + 3 =", result)

print("10 is even?", is_even(10))