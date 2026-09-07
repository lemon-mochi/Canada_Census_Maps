 Census Maps 🇨🇦
This is a web application that displays Canadian census data on a map. The design is meant to be simple, so that even non-technical users may easily use. Canada is the greatest country on Earth and it deserves a web application that shows its greatness through our census data. \
The thistle🪻, shamrock☘️, rose🌹 entwine,\
🍁🍁🍁THE MAPLE LEAF FOREVER!!!🍁🍁🍁

# Running locally #
This project requires a somewhat complicated setup in order to run locally. I have listed what must be done.

## Setting up virtual Python environment ##
Make sure you are in the `backend` directory first
```
cd backend/
```
Enter the following in the terminal:
```
# 1. Create the virtual environment (named 'venv')
python3 -m venv venv

# 2. Activate the virtual environment
source venv/bin/activate

# 3. Install packages from the requirements.txt file
pip install -r requirements.txt
```

## Setup boundary files ##

### Download necessary files ###
In order to run the program, you will have to download the boundary files from the official Statistics Canada website.
Census files from [here](https://www12.statcan.gc.ca/census-recensement/2021/geo/sip-pis/boundary-limites/index-eng.cfm).
There is no easy way to download all the needed files at once. You will have to manually download the needed files. I have gathered the needed download links.

[2021 Provinces](https://www12.statcan.gc.ca/census-recensement/2021/geo/sip-pis/boundary-limites/files-fichiers/lpr_000b21a_e.zip)

[2021 Census divisions](https://www12.statcan.gc.ca/census-recensement/2021/geo/sip-pis/boundary-limites/files-fichiers/lcd_000b21a_e.zip)

[2021 Federal electoral districts (2013 Representation Order)](https://www12.statcan.gc.ca/census-recensement/2021/geo/sip-pis/boundary-limites/files-fichiers/lfed000b21a_e.zip)

[2021 Federal electoral districts (2023 Representation Order)](https://open.canada.ca/data/en/dataset/18bf3ea7-1940-46ec-af52-9ba3f77ed708/resource/1f4b018b-a303-48bb-8ea0-10746e7cf435)

[2021 Census subdivisions](https://www12.statcan.gc.ca/census-recensement/2021/geo/sip-pis/boundary-limites/files-fichiers/lcsd000b21a_e.zip)

[2021 Aggregate dissemination areas](https://www12.statcan.gc.ca/census-recensement/2021/geo/sip-pis/boundary-limites/files-fichiers/lada000b21a_e.zip)

[2021 Dissemination areas](https://www12.statcan.gc.ca/census-recensement/2021/geo/sip-pis/boundary-limites/files-fichiers/lda_000b21a_e.zip)

[2016 Provinces](https://www12.statcan.gc.ca/census-recensement/2011/geo/bound-limit/files-fichiers/2016/lpr_000b16a_e.zip)

[2016 Census divisions](https://www12.statcan.gc.ca/census-recensement/2011/geo/bound-limit/files-fichiers/2016/lcd_000b16a_e.zip)

[2016 Federal electoral districts (2013 Representation Order)](https://www12.statcan.gc.ca/census-recensement/2011/geo/bound-limit/files-fichiers/2016/lfed000b16a_e.zip)

[2016 Census subdivisions](https://www12.statcan.gc.ca/census-recensement/2011/geo/bound-limit/files-fichiers/2016/lcsd000b16a_e.zip)

[2016 Aggregate dissemination areas](https://www12.statcan.gc.ca/census-recensement/2011/geo/bound-limit/files-fichiers/2016/lada000b16a_e.zip)

[2016 Dissemination areas](https://www12.statcan.gc.ca/census-recensement/2011/geo/bound-limit/files-fichiers/2016/lda_000b16a_e.zip)

[2011 Provinces](https://www12.statcan.gc.ca/census-recensement/2011/geo/bound-limit/files-fichiers/gpr_000b11a_e.zip)

[2011 Census divisions](https://www12.statcan.gc.ca/census-recensement/2011/geo/bound-limit/files-fichiers/gcd_000b11a_e.zip)

[2011 Federal electoral districts (2003 Representation Order)](https://www12.statcan.gc.ca/census-recensement/2011/geo/bound-limit/files-fichiers/gfed000b11a_e.zip)

[2011 Census subdivisions](https://www12.statcan.gc.ca/census-recensement/2011/geo/bound-limit/files-fichiers/gcsd000b11a_e.zip)

[2011 Census tracts](https://www12.statcan.gc.ca/census-recensement/2011/geo/bound-limit/files-fichiers/gct_000b11a_e.zip)

[2011 Dissemination areas](https://www12.statcan.gc.ca/census-recensement/2011/geo/bound-limit/files-fichiers/gda_000b11a_e.zip)

[2006 Provinces](https://www12.statcan.gc.ca/census-recensement/2011/geo/bound-limit/files-fichiers/gpr_000b06a_e.zip)

[2006 Federal electoral districts (2003 Representation Order)](https://www12.statcan.gc.ca/census-recensement/2011/geo/bound-limit/files-fichiers/gfed000b06a_e.zip)

[2006 Census divisions](https://www12.statcan.gc.ca/census-recensement/2011/geo/bound-limit/files-fichiers/gcd_000b06a_e.zip)

[2006 Census subdivisions](https://www12.statcan.gc.ca/census-recensement/2011/geo/bound-limit/files-fichiers/gcsd000b06a_e.zip)

[2006 Census tracts](https://www12.statcan.gc.ca/census-recensement/2011/geo/bound-limit/files-fichiers/gct_000b06a_e.zip)

[2006 Dissemination areas](https://www12.statcan.gc.ca/census-recensement/2011/geo/bound-limit/files-fichiers/gda_000b06a_e.zip)

After downloading the boundary files, you will have to extract them. Put the extracted directories in `backend/boundaries` directory.
File structure should look like
```
census_maps/ # root directory
├── backend/
├──── boundaries/ # directory
├────── Ida_000b21a_e/ # directory for 2021 Dissemination areas
├──────── Ida_000b21a_e.dbf
├──────── lda_000b21a_e.prj
├──────── lda_000b21a_e.shp
├──────── lda_000b21a_e.shx
├──────── lda_000b21a_e.xml
├────── ... other directories containing boundary definitions
├──── ... other files and directories in backend/
├── frontend/
├──── ... files in frontend/ directory
├── .gitignore
├── README.md # this file
```

The official Statistics Canada website has boundary files for the 2001 census but they are not available in the `.shp` format. I was able to find an alternative source that has `.geojson` files that represent the boundaries. [Abacus Data Network, Statistics Canada Open License](https://abacus.library.ubc.ca/dataverse/statcan-public). The next step shows how to convert the `.shp` files into `.geojson`. Since the files from the Abacus Data Network are already in the `.geojson` format, you may put them in the `backend/geojson/` directory, after extracting the `.zip`. The way you download files using the website is too complicated. To simplify the process, I have put the `.zip` files into my Google Drive, where you may download it.

[2001 All geographies](https://drive.google.com/file/d/1LtJQ5LADBmt3HlxsxC6UBjUkVJEskxbM/view?usp=sharing)

After extracting the `.zip` file, you will see a `MANIFEST.txt` file, and a directory called `Data`. Place both of them into the `backend/geojson/{census_year}` directory, where `{census_year}` matches the census year of the downloaded file.

### Converting .shp files to .geojson ###
To create the `.geojson` files needed to run the application, run the `create_geojson_files.py` program. This will run through all the directories in the `boundaries/` directory and create `.geojson` files in the `backend/geojson` directory. This will take a few minutes to run.
```
python3 create_geojson_files.py
```

### Implement Vector Tiles ###

The boundaries for the census subdivions, census tracts, and dissemination areas are very small. The program cannot handle all of them. To deal with this, you will have to use vector tiles. This uses `tippecanoe`, which will need to be installed.
```
git clone https://github.com/felt/tippecanoe.git
cd tippecanoe
make -j
sudo make install
```
Make sure the `convert_boundaries.sh` file is executable.
```
chmod +x convert_boundaries.sh
```

Then, run the `convert_boundaries.sh` file in the `backend/` directory to convert all the `.geojson` files into the vector tiles. This will take a few minutes.
```
./convert_boundaries.sh
```

## Setup census data ##

#### Download necessary files ###
You will also need to download the files containing census data. These files are very large and will take a while to download. I have gathered the needed download links.

[2021 Canada, provinces, territories, census divisions (CDs), census subdivisions (CSDs) and dissemination areas (DAs)](https://www12.statcan.gc.ca/census-recensement/2021/dp-pd/prof/details/download-telecharger/comp/GetFile.cfm?Lang=E&FILETYPE=CSV&GEONO=006)

[2021 Federal electoral districts (2013 Representation Order)](https://www12.statcan.gc.ca/census-recensement/2021/dp-pd/prof/details/download-telecharger/comp/GetFile.cfm?Lang=E&FILETYPE=CSV&GEONO=010)

[2021 Federal electoral districts (2023 Representation Order)](https://www12.statcan.gc.ca/census-recensement/2021/dp-pd/prof/details/download-telecharger/comp/GetFile.cfm?Lang=E&FILETYPE=CSV&GEONO=029)

[2021 Aggregate dissemination areas](https://www12.statcan.gc.ca/census-recensement/2021/dp-pd/prof/details/download-telecharger/comp/GetFile.cfm?Lang=E&FILETYPE=CSV&GEONO=012)

[2016 Canada, provinces, territories, census divisions (CDs), census subdivisions (CSDs) and dissemination areas (DAs)](https://www12.statcan.gc.ca/census-recensement/2016/dp-pd/prof/details/download-telecharger/comp/GetFile.cfm?Lang=E&FILETYPE=CSV&GEONO=044)

[2016 Federal electoral districts (2013 Representation Order)](https://www12.statcan.gc.ca/census-recensement/2016/dp-pd/prof/details/download-telecharger/comp/GetFile.cfm?Lang=E&FILETYPE=CSV&GEONO=045)

[2016 Aggregate dissemination areas](https://www12.statcan.gc.ca/census-recensement/2016/dp-pd/prof/details/download-telecharger/comp/GetFile.cfm?Lang=E&FILETYPE=CSV&GEONO=050)

You do not have to extract these `.zip` files. Simply put them in `backend/census_data`.


## Create the parquet files that contain Census data ##
Parquet files are a compressed data format better for high-performance analytics. For this project, it is necessary to convert the `.csv` files into Parquet files for faster retrieval.
Run the `create_parquet_files.py` program to create the needed Parquet files. Running this program will create the `temp_parquet_data/` directory within `backend/`. This wil take a few minutes.
```
python3 create_parquet_files.py
```

Next you will want to simplify the `.parquet` file. To do this, run the following:
```
python3 cleanup_parquet.py
```
This will create the `parquet_data/` directory. This is the directory the server will use to retrieve data.

# Running the backend #
To run the backend server,
```
uvicorn main:app --reload
```