from astropy.timeseries import LombScargle
import numpy as np 
import base as b 

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