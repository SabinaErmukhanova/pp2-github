# A class is a blueprint for creating objects.
class Person:
    # These are class attributes (shared by all objects)
    name = ""
    age = 0


# Create first object from Person class
person1 = Person()

# Assign values to object attributes
person1.name = "Sabina"
person1.age = 19

# Print object data
print("Name:", person1.name)
print("Age:", person1.age)