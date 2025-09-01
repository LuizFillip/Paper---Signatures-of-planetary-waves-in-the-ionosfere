import matplotlib.pyplot as plt
import numpy as np
import base as b
import PW as pw
import datetime as dt

b.sci_format(fontsize=25)

def plot_mean(ax, df, col, freq="5D"):

    mean = df[[col, "doy"]].resample(freq).mean()
    std = df[[col, "doy"]].resample(freq).std()

    ax.errorbar(
        mean.doy,
        mean[col],
        yerr=std[col],
        lw=2,
        marker="o",
        markersize=10,
        capsize=7,
    )

def plot_desviation_from_mean(ax, df, col, dtrend=False, freq="5D"):
    

    if dtrend:
        df["mean"] = df[col].rolling(freq).mean()

        df[col] = df[col] - df["mean"]

    df["std"] = df[col].rolling(freq).std()

    ax.errorbar(
        df["doy"],
        df[col],
        yerr=df["std"],
        linestyle="none",
        marker="o",
        alpha=0.5,
        markersize=7,
    )

    return


def plot_infos(df, ax, i):
    idx = df.index
    s = idx[0].date()
    e = idx[-1].date()
    l = b.chars()[i]

    ax.text(0.01, 0.9, f"({l}) {s} - {e}", transform=ax.transAxes)

    return None


titles = {
    "start": "EPBs start time (UT)",
    "duration": "EPBs night duration",
    "time": "PRE time (UT)",
    "vp": "PRE magnitude",
    "hF": "h`F (km)",
    "foF2": "foF2",
    "vnu_zonal": "Zonal wind (m/s)",
    "mean": "Average ROTI (TEC/min)",
}


def plot_column_data(axs, j, df, col, j1=2.2):

    if j == None:
        ax = axs[0]
        ax1 = axs[-1]
    else:
        ax1 = axs[-1, j]
        ax = axs[0, j]

    doy = df["doy"].values

    sst = df[col].values

    plot_desviation_from_mean(ax, df, col)

    # df = df.rename(columns = {col: 'roti'})
    ax.set(ylabel=titles[col])

    sig95, power, doy, period = pw.Wavelet(sst, doy, j1=j1)

    pw.plot_wavelet_subplot(ax1, doy, period, power, sig95)

    ax1.set(
        xlabel="Day of year",
        ylabel="Period (days)",
        xlim=[220, 320],
        yticks=np.arange(2, 11, 1),
    )

    # for line in [265, 280]:
    #     ax1.axvline(line, color="w", lw=3)

    return ax


def plot_start_time_and_roti(dn, days):

    fig, ax = plt.subplots(figsize=(16, 12), nrows=2, ncols=2, sharex=True, dpi=300)

    plt.subplots_adjust(hspace=0.05, wspace=0.4)

    df = pw.epbs_start_time(dn, days)

    ax2 = plot_column_data(ax, 0, df, col="start")

    ax2.set(ylim=[21, 23])
    df = pw.avg_of_roti(dn, days)

    ax2 = plot_column_data(ax, 1, df, col="roti")

    ax2.set(ylim=[0, 2])

    for i, axs in enumerate(ax.flat):
        l = b.chars()[i]
        if i == 3:
            c = "w"
        else:
            c = "k"
        axs.text(
            0.05, 0.85, f"({l})", 
            transform=axs.transAxes, color=c, fontsize=35)

    return None


def plot_single_spectral_and_ts(dn, days, col = 'roti'):

    fig, ax = plt.subplots(
        figsize=(12, 10), 
        nrows=2, sharex=True, dpi=300
        )

    plt.subplots_adjust(hspace=0.05, wspace=0.4)


    # col = "time"
    # df = pw.vertical_drift(dn, days)
    df = pw.epbs_start_time(dn, days)
    
    plot_column_data(ax, None, df, col)

    for i, axs in enumerate(ax.flat):
        l = b.chars()[i]
        if i == 3:
            c = "w"
        else:
            c = "k"
        axs.text(
            0.01, 0.85, f"({l})", 
            transform=axs.transAxes, color=c, fontsize=35)
        
    dne = (dn + dt.timedelta(days = days)).strftime('%Y-%m-%d')
    dns = dn.strftime('%Y-%m-%d')
    title = f'{dns} to {dne}'
    ax[0].set(title = title)
    return fig



# dn = dt.datetime(2019, 9, 1)
# days = 60
# fig = plot_single_spectral_and_ts(dn, days, col = 'mean')

