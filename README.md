# Census Maps 🇨🇦 #
This is a web application that displays Canadian census data on a map. The design is meant to be simple, so that even non-technical users may easily use. Canada is the greatest country on Earth and it deserves a web application that shows its greatness through our census data. \
The thistle🪻, shamrock☘️, rose🌹 entwine,\
🍁🍁🍁THE MAPLE LEAF FOREVER!!!🍁🍁🍁

There is no thistle emoji so I used the closest looking thing. If you are not satisfied, here is a unicorn: 🦄.

# Running locally #
You will need to gather vector tiles and parquet files for this program to work properly.\
If you would like to create the files from scrath, you can follow the procedure I have listed out.
However, this is somewhat complicated as there are multiple steps that must be followed. Additionally, the official Statisitcs Canada site is often not able to load properly, so you may run into troubles downloading the files.

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

The official Statistics Canada website has boundary files for the 2001 census but they are not available in the `.shp` format. I was able to find an alternative source that has `.geojson` files that represent the boundaries. [Abacus Data Network, Statistics Canada Open License](https://abacus.library.ubc.ca/dataverse/statcan-public). The next step shows how to convert the `.shp` files into `.geojson`. Since the files from the Abacus Data Network are already in the `.geojson` format, you may put them in the `backend/geojson/{census_year}` directory, after extracting the `.zip`. The way you download files using the website is too complicated. To simplify the process, I have put the `.zip` files into my Google Drive, where you may download it. The license allows me to do this.

[2001 All geographies](https://drive.google.com/file/d/1ykD9uJug7wOHgH9A7-T87gYNIIcGTK9Y/view?usp=sharing)

[1996 All geographies](https://drive.google.com/file/d/19NGWzwHYPQDOIQNT0HQrCsFoyPR-qnty/view?usp=sharing)

[1991 All geographies](https://drive.google.com/file/d/1phRbwAtwk9sCv8NBoVSLML_3EdmfgOLI/view?usp=sharing)

[1986 All geographies](https://drive.google.com/file/d/17WtlTpVldtydKmBdYhFskBCFzTU5O7lc/view?usp=sharing)

[1981 All geographies (except for census tracts)](https://drive.google.com/file/d/13132K4Qw3WDbxA7NPCqJJPeuXwtmhzZg/view?usp=sharing)

The data for the 1981 census tracts are from the [Borealis Data](https://borealisdata.ca/dataverse/unicen_boundaries)

[1981 Census tracts](https://borealisdata.ca/dataset.xhtml?persistentId=doi:10.5683/SP3/8OFB0M#)

After extracting the `.zip` file, you will see a `MANIFEST.txt` file, and a directory called `Data`. Place both of them into the `backend/1981-2001_geojson/{census_year}` directory, where `{census_year}` matches the census year of the downloaded file. For the 1981 census tracts data, simply place the `.geojson` file with the other `.geojson` files for the 1981 census.

Then, run the `merge_split_geojson.py` file to merge needed `.geojson` files together.
```
python3 merge_split_geojson.py
```
Optional: you can now delete the directories for 1986 census tracts, 1991 census tracts, and 1991 enumeration areas. If you decide not to delete these files, the bash file will create extra unused vector tiles (more information about bash file in the following sections).

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
You will also need to download the files containing census data. These files are very large and will take a while to download. I have gathered the needed download links. You do not have to extract these `.zip` files. Simply put them in `backend/census_data`.

[2021 Canada, provinces, territories, census divisions (CDs), census subdivisions (CSDs) and dissemination areas (DAs)](https://www12.statcan.gc.ca/census-recensement/2021/dp-pd/prof/details/download-telecharger/comp/GetFile.cfm?Lang=E&FILETYPE=CSV&GEONO=006)

[2021 Federal electoral districts (2013 Representation Order)](https://www12.statcan.gc.ca/census-recensement/2021/dp-pd/prof/details/download-telecharger/comp/GetFile.cfm?Lang=E&FILETYPE=CSV&GEONO=010)

[2021 Federal electoral districts (2023 Representation Order)](https://www12.statcan.gc.ca/census-recensement/2021/dp-pd/prof/details/download-telecharger/comp/GetFile.cfm?Lang=E&FILETYPE=CSV&GEONO=029)

[2021 Aggregate dissemination areas](https://www12.statcan.gc.ca/census-recensement/2021/dp-pd/prof/details/download-telecharger/comp/GetFile.cfm?Lang=E&FILETYPE=CSV&GEONO=012)

[2016 Canada, provinces, territories, census divisions (CDs), census subdivisions (CSDs) and dissemination areas (DAs)](https://www12.statcan.gc.ca/census-recensement/2016/dp-pd/prof/details/download-telecharger/comp/GetFile.cfm?Lang=E&FILETYPE=CSV&GEONO=044)

[2016 Federal electoral districts (2013 Representation Order)](https://www12.statcan.gc.ca/census-recensement/2016/dp-pd/prof/details/download-telecharger/comp/GetFile.cfm?Lang=E&FILETYPE=CSV&GEONO=045)

[2016 Aggregate dissemination areas](https://www12.statcan.gc.ca/census-recensement/2016/dp-pd/prof/details/download-telecharger/comp/GetFile.cfm?Lang=E&FILETYPE=CSV&GEONO=050)

[2011 Canada, provinces and territories Census Profile](https://www12.statcan.gc.ca/census-recensement/2011/dp-pd/prof/details/download-telecharger/comprehensive/comp_download.cfm?CTLG=98-316-XWE2011001&FMT=CSV101&Lang=E&Tab=1&Geo1=PR&Code1=01&Geo2=PR&Code2=01&Data=Count&SearchText=&SearchType=Begins&SearchPR=01&B1=All&Custom=&TABID=1)

[2011 Census divisions Census Profile](https://www12.statcan.gc.ca/census-recensement/2011/dp-pd/prof/details/download-telecharger/comprehensive/comp_download.cfm?CTLG=98-316-XWE2011001&FMT=CSV701&Lang=E&Tab=1&Geo1=PR&Code1=01&Geo2=PR&Code2=01&Data=Count&SearchText=&SearchType=Begins&SearchPR=01&B1=All&Custom=&TABID=1)

[2011 Census subdivisions Census Profile](https://www12.statcan.gc.ca/census-recensement/2011/dp-pd/prof/details/download-telecharger/comprehensive/comp_download.cfm?CTLG=98-316-XWE2011001&FMT=CSV301&Lang=E&Tab=1&Geo1=PR&Code1=01&Geo2=PR&Code2=01&Data=Count&SearchText=&SearchType=Begins&SearchPR=01&B1=All&Custom=&TABID=1)

[2011 Census tracts Census Profile](https://www12.statcan.gc.ca/census-recensement/2011/dp-pd/prof/details/download-telecharger/comprehensive/comp_download.cfm?CTLG=98-316-XWE2011001&FMT=CSV401&Lang=E&Tab=1&Geo1=PR&Code1=01&Geo2=PR&Code2=01&Data=Count&SearchText=&SearchType=Begins&SearchPR=01&B1=All&Custom=&TABID=1)

[2011 Federal electoral districts (2003 representation order) Census Profile](https://www12.statcan.gc.ca/census-recensement/2011/dp-pd/prof/details/download-telecharger/comprehensive/comp_download.cfm?CTLG=98-316-XWE2011001&FMT=CSV501&Lang=E&Tab=1&Geo1=PR&Code1=01&Geo2=PR&Code2=01&Data=Count&SearchText=&SearchType=Begins&SearchPR=01&B1=All&Custom=&TABID=1)

[2011 Census dissemination areas Census Profile](https://www12.statcan.gc.ca/census-recensement/2011/dp-pd/prof/details/download-telecharger/comprehensive/comp_download.cfm?CTLG=98-316-XWE2011001&FMT=CSV1501&Lang=E&Tab=1&Geo1=PR&Code1=01&Geo2=PR&Code2=01&Data=Count&SearchText=&SearchType=Begins&SearchPR=01&B1=All&Custom=&TABID=1)

[2011 Canada, provinces and territories NHS](https://www12.statcan.gc.ca/nhs-enm/2011/dp-pd/prof/details/download-telecharger/comprehensive/comp_download.cfm?CTLG=99-004-XWE2011001&FMT=CSV101&Lang=E&Geo1=PR&Code1=01&Data=Count&SearchText=&SearchType=Begins&SearchPR=01&A1=All&B1=All&Custom=&TABID=1)

[2011 Census divisions Census Profile NHS](https://www12.statcan.gc.ca/nhs-enm/2011/dp-pd/prof/details/download-telecharger/comprehensive/comp_download.cfm?CTLG=99-004-XWE2011001&FMT=CSV701&Lang=E&Geo1=PR&Code1=01&Data=Count&SearchText=&SearchType=Begins&SearchPR=01&A1=All&B1=All&Custom=&TABID=1)

[2011 Census subdivisions NHS](https://www12.statcan.gc.ca/nhs-enm/2011/dp-pd/prof/details/download-telecharger/comprehensive/comp_download.cfm?CTLG=99-004-XWE2011001&FMT=CSV301&Lang=E&Geo1=PR&Code1=01&Data=Count&SearchText=&SearchType=Begins&SearchPR=01&A1=All&B1=All&Custom=&TABID=1)

[2011 Census tracts NHS](https://www12.statcan.gc.ca/nhs-enm/2011/dp-pd/prof/details/download-telecharger/comprehensive/comp_download.cfm?CTLG=99-004-XWE2011001&FMT=CSV401&Lang=E&Geo1=PR&Code1=01&Data=Count&SearchText=&SearchType=Begins&SearchPR=01&A1=All&B1=All&Custom=&TABID=1)

[2011 Federal electoral districts (2003 Representation Order) NHS](https://www12.statcan.gc.ca/nhs-enm/2011/dp-pd/prof/details/download-telecharger/comprehensive/comp_download.cfm?CTLG=99-004-XWE2011001&FMT=CSV501&Lang=E&Geo1=PR&Code1=01&Data=Count&SearchText=&SearchType=Begins&SearchPR=01&A1=All&B1=All&Custom=&TABID=1)

The 2011 NHS data for dissemination areas is not available on Satistics Canada's official website. I was able to find the data elsewhere. Most people only care about the user experience but not the developer's experience. If you want to know how I got this data, read [2011_NHS_Data.md](2011_NHS_Data.md). The needed file was uploaded to my Google Drive.

[2011 Dissemination Areas NHS](https://drive.google.com/file/d/1BrJstkQiBlAOLRIsTKObEWf5DZkTXBx5/view?usp=sharing)

The 1996 - 2006. Data is in the `.XML` format.

For 2006 census data, there are multiple datasets that contain information based on topic. The dataset related to incomes and earnings is the one I chose as it also contains information from different topics. Also, I noticed that each `.XML` file maps their `DIM0` value in a different way. So, one file might have `DIM0` 1 map to 2006 population while another might map it to 2001 population. I tried using programming tricks but nothing seemed to work. I decided to just manually inspect the values and create a mapping of ids that map to only one characteristic, so everything can be consistent. I used excel for this. Sometimes, the non-technical solution is the best one. The mappings are in `backend/xml_mappings`.

[2006 Canada, Provinces, Territories, Census Divisions, Census Subdivisions and Dissemination Areas](https://www12.statcan.gc.ca/census-recensement/2006/dp-pd/prof/rel/OpenDataDownload.cfm?PID=94534)

[2006 Census Tracts](https://www12.statcan.gc.ca/census-recensement/2006/dp-pd/prof/rel/OpenDataDownload.cfm?PID=94537)

[2006 Federal electoral districts (2003 Representation Order)](https://www12.statcan.gc.ca/census-recensement/2006/dp-pd/prof/rel/OpenDataDownload.cfm?PID=94539)

The three XML files for 2001 have different numbers of characteristics. To see this, you can download a smaller `.csv` files from the datasets used from Statistics Canada's website. The file `backend/test_2001_characteristics.py` to see which characteristics are missing from each XML file. 

[2001 Canada, Provinces, Territories, Census Divisions, Census Subdivisions and Dissemination Areas](https://www12.statcan.gc.ca/English/census01/products/standard/profiles/OpenDataDownload.cfm?PID=72849)

[2001 Census Tracts](https://www12.statcan.gc.ca/English/census01/products/standard/profiles/OpenDataDownload.cfm?PID=72852)

[2001 Federal electoral districts (1996 Representation Order)](https://www12.statcan.gc.ca/English/census01/products/standard/profiles/OpenDataDownload.cfm?PID=71418)

[1996 Canada, Provinces, Territories, Census divisions and Census subdivisions](https://www12.statcan.gc.ca/English/census96/data/profiles/OpenDataDownload.cfm?PID=35782)

[1996 Census tracts](https://www12.statcan.gc.ca/English/census96/data/profiles/OpenDataDownload.cfm?PID=35716)

[1996 Federal electoral districts (1996 Representation Order)](https://www12.statcan.gc.ca/English/census96/data/profiles/OpenDataDownload.cfm?PID=35257)

[1996 Enumeration Areas](https://www12.statcan.gc.ca/English/census96/data/profiles/OpenDataDownload.cfm?PID=35804)

For census data from 1981 - 1991, data is only available in the `.IVT` format. You will have to download the [beyond 20/20 browser](https://web.archive.org/web/20160804181508/http://www2.beyond2020.com/SC/ProBrowser.exe) to convert it to the `.csv` format. However, I have already done that so you can simply download the entire thing as a big zip file from my Google Drive.

[1991 All data from Google Drive](https://drive.google.com/file/d/1yuTFWOEnVmNfNjTb2FIP6No-3IIs2y6z/view?usp=sharing)

[1986 All data drom Google Drive](https://drive.google.com/file/d/1topoCBcNvNUlW9aSb46qA-38xdufZs9z/view?usp=sharing)

[1981 All data from Google Drive](https://drive.google.com/file/d/1vbey-o3oA7Mdp_ibfplke1doGvLxGkBB/view?usp=sharing)

Alternatively, you can download the original `.IVT` files.

[1991 Canada, Provinces, Territories, Census divisions and Census subdivisions Part A](https://www12.statcan.gc.ca/English/census91/data/profiles/Download.cfm?PID=29)

[1991 Canada, Provinces, Territories, Census divisions and Census subdivisions Part B](https://www12.statcan.gc.ca/English/census91/data/profiles/Download.cfm?PID=30)

[1991 Census Tracts Part A](https://www12.statcan.gc.ca/English/census91/data/profiles/Download.cfm?PID=233)

[1991 Census Tracts Part B](https://www12.statcan.gc.ca/English/census91/data/profiles/Download.cfm?PID=234)

[1991 Federal Electoral Districts (1987 Representation Order) Part A](https://www12.statcan.gc.ca/English/census91/data/profiles/Download.cfm?PID=221)

[1991 Federal Electoral Districts (1987 Representation Order) Part B](https://www12.statcan.gc.ca/English/census91/data/profiles/Download.cfm?PID=222)

[1986 Canada, Provinces, Territories, Census divisions and Census subdivisions Part A](https://www12.statcan.gc.ca/English/census86/data/tables/Download.cfm?PID=113684)

[1986 Canada, Provinces, Territories, Census divisions and Census subdivisions Part B](https://www12.statcan.gc.ca/English/census86/data/tables/Download.cfm?PID=113685)

[1986 Census Tracts Part A](https://www12.statcan.gc.ca/English/census86/data/tables/Download.cfm?PID=113686)

[1986 Census Tracts Part B](https://www12.statcan.gc.ca/English/census86/data/tables/Download.cfm?PID=113687)

[1981 Canada, Provinces, Territories, Census divisions and Census subdivisions Part A](https://www12.statcan.gc.ca/English/census81/data/tables/Download.cfm?PID=113751)

[1981 Canada, Provinces, Territories, Census divisions and Census subdivisions Part B](https://www12.statcan.gc.ca/English/census81/data/tables/Download.cfm?PID=113752)

[1981 Census Tracts Part A](https://www12.statcan.gc.ca/English/census81/data/tables/Download.cfm?PID=113753)

[1981 Census Tracts Part B](https://www12.statcan.gc.ca/English/census81/data/tables/Download.cfm?PID=113754)

## Create the parquet files that contain Census data ##
For both jupyter notebooks, use the `.venv` virtual enviroment you created earlier.
Parquet files are a compressed data format better for high-performance analytics. For this project, it is necessary to convert the `.csv` files into Parquet files for faster retrieval.
Run the `create_parquet_files.ipynb` notebook to create the needed Parquet files. Running this program will create the `temp_parquet_data/` directory within `backend/`. This wil take a few minutes. Also, you may need to install `7z` to run the notebook.
```
sudo apt install p7zip-full
```

Next you will want to simplify the `.parquet` file. To do this, run the `cleanup_parquet.ipynb` notebook.
This will create the `parquet_data/` directory. This is the directory the server will use to retrieve data.

# Running the backend #
To run the backend server,
```
uvicorn main:app --reload
```

# Running the frontend #
```
npm install
npm run dev # for running locally
```