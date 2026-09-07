import geopandas as gpd
from pathlib import Path

# 1. Load the downloaded StatCan Shapefile
# Example: Census Subdivisions files 
shapefile_path_dir = Path("./boundaries")
output_path_dir = Path("./geojson")

for shapefile in shapefile_path_dir.rglob("*.shp"):
    print(f"Processing: {shapefile}")
    # shapefile_path = os.path.join(shapefile_path_dir, folder, f"{folder}.shp")

    
    gdf = gpd.read_file(shapefile)

    # 2. Re-project coordinates from NAD83 (StatCan native) to WGS84 (Web Maps)
    gdf_wgs84 = gdf.to_crs(epsg=4326)

    output_path = output_path_dir / f"{shapefile.stem}.geojson"

    # 3. Export directly to GeoJSON for use in Leaflet / Mapbox
    gdf_wgs84.to_file(f"{output_path}", driver="GeoJSON")