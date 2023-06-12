#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import pandas as pd
import gc
import time
import datetime

path1 = '/data/original_data/thl_social_assistance/3214_FinRegistry_puolisontoitu_MattssonHannele07122020.csv.finreg_IDs'
path2 = '/data/original_data/thl_social_assistance/3214_FinRegistry_toitu_MattssonHannele07122020.csv.finreg_IDs'
sep = ';' # '\t' cancer / ';' DVV, THL
start_time = time.time()
df1 = pd.read_csv(path1,sep = sep, encoding='utf-8') #, delim_whitespace=True) # error_bad_lines=False , sep = '/t', engine='python'  , header=None 
run_time = time.time()-start_time
print(run_time)

start_time = time.time()
df2 = pd.read_csv(path2,sep = sep, encoding='utf-8') #, delim_whitespace=True) # error_bad_lines=False , sep = '/t', engine='python'  , header=None 
run_time = time.time()-start_time
print(run_time)


# In[ ]:

# save file 1
df1.to_csv('/data/processed_data/thl_social_assistance/spouse_provision_2023-05-29.csv', sep=",", index = False)
df1.to_csv('/data/processed_data/thl_social_assistance/spouse_provision.csv', sep=",", index = False)
df1.to_feather("/data/processed_data/thl_social_assistance/spouse_provision_2023-05-29.feather")
df1.to_feather("/data/processed_data/thl_social_assistance/spouse_provision.feather")

# save file 2
df2.to_csv('/data/processed_data/thl_social_assistance/provision_2023-05-29.csv', sep=",", index = False)
df2.to_csv('/data/processed_data/thl_social_assistance/provision.csv', sep=",", index = False)
df2.to_feather("/data/processed_data/thl_social_assistance/provision_2023-05-29.feather")
df2.to_feather("/data/processed_data/thl_social_assistance/provision.feather")
