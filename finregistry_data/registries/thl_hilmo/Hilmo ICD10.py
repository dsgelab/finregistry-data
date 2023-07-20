#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import pandas as pd
import gc
import time
import datetime


# ## Data update files for a period 2020-2021

# In[ ]:


path = '/data/original_data/thl_hilmo/THL2021_2196_HILMO_2019_2021.csv.finreg_IDs'
sep = ';' # '\t' cancer / ';' DVV, THL
start_time = time.time()
df4 = pd.read_csv(path,sep = sep, encoding='latin-1',dtype={"TUPVA": "string","LANTTUPVA": "string","LANTKASPVA": "string","JONOPVM": "string","LPVM": "string"}) #, delim_whitespace=True) # error_bad_lines=False , sep = '/t', engine='python'  , header=None 
run_time = time.time()-start_time
print(run_time)

df4['TUPVA'] = pd.to_datetime(df4['TUPVA'], errors='coerce',format='%d.%m.%Y %H:%M')
df4['TUPVA'] = df4['TUPVA'].dt.strftime('%Y-%m-%d')

df4['LANTTUPVA'] = pd.to_datetime(df4['LANTTUPVA'],errors='coerce',format='%d.%m.%Y %H:%M')
df4['LANTTUPVA'] = df4['LANTTUPVA'].dt.strftime('%Y-%m-%d')

df4['LANTKASPVA'] = pd.to_datetime(df4['LANTKASPVA'],errors='coerce',format='%d.%m.%Y %H:%M')
df4['LANTKASPVA'] = df4['LANTKASPVA'].dt.strftime('%Y-%m-%d')

df4['JONOPVM'] = pd.to_datetime(df4['JONOPVM'],errors='coerce',format='%d.%m.%Y %H:%M')
df4['JONOPVM'] = df4['JONOPVM'].dt.strftime('%Y-%m-%d')

df4['LPVM'] = pd.to_datetime(df4['LPVM'],errors='coerce',format='%d.%m.%Y %H:%M')
df4['LPVM'] = df4['LPVM'].dt.strftime('%Y-%m-%d')

df4.to_csv('/data/processed_data/thl_hilmo/THL2021_2196_HILMO_2019_2021.csv.finreg_IDsp',index=False)


# In[ ]:


path = '/data/original_data/thl_hilmo/THL2021_2196_HILMO_LAAKITYS.csv.finreg_IDs'
sep = ';' # '\t' cancer / ';' DVV, THL
start_time = time.time()
df1 = pd.read_csv(path,sep = sep, encoding='latin-1',dtype={"MAAR_PVM": "string"}) #, delim_whitespace=True) # error_bad_lines=False , sep = '/t', engine='python'  , header=None 
run_time = time.time()-start_time
print(run_time)

# change date format from ddMONyyyy:hh:mm:ss to YYYY-MM-DD

df1['MAAR_PVM'] = pd.to_datetime(df1['MAAR_PVM'], format="%d%b%Y:%H:%M:%S",errors='coerce') # 15MAY2015:00:00:00
df1['MAAR_PVM'] = df1['MAAR_PVM'].dt.strftime('%Y-%m-%d')


df1.to_csv('/data/processed_data/thl_hilmo/THL2021_2196_HILMO_LAAKITYS.csv.finreg_IDsp',index=False)


# In[ ]:


path = '/data/original_data/thl_hilmo/THL2021_2196_HILMO_TOIMP.csv.finreg_IDs'
sep = ';' # '\t' cancer / ';' DVV, THL
start_time = time.time()
df2 = pd.read_csv(path,sep = sep, encoding='latin-1',dtype={"TOIMPALKUPVM": "string", "TOIMPLOPPUPVM": "string"}) #, delim_whitespace=True) # error_bad_lines=False , sep = '/t', engine='python'  , header=None 
run_time = time.time()-start_time
print(run_time)

# chanhge date fromat for two columns from  dd.mm.yyyy hh:mm to YYYY-MM-DD

df2['TOIMPALKUPVM'] = pd.to_datetime(df2['TOIMPALKUPVM'],errors='coerce',format='%d.%m.%Y %H:%M')
df2['TOIMPALKUPVM'] = df2['TOIMPALKUPVM'].dt.strftime('%Y-%m-%d')

df2['TOIMPLOPPUPVM'] = pd.to_datetime(df2['TOIMPLOPPUPVM'],errors='coerce',format='%d.%m.%Y %H:%M')
df2['TOIMPLOPPUPVM'] = df2['TOIMPLOPPUPVM'].dt.strftime('%Y-%m-%d')

df2.to_csv('/data/processed_data/thl_hilmo/THL2021_2196_HILMO_TOIMP.csv.finreg_IDsp',index=False)


# In[ ]:


# For the rest of the Hilmo files just change separator from ";" to "," (open files and save with "," spearator)

# THL2021_2196_HILMO_2019_2021.csv.finreg_IDs
# THL2021_2196_HILMO_DIAG.csv.finreg_IDs
# THL2021_2196_HILMO_HAITMP.csv.finreg_IDs
# THL2021_2196_HILMO_HHAITTA.csv.finreg_IDs
# THL2021_2196_HILMO_LAAKITYS.csv.finreg_IDs ---
# THL2021_2196_HILMO_PSYKLAAKE.csv.finreg_IDs
# THL2021_2196_HILMO_PSYKP.csv.finreg_IDs
# THL2021_2196_HILMO_PSYKPPAK.csv.finreg_IDs
# THL2021_2196_HILMO_SYP.csv.finreg_IDs
# THL2021_2196_HILMO_TEHOHOITO.csv.finreg_IDs
# THL2021_2196_HILMO_TOIMP.csv.finreg_IDs ---
# THL2021_2196_HILMO_TULOSYY.csv.finreg_IDs


# In[ ]:


path = '/data/original_data/thl_hilmo/THL2021_2196_HILMO_DIAG.csv.finreg_IDs'
sep = ';' # '\t' cancer / ';' DVV, THL
start_time = time.time()
df3 = pd.read_csv(path,sep = sep, encoding='latin-1') #dtype={"TOIMPALKUPVM": "string", "TOIMPLOPPUPVM": "string"}, delim_whitespace=True) # error_bad_lines=False , sep = '/t', engine='python'  , header=None 
run_time = time.time()-start_time
print(run_time)
print(df3.shape)
df3.to_csv('/data/processed_data/thl_hilmo/THL2021_2196_HILMO_DIAG.csv.finreg_IDsp',index=False)


# In[ ]:


path = '/data/original_data/thl_hilmo/THL2021_2196_HILMO_HAITMP.csv.finreg_IDs'
sep = ';' # '\t' cancer / ';' DVV, THL
start_time = time.time()
df3 = pd.read_csv(path,sep = sep, encoding='latin-1') #dtype={"TOIMPALKUPVM": "string", "TOIMPLOPPUPVM": "string"}, delim_whitespace=True) # error_bad_lines=False , sep = '/t', engine='python'  , header=None 
run_time = time.time()-start_time
print(run_time)
print(df3.shape)
df3.to_csv('/data/processed_data/thl_hilmo/THL2021_2196_HILMO_HAITMP.csv.finreg_IDsp',index=False)


# In[ ]:


path = '/data/original_data/thl_hilmo/THL2021_2196_HILMO_HHAITTA.csv.finreg_IDs'
sep = ';' # '\t' cancer / ';' DVV, THL
start_time = time.time()
df3 = pd.read_csv(path,sep = sep, encoding='latin-1') #dtype={"TOIMPALKUPVM": "string", "TOIMPLOPPUPVM": "string"}, delim_whitespace=True) # error_bad_lines=False , sep = '/t', engine='python'  , header=None 
run_time = time.time()-start_time
print(run_time)
print(df3.shape)
df3.to_csv('/data/processed_data/thl_hilmo/THL2021_2196_HILMO_HHAITTA.csv.finreg_IDsp',index=False)


# In[ ]:


path = '/data/original_data/thl_hilmo/THL2021_2196_HILMO_PSYKLAAKE.csv.finreg_IDs'
sep = ';' # '\t' cancer / ';' DVV, THL
start_time = time.time()
df3 = pd.read_csv(path,sep = sep, encoding='latin-1') #dtype={"TOIMPALKUPVM": "string", "TOIMPLOPPUPVM": "string"}, delim_whitespace=True) # error_bad_lines=False , sep = '/t', engine='python'  , header=None 
run_time = time.time()-start_time
print(run_time)
print(df3.shape)
df3.to_csv('/data/processed_data/thl_hilmo/THL2021_2196_HILMO_PSYKLAAKE.csv.finreg_IDsp',index=False)


# In[ ]:


path = '/data/original_data/thl_hilmo/THL2021_2196_HILMO_PSYKP.csv.finreg_IDs'
sep = ';' # '\t' cancer / ';' DVV, THL
start_time = time.time()
df3 = pd.read_csv(path,sep = sep, encoding='latin-1') #dtype={"TOIMPALKUPVM": "string", "TOIMPLOPPUPVM": "string"}, delim_whitespace=True) # error_bad_lines=False , sep = '/t', engine='python'  , header=None 
run_time = time.time()-start_time
print(run_time)
print(df3.shape)
df3.to_csv('/data/processed_data/thl_hilmo/THL2021_2196_HILMO_PSYKP.csv.finreg_IDsp',index=False)


# In[ ]:


path = '/data/original_data/thl_hilmo/THL2021_2196_HILMO_PSYKPPAK.csv.finreg_IDs'
sep = ';' # '\t' cancer / ';' DVV, THL
start_time = time.time()
df3 = pd.read_csv(path,sep = sep, encoding='latin-1') #dtype={"TOIMPALKUPVM": "string", "TOIMPLOPPUPVM": "string"}, delim_whitespace=True) # error_bad_lines=False , sep = '/t', engine='python'  , header=None 
run_time = time.time()-start_time
print(run_time)
print(df3.shape)
df3.to_csv('/data/processed_data/thl_hilmo/THL2021_2196_HILMO_PSYKPPAK.csv.finreg_IDsp',index=False)


# In[ ]:


path = '/data/original_data/thl_hilmo/THL2021_2196_HILMO_SYP.csv.finreg_IDs'
sep = ';' # '\t' cancer / ';' DVV, THL
start_time = time.time()
df3 = pd.read_csv(path,sep = sep, encoding='latin-1') #dtype={"TOIMPALKUPVM": "string", "TOIMPLOPPUPVM": "string"}, delim_whitespace=True) # error_bad_lines=False , sep = '/t', engine='python'  , header=None 
run_time = time.time()-start_time
print(run_time)
print(df3.shape)
df3.to_csv('/data/processed_data/thl_hilmo/THL2021_2196_HILMO_SYP.csv.finreg_IDsp',index=False)


# In[ ]:


path = '/data/original_data/thl_hilmo/THL2021_2196_HILMO_TEHOHOITO.csv.finreg_IDs'
sep = ';' # '\t' cancer / ';' DVV, THL
start_time = time.time()
df3 = pd.read_csv(path,sep = sep, encoding='latin-1') #dtype={"TOIMPALKUPVM": "string", "TOIMPLOPPUPVM": "string"}, delim_whitespace=True) # error_bad_lines=False , sep = '/t', engine='python'  , header=None 
run_time = time.time()-start_time
print(run_time)
print(df3.shape)
df3.to_csv('/data/processed_data/thl_hilmo/THL2021_2196_HILMO_TEHOHOITO.csv.finreg_IDsp',index=False)


# In[ ]:


path = '/data/original_data/thl_hilmo/THL2021_2196_HILMO_TULOSYY.csv.finreg_IDs'
sep = ';' # '\t' cancer / ';' DVV, THL
start_time = time.time()
df3 = pd.read_csv(path,sep = sep, encoding='latin-1') #dtype={"TOIMPALKUPVM": "string", "TOIMPLOPPUPVM": "string"}, delim_whitespace=True) # error_bad_lines=False , sep = '/t', engine='python'  , header=None 
run_time = time.time()-start_time
print(run_time)
print(df3.shape)
df3.to_csv('/data/processed_data/thl_hilmo/THL2021_2196_HILMO_TULOSYY.csv.finreg_IDsp',index=False)


# ## Old files for a period up to 2019

# In[ ]:


path = '/data/original_data/thl_hilmo/thl2019_1776_hilmo.csv.finreg_IDs'
sep = ';' # '\t' cancer / ';' DVV, THL
start_time = time.time()
df4 = pd.read_csv(path,sep = sep, encoding='latin-1',dtype={"TUPVA": "string","LANTTUPVA": "string","LANTKASPVA": "string","JONOPVM": "string","LPVM": "string"}) #, delim_whitespace=True) # error_bad_lines=False , sep = '/t', engine='python'  , header=None 
run_time = time.time()-start_time
print(run_time)

df4['TUPVA'] = pd.to_datetime(df4['TUPVA'], errors='coerce',format='%d.%m.%Y %H:%M')
df4['TUPVA'] = df4['TUPVA'].dt.strftime('%Y-%m-%d')


df4['LANTTUPVA'] = pd.to_datetime(df4['LANTTUPVA'],errors='coerce',format='%d.%m.%Y %H:%M')
df4['LANTTUPVA'] = df4['LANTTUPVA'].dt.strftime('%Y-%m-%d')

df4['LANTKASPVA'] = pd.to_datetime(df4['LANTKASPVA'],errors='coerce',format='%d.%m.%Y %H:%M')
df4['LANTKASPVA'] = df4['LANTKASPVA'].dt.strftime('%Y-%m-%d')

df4['JONOPVM'] = pd.to_datetime(df4['JONOPVM'],errors='coerce',format='%d.%m.%Y %H:%M')
df4['JONOPVM'] = df4['JONOPVM'].dt.strftime('%Y-%m-%d')

df4['LPVM'] = pd.to_datetime(df4['LPVM'],errors='coerce',format='%d.%m.%Y %H:%M')
df4['LPVM'] = df4['LPVM'].dt.strftime('%Y-%m-%d')

df4.to_csv('/data/processed_data/thl_hilmo/thl2019_1776_hilmo.csv.finreg_IDsp',index=False)


# In[ ]:


path = '/data/original_data/thl_hilmo/thl2019_1776_hilmo_laakkeet.csv.finreg_IDs'
sep = ';' # '\t' cancer / ';' DVV, THL
start_time = time.time()
df1 = pd.read_csv(path,sep = sep, encoding='latin-1',dtype={"MAAR_PVM": "string"}) #, delim_whitespace=True) # error_bad_lines=False , sep = '/t', engine='python'  , header=None 
run_time = time.time()-start_time
print(run_time)

# change date format from ddMONyyyy:hh:mm:ss to YYYY-MM-DD

df1['MAAR_PVM'] = pd.to_datetime(df1['MAAR_PVM'], format="%d%b%Y:%H:%M:%S",errors='coerce') # 15MAY2015:00:00:00
df1['MAAR_PVM'] = df1['MAAR_PVM'].dt.strftime('%Y-%m-%d')


df1.to_csv('/data/processed_data/thl_hilmo/thl2019_1776_hilmo_laakkeet.csv.finreg_IDsp',index=False)


# In[ ]:


path = '/data/original_data/thl_hilmo/thl2019_1776_hilmo_toimenpide.csv.finreg_IDs'
sep = ';' # '\t' cancer / ';' DVV, THL
start_time = time.time()
df2 = pd.read_csv(path,sep = sep, encoding='latin-1',dtype={"TOIMPALKUPVM": "string", "TOIMPLOPPUPVM": "string"}) #, delim_whitespace=True) # error_bad_lines=False , sep = '/t', engine='python'  , header=None 
run_time = time.time()-start_time
print(run_time)

# chanhge date fromat for two columns from  dd.mm.yyyy hh:mm to YYYY-MM-DD

df2['TOIMPALKUPVM'] = pd.to_datetime(df2['TOIMPALKUPVM'],errors='coerce',format='%d.%m.%Y %H:%M')
df2['TOIMPALKUPVM'] = df2['TOIMPALKUPVM'].dt.strftime('%Y-%m-%d')

df2['TOIMPLOPPUPVM'] = pd.to_datetime(df2['TOIMPLOPPUPVM'],errors='coerce',format='%d.%m.%Y %H:%M')
df2['TOIMPLOPPUPVM'] = df2['TOIMPLOPPUPVM'].dt.strftime('%Y-%m-%d')

df2.to_csv('/data/processed_data/thl_hilmo/thl2019_1776_hilmo_toimenpide.csv.finreg_IDsp',index=False)


# In[ ]:


# For the rest of the Hilmo files just change separator from ";" to "," (open files and save with "," spearator) like below: 


# In[ ]:


path = '/data/original_data/thl_hilmo/thl2019_1776_hilmo_tusyy.csv.finreg_IDs'
sep = ';' # '\t' cancer / ';' DVV, THL
start_time = time.time()
df3 = pd.read_csv(path,sep = sep, encoding='latin-1') #dtype={"TOIMPALKUPVM": "string", "TOIMPLOPPUPVM": "string"}, delim_whitespace=True) # error_bad_lines=False , sep = '/t', engine='python'  , header=None 
run_time = time.time()-start_time
print(run_time)
print(df3.shape)
df3.to_csv('/data/processed_data/thl_hilmo/thl2019_1776_hilmo_tusyy.csv.finreg_IDsp',index=False)
