#Write a Python program to calculate the area of regular polygon.
#Formula: Area = (n * s²) / (4 * tan(π/n))
import math

# Input values
n = int(input("Input number of sides: "))
s = float(input("Input the length of a side: "))

# Calculate area
area = (n * s * s) / (4 * math.tan(math.pi / n))

# Print result
print("The area of the polygon is:", round(area))