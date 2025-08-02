import core as c
import pandas as pd
import datetime as dt 


def filter_storms(df):
    df.index = pd.to_datetime(df.index.date)
    df_source = c.geo_index(eyear = 2023)
    df['dst'] = df.index.map(df_source['dst'])
    df['kp'] =  df.index.map(df_source['kp'])
    return df.loc[df['kp'] <= 3] 

            
def reindex_data(df):
    idx = df.index
    full_index = pd.date_range(idx[0], idx[-1], freq='D')
    return df.reindex(full_index)


def filter_doys(df, dn, days = 260):
    
    delta = dt.timedelta(days = days)
    
    df = df.loc[
        (df.index >= dn) & 
        (df.index <= dn + delta)
        ]
    
    df['doy'] = df.index.day_of_year
    df['year'] = df.index.year

    offset = df['year'] -  df['year'].min()
    
    df['doy'] = df['doy'] + 365 * offset
    
    return df 
