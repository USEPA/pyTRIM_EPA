# -*- coding: utf-8 -*-
"""

To generate chemical concentration output file from previously generated chemical mass time series results and compartment volumes/mass matrices

Created on Thu Aug 25 08:56:43 2022

@author: 13963

"""

from numpy import nan,array
import pandas as pd

def compute_conc(nt,df_nt,vmu,df_vmu): # arguments are the chemical mass array (nt), mass dataframe

    df_vmu['Mass_to_Conc_Conv_Factor']=nan    
    index_list=list(df_vmu.index)
    for i in index_list: #loop over the rows of the compartment volume mass units dataframe
        if df_vmu.loc[i,'concentrationoutputfactor']==nan:
           pass
        else:
            if 'mass' in df_vmu.loc[i,'denominator']:
                df_vmu.loc[i,'Mass_to_Conc_Conv_Factor']=1/df_vmu.loc[i,'mass_kg']*df_vmu.loc[i,'concentrationoutputfactor']                
            if 'volume' in df_vmu.loc[i,'denominator']:
                    df_vmu.loc[i,'Mass_to_Conc_Conv_Factor']=1/df_vmu.loc[i,'volume_m3']*df_vmu.loc[i,'concentrationoutputfactor']                
            if 'volume_L' in df_vmu.loc[i,'denominator']: # need to convert volume from m3 to L for these compartments (surface water and groundwater)
                    df_vmu.loc[i,'Mass_to_Conc_Conv_Factor']=1/(df_vmu.loc[i,'volume_m3']*1000)*df_vmu.loc[i,'concentrationoutputfactor']                


    df_conc=pd.DataFrame()
    df_conc['time_in_days']=df_nt['time_in_days'] # add time column
    
    for i in index_list:
        conv_fact=df_vmu.loc[i,'Mass_to_Conc_Conv_Factor']
        units=df_vmu.loc[i,'concentrationoutputunits'] 
        # col_name=i+'_'+units
        col_name=i
        col_val=array(df_nt[i])*conv_fact
        df_conc[col_name]=col_val
        df_conc[col_name+'_units']=units    
                     
    return(df_conc)
    
    