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
from numpy import array
from numpy import linspace
from datetime import *




def clean_chem_names(name): # function to replace certain special characters with underscore; leaves float values alone
    try:
        name=float(name) 
    except:
        pass
    if type(name)==str:
        # cname = 'chem_'+re.sub('[^0-9a-za-z]+', '_', name)
        cname='chem_'+re.sub(r'\W+', '_', name) ## changed for TCDD. check if affect other chems.
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


def recast_met_file(old_met): # simulation start date, end date, and num steps will also have to be arguments, eventually
    
    ts = linspace(0,int(365*50),int(365*50*24)) # time line in hours for 50 years, tstart and tend should be inputs. must match solve_ode interval.
    
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



def process_met(inputs): ## one time process met and return vectors (modified -- not wt averages)
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
    df2['ae']=pd.to_numeric(df2['allowexchange'], errors='coerce')

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
                

    del df['_merge']

            
    # process LF file

    mfpn=os.path.join(mfp,mfn_lf)
    df3=pd.read_csv(mfpn) 
    ## operations to drop faulty date data
    df3['dlist']=df3['##date'].str.split('/') # split date column into list
    df3=df3[df.dlist.str.len()==3] # drop rows that have less than three elements
    df3[['Month','Day','Year']] = df3['##date'].str.split("/",expand=True)
    df3['Month']=pd.to_numeric(df3['Month'], errors='coerce')    
    df3['Day']=pd.to_numeric(df3['Day'], errors='coerce')    
    df3['Year']=pd.to_numeric(df3['Year'], errors='coerce')   
    # df['Hour']=pd.to_numeric(df['hour'], errors='coerce')
    # df=df.loc[(df.Month<13) & (df.Day<32) & (df.Year<2100)&(df.Hour<25)] # drop faulty
    df3=df3.loc[(df3.Month<13) & (df3.Day<32) & (df3.Year<2100)] # drop faulty
    df3['lf']=pd.to_numeric(df3['litterfallrate'], errors='coerce')
    df3['DT']=list(pd.to_datetime(df3[['Year', 'Month', 'Day']],errors='coerce'))

    df=pd.merge_asof(df, df3[['DT','lf']], on='DT',direction='backward') # perform closest join in backwards direction
    
    df=recast_met_file(df) # recast metfile


    met_dict={}
    
    for k,v in metcol_dict.items():
        df['metcol']=pd.to_numeric(df[k], errors='coerce')
        met_dict['vector_'+k]=array(df['metcol'])

    met_dict['vector_allowexchange']=array(df['ae'])
    met_dict['vector_litterfallrate']=array(df['lf'])



    return(met_dict)
