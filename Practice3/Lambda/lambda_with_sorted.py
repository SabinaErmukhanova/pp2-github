students = [("Tair", 85), ("Ali", 92), ("Dana", 78)]

# Sort by score
sorted_students = sorted(students, key=lambda x: x[1])

print("Sorted by score:", sorted_students)