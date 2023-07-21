#!/usr/bin/env python
# coding: utf-8

# # New files for 2020-2021 period

# In[ ]:


import pandas as pd
import numpy as np
import gc
import time
import datetime

# concatenates month files into year files, drops duplicates rearanges columns and deletes a redundant column ['TILASTOVUOSI']  with a single unique value denoting a year

results = np.zeros([1,3])
for n in ['2020','2021']: #['2020','2021']:
    zzz=0
    for m in range(1,13):
        ym = n+str(m).zfill(2)
        path = "/data/original_data/kela_purchase/81_522_2022_LAAKEOSTOT_"+ym+".csv.finreg_IDs"
        print(path)

        start_time = time.time()
        df = pd.read_csv(path,sep = ';')
        run_time = time.time()-start_time;print(run_time)


        a = df.shape[0]
        df.drop_duplicates(inplace=True)
        duplicates= str(a-df.shape[0])
        print(ym,duplicates)
        if zzz==0:
            df2 = df.copy()
        else:
            df2 = pd.concat([df2, df], ignore_index=True)
            
        
        results = np.concatenate([results,np.concatenate([[[ym]],[[duplicates]],[[a]]], axis = 1)]) # 2020 duplicates:18382, final size:54545942 / 2021 duplicates:10652, final size:57037054

 
        zzz = zzz+1
    df2.rename(columns={'ostopv': 'OSTOPV','kust_eur':'KUST_EUR','korv_eur':'KORV_EUR','kakorv_eur':'KAKORV_EUR','shp_nro':'SHP','tilastovuosi':'TILASTOVUOSI'}, inplace=True)
    del df2['TILASTOVUOSI']
    df2 = df2[['HETU','ATC','OSTOPV','PLKM','KUST_EUR','KORV_EUR','KAKORV_EUR','RPK','VNRO','LAJI','SAIR','RKPV','RGTNO','ASKU','SHP','ANJA']]

    
    w_path = "/data/processed_data/kela_purchase/81_522_2022_LAAKEOSTOT_"+n+".csv.finreg_IDsp"          
    df2.to_csv(w_path,index=False)


# # OLD files up to 2019 (inclusinve)

# In[ ]:


import pandas as pd
import numpy as np
import gc
import time
import datetime


# A loop to remove duplicates from all purchase files and to record number of duplicates by year
results = np.zeros([1,2])
for n in range(1995,2020):
    path = '/data/original_data/kela_purchase/175_522_2020_LAAKEOSTOT_'+str(n)+'.csv.finreg_IDs'
    start_time = time.time()
    df = pd.read_csv(path,sep = ';', encoding='latin-1', dtype={"RKPV": "string","VNRO":"string","SHP":"string","ASKU":"string","RGTNO":"string","SAIR":"string"})
    run_time = time.time()-start_time;print(run_time)


    a = df.shape[0]
    df.drop_duplicates(inplace=True)
    duplicates= str(a-df.shape[0])
    print(n,duplicates)
    
    df['RKPV'] = pd.to_datetime(df['RKPV'], errors='coerce',format='%y%m%d')
    
    results = np.concatenate([results,np.concatenate([[[n]],[[duplicates]]], axis = 1)])
    w_path = '/data/processed_data/kela_purchase/175_522_2020_LAAKEOSTOT_'+str(n)+'.csv.finreg_IDsp'
    df.to_csv(w_path,index=False)
