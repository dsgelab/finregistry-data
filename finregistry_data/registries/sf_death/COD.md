
## Data update files for a period up to 2020


```python
import pandas as pd
import gc
import time
import datetime


path = '/data/original_data/sf_death/thl2021_2196_ksyy_tutkimus.csv.finreg_IDs'
sep = ';' # '\t' cancer / ';' DVV, THL
start_time = time.time()
df1 = pd.read_csv(path,sep = sep, encoding='latin-1') #, delim_whitespace=True) # error_bad_lines=False , sep = '/t', engine='python'  , header=None 
run_time = time.time()-start_time
print(run_time)


df1['KPV'] = pd.to_datetime(df1['KPV'],format='%d.%m.%Y %H:%M')
df1['KPV'] = df1['KPV'].dt.strftime('%Y-%m-%d')

df1.to_csv('/data/processed_data/sf_death/thl2021_2196_ksyy_tutkimus.csv.finreg_IDsp',index=False)

path2 = '/data/original_data/sf_death/thl2021_2196_ksyy_vuosi.csv.finreg_IDs'
sep = ';' # '\t' cancer / ';' DVV, THL
start_time = time.time()
df2 = pd.read_csv(path2,sep = sep, encoding='latin-1') #, delim_whitespace=True) # error_bad_lines=False , sep = '/t', engine='python'  , header=None 
run_time = time.time()-start_time
print(run_time)

df2['KPV'] = pd.to_datetime(df2['KPV'],format='%d.%m.%Y %H:%M')
df2['KPV'] = df2['KPV'].dt.strftime('%Y-%m-%d')

df2.to_csv('/data/processed_data/sf_death/thl2021_2196_ksyy_vuosi.csv.finreg_IDsp',index=False)
```

## Old files for a period up to 2019


```python
import pandas as pd
import gc
import time
import datetime


path = '/data/original_data/sf_death/thl2019_1776_ksyy_tutkimus.csv.finreg_IDs'
sep = ';' # '\t' cancer / ';' DVV, THL
start_time = time.time()
df1 = pd.read_csv(path,sep = sep, encoding='latin-1') #, delim_whitespace=True) # error_bad_lines=False , sep = '/t', engine='python'  , header=None 
run_time = time.time()-start_time
print(run_time)

df1['KPV'] = pd.to_datetime(df1['KPV'],format='%d.%m.%Y %H:%M')
df1['KPV'] = df1['KPV'].dt.strftime('%Y-%m-%d')

df1.to_csv('/data/processed_data/sf_death/thl2019_1776_ksyy_tutkimus.csv.finreg_IDsp',index=False)

path2 = '/data/original_data/sf_death/thl2019_1776_ksyy_vuosi.csv.finreg_IDs'
sep = ';' # '\t' cancer / ';' DVV, THL
start_time = time.time()
df2 = pd.read_csv(path2,sep = sep, encoding='latin-1') #, delim_whitespace=True) # error_bad_lines=False , sep = '/t', engine='python'  , header=None 
run_time = time.time()-start_time
print(run_time)

df2['KPV'] = pd.to_datetime(df2['KPV'],format='%d.%m.%Y %H:%M')
df2['KPV'] = df2['KPV'].dt.strftime('%Y-%m-%d')

df2.to_csv('/data/processed_data/sf_death/thl2019_1776_ksyy_vuosi.csv.finreg_IDsp',index=False)
```