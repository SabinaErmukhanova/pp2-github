#Write a Python program to print yesterday, today, tomorrow.
from datetime import datetime, timedelta

# Get today's date
today = datetime.now()

# Calculate yesterday and tomorrow
yesterday = today - timedelta(days=1)
tomorrow = today + timedelta(days=1)

# Print results
print("Yesterday:", yesterday)
print("Today:", today)
print("Tomorrow:", tomorrow)