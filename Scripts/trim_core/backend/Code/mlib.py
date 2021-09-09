# -*- coding: utf-8 -*-
"""
Created on Mon Apr  5 14:41:50 2021
@author: 13963

This module reads in the legacy TRIM.FaTE master library in csv format
It creates dataframes to store the whole library, algorithms, matrix of algorithm applicability, and chemicals
It writes scripts to define algorithm,  chemical,  and generic compartment classes, specifically: define_algs.py, define_chem_classes.py, define_comp_classes.py

"""

import pandas as pd
import os
import re
from numpy import nan
#import required_elements as req
import required_elements_temp as req
from util_functions import * 

def process_master_library(inputs):

    ifp=inputs['path_inputs']
    ifn=inputs['master_library_file']
    
    ifpn=os.path.join(ifp,ifn)
    
    header=pd.read_csv(ifpn,sep=';',nrows=0,encoding='windows-1252').columns
    
    df_lib=pd.read_csv(ifpn,sep=';',names=header,skiprows=[0],encoding='windows-1252') # read library into dataframe
    
    ############ WRITE PYTHON SCRIPT TO DEFINE ALGORITHM CLASSES 
    
    df_alg=df_lib.loc[df_lib['ObjectType']=='Algorithm']
    grouped_alg = df_alg.groupby("ObjectName")
    
    
    ofp=inputs['path_code']
    ofn=r'define_algs.py'
    ofpn=os.path.join(ofp,ofn)
    
    
    def clean_names(name): # function to replace certain special characters with underscore; leaves float values alone
        try:
            name=float(name) 
        except:
            pass
        if type(name)==str:
            cname = re.sub('[^0-9a-zA-Z]+', '_', name)
            cname=cname.strip('_')
            return(cname)            
        return(name)  
    
    def clean_props(prop): # function to convert properties to Pythonic syntax, 
        if '?' in prop: # change ternary if then else syntax to Pythonic syntax
            cond=prop.split('?')[0].strip()
            v1=prop.split('?')[1].strip().split(':')[0].strip()
            v2=prop.split('?')[1].strip().split(':')[1].strip()
            prop= v1+' if ' +cond.replace('&&',' and ')+' else ' +v2
        prop=prop.replace('Constants','self.Constants')
        prop=prop.replace('containingScenario','self.containingScenario')
        prop=prop.replace('ReceivingCompartment','self.ReceivingCompartment')
        prop=prop.replace('SendingCompartment','self.SendingCompartment')
        prop=prop.replace('Sendingcompartment','self.SendingCompartment')
        prop=prop.replace('Algorithm.','self.')
        prop=prop.replace('Chemical.','Chemical_')
        prop=prop.replace('Z_total','Z_Total')
        prop=prop.replace ('!',' not ')
        prop=prop.replace('SendingChemical_','currentChemical.')
        prop=prop.replace('MolecularWeight','molecularWeight')
        
#        prop-prop.replace('self.Sendingcompartment.Flushes_per_year','self.SendingCompartment.Flushes_per_year')
        if 'self.ReaerationVelocity_OwensFormula' in prop: # temporary till ternary convertor
            prop='self.ReaerationVelocity_OwensFormula * self.RatioofVolatilizationRatetoReaerationRate'

        if 'TheLink.InterfacialArea' in prop: # replace TheLink interfacial area custom function with Python function
            prop=prop.replace('TheLink.InterfacialArea','check_neighbor(self.SendingCompartment,self.ReceivingCompartment,self.dict_inputs).is_neighbor()[1]')           
        if 'TheLink.FractionSpecificcompartmentDiet' in prop: # replace TheLink.FractionSpecificcompartmentDiet with 1. I believe this okay but check UG.
            prop=prop.replace('TheLink.FractionSpecificcompartmentDiet','1')          
        return (prop)
   
    required_algs=req.required_algorithms # look up list of required algorithms
    
    with open(ofpn, 'w') as f:  
        f.write('### Note: This is an auto generated script' +'\n')        
        f.write('from find_neighbors import *' +'\n')
        f.write('from numpy import sqrt' +'\n')
        
        for index,group in enumerate(grouped_alg.groups):
            if group not in required_algs:
                continue
            alg_name=clean_names(group)
            alg_props=list(grouped_alg.get_group(group)['PropertyName'].unique())
            tf=grouped_alg.get_group(group).loc[grouped_alg.get_group(group)['PropertyName']=='transferFactor']['PropertyValue'].values[0]#.replace('SendingCompartment','self.SendingCompartment').replace('ReceivingCompartment','self.ReceivingCompartment')
            tf=clean_props(tf)
    
#            if 'TheLink.InterfacialArea' not in tf and 'TheLink.FractionSpecificcompartmentDiet' not in tf and 'TheLink' in tf: #these need fixes
#                print (tf)
#                print ()
    

            
            f.write('class '+str(alg_name)+':'+'\n' +\
                    '\t'+\
                    'def __init__(self, Constants,containingScenario,currentChemical,SendingCompartment, ReceivingCompartment,dict_inputs):\n\t\t'+\
                    'self.Name='+"'"+group+"'"+'\n\t\t'+\
                    'self.Constants=Constants\n\t\t'+\
                    'self.containingScenario=containingScenario\n\t\t'+\
                    'self.currentChemical=currentChemical\n\t\t'+\
                    'self.SendingCompartment=SendingCompartment\n\t\t'+\
                    'self.ReceivingCompartment=ReceivingCompartment\n\t\t'+\
                    'self.category='+"'"+grouped_alg.get_group(group).loc[grouped_alg.get_group(group)['PropertyName']=='category']['PropertyValue'].values[0]+"'"+'\n\t\t'
                    'self.chemicalCategory='+"'"+grouped_alg.get_group(group).loc[grouped_alg.get_group(group)['PropertyName']=='chemicalCategory']['PropertyValue'].values[0]+"'"+'\n\t\t'
                    'self.doesTransformChemical='+"'"+grouped_alg.get_group(group).loc[grouped_alg.get_group(group)['PropertyName']=='doesTransformChemical']['PropertyValue'].values[0]+"'"+'\n\t\t'
                    'self.TransportChemical='+"'"+grouped_alg.get_group(group).loc[grouped_alg.get_group(group)['PropertyName']=='doesTransportChemical']['PropertyValue'].values[0]+"'"+'\n\t\t'
                    'self.enabled='+"'"+grouped_alg.get_group(group).loc[grouped_alg.get_group(group)['PropertyName']=='enabled']['PropertyValue'].values[0]+"'"+'\n\t\t'
                    'self.isDefaultForCategory='+"'"+grouped_alg.get_group(group).loc[grouped_alg.get_group(group)['PropertyName']=='isDefaultForCategory']['PropertyValue'].values[0]+"'"+'\n\t\t'
                    'self.mate='+"'"+grouped_alg.get_group(group).loc[grouped_alg.get_group(group)['PropertyName']=='mate']['PropertyValue'].values[0]+"'"+'\n\t\t'
                    'self.receivingChemicalName='+"'"+grouped_alg.get_group(group).loc[grouped_alg.get_group(group)['PropertyName']=='receivingChemicalName']['PropertyValue'].values[0]+"'"+'\n\t\t'
                    'self.receivingCompartmentCategory='+"'"+grouped_alg.get_group(group).loc[grouped_alg.get_group(group)['PropertyName']=='receivingCompartmentCategory']['PropertyValue'].values[0]+"'"+'\n\t\t'
                    'self.sendingCompartmentCategory='+"'"+grouped_alg.get_group(group).loc[grouped_alg.get_group(group)['PropertyName']=='sendingCompartmentCategory']['PropertyValue'].values[0]+"'"+'\n\t\t'
                    'self.sendingChemicalName='+"'"+grouped_alg.get_group(group).loc[grouped_alg.get_group(group)['PropertyName']=='sendingChemicalName']['PropertyValue'].values[0]+"'"+'\n\t\t'
                    'self.dict_inputs=dict_inputs'+'\n\t\t')
                    
            residual_props=set(alg_props)-set(['category','chemicalCategory','doesTransformChemical','doesTransportChemical','enabled','isDefaultForCategory','mate','receivingChemicalName','receivingCompartmentCategory','sendingCompartmentCategory','sendingChemicalName','transferFactor'])

            indep_rp=[] # initialize list of independent residual properties
            dep_rp_1=[] # initialize list of dependent residual properties that depend on independent residual properties
            dep_rp_2=[] # initialize list of dependent residual properties that depend on other dependent residual properties
            
            
            rp_tup=[] # lst of tuples of (residual prop name, residual prop value)
            for prop in residual_props:
                prop_val=grouped_alg.get_group(group).loc[grouped_alg.get_group(group)['PropertyName']==prop]['PropertyValue'].values[0] #property value
                ptup=(prop,prop_val)
                rp_tup.append(ptup)
            
            for ptup in rp_tup: # loop over tuples of residual properties
                indep=True
                for rp in residual_props:
                    if rp in ptup[1]:
                       indep=False # if a residual property value refers to another residual property it is not independnet
                       break
                if indep:
                    indep_rp.append(ptup[0])
            dep_rp=list(set(residual_props)-set(indep_rp)) # dependent residual properties
            
            for drp in dep_rp: # loop over dependent properties
                dep_val=grouped_alg.get_group(group).loc[grouped_alg.get_group(group)['PropertyName']==drp]['PropertyValue'].values[0] #property value
                for pname in dep_rp: # loop again over dependent properties list
                    if pname in dep_val: # if any dep prop in dep_val, it is a class 2 dependent property
                        dep_rp_2.append(drp)
                        break
            dep_rp_1=set(dep_rp)-set(dep_rp_2)            
         
                        

            for prop in indep_rp:
                prop_val=grouped_alg.get_group(group).loc[grouped_alg.get_group(group)['PropertyName']==prop]['PropertyValue'].values[0] #property value
                prop_val=clean_props(prop_val)
                if prop=='compartmentRelationship':
                    f.write('\n\t\t'
                            'self.'+prop+'='+"'"+prop_val+"'")                
                else:
                    f.write('\n\t\t'
                            'self.'+prop+'='+prop_val)                
            f.write('\n')    

            for prop in dep_rp_1:
                prop_val=grouped_alg.get_group(group).loc[grouped_alg.get_group(group)['PropertyName']==prop]['PropertyValue'].values[0] #property value
                prop_val=clean_props(prop_val)
                if prop=='compartmentRelationship':
                    f.write('\n\t\t'
                            'self.'+prop+'='+"'"+prop_val+"'")                
                else:
                    f.write('\n\t\t'
                            'self.'+prop+'='+prop_val)                
            f.write('\n')    

            for prop in sorted(list(dep_rp_2)):
                prop_val=grouped_alg.get_group(group).loc[grouped_alg.get_group(group)['PropertyName']==prop]['PropertyValue'].values[0] #property value
                prop_val=clean_props(prop_val)
                if prop=='compartmentRelationship':
                    f.write('\n\t\t'
                            'self.'+prop+'='+"'"+prop_val+"'")                
                else:
                    f.write('\n\t\t'
                            'self.'+prop+'='+prop_val)                
            f.write('\n\t\t')    

            f.write('try: \n\t\t\t' +\
                    'self.transferFactor='+ tf +'\n\t\t'+\
                    'except: \n\t\t\t'+\
                    'self.transferFactor="TF Computation Error"')                

            f.write('\n\n')    
   
        
    ########### CREATE MATRIX OF ALGORITHM APPLICABILITY i.e. which algorithms apply given a receiving compartment and a sending compartment
    
    alg_mat=[]
            
    for index,group in enumerate(grouped_alg.groups):    
        if group not in required_algs:
            continue    
        
        alg_name=clean_names(group)    
        category=grouped_alg.get_group(group).loc[grouped_alg.get_group(group)['PropertyName']=='category']['PropertyValue'].values[0]
        chemical_category=grouped_alg.get_group(group).loc[grouped_alg.get_group(group)['PropertyName']=='chemicalCategory']['PropertyValue'].values[0]
        enabled=grouped_alg.get_group(group).loc[grouped_alg.get_group(group)['PropertyName']=='enabled']['PropertyValue'].values[0]
        isDefaultForCategory=grouped_alg.get_group(group).loc[grouped_alg.get_group(group)['PropertyName']=='isDefaultForCategory']['PropertyValue'].values[0]
        receivingChemicalName=grouped_alg.get_group(group).loc[grouped_alg.get_group(group)['PropertyName']=='receivingChemicalName']['PropertyValue'].values[0]
        receivingCompartmentCategory=grouped_alg.get_group(group).loc[grouped_alg.get_group(group)['PropertyName']=='receivingCompartmentCategory']['PropertyValue'].values[0]
        sendingCompartmentCategory=grouped_alg.get_group(group).loc[grouped_alg.get_group(group)['PropertyName']=='sendingCompartmentCategory']['PropertyValue'].values[0]
        sendingChemicalName=grouped_alg.get_group(group).loc[grouped_alg.get_group(group)['PropertyName']=='sendingChemicalName']['PropertyValue'].values[0]
        alg_mat.append((index,group,alg_name,category,chemical_category,enabled,isDefaultForCategory,receivingChemicalName,receivingCompartmentCategory,sendingCompartmentCategory,sendingChemicalName))
    
    cols=['index','group','Alg_Name_New','category','chemical_category','enabled','isDefaultForCategory','receivingChemicalName','receivingCompartmentCategory','sendingCompartmentCategory','sendingChemicalName']   
    df_alg_mat=pd.DataFrame(alg_mat,columns=cols)
    
       
    
    
    #### ############ WRITE PYTHON SCRIPT TO DEFINE CHEMICAL CLASSES
    
    ofn=r'define_chem_classes.py'
    ofpn=os.path.join(ofp,ofn)
    
    def clean_names(name): # function to replace certain special characters with underscore; leaves float values alone
        try:
            name=float(name) 
        except:
            pass
        if type(name)==str:
            cname = 'Chem_'+re.sub('[^0-9a-zA-Z]+', '_', name)
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
    
    df_chem=df_lib.loc[df_lib['ObjectType']=='Chemical']
    grouped_chem = df_chem.groupby("ObjectName")
    
    
    desired_order=['Original_Chemical_Name','CAS','category','D_pureair','D_pureair_m2_s','D_purewater','D_purewater_m2_per_s','doesTransform','enabled','HenryLawConstant','H_over_R_T','AirWaterPartitionCoefficient','K_ow','K_OA','K_oc','log10_K_OA','log10_K_ow','MeltingPoint','molecularWeight','ReferenceBird_BodyWeight','ReferenceBird_EliminationRate','ReferenceBird_GeneralDegradationRate','ReferenceMammal_BodyWeight','ReferenceMammal_EliminationRate','ReferenceMammal_GeneralDegradationRate','Z_pureair','Z_purewater']
    formula_props=['D_pureair','D_pureair_m2_s','D_purewater','D_purewater_m2_per_s','HenryLawConstant','H_over_R_T','AirWaterPartitionCoefficient','K_ow','K_OA','K_oc','log10_K_OA','log10_K_ow','MeltingPoint','molecularWeight','ReferenceBird_BodyWeight','ReferenceBird_EliminationRate','ReferenceBird_GeneralDegradationRate','ReferenceMammal_BodyWeight','ReferenceMammal_EliminationRate','ReferenceMammal_GeneralDegradationRate','Z_pureair','Z_purewater','VaporWashoutRatio','molesOfReportingChemicalPerMolesOfThisChemical','reportingChemicalMW']
    
    chem_dict={}
    sim_chem_list=inputs['simulation_Chemicals']
    sim_chem_list_clean=[clean_chem_names(x) for x in sim_chem_list]
    
    with open(ofpn, 'w') as f:  
        f.write('### Note: This is an auto generated script' +'\n')        
        f.write('''\

from math import log
from constants import *
from define_scenario import *
from define_attributes_props import *

''')

        
        for index,group in enumerate(grouped_chem.groups):
            chem_name=clean_chem_names(group) # for use as object name
            if chem_name not in sim_chem_list_clean:
                continue
            chem_dict[index]=chem_name
            chem_name_strip=chem_name.strip('_') # for use as cleaned original chem name
            chem_props=list(grouped_chem.get_group(group)['PropertyName'].unique())
            chem_props_ordered=[x for x in desired_order if x in chem_props]
            chem_props_residual=list(set(chem_props)-set(chem_props_ordered)) # residual chem props not in ordered list
            
            f.write('class '+str(chem_name)+':'+'\n' +\
                    '\t'+\
                    'def __init__(self,Constants,containingScenario):\n\t\t'+\
                    'self.containingScenario=containingScenario\n\t\t'+\
                    'self.Constants=Constants\n\t\t'+\
                    'self.Name='+"'"+str(chem_name_strip)+"'")
            for prop in chem_props_ordered:
                prop_val=grouped_chem.get_group(group).loc[grouped_chem.get_group(group)['PropertyName']==prop]['PropertyValue'].values[0] #property value
                if prop in formula_props:
                    prop_val=clean_props(prop_val)
                    f.write('\n\t\t'
                            'self.'+prop+'='+prop_val)                
                else:
                    f.write('\n\t\t'
                            'self.'+prop+'='+"'"+prop_val+"'")                
            for prop in chem_props_residual:
                prop_val=grouped_chem.get_group(group).loc[grouped_chem.get_group(group)['PropertyName']==prop]['PropertyValue'].values[0] #property value
                if prop in formula_props:
                    prop_val=clean_props(prop_val)
                    f.write('\n\t\t'
                            'self.'+prop+'='+prop_val)                
                else:
                    f.write('\n\t\t'
                            'self.'+prop+'='+"'"+prop_val+"'")                
  
            f.write('\n\n')    

        f.write('chem_objects_dict={}'+'\n')   
        for k,v in chem_dict.items():
            if v not in sim_chem_list_clean:
                continue
            f.write(str(v)+'='+str(v)+'(Constants,containingScenario)'+'\n')
            f.write('chem_objects_dict['+'"'+str(v)+'"'+']='+str(v)+'\n')
        
    f.close()    
    
    
    
    #### ############ WRITE PYTHON SCRIPT TO DEFINE GENERAL COMPARTMENT CLASSES
    
    #Note: problem with multiple if then statements in Benthic Carnivore, FishTransferEfficiency
    # problem with double inverted comma for abbreviation property for As and Cd
    
    ofn=r'define_comp_classes.py'
    ofpn=os.path.join(ofp,ofn)
    
    def clean_names(name): # function to replace certain special characters with underscore; leaves float values alone
        try:
            name=float(name) 
        except:
            pass
        if type(name)==str:
            cname = re.sub('[^0-9a-zA-Z]+', '_', name)
            cname = cname.replace('Halflife','HalfLife')      
            return(cname)
        return(name)  
    
    
    def clean_props(prop): # function to convert properties to Pythonic syntax, 
        if '?' in prop: # change Java if then else syntax to Pythonic syntax
            cond=prop.split('?')[0].strip()
            v1=prop.split('?')[1].strip().split(':')[0].strip()
            v2=prop.split('?')[1].strip().split(':')[1].strip()
            prop= v1+' if ' +cond.replace('&&',' and ')+' else ' +v2
        prop=prop.replace('compartment.','self.')
        prop=prop.replace('Compartment.','self.')
        prop=prop.replace('ln','log')
        prop=prop.replace('false','False')
        prop=prop.replace('true','True')
        prop=prop.replace('Constants','self.Constants')
        prop=prop.replace('containingScenario','self.containingScenario')
        prop=prop.replace('currentChemical','self.currentChemical')
        prop=prop.replace('<Unset>','"<Unset>"')
        prop=prop.replace('Halflife','HalfLife')
        prop=prop.replace('Z_vapor','Z_Vapor')
        prop=prop.replace('D_Purewater','D_purewater')
        prop=prop.replace('FractionMass_Vapor','FractionMass_vapor')
        if 'currentChemical' not in prop and 'Chemical.' in prop:
            prop=prop.replace('Chemical.','Chemical_')
        if 'self.Chemical.' in prop:
            prop=prop.replace('self.Chemical.','self.Chemical_')
#        if 'self.Height' in prop:
#            prop=prop.replace('self.Height','float(self.containingVolumeElement.Height)')
#        if 'self.Volume *' in prop:
#            prop=prop.replace('self.Volume *','float(self.containingVolumeElement.Volume) *')
            
        if 'VolumeFraction_algae' in prop:
            prop=prop.replace('VolumeFraction_algae','VolumeFraction_Algae')
        if 'Chemical_Z_algae' in prop:
            prop=prop.replace('Chemical_Z_algae','Chemical_Z_Algae')
        if 'self.Volume *' in prop:
            prop=prop.replace('self.Volume *','self.containingVolumeElement.Volume *')
        if 'self.Volume*' in prop:
            prop=prop.replace('self.Volume*','self.containingVolumeElement.Volume*')

        if 'self.Height' in prop:
            prop=prop.replace('self.Height','self.containingVolumeElement.Height')

    
        return (prop)
    
    df_comp_lib=df_lib.loc[df_lib['ObjectType']=='Compartment']
    grouped_comp = df_comp_lib.groupby("ObjectName")

#    def hack_func(value): # temporary hack -- fix later
#        if type(value)!=float and 'Max(linked' in value:
#            value='0.01'
#        if type(value)!=float and 'pH' in value:
#            value='0.01'
#        if type(value)!=float and 'Chloride' in value:
#            value='0.01'
#        if value=='<Unset>':
#            value='0.01' 
#        if type(value)!=float and 'WaterTemperature_C' in value:
#            value='25'


    def hack_func(value,name): # temporary hack -- fix later
        if type(value)!=float and 'Max(linked' in value:
            value='0.01'
        if type(value)!=float and 'pH' in value:
            value='0.01'
        if type(value)!=float and 'Chloride' in value:
            value='0.01'
        if value=='<Unset>' and name=='isFlowing':
            value='False' 
        if value=='<Unset>':
            value='0.01' 
        if name=='WaterViscosity':
            value='1.197E-02' 

        if type(value)!=float and 'WaterTemperature_C' in value:
            value='25'


        
        return(value)
    
#    df_comp_lib['PropertyValue']=df_comp_lib['PropertyValue'].apply(hack_func) # temporary hack -- fix later
    df_comp_lib['PropertyValue']=df_comp_lib.apply(lambda x: hack_func(x['PropertyValue'], x['PropertyName']), axis=1)


    required_comps=req.required_compartments # look up list of required algorithms

    
    from numpy import isnan
    with open(ofpn, 'w') as f:  
        f.write('### Note: This is an auto generated script' +'\n')        
        f.write('from math import log' + '\n')
        f.write('from numpy import nan' + '\n')
        f.write('from numpy import sqrt' + '\n')
        f.write('''
    
def Function_ChemicalTransferEfficiencyinFish(BW,log10_K_ow):
    if BW > 0.1:
        if log10_K_ow < 3:
            r=10 ** (-1.5 + 0.4 * log10_K_ow)
        else:
            if (log10_K_ow >= 3) and (log10_K_ow < 6):
               r=0.5 
            else:
                r=10 ** (1.2 - 0.25 * log10_K_ow) 
    else:
        if log10_K_ow < 5:
            r=10 ** (-2.6 + 0.5 * log10_K_ow)
        else:
            if (log10_K_ow >= 5) and (log10_K_ow < 6):
               r=0.8 
            else:
                r=10 ** (2.9 - 0.5 * log10_K_ow) 
    return(r)
        
''')
            
        for index,group in enumerate(grouped_comp.groups): # loop over compartments
            if group not in required_comps:
                continue

            comp_name=clean_names(group)
#            print (group, '||',comp_name)
            # print (index,comp_name)
    #        comp_props_ordered=[x for x in desired_order if x in chem_props]
            f.write('\n'+'class '+str(comp_name)+':'+'\n' +\
                    '\t'+\
                    'def __init__(self,Constants,containingScenario,currentChemical,containingVolumeElement):\n\t\t'+\
                                    'self.containingScenario=containingScenario\n\t\t'+\
                                    'self.currentChemical=currentChemical\n\t\t'+\
                                    'self.Constants=Constants\n\t\t'+\
                                    'self.containingVolumeElement=containingVolumeElement\n\t\t')
#            comp_props=list(grouped_comp.get_group(group)['PropertyName'].unique()) # unique properties
    
            all_props=list(grouped_comp.get_group(group)['PropertyName']) # all property names 
            all_vals=list(grouped_comp.get_group(group)['PropertyValue']) # all property values 
            all_types=list(grouped_comp.get_group(group)['DataType']) # # all property types 
    
            c_p=tuple(zip(all_props,all_vals,all_types))
    
            constant_props=[] # properties that depend on constant number     
            bool_props=[] # boolean properties
            non_formula_props=[] # non formula props
            formula_props=[] # list of formula properties that are formulaic
            formula_props_dep_constant=[] # formulaic properties that depend on constants only
            formula_props_dep_prop=[] # formulaic properties that depend on other formulaic properties
            
            for t in c_p:
                if (t[2]=='Category Property')|(t[2]=='Text Property'):
                    non_formula_props.append(t[0])            
                if t[2]=='Constant Real Number Property':
                    constant_props.append(t[0])
                if t[2]=='True/False (Boolean) Property':
                     bool_props.append(t[0])                
                if t[2]=='Formula':
                    formula_props.append(t[0])
    
            non_formula_props=set(non_formula_props)
            bool_props=set(bool_props)
            constant_props=set(constant_props)
            formula_props=set(formula_props)
    
            constant_props_2=[] # any constant prop that is also in formula props must be removed
            for p in constant_props:
                if p not in formula_props:
                       constant_props_2.append(p)             
                       
    
            for t in c_p:
                if t[0] in formula_props: 
                    for fp in formula_props:
                        if fp.lower() in t[1].lower(): #if a property refers to a dependent property
                            formula_props_dep_prop.append(t[0])
            
            formula_props_dep_prop=set(formula_props_dep_prop)
            formula_props_dep_constant=formula_props-formula_props_dep_prop # these must be dependent properties that depend on float properties
            
            formula_props_dep_prop_c=[] # formula props that depend on formula props that depend on constants
            formula_props_dep_prop_f=[] # formula props that depend on formula props that depend on other formula props
            
            for t in c_p:
                if t[0] in formula_props_dep_prop: 
                    for fp in formula_props_dep_constant:
                        if fp.lower() in t[1].lower(): #if a property refers to a property that depends on constants
                            flag=False
                            for fp2 in formula_props_dep_prop:
                                 if fp2.lower() in t[1].lower():
                                     flag=True 
                                     break
                            if not flag:
                                formula_props_dep_prop_c.append(t[0])
    
            formula_props_dep_prop_c=set(formula_props_dep_prop_c)
            formula_props_dep_prop_f=formula_props_dep_prop-formula_props_dep_prop_c
    
            formula_props_dep_prop_f1=[] # formula props that depend on formula props that depend on  formula props that depend on independent formula properties
            formula_props_dep_prop_f2=[] # formula props that depend on formula props that depend on other formula props 
    
            for t in c_p:
                if t[0] in formula_props_dep_prop_f: 
                    for fp in formula_props_dep_prop_f:
                        if fp.lower() in t[1].lower(): #if a property refers to a dependent property
                            formula_props_dep_prop_f2.append(t[0])
    

            formula_props_dep_prop_f2=set(formula_props_dep_prop_f2)
            formula_props_dep_prop_f1=formula_props_dep_prop_f-formula_props_dep_prop_f2
    
            special_cases=['VolumeFraction_Liquid','VolumeFraction_Solid','GenericDenominatorforCalculatingFractioninPhases']
    
            comp_props_ordered=sorted(list(non_formula_props))+sorted(list(bool_props))+sorted(list(constant_props_2))+sorted(list(formula_props_dep_constant))+sorted(list(formula_props_dep_prop_c))+special_cases+sorted(list(formula_props_dep_prop_f1))+sorted((list(formula_props_dep_prop_f2)))
     
#            print (comp_props_ordered)
#            print()
            for prop in comp_props_ordered:
                df_prop_val=grouped_comp.get_group(group).loc[grouped_comp.get_group(group)['PropertyName']==prop]# data frame of property values (multi line if chemical specific)
                chems=list(df_prop_val['SpecificChemical'])
                prop_cl=clean_props(prop)
    #            f.write('\n\t\t'
    #                    'self.'+prop_cl+'='+'{}')   
                if len(chems)==1 and type(chems[0])== float:#isnan(chems[0]): # if only nan:
                    f.write('\n\t\t'
                            'self.'+prop_cl+'='+'()')   
                    ch_name='nan'
                    prop_val=df_prop_val['PropertyValue'].values[0]

                    if prop=="SedimentResuspensionVelocity": # temp hack to deal with sediment resuspension issue 
                        prop_val="9.64763202734353e-05"
                        
                    if type(prop_val)==float:
                        if isnan(prop_val):
                            prop_val='nan'
                    if (prop not in non_formula_props): 
                        #print (prop_val)
                        try:
                            prop_val=clean_props(prop_val)    
                        except:
                            pass
                        f.write('\n\t\t'
                                'self.'+prop_cl+'='+prop_val)                                
                    else:
                        f.write('\n\t\t'
                                'self.'+prop_cl+'='+"'"+prop_val+"'")                                
                else: # multiple chems
                    f.write('\n\t\t'
                           'self.'+prop_cl+'='+'{}')   
                    
                    for chem in chems: 
                        
                        if type(chem)==float:
                            ch_name='nan'
                            prop_val=df_prop_val[df_prop_val['SpecificChemical'].isnull()]['PropertyValue'].values[0]
                        else:
                            if comp_name in ["Benthic_Carnivore","Benthic_Omnivore","Benthic_Invertebrate"] and prop=="ChemicalTransferEfficiencyinFish":
                                prop_val="Function_ChemicalTransferEfficiencyinFish(compartment.BW,currentChemical.log10_K_ow)"
                            else:
                                prop_val=df_prop_val.loc[df_prop_val['SpecificChemical']==chem,'PropertyValue'].values[0]             
                            ch_name=clean_chem_names(chem)
                        if (prop not in non_formula_props) and (prop not in bool_props):
                            #print (prop_val)
                            try:
                                prop_val=clean_props(prop_val)    
                            except:
                                pass
                            f.write('\n\t\t' 
                                    'self.'+prop_cl+'["'+str(ch_name)+'"]'+'='+prop_val)                
                        else:
                            f.write('\n\t\t'
                                    'self.'+prop_cl+'["'+str(ch_name)+'""]'+'='+"'"+prop_val+"'") 
                    f.write('\n\t\t'
                                'try:\n\t\t\t'    
                                'self.Chemical_'+prop_cl+'='+'self.'+prop_cl+'[self.'+str('currentChemical.Name')+']\n\t\t'
                                'except:\n\t\t\t'
                                'self.Chemical_'+prop_cl+'=nan')
                f.write('\n')   
    
    #        if comp_name.strip()=='Air':
    #                break
    #            
    
        
        
    f.close()
    
    return(df_lib,df_alg,df_alg_mat,df_chem)  
    
if __name__ == '__main__':
    df_lib,df_alg,df_alg_mat,df_chem=process_master_library(inputs)


    