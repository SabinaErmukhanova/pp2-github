# This file shows how methods work inside a class.
class Student:
    def __init__(self, name):
        # Save student name
        self.name = name

    # This is an instance method
    # Every object of Student can use it
    def greet(self):
        # self.name means we use data from THIS object
        print("Hello, I am", self.name)


# Create object
student1 = Student("Sabina")

# Call method
student1.greet()