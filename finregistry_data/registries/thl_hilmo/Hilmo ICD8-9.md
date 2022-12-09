

```python
import pandas as pd
import gc
import time
import datetime


path = '/data/original_data/thl_hilmo/thl2019_1776_poisto_6986.csv.finreg_IDs'
sep = ';' # '\t' cancer / ';' DVV, THL
start_time = time.time()
df1 = pd.read_csv(path,sep = sep, encoding='latin-1',dtype={"TULOPV": "string", "LAHTOPV": "string"}) #, delim_whitespace=True) # error_bad_lines=False , sep = '/t', engine='python'  , header=None 
run_time = time.time()-start_time
print(run_time)

# chanhge date fromat for two columns from  dd.mm.yyyy hh:mm to YYYY-MM-DD

df1['TULOPV'] = pd.to_datetime(df1['TULOPV'], errors='coerce',format='%d.%m.%Y %H:%M')
df1['TULOPV'] = df1['TULOPV'].dt.strftime('%Y-%m-%d')

df1['LAHTOPV'] = pd.to_datetime(df1['LAHTOPV'], errors='coerce',format='%d.%m.%Y %H:%M')
df1['LAHTOPV'] = df1['LAHTOPV'].dt.strftime('%Y-%m-%d')

df1.to_csv('/data/processed_data/thl_hilmo/thl2019_1776_poisto_6986.csv.finreg_IDsp',index=False)
```


```python
path2 = '/data/original_data/thl_hilmo/thl2019_1776_poisto_8793.csv.finreg_IDs'
sep = ';' # '\t' cancer / ';' DVV, THL
start_time = time.time()
df2 = pd.read_csv(path2,sep = sep, encoding='latin-1',dtype={"TUPVA": "string", "LPVM": "string","JOPVM": "string"}) #, delim_whitespace=True) # error_bad_lines=False , sep = '/t', engine='python'  , header=None 
run_time = time.time()-start_time
print(run_time)

# chanhge date fromat for two columns from  dd.mm.yyyy hh:mm to YYYY-MM-DD

df2['TUPVA'] = pd.to_datetime(df2['TUPVA'], errors='coerce',format='%d.%m.%Y %H:%M')
df2['TUPVA'] = df2['TUPVA'].dt.strftime('%Y-%m-%d')

df2['LPVM'] = pd.to_datetime(df2['LPVM'], errors='coerce',format='%d.%m.%Y %H:%M')
df2['LPVM'] = df2['LPVM'].dt.strftime('%Y-%m-%d')

df2['JOPVM'] = pd.to_datetime(df2['JOPVM'], errors='coerce',format='%d.%m.%Y %H:%M')
df2['JOPVM'] = df2['JOPVM'].dt.strftime('%Y-%m-%d')

df2.to_csv('/data/processed_data/thl_hilmo/thl2019_1776_poisto_8793.csv.finreg_IDsp',index=False)
```