"""
merge_split_geojson.py
The 1986 and 1991 census tracts and 1991 enumeration areas are split into
multiple .geojson files. This program merges them together so they can easily
be converted to vector tiles by the bash file, convert_boundaries.sh
"""

import os
import geopandas as gpd
import pandas as pd

def merge_geojson_geopandas(input_folder, output_filename):
    """
    Merges all GeoJSON files in a folder into a single GeoJSON file using GeoPandas.
    """
    gdfs = []
    
    # Loop through all files in the directory
    for file in os.listdir(input_folder):
        if file.endswith(".geojson") or file.endswith(".json"):
            file_path = os.path.join(input_folder, file)
            print(f"Reading: {file}")
            
            # Read GeoJSON into a GeoDataFrame
            gdf = gpd.read_file(file_path)
            gdfs.append(gdf)
            
    if not gdfs:
        print("No GeoJSON files found.")
        return

    # Concatenate all GeoDataFrames together
    print("Merging files...")
    merged_gdf = gpd.GeoDataFrame(pd.concat(gdfs, ignore_index=True))
    
    # Save the combined result
    merged_gdf.to_file(output_filename, driver="GeoJSON")
    print(f"Successfully created: {output_filename}")

merge_geojson_geopandas("./1981-2001_geojson/1986/Data/Census Tracts/", "./geojson/1986_ct.geojson")
merge_geojson_geopandas("./1981-2001_geojson/1991/Data/Census Tracts/", "./geojson/1991_ct.geojson")
merge_geojson_geopandas("./1981-2001_geojson/1991/Data/Enumeration Areas/", "./geojson/1991_ea.geojson")