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

## 2011 NHS data for DAs
Read [2011_NHS_Data.md](2011_NHS_Data.md) for this information.

## 2006-1996 .XML files
The `.XML` files were extremely large. Some files were over 40 GB when unzipped. The solution was to temporarily unzip every file one by one, create a temporary parquet file, delete the temporary `.XML` file, then merge the parquet files together once everything was done processing. Each `.XML` file had its own characteristic id system. This means the characteristic ids mapped to different characteristics for each file. I had to create my own characteristic system. To do this, I downloaded a sample `.csv` file for each geographic level from Statistics Canada. Then I took the list of characteristics from each `.csv` file and compared them to each other in excel. Then I assigned a number to each characteristic to act as its characteristic's id.

## 1991-1981 .IVT files
For the 1991, 1986, and 1981 census, the data was only available in the `.IVT` format. This is a proprietary data format that is used by Statistics Canada. It does not work with Pandas or PySpark. Luckily, I was able to use [beyond 20/20 browser](http://www.beyond2020.com/media/downloads/SC/ProBrowser.exe) to convert it to the `.csv` format for most of the data. I was not able to convert the data for 1991 enumeration areas as the data was too large to convert to `.csv`. Once again, there was no consistent characteristic id system, meaning I had to create one by using excel.

## Geographic mappings
This program needs to match the geographic information from the database to the geogrpahic information in the vector tiles. The basic idea is the take the information from vector tiles that are currently visible on screen, convert them into a code that the backend can understand, then convert them back so the data can be mapped to the vector tile. I used [pmtiles.io](https://pmtiles.io) to analyze the vector tiles. For the 2021 census, I was able to use `DGUID` to map easily for all geographic levels exept for federal electoral districts (2023 representation order). For older census years, it was not as simple as I would have to reconstruct codes. The file `frontend/src/constants/GeoCodeIDs.jsx` contains information about which feature of a vector tile should be used as the geographic code to retrieve data from the database. The file `frontend/src/constants/GeoMappings.jsx` contains the functions needed to convert the vector tiles properties into geographic codes.

## 1991 census tracts
1991 census tracts was a special case. I had to reconstruct the code using the 'CA', 'PROV', and 'CT_CODE' features. This was a problem. The source `.geojson` for 1991 census tracts came in two separate files. The `l91ctpct_geojson` file contained the 'CA', 'PROV' and 'CT_CODE'. However, the `l91ct_geojson` file contained the 'CA_CTNAME' feature which is needed to uniquely identify each census tract. This means I would have to use both files. So, I wrote a python script, `backend/geographies/merge_split_geojson.py` to merge the two `geojson` files for 1991 census tracts. Then, another problem arose. For core cities of metropolitan areas (like Toronto, Vancouver, Montreal, etc.), the 'CT_NAME' always begins with a '0'. In the `l91ct_geojson` file, there was always a leading 0. In the `l91ctpct_geojson` file, there was never a leading zero. For example, in Vancouver, the 'CT_NAME' could be '052.00' and '52.00'. So, in order to merge them properly I had to add a function to pad leading zeros.
```
def normalize_ct_name(series):
    return series.astype(str).str.zfill(6)
```
