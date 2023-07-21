#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import pandas as pd
import gc
import time
import datetime


path = '/data/original_data/soshilmo/thl2019_1776_soshilmo.csv.finreg_IDs'
sep = ';' # '\t' cancer / ';' DVV, THL
start_time = time.time()
df = pd.read_csv(path,sep = sep, encoding='latin-1') #, delim_whitespace=True) # error_bad_lines=False , sep = '/t', engine='python'  , header=None 
run_time = time.time()-start_time
print(run_time)


# Change date format in clumns: 'TUPVA', 'LPVM', from  dd.mm.yyyy hh:mm to YYYY-MM-DD

df['TUPVA'] = pd.to_datetime(df['TUPVA'], errors='coerce',format='%d.%m.%Y %H:%M')
df['TUPVA'] = df['TUPVA'].dt.strftime('%Y-%m-%d')

df['LPVM'] = pd.to_datetime(df['LPVM'], errors='coerce',format='%d.%m.%Y %H:%M')
df['LPVM'] = df['LPVM'].dt.strftime('%Y-%m-%d')

# corect gender formating for several values
df.at[1044301, 'SUKUP'] = 1
df.loc[(df['TNRO'] == 'FR5071802'),'SUKUP'] = 1

df.to_csv('/data/processed_data/thl2019_1776_soshilmo.csv.finreg_IDsp',index=False)
