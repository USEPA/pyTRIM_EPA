# -*- coding: utf-8 -*-
"""
created on mon jul 19 15:47:12 2021
@author: 13963

utility functions for all modules

"""
import re

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

import os
import pandas as pd
from numpy import timedelta64

# def frac_time_rain(mfp,mfn):
#     mfpn=os.path.join(mfp,mfn)
#     df=pd.read_csv(mfpn) 
#     ## operations to drop faulty date data
#     df['dlist']=df['date'].str.split('/') # split date column into list
#     df=df[df.dlist.str.len()==3] # drop rows that have less than three elements
#     df[['Month','Day','Year']] = df.date.str.split("/",expand=True)
#     df['Month']=pd.to_numeric(df['Month'], errors='coerce')    
#     df['Day']=pd.to_numeric(df['Day'], errors='coerce')    
#     df['Year']=pd.to_numeric(df['Year'], errors='coerce')   
#     df['Hour']=pd.to_numeric(df['xhour'], errors='coerce')
#     df=df.loc[(df.Month<13) & (df.Day<32) & (df.Year<2100)&(df.Hour<25)] # drop faulty
#     df['DT']=list(pd.to_datetime(df[['Year', 'Month', 'Day','Hour']],errors='coerce'))
#     df['date_delta'] = (df['DT'] - df['DT'].min())  / timedelta64(1,'D')
#     df['time_delta']=df['date_delta'].diff()
#     df['rain']=pd.to_numeric(df['rain'], errors='coerce')
#     df['is_rain'] = [1 if x > 0 else 0 for x in df['rain']]
#     df['raintime']=df['is_rain']*df['time_delta']
#     rain_frac_time=df['raintime'].sum()/df['time_delta'].sum()    
#     return(rain_frac_time)


# def get_met_wt_ave(mfp,mfn,metcol):
#     mfpn=os.path.join(mfp,mfn)
#     df=pd.read_csv(mfpn) 
#     ## operations to drop faulty date data
#     df['dlist']=df['date'].str.split('/') # split date column into list
#     df=df[df.dlist.str.len()==3] # drop rows that have less than three elements
#     df[['Month','Day','Year']] = df.date.str.split("/",expand=True)
#     df['Month']=pd.to_numeric(df['Month'], errors='coerce')    
#     df['Day']=pd.to_numeric(df['Day'], errors='coerce')    
#     df['Year']=pd.to_numeric(df['Year'], errors='coerce')   
#     df['Hour']=pd.to_numeric(df['xhour'], errors='coerce')
#     df=df.loc[(df.Month<13) & (df.Day<32) & (df.Year<2100)&(df.Hour<25)] # drop faulty
#     df['DT']=list(pd.to_datetime(df[['Year', 'Month', 'Day','Hour']],errors='coerce'))
#     df['date_delta'] = (df['DT'] - df['DT'].min())  / timedelta64(1,'D')
#     df['time_delta']=df['date_delta'].diff()
#     df[metcol]=pd.to_numeric(df[metcol], errors='coerce')
#     df['prod']=df[metcol]*df['time_delta']
#     wt_ave=df['prod'].sum()/df['time_delta'].sum()    
#     return(wt_ave)


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
    df['DT']=list(pd.to_datetime(df[['Year', 'Month', 'Day','Hour']],errors='coerce'))
    df['date_delta'] = (df['DT'] - df['DT'].min())  / timedelta64(1,'D')
    df['time_delta']=df['date_delta'].diff()

    # clean up non sequential dates. slow 

    df['DT_Check']=df.DT>=(df.DT.shift())
    df=df[df['DT_Check']]
    

   ### need to clean up messy met file to get reasonable averages. This shouldnt be required with a quality met file.             

    met_dict={}
    metcol_dict={'rain':(0,1),'airtemperature':(200,373),'horizontalwindspeed':(0,12),'winddirection':(0,360),'mixingheight':(0,1000),'isday':(0,1),'cumulativerain':(0,1.6)} # k, v represent name and min-max
    
    for k,v in metcol_dict.items():
        df2=df
        df2['metcol']=pd.to_numeric(df[k], errors='coerce')
        df2=df2[(df2['metcol']<=v[1])&(df2['metcol']>=v[0])] # keep rows within min max bounds
        df2['prod']=df2['metcol']*df2['time_delta']
        wt_ave=df2['prod'].sum()/df2['time_delta'].sum()    
        met_dict['wt_av_'+k]=wt_ave
    df['rain']=pd.to_numeric(df['rain'], errors='coerce')
    df['is_rain'] = [1 if x > 0 else 0 for x in df['rain']]
    df['raintime']=df['is_rain']*df['time_delta']
    rain_frac_time=df['raintime'].sum()/df['time_delta'].sum()    
    met_dict['frac_time_rain']=rain_frac_time

    # process AE file ## has unusal data column header -- not interfered with original data. Ignored hour resolution. 
    
    mfpn=os.path.join(mfp,mfn_ae)
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

    df['ae']=pd.to_numeric(df['allowexchange'], errors='coerce')
    df['prod']=df['ae']*df['time_delta']
    wt_ave=df['prod'].sum()/df['time_delta'].sum()    
    met_dict['wt_av_allowexchange']=wt_ave

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

    df['lf']=pd.to_numeric(df['litterfallrate'], errors='coerce')
    df['prod']=df['lf']*df['time_delta']
    wt_ave=df['prod'].sum()/df['time_delta'].sum()    
    met_dict['wt_av_litterfallrate']=wt_ave
    

    return(met_dict)
