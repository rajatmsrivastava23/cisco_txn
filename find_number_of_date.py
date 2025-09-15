
from datetime import datetime

# Input dates
date1 = '01-08-2025'
date2 = '31-08-2025'

# Get today's date as reference (D-Day)
d_day = datetime.today().date()

# Convert input strings to date objects
date_obj1 = datetime.strptime(date1, '%d-%m-%Y').date()
date_obj2 = datetime.strptime(date2, '%d-%m-%Y').date()

# Calculate days difference from D-Day
d_diff1 = (d_day - date_obj1).days
d_diff2 = (d_day - date_obj2).days

# Format and print
print(f"{date1} -> D-{d_diff1}")
print(f"{date2} -> D-{d_diff2}")
