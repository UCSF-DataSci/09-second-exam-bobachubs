#!/bin/bash

input_file="ms_data_dirty.csv"
output_file="ms_data.csv"
lst_file="insurance.lst"

# awk -F ',' '
#     # skip comments
#     !/#/ && NF > 0 {
#         # replace ,, with , in each line
#         gsub(/,,/, ",")
#         # keep lines that have > 0 number of fields, print the line
#         if ($6 >=2 && $6 <= 8) print $1 "," $2 "," $4 "," $5 "," $6
#     }
# ' "$input_file" > "$output_file"

{
    grep -v '^#' "$input_file" |         
    sed '/^$/d' | #empty lines
    sed 's/,,/,/g' |
    awk -F ',' '
    NR == 1 {print $1 "," $2 "," $4 "," $5 "," $6}                
    NR > 1 {                             
        if ($6 >= 2.0 && $6 <= 8.0)
        {print $1 "," $2 "," $4 "," $5 "," $6}
    }' 
} > "$output_file"

echo "data cleaned and saved to $output_file"

echo "insurance_type" > lst_file
echo "Health" >> lst_file
echo "Dental" >> lst_file
echo "Vision" >> lst_file
echo "Car" >> lst_file
echo "Life" >> lst_file

echo "insurance labels added to $lst_file"

total_rows=$(tail -n +2 "$output_file" | wc -l) #skip header

echo "Total number of visits: $total_rows"
echo "First few records: "

head -n 5 $output_file
