# -*- coding: utf-8 -*-
"""
created on wed mar 31 21:15:14 2021
@author: 13963

parses properties text file  and stores as DataFrames of properties, links, including pseudo links
auto writes scripts to define attributes of scenario and various objects, specifically define_scenario.py and define_attributes_props.py

"""
import pandas as pd
import os
import re
from util_functions import * 




def define_properties(inputs):


    ifp=inputs['path_inputs']
    ifn=inputs['prop_file']    
    ifpn=os.path.join(ifp,ifn)
    

    prop_file=open(ifpn,'r') 
    prop_lines=prop_file.readlines()
    val_end_flag=False
    #### read volume element & compartment properties 
    
    prop_owner_types=['volumeelement','compartment','scenario']# list of property owners for which we are gathering inputs          
    prop_tuples=[] # initialize list for storing point lines
    prop_owner_list=[] # initialize list of property owners    
    
    for line in prop_lines: # loop over lines 
        line=line.strip() # strip /n and space       
        if line[:2]==r'//' or line=='': # if a comment or if blank, move on to next line
            continue # move to next line
        line_nc=line.split("//")[0] # line stripped of comment    
        prop_type=line_nc.split(':')[0].strip() # split on : . text to the left is the property type 
        if prop_type in prop_owner_types: # if volume element or compartment
            prop_type_flag=True # flag indicates that a new ve or comp has begun
            if val_end_flag and prop_type_flag: # if value reading has ended and a new property type has begun: 
                prop_owner_list=[]; prop="";form="";value="";val_end_flag=False         # initialize list and values    
            prop_owner=line_nc.split(":")[1].strip()
            prop_owner_list.append((prop_type,prop_owner)) 
        elif line_nc[:9]=="property:":        
            prop=line_nc.split(":")[1].strip()
        elif line_nc[:5]=="form:":   
            form=line_nc.split(":")[1].strip()
        elif line_nc[:6]=="value:":  
    #        value=line_nc.split(":")[1].strip()
            value="".join(line_nc.split(":")[1:])
            value=value.strip()
            for p_owner in prop_owner_list:                
                p=(p_owner[0],p_owner[1],prop,form,value)
    #            print (p)
                prop_tuples.append(p)
                val_end_flag=True      
            
    df_props=pd.DataFrame(prop_tuples,columns=['prop_type', 'prop_owner', 'property','form','value'])
    
    
    #### read links

    link_tuples=[]
    algs=[]
    for line in prop_lines: # loop over lines 
        line=line.strip() # strip /n and space       
        if line[:2]==r'//' or line=='': # if a comment or if blank, move on to next line
            continue # move to next line
        line_nc=line.split("//")[0] # line stripped of comment    
        prop_type=line_nc.split(':')[0].strip() # split on : . text to the left is the property type 
        if prop_type=='newlink': # if new link reinitialize algs list   
                algs=[]; sc="";rc="";prop="";form="";value=""         # initialize list and values
        elif prop_type=="sendingcompartment":
            sc=line_nc.split(':')[1].strip()
        elif prop_type=="receivingcompartment":
            rc=line_nc.split(':')[1].strip()
        elif prop_type=="algorithm":
            al=line_nc.split(':')[1].strip()
            algs.append(al)
        elif prop_type=="property":
            prop=line_nc.split(':')[1].strip()
        elif prop_type=="form":
            form=line_nc.split(':')[1].strip()
        elif prop_type=="value":
            val=line_nc.split(':')[1].strip()  
            if algs!=[] and sc!="" and rc!="": # as soon as value is read, associate it with all linked algorithms and add tuples to list 
                for alg in algs:
                     lp=(sc,rc,alg,prop,form,val)
                     link_tuples.append(lp)
    
            
        
    df_links=pd.DataFrame(link_tuples,columns=['sending_compartment', 'receiving_compartment', 'algorithm','property','form','value'])
    df_links=df_links.drop_duplicates()



    #### read other properties  file
    

#    ifp=inputs['path_inputs']
#    ifn=inputs['prop_file_2']    
#    ifpn=os.path.join(ifp,ifn)
#    
#
#    prop_file=open(ifpn,'r') 
#    prop_lines=prop_file.readlines()
#    val_end_flag=False
#
#    
#    prop_owner_types=['volumeelement','compartment','scenario']# list of property owners for which we are gathering inputs          
#    prop_tuples=[] # initialize list for storing point lines
#    prop_owner_list=[] # initialize list of property owners    
#    
#    for line in prop_lines: # loop over lines 
#        line=line.strip() # strip /n and space       
#        if line[:2]==r'//' or line=='': # if a comment or if blank, move on to next line
#            continue # move to next line
#        line_nc=line.split("//")[0] # line stripped of comment    
#        prop_type=line_nc.split(':')[0].strip() # split on : . text to the left is the property type 
#        if prop_type in prop_owner_types: # if volume element or compartment
#            prop_type_flag=True # flag indicates that a new ve or comp has begun
#            if val_end_flag and prop_type_flag: # if value reading has ended and a new property type has begun: 
#                prop_owner_list=[]; prop="";form="";value="";val_end_flag=False         # initialize list and values    
#            prop_owner=line_nc.split(":")[1].strip()
#            prop_owner_list.append((prop_type,prop_owner)) 
#        elif line_nc[:9]=="property:":        
#            prop=line_nc.split(":")[1].strip()
#        elif line_nc[:5]=="form:":   
#            form=line_nc.split(":")[1].strip()
#        elif line_nc[:6]=="value:":  
#    #        value=line_nc.split(":")[1].strip()
#            value="".join(line_nc.split(":")[1:])
#            value=value.strip()
#            for p_owner in prop_owner_list:                
#                p=(p_owner[0],p_owner[1],prop,form,value)
#    #            print (p)
#                prop_tuples.append(p)
#                val_end_flag=True      
#            
#    try:           
#        df_props_2=pd.DataFrame(prop_tuples,columns=['prop_type', 'prop_owner', 'property','form','value'])
#    except:
#        df_props_2=pd.DataFrame(columns=['prop_type', 'prop_owner', 'property','form','value'])
#    
#    val_end_flag=False 
#    link_tuples=[]
#    algs=[]
#    for line in prop_lines: # loop over lines 
#        line=line.strip() # strip /n and space       
#        if line[:2]==r'//' or line=='': # if a comment or if blank, move on to next line
#            continue # move to next line
#        line_nc=line.split("//")[0] # line stripped of comment    
#        prop_type=line_nc.split(':')[0].strip() # split on : . text to the left is the property type 
#        if prop_type=='new link': # if volume element or compartment        
#            new_link_flag=True # flag indicates that a new link has begun
#            if val_end_flag and new_link_flag: # if value reading has ended and a new property type has begun: 
#                algs=[]; sc="";rc="";prop="";form="";value="";val_end_flag=False         # initialize list and values    
#        elif prop_type=="sendingcompartment":
#            sc=line_nc.split(':')[1].strip()
#        elif prop_type=="receivingcompartment":
#            rc=line_nc.split(':')[1].strip()
#        elif prop_type=="algorithm":
#            al=line_nc.split(':')[1].strip()
#            algs.append(al)
#        elif prop_type=="property":
#            prop=line_nc.split(':')[1].strip()
#        elif prop_type=="form":
#            form=line_nc.split(':')[1].strip()
#        elif prop_type=="value":
#            val=line_nc.split(':')[1].strip()
#            val_end_flag=True      
#            if algs!=[] and sc!="" and rc!="": 
#                for alg in algs:
#                     lp=(sc,rc,alg,prop,form,val)
#                     link_tuples.append(lp)
#    
#            
#    try:    
#        df_links_2=pd.DataFrame(link_tuples,columns=['sending_compartment', 'receiving_compartment', 'algorithm','property','form','value'])
#    except:
#        df_links_2=pd.DataFrame(columns=['sending_compartment', 'receiving_compartment', 'algorithm','property','form','value'])
#
#    
   
    #### read custom links  file. Note this part of the code is specific to the way inputs were specified for the Foundries run. May not have generic value.
    

    ifp=inputs['path_inputs']
    ifn=inputs['prop_file_3']    
    ifpn=os.path.join(ifp,ifn)
    

    prop_file=open(ifpn,'r') 
    prop_lines=prop_file.readlines()
    val_end_flag=False
    
    prop_owner_types=['compartment','link']# list of property owners for which we are gathering inputs          
    prop_tuples=[] # initialize list for storing point lines
    prop_owner_list=[] # initialize list of property owners    
    
    for line in prop_lines: # loop over lines 
        line=line.strip() # strip /n and space       
        if line[:2]==r'//' or line=='': # if a comment or if blank, move on to next line
            continue # move to next line
        line_nc=line.split("//")[0] # line stripped of comment    
        prop_type=line_nc.split(':')[0].strip() # split on : . text to the left is the property type 
        if prop_type in prop_owner_types: # if volume element or compartment
            prop_type_flag=True # flag indicates that a new ve or comp has begun
            if val_end_flag and prop_type_flag: # if value reading has ended and a new property type has begun: 
                prop_owner_list=[]; prop="";form="";value="";val_end_flag=False         # initialize list and values    
            prop_owner=line_nc.split(":")[1].strip()
            prop_owner_list.append((prop_type,prop_owner)) 
        elif line_nc[:9]=="property:":        
            prop=line_nc.split(":")[1].strip()
        elif line_nc[:5]=="form:":   
            form=line_nc.split(":")[1].strip()
        elif line_nc[:6]=="value:":  
    #        value=line_nc.split(":")[1].strip()
            value="".join(line_nc.split(":")[1:])
            value=value.strip()
            for p_owner in prop_owner_list:                
                p=(p_owner[0],p_owner[1],prop,form,value)
    #            print (p)
                prop_tuples.append(p)
                val_end_flag=True      
    
    try:        
        df_props_3=pd.DataFrame(prop_tuples,columns=['prop_type', 'prop_owner', 'property','form','value'])
    except:
        df_props_3=pd.DataFrame(columns=['prop_type', 'prop_owner', 'property','form','value'])
    
#    df_link_props=df_props_3.loc[df_props_3['prop_type']=='link'] # not required because same information in df_links_3
#    
    df_non_link_props=df_props_3.loc[df_props_3['prop_type']!='link']
    
    df_props=df_props.append(df_non_link_props) # append the non link props to the main df_props
    df_props=df_props.reset_index(drop=True) # reset index from zero
    
    val_end_flag=False 
    link_tuples=[]
    algs=[]; sc="";rc="";prop="";form="";value="";
    for line in prop_lines: # loop over lines 
        line=line.strip() # strip /n and space       
        if line[:2]==r'//' or line=='': # if a comment or if blank, move on to next line
            continue # move to next line
        line_nc=line.split("//")[0] # line stripped of comment    
        prop_type=line_nc.split(':')[0].strip() # split on : . text to the left is the property type 
        if prop_type=='new link': # if new link        
            new_link_flag=True # flag indicates that a new link has begun
            if val_end_flag and new_link_flag: # if value reading has ended and a new property type has begun: 
                algs=[]; sc="";rc="";prop="";form="";value="";val_end_flag=False         # initialize list and values    
        elif prop_type=="sendingcompartment":
            sc=line_nc.split(':')[1].strip()
        elif prop_type=="receivingcompartment":
            rc=line_nc.split(':')[1].strip()
        elif prop_type=="algorithm":
            al=line_nc.split(':')[1].strip()
            algs.append(al)
        elif prop_type=="property":
            prop=line_nc.split(':')[1].strip()
        elif prop_type=="form":
            form=line_nc.split(':')[1].strip()
        elif prop_type=="value":
            val=line_nc.split(':')[1].strip()
            val_end_flag=True      
            if algs!=[] and sc!="" and rc!="": 
                for alg in algs:
                     lp=(sc,rc,alg,prop,form,val)
                     link_tuples.append(lp)
            
        
    try:
        df_links_3=pd.DataFrame(link_tuples,columns=['sending_compartment', 'receiving_compartment', 'algorithm','property','form','value'])
        df_links_3=df_links_3.drop_duplicates()
    except:
        df_links_3=pd.DataFrame(columns=['sending_compartment', 'receiving_compartment', 'algorithm','property','form','value'])

#    df_props=df_props.append(df_props_2)
#    df_props=df_props.append(df_props_3)
#
##    df_links=df_props.append(df_links_2)
    df_links=df_links.append(df_links_3) # append links in df_links_3 to main df_links
    df_links=df_links.reset_index(drop=True) # reset index from zero
#
#    
    #### read pseudo volume element links
    
     
    ifn=inputs['plink_file']
    ifpn=os.path.join(ifp,ifn)
    
    prop_file=open(ifpn,'r') 
    prop_lines=prop_file.readlines()
    
    link_tuples=[]
    for line in prop_lines: # loop over lines 
        line=line.strip() # strip /n and space       
        if line[:2]==r'//' or line=='': # if a comment or if blank, move on to next line
            continue # move to next line
        line_nc=line.split("//")[0] # line stripped of comment    
        prop_type=line_nc.split(':')[0].strip() # split on : . text to the left is the property type 
        if prop_type=="sendingcompartment":
            sc=line_nc.split(':')[1].strip()
        elif prop_type=="receivingcompartment":
            rc=line_nc.split(':')[1].strip()
        elif prop_type=="algorithm":
            al=line_nc.split(':')[1].strip()
            lp=(sc,rc,al)
            link_tuples.append(lp)
    
            
        
    df_plinks=pd.DataFrame(link_tuples,columns=['sending_compartment', 'receiving_compartment', 'algorithm'])
    
    ############# autowrite define_scenario codefile
    
    ofp=inputs['path_code']        
    ofn=r'define_scenario.py'
    ofpn=os.path.join(ofp,ofn)
    
    
    def clean_names(name): # function to replace certain special characters with underscore
        cname=name.replace(r'/','_').replace(r'-','_').replace(' ','_').replace('___','_').replace('__','_')
        return (cname)
    
    sc_name=df_props.loc[df_props['prop_type']=='scenario']['prop_owner'].values[0]
    
    sc_name_new=clean_names(sc_name)
    
    with open(ofpn, 'w') as f:
        f.write('''\
'### note: this is an auto generated script'                

class scenario:()
''')   
    
    with open(ofpn, 'a') as f:    
        f.write(str(sc_name_new)+\
                            "=scenario()"+'\n'+\
                 'containingscenario='+ str(sc_name_new)          )
        
    ### autowrite add_attributes_prop.py codefile
        
    
    ### assumes df_prop in memory
    
    def clean_names(name): # function to replace certain special characters with underscore
        cname=name.replace(r'/','_').replace(r'-','_').replace(' ','_').replace('___','_').replace('__','_')
        # standardize plant composite compartment names to avoid double mention of component as implemented in comp.py
        plant_types=['deciduous_forest_in_','coniferous_forest_in','grasses_herbs_in'] 
        for plant in plant_types:
            if plant in cname:
                cname=cname.replace(plant+plant,plant) # replace double occurrence with single mention
        return (cname)
    
    def clean_values(name): # function to replace certain special characters with underscore
        if type(name)==str:
            cname=str(name.replace(r'/','_').replace(' ','_').replace('___','_').replace('__','_'))
            cname=cname.replace('False','False')
            cname=cname.replace('True','True')
            if r'c\\' in cname:
                try:
                    metfile=cname.split('\\')[-1].split(',')[0].strip('_') 
                    metfile=metfile[:-4]+'.csv'
                    metcol=cname.split('\\')[-1].split(',')[1].strip('_')                    
                    # cname='get_met_ave('+'"'+metfile+'"'+','+'"'+metcol+'"'+')' # use met averages to replace time series
                    # cname='get_met_wt_ave(mfp,mfn,'+'"'+metcol+'"'+')' # use wt met averages to replace time series (doesnt work)
                    met_key_name="wt_av_"+metcol
                    # cname='dict_inputs["met_dict"]["'+str(met_key_name)+'"]'
                    cname=str(met_key_name)
                except:
                    pass                
        return (cname)
    
    def add_quotes(name): # function to add quotes to strings containing \ or / ## this is very hacky for now
        # if type(name)==str and (r'\\' in name or '_' in name or name=='annual') and ('get_met_ave' not in name):
        # if type(name)==str and (r'\\' in name or '_' in name or name=='annual') and ('get_met_wt_ave' not in name):
        if type(name)==str and (r'\\' in name or '_' in name or name=='annual') and (name not in inputs['met_dict'].keys()):
            cname="'"+name+"'"
            return (cname)
        return(name)
    
    df_props['prop_owner_new']=df_props['prop_owner'].apply(clean_names)
    df_props['property_new']=df_props['property'].apply(clean_names)
    df_props['value_new']=df_props['value'].apply(clean_values)
    df_props['value_new']=df_props['value_new'].apply(add_quotes)

    def clean_names_algs(name): # not sure if this same function could be applied to props above -- clean up later. function to replace certain special characters with underscore; leaves float values alone
        try:
            name=float(name) 
        except:
            pass
        if type(name)==str:
            cname = re.sub('[^0-9a-za-z]+', '_', name)
            cname=cname.strip('_')
            return(cname)            
        return(name)  

    def standardize_adv_sinks(cname):        
            cname=cname.replace('soil_advection_sink','sink_in_sink_for_soil_surface') # fix different names for advection sinks in input files and compartment names 
            return(cname)            


    df_links['sending_compartment_new']=df_links['sending_compartment'].apply(clean_names_algs)    
    df_links['receiving_compartment_new']=df_links['receiving_compartment'].apply(clean_names_algs)    
    df_links['sending_compartment_new']=df_links['sending_compartment_new'].apply(standardize_adv_sinks)    
    df_links['receiving_compartment_new']=df_links['receiving_compartment_new'].apply(standardize_adv_sinks)    

    df_links['algorithm_new']=df_links['algorithm'].apply(clean_names_algs)    

    
    ofn=r'define_attributes_props.py'
    ofpn=os.path.join(ofp,ofn)
    
    with open(ofpn, 'w') as f:
        f.write('### note: this is an auto generated script' +'\n')        
        f.write('''\
import pandas as pd
import os
from constants import *
from define_scenario import *
from define_ve import *
from define_pve import *
from define_algs import *
from define_ps_algs import *
from util_functions import *


def get_met_ave(mfn,mfcol):
    mfpn=os.path.join(mfp,mfn)
    df=pd.read_csv(mfpn) 
    try:
        ave=pd.to_numeric(df[mfcol], errors='coerce').mean()
    except:
        ave=0
    return(ave)
        
''')

        # f.write('mfp=r"'+str(inputs['path_inputs'])+'"'+'   # path to met file'+'\n') 
        # f.write('mfn=r"'+str(inputs['met_file'])+'"'+'   # met file name'+'\n\n\n') 
        for k,v in inputs['met_dict'].items():
            f.write(k+'='+str(v)+'\n')
        f.write('\n')    

        for i in range(len(df_props)):
            obj=df_props.loc[i,'prop_owner_new']
            if True: # temporary. use condition below later.
    #        if obj in locals(): # may miss a few objects owing to name cleaning?
    #            print (obj)
                f.write('try:'+'\n\t')
                f.write(str(obj)+\
                       "." +\
                       str(df_props.loc[i,'property_new'])+\
                       "="+\
                       str(df_props.loc[i,'value_new']))
                f.write('\n'+'except:'+'\n\t'+'pass') 
                f.write('\n')            

#### Read, process, and write other properties file


    ifp=inputs['path_inputs']
    ifn=inputs['prop_file_2']    
    ifpn=os.path.join(ifp,ifn)
    

    prop_file=open(ifpn,'r') 
    prop_lines=prop_file.readlines()
    val_end_flag=False
    #### read volume element & compartment properties 
    
    prop_owner_types=['volumeelement','compartment','scenario']# list of property owners for which we are gathering inputs          
    prop_tuples=[] # initialize list for storing point lines
    prop_owner_list=[] # initialize list of property owners    
    
    for line in prop_lines: # loop over lines 
        line=line.strip() # strip /n and space       
        if line[:2]==r'//' or line=='': # if a comment or if blank, move on to next line
            continue # move to next line
        line_nc=line.split("//")[0] # line stripped of comment    
        prop_type=line_nc.split(':')[0].strip() # split on : . text to the left is the property type 
        if prop_type in prop_owner_types: # if volume element or compartment
            prop_type_flag=True # flag indicates that a new ve or comp has begun
            if val_end_flag and prop_type_flag: # if value reading has ended and a new property type has begun: 
                prop_owner_list=[]; prop="";form="";value="";val_end_flag=False         # initialize list and values    
            prop_owner=line_nc.split(":")[1].strip()
            prop_owner_list.append((prop_type,prop_owner)) 
        elif line_nc[:9]=="property:":        
            prop=line_nc.split(":")[1].strip()
        elif line_nc[:5]=="form:":   
            form=line_nc.split(":")[1].strip()
        elif line_nc[:6]=="value:":  
    #        value=line_nc.split(":")[1].strip()
            value="".join(line_nc.split(":")[1:])
            value=value.strip()
            for p_owner in prop_owner_list:                
                p=(p_owner[0],p_owner[1],prop,form,value)
    #            print (p)
                prop_tuples.append(p)
                val_end_flag=True      
            
    df_props_2=pd.DataFrame(prop_tuples,columns=['prop_type', 'prop_owner', 'property','form','value'])
    
    df_props_2['prop_owner_new']=df_props_2['prop_owner'].apply(clean_names)
    df_props_2['property_new']=df_props_2['property'].apply(clean_names)
    df_props_2['value_new']=df_props_2['value'].apply(clean_values)
    df_props_2['value_new']=df_props_2['value_new'].apply(add_quotes)

    with open(ofpn, 'a') as f:
        f.write('### note: this is to write other properties' +'\n')        
        for i in range(len(df_props_2)):
            obj=df_props_2.loc[i,'prop_owner_new']
            if True: # temporary. use condition below later.
    #        if obj in locals(): # may miss a few objects owing to name cleaning?
    #            print (obj)
                cname=df_props_2.loc[i,'value'].split('}')[0].replace('{','').strip()# get chem name
                cname=clean_chem_names(cname)
                pval=df_props_2.loc[i,'value'].split('}')[1].replace('{','').strip() # get value
                f.write('try:'+'\n\t')
                f.write(str(obj)+\
                       "." +\
                       str(df_props_2.loc[i,'property_new'])+\
                       "['"+\
                       str(cname)+\
                       "']="+\
                       str(pval))+\
                f.write('\n'+'except:'+'\n\t'+'pass') 
                f.write('\n')            


            
    return(df_props,df_props_2,df_links,df_plinks)