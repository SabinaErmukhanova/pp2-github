#Write a Python program to drop microseconds from datetime.
from datetime import datetime

# Get current date and time
now = datetime.now()

# Remove microseconds
without_microseconds = now.replace(microsecond=0)

# Print result
print("With microseconds:", now)
print("Without microseconds:", without_microseconds)