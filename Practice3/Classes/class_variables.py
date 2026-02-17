# Difference between class variables and instance variables
class Car:
    # Class variable (shared by ALL objects)
    wheels = 4

    def __init__(self, brand):
        # Instance variable (belongs to each object separately)
        self.brand = brand


# Create two objects
car1 = Car("BMW")
car2 = Car("Toyota")

# Each object has its own brand
print("Car1 brand:", car1.brand)
print("Car2 brand:", car2.brand)

# But wheels is shared by all cars
print("Car wheels:", Car.wheels)