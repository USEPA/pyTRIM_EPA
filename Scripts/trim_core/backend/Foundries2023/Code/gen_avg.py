# -*- coding: utf-8 -*-
"""
To generate annual average mass and concentration output

Created on Wed Nov 29 10:23:39 2023

@author: 13963
"""

import pandas as pd

def gen_avg(df_nt,df_conc,inputs):
    start_date,end_date=inputs['simulation_start_date'],inputs['simulation_end_date'] # get simulation start and end dates
    start_date = pd.to_datetime(start_date, format='%d/%m/%Y')    #convert the start_date and end_date to datetime objects
    end_date = pd.to_datetime(end_date, format='%d/%m/%Y')    #convert the start_date and end_date to datetime objects
    df_nt.iloc[:,0] = pd.to_datetime(df_nt.iloc[:,0], origin=start_date, unit='d')    #convert the first col (time in d) to datetime objects
    df_conc.iloc[:,0] = pd.to_datetime(df_conc.iloc[:,0], origin=start_date, unit='d')    #convert the first col (time in d) to datetime objects
    df_nt['year'] = df_nt.iloc[:,0].dt.year   # create year column
    df_conc['year'] = df_conc.iloc[:,0].dt.year  # create year column
    #group the data by year and calculate the annual averages
    dfn_avg = df_nt.groupby('year').mean().reset_index() 
    dfn_avg=dfn_avg.head(len(dfn_avg)-1)# drop last line (just one day)
    dfc_avg = df_conc.groupby('year').mean().reset_index() 
    dfc_avg=dfc_avg.head(len(dfc_avg)-1)# drop last line (just one day)
    return(dfn_avg,dfc_avg)


