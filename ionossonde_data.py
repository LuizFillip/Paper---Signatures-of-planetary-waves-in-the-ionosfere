import matplotlib.pyplot as plt 

import PW as pw
import pandas as pd 
import datetime as dt 
import base as b 
import os 


def dtrend(df, col, threshold = 200, freq = '15D'):
    
    df = df.loc[~(df[col] < threshold)]
    
    df = pw.reindex_data(df).interpolate()
    
    df['avg'] = df[col].rolling(freq).mean()
    df[col] = df[col] - df['avg']
    
    return df

def heights_frequency(
        dn, days, 
        col,
        site = 'saa', 
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
    # print(df)
    # df = df.resample('1D').mean()
    df = df.loc[df.index.hour == 22]
    df = df[~df.index.duplicated(keep='first')]
    df = pw.filter_storms(df)
    
    df = pw.filter_doys(df, dn, days = days)
    
    if reindex:
        df = pw.reindex_data(df).interpolate(
            # method = 'spline', 
            # order = 5
            )

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

def test_doy_diff(df):
    assert (df['doy'].diff().dropna() == 1).all()
    

def plot_long_term_series(dn, days, site = 'saa'):
    
    fig, ax = plt.subplots(
        nrows = 2, 
        ncols = 2,
        dpi = 300, 
        sharex = True,
        figsize = (16, 8)
        )
      
    titles = {
        'fza': 'Fortaleza',
        'saa': 'São Luís'
        }
    plt.subplots_adjust(hspace = 0.02)
    df =  heights_frequency(
            dn, days, 
            site = site, 
            reindex = False
            )
    
    freq = '15D'
    color = '#0C5DA5'
    labels = ['h`F (km)', 'foF2 (MHz)']
    limits = [[100, 700], [0, 16]]
    
    
    for i, col in enumerate(['hF', 'foF2']):
           
        df['std'] = df[col].rolling(freq).std()
           
        ax[i, 0].errorbar(
            df.index,
            df[col], 
            color = color,
            yerr = df['std'],
            linestyle = 'none', 
            marker = 'o', 
            alpha = 0.5
            ) 
        
        mean = df[col].resample(freq).mean()
        std = df[col].resample(freq).std()
        
        ax[i, 0].errorbar(
            mean.index,
            mean, 
            yerr = std, 
            marker = 'o', 
            markersize = 10, 
            color = 'k'
            )
        
        ax[i, 0].set(
            ylabel = labels[i], 
            ylim = limits[i],
            xlim = [df.index[0], df.index[-1]]
            )
        
    b.format_month_axes(
        ax[1, 1], 
        month_locator = 3, 
        pad = 60
        )
        
    ds = vertical_drift(
        dn, days, 
        reindex = False, 
        site = site
        )
    labels = ['PRE magnitude (m/s)', 'PRE time (UT)']
    limits = [[0, 90], [20, 24]]
    
    
    for j, col in enumerate(['vp', 'time']):
        
        ds['std'] = ds[col].rolling(freq).std()
        
        ax[j, 1].errorbar(
            ds.index,
            ds[col], 
            yerr = ds['std'],
            linestyle = 'none', 
            marker = 'o', 
            markersize = 7,
            alpha = 0.5, 
            color = color
            ) 
            
        mean = ds[col].resample(freq).mean()
        std = ds[col].resample(freq).std()
        
        ax[j, 1].errorbar(
            mean.index,
            mean, 
            yerr = std,
            color = 'k',
            marker = 'o', 
            markersize = 10
            )
        ax[j, 1].set(
            ylabel = labels[j],
            ylim = limits[j],
            xlim = [df.index[0], df.index[-1]]
            )
        
    b.format_month_axes(
        ax[1, 0], 
        month_locator = 3, 
        pad = 60, 
        )
        
        
    fig.suptitle(f'Ionossonde {titles[site]} parameters')
    
    
dn = dt.datetime(2013, 9, 11) 

days = 620

# plot_long_term_series(dn, days)

