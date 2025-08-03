
import PW as pw
import pandas as pd 
import datetime as dt 
import base as b 
import os 

def heights_frequency(
        dn, days, 
        site = 'SaoLuis', 
        reindex = True
        ):
    
    infile = f'spectral/data/{site}/'
    
    out = []
    for fn in os.listdir(infile):
        try:
            out.append(b.load(infile + fn))
        except:
            continue
        
    df = pd.concat(out)
    
    df = df.loc[df.index.hour == 22]
    
    df = pw.filter_storms(df)
    
    df = pw.filter_doys(df, dn, days = days)
    
    if reindex:
        df = pw.reindex_data(df).interpolate()

    columns = ['foF2', 'hF', 'hmF2', 'doy']
    
    return df[columns].dropna()

def fix_drift(df):
    df['time'] = df.index.to_series(
        ).apply(b.dn2float)
    
    df.rename(
        columns = {'vzp': 'vp'}, 
        inplace = True)
    
    df.index = pd.to_datetime(df.index.date)  

    return df 

def vertical_drift(
        dn, 
        days, 
        reindex = True, 
        site = 'saa'
        ):
    path = f'digisonde/data/drift/PRE/{site}/'
  
    out = []
    
    for fn in os.listdir(path):
        
        df = b.load(path + fn)
        
        if 'vzp' in df.columns:
            out.append(fix_drift(df))
        else:
            out.append(df)
        
    df = pd.concat(out).sort_index()
   
    df = pw.filter_storms(df)
    df = pw.filter_doys(df, dn, days = days)
    df = df[~df.index.duplicated(keep='first')]
    
    if reindex:
        df = pw.reindex_data(df).interpolate()
        
    return df 
    
    # return df 

def test_doy_diff(df):
    assert (df['doy'].diff().dropna() == 1).all()
    
    
def test_ionospheric_par():
    
    dn = dt.datetime(2013, 8, 1) 

    days = 230
     
    df = heights_frequency(dn, days)
    
    
    
    
    # print(check_diff)
    return df 

dn = dt.datetime(2013, 8, 1) 

days = 620



import matplotlib.pyplot as plt 

fig, ax = plt.subplots(
    nrows = 2, 
    ncols = 2,
    dpi = 300, 
    sharex = True,
    figsize = (12, 10)
    )

df =  heights_frequency(
        dn, days, site = 'SaoLuis', 
        reindex = False)

freq = '10D'
for i, col in enumerate(['hF', 'foF2']):
    
    df['std'] = df[col].rolling(freq).std()
       
    ax[i, 0].errorbar(
        df.index,
        df[col], 
        yerr = df['std'],
        linestyle = 'none', 
        marker = 'o', 
        ) 

ds = vertical_drift(dn, days, reindex = False)

for j, col in enumerate(['vp', 'time']):
    mean = ds[col].resample(freq).mean()
    std = ds[col].resample(freq).std()
    
    ax[j, 1].errobar(
        mean.index,
        mean, 
        yerr = std, 
        marker = 'o', 
        markersise = 10
        )
    ds['std'] = ds[col].rolling(freq).std()
    
    ax[j, 1].errorbar(
        ds.index,
        ds[col], 
        yerr = ds['std'],
        linestyle = 'none', 
        marker = 'o', 
        ) 
    
    b.format_time_axes()
    
    
