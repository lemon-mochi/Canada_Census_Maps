import geopandas as gpd

# 1. Load the downloaded StatCan Shapefile
# Example: Census Subdivisions file (e.g., lda_000b21a_e.shp)
shapefile_path = "./boundaries/da/lda_000b21a_e.shp"
gdf = gpd.read_file(shapefile_path)

# 2. Re-project coordinates from NAD83 (StatCan native) to WGS84 (Web Maps)
gdf_wgs84 = gdf.to_crs(epsg=4326)

# 3. (Optional) Filter for a specific province to keep file size small
# 'PRUID' 59 is British Columbia, 35 is Ontario, 24 is Quebec, etc.
bc_subdivisions = gdf_wgs84[gdf_wgs84['PRUID'] == '59']

# 4. Export directly to GeoJSON for use in Leaflet / Mapbox
bc_subdivisions.to_file("bc_census_da.geojson", driver="GeoJSON")