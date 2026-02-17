# First parent class
class Father:
    def drive(self):
        print("Father can drive")

# Second parent class
class Mother:
    def cook(self):
        print("Mother can cook")

# Child inherits from BOTH classes
class Child(Father, Mother):
    pass


# Create Child object
child1 = Child()

# Child can use methods from both parents
child1.drive()
child1.cook()