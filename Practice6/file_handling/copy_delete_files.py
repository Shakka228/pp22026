import shutil
import os

# Copy file
shutil.copy("sample.txt", "sample_copy.txt")
print("File copied.")

# Backup file
shutil.copy("sample.txt", "sample_backup.txt")
print("Backup created.")

# Delete file safely
if os.path.exists("sample_copy.txt"):
    os.remove("sample_copy.txt")
    print("File deleted.")
else:
    print("File does not exist.")
