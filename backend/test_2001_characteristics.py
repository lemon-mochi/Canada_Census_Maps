"""
The 2001 xml files have inconsistent values form DIM0. This file sorts it out.
"""
import pandas as pd

largest_file = "./csv_test/7141820260926085437.CSV"
middle_file = "./csv_test/7285220260926085449.CSV"
smallest_file = "./csv_test/7284920260926085514.CSV"

df_largest = pd.read_csv(largest_file, header=None, skiprows=2, on_bad_lines='skip')
df_middle = pd.read_csv(middle_file, header=None, skiprows=2, on_bad_lines='skip')
df_smallest = pd.read_csv(smallest_file, header=None, skiprows=2, on_bad_lines='skip')

largest_ids = set(df_largest.iloc[:, 0])
middle_ids = set(df_middle.iloc[:, 0])
smallest_ids = set(df_smallest.iloc[:, 0])

all_ids = largest_ids | middle_ids | smallest_ids

comparison = pd.DataFrame({
    "DIM0": sorted(all_ids),
})

comparison["largest"] = comparison["DIM0"].isin(largest_ids)
comparison["middle"] = comparison["DIM0"].isin(middle_ids)
comparison["smallest"] = comparison["DIM0"].isin(smallest_ids)

missing_from_largest = comparison[~comparison["largest"]]
missing_from_middle = comparison[~comparison["middle"]]
missing_from_smallest = comparison[~comparison["smallest"]]

with open("output.txt", "w") as f:
    pd.set_option('display.max_rows', None)

    print("Missing from largest:", file=f)
    print(missing_from_largest["DIM0"], file=f)

    print("Missing from middle:", file=f)
    print(missing_from_middle["DIM0"], file=f)

    print("Missing from smallest:", file=f)
    print(missing_from_smallest["DIM0"], file=f)
