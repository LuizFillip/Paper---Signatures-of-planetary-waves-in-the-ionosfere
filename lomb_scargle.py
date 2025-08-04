from astropy.timeseries import LombScargle
import numpy as np 
import base as b 

def phase_folded(ls, x, y, best_period):
    
    dy = np.full_like(y, 0.05) 
    phase = (x % best_period) / best_period
    sorted_indices = np.argsort(phase)
    phase_sorted = phase[sorted_indices]
    y_sorted = y[sorted_indices]
    
    # Modelo ajustado (curva suavizada)
    model = ls.model(x, 1 / best_period)
    
    amplitude = ls.model(x[sorted_indices], 1 / best_period)
    
    yerr = dy[sorted_indices]
    return phase_sorted, amplitude,  y_sorted, yerr



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
        
        self.fap_level = ls.false_alarm_level(0.05)
    
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
    
    
def plot_(ax, x, y, best_period):
    ax.set(
        ylim = [0, 0.8], 
        ylabel = 'PSD (normalized)', 
        xlabel = 'Periods (days)', 
        title = f'Best period: {round(best_period)} days'
        )
    
    inset_ax = ax.inset_axes([0.55, 0.55, 0.4, 0.4])

    phase_sorted, amplitude, y_sorted, yerr = phase_folded(
        ls, x, y, 
        best_period
        )
    inset_ax.errorbar(
        phase_sorted, y_sorted, 
        yerr=yerr, 
        fmt='ko', markersize=3)
    
    inset_ax.plot(phase_sorted, amplitude, 'b-')
    
    inset_ax.set(
        xlabel = 'phase', 
        ylabel = 'mag'
        )