def subtract(a, b):
    return a - b

def get_full_name(first, last):
    return first + " " + last

def maximum(a, b):
    if a > b:
        return a
    return b

# Test
print("10 - 3 =", subtract(10, 3))

full_name = get_full_name("Sabina", "Ermukhanova")
print("Full name:", full_name)

print("Max:", maximum(7, 12))