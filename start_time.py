import datetime as dt 
import PlasmaBubbles as pb
import pandas as pd
import base as b 
import PW as pw



def extrapolate_backward(df, dn):
    
    new_index = pd.date_range(
        dn.date(), df.index[-1], freq = 'D'
        )
    
    df = df.reindex(new_index).interpolate(
        method ='linear', limit_direction ='backward')

    return df  

def epbs_start_time(
        dn, days, reindex = True):
     
    p = pb.BubblesPipe(
        'events_5', 
        drop_lim = 0.5, 
        storm = 'quiet'
        )
    
    ds = p.sel_type('sunset')
    
    df = ds.loc[(ds['lon'] == -50)]
       
    df = df[~df.index.duplicated(keep = 'first')]

    df = pw.filter_doys(df, dn, days = days)
    df = df.loc[~(df['start'] > 22.50)]
    df = df.loc[~(df['duration'] < 2)]
    if reindex:
        df = pw.reindex_data(df).interpolate(
            method = 'spline', 
            order = 5
            )
    
    return df 

def roti(year, col = '-50'):
    
    infile = f'E:\\database\\epbs\\longs\\{year}'
    
    df = b.load(infile)
    
    df = df.between_time('21:00', '23:00')
    
    ds = df.resample('1D').mean()
    
    ds = b.re_index(ds).interpolate()

    return ds.loc[ds.index.year == year, [col]]


def avg_of_roti(dn, days):
    
    df = roti(dn.year, col = '-50')
    
    df = pw.filter_storms(df)
    
    df = pw.filter_doys(df, dn, days = days)
    
    df.rename(columns = {'-50':'roti'}, 
              inplace = True)
    
    return df 


def test_epbs_start_time(dn, days):
        
    epbs_start_time( dn, days, reindex = True)