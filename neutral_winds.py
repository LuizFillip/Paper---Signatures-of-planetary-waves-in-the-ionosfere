import base as b 

def removing_noise(
        df, 
        col = 'vnu_zonal',
        factor = 1.4, 
        N = 60
        ):
    
    smooth_factor = N * 1
    
    df['avg'] =  b.smooth2(b.running(df[col], N), smooth_factor
        )
    
    df['std'] =  b.smooth2(
        b.running_std(df[col], N), 
        smooth_factor
        )

    cond = (
        df[col] > df['avg'] + 
        df['std'] * factor
            )
    
    
    return df.loc[~(cond)]

def winds(dn, days, col = 'vnu_zonal'):

    df = b.load('cariri')
    
    df = pb.filter_doys(df, dn, days = days)
    
    df = df.between_time('21:00', '22:00')
    
    df = df.loc[~((df[col] < 0) | (df[col] > 200))]
    
    df = df.resample('3H').mean().dropna()
     
    df = df.loc[~(df[col] < 0 )].interpolate()
    
    df = removing_noise(df, factor = 1., N = 10)
    
    df = reindex_data(df).interpolate()
    
    return df[[ col, 'avg','doy']]