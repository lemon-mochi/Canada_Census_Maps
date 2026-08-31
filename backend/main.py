from pathlib import Path
import requests
import io
import zipfile

import pandas as pd
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

BASE_DIR = Path(__file__).resolve().parent

print("BASE_DIR:", BASE_DIR)
print("Tiles directory:", BASE_DIR / "tiles_output")
print("Exists:", (BASE_DIR / "tiles_output").exists())
print("Files:", list((BASE_DIR / "tiles_output").glob("*")))

app.mount(
    "/tiles_output",
    StaticFiles(directory=BASE_DIR / "tiles_output"),
    name="tiles_output",
)

@app.get("/debug")
def debug():
    tiles_dir = BASE_DIR / "tiles_output"

    return {
        "directory": str(tiles_dir),
        "exists": tiles_dir.exists(),
        "files": [f.name for f in tiles_dir.iterdir()] if tiles_dir.exists() else [],
    }

def parse_statcan_sdmx_to_pruid_map(json_data):
    structure = json_data['data']['structures'][0]
    
    # 1. Build PRUID (ALT_GEO_CODE) mapping from structural attributes
    # Find the REF_AREA dimension index in the series dimensions list
    series_dims = structure['dimensions']['series']
    ref_area_dim_idx = next(i for i, dim in enumerate(series_dims) if dim['id'] == 'REF_AREA')
    
    # Find the ALT_GEO_CODE attribute structure
    series_attrs = structure['attributes']['series']
    alt_geo_attr = next(attr for attr in series_attrs if attr['id'] == 'ALT_GEO_CODE')
    alt_geo_values = alt_geo_attr['values']  # List of dicts like [{"value": "35"}, ...]
    
    series_data = json_data['data']['dataSets'][0]['series']
    pruid_pop_map = {}

    for series_key, series_val in series_data.items():
        indices = [int(i) for i in series_key.split(':')]
        
        # Determine the REF_AREA index for this series
        ref_area_idx = indices[ref_area_dim_idx]
        
        # Get corresponding series attributes
        # series_val['attributes'] contains attribute indices corresponding to series_attrs
        attr_indices = series_val['attributes']
        
        # Index 4 in attributes corresponds to ALT_GEO_CODE in StatCan SDMX structure
        # We fall back to looking up from the values array
        alt_geo_val_idx = attr_indices[4]
        
        if alt_geo_val_idx is not None and alt_geo_val_idx < len(alt_geo_values):
            pruid = str(alt_geo_values[alt_geo_val_idx]['value'])
            
            # Format to 2-digit string (e.g., '35')
            pruid = pruid.zfill(2)
            
            # Extract observation population count
            obs_val = series_val['observations']['0'][0]
            if obs_val is not None and pruid != "01":  # Skip "01" (Canada total)
                pruid_pop_map[pruid] = int(obs_val)

    return pruid_pop_map


# PRODUCT_ID = 98100001
# STATCAN_API_URL = f"https://api.statcan.gc.ca/census-recensement/profile/sdmx/rest/data/"

CACHED_POPULATION_DATA = None

@app.get("/api/province-population")
def get_province_population():
    agencyID = "STC_CP"
    dataflow = "DF_PR"
    key = "A5..1.1.1"
    parameters = "format=jsondata"

    url = f"https://api.statcan.gc.ca/census-recensement/profile/sdmx/rest/data/{agencyID},{dataflow}/{key}?{parameters}"


    global CACHED_POPULATION_DATA
    if CACHED_POPULATION_DATA is not None:
        return {"status": "success", "data": CACHED_POPULATION_DATA}

    # 1. Fetch dynamic download URL from StatCan
    response = requests.get(url, params={})

    data = response.json()


    # print("STATUS:", response.status_code)
    # print("URL:", response.url)
    # print("RESPONSE:", response.text[:1000])

    response.raise_for_status()

    parsed_json = parse_statcan_sdmx_to_pruid_map(json_data=data)

    print("parsed_json:", parsed_json)

    return parsed_json

    # # 2. Extract CSV into RAM
    # zip_res = requests.get(data.get("object"))
    # zip_file = zipfile.ZipFile(io.BytesIO(zip_res.content))
    # csv_filename = [f for f in zip_file.namelist() if f.endswith(".csv") and not f.endswith("_MetaData.csv")][0]

    # with zip_file.open(csv_filename) as f:
    #     population_column = (
    #         "Population and dwelling counts (11): Population, 2021 [1]"
    #     )        
    #     # Load necessary fields
    #     df = pd.read_csv(
    #         f,
    #         usecols=["GEO", "DGUID", population_column],
    #         low_memory=False
    #     )

    #     # Extract PRUID from the last two digits of DGUID
    #     df["PRUID"] = df["DGUID"].str[-2:]

    #     # Keep only the province id and 2021 population
    #     df = df[["PRUID", population_column]]

    #     # Remove rows where population isn't available
    #     df = df.dropna(subset=[population_column])

    #     return {
    #         "data": {
    #             row["PRUID"]: row[population_column]
    #             for _, row in df.iterrows()
    #         }
    #     }