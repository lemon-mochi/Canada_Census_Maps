from pathlib import Path

from fastapi import HTTPException
import duckdb

from config import TILES_DIR


def vector_tile_path(census_year: int, geo_level: str) -> Path:
    if census_year == 1981:
        if geo_level == "Province":
            return TILES_DIR / "prov1981_poly_geojson.pmtiles"
        elif geo_level == "Census division":
            return TILES_DIR / "cd_dr1981_poly_geojson.pmtiles"
        elif geo_level == "Census subdivision":
            return TILES_DIR / "csd1981_poly_geojson.pmtiles"
        elif geo_level == "Census tract":
            return TILES_DIR / "ct_1981_orig_CBF.pmtiles"

    elif census_year == 1986:
        if geo_level == "Province":
            return TILES_DIR / "can86prov_geojson.pmtiles"
        elif geo_level == "Census division":
            return TILES_DIR / "cd86_geojson.pmtiles"
        elif geo_level == "Census subdivision":
            return TILES_DIR / "csd86_geojson.pmtiles"
        elif geo_level == "Census tract":
            return TILES_DIR / "ct_1986.pmtiles" 

    elif census_year == 1991:
        if geo_level == "Province":
            return TILES_DIR / "l91prv_geojson.pmtiles"
        elif geo_level == "Census division":
            return TILES_DIR / "l91cd_geojson.pmtiles"
        elif geo_level == "Census subdivision":
            return TILES_DIR / "l91csd_geojson.pmtiles"
        elif geo_level == "Federal electoral district (1987 Representation Order)":
            return TILES_DIR / "l91fed_geojson.pmtiles"
        elif geo_level == "Census tract":
            return TILES_DIR / "1991_ct.pmtiles"

    elif census_year == 1996:
        if geo_level == "Province":
            return TILES_DIR / "GPRE000A_geojson.pmtiles"
        elif geo_level == "Census division":
            return TILES_DIR / "GCD_000A_geojson.pmtiles"
        elif geo_level == "Census subdivision":
            return TILES_DIR / "GCSD000A_geojson.pmtiles"
        elif geo_level == "Census tract":
            return TILES_DIR / "GCT_000A_geojson.pmtiles"
        elif geo_level == "Federal electoral district (1996 Representation Order)":
            return TILES_DIR / "GFED000A_geojson.pmtiles"
        elif geo_level == "Enumeration area":
            return TILES_DIR / "GEA_000A_geojson.pmtiles"

    elif census_year == 2001:
        if geo_level == "Province":
            return TILES_DIR / "gpr_000b02m_e_geojson.pmtiles"
        elif geo_level == "Census division":
            return TILES_DIR / "gcd_000b02m_e_geojson.pmtiles"
        elif geo_level == "Census subdivision":
            return TILES_DIR / "gcsd000b02m_e_geojson.pmtiles"
        elif geo_level == "Census tract":
            return TILES_DIR / "gct_000b02m_e_geojson.pmtiles"
        elif geo_level == "Federal electoral district (1996 Representation Order)":
            return TILES_DIR / "gfed000b02m_e_geojson.pmtiles"
        elif geo_level == "Dissemination area":
            return TILES_DIR / "gda_000b02m_e_geojson.pmtiles"

    elif census_year == 2006:
        if geo_level == "Province":
            return TILES_DIR / "gpr_000b06a_e.pmtiles"
        elif geo_level == "Census division":
            return TILES_DIR / "gcd_000b06a_e.pmtiles"
        elif geo_level == "Census subdivision":
            return TILES_DIR / "gcsd000b06a_e.pmtiles"
        elif geo_level == "Federal electoral district (2003 Representation Order)":
            return TILES_DIR / "gfed000b06a_e.pmtiles"
        elif geo_level == "Census tract":
            return TILES_DIR / "gct_000b06a_e.pmtiles"
        elif geo_level == "Dissemination area":
            return TILES_DIR / "gda_000b06a_e.pmtiles"

    elif census_year == 2010:
        return TILES_DIR / "gda_000b11a_e.pmtiles"

    elif census_year == 2011:
        if geo_level == "Province":
            return TILES_DIR / "gpr_000b11a_e.pmtiles"
        elif geo_level == "Census division":
            return TILES_DIR / "gcd_000b11a_e.pmtiles"
        elif geo_level == "Census subdivision":
            return TILES_DIR / "gcsd000b11a_e.pmtiles"
        elif geo_level == "Federal electoral district (2003 Representation Order)":
            return TILES_DIR / "gfed000b11a_e.pmtiles"
        elif geo_level == "Census tract":
            return TILES_DIR / "gct_000b11a_e.pmtiles"
        elif geo_level == "Dissemination area":
            return TILES_DIR / "gda_000b11a_e.pmtiles"

    elif census_year == 2016:
        if geo_level == "Province":
            return TILES_DIR / "lpr_000b16a_e.pmtiles"
        elif geo_level == "Census division":
            return TILES_DIR / "lcd_000b16a_e.pmtiles"
        elif geo_level == "Census subdivision":
            return TILES_DIR / "lcsd000b16a_e.pmtiles"
        elif geo_level == "Federal electoral district (2013 Representation Order)":
            return TILES_DIR / "lfed000b16a_e.pmtiles"
        elif geo_level == "Aggregate dissemination area":
            return TILES_DIR / "lada000b16a_e.pmtiles"
        elif geo_level == "Dissemination area":
            return TILES_DIR / "lda_000b16a_e.pmtiles"

    elif census_year == 2021:
        if geo_level == "Province":
            return TILES_DIR / "lpr_000b21a_e.pmtiles"
        elif geo_level == "Census division":
            return TILES_DIR / "lcd_000b21a_e.pmtiles"
        elif geo_level == "Census subdivision":
            return TILES_DIR / "lcsd000b21a_e.pmtiles"
        elif geo_level == "Federal electoral district (2013 Representation Order)":
            return TILES_DIR / "lfed000b21a_e.pmtiles"
        elif geo_level == "Federal electoral district (2023 Representation Order)":
            return TILES_DIR / "FED_CA_2023_EN.pmtiles"
        elif geo_level == "Aggregate dissemination area":
            return TILES_DIR / "lada000b21a_e.pmtiles"
        elif geo_level == "Dissemination area":
            return TILES_DIR / "lda_000b21a_e.pmtiles"

    raise HTTPException(
        status_code=404,
        detail=f"No vector tiles available for {census_year} / {geo_level}",
    )

def geo_mappings(
    db,
    path: str,
    geo_level: str):

    if geo_level == "Census tract":
        query = """
            SELECT CTUID AS CTuid, GEO_CODE
            FROM read_parquet(?)
            WHERE CTUID IS NOT NULL
        """
    else:
        query = """
            SELECT GEO_NAME AS DAUID, GEO_CODE
            FROM read_parquet(?)
            WHERE LENGTH(GEO_CODE) = 11
        """

    rows = db.execute(query, [str(path)]).fetchall()

    return {
        str(tile_id): str(geo_code)
        for tile_id, geo_code in rows
    }