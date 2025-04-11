# -*- coding: utf-8 -*-
"""
Created on Wed Jan 11 11:16:02 2023

@author: 13963
"""

import numpy as np
from datetime import *
import os

import pandas as pd


def recast_met_file(old_met): # simulation start date, end date, and num steps will also have to be arguments, eventually
    
    ts = np.linspace(0,int(365.25*50),int(365.25*50*24)) # time line in hours for 50 years, tstart and tend should be inputs
    
    dt=[] # initialize list for date time series
    for x in ts: # loop over element of time series array
        dt.append(datetime(1990, 1, 1,0,0,0) + timedelta(x)) # create date-time object by adding cumulative hours from starting time
    
    new_met=pd.DataFrame() # new df for met   
    new_met['Date']=dt # time series showing date time object
    new_met['Cumulative_Days']=ts # time series showing cumulative time in hours
    
    dt2=[] # initialize list for date series from old met file
    for x in list(old_met.date): # loop over date field in old met file
        dt2.append(datetime.strptime(x, '%m/%d/%Y').date()) # convert to date object
    
    hr=[] # initialize list for hour series from old met file
    for x in list(old_met.xhour) :# loop over hour field in old met file
        hr.append(time(x)) # convert to time object
    
    combined=[] #   initialize list for combined date hour series from old met file
    for x,y in zip(dt2,hr):
        combined.append(datetime.combine(x, y))
    
    cum_days=[] #   initialize list for cumulative hour series from old met file
    for x in combined:
        cum_days.append(abs(x-datetime(1990, 1, 1,0,0,0)).total_seconds() / (24*60*60)) # compute difference from starting time
    
    old_met['Cumulative_Days']=cum_days # add cumulative hour field to old met file
    
    new_met=pd.merge_asof(new_met, old_met, on='Cumulative_Days',direction='backward') # perform closest join in backwards direction

    return (new_met)   

ifp=r'C:\Users\13963\OneDrive - ICF\Documents\RTR\PyTRIM\Air_TS\input_files'
ifn=r'metdata_streamlined.csv'
ifpn=os.path.join(ifp,ifn)

old_met=pd.read_csv(ifpn)

new_met=recast_met_file(old_met)

ofpn=ifpn[:-4]+'_recast.csv'

new_met.to_csv(ofpn,index=False)