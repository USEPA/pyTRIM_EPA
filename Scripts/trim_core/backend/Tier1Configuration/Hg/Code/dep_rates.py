# -*- coding: utf-8 -*-
"""
created on thu jul  8 15:39:50 2021
@author: 13963

reads and parse deposition rates file 
auto writes code to add deposition attributes to pseudo source compartments, specifically define_attributes_dep_rates.py

"""

import pandas as pd
import os
import re
from util_functions import * 

def define_deposition_rates(inputs):
    
    
    ifp=inputs['path_inputs']
    ifn=inputs['dep_rates_file']
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
            cname = re.sub('[^0-9a-za-z]+', '_', name)
            return(cname)
        return(name)  
    
    
    def clean_props(prop): # function to convert properties to pythonic syntax, 
        if '?' in prop: # change java if then else syntax to pythonic syntax
            cond=prop.split('?')[0].strip()
            v1=prop.split('?')[1].strip().split(':')[0].strip()
            v2=prop.split('?')[1].strip().split(':')[1].strip()
            prop= v1+' if ' +cond.replace('&&',' and ')+' else ' +v2
        prop=prop.replace('constants','self.constants')
        prop=prop.replace('containingscenario','self.containingscenario')
        prop=prop.replace('chemical','self')
        prop=prop.replace('ln','log')
        prop=prop.replace('<unset>','"<unset>"')
        return (prop)
    
    
    for line in dr_lines: # loop over lines 
        line=line.strip()        
        line_nc=line.split("//")[0] # line stripped of comment
        if line_nc[:12]=="pointsource:":
            ps=line_nc.split(":")[1].strip()
            ve=ps.replace(' for ','_')
            comp=ve.split('_')[0]+'_in_'+ve
        elif line_nc[:9]=="property:":   
            prop=line_nc.split(":")[1].strip()
        elif line_nc[:6]=="value:":   
            val=line_nc.split(":")[1].strip()
            chem=val.split("}")[0].strip().replace('{','')
            chem=clean_names(chem)
            dep=val.split("}")[1].strip()
            c=(ve,comp,prop,chem,dep)
            dr_tuples.append(c)        
    df_dr=pd.DataFrame(dr_tuples,columns=['volume element', 'compartment', 'property','chemical','surface deposition rate'])
    df_dr['chemical']=df_dr['chemical'].apply(clean_chem_names)    
    
    #### write script to add deposition rates as properties of pseudo compartments
    
    ofp=inputs['path_code']
    ofn=r'define_attributes_dep_rates.py'
    ofpn=os.path.join(ofp,ofn)
    
    with open(ofpn, 'w') as f:
        f.write('### note: this is an auto generated script' +'\n')        
        for i in range(len(df_dr)):
            obj=df_dr.loc[i,'compartment']
            f.write('try:'+'\n\t'+\
                    str(obj)+\
                   ".emission_rate['" +\
                   str(df_dr.loc[i,'chemical'])+\
                  "']="+\
                   str(df_dr.loc[i,'surface deposition rate'])+\
                   '*'+\
                   obj+\
                   ".parcel_area"+'\n'\
                   'except:'+'\n\t'+\
                   'pass')
            f.write('\n')            
            
    return(df_dr)