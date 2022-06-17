'''Joining 1 km² metadata from Statics Finland'''
import pandas
import geopandas

shp2010 = geopandas.read_file("one_km_files/rttk1km_2010.shp")
shp2010.head()

dvv = pandas.read_csv('/data/projects/project_akarvane/geo/living_pno.csv')
dvv.columns
dvv = dvv.drop(['Residence_type', 'Municipality', 'Municipality_name', 'Unnamed: 0', 'Building_ID', 'Residence_code', 'Post_code'], axis=1)

dvv = dvv.drop_duplicates(['FINREGISTRYID','Start_of_residence'])  # *1
dvv.shape  # must be: 35041489 , 15
#s1 = dvv.iloc[:, : 15]        # if ncol of dvv = 15, then no subset needed, because it's not a subset then

geo_s1 = geopandas.GeoDataFrame(dvv, geometry=geopandas.points_from_xy(dvv.Longitude, dvv.Latitude, crs='epsg:3067'))
geo_s1.rename(columns = {'index_right':'index_right_0'}, inplace = True)
dvv_shp2010 = geo_s1.sjoin(shp2010, how='left', predicate='intersects') 
    
dvv_shp2010 = dvv_shp2010.drop_duplicates(['FINREGISTRYID','Start_of_residence'])
dvv_shp2010.shape  # 35041489, 127
dvv_shp2010.to_csv('one_km_files/dvv_azip_1km_shp_2010.csv')



