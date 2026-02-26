#Write a Python program to convert degree to radian.
import math

# Input degree
degree = float(input("Input degree: "))

# Convert to radians
radian = degree * (math.pi / 180)

# Print result
print("Output radian:", round(radian, 6))