import base as b 
import PW as pw 
import datetime as dt 

def removing_noise(
        df, 
        col = 'vnu_zonal',
        factor = 1.4, 
        N = 60
        ):
    
    smooth_factor = N * 1
    
    df['avg'] =  b.smooth2(
        b.running(df[col], N),               
                           smooth_factor
        )
    
    df['std'] =  b.smooth2(b.running_std(df[col], N), 
        smooth_factor
        )

    cond = (df[col] > df['avg'] + df['std'] * factor)
       
    return df.loc[~(cond)]

def winds(dn, days, col = 'vnu_zonal'):

    df = b.load('cariri')
    
    df = pw.filter_doys(df, dn, days = days)
    
    df = df.between_time('21:00', '23:00')
    
    df = df.resample('3H').mean().dropna()
     
    if 'vnu' in col:
        df = df.loc[~(df[col] < 0 )].interpolate()
        df = df.loc[~((df[col] < 0) | 
                      (df[col] > 200))]
    
    if 'tn' in col:
        
        df = df.loc[~((df[col] > 1500) | 
                      (df[col] < 900))]


    df = pw.reindex_data(df).interpolate()
    
    return df[[col,'doy']]

