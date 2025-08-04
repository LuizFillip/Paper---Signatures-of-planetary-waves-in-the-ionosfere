import PW as pw
import datetime as dt 
import matplotlib.pyplot as plt 
import base as b 

freq = '15D'
col = 'start'

delta = dt.timedelta(days = 0)
dn = dt.datetime(2013, 1, 1) + delta

df = pw.epbs_start_time(dn, days = 50, reindex = False)

df['mean'] = df[col].rolling(freq).mean()

# df[col] = df[col] - df['mean']

fig, ax = plt.subplots(
    nrows = 2, 
    # ncols = 2,
    dpi = 300, 
    # sharex = True,
    figsize = (16, 8)
    )

df = df.dropna()
color = '#0C5DA5'
df['std'] = df[col].rolling(freq).std()

x = df['doy'].values
y = df[col].values
ax[0].scatter(x, y) 

ls = pw.Lomb_Scargle(x, y, Tmax = 20)

periods, power = ls.result

ax[1].plot(periods, power )

best_T = ls.best_T 
fit = b.CurveFit(x, y, period = 16)

new_x, new_y = fit.get_values

ax[0].plot(new_x, new_y)




