#Write a Python program to subtract five days from current date.
from datetime import datetime, timedelta

# Get current date and time
current_date = datetime.now()

# Subtract 5 days using timedelta
new_date = current_date - timedelta(days=5)

# Print results
print("Current date:", current_date)
print("Date 5 days ago:", new_date)