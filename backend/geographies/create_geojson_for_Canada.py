
from pathlib import Path
import geopandas as gpd
import os
from shapely import make_valid

os.environ["OGR_GEOJSON_MAX_OBJ_SIZE"] = "0"

# Paths are relative to the directory you run this script from.
GEOJSON_DIR = Path("geojson")

PROVINCE_FILES = {
    1981: "1981-2001_geojson/1981/Data GeoJSON/prov1981_poly_geojson.geojson",
    1986: "1981-2001_geojson/1986/Data/Provincial Boundaries/can86prov_geojson.geojson",
    1991: "1981-2001_geojson/1991/Data/Provincial Boundaries/l91prv_geojson.geojson",
    1996: "1981-2001_geojson/1996/Data/Provinces/GeoJSON/GPRE000A_geojson.geojson",
    2001: "1981-2001_geojson/2001/Data/National/Provinces/GeoJSON/gpr_000b02m_e_geojson.geojson",
    2006: "geojson/gpr_000b06a_e.geojson",
    2011: "geojson/gpr_000b11a_e.geojson",
    2016: "geojson/lpr_000b16a_e.geojson",
    2021: "geojson/lpr_000b21a_e.geojson",
}


def process_single_year(year, filename):
    source = Path(filename)

    if not source.exists():
        print(f"Skipping {year}: missing {source}")
        return

    print(f"Processing {year}...", flush=True)

    encoding = "UTF-8" if year not in (1996, 2001) else "ISO-8859-1"
    provinces = gpd.read_file(source, encoding=encoding)

    if provinces.empty:
        print(f"Skipping {year}: no features found")
        return

    # Union the provincial polygons into one Canada geometry.
    geometries = provinces.geometry.map(
        lambda geom: make_valid(geom) if geom is not None and not geom.is_valid else geom
    )

    canada_geometry = geometries.union_all()

    # Preserve the requested geographic identifiers.
    if year <= 1996:
        code_column = "GEO_CODE"
        canada_code = "00"
    elif year == 2021:
        code_column = "DGUID"
        canada_code = "2021A000011124"
    else:
        code_column = "GEO_CODE"
        canada_code = "01"

    canada = gpd.GeoDataFrame(
        {
            code_column: [canada_code],
            "NAME": ["Canada"],
        },
        geometry=[canada_geometry],
        crs=provinces.crs,
    )

    GEOJSON_DIR.mkdir(parents=True, exist_ok=True)
    output_geojson = GEOJSON_DIR / f"canada_{year}.geojson"

    canada.to_file(output_geojson, driver="GeoJSON")

    print(f"Created {output_geojson}", flush=True)


def build_canada_geojson():
    GEOJSON_DIR.mkdir(parents=True, exist_ok=True)

    for year, filename in PROVINCE_FILES.items():
        try:
            process_single_year(year, filename)
        except Exception as e:
            print(f"Error processing {year}: {e}", flush=True)


if __name__ == "__main__":
    build_canada_geojson()
