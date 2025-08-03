import numpy as np 
import PlasmaBubbles as pb 
import pandas as pd 
import datetime as dt 
import os 
import matplotlib.pyplot as plt
import base as b 
import spectral as sp


def reindex_data(df):
    idx = df.index
    full_index = pd.date_range(idx[0], idx[-1], freq='D')
    
    return df.reindex(full_index)

def iono_data(dn, days):
    
    infile = 'spectral/data/Fortaleza/'
    
    out = []
    for fn in os.listdir(infile):
        try:
            out.append(b.load(infile + fn))
        except:
            continue
        
    df = pd.concat(out)
    
    df = df.loc[df.index.hour == 22]
    
    df = pb.filter_doys(
        df, dn, days = days).interpolate()
    
    df = pb.cummulative_doy(df)
    df = df[['foF2', 'hF', 'doy']].dropna()
    return df 

def bubbles_set(dn, days):
    
    p = pb.BubblesPipe(
        'events_5', 
        drop_lim = 0.3, 
        storm = None
        )
    
    ds = p.sel_type('sunset')
    
    df = ds.loc[(ds['lon'] == -50)]
       
    df = df[~df.index.duplicated(keep='first')]

    df = pb.filter_doys(
        df, dn, days = days).interpolate()
    
    return pb.cummulative_doy(df).interpolate(
        method = 'spline', 
        order = 5
        )




def plot_timeseries_and_wavelet(
        ax, 
        ax1, 
        df, 
        col, 
        j1 = 2.3
        ):
    
    x = df['doy'].values
    y = df[col].values 

    ax.plot(x, y)
    
    wave = sp.wavelet_transform(y, x, j1 = j1) 
    
    ax1.contourf(
        wave.time, 
        wave.period, 
        wave.power, 
        levels = 50,
        cmap = 'jet'
        )

dn = dt.datetime(2013, 9, 1) 
days = 260


fig, ax = plt.subplots(
    nrows = 2, 
    ncols = 2,
    sharex = True,
    dpi = 300,
    figsize = (14, 8)
    )
df = bubbles_set(dn, days)

plot_timeseries_and_wavelet(
    ax[0, 0], ax[1, 0], df, 
    'start', j1 = 2.3
    )

df = iono_data(dn, days)


plot_timeseries_and_wavelet(
    ax[0, 1], 
    ax[1, 1], df, 
    'hF', j1 = 2.3
    )

df 