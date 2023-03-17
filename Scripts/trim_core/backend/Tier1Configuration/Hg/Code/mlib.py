# -*- coding: utf-8 -*-
"""
created on mon apr  5 14:41:50 2021
@author: 13963

this module reads in the legacy trim.fate master library in csv format
it creates DataFrames to store the whole library, algorithms, matrix of algorithm applicability, and chemicals
it writes scripts to define algorithm,  chemical,  and generic compartment classes, specifically: define_algs.py, define_chem_classes.py, define_comp_classes.py

"""

import pandas as pd
import os
import re
from numpy import nan
#import required_elements as req
import required_elements_temp as req
from util_functions import * 


def linkcomp(txt):

    s=txt.split('(linkedcompartment')
    e1=s[0]
    e2=s[1].split(']')[0].strip('[').split('|')[1].strip().replace(' ','_')
    e3=s[1].split(']')[1].split(')')[0].strip().strip('.')
    
    rem_list=s[1].split(']')[1].split(')')[1:]
    if rem_list[-1]==['']:
        rem_list=rem_list[:-1]
        rem_list=[x+')' for x in rem_list]
    else:
        last=rem_list[-1:]
        rem_list=[x+')' for x in rem_list[:-1]] +last
    
    e4=''.join(rem_list)
    
    exp=e1+'linkedCompartmentvalue(self.containingvolumeelement,self.comp_objects_dict,"'+e2+'","'+e3+'")'+e4
    return (exp)


def process_master_library(inputs):

    ifp=inputs['path_inputs']
    ifn=inputs['master_library_file']
    
    ifpn=os.path.join(ifp,ifn)
    
    header=pd.read_csv(ifpn,sep=';',nrows=0,encoding='windows-1252').columns
    
    df_lib=pd.read_csv(ifpn,sep=';',names=header,skiprows=[0],encoding='windows-1252') # read library into DataFrame
    
    ############ write python script to define algorithm classes 
    
    df_alg=df_lib.loc[df_lib['objecttype']=='algorithm']
    grouped_alg = df_alg.groupby("objectname")
    
    
    ofp=inputs['path_code']
    ofn=r'define_algs.py'
    ofpn=os.path.join(ofp,ofn)
    
    
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
    
    def clean_props(prop): # function to convert properties to pythonic syntax, 
           
        if '?' in prop: # change ternary if then else syntax to pythonic syntax
            prop=ternary2python(prop)
            
        prop=prop.replace('constants','self.constants')
        prop=prop.replace('containingscenario','self.containingscenario')
        prop=prop.replace('receivingcompartment','self.receivingcompartment')
        prop=prop.replace('sendingcompartment','self.sendingcompartment')
#        prop=prop.replace('sendingcompartment','self.sendingcompartment')
        prop=prop.replace('algorithm.','self.')
        prop=prop.replace('chemical.','chemical_')
        prop=prop.replace('z_total','z_total')
        prop=prop.replace ('!',' not ')
        prop=prop.replace('sendingchemical_','self.currentchemical.')
        prop=prop.replace('receivingchemical_','self.currentchemical.')
        prop=prop.replace('molecularweight','molecularweight')        
        prop=prop.replace('ln','log')
        prop=prop.replace('if (self.containingscenario.rain==0 and self.sendingcompartment.volume>0) else 0',' * (1-self.dict_inputs["met_dict"]["frac_time_rain"]) if self.sendingcompartment.volume>0 else 0')   ## important: replace rain time dependent switch with fraction of time rain for static non time series analysis. affects algorithm -- blowing particles of leaf to air    (when not raining)
        prop=prop.replace('if (self.containingscenario.rain>0 and self.sendingcompartment.volume>0) else 0','*self.dict_inputs["met_dict"]["frac_time_rain"]') ## important: replace rain time dependent switch with fraction of time rain for static non time series analysis. affects algorithm -- blowing particles of leaf to ground    (when raining)

        
        if 'thelink.interfacialarea' in prop: # replace thelink interfacial area custom function with python function
            prop=prop.replace('thelink.interfacialarea','check_neighbor(self.sendingcompartment,self.receivingcompartment,self.dict_inputs).is_neighbor()[1]')           
        if 'thelink.fractionspecificcompartmentdiet' in prop: # replace thelink.fractionspecificcompartmentdiet with 1. i believe this okay but check ug.
            prop=prop.replace('thelink.fractionspecificcompartmentdiet','1')          

        if 'thelink.bulkwaterflowrate_volumetric' in prop: # hack to deal with interconnected water bodies
            prop=prop.replace('thelink.bulkwaterflowrate_volumetric',"float(self.dict_inputs['df_links'].loc[(self.dict_inputs['df_links']['receiving_compartment_new']==self.receivingcompartment.name)&(self.dict_inputs['df_links']['sending_compartment_new']==self.sendingcompartment.name)&(self.dict_inputs['df_links']['property']=='bulkwaterflowrate_volumetric'),'value'].values[0])")          

        if 'thelink.fractionoftotalrunoff' in prop: # hack to deal with runoff link
            prop=prop.replace('thelink.fractionoftotalrunoff',"float(self.dict_inputs['df_links'].loc[(self.dict_inputs['df_links']['receiving_compartment_new']==self.receivingcompartment.name)&(self.dict_inputs['df_links']['sending_compartment_new']==self.sendingcompartment.name)&(self.dict_inputs['df_links']['property']=='fractionoftotalrunoff'),'value'].values[0])")          
        if 'thelink.fractionoftotalerosion' in prop: # hack to deal with erosion link
            prop=prop.replace('thelink.fractionoftotalerosion',"float(self.dict_inputs['df_links'].loc[(self.dict_inputs['df_links']['receiving_compartment_new']==self.receivingcompartment.name)&(self.dict_inputs['df_links']['sending_compartment_new']==self.sendingcompartment.name)&(self.dict_inputs['df_links']['property']=='fractionoftotalerosion'),'value'].values[0])")          
        
        if 'sendingwithincompositecompartment[terrestrial plant | leaf]'in prop:
            prop=prop.replace('sendingwithincompositecompartment[terrestrial plant | leaf].','self.sendingcompartment.associated_leaf_comp.')

        if 'thelink.rechargerate'in prop: ## default value -- find a way to read default values when properties are not defined in properties file
            prop=prop.replace('thelink.rechargerate','default_rechargerate')

        if 'sendingvolumeelementsumof[terrestrial plant | leaf]'in prop:
            prop=prop.replace('sendingvolumeelementsumof[terrestrial plant | leaf].','self.sendingcompartment.associated_leaf_comp.')
        

        if 'self.sendingcompartment.allowexchange_forother' in prop and '1-self.dict_inputs["met_dict"]["frac_time_rain"]' in prop: # to address interaction between exchange and rain
            prop=prop.replace('self.sendingcompartment.allowexchange_forother','1')
            # prop=prop.replace('1-self.dict_inputs["met_dict"]["frac_time_rain"]','self.dict_inputs["met_dict"]["frac_time_exchange_no_rain"]')
            prop=prop.replace('1-self.dict_inputs["met_dict"]["frac_time_rain"]','(self.dict_inputs["met_dict"]["frac_time_exchange_no_rain"] if ("coniferous" not in self.sendingcompartment.name) else (1-self.dict_inputs["met_dict"]["frac_time_rain"]))' )

        if 'self.sendingcompartment.allowexchange_forother' in prop and 'self.dict_inputs["met_dict"]["frac_time_rain"]' in prop: # to address interaction between exchange and rain
            prop=prop.replace('self.sendingcompartment.allowexchange_forother','1')
            # prop=prop.replace('self.dict_inputs["met_dict"]["frac_time_rain"]','self.dict_inputs["met_dict"]["frac_time_exchange_rain"]')
            # prop=prop.replace('self.dict_inputs["met_dict"]["frac_time_rain"]','(self.dict_inputs["met_dict"]["frac_time_exchange_rain"] if ("coniferous" not in self.sendingcompartment.name) else self.dict_inputs["met_dict"]["frac_time_rain"])')
            prop=prop.replace('self.dict_inputs["met_dict"]["frac_time_rain"]','(self.dict_inputs["met_dict"]["wt_av_allowexchange"] if ("coniferous" not in self.sendingcompartment.name) else 1)')

        if '((self.receivingcompartment.chemical_dustresuspensionrate * (1 -  (  self.sendingcompartment.associated_leaf_comp.allowexchange_forair * self.sendingcompartment.associated_leaf_comp.drydepinterceptionfraction )))' in prop: # fix to ensure alg 4000 works for vegetationless compartments
            prop=prop.replace('((self.receivingcompartment.chemical_dustresuspensionrate * (1 -  (  self.sendingcompartment.associated_leaf_comp.allowexchange_forair * self.sendingcompartment.associated_leaf_comp.drydepinterceptionfraction )))','((self.receivingcompartment.chemical_dustresuspensionrate * (1 -(self.sendingcompartment.associated_leaf_comp.allowexchange_forair * self.sendingcompartment.associated_leaf_comp.drydepinterceptionfraction) if hasattr(self.sendingcompartment,"associated_leaf_comp") else 1))')

        return (prop)
   
    required_algs=req.required_algorithms # look up list of required algorithms
    required_algs=list(set(required_algs)) # get rid of dups if any
    
    with open(ofpn, 'w') as f:  
        f.write('### note: this is an auto generated script' +'\n')        
        f.write('from find_neighbors import *' +'\n')
        f.write('from numpy import sqrt,nan,log,exp' +'\n')
        f.write('from util_functions import *' +'\n')
        f.write('mfp=r"'+str(inputs['path_inputs'])+'"'+'   # path to met file'+'\n') 
        f.write('mfn=r"'+str(inputs['met_file'])+'"'+'   # met file name'+'\n') 
        f.write('default_rechargerate=1.42e-04'+'\n\n\n')
        # f.write('print("Fraction Time Rain = ", frac_time_rain(mfp,mfn))'+'\n\n\n') # test 

        
        for index,group in enumerate(grouped_alg.groups):
            if group not in required_algs:
                continue
            alg_name=clean_names(group)
            alg_props=list(grouped_alg.get_group(group)['propertyname'].unique())
            tf=grouped_alg.get_group(group).loc[grouped_alg.get_group(group)['propertyname']=='transferfactor']['propertyvalue'].values[0]#.replace('sendingcompartment','self.sendingcompartment').replace('receivingcompartment','self.receivingcompartment')
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
                    'self.category='+"'"+grouped_alg.get_group(group).loc[grouped_alg.get_group(group)['propertyname']=='category']['propertyvalue'].values[0]+"'"+'\n\t\t'
                    'self.chemicalcategory='+"'"+grouped_alg.get_group(group).loc[grouped_alg.get_group(group)['propertyname']=='chemicalcategory']['propertyvalue'].values[0]+"'"+'\n\t\t'
                    'self.doestransformchemical='+"'"+grouped_alg.get_group(group).loc[grouped_alg.get_group(group)['propertyname']=='doestransformchemical']['propertyvalue'].values[0]+"'"+'\n\t\t'
                    'self.transportchemical='+"'"+grouped_alg.get_group(group).loc[grouped_alg.get_group(group)['propertyname']=='doestransportchemical']['propertyvalue'].values[0]+"'"+'\n\t\t'
                    'self.enabled='+"'"+grouped_alg.get_group(group).loc[grouped_alg.get_group(group)['propertyname']=='enabled']['propertyvalue'].values[0]+"'"+'\n\t\t'
                    'self.isdefaultforcategory='+"'"+grouped_alg.get_group(group).loc[grouped_alg.get_group(group)['propertyname']=='isdefaultforcategory']['propertyvalue'].values[0]+"'"+'\n\t\t'
                    'self.mate='+"'"+grouped_alg.get_group(group).loc[grouped_alg.get_group(group)['propertyname']=='mate']['propertyvalue'].values[0]+"'"+'\n\t\t'
                    'self.receivingchemicalname='+"'"+grouped_alg.get_group(group).loc[grouped_alg.get_group(group)['propertyname']=='receivingchemicalname']['propertyvalue'].values[0]+"'"+'\n\t\t'
                    'self.receivingcompartmentcategory='+"'"+grouped_alg.get_group(group).loc[grouped_alg.get_group(group)['propertyname']=='receivingcompartmentcategory']['propertyvalue'].values[0]+"'"+'\n\t\t'
                    'self.sendingcompartmentcategory='+"'"+grouped_alg.get_group(group).loc[grouped_alg.get_group(group)['propertyname']=='sendingcompartmentcategory']['propertyvalue'].values[0]+"'"+'\n\t\t'
                    'self.sendingchemicalname='+"'"+grouped_alg.get_group(group).loc[grouped_alg.get_group(group)['propertyname']=='sendingchemicalname']['propertyvalue'].values[0]+"'"+'\n\t\t'
                    'self.dict_inputs=dict_inputs'+'\n\t\t')
                    
            residual_props=set(alg_props)-set(['category','chemicalcategory','doestransformchemical','doestransportchemical','enabled','isdefaultforcategory','mate','receivingchemicalname','receivingcompartmentcategory','sendingcompartmentcategory','sendingchemicalname','transferfactor'])

### testing method decorator approach

            for prop in residual_props:
                prop_val=grouped_alg.get_group(group).loc[grouped_alg.get_group(group)['propertyname']==prop]['propertyvalue'].values[0] #property value
                prop_val=clean_props(prop_val)
                if type(prop_val)==float or is_number(prop_val):
                    f.write('\n\t'+\
                            '_'+prop+'='+prop_val +'\n\t' +\
                            '@property'+'\n\t' +\
                            'def '+prop+'(self):'+'\n\t\t' +\
                            'return self._'+prop+'\n\n\t' +\
                            '@'+prop+'.setter''\n\t' +\
                            'def '+prop+'(self,value):'+'\n\t\t' +\
                            'self._'+prop+'=value\n')             
                else:
                    if prop=='compartmentrelationship': # write as string
                        f.write('\n\t'+\
                                '@property'+'\n\t' +\
                                'def '+prop+'(self):'+'\n\t\t' +\
                                'return ("'+prop_val+'")\n\t') 
                    else:
                        f.write('\n\t'+\
                                '@property'+'\n\t' +\
                                'def '+prop+'(self):'+'\n\t\t' +\
                                'return ('+prop_val+')\n\t') 


            f.write('\n\t'+\
                    '@property'+'\n\t' +\
                    'def transferfactor(self):'+'\n\t\t' +\
                    'try:'+'\n\t\t\t' +\
                    'r='+tf+'\n\t\t' +\
                    'except:'+'\n\t\t\t' +\
                    'r=nan'+'\n\t\t'+\
                    'return (r)') 

            f.write('\n\n')    

   
        
    ########### create matrix of algorithm applicability i.e. which algorithms apply given a receiving compartment and a sending compartment
    
    alg_mat=[]
            
    for index,group in enumerate(grouped_alg.groups):    
        if group not in required_algs:
            continue    
        
        alg_name=clean_names(group)    
        category=grouped_alg.get_group(group).loc[grouped_alg.get_group(group)['propertyname']=='category']['propertyvalue'].values[0]
        chemical_category=grouped_alg.get_group(group).loc[grouped_alg.get_group(group)['propertyname']=='chemicalcategory']['propertyvalue'].values[0]
        enabled=grouped_alg.get_group(group).loc[grouped_alg.get_group(group)['propertyname']=='enabled']['propertyvalue'].values[0]
        isdefaultforcategory=grouped_alg.get_group(group).loc[grouped_alg.get_group(group)['propertyname']=='isdefaultforcategory']['propertyvalue'].values[0]
        receivingchemicalname=grouped_alg.get_group(group).loc[grouped_alg.get_group(group)['propertyname']=='receivingchemicalname']['propertyvalue'].values[0]
        receivingcompartmentcategory=grouped_alg.get_group(group).loc[grouped_alg.get_group(group)['propertyname']=='receivingcompartmentcategory']['propertyvalue'].values[0]
        sendingcompartmentcategory=grouped_alg.get_group(group).loc[grouped_alg.get_group(group)['propertyname']=='sendingcompartmentcategory']['propertyvalue'].values[0]
        sendingchemicalname=grouped_alg.get_group(group).loc[grouped_alg.get_group(group)['propertyname']=='sendingchemicalname']['propertyvalue'].values[0]
        alg_mat.append((index,group,alg_name,category,chemical_category,enabled,isdefaultforcategory,receivingchemicalname,receivingcompartmentcategory,sendingcompartmentcategory,sendingchemicalname))
    
    cols=['index','group','alg_name_new','category','chemical_category','enabled','isdefaultforcategory','receivingchemicalname','receivingcompartmentcategory','sendingcompartmentcategory','sendingchemicalname']   
    df_alg_mat=pd.DataFrame(alg_mat,columns=cols)
    
       
    
    
    #### ############ write python script to define chemical classes
    
    ofn=r'define_chem_classes.py'
    ofpn=os.path.join(ofp,ofn)
    
    def clean_names(name): # function to replace certain special characters with underscore; leaves float values alone
        try:
            name=float(name) 
        except:
            pass
        if type(name)==str:
            cname = 'chem_'+re.sub('[^0-9a-za-z]+', '_', name)
            return(cname)
        return(name)  
    

    def clean_props(prop): # function to convert properties to pythonic syntax, 

        if '?' in prop: # change ternary if then else syntax to pythonic syntax
            prop=ternary2python(prop)
        prop=prop.replace('constants','self.constants')
        prop=prop.replace('containingscenario','self.containingscenario')
        prop=prop.replace('chemical','self')
        prop=prop.replace('ln','log')
        prop=prop.replace('<unset>','"<unset>"')

        return (prop)
    
    df_chem=df_lib.loc[df_lib['objecttype']=='chemical']
    grouped_chem = df_chem.groupby("objectname")
    
    
#    desired_order=['original_chemical_name','cas','category','d_pureair','d_pureair_m2_s','d_purewater','d_purewater_m2_per_s','doestransform','enabled','henrylawconstant','h_over_r_t','airwaterpartitioncoefficient','k_ow','k_oa','k_oc','log10_k_oa','log10_k_ow','meltingpoint','molecularweight','referencebird_bodyweight','referencebird_eliminationrate','referencebird_generaldegradationrate','referencemammal_bodyweight','referencemammal_eliminationrate','referencemammal_generaldegradationrate','z_pureair','z_purewater']
    formula_props=['d_pureair','d_pureair_m2_s','d_purewater','d_purewater_m2_per_s','henrylawconstant','h_over_r_t','airwaterpartitioncoefficient','k_ow','k_oa','k_oc','log10_k_oa','log10_k_ow','meltingpoint','molecularweight','referencebird_bodyweight','referencebird_eliminationrate','referencebird_generaldegradationrate','referencemammal_bodyweight','referencemammal_eliminationrate','referencemammal_generaldegradationrate','z_pureair','z_purewater','vaporwashoutratio','molesofreportingchemicalpermolesofthischemical','reportingchemicalmw']
    
    chem_dict={}
    sim_chem_list=inputs['simulation_chemicals']
    sim_chem_list_clean=[clean_chem_names(x) for x in sim_chem_list]
    
    with open(ofpn, 'w') as f:  
        f.write('### note: this is an auto generated script' +'\n')        
        f.write('''\

from math import log
from constants import *
from define_scenario import *
from define_attributes_props import *

''')

## testing method decorator approach

        for index,group in enumerate(grouped_chem.groups):
            chem_name=clean_chem_names(group) # for use as object name
            if chem_name not in sim_chem_list_clean:
                continue
            chem_dict[index]=chem_name
            chem_name_strip=chem_name.strip('_') # for use as cleaned original chem name
            chem_props=list(grouped_chem.get_group(group)['propertyname'].unique())

            f.write('\n\n'+'class '+str(chem_name)+':'+'\n' +\
                    '\t'+\
                    'def __init__(self,constants,containingscenario):\n\t\t'+\
                    'self.containingscenario=containingscenario\n\t\t'+\
                    'self.constants=constants\n\t\t'+\
                    'self.name='+"'"+str(chem_name_strip)+"'"+'\n')

            for prop in chem_props:
                
                prop_val=grouped_chem.get_group(group).loc[grouped_chem.get_group(group)['propertyname']==prop]['propertyvalue'].values[0] #property value
                if type(prop_val)==float or is_number(prop_val):
                    f.write('\n\t'+\
                            '_'+prop+'='+prop_val +'\n\t' +\
                            '@property'+'\n\t' +\
                            'def '+prop+'(self):'+'\n\t\t' +\
                            'return self._'+prop+'\n\n\t' +\
                            '@'+prop+'.setter''\n\t' +\
                            'def '+prop+'(self,value):'+'\n\t\t' +\
                            'self._'+prop+'=value\n')             
                else:
                    if prop in formula_props:                    
                        prop_val=clean_props(prop_val)
                        f.write('\n\t'+\
                                '@property'+'\n\t' +\
                                'def '+prop+'(self):'+'\n\t\t' +\
                                'return ('+prop_val+')\n\t') 
                    else:
                        prop_val=clean_props(prop_val)
                        f.write('\n\t'+\
                                '@property'+'\n\t' +\
                                'def '+prop+'(self):'+'\n\t\t' +\
                                'return ("'+prop_val+'")\n\t') 
                        
        f.write('\n\n')    

        f.write('chem_objects_dict={}'+'\n')   
        for k,v in chem_dict.items():
            if v not in sim_chem_list_clean:
                continue
            f.write(str(v)+'='+str(v)+'(constants,containingscenario)'+'\n')
            f.write('chem_objects_dict['+'"'+str(v)+'"'+']='+str(v)+'\n')
        
    f.close()    
    


    
    
    #### ############ write python script to define general compartment classes
    
    # problem with double inverted comma for abbreviation property for as and cd
    
    ofn=r'define_comp_classes.py'
    ofpn=os.path.join(ofp,ofn)
    
    def clean_names(name): # function to replace certain special characters with underscore; leaves float values alone
        try:
            name=float(name) 
        except:
            pass
        if type(name)==str:
            cname = re.sub('[^0-9a-za-z]+', '_', name)
            cname = cname.replace('halflife','halflife')      
            return(cname)
        return(name)  
    
    
    def clean_props(prop): # function to convert properties to pythonic syntax, 
        hardcode_prop_old='10 ** (-1.5 + 0.4 * self.currentchemical.log10_k_ow) if ( self.currentchemical.log10_k_ow < 3 else 0.5 if (self.currentchemical.log10_k_ow >= 3) and (self.currentchemical.log10_k_ow < 6) else 10 ** (1.2 - 0.25 * self.currentchemical.log10_k_ow) ) if self.bw > 0.1 else 10 ** (-2.6 + 0.5 * self.currentchemical.log10_k_ow) if ( self.currentchemical.log10_k_ow < 5 else 0.8 if (self.currentchemical.log10_k_ow >= 5) and (self.currentchemical.log10_k_ow < 6) else 10 ** (2.9 - 0.5 * self.currentchemical.log10_k_ow) )'
        # hardcode_prop_new='(10 ** (-1.5 + 0.4 * self.currentchemical.log10_k_ow) if ( self.currentchemical.log10_k_ow < 3) else (0.5 if (self.currentchemical.log10_k_ow >= 3) and (self.currentchemical.log10_k_ow < 6) else (10 ** (1.2 - 0.25 * self.currentchemical.log10_k_ow))  if self.bw > 0.1 else (10 ** (-2.6 + 0.5 * self.currentchemical.log10_k_ow) if (self.currentchemical.log10_k_ow < 5) else (0.8 if (self.currentchemical.log10_k_ow >= 5) and (self.currentchemical.log10_k_ow < 6) else (10 ** (2.9 - 0.5 * self.currentchemical.log10_k_ow) )))))'
        hardcode_prop_new='(10 ** (-1.5 + 0.4 * self.currentchemical.log10_k_ow) if ( self.currentchemical.log10_k_ow < 3) else (0.5 if (self.currentchemical.log10_k_ow >= 3) and (self.currentchemical.log10_k_ow < 6) else (10 ** (1.2 - 0.25 * self.currentchemical.log10_k_ow)) ) ) if self.bw > 0.1 else (10 ** (-2.6 + 0.5 * self.currentchemical.log10_k_ow) if (self.currentchemical.log10_k_ow < 5) else (0.8 if (self.currentchemical.log10_k_ow >= 5) and (self.currentchemical.log10_k_ow < 6) else (10 ** (2.9 - 0.5 * self.currentchemical.log10_k_ow) )))'
        prop=prop.replace('(compartment.allowexchange_forother > 0 ? compartment.wetvolumeperarea * containingvolumeelement.area : 0)','compartment.allowexchange_forother > 0 ? compartment.wetvolumeperarea * containingvolumeelement.area : 0') # ternary convertor doesnt handle props enclosed in paranthesis 
        if '?' in prop: # change ternary if then else syntax to pythonic syntax
            prop=ternary2python(prop)
            
        prop=prop.replace('compartment.','self.')
        prop=prop.replace('compartment.','self.')
        prop=prop.replace('ln','log')
        prop=prop.replace('False','False')
        prop=prop.replace('True','True')
        prop=prop.replace('constants','self.constants')
        prop=prop.replace('containingscenario','self.containingscenario')
        prop=prop.replace('withincontainingvolumeelement[abiotic | soil | surface soil].area','self.associated_soil_comp.area')
        prop=prop.replace('containingvolumeelement','self.containingvolumeelement')
        prop=prop.replace('currentchemical','self.currentchemical')
        prop=prop.replace('<unset>','"<unset>"')
        prop=prop.replace('halflife','halflife')
        prop=prop.replace('z_vapor','z_vapor')
        prop=prop.replace('d_purewater','d_purewater')
        prop=prop.replace('fractionmass_vapor','fractionmass_vapor')
        prop=prop.replace('(compartment.allowexchange_forother > 0 ? compartment.wetvolumeperarea * containingvolumeelement.area : 0)','compartment.allowexchange_forother > 0 ? compartment.wetvolumeperarea * containingvolumeelement.area : 0') 
        prop=prop.replace('withincompositecompartment[terrestrial plant | leaf | leaf - deciduous forest].','self.associated_leaf_comp.')
        prop=prop.replace('withincompositecompartment[terrestrial plant | leaf | leaf - coniferous forest].','self.associated_leaf_comp.')
        prop=prop.replace('withincompositecompartment[terrestrial plant | leaf].','self.associated_leaf_comp.')  
        prop=prop.replace('withincompositecompartment[terrestrial plant | leaf | leaf - grasses/herbs].','self.associated_leaf_comp.')
        prop=prop.replace('withincontainingvolumeelement[abiotic | soil | surface soil].area','self.associated_soil_comp.area')
        prop=prop.replace('self.allowexchange_dynamic','wt_av_allowexchange') # Call dynamic allow exchange defined at top of script





        if 'linkedcompartment' in prop:
            prop=linkcomp(prop)
        if 'currentchemical' not in prop and 'chemical.' in prop:
            prop=prop.replace('chemical.','chemical_')
        if 'self.chemical.' in prop:
            prop=prop.replace('self.chemical.','self.chemical_')
#        if 'self.height' in prop:
#            prop=prop.replace('self.height','float(self.containingvolumeelement.height)')
#        if 'self.volume *' in prop:
#            prop=prop.replace('self.volume *','float(self.containingvolumeelement.volume) *')
            
        if 'volumefraction_algae' in prop:
            prop=prop.replace('volumefraction_algae','volumefraction_algae')
        if 'chemical_z_algae' in prop:
            prop=prop.replace('chemical_z_algae','chemical_z_algae')
        if 'fractionsand' in prop:
            prop=prop.replace('fractionsand','fractionsand')

        if 'organiccarboncontent' in prop:
            prop=prop.replace('organiccarboncontent','organiccarboncontent')

        if prop==hardcode_prop_old:
            prop=hardcode_prop_new

### 083022 Testing commenting out these because some self.height and self.volume may be calculated differently from parent volume abiotic element. e.g. stem. not sure of impacts on others.            

        # if 'self.volume *' in prop:
        #     prop=prop.replace('self.volume *','self.containingvolumeelement.volume *')
        # if 'self.volume*' in prop:
        #     prop=prop.replace('self.volume*','self.containingvolumeelement.volume*')

        # if 'self.height' in prop:
        #     prop=prop.replace('self.height','self.containingvolumeelement.height')

    
        return (prop)


       
   
       
    
    df_comp_lib=df_lib.loc[df_lib['objecttype']=='compartment']
    grouped_comp = df_comp_lib.groupby("objectname")



    def hack_func(value,name): # temporary hack -- fix later
        if type(value)!=float and 'max(linked' in value:
            value='1.171E-05'
        if value=='<unset>' and name=='isflowing':
            value='False' 
        if value=='<unset>':
            value='0.01'         
        return(value)
    
#    df_comp_lib['propertyvalue']=df_comp_lib['propertyvalue'].apply(hack_func) # temporary hack -- fix later
    df_comp_lib['propertyvalue']=df_comp_lib.apply(lambda x: hack_func(x['propertyvalue'], x['propertyname']), axis=1)


    required_comps=req.required_compartments # look up list of required algorithms

    
    from numpy import isnan
    with open(ofpn, 'w') as f:  
        f.write('### note: this is an auto generated script' +'\n')        
        f.write('from math import log, log10' + '\n')
        f.write('from numpy import nan, sqrt, exp' + '\n')
 
        f.write('''\

def linkedCompartmentvalue(containingvolumeelement,comp_objects_dict,primary_abiotic,prop_name):
    ve_name=containingvolumeelement.ve_name
    if primary_abiotic==containingvolumeelement.primary_abiotic.replace(' ','_'): # if else is a dirty hack in place of a robust link checking process       
        comp_name=primary_abiotic+'_in_'+ve_name
    else:
        if containingvolumeelement.primary_abiotic=='sediment' and primary_abiotic=='surface_water':
             comp_name='surface_water'+'_in_sw_'+containingvolumeelement.parcel_name    
    val_str='comp_objects_dict["'+comp_name+'"].'+prop_name
    val=eval(val_str)
    return(val)  
    ''')
 

        
        f.write('\n')  # implement a cleaner way of giving comp classes access to met dict (e.g. make inputs or dict_inputs a parameter in comp class definition? ORM approach may supercede all this)
        for k,v in inputs['met_dict'].items():
            f.write(k+'='+str(v)+'\n')
        f.write('\n')               
    
# method decorator approach 

        for index,group in enumerate(grouped_comp.groups): # loop over compartments
            if group not in required_comps:
                continue

            comp_name=clean_names(group)
            f.write('\n'+'class '+str(comp_name)+':'+'\n' +\
                    '\t'+\
                    'def __init__(self,constants,containingscenario,currentchemical,containingvolumeelement,comp_objects_dict):\n\t\t'+\
                                    'self.containingscenario=containingscenario\n\t\t'+\
                                    'self.currentchemical=currentchemical\n\t\t'+\
                                    'self.constants=constants\n\t\t'+\
                                    'self.containingvolumeelement=containingvolumeelement\n\t\t'+\
                                    'self.comp_objects_dict=comp_objects_dict')
#            comp_props=list(grouped_comp.get_group(group)['propertyname'].unique()) # unique properties
    
            all_props=list(grouped_comp.get_group(group)['propertyname']) # all property names 
            all_vals=list(grouped_comp.get_group(group)['propertyvalue']) # all property values 
            all_types=list(grouped_comp.get_group(group)['datatype']) # # all property types 

            if group=="advection sink":                 # hack to fix default category name in advection sinks which is set to air in library
                cat_index=all_props.index('category') # index of category property
                del all_props[cat_index]
                del all_vals[cat_index]
                del all_types[cat_index]
            
            c_p=tuple(zip(all_props,all_vals,all_types))
    
            constant_props=[] # properties that depend on constant number     
            bool_props=[] # boolean properties
            non_formula_props=[] # non formula props
            formula_props=[] # list of formula properties that are formulaic

            for t in c_p:
                if (t[2]=='category property')|(t[2]=='text property'):
                    non_formula_props.append(t[0])            
                if t[2]=='constant real number property':
                    constant_props.append(t[0])
                if t[2]=='True/False (boolean) property':
                     bool_props.append(t[0])                
                if t[2]=='formula':
                    formula_props.append(t[0])

            for prop in set(all_props):
                df_prop_val=grouped_comp.get_group(group).loc[grouped_comp.get_group(group)['propertyname']==prop]# data frame of property values (multi line if chemical specific)
                chems=list(df_prop_val['specificchemical'])
                prop_cl=clean_props(prop)


                if len(chems)==1 and type(chems[0])== float:#isnan(chems[0]): # if only nan:
                    ch_name='nan'
                    prop_val=df_prop_val['propertyvalue'].values[0]
                    try:
                        prop_val=clean_props(prop_val)    
                    except:
                        pass
                    if prop=="sedimentresuspensionvelocity": # temp hack to deal with sediment resuspension issue 
                        prop_val="9.64763202734353e-05"
                        prop_val="6.69E-5"

                    if prop=="calculatewetdepinterceptionfraction": # temp hack to deal with CalculateWetDepInterceptionFraction (false in library but read in as true in Foundries run) 
                        prop_val="False"

                    if 'coniferous' in group and 'wt_av_allowexchange' in prop_val: # hack to deal with coniferous plants having allow exchange of 1
                        prop_val=prop_val.replace('wt_av_allowexchange','1')

                    if 'coniferous' not in group and 'litterfallrate' in prop: # hack to deal with non coniferous plants needing to be assigned wt_av_litterfallrate
                        prop_val='wt_av_litterfallrate'

                        
#                    if type(prop_val)==float or is_number(prop_val):
#                        if isnan(prop_val):
#                            prop_val='nan'
                    if (prop in constant_props): 
                        #print (prop_val)
                        f.write('\n\t'+\
                            '_'+prop+'='+prop_val +'\n\t' +\
                            '@property'+'\n\t' +\
                            'def '+prop+'(self):'+'\n\t\t' +\
                            'return self._'+prop+'\n\t'+\
                            '@'+prop+'.setter''\n\t' +\
                            'def '+prop+'(self,value):'+'\n\t\t' +\
                            'self._'+prop+'=value\n')             
                            
                    # if (prop in bool_props): 
                    #     f.write('\n\t'+\
                    #             '@property'+'\n\t' +\
                    #             'def '+prop+'(self):'+'\n\t\t' +\
                    #             'return ('+prop_val+')\n\t')                 

                    if (prop in bool_props): 
                        f.write('\n\t'+\
                            '_'+prop+'='+prop_val +'\n\t' +\
                            '@property'+'\n\t' +\
                            'def '+prop+'(self):'+'\n\t\t' +\
                            'return self._'+prop+'\n\t'+\
                            '@'+prop+'.setter''\n\t' +\
                            'def '+prop+'(self,value):'+'\n\t\t' +\
                            'self._'+prop+'=value\n')             

                        

                    if (prop in non_formula_props): 
                        if type(prop_val)==float:
                            prop_val='nan'
                        f.write('\n\t'+\
                                '@property'+'\n\t' +\
                                'def '+prop+'(self):'+'\n\t\t' +\
                                'return ("'+prop_val+'")\n\t')     

                    if (prop in formula_props): 
                        f.write('\n\t'+\
                                '@property'+'\n\t' +\
                                'def '+prop+'(self):'+'\n\t\t' +\
                                'return ('+prop_val+')\n\t')   


                # else: # multiple chems
                #     schems=[x for x in chems if x in inputs['simulation_chemicals']] #simulation chems only
                #     f.write('\n\t'+\
                #         '@property'+'\n\t' +\
                #         'def '+prop_cl+'(self):'+'\n\t\t' +\
                #         'cdict={}')
                #     for chem in schems:
                #         if type(chem)==float:
                #             ch_name='nan'
                #             prop_val=df_prop_val[df_prop_val['specificchemical'].isnull()]['propertyvalue'].values[0]
                #         else:
                #             prop_val=df_prop_val.loc[df_prop_val['specificchemical']==chem,'propertyvalue'].values[0]             
                #             ch_name=clean_chem_names(chem)
                #         if (prop not in non_formula_props) and (prop not in bool_props):
                #             try:
                #                 prop_val=clean_props(prop_val)    
                #             except:
                #                 pass
                #         ### the try except is because it tries to evaluate each chemical even when it is not the current chemical with the method decorator approach
                #         f.write('\n\t\t'+\
                #                 'try:''\n\t\t\t'+\
                #                 'cdict["'+ch_name+'"]='+prop_val+'\n\t\t'+\
                #                 'except:''\n\t\t\t'+\
                #                 'cdict["'+ch_name+'"]=nan'+'\n\t\t')
                #     f.write('\n\t\t'+\
                #             'return cdict')
                #     f.write('\n')
                #     cpname='chemical_'+prop_cl
                #     cprop='self.'+prop_cl+'[self.currentchemical.name]'
                #     f.write('\n\t'+\
                #         '@property'+'\n\t' +\
                #         'def '+cpname+'(self):'+'\n\t\t' +\
                #         'return '+cprop)



                else: # multiple chems # condition is a dirty hack for applying values in other properties file. will not work if file includes other types of props than in the condition statement.
                    # condition= ('soil' in group) and (prop_cl=='methylationrate' or prop_cl=='demethylationrate' or prop_cl=='reductionrate' or prop_cl=='oxidationrate')
                    condition= ('soil' in group) and (prop_cl=='methylationrate' or prop_cl=='demethylationrate' or prop_cl=='reductionrate' or prop_cl=='oxidationrate')

                    if not condition:
                        schems=[x for x in chems if x in inputs['simulation_chemicals']] #simulation chems only
                        f.write('\n\n\t'+\
                            '@property'+'\n\t' +\
                            'def '+prop_cl+'(self):'+'\n\t\t' +\
                            'cdict={}')
                        for chem in schems:
                            if type(chem)==float:
                                ch_name='nan'
                                prop_val=df_prop_val[df_prop_val['specificchemical'].isnull()]['propertyvalue'].values[0]
                            else:
                                prop_val=df_prop_val.loc[df_prop_val['specificchemical']==chem,'propertyvalue'].values[0]             
                                ch_name=clean_chem_names(chem)
                            if (prop not in non_formula_props) and (prop not in bool_props):
                                try:
                                    prop_val=clean_props(prop_val)    
                                except:
                                    pass
                            ### the try except is because it tries to evaluate each chemical even when it is not the current chemical with the method decorator approach
                            f.write('\n\t\t'+\
                                    'try:''\n\t\t\t'+\
                                    'cdict["'+ch_name+'"]='+prop_val+'\n\t\t'+\
                                    'except:''\n\t\t\t'+\
                                    'cdict["'+ch_name+'"]=nan'+'\n\t\t')
                        f.write('\n\t\t'+\
                                'return cdict')
                        f.write('\n')
                        cpname='chemical_'+prop_cl
                        cprop='self.'+prop_cl+'[self.currentchemical.name]'
                        f.write('\n\t'+\
                            '@property'+'\n\t' +\
                            'def '+cpname+'(self):'+'\n\t\t' +\
                            'return '+cprop +'\n')
                            



# ## comment out -- do not create certain properties of soil class that will be directly created in the instance                                        
#                     if condition:
#                         schems=[x for x in chems if x in inputs['simulation_chemicals']] #simulation chems only
#                         f.write('\n\n\t'+\
#                                 prop_cl+'_cdict'+'={}')
#                         for chem in schems:
#                             if type(chem)==float:
#                                 ch_name='nan'
#                                 prop_val=df_prop_val[df_prop_val['specificchemical'].isnull()]['propertyvalue'].values[0]
#                             else:
#                                 prop_val=df_prop_val.loc[df_prop_val['specificchemical']==chem,'propertyvalue'].values[0]             
#                                 ch_name=clean_chem_names(chem)
#                             if (prop not in non_formula_props) and (prop not in bool_props):
#                                 try:
#                                     prop_val=clean_props(prop_val)    
#                                 except:
#                                     pass
#                             ### the try except is because it tries to evaluate each chemical even when it is not the current chemical with the method decorator approach
#                             f.write('\n\t'+\
#                                     'try:''\n\t\t'+\
#                                     prop_cl+'_cdict["'+ch_name+'"]='+prop_val+'\n\t'+\
#                                     'except:''\n\t\t'+\
#                                     prop_cl+'_cdict["'+ch_name+'"]=nan'+'\n\t')

#                         f.write('\n')

#                         f.write('\n\t'+\
#                         '@property'+'\n\t' +\
#                         'def '+prop_cl+'(self):'+'\n\t\t' +\
#                         'return self.'+prop_cl+'_cdict')

#                         cpname='chemical_'+prop_cl
#                         cprop='self.'+prop_cl+'[self.currentchemical.name]'
#                         f.write('\n\t'+\
#                             '@property'+'\n\t' +\
#                             'def '+cpname+'(self):'+'\n\t\t' +\
#                             'return '+cprop)


                    if condition:
                        
                        schems=[x for x in chems if x in inputs['simulation_chemicals']] #simulation chems only
                        f.write('\n\t@property')+\
                        f.write('\n\t'+\
                            'def '+prop_cl+'(self):'+'\n\t\t'+\
                                'if not hasattr(self,"_'+prop_cl+'"):\n\t\t\t'+\
                                    'self._'+prop_cl+'={}'+'\n\t\t\t')

                            
                                            
                                    

                        for chem in schems: # there is only one chemical for these properties or this wouldnt work
                            if type(chem)==float:
                                ch_name='nan'
                                prop_val=df_prop_val[df_prop_val['specificchemical'].isnull()]['propertyvalue'].values[0]
                            else:
                                prop_val=df_prop_val.loc[df_prop_val['specificchemical']==chem,'propertyvalue'].values[0]             
                                ch_name=clean_chem_names(chem)
                            if (prop not in non_formula_props) and (prop not in bool_props):
                                try:
                                    prop_val=clean_props(prop_val)    
                                except:
                                    pass
                            ### the try except is because it tries to evaluate each chemical even when it is not the current chemical with the method decorator approach
                            f.write('try:'+'\n\t\t\t\t'+\
                                    'self._'+prop_cl+'["'+ch_name+'"]='+prop_val+'\n\t\t\t'+\
                                    'except:'+'\n\t\t\t\t'+\
                                    'self._'+prop_cl+'["'+ch_name+'"]=nan'+'\n\t\t'+\
                                    'return self._'+prop_cl)
 
                                
                    cpname='chemical_'+prop_cl
                    cprop='self.'+prop_cl+'[self.currentchemical.name]'
                    f.write('\n\t'+\
                        '@property'+'\n\t' +\
                        'def '+cpname+'(self):'+'\n\t\t' +\
                        'return '+cprop +'\n')


    
                # else: # multiple chems
                #     schems=[x for x in chems if x in inputs['simulation_chemicals']] #simulation chems only
                #     f.write('\n\t@property')+\
                #     f.write('\n\t'+\
                #         'def _'+prop_cl+'(self):'+'\n\t\t')
                #     f.write('_cdict={}')    
                #     for chem in schems:
                #         if type(chem)==float:
                #             ch_name='nan'
                #             prop_val=df_prop_val[df_prop_val['specificchemical'].isnull()]['propertyvalue'].values[0]
                #         else:
                #             prop_val=df_prop_val.loc[df_prop_val['specificchemical']==chem,'propertyvalue'].values[0]             
                #             ch_name=clean_chem_names(chem)
                #         if (prop not in non_formula_props) and (prop not in bool_props):
                #             try:
                #                 prop_val=clean_props(prop_val)    
                #             except:
                #                 pass
                #         ### the try except is because it tries to evaluate each chemical even when it is not the current chemical with the method decorator approach
                #         f.write('\n\t\t'+\
                #                 'try:'+'\n\t\t\t'+\
                #                 '_cdict["'+ch_name+'"]='+prop_val+'\n\t\t'+\
                #                 'except:'+'\n\t\t\t'+\
                #                 '_cdict["'+ch_name+'"]=nan')
                #     f.write('\n\t\t'+'return(_cdict)')    
                #     f.write('\n\t'+\
                #         '@property'+'\n\t' +\
                #         'def '+prop_cl+'(self):'+'\n\t\t' +\
                #             'if not hasattr(self, _'+prop_cl+':\n\t\t\t'+\
                #                 'self._'+prop_cl+'={}')
                #     f.write('\n\t'+\
                #             '@'+prop_cl+'.setter'+'\n\t' +\
                #             'def '+prop_cl+'(self,value):'+'\n\t\t' +\
                #             'self._'+prop_cl+'=value\n\t') 
                #     cpname='chemical_'+prop_cl
                #     cprop='self.'+prop_cl+'[self.currentchemical.name]'
                #     f.write('\n\t'+\
                #         '@property'+'\n\t' +\
                #         'def '+cpname+'(self):'+'\n\t\t' +\
                #         'return '+cprop)
        
        
    f.close()
    
    return(df_lib,df_alg,df_alg_mat,df_chem)  
    
if __name__ == '__main__':
    df_lib,df_alg,df_alg_mat,df_chem=process_master_library(inputs)


    