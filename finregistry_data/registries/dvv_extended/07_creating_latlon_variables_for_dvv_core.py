import pandas
import geopandas

dvv = pandas.read_csv("dvv_ext_core.csv")
dvv = geopandas.GeoDataFrame(dvv, geometry=geopandas.points_from_xy(dvv.Longitude, dvv.Latitude, crs='epsg:3067'))

dvv2 = dvv.copy()
dvv2 = dvv2.to_crs("EPSG:4326")
print(dvv2.geometry.head())

# removing rows with empty geometry due to empty latitude in the first place:
dvv3 = dvv2.loc[~dvv2['geometry'].is_empty, :].copy()

dvv3['lon'] = dvv3['geometry'].x
dvv3['lat'] = dvv3['geometry'].y

dvv3 = dvv3[['lon', 'lat', 'ident']]

dvv3.to_csv('~/dvv_ext_ess_lat_lon.csv')
