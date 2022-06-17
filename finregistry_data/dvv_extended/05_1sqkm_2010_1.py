'''Joining 1 km² metadata from Statics Finland'''
import pandas
import geopandas

shp2010 = geopandas.read_file("one_km_files/rttk1km_2010.shp")
shp2010.head()

dvv = pandas.read_csv('~/dvv_ext_core.csv')
dvv.columns

dvv = dvv.drop_duplicates(['FINREGISTRYID','Start_of_residence'])  
dvv.shape  # must be: 35041489 , 15

geo_s1 = geopandas.GeoDataFrame(dvv, geometry=geopandas.points_from_xy(dvv.Longitude, dvv.Latitude, crs='epsg:3067'))
geo_s1.rename(columns = {'index_right':'index_right_0'}, inplace = True)
dvv_shp2010 = geo_s1.sjoin(shp2010, how='left', predicate='intersects') 
    
dvv_shp2010 = dvv_shp2010.drop_duplicates(['FINREGISTRYID','Start_of_residence'])
dvv_shp2010.shape  # 35041489, 127
dvv_shp2010.to_csv('one_km_files/dvv_azip_1km_shp_2010.csv')



