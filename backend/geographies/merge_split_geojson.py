"""
merge_split_geojson.py
The 1991 census tracts are split into
multiple .geojson files. This program merges them together so they can easily
be converted to vector tiles by the bash file, convert_boundaries.sh
"""

import os
import geopandas as gpd


def normalize_ct_name(series):
    return series.astype(str).str.zfill(6)


def merge_geojson_geopandas(input_folder, output_filename):
    files = [
        file
        for file in os.listdir(input_folder)
        if file.endswith(".geojson") or file.endswith(".json")
    ]

    if len(files) != 2:
        raise ValueError(f"Expected 2 GeoJSON files, found {len(files)}")

    gdfs = {}

    for file in files:
        path = os.path.join(input_folder, file)
        print(f"Reading: {file}")

        gdf = gpd.read_file(path)

        if "CA_CTNAME" in gdf.columns:
            gdfs["ca_ctname"] = gdf
        elif "CT_CODE" in gdf.columns and "PROV" in gdf.columns:
            gdfs["ct_code"] = gdf
        else:
            raise ValueError(f"Could not identify file: {file}")

    ca_ctname = gdfs["ca_ctname"]
    ct_code = gdfs["ct_code"]

    ca_ctname["CT_NAME"] = normalize_ct_name(ca_ctname["CT_NAME"])
    ct_code["CT_NAME"] = normalize_ct_name(ct_code["CT_NAME"])

    # Make sure CA + CT_NAME really is unique.
    if ca_ctname.duplicated(["CA", "CT_NAME"]).any():
        raise ValueError("CA + CT_NAME is not unique in CA_CTNAME file")

    if ct_code.duplicated(["CA", "CT_NAME"]).any():
        raise ValueError("CA + CT_NAME is not unique in CT_CODE file")

    # Only bring the missing attributes across.
    attributes = ct_code[["CA", "CT_NAME", "CT_CODE", "PROV"]]

    merged_gdf = ca_ctname.merge(
        attributes,
        on=["CA", "CT_NAME"],
        how="left",
        validate="one_to_one",
    )

    # Keep the geometry from the CA_CTNAME file.
    merged_gdf = gpd.GeoDataFrame(
        merged_gdf,
        geometry="geometry",
        crs=ca_ctname.crs,
    )

    print(f"Merged {len(merged_gdf)} census tracts")

    merged_gdf.to_file(
        output_filename,
        driver="GeoJSON",
    )

    print(f"Successfully created: {output_filename}")


merge_geojson_geopandas(
    "./1981-2001_geojson/1991/Data/Census Tracts/",
    "./geojson/1991_ct.geojson",
)
