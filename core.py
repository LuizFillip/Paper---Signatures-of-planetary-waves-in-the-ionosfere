import PW as pw
import datetime as dt 
import matplotlib.pyplot as plt
import xarray as xr 
import base as b 
import numpy as np 
import pandas as pd

def plot_wavelet_subplot(ax, doy, period, power, sig95):

    cf = ax.contourf(
        doy, 
        period, 
        power, 
        levels = 30, 
        cmap = b.custom_cmap()
        )
     
    step = find_step(power, vmin = 0.0, n = 4)
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
        
        
titles = {
    'start': 'EPBs start time', 
    'duration': 'EPBs night duration',
    'time': 'PRE time', 
    'vp': 'PRE magnitude', 
    'hF': 'h`F', 
    'foF2': 'foF2', 
    'vnu_zonal': 'Zonal wind', 
    'roti': 'Average ROTI'
    }

ylabel = {
    
    }

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
        
        if ((year == middle) | (year == years[-1])):
            
            ax.set_xlabel('Day of year', fontsize = 30)
        
        if year <= middle:
          
            ax.set_ylabel('Periods (days)', fontsize = 30)
                
    fig.suptitle(titles[col], y = 0.95, fontsize = 30)
    
    plt.show()
    return fig 


days = 365


col = 'hF'

# years = np.arange(2013, 2023)

dn = dt.datetime(2013, 1, 1) 
dn = dt.datetime(2013, 9, 15)
days  = 100
 
# col = 'time'
# df =  pw.vertical_drift(dn, days)

col = 'foF2'
df = pw.heights_frequency(dn, days, col)

col = 'vnu_zonal'
df = pw.winds(dn, days, col )

col = 'start'
df = pw.epbs_start_time(dn, days )



# fig = plot_all_years_wavelet(
#         func, 
#         col,
#         years, 
#         j1 = 2.3, #3.9, 
#         days = 365,
#         ncols = 1
#         )



def roti(year, col = '-50'):
    
    infile = f'E:\\database\\epbs\\longs\\{year}'
    
    df = b.load(infile)
    
    df = df.between_time('21:00', '23:00')
    
    ds = df.resample('1D').mean()
    
    ds = b.re_index(ds).interpolate()

    return ds.loc[ds.index.year == year,  [col]]

year = 2013
df = roti(year, col = '-50')

df['doy'] = df.index.day_of_year

df.rename(columns = {'-50':'roti'}, inplace = True)

col = 'epb'


fig, ax = plt.subplots(
      figsize = (12, 8),
      nrows = 2,
      sharex = True, 
      dpi = 300
      )


j1 = 2.2


doy = df['doy'].values

sst = df[col].values 

ax[0].plot(doy, sst)

ax[0].set(title = titles[col])

sig95, power, doy, period = pw.Wavelet(
    sst, doy, j1 = j1)

plot_wavelet_subplot(ax[-1], doy, period, power, sig95)

ax[-1].set(
    xlabel = 'Day of year',
    ylabel = 'Period (days)', 
    xlim = [220, 300]
    )