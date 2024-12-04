import pandas as pd
import numpy as np

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

# 1. 
df = pd.read_csv('ms_data.csv', delimiter=',')
df.visit_date = pd.to_datetime(df.visit_date)
df = df.sort_values(by=['patient_id', 'visit_date']) # it's already sorted btw
df.education_level = df.education_level.astype("category")
# print(df.info())

#2. 
insurances = []
with open('insurance.lst', 'r') as f:
    for line in f:
        insurances.append(line.strip())
insurances.pop(0)

insurance_assignments = pd.Series(
    np.random.choice(insurances, size=len(df['patient_id'].unique()), replace=True),
    index=df['patient_id'].unique()
)

df['insurance_type'] = df['patient_id'].map(insurance_assignments)

cost_map = {
    'Health': 150,
    'Dental': 100,
    'Vision': 80,
    'Home': 120,
    'Car': 90,
    'Travel': 50,
    'Life': 75
}

cost_plans = {
    'basic': 1,
    'premium': 1.5,
    'platinum': 1.75
}

cost_assignments = pd.Series(
    np.random.choice(list(cost_plans), size=len(df['insurance_type'].unique()), replace=True),
    index=df['insurance_type'].unique()
)

df['cost_plan'] = df['insurance_type'].map(cost_assignments)

variation = .1

def generate_visit_costs(row):
    base_cost = cost_map[row['insurance_type']]
    multiplier = cost_plans[row['cost_plan']]
    age_factor = 1 + (row['age'] - min(df.age)) / 100
    var = np.random.uniform(1-variation, 1+variation)
    return round(base_cost * multiplier * var * age_factor, 2)

df['visit_cost'] = df.apply(generate_visit_costs, axis=1)

df = df.drop(['cost_plan'], axis=1)

# df.to_csv('test.csv', index=False)

# 3.
print("Mean walking speed by education level: ", df.groupby('education_level')['walking_speed'].mean())
print("Mean visit costs by insurance type: ", df.groupby('insurance_type')['visit_cost'].mean())
print("Age correlation with walking speed: ", df['age'].corr(df['walking_speed']))

