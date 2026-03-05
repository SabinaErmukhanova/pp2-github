# Import regular expressions module
# This module allows us to search text using patterns
import re

# Import json module
# We use it to print the final result in a structured JSON format
import json


# Open the receipt file (raw.txt) in read mode
# encoding="utf-8" ensures correct reading of special characters
file = open("raw.txt", "r", encoding="utf-8")

# Read the entire file content and store it in the variable "text"
text = file.read()


# EXTRACT PRICES 

# This regex finds prices like:
# 1 200,00
# 850,50
# Explanation:
# \d          → first digit
# [\d ]*      → any digits or spaces
# ,\d{2}      → comma and exactly two decimal digits
prices = re.findall(r'\d[\d ]*,\d{2}', text)


#  EXTRACT PRODUCT NAMES 

# This regex extracts product names from the receipt
# Explanation:
# \n\d+\.     → line break followed by item number (1., 2., 3.)
# \n([^\n]+)  → next line contains the product name
products = re.findall(r'\n\d+\.\n([^\n]+)', text)


#  EXTRACT DATE 

# This pattern finds dates in format:
# DD.MM.YYYY
date = re.search(r'\d{2}\.\d{2}\.\d{4}', text)


#  EXTRACT TIME 

# This pattern finds time in format:
# HH:MM:SS
time = re.search(r'\d{2}:\d{2}:\d{2}', text)


#  FIND PAYMENT METHOD 

# Look for the phrase "Банковская карта" in the receipt
# If found, it means payment was done by bank card
payment = re.search(r'Банковская карта', text)


#  CLEAN PRICE VALUES 

# Create empty list to store numeric prices
clean_prices = []

# Loop through each extracted price
for p in prices:
    
    # Remove spaces in numbers (example: "1 200,00")
    # Replace comma with dot so Python can convert it to float
    value = p.replace(" ", "").replace(",", ".")
    
    # Convert string price to float and add to list
    clean_prices.append(float(value))


#  CALCULATE TOTAL

# Sum all prices
total = sum(clean_prices)


#  CREATE STRUCTURED RESULT 

# Create dictionary to store extracted information
result = {

    # List of product names
    "products": products,

    # Original prices as text
    "prices": prices,

    # Extracted date (if found)
    "date": date.group() if date else "",

    # Extracted time (if found)
    "time": time.group() if time else "",

    # Payment method detection
    "payment_method": "Bank Card" if payment else "Unknown",

    # Calculated total amount
    "calculated_total": round(total, 2)
}


# PRINT RESULT 

# Print result in formatted JSON
# indent=4 makes it readable
# ensure_ascii=False allows non-English characters
print(json.dumps(result, indent=4, ensure_ascii=False))