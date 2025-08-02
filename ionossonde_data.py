import numpy as np 
import PlasmaBubbles as pb 
import pandas as pd 
import datetime as dt 
import matplotlib.pyplot as plt
import base as b 
import os 

def heights_frequency(dn, days):
    
    infile = 'spectral/data/SaoLuis/'
    
    out = []
    for fn in os.listdir(infile):
        try:
            out.append(b.load(infile + fn))
        except:
            continue
        
    df = pd.concat(out)
    
    df = df.loc[df.index.hour == 22]
    
    df = pb.filter_doys(
        df, dn, days = days).interpolate()
    
    df = pb.cummulative_doy(df)
    df.index = pd.to_datetime(df.index.date)
    df_source = c.geo_index(eyear = 2023)
    df['dst'] = df.index.map(df_source['dst'])
    df['kp'] =  df.index.map(df_source['kp'])
    df = df.loc[df['kp'] <= 3] 
    
    
    columns = ['foF2', 'hF', 'hmF2', 'doy']
    return df[columns].dropna()