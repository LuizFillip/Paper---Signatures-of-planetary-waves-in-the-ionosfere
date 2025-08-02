import numpy as np 
import PlasmaBubbles as pb 
import pandas as pd 
import datetime as dt 
from astropy.timeseries import LombScargle
import matplotlib.pyplot as plt
import base as b 
import os 
import spectral as sp 


class Lomb_Scargle(object):

    def __init__(self, x, y, Tmax = 500):
    
        ls = LombScargle(
            x, y, 
            normalization='psd'
            )
        
        frequency, self.power = ls.autopower(
            minimum_frequency = 1/Tmax,
            maximum_frequency = 1/2, 
            samples_per_peak = 20
            )
        
        self.periods = 1 / frequency
        
        self.best_T = self.periods[
            np.argmax(self.power)
            ]
        
        self.x = x
        self.y = y
    
    @property 
    def result(self):
        return self.periods, self.power
    
    @property 
    def dtrend(self):
        
        fit = b.CurveFit(
            self.x, 
            self.y, 
            period = self.best_T
            )

        new_x, new_y = fit.residual
        
        return new_x, new_y
            


def iono_data(dn):
    
    infile = 'spectral/data/Fortaleza/'
    
    out = []
    for fn in os.listdir(infile):
        try:
            out.append(b.load(infile + fn))
        except:
            continue
        
    df = pd.concat(out)
    
    df = df.loc[df.index.hour == 22]
    
    dn = dt.datetime(2013, 9, 1) 
    
    df = pb.filter_doys(
        df, dn, days = 260).interpolate()
    
    df = pb.cummulative_doy(df)
    df = df[['foF2', 'hF', 'doy']].dropna()
    return df 


# col = 'hF'
fig, ax = plt.subplots(
    nrows = 2, 
    # sharex = True,
    dpi = 300,
    figsize = (14, 8)
    )

def winds_set(dn, days):
    df = b.load('cariri')
    
    df = df.loc[~(df['vnu_zonal'] < 0)]
    df = df.between_time('22:00', '23:00')
    
    df = df.resample('1D').mean()

    df = pb.filter_doys(
        df, dn, days = days).dropna()
    
    return pb.cummulative_doy(df).interpolate()

dn = dt.datetime(2013, 9, 1) 
days = 260

df = winds_set(dn, days)

y = df['vnu_zonal'].values
x = df['doy'].values


ls = Lomb_Scargle(x, y, Tmax =  25)
period, power = ls.result

ax[0].scatter(x, y)

wave = sp.wavelet_transform(y, x, j1 = 2.5) 

ax[1].contourf(
    wave.time, 
    wave.period, 
    wave.power, 
    levels = 50,
    cmap = 'jet'
    )