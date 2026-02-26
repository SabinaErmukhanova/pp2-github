# Create a generator that generates the squares of numbers up to some number N.
# Generator function
def generate_squares(n):
    for i in range(n + 1):
        yield i * i  # Return square of number


# Test generator
n = 5
for value in generate_squares(n):
    print(value)