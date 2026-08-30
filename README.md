# Census Maps #
This is a web application that displays Canadian census data on a map. The design is meant to be simple, so that even non-technical users may easily use.

## Running locally ##

### Download necessary files ###
In order to run the program, you will have to download the boundary files from the official Statistics Canada website.
Census files from [here](https://www12.statcan.gc.ca/census-recensement/2021/geo/sip-pis/boundary-limites/index-eng.cfm).
There is no easy way to download all the needed files at once. You will have to manually download the needed files. I have gathered the needed download links.

[2021 Provinces](https://www12.statcan.gc.ca/census-recensement/alternative_alternatif.cfm?l=eng&dispext=zip&teng=lpr_000b21a_e.zip&k=%20%20%20130596&loc=//www12.statcan.gc.ca/census-recensement/2021/geo/sip-pis/boundary-limites/files-fichiers/lpr_000b21a_e.zip)

[2021 Census divisions](https://www12.statcan.gc.ca/census-recensement/alternative_alternatif.cfm?l=eng&dispext=zip&teng=lcd_000b21a_e.zip&k=%20%20%20136594&loc=//www12.statcan.gc.ca/census-recensement/2021/geo/sip-pis/boundary-limites/files-fichiers/lcd_000b21a_e.zip)

[2021 Federal electoral districts (2013 Representation Order)](https://www12.statcan.gc.ca/census-recensement/alternative_alternatif.cfm?l=eng&dispext=zip&teng=lfed000b21a_e.zip&k=%20%20%20136181&loc=//www12.statcan.gc.ca/census-recensement/2021/geo/sip-pis/boundary-limites/files-fichiers/lfed000b21a_e.zip)

[2021 Census subdivisions](https://www12.statcan.gc.ca/census-recensement/alternative_alternatif.cfm?l=eng&dispext=zip&teng=lcsd000b21a_e.zip&k=%20%20%20152326&loc=//www12.statcan.gc.ca/census-recensement/2021/geo/sip-pis/boundary-limites/files-fichiers/lcsd000b21a_e.zip)

[2021 Census tracts](https://www12.statcan.gc.ca/census-recensement/alternative_alternatif.cfm?l=eng&dispext=zip&teng=lct_000b21a_e.zip&k=%20%20%20%2013089&loc=//www12.statcan.gc.ca/census-recensement/2021/geo/sip-pis/boundary-limites/files-fichiers/lct_000b21a_e.zip)

[2021 Dissemination areas](https://www12.statcan.gc.ca/census-recensement/alternative_alternatif.cfm?l=eng&dispext=zip&teng=lda_000b21a_e.zip&k=%20%20%20192424&loc=//www12.statcan.gc.ca/census-recensement/2021/geo/sip-pis/boundary-limites/files-fichiers/lda_000b21a_e.zip)


After downloading the files, you will have to extract them. Create a directory called `boundaries` within the `backend` directory. Put the extracted directories in there.
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

### Setting up virtual Python environment ###
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

### Converting .shp files to .geojson ###
To create the `.geojson` files needed to run the application, run the `create_geojson_files.py` program. This will run through all the directories in the `boundaries/` directory and create `.geojson` files in the root directory.
```
python3 create_geojson_files.py
```

### Implement Vector Tiles ###
The boundaries for the census subdivions, census tracts, and dissemination areas are very small. The program cannot handle all of them. To deal with this, you will have to use vector tiles. This uses `tippecanoe`, which will need to be installed.
```
git clone https://github.com/mapbox/tippecanoe.git
cd tippecanoe
make -j
make install # you may have to use `sudo make install`
```
Make sure the `convert_boundaries.sh` file is executable.
```
chmod +x convert_boundaries.sh
```

Then, run the `convert_boundaries.sh` file to convert all the `.geojson` files into the vector tiles. This will take a few minutes.
```
./convert_boundaries.sh
```