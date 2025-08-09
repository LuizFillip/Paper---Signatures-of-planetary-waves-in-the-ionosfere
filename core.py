import PW as pw
import datetime as dt 
import matplotlib.pyplot as plt
import xarray as xr 
import base as b 
import numpy as np 
import pandas as pd

def plot_wavelet_subplot(
        ax, doy, period, power, sig95):

    cf = ax.contourf(
        doy, 
        period, 
        power, 
        levels = 30, 
        cmap = b.custom_cmap()
        )
     
    step = find_step(power, vmin = 0.0, n = 4)
    # step = 0.05
    ticks = np.arange(0, power.max(), step)
    b.colorbar(
            cf, 
            ax, 
            ticks = ticks, 
            label = 'PSD', 
            height = "100%", 
            width = "3%",
            orientation = "vertical", 
            anchor = (.05, 0., 1, 1), 
            color = 'k'
            )
    
   
    
    ax.contour(
        doy, period, 
        sig95, [-99, 1], 
        colors = 'k'
               )
    ax.set(
        yticks = np.arange(2, max(period), 2), 
        xticks = np.arange(min(doy), max(doy), 20),
        ylim = [2, max(period)]
           )
    
    # ax.text(
    #     0.4, 0.5, 'No EPBs', 
    #     color = 'w', 
    #     transform = ax.transAxes
    #     )
    
    for line in [265, 275]:
        ax.axvline(line, color = 'w', lw = 2)
    return 

   
def find_maximus(ds_total, years):
    res = [ds_total.power.sel(
        year=yr).max().item()
                for yr in years]

    return max(res)

  
def join_datasets(col, func, years, days, j1, freq = '15D'):
    
    datasets = []
    
    for num, year in enumerate(years):
       
        dn = dt.datetime(year, 1, 1) 
        df = func(dn, days)
        df = df.drop_duplicates(subset='doy')
        
        df['mean'] = df[col].rolling(freq).mean()
        
        df[col] = df[col] - df['mean']
        
        sst = df[col].values 
        doy = df['doy'].values 
        
        sig95, power, doy, period = pw.Wavelet(
            sst, doy, j1 = j1)
        
        ds = xr.Dataset(
            {
                'power': (['period', 'doy'], power),
                'sig95': (['period', 'doy'], sig95)
            },
            coords = {
                'period': period,
                'doy': doy,
                'start': ('year', [df.index[0]]),
                'end': ('year', [df.index[-1]])
            }
        )
   
        if 'year' not in ds.dims:
            
            ds = ds.expand_dims({'year': [year]})

        datasets.append(ds)
    
    return xr.concat(datasets, dim = 'year')

def find_step(vals, vmin = 0.0, n = 5, order = 2):
    
    arr = np.sort(vals.flatten())
    
    arr = arr[~np.isnan(arr)]
    
    interval_total = np.nanmax(arr) - vmin
 
    return round(interval_total / n, order)
    
def plot_sets(ax, power):
    s = pd.to_datetime(power['start'].values).date()
    e = pd.to_datetime(power['end'].values).date()
    
    ax.set(title = f'{s} - {e}', )
        
        


def plot_all_years_wavelet(
        func, 
        col,
        years, 
        j1 = 2.1, 
        days = 365,
        ncols = 2
        ):
    
    
    ds_total = join_datasets(
        col, func, years, days, j1)
    
    years = ds_total.year.values
    
    n = len(years)
   
    fig, axes = plt.subplots(
        nrows = n // 2, 
        ncols = ncols,
        figsize = (ncols * 9, (n // 2) * 4), 
        sharex = True, 
        sharey = True
        )
    
    plt.subplots_adjust(
        hspace = 0.2, 
        wspace = 0.2
        )
    
    for i, year in enumerate(years):
        
        if n > 1:
            ax = axes.flatten(order = 'F')[i]
        else:
            ax = axes
            
        power = ds_total.power.sel(year = year)        
        doy = ds_total.doy.values
        period = ds_total.period.values
        
        sig95 =  ds_total.sig95.sel(year = year)
        
        plot_wavelet_subplot(ax, doy, period, power, sig95)
        
        plot_sets(ax, power)
        
        middle = years[n // 2 - 1]
        
        if ((year == middle) | 
            (year == years[-1])):
            
            ax.set_xlabel('Day of year', 
                          fontsize = 30)
        
        if year <= middle:
          
            ax.set_ylabel('Periods (days)', 
                          fontsize = 30)
                
    # fig.suptitle(titles[col], y = 0.95, 
    #              fontsize = 30)
    
    plt.show()
    return fig 





