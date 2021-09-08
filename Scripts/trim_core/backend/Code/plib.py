# -*- coding: utf-8 -*-
"""
created on mon apr 12 21:46:07 2021
@author: 13963

parses pseudo source library objects text file and auto writes code to define pseudo source algorithm classes, specifically define_ps_algs.py

"""

import pandas as pd
import os
import re

def process_pseudo_library(inputs):

    ifp=inputs['path_inputs']
    ifn=inputs['pseudo_library_file']    
    ifpn=os.path.join(ifp,ifn)
    
    plib_file=open(ifpn,'r') 
    plib_lines=plib_file.readlines()
    
    
    #### read algorithhms
    
    alg_tuples=[] # initialize list for storing point lines
    alg_flag=False # initialize copy condition
    prop_flag=False # initialize copy condition
    val_flag=False # initialize copy condition
    
    
    for line in plib_lines: # loop over lines
        line_nc=line.strip()     # strip space and new line    
        line_nc=line_nc.split("//")[0] # line stripped of comment
        ptype=line_nc.split(":")[0].strip() # if line has a :, get text to left
        if ptype=="algorithm": # get algorithm name (assumed to be on single line)
            alg_flag=True
            alg_name=line_nc.split(":")[1].strip()
#            print ('*******************************************')
#            print (alg_name)
            continue
        if alg_flag==True and ptype=="property": # get property name (assumed to be on single line) 
            prop_flag=True
            prop_name=line_nc.split(":")[1].strip()        
            # print (prop_name)
            continue
        if alg_flag==True and prop_flag==True and ptype=="value": # get value name (not assumed to be on single line)
            val_flag=True
            val_name=line_nc.split(":")[1:]
            val_name=[x.strip() for x in val_name]
            val_name=':'.join(val_name)   
            continue        
            # print (val_name) 
        if alg_flag==True and prop_flag==True and val_flag==True and (':' not in line_nc): # get remainder of value ( not assumed to be on single line)
            val_name=val_name+line_nc  # join multiline values
            # print (val_name) 
            continue
        if alg_flag==True and prop_flag==True and val_flag==True and (ptype=='property'or ptype=='description' or line[:10]=="algorithm:"): # condition to determine when value reading is over
            r=(alg_name,prop_name,val_name)
#            print (r)
            alg_tuples.append(r)
            prop_flag=False # reinitialize copy condition
            val_flag=False # reinitialize copy condition
            prop_name=""; val_name=""; 
            continue
        if alg_flag==True and (ptype=='pointsource'or ptype=='ptype'or ptype=='compartment'):
            alg_flag=False
    df_psalgs=pd.DataFrame(alg_tuples,columns=['algorithm','property','value']) # convert to DataFrame
    
    ofpn=os.path.join(ifp,"pseudoalgs.csv")
    df_psalgs.to_csv(ofpn,index=False)
    
    
    #### read point sources
    
    ps_tuples=[] # initialize list for storing point lines
    ps_flag=False # initialize copy condition
    prop_flag=False # initialize copy condition
    val_flag=False # initialize copy condition
    
    
    for line in plib_lines: # loop over lines
        line_nc=line.strip()     # strip space and new line    
        line_nc=line_nc.split("//")[0] # line stripped of comment
        ptype=line_nc.split(":")[0].strip() # if line has a :, get text to left
        if ptype=="pointsource": # get algorithm name (assumed to be on single line)
            ps_flag=True
            ps_name=line_nc.split(":")[1].strip()
#            print ('*******************************************')
#            print (ps_name)
            continue
        if ps_flag==True and ptype=="property": # get property name (assumed to be on single line) 
            prop_flag=True
            prop_name=line_nc.split(":")[1].strip()        
            # print (prop_name)
            continue
        if ps_flag==True and prop_flag==True and ptype=="value": # get value name (assumed to be on single line)
            val_flag=True
            val_name=line_nc.split(":")[1].strip()
            r=(ps_name,prop_name,val_name)
#            print (r)
            ps_tuples.append(r)        
            continue        
    df_ps=pd.DataFrame(ps_tuples,columns=['pointsource','property','value'])
    
    
    #### read ptypes -- not perfect -- order is different across 6 ptypes so script below doesnt grab all descriptions. may not be necessary because this is basically variable declaration.
    
    pt_tuples=[] # initialize list for storing point lines
    
    pt_flag=False # initialize copy condition
    desc_flag=False # initialize copy condition
    dt_flag=False
    units_flag=False # initialize copy condition
    pt_name='';desc_name='';dt_name='';unit_name=''; dv_name="";
    
    for line in plib_lines: # loop over lines
        line_nc=line.strip()     # strip space and new line    
        line_nc=line_nc.split("//")[0] # line stripped of comment
        ptype=line_nc.split(":")[0].strip() # if line has a :, get text to left
        if ptype=="ptype" or ptype=="ptype": # get algorithm name (assumed to be on single line)
            pt_flag=True
            pt_name=line_nc.split(":")[1].strip()
#            print ('*******************************************')
#            print (pt_name)
            continue
        if pt_flag==True and ptype=="description": # get property name (assumed not to be on single line) 
            desc_flag=True
            desc_name=line_nc.split(":")[1].strip()        
            # print (prop_name)
            continue
        if pt_flag==True and desc_flag==True and (':' not in line_nc): # get remainder of value ( not assumed to be on single line)
            desc_name=desc_name+line_nc  # join multiline values
            continue
        if pt_flag==True and ptype=='datatype':
            desc_flag=False
            dt_name=line_nc.split(":")[1].strip()
            continue
        if pt_flag==True and ptype=='defaultvalue':
            dv_name=line_nc.split(":")[1].strip()
            continue
        if pt_flag==True and ptype=='units':
            dt_flag=False
            unit_name=line_nc.split(":")[1].strip()
            r=(pt_name,desc_name,dt_name,dv_name,unit_name)
            pt_tuples.append(r)
            units_flag=False
            pt_flag=False
            pt_name='';desc_name='';dt_name='';unit_name=''; dv_name="";
            continue
            
    df_pt=pd.DataFrame(pt_tuples)
    
    
    
    ############ write python script to define pseudo algorithm classes 
    
    
    ofp=inputs['path_code']
    ofn=r'define_ps_algs.py'
    ofpn=os.path.join(ofp,ofn)
    
    algs=df_psalgs["algorithm"].tolist()
    
    
    
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
        prop=prop.replace('[','')
        prop=prop.replace(']','')
    
        if '?' in prop: # change java if then else syntax to pythonic syntax
            cond=prop.split('?')[0].strip()
            v1=prop.split('?')[1].strip().split(':')[0].strip()
            v2=prop.split('?')[1].strip().split(':')[1].strip()
            prop= v1+' if ' +cond.replace('&&',' and ')+' else ' +v2
        prop=prop.replace('constants','self.constants')
        prop=prop.replace('containingscenario','self.containingscenario')
        prop=prop.replace('receivingcompartment','self.receivingcompartment')
        prop=prop.replace('sendingcompartment','self.sendingcompartment')
        prop=prop.replace('algorithm.','self.')
        if 'thelink.interfacialarea' in prop: # replace thelink interfacial area custom function with python function
            prop=prop.replace('thelink.interfacialarea','check_neighbor(self.sendingcompartment,self.receivingcompartment).is_neighbor()[1]')           
        if 'thelink.fractionspecificcompartmentdiet' in prop: # replace thelink.fractionspecificcompartmentdiet with 1. i believe this okay but check ug.
            prop=prop.replace('thelink.fractionspecificcompartmentdiet','1')          
        return (prop)
    
    
    grouped_alg = df_psalgs.groupby("algorithm")
    
    
    
    with open(ofpn, 'w') as f:  
        f.write('### note: this is an auto generated script' +'\n')                
        f.write('from numpy import nan' + '\n\n')
        for index,group in enumerate(grouped_alg.groups):
            if "surface water" not in group: # temp
                continue
#            print (group)
#            print(grouped_alg.get_group(group))
    
            alg_name=clean_names(group)
            alg_props=list(grouped_alg.get_group(group)['property'].unique())
            try:
                tf=grouped_alg.get_group(group).loc[grouped_alg.get_group(group)['property']=='transferfactor']['value'].values[0]#.replace('sendingcompartment','self.sendingcompartment').replace('receivingcompartment','self.receivingcompartment')
            except:
                tf="nan"
            tf=clean_props(tf)
    
                
            f.write('class '+str(alg_name)+':'+'\n' +\
                    '\t'+\
                    'def __init__(self, constants,containingscenario,currentchemical,sendingcompartment, receivingcompartment,dict_inputs):\n\t\t'+\
                    'self.name='+"'"+group+"'"+'\n\t\t'+\
                    'self.constants=constants\n\t\t'+\
                    'self.containingscenario=containingscenario\n\t\t'+\
                    'self.currentchemical=currentchemical\n\t\t'+\
                    'self.sendingcompartment=sendingcompartment\n\t\t'+\
                    'self.receivingcompartment=receivingcompartment\n\t\t'+\
                    'self.doestransformchemical= "False"\n\t\t'+\
                    'try: \n\t\t\t'
                    'self.transferfactor='+ tf +'\n\t\t'\
                    'except: \n\t\t\t'       
                    'self.transferfactor="tf computation error"')     
            
            residual_props=set(alg_props)-set(['category','chemicalcategory','doestransformchemical','doestransportchemical','enabled','isdefaultforcategory','mate','receivingchemicalname','receivingcompartmentcategory','sendingcompartmentcategory','sendingchemicalname','transferfactor'])
            for prop in residual_props:
                prop_val=grouped_alg.get_group(group).loc[grouped_alg.get_group(group)['property']==prop]['value'].values[0] #property value
                prop_val=clean_props(prop_val)
                if prop=='compartmentrelationship':
                    f.write('\n\t\t'
                            'self.'+prop+'='+"'"+prop_val+"'")                
                else:
                    f.write('\n\t\t'
                            'self.'+prop+'='+prop_val)                
            f.write('\n\n')    
            
    return(df_psalgs,df_ps,df_pt)
    
    
if __name__ == '__main__':
    df_psalgs,df_ps,df_pt=process_pseudo_library(inputs)
