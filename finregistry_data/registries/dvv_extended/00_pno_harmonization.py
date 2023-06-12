'''Harmonization of Postal Codes and Municipalities by converting them to 2022 versions'''
import geopandas
import pandas

pno = geopandas.read_file('/data/projects/project_akarvane/geo/pno_2022/pno_2022Polygon.shp')  # 2022 Postal Codes and Municipalities
living = pandas.read_csv('/data/processed_data/dvv/Tulokset_1900-2010_tutkhenk_asuinhist.txt.finreg_IDsp')  # DVV Living Registry

living = living.head(10)

geo_living = geopandas.GeoDataFrame(living, geometry=geopandas.points_from_xy(living.Longitude, living.Latitude, crs='epsg:3067'))

living_pno = geo_living.sjoin(pno, how='left', predicate='intersects')

living_pno.to_csv('/data/projects/project_akarvane/geo/living_pno.csv')
