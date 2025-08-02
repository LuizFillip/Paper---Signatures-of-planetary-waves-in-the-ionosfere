import specral as sp
import numpy as np 

def custom_cmap(N=256):
    from matplotlib.colors import LinearSegmentedColormap

    colors = [
    (0.00, "#000000"),  # preto
    (0.10, "#0000ff"),  # azul
    (0.20, "#00bfff"),  # azul claro
    (0.35, "#00ffff"),  # ciano
    (0.50, "#00ff00"),  # verde
    (0.65, "#ffff00"),  # amarelo
    (0.80, "#ffa500"),  # laranja
    (0.95, "#ff0000"),  # vermelho
    (1.00, "#ffffff"),  
]
    return LinearSegmentedColormap.from_list(
        "custom_continuous", colors, N=N)


def plot_wavelet(ax, sst, time, j1 = 2.3):
    sst = sst - np.mean(sst)
    variance = np.std(sst, ddof = 1) ** 2
 
    if 0:
        variance = 1.0
        sst = sst / np.std(sst, ddof=1)
        
    n = len(sst)
    dt = time[1] - time[0]
    pad = 1  
    dj = 0.25  # this will do 4 sub-octaves per octave
    s0 = 2 * dt  # this says start at a scale of 6 months
    j1 = j1 / dj  # this says do 7 powers-of-two with dj sub-octaves each
    lag1 = 0.72  # lag-1 autocorrelation for red noise background

    mother = 'MORLET'
    
    # Wavelet transform:
    wave, period, scale, coi = sp.wavelet(sst, dt, pad, dj, s0, j1, mother)
    power = (np.abs(wave)) ** 2  # compute wavelet power spectrum

    # Significance levels:
    signif = sp.wave_signif(
        ([variance]), dt=dt, sigtest = 0, 
        scale=scale,
        lag1=lag1, 
        mother=mother)
    
    sig95 = signif[:, np.newaxis].dot(
        np.ones(n)[np.newaxis, :])
    sig95 = power / sig95  


    
    ax.contourf(time, period, power, 30, cmap = custom_cmap())
    
    ax.contour(
        time, period, 
        sig95, [-99, 1], 
        colors = 'k'
               )

    ax.set(
        ylim = [np.min(period), np.max(period)], 
        # yticks = np.arange(2, np.max(period) + 1, 1), 
        xlim = [250, 315], 
        xlabel = 'Doy', 
        ylabel = 'Periods (days)'
        )


def plot_reference_lines(ax):
    
    for line in [265, 280]:
        
        ax.axvline(line, color = 'w', lw = 2)

    ax.axhline(6, color = 'w', lw = 2)