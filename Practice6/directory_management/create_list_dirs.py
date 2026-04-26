import os

# Create directories
os.makedirs("test_dir/sub_dir", exist_ok=True)

# Current directory
print("Current directory:", os.getcwd())

# List files and folders
print("Directory contents:")
for item in os.listdir():
    print(item)
