import matplotlib.pyplot as plt 
import numpy as np 
import base as b 
import PW as pw
import datetime as dt 


def plot_desviation_from_mean(
        ax, df, col, dtrend = False
        ):
    
    # df[col] = df[col] - df[col].mean()
    freq = '5D'
    # mean = df[[col, 'doy']].resample(freq).mean()
    # std = df[[col, 'doy']].resample(freq).std()
        
    # ax.errorbar(
    #     mean.doy, 
    #     mean[col], 
    #     yerr = std[col],
    #     linestyle = 'none',
    #     marker = 's', 
    #     markersize = 10,
    #     )
    if dtrend:
        df['mean'] = df[col].rolling(freq).mean()
        
        df[col] = df[col] - df['mean']
    
    df['std'] = df[col].rolling(freq).std()

    ax.errorbar(
        df['doy'], 
        df[col], 
        yerr = df['std'], 
        linestyle = 'none', 
        marker = 'o', 
        # alpha = 0.5,
        markersize = 5
        )
    
    
    return 
    


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
    



titles = {
    'start': 'EPBs start time (UT)', 
    'duration': 'EPBs night duration',
    'time': 'PRE time (UT)', 
    'vp': 'PRE magnitude', 
    'hF': 'h`F (km)', 
    'foF2': 'foF2', 
    'vnu_zonal': 'Zonal wind (m/s)', 
    'roti': 'Average ROTI (TEC/min)'
    }



def plot_column_data(ax, j, df, col, j1 = 2.2):
    
    doy = df['doy'].values
    
    sst = df[col].values 
    
    plot_desviation_from_mean(ax[0, j], df, col)
    
    ax[0, j].set(ylabel = titles[col])
    
    sig95, power, doy, period = pw.Wavelet(
        sst, doy, j1 = j1)
    
    pw.plot_wavelet_subplot(
        ax[-1, j], doy, period, power, sig95)
    
    ax[-1, j].set(
        xlabel = 'Day of year - 2013',
        ylabel = 'Period (days)', 
        xlim = [220, 320], 
        yticks = np.arange(2, 11, 1)
        )

def plot_start_time_and_roti():

    fig, ax = plt.subplots(
          figsize = (16, 10),
          nrows = 2,
          ncols = 2,
          sharex = True, 
          dpi = 300
          )
    
    
    plt.subplots_adjust(hspace = 0.05, wspace = 0.4)
    
    dn = dt.datetime(2013, 8, 1)
    days  = 120
     
    df = pw.epbs_start_time(dn, days )
    
    plot_column_data(ax, 0, df, col = 'start')
    
    df = pw.avg_of_roti(dn, days)
    
    plot_column_data(ax, 1, df, col = 'roti')


fig, ax = plt.subplots(
      figsize = (16, 10),
      nrows = 2,
      ncols = 2,
      sharex = True, 
      dpi = 300
      )

plt.subplots_adjust(hspace = 0.05, wspace = 0.4)

dn = dt.datetime(2013, 9, 11)
days  = 120

# col = 'time'
df =  pw.vertical_drift(dn, days)

plot_column_data(ax, 0, df, 'vp') 

col = 'hF'
df = pw.heights_frequency(dn, days, col)


plot_column_data(ax, 1, df, col) 
