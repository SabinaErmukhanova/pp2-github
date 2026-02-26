Write a program using generator to print the even numbers between 0 and n in comma separated form where n is input from console.
# Generator function
def even_numbers(n):
    for i in range(n + 1):
        if i % 2 == 0:
            yield i


# Input from user
n = int(input("Enter a number: "))

# Convert generator to list and print comma separated
print(",".join(str(num) for num in even_numbers(n)))