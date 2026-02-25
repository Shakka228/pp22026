from datetime import datetime, timedelta

# 1️ Subtract five days from current date
current_date = datetime.now()
five_days_ago = current_date - timedelta(days=5)

print("Current date:", current_date)
print("Five days ago:", five_days_ago)
print("-" * 40)

# 2️ Print yesterday, today, tomorrow
today = datetime.now()
yesterday = today - timedelta(days=1)
tomorrow = today + timedelta(days=1)

print("Yesterday:", yesterday)
print("Today:", today)
print("Tomorrow:", tomorrow)
print("-" * 40)

# 3️ Drop microseconds from datetime
now = datetime.now()
without_microseconds = now.replace(microsecond=0)

print("Original datetime:", now)
print("Without microseconds:", without_microseconds)
print("-" * 40)

# 4  Calculate difference between two dates in seconds
date1 = datetime(2026, 2, 20, 12, 0, 0)
date2 = datetime(2026, 2, 25, 15, 30, 0)

difference = date2 - date1

print("Difference in seconds:", difference.total_seconds())
