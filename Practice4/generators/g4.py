#Implement a generator called squares to yield the square of all numbers from (a) to (b). Test it with a "for" loop and print each of the yielded values.
# Generator function
def squares(a, b):
    for i in range(a, b + 1):
        yield i * i


# Test
for num in squares(2, 6):
    print(num)