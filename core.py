import PW as pw
import datetime as dt 
import matplotlib.pyplot as plt
import xarray as xr 
import base as b 
import numpy as np 
import pandas as pd

def plot_all_years(df, col):
    
    sst = df[col].values 
    time = df['doy'].values
    
    b.sci_format(fontsize = 18)


    fig, axs = plt.subplots(
        dpi = 300,
        nrows = 3,
        ncols = 3,
        sharex = True, 
        sharey = True,
        figsize = (16, 12)
        )


    plt.subplots_adjust(wspace = 0.02)

    idx = df.index
    s = idx[0].date()
    e = idx[-1].date()
    
    pw.plot_wavelet(ax, sst, time, j1 = j1)
    
    ax.set(
        yticks = np.arange(2, 18, 2),
        ylabel = '', 
        xlabel = '', 
        title = f'{s} - {e}'
        )
    
    for line in [300, 340]:
        
        ax.axvline(
            line, 
            color = 'white', 
            lw = 3
            )
    for ln in [3, 6, 9]:
        ax.axhline(ln, color = 'white', 
                   linestyle = '--')
        
    axs[2, 0].set(
        xlabel = 'Doy', 
        ylabel = 'Period (days)'
        )
    
    
    fig.suptitle(
        'EPBs start time', 
        y = 1.03, 
        fontsize = 30
        )
    
   
def find_maximus(ds_total):
    res = [ds_total.power.sel(
        year=yr).max().item()
                for yr in years]

    return max(res)

 
# df =

# df = 
        
def join_datasets(col, func, years, days, j1):
    
    datasets = []
    
    for num, year in enumerate(years):
       
        dn = dt.datetime(year, 8, 1) 
        df = func(dn, days)
        df = df.drop_duplicates(subset='doy')
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
    
    return xr.concat(datasets, dim='year')

def find_step(vals, vmin = 0.0, n = 5, order = 2):
    
    arr = np.sort(vals.flatten())
    
    arr = arr[~np.isnan(arr)]
    
    vmax = np.nanmax(arr)
    
    intervalo_total = vmax - vmin
    passo = intervalo_total / n
    
    return round(passo, order)
    
   

days = 620

j1 = 2.1

col = 'foF2'

titles = {
    'start': 'EPBs start time', 
    'duration': 'EPBs night duration',
    'time': 'PRE time', 
    'vp': 'PRE magnitude', 
    'hF': 'h`F', 
    'foF2': 'foF2'
    }

years = [2013, 2019]

# func = pw.epbs_start_time
# func =  pw.vertical_drift

func = pw.heights_frequency

ds_total = join_datasets(col, func, years, days, j1)


years = ds_total.year.values

fig, axes = plt.subplots(
    nrows = 2, 
    figsize = (12, 8), 
    sharex = True, 
    sharey = True
    )

plt.subplots_adjust(hspace = 0.01)


for i, year in enumerate(years):
    ax = axes.flat[i]
    
    power = ds_total.power.sel(year = year)
    doy = ds_total.doy.values
    period = ds_total.period.values
    
    s = pd.to_datetime(power['start'].values).date()
    e = pd.to_datetime(power['end'].values).date()
    
    
    sig95 =  ds_total.sig95.sel(year = year)
    
    cf = ax.contourf(
        doy, 
        period, 
        power, 
        levels = 30, 
        cmap = b.custom_cmap(), 
        extend = 'both',
        )
    vals = power.values
   
    step = find_step(vals, vmin = 0.0, n = 5)
    ticks = np.arange(0, power.max() + step, step)
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
    
    ax.set(title = f'{s} - {e}')
    
    power_rel = power / sig95
    
    ax.contour(
        doy, period, 
        sig95, [-99, 1], 
        colors = 'k'
               )
    ax.set(yticks = np.arange(2, 12, 1), 
           ylabel = 'Periods (day)', 
           xticks = np.arange(250, 850, 50), 
           xlim = [250, 850],
           ylim = [2, 10]
           )

    for line in range(3):
        ax.axvline(
            365 * line,
            lw = 3,
            color = 'w', linestyle = '--'
            )
        
    # for row in [3, 6, 9]:
        
    #     ax.axhline(row, color = 'w', lw = 1)
        
axes[-1].set(xlabel = 'Day of year')
fig.suptitle(titles[col])

plt.tight_layout()
plt.show()

