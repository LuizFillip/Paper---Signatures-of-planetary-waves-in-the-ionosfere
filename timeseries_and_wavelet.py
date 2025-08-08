import matplotlib.pyplot as plt 
import numpy as np 

def plot_desviation_from_mean(ax, df, col):
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
    df['mean'] = df[col].rolling(freq).mean()
    
    df[col] = df[col] - df['mean']
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
    
    df = df.dropna()
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
        ylim = [0, max(power)]
        )

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
        dn = dt.datetime(year, 8, 1) 
        
        
        df = epbs_start_time(
            dn, days, 
            reindex = False
            )
        
        plot_desviation_from_mean(ax[i], df, col)
        
        df = df.copy().dropna()
        y = df[col].values
        x = df['doy'].values 