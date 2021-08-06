# -*- coding: utf-8 -*-
"""
Created on Mon Apr 12 21:46:07 2021
@author: 13963

Parses pseudo source library objects text file and auto writes code to define pseudo source algorithm classes, specifically define_ps_algs.py

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
    
    
    #### Read Algorithhms
    
    alg_tuples=[] # initialize list for storing point lines
    Alg_Flag=False # initialize copy condition
    Prop_Flag=False # initialize copy condition
    Val_Flag=False # initialize copy condition
    
    
    for line in plib_lines: # loop over lines
        line_nc=line.strip()     # strip space and new line    
        line_nc=line_nc.split("//")[0] # line stripped of comment
        ptype=line_nc.split(":")[0].strip() # if line has a :, get text to left
        if ptype=="Algorithm": # get algorithm name (assumed to be on single line)
            Alg_Flag=True
            alg_name=line_nc.split(":")[1].strip()
#            print ('*******************************************')
#            print (alg_name)
            continue
        if Alg_Flag==True and ptype=="Property": # get property name (assumed to be on single line) 
            Prop_Flag=True
            prop_name=line_nc.split(":")[1].strip()        
            # print (prop_name)
            continue
        if Alg_Flag==True and Prop_Flag==True and ptype=="Value": # get value name (NOT assumed to be on single line)
            Val_Flag=True
            val_name=line_nc.split(":")[1:]
            val_name=[x.strip() for x in val_name]
            val_name=':'.join(val_name)   
            continue        
            # print (val_name) 
        if Alg_Flag==True and Prop_Flag==True and Val_Flag==True and (':' not in line_nc): # get remainder of value ( NOT assumed to be on single line)
            val_name=val_name+line_nc  # join multiline values
            # print (val_name) 
            continue
        if Alg_Flag==True and Prop_Flag==True and Val_Flag==True and (ptype=='Property'or ptype=='Description' or line[:10]=="Algorithm:"): # condition to determine when value reading is over
            r=(alg_name,prop_name,val_name)
#            print (r)
            alg_tuples.append(r)
            Prop_Flag=False # reinitialize copy condition
            Val_Flag=False # reinitialize copy condition
            prop_name=""; val_name=""; 
            continue
        if Alg_Flag==True and (ptype=='PointSource'or ptype=='PType'or ptype=='Compartment'):
            Alg_Flag=False
    df_psalgs=pd.DataFrame(alg_tuples,columns=['Algorithm','Property','Value']) # convert to dataframe
    
    ofpn=os.path.join(ifp,"PseudoAlgs.csv")
    df_psalgs.to_csv(ofpn,index=False)
    
    
    #### Read Point Sources
    
    ps_tuples=[] # initialize list for storing point lines
    PS_Flag=False # initialize copy condition
    Prop_Flag=False # initialize copy condition
    Val_Flag=False # initialize copy condition
    
    
    for line in plib_lines: # loop over lines
        line_nc=line.strip()     # strip space and new line    
        line_nc=line_nc.split("//")[0] # line stripped of comment
        ptype=line_nc.split(":")[0].strip() # if line has a :, get text to left
        if ptype=="PointSource": # get algorithm name (assumed to be on single line)
            PS_Flag=True
            ps_name=line_nc.split(":")[1].strip()
#            print ('*******************************************')
#            print (ps_name)
            continue
        if PS_Flag==True and ptype=="Property": # get property name (assumed to be on single line) 
            Prop_Flag=True
            prop_name=line_nc.split(":")[1].strip()        
            # print (prop_name)
            continue
        if PS_Flag==True and Prop_Flag==True and ptype=="Value": # get value name (assumed to be on single line)
            Val_Flag=True
            val_name=line_nc.split(":")[1].strip()
            r=(ps_name,prop_name,val_name)
#            print (r)
            ps_tuples.append(r)        
            continue        
    df_ps=pd.DataFrame(ps_tuples,columns=['PointSource','Property','Value'])
    
    
    #### Read Ptypes -- Not perfect -- order is different across 6 ptypes so script below doesnt grab all descriptions. May not be necessary because this is basically variable declaration.
    
    pt_tuples=[] # initialize list for storing point lines
    
    PT_Flag=False # initialize copy condition
    Desc_Flag=False # initialize copy condition
    DT_Flag=False
    Units_Flag=False # initialize copy condition
    pt_name='';desc_name='';dt_name='';unit_name=''; dv_name="";
    
    for line in plib_lines: # loop over lines
        line_nc=line.strip()     # strip space and new line    
        line_nc=line_nc.split("//")[0] # line stripped of comment
        ptype=line_nc.split(":")[0].strip() # if line has a :, get text to left
        if ptype=="Ptype" or ptype=="PType": # get algorithm name (assumed to be on single line)
            PT_Flag=True
            pt_name=line_nc.split(":")[1].strip()
#            print ('*******************************************')
#            print (pt_name)
            continue
        if PT_Flag==True and ptype=="Description": # get property name (assumed NOT to be on single line) 
            Desc_Flag=True
            desc_name=line_nc.split(":")[1].strip()        
            # print (prop_name)
            continue
        if PT_Flag==True and Desc_Flag==True and (':' not in line_nc): # get remainder of value ( NOT assumed to be on single line)
            desc_name=desc_name+line_nc  # join multiline values
            continue
        if PT_Flag==True and ptype=='DataType':
            Desc_Flag=False
            dt_name=line_nc.split(":")[1].strip()
            continue
        if PT_Flag==True and ptype=='DefaultValue':
            dv_name=line_nc.split(":")[1].strip()
            continue
        if PT_Flag==True and ptype=='Units':
            DT_Flag=False
            unit_name=line_nc.split(":")[1].strip()
            r=(pt_name,desc_name,dt_name,dv_name,unit_name)
            pt_tuples.append(r)
            Units_Flag=False
            PT_Flag=False
            pt_name='';desc_name='';dt_name='';unit_name=''; dv_name="";
            continue
            
    df_pt=pd.DataFrame(pt_tuples)
    
    
    
    ############ WRITE PYTHON SCRIPT TO DEFINE PSEUDO ALGORITHM CLASSES 
    
    
    ofp=inputs['path_code']
    ofn=r'define_ps_algs.py'
    ofpn=os.path.join(ofp,ofn)
    
    algs=df_psalgs["Algorithm"].tolist()
    
    
    
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
        prop=prop.replace('[','')
        prop=prop.replace(']','')
    
        if '?' in prop: # change Java if then else syntax to Pythonic syntax
            cond=prop.split('?')[0].strip()
            v1=prop.split('?')[1].strip().split(':')[0].strip()
            v2=prop.split('?')[1].strip().split(':')[1].strip()
            prop= v1+' if ' +cond.replace('&&',' and ')+' else ' +v2
        prop=prop.replace('Constants','self.Constants')
        prop=prop.replace('containingScenario','self.containingScenario')
        prop=prop.replace('ReceivingCompartment','self.ReceivingCompartment')
        prop=prop.replace('SendingCompartment','self.SendingCompartment')
        prop=prop.replace('Algorithm.','self.')
        if 'TheLink.InterfacialArea' in prop: # replace TheLink interfacial area custom function with Python function
            prop=prop.replace('TheLink.InterfacialArea','check_neighbor(self.SendingCompartment,self.ReceivingCompartment).is_neighbor()[1]')           
        if 'TheLink.FractionSpecificcompartmentDiet' in prop: # replace TheLink.FractionSpecificcompartmentDiet with 1. I believe this okay but check UG.
            prop=prop.replace('TheLink.FractionSpecificcompartmentDiet','1')          
        return (prop)
    
    
    grouped_alg = df_psalgs.groupby("Algorithm")
    
    
    
    with open(ofpn, 'w') as f:  
        f.write('### Note: This is an auto generated script' +'\n')                
        f.write('from numpy import nan' + '\n\n')
        for index,group in enumerate(grouped_alg.groups):
            if "Surface water" not in group: # temp
                continue
#            print (group)
#            print(grouped_alg.get_group(group))
    
            alg_name=clean_names(group)
            alg_props=list(grouped_alg.get_group(group)['Property'].unique())
            try:
                tf=grouped_alg.get_group(group).loc[grouped_alg.get_group(group)['Property']=='transferFactor']['Value'].values[0]#.replace('SendingCompartment','self.SendingCompartment').replace('ReceivingCompartment','self.ReceivingCompartment')
            except:
                tf="nan"
            tf=clean_props(tf)
    
                
            f.write('class '+str(alg_name)+':'+'\n' +\
                    '\t'+\
                    'def __init__(self, Constants,containingScenario,currentChemical,SendingCompartment, ReceivingCompartment):\n\t\t'+\
                    'self.Name='+"'"+group+"'"+'\n\t\t'+\
                    'self.Constants=Constants\n\t\t'+\
                    'self.containingScenario=containingScenario\n\t\t'+\
                    'self.currentChemical=currentChemical\n\t\t'+\
                    'self.SendingCompartment=SendingCompartment\n\t\t'+\
                    'self.ReceivingCompartment=ReceivingCompartment\n\t\t'+\
                    'try: \n\t\t\t'
                    'self.transferFactor='+ tf +'\n\t\t'\
                    'except: \n\t\t\t'       
                    'self.transferFactor="TF Computation Error"')     
            
            residual_props=set(alg_props)-set(['category','chemicalCategory','doesTransformChemical','doesTransportChemical','enabled','isDefaultForCategory','mate','receivingChemicalName','receivingCompartmentCategory','sendingCompartmentCategory','sendingChemicalName','transferFactor'])
            for prop in residual_props:
                prop_val=grouped_alg.get_group(group).loc[grouped_alg.get_group(group)['Property']==prop]['Value'].values[0] #property value
                prop_val=clean_props(prop_val)
                if prop=='compartmentRelationship':
                    f.write('\n\t\t'
                            'self.'+prop+'='+"'"+prop_val+"'")                
                else:
                    f.write('\n\t\t'
                            'self.'+prop+'='+prop_val)                
            f.write('\n\n')    
            
    return(df_psalgs,df_ps,df_pt)
    
    
if __name__ == '__main__':
    df_psalgs,df_ps,df_pt=process_pseudo_library(inputs)
