# -*- coding: utf-8 -*-
"""
created on mon jul 19 15:47:12 2021
@author: 13963

utility functions for all modules

"""
import re
import os
import pandas as pd
from numpy import timedelta64
from numpy import nan

def clean_chem_names(name): # function to replace certain special characters with underscore; leaves float values alone
    try:
        name=float(name) 
    except:
        pass
    if type(name)==str:
        cname = 'chem_'+re.sub('[^0-9a-za-z]+', '_', name)
        return(cname)
    return(name)  
    
def ternary2python(xpr):
    question_mark = xpr.find("?")
    colon = xpr.find(":", question_mark)

    # if no (or no more) if conditions return the expression
    if (question_mark == -1) or (colon == -1):
        return xpr

    # extract outer if condition and expressions (True & False)
    condition = xpr[0:question_mark].replace("&&", "and").replace("||", "or").strip()
    expressions = xpr[(question_mark + 1):xpr.__len__()].strip()

    True_expression = ""
    False_expression = ""

    # while looking in pairs, find the location where the colon occurs before the question mark
    question_mark = expressions.find("?")
    colon = expressions.find(":")
    while ((question_mark != -1) and (colon != -1)) and (question_mark < colon):
        question_mark = expressions.find("?", question_mark + 1)
        colon = expressions.find(":", colon + 1)

    # extract True and False expressions
    True_expression = f'{expressions[0:colon].strip()}'
    False_expression = f'{expressions[(colon + 1):expressions.__len__()].strip()}'

    return f'{ternary2python(True_expression)} if {condition} else {ternary2python(False_expression)}'


def is_number(s): # checks if string is number
    try:
        float(s)
        return True
    except ValueError:
        try:
            int(s)
            return True
        except ValueError:
            return False
        
def clean_names(name): # function to replace certain special characters with underscore; leaves float values alone
    try:
        name=float(name) 
    except:
        pass
    if type(name)==str:
        cname = re.sub('[^0-9a-za-z]+', '_', name)
        cname=cname.strip('_')
        return(cname)            
    return(name)     


def process_met(inputs): ## one time process all met weighted averages
    mfp=inputs['path_inputs']    
    mfn_met=inputs['met_file']
    mfn_ae=inputs['allowexchange_file']
    mfn_lf=inputs['litterfall_file']

    # first process met file
    mfpn=os.path.join(mfp,mfn_met)
    df=pd.read_csv(mfpn) 
    ## operations to drop faulty date data
    df['dlist']=df['date'].str.split('/') # split date column into list
    df=df[df.dlist.str.len()==3] # drop rows that have less than three elements
    df[['Month','Day','Year']] = df.date.str.split("/",expand=True)
    df['Month']=pd.to_numeric(df['Month'], errors='coerce')    
    df['Day']=pd.to_numeric(df['Day'], errors='coerce')    
    df['Year']=pd.to_numeric(df['Year'], errors='coerce')   
    df['Hour']=pd.to_numeric(df['xhour'], errors='coerce')
    df=df.loc[(df.Month<13) & (df.Day<32) & (df.Year<2100)&(df.Hour<25)] # drop faulty

    metcol_dict={'rain':(0,1),'airtemperature':(200,373),'horizontalwindspeed':(0,100),'winddirection':(-360,360),'mixingheight':(0,1000),'isday':(0,1),'cumulativerain':(0,1.6)} # k, v represent name and min-max
    for k,v in metcol_dict.items():
        df['metcol']=pd.to_numeric(df[k], errors='coerce')
        df=df[(df['metcol']<=v[1])&(df['metcol']>=v[0])] # keep rows within min max bounds


    df['DT']=list(pd.to_datetime(df[['Year', 'Month', 'Day','Hour']],errors='coerce'))
    df['date_delta'] = (df['DT'] - df['DT'].min())  / timedelta64(1,'D')
    df['time_delta']=df['date_delta'].diff()
    df['time_delta']=df['time_delta'].shift(-1) # shift up the column 1 so that applicability of met condition is aligned to duration

    # clean up non sequential dates. slow 

    df['DT_Check']=df.DT>=(df.DT.shift())
    df=df[df['DT_Check']]
    # df=df[(df['time_delta']<0.05)&(df['time_delta']>0)]# assume all observations valid for an hour since this is an hourly met file. eliminate overinfluential observations. not sure if needed but checking.
    # df=df[df['time_delta']>0]# assume all observations valid for an hour since this is an hourly met file. eliminate overinfluential observations. not sure if needed but checking.
    # df=df[(df['time_delta']<1)&(df['time_delta']>0)]# assume all observations valid for an hour since this is an hourly met file. eliminate overinfluential observations. not sure if needed but checking.
    

   ### need to clean up messy met file to get reasonable averages. This shouldnt be required with a quality met file.             

    met_dict={}
    
    for k,v in metcol_dict.items():
        df['metcol']=pd.to_numeric(df[k], errors='coerce')
        df['prod']=df['metcol']*df['time_delta']
        wt_ave=df['prod'].sum()/df['time_delta'].sum()    
        met_dict['wt_av_'+k]=wt_ave
    df['rain']=pd.to_numeric(df['rain'], errors='coerce')
    df['is_rain'] = [1 if x > 0 else 0 for x in df['rain']]
    df['raintime']=df['is_rain']*df['time_delta']
    rain_frac_time=df['raintime'].sum()/df['time_delta'].sum()    
    met_dict['frac_time_rain']=rain_frac_time
    # met_dict['wt_av_rain']=rain_frac_time # overwrite wt_av_rain with rain_frac_time (superior method, i think)


    # process AE file ## has unusal data column header -- not interfered with original data. Ignored hour resolution. 
    
    mfpn=os.path.join(mfp,mfn_ae)
    df2=pd.read_csv(mfpn) 
    ## operations to drop faulty date data
    df2['dlist']=df2['##date'].str.split('/') # split date column into list
    df2=df2[df2.dlist.str.len()==3] # drop rows that have less than three elements
    df2[['Month','Day','Year']] = df2['##date'].str.split("/",expand=True)
    df2['Month']=pd.to_numeric(df2['Month'], errors='coerce')    
    df2['Day']=pd.to_numeric(df2['Day'], errors='coerce')    
    df2['Year']=pd.to_numeric(df2['Year'], errors='coerce')   
    df2=df2.loc[(df2.Month<13) & (df2.Day<32) & (df2.Year<2100)] # drop faulty

    df2['DT']=list(pd.to_datetime(df2[['Year', 'Month', 'Day']],errors='coerce'))
    df2['date_delta'] = (df2['DT'] - df2['DT'].min())  / timedelta64(1,'D')
    df2['time_delta']=df2['date_delta'].diff()
    df2['time_delta']=df2['time_delta'].shift(-1) # shift up the column 1 so that applicability of met condition is aligned to duration

    df2['ae']=pd.to_numeric(df2['allowexchange'], errors='coerce')
    df2['prod']=df2['ae']*df2['time_delta']
    wt_ave=df2['prod'].sum()/df2['time_delta'].sum()    
    met_dict['wt_av_allowexchange']=wt_ave

    df=df.merge(df2[['DT','ae']],how='left',on='DT',indicator=True) # merge in AE
    
    first_ind=df.loc[df['_merge']=='both'].index[0]# index first date in AE file
    if first_ind!=0: # if the first value in the ae file is greater than the first date in the met file assume the opposite condition is true
        first_ae_val=df.loc[first_ind,'ae'] # first ae value
        if first_ae_val==1:
            df.loc[0,'ae']=0
        else:
            df.loc[0,'ae']=1
        
    df.ae.fillna(value=pd.np.nan, inplace=True) # fill None values with nan
    
    df['ae'].fillna(method='ffill', inplace=True) # fill nan values with previous non nan value

    df['exch_no_rain']=df['ae']*(1-df['is_rain'])
    df['exch_rain']=df['ae']*df['is_rain']
    df['exchnoraintime']=df['exch_no_rain']*df['time_delta']
    df['exchraintime']=df['exch_rain']*df['time_delta']
    exch_no_rain_frac_time=df['exchnoraintime'].sum()/df['time_delta'].sum()    
    exch_rain_frac_time=df['exchraintime'].sum()/df['time_delta'].sum()    

    met_dict['frac_time_exchange_no_rain']=exch_no_rain_frac_time
    met_dict['frac_time_exchange_rain']=exch_rain_frac_time
                
    ### Compute interaction between isday and allow exchange. 
    df=df
    df['isday']=pd.to_numeric(df['isday'], errors='coerce')
    df=df.loc[(df.isday==1) | (df.isday==0)] # keep only valid isday data
    df['ae_isday']=df['ae']*df.isday
    df['aeisdaytime']=df['ae_isday']*df['time_delta']    
    exch_day_frac_time=df['aeisdaytime'].sum()/df['time_delta'].sum()    
    met_dict['frac_time_exchange_day']=exch_day_frac_time      

    df['ae_notday']=df['ae']*(1-df.isday)
    df['aenotdaytime']=df['ae_notday']*df['time_delta']    
    exch_not_day_frac_time=df['aenotdaytime'].sum()/df['time_delta'].sum()    
    met_dict['frac_time_exchange_not_day']=exch_not_day_frac_time      

            
    # process LF file

    mfpn=os.path.join(mfp,mfn_lf)
    df=pd.read_csv(mfpn) 
    ## operations to drop faulty date data
    df['dlist']=df['##date'].str.split('/') # split date column into list
    df=df[df.dlist.str.len()==3] # drop rows that have less than three elements
    df[['Month','Day','Year']] = df['##date'].str.split("/",expand=True)
    df['Month']=pd.to_numeric(df['Month'], errors='coerce')    
    df['Day']=pd.to_numeric(df['Day'], errors='coerce')    
    df['Year']=pd.to_numeric(df['Year'], errors='coerce')   
    # df['Hour']=pd.to_numeric(df['hour'], errors='coerce')
    # df=df.loc[(df.Month<13) & (df.Day<32) & (df.Year<2100)&(df.Hour<25)] # drop faulty
    df=df.loc[(df.Month<13) & (df.Day<32) & (df.Year<2100)] # drop faulty

    df['DT']=list(pd.to_datetime(df[['Year', 'Month', 'Day']],errors='coerce'))
    # df['DT']=list(pd.to_datetime(df[['Year', 'Month', 'Day','Hour']],errors='coerce'))
    df['date_delta'] = (df['DT'] - df['DT'].min())  / timedelta64(1,'D')
    df['time_delta']=df['date_delta'].diff()
    df['time_delta']=df['time_delta'].shift(-1) # shift up the column 1 so that applicability of met condition is aligned to duration

    df['lf']=pd.to_numeric(df['litterfallrate'], errors='coerce')
    df['prod']=df['lf']*df['time_delta']
    wt_ave=df['prod'].sum()/df['time_delta'].sum()    
    met_dict['wt_av_litterfallrate']=wt_ave
    # met_dict['wt_av_litterfallrate']=0.0745 # fix
    # met_dict['wt_av_allowexchange']=5/12
    

    return(met_dict)
