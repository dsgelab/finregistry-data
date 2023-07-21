import pandas
import geopandas

shp2018 = geopandas.read_file("/home/jgerman/one_km_files/rttk1km_2018.shp")

for col_name in shp2018.columns: 
    print(col_name)

    
shp2018.drop(shp2018.iloc[:, 0:31], inplace = True, axis = 1)    
shp2018.columns

dvv = pandas.read_csv("~/dvv_ext_core.csv")
print(dvv.columns)
print(dvv.shape)

# Keeping only the necessary columns to minimize risk of memory error when merging the files
dvv.drop(dvv.iloc[:, 5:24], inplace = True, axis = 1)

geo_s1 = geopandas.GeoDataFrame(dvv, geometry=geopandas.points_from_xy(dvv.Longitude, dvv.Latitude, crs='epsg:3067'))

geo_s1.crs == shp2018.crs

dvv_shp2018 = geo_s1.sjoin(shp2018, how='left', predicate='intersects')
dvv_shp2018 = dvv_shp2018.drop_duplicates(['FINREGISTRYID','Start_of_residence'])

dvv_shp2018.columns
dvv_shp2018.drop(dvv_shp2018.iloc[:, 0:5], inplace = True, axis = 1)
dvv_shp2018.drop(dvv_shp2018.iloc[:, 1:3], inplace = True, axis = 1)

dvv_shp2018.to_csv('/home/jgerman/dvv_ext_1sqkm_2018.csv', index = False)

