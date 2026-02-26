#Write a Python program to calculate the area of a trapezoid.
#Formula: Area = (base1 + base2) * height / 2
# Input values
height = float(input("Height: "))
base1 = float(input("Base, first value: "))
base2 = float(input("Base, second value: "))

# Calculate area
area = (base1 + base2) * height / 2

# Print result
print("Area of trapezoid:", area)