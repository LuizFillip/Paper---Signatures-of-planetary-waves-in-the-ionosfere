import datetime as dt 
import PlasmaBubbles as pb
import pandas as pd
import base as b 
import PW as pw
import matplotlib.pyplot as plt 
import numpy as np 


def epbs_start_time(dn, days):
     
    p = pb.BubblesPipe(
        'events_5', 
        drop_lim = 0.5, 
        storm = 'quiet'
        )
    
    ds = p.sel_type('sunset')
    
    df = ds.loc[(ds['lon'] == -50)]
       
    df = df[~df.index.duplicated(keep='first')]

    df = pw.filter_doys(df, dn, days = days)
    
    df = pw.reindex_data(df).interpolate()

    return df



def plot_desviation_from_mean(ax, df, col):
    # df[col] = df[col] - df[col].mean()
    freq = '15D'
    mean = df[[col, 'doy']].resample(freq).mean()
    std = df[[col, 'doy']].resample(freq).std()
        
    ax.errorbar(
        mean.doy, 
        mean[col], 
        yerr = std[col],
        linestyle = 'none',
        marker = 's', 
        markersize = 10,
        )
    
    df['std'] = df[col].rolling('5D').std()

    ax.errorbar(
        df['doy'], 
        df[col], 
        yerr = df['std'], 
        linestyle = 'none', 
        marker = 'o', 
        # alpha = 0.5,
        markersize = 5
        )
    
    df = df.interpolate()
    x = df['doy'].values
    y = df[col].values 
    fit = b.CurveFit(x, y, period = 180)
    
    
    xfit, yfit = fit.get_values
    ax.plot(xfit, yfit, lw = 2, color = 'r') 
    
    
    return fit
    


def plot_infos(df, ax, i):
    idx = df.index
    s = idx[0].date()
    e = idx[-1].date()
    l = b.chars()[i]
  
    ax.text(
        0.01, 0.8, 
        f'({l}) {s} - {e}', 
        transform = ax.transAxes
        )
    


def plot_residual(ax, fit):
    
    x, y = fit.residual
    ax.scatter(x, y)
    
    ax.set(ylim = [-1, 1]) 

def plot_ls(ax, x, y, Tmax = 300):
    
    y = y - np.mean(y)
    yfilt = b.filter_frequencies(
            y, 
            high_period = 20, 
            low_period = 2, 
            fs = 6, 
            order = 5
            )
    
    ls = pw.Lomb_Scargle(x, yfilt, Tmax = Tmax)
    
    periods, power = ls.result
    
    ax.plot(periods, power)
    
    ax.axhline(ls.best_T, lw = 2, color = 'r')
    # print(ls.best_T)
    ax.set(
        
           ylim = [0, max(power)])

def plot_time_start(years, days, col = 'start'):
    
    fig, ax = plt.subplots(
        dpi = 300, 
        nrows = len(years),
        ncols = 1,
        sharex = 'col',
        # sharey = True,
        figsize = (14, 16)
        )
    
    plt.subplots_adjust(hspace = 0.01)
    
    for i, year in enumerate(years):
        dn = dt.datetime(year, 9, 1) 
        
        
        df = epbs_start_time(dn, days)
        
        fit = plot_desviation_from_mean(ax[i], df, col)
        
        df = df.copy().dropna()
        y = df[col].values
        x = df['doy'].values 
        
        # plot_ls( ax[i, 1], x, y)

years = [2013, 2019]

days = 230
plot_time_start(years, days)