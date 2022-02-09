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

def frac_time_rain(mfp,mfn):
    mfpn=os.path.join(mfp,mfn)
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
    df['rain']=pd.to_numeric(df['rain'], errors='coerce')
    df['is_rain'] = [1 if x > 0 else 0 for x in df['rain']]
    df['raintime']=df['is_rain']*df['time_delta']
    rain_frac_time=df['raintime'].sum()/df['time_delta'].sum()    
    return(rain_frac_time)