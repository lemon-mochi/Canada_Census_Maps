def geo_mappings(db, path: str, geo_level: str):

    if geo_level == "Census tract":
        query = """
            SELECT CTUID AS TILE_CODE, GEO_CODE
            FROM read_parquet(?)
            WHERE CTUID IS NOT NULL
        """
    else:
        query = """
            SELECT GEO_NAME AS TILE_CODE, GEO_CODE
            FROM read_parquet(?)
            WHERE LENGTH(GEO_CODE) = 11
        """

    rows = db.execute(query, [str(path)]).fetchall()

    return {str(tile_id): str(geo_code) for tile_id, geo_code in rows}
