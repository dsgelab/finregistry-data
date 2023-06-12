
## Data update files for a period 2020-2021


```python
import pandas as pd
import gc
import time
import datetime


path = '/data/original_data/thl_avohilmo/THL2021_2196_AVOHILMO_LAAKE.csv.finreg_IDs'
sep = ';' # '\t' cancer / ';' DVV, THL
start_time = time.time()
df = pd.read_csv(path,sep = sep, encoding='latin-1',dtype={"LAAKE_MAARATTY": "string"}) #, delim_whitespace=True) # error_bad_lines=False , sep = '/t', engine='python'  , header=None 
run_time = time.time()-start_time
print(run_time)


df['LAAKE_MAARATTY'] = pd.to_datetime(df['LAAKE_MAARATTY'], errors='coerce',format='%d.%m.%Y %H:%M')
df['LAAKE_MAARATTY'] = df['LAAKE_MAARATTY'].dt.strftime('%Y-%m-%d')

df.to_csv('/data/processed_data/thl_avohilmo/THL2021_2196_AVOHILMO_LAAKE.csv.finreg_IDsp',index=False)
```


```python
import numpy as np
#import math
def year(x):
#    if math.isnan(x):
#        return np.nan

    try:
        return x[0:4]
    except AttributeError:
        return np.nan
    except ValueError:
        return np.nan
    except TypeError:
        return np.nan
    
with pd.option_context('display.max_rows', 100, 'display.max_columns', 50):  # more options can be specified also
    print(df['LAAKE_MAARATTY'].apply(year).value_counts(dropna=False).sort_index(ascending=True))
```


```python
path = '/data/original_data/thl_avohilmo/THL2021_2196_AVOHILMO_LAHETE.csv.finreg_IDs'
sep = ';' # '\t' cancer / ';' DVV, THL
start_time = time.time()
df = pd.read_csv(path,sep = sep, encoding='latin-1',dtype={"LAHETE_AJANKOHTA": "string"}) #, delim_whitespace=True) # error_bad_lines=False , sep = '/t', engine='python'  , header=None 
run_time = time.time()-start_time
print(run_time)

df['LAHETE_AJANKOHTA'] = pd.to_datetime(df['LAHETE_AJANKOHTA'], errors='coerce',format='%d.%m.%Y %H:%M')
df['LAHETE_AJANKOHTA'] = df['LAHETE_AJANKOHTA'].dt.strftime('%Y-%m-%d')

df.to_csv('/data/processed_data/thl_avohilmo/THL2021_2196_AVOHILMO_LAHETE.csv.finreg_IDsp',index=False)
```


```python
with pd.option_context('display.max_rows', 100, 'display.max_columns', 50):  # more options can be specified also
    print(df['LAHETE_AJANKOHTA'].apply(year).value_counts(dropna=False).sort_index(ascending=True))
```


```python
path = '/data/original_data/thl_avohilmo/THL2021_2196_AVOHILMO_ROKOTUS.csv.finreg_IDs'
sep = ';' # '\t' cancer / ';' DVV, THL
start_time = time.time()
df = pd.read_csv(path,sep = sep, encoding='latin-1',dtype={"LAHETE_AJANKOHTA": "string"}) #, delim_whitespace=True) # error_bad_lines=False , sep = '/t', engine='python'  , header=None 
run_time = time.time()-start_time
print(run_time)

df['LAAKE_MAARATTY'] = pd.to_datetime(df['LAAKE_MAARATTY'], errors='coerce',format='%d.%m.%Y %H:%M')
df['LAAKE_MAARATTY'] = df['LAAKE_MAARATTY'].dt.strftime('%Y-%m-%d')

df['ROKOTE_ANTOPVM'] = pd.to_datetime(df['ROKOTE_ANTOPVM'], errors='coerce',format='%d.%m.%Y %H:%M')
df['ROKOTE_ANTOPVM'] = df['ROKOTE_ANTOPVM'].dt.strftime('%Y-%m-%d')

#with pd.option_context('display.max_rows', 100, 'display.max_columns', 50):  # more options can be specified also
#    print(df['LAAKE_MAARATTY'].apply(year).value_counts().sort_index(ascending=True))
             
#with pd.option_context('display.max_rows', 100, 'display.max_columns', 50):  # more options can be specified also
#    print(df['ROKOTE_ANTOPVM'].apply(year).value_counts().sort_index(ascending=True))             
    
df.to_csv('/data/processed_data/thl_avohilmo/THL2021_2196_AVOHILMO_ROKOTUS.csv.finreg_IDsp',index=False)
```


```python
with pd.option_context('display.max_rows', 100, 'display.max_columns', 50):  # more options can be specified also
    print(df['LAAKE_MAARATTY'].apply(year).value_counts(dropna=False).sort_index(ascending=True))
```


```python
with pd.option_context('display.max_rows', 100, 'display.max_columns', 50):  # more options can be specified also
    print(df['ROKOTE_ANTOPVM'].apply(year).value_counts(dropna=False).sort_index(ascending=True))
```

### For the rest of the files change separator from ';' to ',' 


```python
# changing separator from ';' to ','
path = '/data/original_data/thl_avohilmo/THL2021_2196_AVOHILMO_ICD10_DIAG.csv.finreg_IDs'
sep = ';' # '\t' cancer / ';' DVV, THL
start_time = time.time()
df = pd.read_csv(path,sep = sep, encoding='latin-1') # , encoding='latin-1' dtype={ "LAHETE_AJANKOHTA": "string"} delim_whitespace=True) # error_bad_lines=False , sep = '/t', engine='python'  , header=None 
run_time = time.time()-start_time
print(run_time)

df.to_csv('/data/processed_data/thl_avohilmo/THL2021_2196_AVOHILMO_ICD10_DIAG.csv.finreg_IDsp',index=False)
```


```python
# changing separator from ';' to ','
path = '/data/original_data/thl_avohilmo/THL2021_2196_AVOHILMO_JATKOH.csv.finreg_IDs'
sep = ';' # '\t' cancer / ';' DVV, THL
start_time = time.time()
df = pd.read_csv(path,sep = sep, encoding='latin-1') # , encoding='latin-1' dtype={ "LAHETE_AJANKOHTA": "string"} delim_whitespace=True) # error_bad_lines=False , sep = '/t', engine='python'  , header=None 
run_time = time.time()-start_time
print(run_time)

df.to_csv('/data/processed_data/thl_avohilmo/THL2021_2196_AVOHILMO_JATKOH.csv.finreg_IDsp',index=False)
```

    71.27313947677612



```python
# changing separator from ';' to ','
path = '/data/original_data/thl_avohilmo/THL2021_2196_AVOHILMO_ICPC2_DIAG.csv.finreg_IDs'
sep = ';' # '\t' cancer / ';' DVV, THL
start_time = time.time()
df = pd.read_csv(path,sep = sep, encoding='latin-1') # , encoding='latin-1' dtype={ "LAHETE_AJANKOHTA": "string"} delim_whitespace=True) # error_bad_lines=False , sep = '/t', engine='python'  , header=None 
run_time = time.time()-start_time
print(run_time)

df.to_csv('/data/processed_data/thl_avohilmo/THL2021_2196_AVOHILMO_ICPC2_DIAG.csv.finreg_IDsp',index=False)
```


```python
# changing separator from ';' to ','
path = '/data/original_data/thl_avohilmo/THL2021_2196_AVOHILMO_KOTIHOITO.csv.finreg_IDs'
sep = ';' # '\t' cancer / ';' DVV, THL
start_time = time.time()
df = pd.read_csv(path,sep = sep, encoding='latin-1') # , encoding='latin-1' dtype={ "LAHETE_AJANKOHTA": "string"} delim_whitespace=True) # error_bad_lines=False , sep = '/t', engine='python'  , header=None 
run_time = time.time()-start_time
print(run_time)

df.to_csv('/data/processed_data/thl_avohilmo/THL2021_2196_AVOHILMO_KOTIHOITO.csv.finreg_IDsp',index=False)
```

    49.76960301399231



```python
# changing separator from ';' to ','
path = '/data/original_data/thl_avohilmo/THL2021_2196_AVOHILMO_ROKOSUOJA.csv.finreg_IDs'
sep = ';' # '\t' cancer / ';' DVV, THL
start_time = time.time()
df = pd.read_csv(path,sep = sep, encoding='latin-1') # , encoding='latin-1' dtype={ "LAHETE_AJANKOHTA": "string"} delim_whitespace=True) # error_bad_lines=False , sep = '/t', engine='python'  , header=None 
run_time = time.time()-start_time
print(run_time)

df.to_csv('/data/processed_data/thl_avohilmo/THL2021_2196_AVOHILMO_ROKOSUOJA.csv.finreg_IDsp',index=False)
```

    5.275746583938599



```python
# changing separator from ';' to ','
path = '/data/original_data/thl_avohilmo/thl2021_2196_avohilmo_suu_toimp.csv.finreg_IDs'
sep = ';' # '\t' cancer / ';' DVV, THL
start_time = time.time()
df = pd.read_csv(path,sep = sep, encoding='latin-1') # , encoding='latin-1' dtype={ "LAHETE_AJANKOHTA": "string"} delim_whitespace=True) # error_bad_lines=False , sep = '/t', engine='python'  , header=None 
run_time = time.time()-start_time
print(run_time)

df.to_csv('/data/processed_data/thl_avohilmo/thl2021_2196_avohilmo_suu_toimp.csv.finreg_IDsp',index=False)
```

    15.250893354415894



```python
# changing separator from ';' to ','
path = '/data/original_data/thl_avohilmo/THL2021_2196_AVOHILMO_TOIMP.csv.finreg_IDs'
sep = ';' # '\t' cancer / ';' DVV, THL
start_time = time.time()
df = pd.read_csv(path,sep = sep, encoding='latin-1') # , encoding='latin-1' dtype={ "LAHETE_AJANKOHTA": "string"} delim_whitespace=True) # error_bad_lines=False , sep = '/t', engine='python'  , header=None 
run_time = time.time()-start_time
print(run_time)

df.to_csv('/data/processed_data/thl_avohilmo/THL2021_2196_AVOHILMO_TOIMP.csv.finreg_IDsp',index=False)
```

    82.13827466964722



```python
#filenames
#THL2021_2196_AVOHILMO_ICD10_DIAG.csv.finreg_IDs
#THL2021_2196_AVOHILMO_ICPC2_DIAG.csv.finreg_IDs
#THL2021_2196_AVOHILMO_JATKOH.csv.finreg_IDs
#THL2021_2196_AVOHILMO_KOTIHOITO.csv.finreg_IDs
#THL2021_2196_AVOHILMO_LAAKE.csv.finreg_IDs v
#THL2021_2196_AVOHILMO_LAHETE.csv.finreg_IDs v
#THL2021_2196_AVOHILMO_ROKOSUOJA.csv.finreg_IDs
#THL2021_2196_AVOHILMO_ROKOTUS.csv.finreg_IDs v

```

## Old files for a period up to 2019


```python
import pandas as pd
import gc
import time
import datetime


path = '/data/original_data/thl_avohilmo/thl2019_1776_avohilmo_17_20_laake.csv.finreg_IDs'
sep = ';' # '\t' cancer / ';' DVV, THL
start_time = time.time()
df = pd.read_csv(path,sep = sep, encoding='latin-1',dtype={"LAAKE_MAARATTY": "string"}) #, delim_whitespace=True) # error_bad_lines=False , sep = '/t', engine='python'  , header=None 
run_time = time.time()-start_time
print(run_time)


df['LAAKE_MAARATTY'] = pd.to_datetime(df['LAAKE_MAARATTY'], errors='coerce',format='%d.%m.%Y %H:%M')
df['LAAKE_MAARATTY'] = df['LAAKE_MAARATTY'].dt.strftime('%Y-%m-%d')

df.to_csv('/data/processed_data/thl_avohilmo/thl2019_1776_avohilmo_17_20_laake.csv.finreg_IDsp',index=False)
```


```python
import numpy as np
#import math
def year(x):
#    if math.isnan(x):
#        return np.nan

    try:
        return x[0:4]
    except AttributeError:
        return np.nan
    except ValueError:
        return np.nan
    except TypeError:
        return np.nan
    
with pd.option_context('display.max_rows', 100, 'display.max_columns', 50):  # more options can be specified also
    print(df['LAAKE_MAARATTY'].apply(year).value_counts(dropna=False).sort_index(ascending=True))
```


```python
path = '/data/original_data/thl_avohilmo/thl2019_1776_avohilmo_laake.csv.finreg_IDs'
sep = ';' # '\t' cancer / ';' DVV, THL
start_time = time.time()
df = pd.read_csv(path,sep = sep, encoding='latin-1',dtype={"LAAKE_MAARATTY": "string"}) #, delim_whitespace=True) # error_bad_lines=False , sep = '/t', engine='python'  , header=None 
run_time = time.time()-start_time
print(run_time)

df['LAAKE_MAARATTY'] = pd.to_datetime(df['LAAKE_MAARATTY'], errors='coerce',format='%d.%m.%Y %H:%M')
df['LAAKE_MAARATTY'] = df['LAAKE_MAARATTY'].dt.strftime('%Y-%m-%d')

#df.to_csv('/data/processed_data/thl_avohilmo/thl2019_1776_avohilmo_laake.csv.finreg_IDsp',index=False)
```


```python
with pd.option_context('display.max_rows', 100, 'display.max_columns', 50):  # more options can be specified also
    print(df['LAAKE_MAARATTY'].apply(year).value_counts(dropna=False).sort_index(ascending=True))
```


```python
path = '/data/original_data/thl_avohilmo/thl2019_1776_avohilmo_17_20_lahete.csv.finreg_IDs'
sep = ';' # '\t' cancer / ';' DVV, THL
start_time = time.time()
df = pd.read_csv(path,sep = sep, encoding='latin-1',dtype={"LAHETE_AJANKOHTA": "string"}) #, delim_whitespace=True) # error_bad_lines=False , sep = '/t', engine='python'  , header=None 
run_time = time.time()-start_time
print(run_time)

df['LAHETE_AJANKOHTA'] = pd.to_datetime(df['LAHETE_AJANKOHTA'], errors='coerce',format='%d.%m.%Y %H:%M')
df['LAHETE_AJANKOHTA'] = df['LAHETE_AJANKOHTA'].dt.strftime('%Y-%m-%d')

df.to_csv('/data/processed_data/thl_avohilmo/thl2019_1776_avohilmo_17_20_lahete.csv.finreg_IDsp',index=False)
```


```python
with pd.option_context('display.max_rows', 100, 'display.max_columns', 50):  # more options can be specified also
    print(df['LAHETE_AJANKOHTA'].apply(year).value_counts(dropna=False).sort_index(ascending=True))
```


```python
path = '/data/original_data/thl_avohilmo/thl2019_1776_avohilmo_lahete.csv.finreg_IDs'
sep = ';' # '\t' cancer / ';' DVV, THL
start_time = time.time()
df = pd.read_csv(path,sep = sep, encoding='latin-1',dtype={"LAHETE_AJANKOHTA": "string"}) #, delim_whitespace=True) # error_bad_lines=False , sep = '/t', engine='python'  , header=None 
run_time = time.time()-start_time
print(run_time)

df['LAHETE_AJANKOHTA'] = pd.to_datetime(df['LAHETE_AJANKOHTA'], errors='coerce',format='%d.%m.%Y %H:%M')
df['LAHETE_AJANKOHTA'] = df['LAHETE_AJANKOHTA'].dt.strftime('%Y-%m-%d')

#with pd.option_context('display.max_rows', 100, 'display.max_columns', 50):  # more options can be specified also
#    print(df['LAHETE_AJANKOHTA'].apply(year).value_counts().sort_index(ascending=True))
    
df.to_csv('/data/processed_data/thl_avohilmo/thl2019_1776_avohilmo_lahete.csv.finreg_IDsp',index=False)
```


```python
path = '/data/original_data/thl_avohilmo/thl2019_1776_avohilmo_17_20_rokotus.csv.finreg_IDs'
sep = ';' # '\t' cancer / ';' DVV, THL
start_time = time.time()
df = pd.read_csv(path,sep = sep, encoding='latin-1',dtype={"LAHETE_AJANKOHTA": "string"}) #, delim_whitespace=True) # error_bad_lines=False , sep = '/t', engine='python'  , header=None 
run_time = time.time()-start_time
print(run_time)

df['LAAKE_MAARATTY'] = pd.to_datetime(df['LAAKE_MAARATTY'], errors='coerce',format='%d.%m.%Y %H:%M')
df['LAAKE_MAARATTY'] = df['LAAKE_MAARATTY'].dt.strftime('%Y-%m-%d')

df['ROKOTE_ANTOPVM'] = pd.to_datetime(df['ROKOTE_ANTOPVM'], errors='coerce',format='%d.%m.%Y %H:%M')
df['ROKOTE_ANTOPVM'] = df['ROKOTE_ANTOPVM'].dt.strftime('%Y-%m-%d')

#with pd.option_context('display.max_rows', 100, 'display.max_columns', 50):  # more options can be specified also
#    print(df['LAAKE_MAARATTY'].apply(year).value_counts().sort_index(ascending=True))
             
#with pd.option_context('display.max_rows', 100, 'display.max_columns', 50):  # more options can be specified also
#    print(df['ROKOTE_ANTOPVM'].apply(year).value_counts().sort_index(ascending=True))             
    
df.to_csv('/data/processed_data/thl_avohilmo/thl2019_1776_avohilmo_17_20_rokotus.csv.finreg_IDsp',index=False)
```


```python
path = '/data/original_data/thl_avohilmo/thl2019_1776_avohilmo_rokotus.csv.finreg_IDs'
sep = ';' # '\t' cancer / ';' DVV, THL
start_time = time.time()
df = pd.read_csv(path,sep = sep, encoding='latin-1',dtype={"LAHETE_AJANKOHTA": "string"}) #, delim_whitespace=True) # error_bad_lines=False , sep = '/t', engine='python'  , header=None 
run_time = time.time()-start_time
print(run_time)

df['LAAKE_MAARATTY'] = pd.to_datetime(df['LAAKE_MAARATTY'], errors='coerce',format='%d.%m.%Y %H:%M')
df['LAAKE_MAARATTY'] = df['LAAKE_MAARATTY'].dt.strftime('%Y-%m-%d')

df['ROKOTE_ANTOPVM'] = pd.to_datetime(df['ROKOTE_ANTOPVM'], errors='coerce',format='%d.%m.%Y %H:%M')
df['ROKOTE_ANTOPVM'] = df['ROKOTE_ANTOPVM'].dt.strftime('%Y-%m-%d')

#with pd.option_context('display.max_rows', 100, 'display.max_columns', 50):  # more options can be specified also
#    print(df['LAAKE_MAARATTY'].apply(year).value_counts().sort_index(ascending=True))
             
#with pd.option_context('display.max_rows', 100, 'display.max_columns', 50):  # more options can be specified also
#    print(df['ROKOTE_ANTOPVM'].apply(year).value_counts().sort_index(ascending=True))             
    
df.to_csv('/data/processed_data/thl_avohilmo/thl2019_1776_avohilmo_rokotus.csv.finreg_IDsp',index=False)
```

### For the rest of the files change separator from ';' to ',' like below


```python
# changing separator from ';' to ','
path = '/data/original_data/thl_avohilmo/thl2019_1776_avohilmo_toimenpide.csv.finreg_IDs'
sep = ';' # '\t' cancer / ';' DVV, THL
start_time = time.time()
df = pd.read_csv(path,sep = sep, encoding='latin-1') # , encoding='latin-1' dtype={ "LAHETE_AJANKOHTA": "string"} delim_whitespace=True) # error_bad_lines=False , sep = '/t', engine='python'  , header=None 
run_time = time.time()-start_time
print(run_time)

df.to_csv('/data/processed_data/thl_avohilmo/thl2019_1776_avohilmo_toimenpide.csv.finreg_IDsp',index=False)
```


```python
#filenames
#thl2019_1776_avohilmo_17_20_icd10.csv.finreg_IDs
#thl2019_1776_avohilmo_icd10.csv.finreg_IDs

#thl2019_1776_avohilmo_17_20_icpc2.csv.finreg_IDs
#thl2019_1776_avohilmo_icpc2.csv.finreg_IDs

#thl2019_1776_avohilmo_17_20_jatkoh.csv.finreg_IDs
#thl2019_1776_avohilmo_jatkohoito.csv.finreg_IDs

#thl2019_1776_avohilmo_17_20_kotihoito.csv.finreg_IDs
#thl2019_1776_avohilmo_kotihoito.csv.finreg_IDs

#thl2019_1776_avohilmo_17_20_laake.csv.finreg_IDs (HAS DATES) v
#thl2019_1776_avohilmo_laake.csv.finreg_IDs

#thl2019_1776_avohilmo_17_20_lahete.csv.finreg_IDs (HAS DATES) v
#thl2019_1776_avohilmo_lahete.csv.finreg_IDs

#thl2019_1776_avohilmo_17_20_rokotus.csv.finreg_IDs (HAS DATES)
#thl2019_1776_avohilmo_rokotus.csv.finreg_IDs

#thl2019_1776_avohilmo_17_20_rokotussuoja.csv.finreg_IDs
#thl2019_1776_avohilmo_rokotussuoja.csv.finreg_IDs

#thl2019_1776_avohilmo_17_20_suu_toimp.csv.finreg_IDs
#thl2019_1776_avohilmo_suu_toimenpide.csv.finreg_IDs

#thl2019_1776_avohilmo_17_20_toimenpide.csv.finreg_IDs
#thl2019_1776_avohilmo_toimenpide.csv.finreg_IDs

```