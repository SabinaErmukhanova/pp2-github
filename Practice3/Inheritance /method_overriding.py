# Parent class
class Animal:
    def speak(self):
        print("Animal sound")


# Child class overrides speak()
class Cat(Animal):
    # Same method name as parent
    def speak(self):
        print("Meow")


# Create Cat object
cat1 = Cat()

# Cat uses its own speak() method
# Parent version is replaced
cat1.speak()