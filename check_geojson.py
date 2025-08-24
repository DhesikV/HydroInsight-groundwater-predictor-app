import geopandas as gpd

# Directly load from C:\Hydroinsight
gdf = gpd.read_file("TAMILNADU_SUBDISTRICTS.geojson")

print("\n✅ Columns in GeoJSON:\n", gdf.columns.tolist())
print("\n✅ First 5 rows:\n", gdf.head())
