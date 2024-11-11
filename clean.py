import pandas as pd
import numpy as np

# df_csv = 'ms_data_dirty.csv'
# with open(df_csv, 'r') as f:
#     lines = f.readlines()

# with open ('ms_data.csv', 'w') as f:
#     for line in lines:
#         if line.strip():
#             if '#' in line:
#                 continue
#             if ',,' in line:
#                 line = line.replace(',,', ',')
#             # line = line.replace('\n', '')
#             f.write(line)

df = pd.read_csv('ms_data.csv', delimiter=',')
# print(df.duplicated().sum())
print(df.describe())