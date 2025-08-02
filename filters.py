import core as c
import pandas as pd

def filter_storms(df):
    df.index = pd.to_datetime(df.index.date)
    df_source = c.geo_index(eyear = 2023)
    df['dst'] = df.index.map(df_source['dst'])
    df['kp'] =  df.index.map(df_source['kp'])
    return df.loc[df['kp'] <= 3] 