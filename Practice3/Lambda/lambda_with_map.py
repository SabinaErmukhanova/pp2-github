# Using lambda with map()

numbers = [1, 2, 3, 4]

# Multiply each number by 2
result = list(map(lambda x: x * 2, numbers))

print("Original:", numbers)
print("After map:", result)