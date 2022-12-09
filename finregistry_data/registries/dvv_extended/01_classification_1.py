
'''Adding the shapefiles for classification of the living area into dense/sparse urban/rural''' 
import pandas
import geopandas

# importing the shapefile
pno = geopandas.read_file("shapefiles/densesparse2010/HarvaTiheaTaajama2010.shp")
# importing the new register with more than 35,000,000 rows
living_antti = pandas.read_csv('/data/projects/project_akarvane/geo/living_pno.csv')

living_antti.shape  
living_antti.columns  

#renaming index_right column
living_antti = living_antti.rename({'index_right': 'index_right_0'}, axis=1)

# turning living in a geopandas DF
geo_living_antti = geopandas.GeoDataFrame(living_antti, geometry=geopandas.points_from_xy(living_antti.Longitude, living_antti.Latitude, crs='epsg:3067'))


# s-joining them together
living_pno = geo_living_antti.sjoin(pno, how='left', predicate='intersects')



### JOIING 2nd Shape file:
pno2 = geopandas.read_file("shapefiles/urban_rural2010/YKRKaupunkiMaaseutuLuokitus2010.shp")

#renaming index_right column
living_pno = living_pno.rename({'index_right': 'index_right_1'}, axis=1)

# s-joining them together
living_pno_2 = living_pno.sjoin(pno2, how='left', predicate='intersects')




### JOINING 3rd Shape file:
pno3 = geopandas.read_file("shapefiles/residential2010/HarvaPientaloAlue10.shp")

#renaming index_right column
living_pno_2 = living_pno_2.rename({'index_right': 'index_right_2'}, axis=1)

# s-joining them together
living_pno_3 = living_pno_2.sjoin(pno3, how='left', predicate='intersects')



### JOINING 4th Shape file:
pno4 = geopandas.read_file("shapefiles/residential2010/KerrostaloAlue10.shp")

#renaming index_right column
living_pno_3 = living_pno_3.rename({'index_right': 'index_right_3'}, axis=1)

# s-joining them together
living_pno_4 = living_pno_3.sjoin(pno4, how='left', predicate='intersects')




### JOINING 5th Shape file:
pno5 = geopandas.read_file("shapefiles/residential2010/PientaloAlue10.shp")

#renaming index_right column
living_pno_4 = living_pno_4.rename({'index_right': 'index_right_4'}, axis=1)

# s-joining them together
living_pno_5 = living_pno_4.sjoin(pno5, how='left', predicate='intersects')

#renaming index_right column
living_pno_5 = living_pno_5.rename({'index_right': 'index_right_5'}, axis=1)



# saving the table as csv file
living_pno_5.to_csv('shapefiles/dvv_and_shp_5.csv')



