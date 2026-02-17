# Parent class
class Animal:
    def speak(self):
        print("Animal makes a sound")


# Child class inherits from Animal
class Dog(Animal):
    # Dog automatically gets speak() method
    pass


# Create object of Dog
dog1 = Dog()

# Dog can use method from Animal
dog1.speak()