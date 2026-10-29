# Problems and Solutions #
This `.md` file documents problems encountered while developing the application and the solutions I used.

## 2016 .csv column names and "None" string
The input files for 2016 census data had different column headers. And the file for census subdivisions had an extra column. The solution was to create my own column names rather than relying on the column headers, and to handle the special case for census subdivisions. There was another problem that was much harder to track down. Some of the characteristics had the name: "None". For example, for official languages, if a respondent did not speak English nor French, they would be counted in the "None" category. This was converting the string to Python's `None` type. I solved this by setting `keep_default_na=False`.

## 2011 characteristics
For 2011 and every earlier census, there is no id for the characteristics given. This means I would have to create my own characteristic id system. For 2011, this was simple. I simply had to download sample `.csv` files that had all the characteristic names (these are in `backend/2011_sample`). Then, I had the jupyter notebook read the sample `.csv` files to create the characteristic system. 

## 2011 .csv columns
The input files for 2011 census data was inconsistent. Some files had an extra line at the top while others started with the column headers. Although each file had a different number of columns, I was able to invesestigate and find the pattern needed to extract the columns needed for the `.parquet` file. The following code block shows these problems and the solution.
```
# sometimes, there is an extra row at the top
df = pd.read_csv(f, nrows=1, header=None, encoding='latin1')
top_left_value = df.iat[0, 0]

if top_left_value != "Geo_Code":
    # there is a useless row at the top
    header = 1
else:
    header = 0

f.seek(0)
"""
The 2011 census data has different number of columns depending on the geographic level.
After analyzing the .csv file structure, I noticed that the name of the geography usually
appears one column to the left of the 'Topic' column. 
"""

all_columns = pd.read_csv(
    f,
    header=header,
    nrows=0,
    encoding='latin1'
).columns.tolist()


topic_col_idx = all_columns.index('Topic')

geo_index = topic_col_idx - 1
has_type_col_flag = False
has_gnr_col_flag = False

if all_columns[geo_index] == "GNR":
    has_gnr_col_flag = True
    # remove the GNR column
    geo_index -= 1

if all_columns[geo_index].lower().endswith("type"):
    has_type_col_flag = True
    # type column. No need to keep
    geo_index -= 1

if geo_index > 1:
    columns_to_skip = [1, geo_index - 1]
else:
    columns_to_skip = []

columns_to_keep = [
    i for i in range(len(all_columns))
    if i not in columns_to_skip
]

# do not need to keep the type column
if has_type_col_flag and has_gnr_col_flag:
    columns_to_keep.remove(topic_col_idx - 1)
    columns_to_keep.remove(topic_col_idx - 2)

elif has_type_col_flag:
    columns_to_keep.remove(topic_col_idx - 1)

elif has_gnr_col_flag:
    columns_to_keep.remove(topic_col_idx - 1)


# do not need topic, note, or flags
columns_to_keep.remove(topic_col_idx)
# note is two to the right of topic
columns_to_keep.remove(topic_col_idx + 2)
# flag total is two to the right of topic
columns_to_keep.remove(topic_col_idx + 4)
# flag male is two to the right of flag total
columns_to_keep.remove(topic_col_idx + 6)
# flag female is two to the right of male total
columns_to_keep.remove(topic_col_idx + 8)
```