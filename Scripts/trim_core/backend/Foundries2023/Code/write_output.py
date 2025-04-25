# -*- coding: utf-8 -*-
"""
To write flatfile output

Created on Wed Nov 29 10:23:39 2023

@author: 13963
"""

import pandas as pd
import os


def split_write_files(df,sim_chems,path_output,file_name): # helper function to split and write time series files into excel workbook with multiple worksheets
    ofpn=os.path.join(path_output,file_name)
    writer = pd.ExcelWriter(ofpn, engine='xlsxwriter')
    for chem in sim_chems: # loop over sim chemicals
        prefix='chem_'+chem.replace(' ','_')+'_' # construct prefix
        dft=df[[df.columns[0]]+[x for x in list(df.columns) if prefix in x]] # keep time/year and cols with prefix
        dft.columns=[x.replace(prefix,'',) for x in list(dft.columns)]  # strip prefix       
        # Write each dataframe to a different worksheet.
        dft.to_excel(writer, sheet_name=chem,index=False)
    writer.close()
    return()
    
    
def write_output(df_tm,df_sm,df_nt,df_conc,dfc_avg,dfn_avg,inputs): # function called by main script
    path_output=inputs['path_output']
    ofpn=os.path.join(path_output,'Transfer_Matrix.xlsx')
    df_tm.to_excel(ofpn,index=True) ## write transition matrix
    ofpn=os.path.join(path_output,'Source_Matrix.xlsx')
    df_sm.to_excel(ofpn,index=True) ## write source matrix
    sim_chems=inputs['simulation_chemicals']
    hourly_flag=inputs['hourly_output']    
    split_write_files(dfn_avg, sim_chems, path_output, 'Annual_Average_Mass_in_g.xlsx') # write annual average mass in g
    split_write_files(dfc_avg, sim_chems, path_output, 'Annual_Average_Concentration.xlsx') # write annual concentration   
    if hourly_flag:
        # split_write_files(df_nt, sim_chems, path_output, 'Hourly_Mass_in_g.xlsx') # write hourly mass in g
        # split_write_files(df_conc, sim_chems, path_output, 'Hourly_Concentration.xlsx') # write hourly concentration 
        ofpn=os.path.join(path_output,'Hourly_Mass_in_g.csv')
        df_nt.to_csv(ofpn,index=False)
        ofpn=os.path.join(path_output,'Hourly_Concentration.csv')
        df_conc.to_csv(ofpn,index=False)
        
    return()     
    

    