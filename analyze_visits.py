import pandas as pd

# 1. Load and structure the data:
#    - Read the processed CSV file
#    - Convert visit_date to datetime
#    - Sort by patient_id and visit_date

# 2. Add insurance information:
#    - Read insurance types from `insurance.lst`
#    - Randomly assign (but keep consistent per patient_id)
#    - Generate visit costs based on insurance type:
#      - Different plans have different effects on cost
#      - Add random variation

# 3. Calculate summary statistics:
#    - Mean walking speed by education level
#    - Mean costs by insurance type
#    - Age effects on walking speed

# Tips:

# - Use pandas for data manipulation
#   - `pd.read_csv()` to load data
#   - `pd.to_datetime()` for dates
#   - `.groupby()` for aggregations
# - Expected data types:
#   - `patient_id`: string
#   - `visit_date`: datetime
#   - `age`: float
#   - `education_level`: string/category
#   - `walking_speed`: float
# - Handle missing data appropriately
# - Consider seasonal variations in the data

df = pd.read_csv('ms_data.csv', delimiter=',')
df.visit_date = pd.to_datetime(df.visit_date)
df = df.sort_values(by=['patient_id', 'visit_date']) # it's already sorted btw
# print(df.info())
