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

