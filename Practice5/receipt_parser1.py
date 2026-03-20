# Import the regular expressions module
# It allows us to search text using patterns
import re

# Import JSON module
# It will help us print the final result in structured format
import json


# Open the receipt text file in read mode
# encoding="utf-8" is needed to correctly read non-English characters
file = open("raw.txt", "r", encoding="utf-8")

# Read the entire file and store it in variable "text"
text = file.read()


# -------------------------------
# EXTRACT PRODUCT NAMES
# -------------------------------

# This regex finds product names in the receipt
# Pattern explanation:
# \n      → new line
# \d+\.   → item number like "1." or "2."
# \n      → next line
# ([^\n]+) → capture everything until next new line (product name)
products = re.findall(r'\n\d+\.\n([^\n]+)', text)


# -------------------------------
# EXTRACT QUANTITY AND PRICE
# -------------------------------

# This regex extracts items like:
# 2 x 500,00
# 1 x 350,00
#
# Pattern explanation:
# (\d+)           → quantity (one or more digits)
# \s*             → optional spaces
# x               → multiplication symbol
# \s*             → optional spaces
# ([\d ]*,\d{2})  → price (digits, optional spaces, comma, two decimals)
items = re.findall(r'(\d+,\d+)\s*x\s*([\d ]+,\d{2})', text)


# -------------------------------
# EXTRACT DATE
# -------------------------------

# Pattern matches dates like:
# 18.04.2019
date = re.search(r'\d{2}\.\d{2}\.\d{4}', text)


# -------------------------------
# EXTRACT TIME
# -------------------------------

# Pattern matches times like:
# 11:13:58
time = re.search(r'\d{2}:\d{2}:\d{2}', text)


# -------------------------------
# FIND PAYMENT METHOD
# -------------------------------

# Check if the phrase "Банковская карта" exists in receipt
# If found, payment was made by bank card
payment = re.search(r'Банковская карта', text)


# -------------------------------
# PREPARE LISTS FOR CALCULATIONS
# -------------------------------

# List to store quantities
quantities = []

# List to store unit prices
unit_prices = []

# List to store calculated item prices
calculated_prices = []


# -------------------------------
# PROCESS EACH ITEM
# -------------------------------

# Loop through every match found in "items"
for qty, price in items:

    # Remove spaces from price (example: "1 200,00")
    # Replace comma with dot to make Python understand decimal numbers
    clean_price = price.replace(" ", "").replace(",", ".")

    # Convert quantity from string to integer
    quantity = float(qty.replace(",", "."))

    # Convert price from string to float number
    unit_price = float(clean_price)

    # Multiply quantity by unit price to get total item price
    total_price = quantity * unit_price

    # Store values in lists
    quantities.append(quantity)
    unit_prices.append(round(unit_price, 2))
    calculated_prices.append(round(total_price, 2))


# -------------------------------
# CREATE FINAL RESULT STRUCTURE
# -------------------------------

# Store all extracted information in dictionary
result = {

    # List of product names
    "products": products,

    # Quantities of each product
    "quantities": quantities,

    # Unit price of each product
    "unit_prices": unit_prices,

    # Calculated price (quantity × unit price)
    "calculated_prices": calculated_prices,

    # Extracted date if found
    "date": date.group() if date else "",

    # Extracted time if found
    "time": time.group() if time else "",

    # Payment method
    "payment_method": "Bank Card" if payment else "Unknown",

    # Final total of the receipt
    "total": round(sum(calculated_prices), 2)
}


# -------------------------------
# PRINT RESULT
# -------------------------------

# Convert dictionary to JSON and print it nicely
# indent=4 makes it readable
# ensure_ascii=False keeps non-English characters readable
print(json.dumps(result, indent=4, ensure_ascii=False))