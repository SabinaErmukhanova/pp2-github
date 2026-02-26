#Write a Python program to calculate two date difference in seconds.
from datetime import datetime

# Create two date objects
date1 = datetime(2026, 1, 1, 12, 0, 0)
date2 = datetime(2026, 1, 2, 12, 0, 0)

# Calculate difference
difference = date2 - date1

# Convert difference to seconds
seconds = difference.total_seconds()

print("Difference in seconds:", seconds)