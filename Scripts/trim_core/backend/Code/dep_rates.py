# -*- coding: utf-8 -*-
"""
Created on Thu Jul  8 15:39:50 2021
@author: 13963

Reads and parse deposition rates file 
Auto writes code to add deposition attributes to pseudo source compartments, specifically define_attributes_dep_rates.py

"""

import pandas as pd
import os
import re

def define_deposition_rates(inputs):
    
    
    ifp=inputs['path_inputs']
    ifn=r'Foundries_PS_DepRates_Properties.txt'
    ifpn=os.path.join(ifp,ifn)
    
    dr_file=open(ifpn,'r') 
    dr_lines=dr_file.readlines()
    
    dr_tuples=[] # initialize list for storing point lines
    
    
    def clean_names(name): # function to replace certain special characters with underscore; leaves float values alone
        try:
            name=float(name) 
        except:
            pass
        if type(name)==str:
            cname = re.sub('[^0-9a-zA-Z]+', '_', name)
            return(cname)
        return(name)  
    
    
    def clean_props(prop): # function to convert properties to Pythonic syntax, 
        if '?' in prop: # change Java if then else syntax to Pythonic syntax
            cond=prop.split('?')[0].strip()
            v1=prop.split('?')[1].strip().split(':')[0].strip()
            v2=prop.split('?')[1].strip().split(':')[1].strip()
            prop= v1+' if ' +cond.replace('&&',' and ')+' else ' +v2
        prop=prop.replace('Constants','self.Constants')
        prop=prop.replace('containingScenario','self.containingScenario')
        prop=prop.replace('Chemical','self')
        prop=prop.replace('ln','log')
        prop=prop.replace('<Unset>','"<Unset>"')
        return (prop)
    
    
    for line in dr_lines: # loop over lines 
        line=line.strip()        
        line_nc=line.split("//")[0] # line stripped of comment
        if line_nc[:12]=="PointSource:":
            ps=line_nc.split(":")[1].strip()
            ve=ps.replace(' for ','_')
            comp=ve.split('_')[0]+'_in_'+ve
        elif line_nc[:9]=="Property:":   
            prop=line_nc.split(":")[1].strip()
        elif line_nc[:6]=="Value:":   
            val=line_nc.split(":")[1].strip()
            chem=val.split("}")[0].strip().replace('{','')
            chem=clean_names(chem)
            dep=val.split("}")[1].strip()
            c=(ve,comp,prop,chem,dep)
            dr_tuples.append(c)        
    df_dr=pd.DataFrame(dr_tuples,columns=['Volume Element', 'Compartment', 'Property','Chemical','Surface Deposition Rate'])
    
    
    #### WRITE SCRIPT TO ADD DEPOSITION RATES AS PROPERTIES OF PSEUDO COMPARTMENTS
    
    ofp=inputs['path_code']
    ofn=r'define_attributes_dep_rates.py'
    ofpn=os.path.join(ofp,ofn)
    
    with open(ofpn, 'w') as f:
        f.write('### Note: This is an auto generated script' +'\n')        
        for i in range(len(df_dr)):
            obj=df_dr.loc[i,'Compartment']
            f.write('try:'+'\n\t'+\
                    str(obj)+\
                   ".Emission_Rate['" +\
                   str(df_dr.loc[i,'Chemical'])+\
                  "']="+\
                   str(df_dr.loc[i,'Surface Deposition Rate'])+\
                   '*'+\
                   obj+\
                   ".Parcel_Area"+'\n'\
                   'except:'+'\n\t'+\
                   'pass')
            f.write('\n')            
            
    return(df_dr)