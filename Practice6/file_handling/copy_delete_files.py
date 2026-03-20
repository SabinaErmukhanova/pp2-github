# shutil → used for copying files
import shutil

# os → used for file operations (delete, check existence)
import os

# Copy file: source → destination
shutil.copy("example.txt", "copy_example.txt")

# Check if copied file exists
if os.path.exists("copy_example.txt"):
    
    # Remove (delete) the file
    os.remove("copy_example.txt")