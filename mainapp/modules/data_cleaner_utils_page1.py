import pandas as pd
import numpy as np

def process_file(uploaded_file):
    df = pd.read_csv(uploaded_file, skiprows=1, names=range(100), engine='python')
    df.dropna(axis='columns', how='all', inplace=True)
    df.columns = df.iloc[0]
    df_phonenum = df[['PhoneNo']]
    df_response = df.loc[:, 'UserKeyPress':]
    df_results = pd.concat([df_phonenum, df_response], axis='columns')
    
    total_calls = len(df_results)
    phonenum_recycle = df_results.dropna(subset=['UserKeyPress'])
    phonenum_list = phonenum_recycle[['PhoneNo']]
    
    df_complete = df_results.dropna(axis='index')
    total_pickup = len(df_complete)

    df_complete.columns = np.arange(len(df_complete.columns))
    df_complete['Set'] = 'IVR'
    df_complete = df_complete.loc[:, :'Set']
    df_complete = df_complete.loc[(df_complete.iloc[:, 2].str.len() == 10)]

    return df_complete, phonenum_list, total_calls, total_pickup

