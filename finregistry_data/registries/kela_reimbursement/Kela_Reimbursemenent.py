#!/usr/bin/env python
# coding: utf-8

# # New file up to 2021 (inclusive)

# In[ ]:


import pandas as pd
import gc
import time
import datetime

path = '/data/original_data/kela_reimbursement/81_522_2022_KORVAUSOIKEUDET.csv.finreg_IDs'
sep = ';' # '\t' cancer / ';' DVV, THL
start_time = time.time()
df = pd.read_csv(path,sep = sep, dtype={"korvausoikeus_alpv": "string","korvausoikeus_lopv": "string" }) #, delim_whitespace=True) # error_bad_lines=False , sep = '/t', engine='python'  , header=None, encoding='latin-1'
run_time = time.time()-start_time
print(run_time)

df.rename(columns={'korvausoikeus_alpv': 'KORVAUSOIKEUS_ALPV','korvausoikeus_lopv':'KORVAUSOIKEUS_LOPV'}, inplace=True)

df.to_csv('/data/processed_data/kela_reimbursement/81_522_2022_KORVAUSOIKEUDET.csv.finreg_IDsp',index=False) 


# # OLD file up to 2019 (inclusive)

# In[ ]:


import pandas as pd
import gc
import time
import datetime


path = '/data/original_data/kela_reimbursement/175_522_2020_LAAKEKORVAUSOIKEUDET.csv.finreg_IDs'
sep = ';' # '\t' cancer / ';' DVV, THL
start_time = time.time()
df = pd.read_csv(path,sep = sep, encoding='latin-1', dtype={"APVM": "string","ALPV": "string" }) #, delim_whitespace=True) # error_bad_lines=False , sep = '/t', engine='python'  , header=None 
run_time = time.time()-start_time
print(run_time)

df['APVM'] = pd.to_datetime(df['APVM'], errors='coerce',format='%Y%m')
df['APVM'] = df['APVM'].dt.strftime('%Y-%m')

df['LPVM'] = pd.to_datetime(df['LPVM'], errors='coerce',format='%Y%m')
df['LPVM'] = df['LPVM'].dt.strftime('%Y-%m')


df.to_csv('/data/processed_data/kela_reimbursement/175_522_2020_LAAKEKORVAUSOIKEUDET.csv.finreg_IDsp',index=False) 
