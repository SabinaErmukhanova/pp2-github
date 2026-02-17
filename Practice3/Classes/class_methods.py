# __init__ runs automatically when object is created.
# It is used to initialize object data.

class Person:
    def __init__(self, name, age):
        # self refers to the current object
        # We store values inside the object
        self.name = name
        self.age = age


# Create object and pass values
person1 = Person("Sabina", 19)

# The values were stored automatically
print("Name:", person1.name)
print("Age:", person1.age)