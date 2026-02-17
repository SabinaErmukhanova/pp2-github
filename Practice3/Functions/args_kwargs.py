# Using *args and **kwargs
# *args example
def sum_all(*numbers):
    total = 0
    for n in numbers:
        total += n
    return total

# **kwargs example
def show_info(**info):
    for key, value in info.items():
        print(key, ":", value)

# Test
print("Sum:", sum_all(1, 2, 3, 4))

show_info(name="Sabina", age=19, city="Almaty")