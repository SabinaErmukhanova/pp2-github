# Parent class
class Animal:
    def __init__(self, name):
        # Store name in object
        self.name = name


# Child class
class Dog(Animal):
    def __init__(self, name, breed):
        # Call parent __init__ to set name
        super().__init__(name)

        # Add new attribute only for Dog
        self.breed = breed


# Create Dog object
dog1 = Dog("Rex", "Labrador")

# Name came from parent
print("Name:", dog1.name)

# Breed came from child
print("Breed:", dog1.breed)