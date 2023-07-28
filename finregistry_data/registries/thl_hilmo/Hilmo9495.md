

```python
import pandas as pd
import gc
import time
import datetime


path = '/data/original_data/thl_hilmo/thl2019_1776_hilmo_9495.csv.finreg_IDs'
sep = ';' # '\t' cancer / ';' DVV, THL
start_time = time.time()
df1 = pd.read_csv(path,sep = sep, encoding='latin-1',dtype={"TUPVA": "string", "JOPVM": "string",}) #, delim_whitespace=True) # error_bad_lines=False , sep = '/t', engine='python'  , header=None 
run_time = time.time()-start_time
print(run_time)

# chanhge date fromat for three columns from  dd.mm.yyyy hh:mm to YYYY-MM-DD

df1['TUPVA'] = pd.to_datetime(df1['TUPVA'],format='%d.%m.%Y %H:%M', errors='coerce')
df1['TUPVA'] = df1['TUPVA'].dt.strftime('%Y-%m-%d')

df1['JOPVM'] = pd.to_datetime(df1['JOPVM'],format='%d.%m.%Y %H:%M', errors='coerce')
df1['JOPVM'] = df1['JOPVM'].dt.strftime('%Y-%m-%d')

df1['LPVM'] = pd.to_datetime(df1['LPVM'],format='%d.%m.%Y %H:%M', errors='coerce')
df1['LPVM'] = df1['LPVM'].dt.strftime('%Y-%m-%d')

df1.to_csv('/data/processed_data/thl_hilmo/thl2019_1776_hilmo_9495.csv.finreg_IDsp',index=False)
```


```python
path = '/data/original_data/thl_hilmo/thl2019_1776_hilmo_9495_psykp.csv.finreg_IDs'
sep = ';' # '\t' cancer / ';' DVV, THL
start_time = time.time()
df2 = pd.read_csv(path,sep = sep, encoding='latin-1',dtype={"TUPVA": "string", "JOPVM": "string",}) #, delim_whitespace=True) # error_bad_lines=False , sep = '/t', engine='python'  , header=None 
run_time = time.time()-start_time
print(run_time)
df2.to_csv('/data/processed_data/thl_hilmo/thl2019_1776_hilmo_9495_psykp.csv.finreg_IDsp',index=False)
```


```python
path = '/data/original_data/thl_hilmo/thl2019_1776_hilmo_9495_syp.csv.finreg_IDs'
sep = ';' # '\t' cancer / ';' DVV, THL
start_time = time.time()
df3 = pd.read_csv(path,sep = sep, encoding='latin-1',dtype={"TUPVA": "string", "JOPVM": "string",}) #, delim_whitespace=True) # error_bad_lines=False , sep = '/t', engine='python'  , header=None 
run_time = time.time()-start_time
print(run_time)
df3.to_csv('/data/processed_data/thl_hilmo/thl2019_1776_hilmo_9495_syp.csv.finreg_IDsp',index=False)
```
