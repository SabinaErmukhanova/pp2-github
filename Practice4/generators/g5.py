#Implement a generator that returns all numbers from (n) down to 0.
# Generator function
def countdown(n):
    while n >= 0:
        yield n
        n -= 1


# Test
for num in countdown(5):
    print(num)