#!/usr/bin/env python
# coding: utf-8

# ### The initial step of concatinating file sis not included here (it is just a simple vertical concatenation)

# In[ ]:


import pandas as pd
import gc
import time
import datetime
# MARRIAGE

path1 = '/data/processed_data/DVV/Tulokset_1900-2010_tutkhenk_aviohist.txt.finreg_IDs'
start_time = time.time()
df1 = pd.read_csv(path1,sep = ';', encoding='latin-1', header=None)
run_time = time.time()-start_time;print(run_time)

# Add column names
df1.columns =['FINREGISTRYID','Current_marital_status','Spouse_personal_ID','Spouse_not_in_system','Order_no','Starting_date','Ending_day','Ending_reason']
#df1['Starting_date'] = df1['Starting_date'].astype(str)

# change date formats for 'Starting_date' and 'Ending_day'
df1['Starting_date'] = pd.to_datetime(df1['Starting_date'], format="%Y%m%d",errors='coerce')
df1['Starting_date'] = df1['Starting_date'].dt.strftime('%Y-%m-%d')

df1['Ending_day'] = pd.to_datetime(df1['Ending_day'], format="%Y%m%d",errors='coerce')
df1['Ending_day'] = df1['Ending_day'].dt.strftime('%Y-%m-%d')

#write to csv
df1.to_csv('/data/processed_data/DVV/Tulokset_1900-2010_tutkhenk_aviohist.txt.finreg_IDsp',index=False) # ,index=False, encoding='latin-1'


# In[ ]:


import pandas as pd
import gc
import time
import datetime
path2 = '/data/processed_data/dvv/joined_unprocessed/Tulokset_1900-2010_tutkhenk_asuinhist.txt.finreg_IDs'
start_time = time.time()
df2 = pd.read_csv(path2,sep = ';', encoding='latin-1', header=None, dtype=str)
run_time = time.time()-start_time;print(run_time)

# Add column names
df2.columns =['FINREGISTRYID','Residence_type','Start_of_residence','End_of_residence','Municipality','Municipality_name','Building_ID','Residence_code','Post_code','Latitude','Longitude']

# change date formats for 'Start_of_residence' and 'End_of_residence'
df2['Start_of_residence'] = pd.to_datetime(df2['Start_of_residence'], format="%Y%m%d",errors='coerce')
df2['Start_of_residence'] = df2['Start_of_residence'].dt.strftime('%Y-%m-%d')

df2['End_of_residence'] = pd.to_datetime(df2['End_of_residence'], format="%Y%m%d",errors='coerce')
df2['End_of_residence'] = df2['End_of_residence'].dt.strftime('%Y-%m-%d')

#write to csv
df2.to_csv('/data/processed_data/dvv/Tulokset_1900-2010_tutkhenk_asuinhist.txt.finreg_IDsp',index=False) # ,index=False, encoding='latin-1'


# In[ ]:


path3 = '/data/processed_data/DVV/Tulokset_1900-2010_tutkhenk_ja_sukulaiset.txt.finreg_IDs'
start_time = time.time()
df3 = pd.read_csv(path3,sep = ';', encoding='latin-1', header=None)
run_time = time.time()-start_time;print(run_time)

# Add column names
df3.columns =['FINREGISTRYID','Relationship','How_kinship_has_formed','Relative_ID','Relative_DOB','Relative_death_date','Sex','Mother_tongue',
              'Country_of_residence','Country_name','Emigration_date','Home_town','Municipality_name']

# change date formats for 'Relative_DOB', 'Relative_death_date', Emigration_date
df3['Relative_DOB'] = pd.to_datetime(df3['Relative_DOB'], format="%Y%m%d",errors='coerce')
df3['Relative_DOB'] = df3['Relative_DOB'].dt.strftime('%Y-%m-%d')

df3['Relative_death_date'] = pd.to_datetime(df3['Relative_death_date'], format="%Y%m%d",errors='coerce')
df3['Relative_death_date'] = df3['Relative_death_date'].dt.strftime('%Y-%m-%d')

df3['Emigration_date'] = pd.to_datetime(df3['Emigration_date'], format="%Y%m%d",errors='coerce')
df3['Emigration_date'] = df3['Emigration_date'].dt.strftime('%Y-%m-%d')


#write to csv
df3.to_csv('/data/processed_data/DVV/Tulokset_1900-2010_tutkhenk_ja_sukulaiset.txt.finreg_IDsp',index=False) # ,index=False, encoding='latin-1'
