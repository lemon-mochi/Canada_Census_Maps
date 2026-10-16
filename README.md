# Census Maps 🇨🇦 #
This is a web application that displays Canadian census data on a map. The design is meant to be simple, so that even non-technical users may easily use. Canada is the greatest country on Earth and it deserves a web application that shows its greatness through our census data. \
The thistle🪻, shamrock☘️, rose🌹 entwine,\
🍁🍁🍁THE MAPLE LEAF FOREVER!!!🍁🍁🍁

There is no thistle emoji so I used the closest looking thing. If you are not satisfied, here is a unicorn: 🦄.

A note on the reference: The Maple Leaf Forever is a historic Canadian song, and I am using the reference here as an expression of personal Canadian pride and an appreciation of Canadian history, and not as a statement about who does or does not belong in Canada. Canada’s history includes many different peoples and perspectives, and this project is intended to celebrate the country and its people through census data.

# Deployment #
I attempted to use AWS to deploy this web application. However, using the free tier caused everything to be way too slow. The app was pretty much ususable. I decided that for now, this will be a local only web application. However, I got experience with AWS and cloud development so it was not completely pointless.

# Running Locally #
You can download the files that I created to run this app from my Google Drive.\
[Parquet Data](https://drive.google.com/file/d/1H9ys3eDHWOvqbxRUX2nup5FmI9e1LM-M/view?usp=sharing)\
Download this and place the extracted `.parquet` files in `backend/parquet_data`.\

[Vector Tiles](https://drive.google.com/file/d/1tfz5-W_uowGDeNICkv22-J4_mi-aiKBW/view?usp=sharing)\
Download this and place the extracted `.pmtiles` files in `backend/tiles_output`.\

Alternatively, you can download the files and follow the steps I took to get the parquet and vector tile files.

Read [Setup.md](Setup.md) for instructions on gathering the files needed to run the program.

## Setting up virtual Python environment ##
I used `Python3.12` and `Python3.14` for this project. When I tried on `Python3.10`, I was not able to install all the libraries.
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

# Running test cases #
The test cases are in `backend/tests/`. To run them, use
```
python -m pytest
```
in the `backend/` directory.

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

# Skills Demonstrated #
**Backend Development:** Python, FastAPI, REST API design, endpoint development, request handling, data retrieval, and backend testing with pytest.\
**Data Engineering & Processing:** Pandas, PySpark, Jupyter Notebooks, data cleaning, ETL pipelines, schema normalization, and conversion of raw census datasets into optimized Parquet files.\
**Databases & Querying:** SQL, DuckDB, relational data concepts, analytical queries, and efficient retrieval of census data.\
**Frontend Development:** React, JavaScript, interactive map interfaces, API integration, and dynamic visualization of geographic data.\
**Geospatial Technologies:** Leaflet, MapLibre GL JS, OpenFreeMap, Tippecanoe, and PMTiles for rendering and serving geographic boundaries at multiple levels of detail.\
**Data Formats & Interoperability:** CSV, XML, IVT, Parquet, GeoJSON, ESRI Shapefile (SHP), and PMTiles.\
**Testing & Development Tools:** pytest, Git, Linux, Bash scripting, and automated data-processing workflow\
**Cloud Development:** AWS S3\
**Non-technical:** Canadian history, Canadian geography, sociology