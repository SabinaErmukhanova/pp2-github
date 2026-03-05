# Import the regular expression module
# This module allows us to search text using patterns
import re
# ------------------------------
# 1. Match 'a' followed by zero or more 'b'
# ------------------------------

text1 = "a ab abb abbb ac"       # Example string containing different patterns
pattern1 = r'ab*'                # Regex pattern: 'a' followed by zero or more 'b'

result1 = re.findall(pattern1, text1)  # Find all matches of the pattern in the string

print("1. Matches of 'a' followed by zero or more 'b':")  # Print description
print(result1)                                            # Print results
print()                                                   # Empty line for readability

# ------------------------------
# 2. Match 'a' followed by two to three 'b'
# ------------------------------

text2 = "ab abb abbb abbbb"      # Example string
pattern2 = r'ab{2,3}'            # Pattern: 'a' followed by 2 or 3 'b'

result2 = re.findall(pattern2, text2)   # Search for pattern in the string

print("2. Matches of 'a' followed by 2 to 3 'b':")  # Print description
print(result2)                                      # Print matches
print()

# ------------------------------
# 3. Find lowercase words joined with underscore
# ------------------------------

text3 = "hello_world test_case Example_Test"   # Example text containing different cases
pattern3 = r'[a-z]+_[a-z]+'                    # Pattern: lowercase letters + "_" + lowercase letters

result3 = re.findall(pattern3, text3)          # Find matching patterns

print("3. Lowercase words joined with underscore:")
print(result3)
print()

# ------------------------------
# 4. Find uppercase letter followed by lowercase letters
# ------------------------------

text4 = "London paris Astana NewYork"     # Example string
pattern4 = r'[A-Z][a-z]+'                 # Pattern: one uppercase letter followed by lowercase letters

result4 = re.findall(pattern4, text4)     # Find matches

print("4. Uppercase letter followed by lowercase letters:")
print(result4)
print()

# ------------------------------
# 5. Match 'a' followed by anything ending in 'b'
# ------------------------------

text5 = "ab acb a123b axxb"     # Example string
pattern5 = r'a.*b'              # Pattern: 'a', then any characters, ending with 'b'

result5 = re.findall(pattern5, text5)  # Find all matches

print("5. 'a' followed by anything ending with 'b':")
print(result5)
print()

# ------------------------------
# 6. Replace spaces, commas, and dots with colon
# ------------------------------

text6 = "Hello, world. Python is great"   # Example sentence
pattern6 = r'[ ,.]'                       # Pattern matching space, comma, or dot

result6 = re.sub(pattern6, ":", text6)    # Replace matches with colon

print("6. Replace spaces, commas, and dots with colon:")
print(result6)
print()

# ------------------------------
# 7. Convert snake_case to camelCase
# ------------------------------

text7 = "snake_case_string"           # Example snake_case string

parts = re.split('_', text7)          # Split string at underscore

first_word = parts[0]                 # First word remains lowercase

camel_case = first_word + ''.join(word.capitalize() for word in parts[1:])  
# Capitalize first letter of remaining words and join them

print("7. snake_case to camelCase:")
print(camel_case)
print()

# ------------------------------
# 8. Split string at uppercase letters
# ------------------------------

text8 = "SplitThisStringNow"          # Example camel case string
pattern8 = r'[A-Z][^A-Z]*'            # Pattern: uppercase letter followed by characters until next uppercase

result8 = re.findall(pattern8, text8) # Extract words

print("8. Split string at uppercase letters:")
print(result8)
print()

# ------------------------------
# 9. Insert spaces between capitalized words
# ------------------------------

text9 = "InsertSpacesBetweenWords"    # Example string

result9 = re.sub(r'([A-Z])', r' \1', text9)  # Add space before each capital letter

result9 = result9.strip()             # Remove space at the beginning

print("9. Insert spaces before capital letters:")
print(result9)
print()

# ------------------------------
# 10. Convert camelCase to snake_case
# ------------------------------

text10 = "camelCaseStringExample"     # Example camelCase string

snake_case = re.sub(r'([A-Z])', r'_\1', text10)  # Add underscore before capital letters

snake_case = snake_case.lower()      # Convert entire string to lowercase

print("10. camelCase to snake_case:")
print(snake_case)
print()