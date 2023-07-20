#!/usr/bin/env python
# coding: utf-8

# ## Data update files for a period 2029-2021

# In[ ]:


import pandas as pd
import gc
import time
import datetime


path = '/data/original_data/thl_avohilmo/THL2021_2196_AVOHILMO_2020.csv.finreg_IDs'
sep = ';' # '\t' cancer / ';' DVV, THL
start_time = time.time()
df = pd.read_csv(path,sep = sep, encoding='latin-1',dtype={"SEURANTATIETUE_PAIVITETTY": "string","YHTEYDENOTTO_AJANKOHTA": "string","HOIDONTARVE_AJANKOHTA": "string","AJANVARAUS_AJANKOHTA": "string","AJANVARAUS_VARATTU": "string","KAYNTI_ALKOI": "string","KAYNTI_LOPPUI": "string"}) #, delim_whitespace=True) # error_bad_lines=False , sep = '/t', engine='python'  , header=None 
run_time = time.time()-start_time
print(run_time)


# In[ ]:


df['SEURANTATIETUE_PAIVITETTY'] = pd.to_datetime(df['SEURANTATIETUE_PAIVITETTY'], errors='coerce',format='%d.%m.%Y %H:%M')
df['SEURANTATIETUE_PAIVITETTY'] = df['SEURANTATIETUE_PAIVITETTY'].dt.strftime('%Y-%m-%d')


# In[ ]:


df['YHTEYDENOTTO_AJANKOHTA'] = pd.to_datetime(df['YHTEYDENOTTO_AJANKOHTA'], errors='coerce',format='%d.%m.%Y %H:%M')
df['YHTEYDENOTTO_AJANKOHTA'] = df['YHTEYDENOTTO_AJANKOHTA'].dt.strftime('%Y-%m-%d')


# In[ ]:


df['HOIDONTARVE_AJANKOHTA'] = pd.to_datetime(df['HOIDONTARVE_AJANKOHTA'], errors='coerce',format='%d.%m.%Y %H:%M')
df['HOIDONTARVE_AJANKOHTA'] = df['HOIDONTARVE_AJANKOHTA'].dt.strftime('%Y-%m-%d')


# In[ ]:


df['AJANVARAUS_AJANKOHTA'] = pd.to_datetime(df['AJANVARAUS_AJANKOHTA'], errors='coerce',format='%d.%m.%Y %H:%M')
df['AJANVARAUS_AJANKOHTA'] = df['AJANVARAUS_AJANKOHTA'].dt.strftime('%Y-%m-%d')


# In[ ]:


df['AJANVARAUS_VARATTU'] = pd.to_datetime(df['AJANVARAUS_VARATTU'], errors='coerce',format='%d.%m.%Y %H:%M')
df['AJANVARAUS_VARATTU'] = df['AJANVARAUS_VARATTU'].dt.strftime('%Y-%m-%d')


# In[ ]:


df['KAYNTI_ALKOI'] = pd.to_datetime(df['KAYNTI_ALKOI'], errors='coerce',format='%d.%m.%Y %H:%M')
df['KAYNTI_ALKOI'] = df['KAYNTI_ALKOI'].dt.strftime('%Y-%m-%d')


# In[ ]:


df['KAYNTI_LOPPUI'] = pd.to_datetime(df['KAYNTI_LOPPUI'], errors='coerce',format='%d.%m.%Y %H:%M')
df['KAYNTI_LOPPUI'] = df['KAYNTI_LOPPUI'].dt.strftime('%Y-%m-%d')


# In[ ]:


df.to_csv('/data/processed_data/thl_avohilmo/THL2021_2196_AVOHILMO_2020.csv.finreg_IDsp',index=False)


# In[ ]:


import pandas as pd
import gc
import time
import datetime


path = '/data/original_data/thl_avohilmo/THL2021_2196_AVOHILMO_2021.csv.finreg_IDs'
sep = ';' # '\t' cancer / ';' DVV, THL
start_time = time.time()
df = pd.read_csv(path,sep = sep, encoding='latin-1',dtype={"SEURANTATIETUE_PAIVITETTY": "string","YHTEYDENOTTO_AJANKOHTA": "string","HOIDONTARVE_AJANKOHTA": "string","AJANVARAUS_AJANKOHTA": "string","AJANVARAUS_VARATTU": "string","KAYNTI_ALKOI": "string","KAYNTI_LOPPUI": "string"}) #, delim_whitespace=True) # error_bad_lines=False , sep = '/t', engine='python'  , header=None 
run_time = time.time()-start_time
print(run_time)


# In[ ]:


df['SEURANTATIETUE_PAIVITETTY'] = pd.to_datetime(df['SEURANTATIETUE_PAIVITETTY'], errors='coerce',format='%d.%m.%Y %H:%M')
df['SEURANTATIETUE_PAIVITETTY'] = df['SEURANTATIETUE_PAIVITETTY'].dt.strftime('%Y-%m-%d')


# In[ ]:


df['YHTEYDENOTTO_AJANKOHTA'] = pd.to_datetime(df['YHTEYDENOTTO_AJANKOHTA'], errors='coerce',format='%d.%m.%Y %H:%M')
df['YHTEYDENOTTO_AJANKOHTA'] = df['YHTEYDENOTTO_AJANKOHTA'].dt.strftime('%Y-%m-%d')


# In[ ]:


df['HOIDONTARVE_AJANKOHTA'] = pd.to_datetime(df['HOIDONTARVE_AJANKOHTA'], errors='coerce',format='%d.%m.%Y %H:%M')
df['HOIDONTARVE_AJANKOHTA'] = df['HOIDONTARVE_AJANKOHTA'].dt.strftime('%Y-%m-%d')


# In[ ]:


df['AJANVARAUS_AJANKOHTA'] = pd.to_datetime(df['AJANVARAUS_AJANKOHTA'], errors='coerce',format='%d.%m.%Y %H:%M')
df['AJANVARAUS_AJANKOHTA'] = df['AJANVARAUS_AJANKOHTA'].dt.strftime('%Y-%m-%d')


# In[ ]:


df['AJANVARAUS_VARATTU'] = pd.to_datetime(df['AJANVARAUS_VARATTU'], errors='coerce',format='%d.%m.%Y %H:%M')
df['AJANVARAUS_VARATTU'] = df['AJANVARAUS_VARATTU'].dt.strftime('%Y-%m-%d')


# In[ ]:


df['KAYNTI_ALKOI'] = pd.to_datetime(df['KAYNTI_ALKOI'], errors='coerce',format='%d.%m.%Y %H:%M')
df['KAYNTI_ALKOI'] = df['KAYNTI_ALKOI'].dt.strftime('%Y-%m-%d')


# In[ ]:


df['KAYNTI_LOPPUI'] = pd.to_datetime(df['KAYNTI_LOPPUI'], errors='coerce',format='%d.%m.%Y %H:%M')
df['KAYNTI_LOPPUI'] = df['KAYNTI_LOPPUI'].dt.strftime('%Y-%m-%d')


# In[ ]:


df.to_csv('/data/processed_data/thl_avohilmo/THL2021_2196_AVOHILMO_2021.csv.finreg_IDsp',index=False)


# ## Old files for a period up to 2019

# In[ ]:


import pandas as pd
import gc
import time
import datetime


path = '/data/original_data/thl_avohilmo/thl2019_1776_avohilmo_19_20.csv.finreg_IDs'
sep = ';' # '\t' cancer / ';' DVV, THL
start_time = time.time()
df = pd.read_csv(path,sep = sep, encoding='latin-1',dtype={"SEURANTATIETUE_PAIVITETTY": "string","YHTEYDENOTTO_AJANKOHTA": "string","HOIDONTARVE_AJANKOHTA": "string","AJANVARAUS_AJANKOHTA": "string","AJANVARAUS_VARATTU": "string","KAYNTI_ALKOI": "string","KAYNTI_LOPPUI": "string"}) #, delim_whitespace=True) # error_bad_lines=False , sep = '/t', engine='python'  , header=None 
run_time = time.time()-start_time
print(run_time)


# In[ ]:


df['SEURANTATIETUE_PAIVITETTY'] = pd.to_datetime(df['SEURANTATIETUE_PAIVITETTY'], errors='coerce',format='%d.%m.%Y %H:%M')
df['SEURANTATIETUE_PAIVITETTY'] = df['SEURANTATIETUE_PAIVITETTY'].dt.strftime('%Y-%m-%d')


# In[ ]:


df['YHTEYDENOTTO_AJANKOHTA'] = pd.to_datetime(df['YHTEYDENOTTO_AJANKOHTA'], errors='coerce',format='%d.%m.%Y %H:%M')
df['YHTEYDENOTTO_AJANKOHTA'] = df['YHTEYDENOTTO_AJANKOHTA'].dt.strftime('%Y-%m-%d')


# In[ ]:


df['HOIDONTARVE_AJANKOHTA'] = pd.to_datetime(df['HOIDONTARVE_AJANKOHTA'], errors='coerce',format='%d.%m.%Y %H:%M')
df['HOIDONTARVE_AJANKOHTA'] = df['HOIDONTARVE_AJANKOHTA'].dt.strftime('%Y-%m-%d')


# In[ ]:


df['AJANVARAUS_AJANKOHTA'] = pd.to_datetime(df['AJANVARAUS_AJANKOHTA'], errors='coerce',format='%d.%m.%Y %H:%M')
df['AJANVARAUS_AJANKOHTA'] = df['AJANVARAUS_AJANKOHTA'].dt.strftime('%Y-%m-%d')


# In[ ]:


df['AJANVARAUS_VARATTU'] = pd.to_datetime(df['AJANVARAUS_VARATTU'], errors='coerce',format='%d.%m.%Y %H:%M')
df['AJANVARAUS_VARATTU'] = df['AJANVARAUS_VARATTU'].dt.strftime('%Y-%m-%d')


# In[ ]:


df['KAYNTI_ALKOI'] = pd.to_datetime(df['KAYNTI_ALKOI'], errors='coerce',format='%d.%m.%Y %H:%M')
df['KAYNTI_ALKOI'] = df['KAYNTI_ALKOI'].dt.strftime('%Y-%m-%d')


# In[ ]:


df['KAYNTI_LOPPUI'] = pd.to_datetime(df['KAYNTI_LOPPUI'], errors='coerce',format='%d.%m.%Y %H:%M')
df['KAYNTI_LOPPUI'] = df['KAYNTI_LOPPUI'].dt.strftime('%Y-%m-%d')


# In[ ]:


df.to_csv('/data/processed_data/thl_avohilmo/thl2019_1776_avohilmo_19_20.csv.finreg_IDsp',index=False)


# In[ ]:


import pandas as pd
import gc
import time
import datetime


path = '/data/original_data/thl_avohilmo/thl2019_1776_avohilmo_17_18.csv.finreg_IDs'
sep = ';' # '\t' cancer / ';' DVV, THL
start_time = time.time()
df = pd.read_csv(path,sep = sep, encoding='latin-1',dtype={"SEURANTATIETUE_PAIVITETTY": "string","YHTEYDENOTTO_AJANKOHTA": "string","HOIDONTARVE_AJANKOHTA": "string","AJANVARAUS_AJANKOHTA": "string","AJANVARAUS_VARATTU": "string","KAYNTI_ALKOI": "string","KAYNTI_LOPPUI": "string"}) #, delim_whitespace=True) # error_bad_lines=False , sep = '/t', engine='python'  , header=None 
run_time = time.time()-start_time
print(run_time)


# In[ ]:


df['SEURANTATIETUE_PAIVITETTY'] = pd.to_datetime(df['SEURANTATIETUE_PAIVITETTY'], errors='coerce',format='%d.%m.%Y %H:%M')
df['SEURANTATIETUE_PAIVITETTY'] = df['SEURANTATIETUE_PAIVITETTY'].dt.strftime('%Y-%m-%d')


# In[ ]:


df['YHTEYDENOTTO_AJANKOHTA'] = pd.to_datetime(df['YHTEYDENOTTO_AJANKOHTA'], errors='coerce',format='%d.%m.%Y %H:%M')
df['YHTEYDENOTTO_AJANKOHTA'] = df['YHTEYDENOTTO_AJANKOHTA'].dt.strftime('%Y-%m-%d')


# In[ ]:


df['HOIDONTARVE_AJANKOHTA'] = pd.to_datetime(df['HOIDONTARVE_AJANKOHTA'], errors='coerce',format='%d.%m.%Y %H:%M')
df['HOIDONTARVE_AJANKOHTA'] = df['HOIDONTARVE_AJANKOHTA'].dt.strftime('%Y-%m-%d')


# In[ ]:


df['AJANVARAUS_AJANKOHTA'] = pd.to_datetime(df['AJANVARAUS_AJANKOHTA'], errors='coerce',format='%d.%m.%Y %H:%M')
df['AJANVARAUS_AJANKOHTA'] = df['AJANVARAUS_AJANKOHTA'].dt.strftime('%Y-%m-%d')


# In[ ]:


df['AJANVARAUS_VARATTU'] = pd.to_datetime(df['AJANVARAUS_VARATTU'], errors='coerce',format='%d.%m.%Y %H:%M')
df['AJANVARAUS_VARATTU'] = df['AJANVARAUS_VARATTU'].dt.strftime('%Y-%m-%d')


# In[ ]:


df['KAYNTI_ALKOI'] = pd.to_datetime(df['KAYNTI_ALKOI'], errors='coerce',format='%d.%m.%Y %H:%M')
df['KAYNTI_ALKOI'] = df['KAYNTI_ALKOI'].dt.strftime('%Y-%m-%d')


# In[ ]:


df['KAYNTI_LOPPUI'] = pd.to_datetime(df['KAYNTI_LOPPUI'], errors='coerce',format='%d.%m.%Y %H:%M')
df['KAYNTI_LOPPUI'] = df['KAYNTI_LOPPUI'].dt.strftime('%Y-%m-%d')


# In[ ]:


df.to_csv('/data/processed_data/thl_avohilmo/thl2019_1776_avohilmo_17_18.csv.finreg_IDsp',index=False)


# In[ ]:


import pandas as pd
import gc
import time
import datetime


path = '/data/original_data/thl_avohilmo/thl2019_1776_avohilmo_15_16.csv.finreg_IDs'
sep = ';' # '\t' cancer / ';' DVV, THL
start_time = time.time()
df = pd.read_csv(path,sep = sep, encoding='latin-1',dtype={"SEURANTATIETUE_PAIVITETTY": "string","YHTEYDENOTTO_AJANKOHTA": "string","HOIDONTARVE_AJANKOHTA": "string","AJANVARAUS_AJANKOHTA": "string","AJANVARAUS_VARATTU": "string","KAYNTI_ALKOI": "string","KAYNTI_LOPPUI": "string"}) #, delim_whitespace=True) # error_bad_lines=False , sep = '/t', engine='python'  , header=None 
run_time = time.time()-start_time
print(run_time)


# In[ ]:


df['SEURANTATIETUE_PAIVITETTY'] = pd.to_datetime(df['SEURANTATIETUE_PAIVITETTY'], errors='coerce',format='%d.%m.%Y %H:%M')
df['SEURANTATIETUE_PAIVITETTY'] = df['SEURANTATIETUE_PAIVITETTY'].dt.strftime('%Y-%m-%d')


# In[ ]:


df['YHTEYDENOTTO_AJANKOHTA'] = pd.to_datetime(df['YHTEYDENOTTO_AJANKOHTA'], errors='coerce',format='%d.%m.%Y %H:%M')
df['YHTEYDENOTTO_AJANKOHTA'] = df['YHTEYDENOTTO_AJANKOHTA'].dt.strftime('%Y-%m-%d')


# In[ ]:


df['HOIDONTARVE_AJANKOHTA'] = pd.to_datetime(df['HOIDONTARVE_AJANKOHTA'], errors='coerce',format='%d.%m.%Y %H:%M')
df['HOIDONTARVE_AJANKOHTA'] = df['HOIDONTARVE_AJANKOHTA'].dt.strftime('%Y-%m-%d')


# In[ ]:


df['AJANVARAUS_AJANKOHTA'] = pd.to_datetime(df['AJANVARAUS_AJANKOHTA'], errors='coerce',format='%d.%m.%Y %H:%M')
df['AJANVARAUS_AJANKOHTA'] = df['AJANVARAUS_AJANKOHTA'].dt.strftime('%Y-%m-%d')


# In[ ]:


df['AJANVARAUS_VARATTU'] = pd.to_datetime(df['AJANVARAUS_VARATTU'], errors='coerce',format='%d.%m.%Y %H:%M')
df['AJANVARAUS_VARATTU'] = df['AJANVARAUS_VARATTU'].dt.strftime('%Y-%m-%d')


# In[ ]:


df['KAYNTI_ALKOI'] = pd.to_datetime(df['KAYNTI_ALKOI'], errors='coerce',format='%d.%m.%Y %H:%M')
df['KAYNTI_ALKOI'] = df['KAYNTI_ALKOI'].dt.strftime('%Y-%m-%d')


# In[ ]:


df['KAYNTI_LOPPUI'] = pd.to_datetime(df['KAYNTI_LOPPUI'], errors='coerce',format='%d.%m.%Y %H:%M')
df['KAYNTI_LOPPUI'] = df['KAYNTI_LOPPUI'].dt.strftime('%Y-%m-%d')


# In[ ]:


df.to_csv('/data/processed_data/thl_avohilmo/thl2019_1776_avohilmo_15_16.csv.finreg_IDsp',index=False)


# In[ ]:


import pandas as pd
import gc
import time
import datetime


path = '/data/original_data/thl_avohilmo/thl2019_1776_avohilmo_13_14.csv.finreg_IDs'
sep = ';' # '\t' cancer / ';' DVV, THL
start_time = time.time()
df = pd.read_csv(path,sep = sep, encoding='latin-1',dtype={"SEURANTATIETUE_PAIVITETTY": "string","YHTEYDENOTTO_AJANKOHTA": "string","HOIDONTARVE_AJANKOHTA": "string","AJANVARAUS_AJANKOHTA": "string","AJANVARAUS_VARATTU": "string","KAYNTI_ALKOI": "string","KAYNTI_LOPPUI": "string"}) #, delim_whitespace=True) # error_bad_lines=False , sep = '/t', engine='python'  , header=None 
run_time = time.time()-start_time
print(run_time)


# In[ ]:


df['SEURANTATIETUE_PAIVITETTY'] = pd.to_datetime(df['SEURANTATIETUE_PAIVITETTY'], errors='coerce',format='%d.%m.%Y %H:%M')
df['SEURANTATIETUE_PAIVITETTY'] = df['SEURANTATIETUE_PAIVITETTY'].dt.strftime('%Y-%m-%d')


# In[ ]:


df['YHTEYDENOTTO_AJANKOHTA'] = pd.to_datetime(df['YHTEYDENOTTO_AJANKOHTA'], errors='coerce',format='%d.%m.%Y %H:%M')
df['YHTEYDENOTTO_AJANKOHTA'] = df['YHTEYDENOTTO_AJANKOHTA'].dt.strftime('%Y-%m-%d')


# In[ ]:


df['HOIDONTARVE_AJANKOHTA'] = pd.to_datetime(df['HOIDONTARVE_AJANKOHTA'], errors='coerce',format='%d.%m.%Y %H:%M')
df['HOIDONTARVE_AJANKOHTA'] = df['HOIDONTARVE_AJANKOHTA'].dt.strftime('%Y-%m-%d')


# In[ ]:


df['AJANVARAUS_AJANKOHTA'] = pd.to_datetime(df['AJANVARAUS_AJANKOHTA'], errors='coerce',format='%d.%m.%Y %H:%M')
df['AJANVARAUS_AJANKOHTA'] = df['AJANVARAUS_AJANKOHTA'].dt.strftime('%Y-%m-%d')


# In[ ]:


df['AJANVARAUS_VARATTU'] = pd.to_datetime(df['AJANVARAUS_VARATTU'], errors='coerce',format='%d.%m.%Y %H:%M')
df['AJANVARAUS_VARATTU'] = df['AJANVARAUS_VARATTU'].dt.strftime('%Y-%m-%d')


# In[ ]:


df['KAYNTI_ALKOI'] = pd.to_datetime(df['KAYNTI_ALKOI'], errors='coerce',format='%d.%m.%Y %H:%M')
df['KAYNTI_ALKOI'] = df['KAYNTI_ALKOI'].dt.strftime('%Y-%m-%d')


# In[ ]:


df['KAYNTI_LOPPUI'] = pd.to_datetime(df['KAYNTI_LOPPUI'], errors='coerce',format='%d.%m.%Y %H:%M')
df['KAYNTI_LOPPUI'] = df['KAYNTI_LOPPUI'].dt.strftime('%Y-%m-%d')


# In[ ]:


df.to_csv('/data/processed_data/thl_avohilmo/thl2019_1776_avohilmo_13_14.csv.finreg_IDsp',index=False)


# In[ ]:


import pandas as pd
import gc
import time
import datetime


path = '/data/original_data/thl_avohilmo/thl2019_1776_avohilmo_11_12.csv.finreg_IDs'
sep = ';' # '\t' cancer / ';' DVV, THL
start_time = time.time()
df = pd.read_csv(path,sep = sep, encoding='latin-1',dtype={"SEURANTATIETUE_PAIVITETTY": "string","YHTEYDENOTTO_AJANKOHTA": "string","HOIDONTARVE_AJANKOHTA": "string","AJANVARAUS_AJANKOHTA": "string","AJANVARAUS_VARATTU": "string","KAYNTI_ALKOI": "string","KAYNTI_LOPPUI": "string"}) #, delim_whitespace=True) # error_bad_lines=False , sep = '/t', engine='python'  , header=None 
run_time = time.time()-start_time
print(run_time)


# In[ ]:


df['SEURANTATIETUE_PAIVITETTY'] = pd.to_datetime(df['SEURANTATIETUE_PAIVITETTY'], errors='coerce',format='%d.%m.%Y %H:%M')
df['SEURANTATIETUE_PAIVITETTY'] = df['SEURANTATIETUE_PAIVITETTY'].dt.strftime('%Y-%m-%d')


# In[ ]:


df['YHTEYDENOTTO_AJANKOHTA'] = pd.to_datetime(df['YHTEYDENOTTO_AJANKOHTA'], errors='coerce',format='%d.%m.%Y %H:%M')
df['YHTEYDENOTTO_AJANKOHTA'] = df['YHTEYDENOTTO_AJANKOHTA'].dt.strftime('%Y-%m-%d')


# In[ ]:


df['HOIDONTARVE_AJANKOHTA'] = pd.to_datetime(df['HOIDONTARVE_AJANKOHTA'], errors='coerce',format='%d.%m.%Y %H:%M')
df['HOIDONTARVE_AJANKOHTA'] = df['HOIDONTARVE_AJANKOHTA'].dt.strftime('%Y-%m-%d')


# In[ ]:


df['AJANVARAUS_AJANKOHTA'] = pd.to_datetime(df['AJANVARAUS_AJANKOHTA'], errors='coerce',format='%d.%m.%Y %H:%M')
df['AJANVARAUS_AJANKOHTA'] = df['AJANVARAUS_AJANKOHTA'].dt.strftime('%Y-%m-%d')


# In[ ]:


df['AJANVARAUS_VARATTU'] = pd.to_datetime(df['AJANVARAUS_VARATTU'], errors='coerce',format='%d.%m.%Y %H:%M')
df['AJANVARAUS_VARATTU'] = df['AJANVARAUS_VARATTU'].dt.strftime('%Y-%m-%d')


# In[ ]:


df['KAYNTI_ALKOI'] = pd.to_datetime(df['KAYNTI_ALKOI'], errors='coerce',format='%d.%m.%Y %H:%M')
df['KAYNTI_ALKOI'] = df['KAYNTI_ALKOI'].dt.strftime('%Y-%m-%d')


# In[ ]:


df['KAYNTI_LOPPUI'] = pd.to_datetime(df['KAYNTI_LOPPUI'], errors='coerce',format='%d.%m.%Y %H:%M')
df['KAYNTI_LOPPUI'] = df['KAYNTI_LOPPUI'].dt.strftime('%Y-%m-%d')


# In[ ]:


df.to_csv('/data/processed_data/thl_avohilmo/thl2019_1776_avohilmo_11_12.csv.finreg_IDsp',index=False)
