# -*- coding: utf-8 -*-
"""
Created on Tue Jul 20 10:01:24 2021
@author: 13963

Includes function to create the simulation transition matrix.

"""
from util_functions import * 
from constants import *
from define_scenario import *
from define_ve import *
from define_pve import *
from define_algs import *
from define_ps_algs import *
from define_attributes_props import *
from define_chem_classes import *
from define_comp_classes import *
from find_neighbors import *
import os
import numpy as np
import importlib
import define_comp 


def link_check (comp_objects_dict,comp1_name,comp2_name,dict_inputs,chem_list_clean,currentChemical): # function to check if two compartments are potentially linked and to return connecting algorithms
    link=False # does link exist
    app_algs=[] # list of applicable link algorithms
    if 'Sink' in comp1_name: # Sinks dont send chemical
        return (link, app_algs)
    comp1,comp2=comp_objects_dict[comp1_name],comp_objects_dict[comp2_name]    
    df_alg_mat,df_links=dict_inputs['df_alg_mat'],dict_inputs['df_links']
    cond1=check_neighbor(comp1,comp2,dict_inputs).is_neighbor()[0] # are the compartments in neighboring volume elements?
    if comp1.containingVolumeElement==comp2.containingVolumeElement: # are the compartments in the same volume element? 
        cond2=True
    else:
        cond2=False
    if cond1 or cond2:
    
        df_app=df_alg_mat.loc[(df_alg_mat['sendingCompartmentCategory']==comp1.category) & (df_alg_mat['receivingCompartmentCategory']==comp2.category) & (df_alg_mat['enabled']=='true')]
        if 'Abiotic' in comp1.category and 'Abiotic' in comp2.category:
            df_app2=df_alg_mat.loc[(df_alg_mat['sendingCompartmentCategory']=="Abiotic") & (df_alg_mat['receivingCompartmentCategory']=='Abiotic') & (df_alg_mat['enabled']=='true')]
            df_app=df_app.append(df_app2)
        if len (df_app)==0:
            return(link,app_algs)
        algs_non_chem=list(df_app.loc[(df_app['sendingChemicalName']=='ReplaceMe')]['index']) # algorithms that are not chemical specific
        app_algs.append(algs_non_chem)
        df_app['sendingChemicalName']=df_app['sendingChemicalName'].apply(clean_chem_names) # clean chem names
        df_app['receivingChemicalName']=df_app['receivingChemicalName'].apply(clean_chem_names) # clean chem names
        algs_chem=list(df_app.loc[(df_app['sendingChemicalName']==currentChemical.Name)&(df_app['receivingChemicalName'].isin(chem_list_clean))]['index']) # chemical specific algorithms 
        app_algs.append(algs_chem) # list of applicable algorithms (indices)
        app_algs=[y for x in app_algs for y in x]
        if cond1 or cond2:
            link=True
        return(link,app_algs)
    else:
        return(link, app_algs)
        

def create_trans_mat(inputs,dict_inputs): # function to create transition matrix
    chem_list=inputs['simulation_Chemicals'] # simulation chemicals
    chem_list_clean=[clean_chem_names(x) for x in chem_list] # cleaned chemical names
    comp_list=list(dict_inputs['comp_dict'].values())# list of compartments in simulation
    ncomp=len(comp_list)
    mat_dim= ncomp*ncomp # number of rows or cols in the transition matrix
    tm=np.zeros((mat_dim,mat_dim), dtype=float) # create zero matrix     
    df_alg_mat=dict_inputs['df_alg_mat']      # dataframe of applicable algorithms for combination of sending and receiving compartment types


    for chem_index, chem in enumerate(chem_list_clean): # loop over chemicals
        currentChemical=chem_objects_dict[chem] # current chemical object
        comp_objects_dict=define_comp.define_comp(currentChemical) # create dictionary of compartment objects    
        print ('chemical is ', chem, 'Kd is ',comp_objects_dict['Surface_water_in_SW_LakeCadillac'].Chemical_Kd)
        
        for row_index, comp_row in enumerate(comp_list): # loop over rows (sending compartments)
            for col_index, comp_col in enumerate (comp_list): # loop over columns (sending compartments)
                link,app_algs=link_check(comp_objects_dict,comp_row,comp_col,dict_inputs,chem_list_clean,currentChemical) # call function to check if compartments are linked and if so what algorithms apply
                if link: 
                    for alg in app_algs: # loop over applicable algorithms
                        alg_name=df_alg_mat.loc[df_alg_mat['index']==alg,'Alg_Name_New'].values[0]# lookup alg name by index in df_alg_mat
                        alg_class=eval(alg_name) # temporary -- get rid of eval eventually by placing algorithm objects in a dictionary
                        SendingCompartment=comp_objects_dict[comp_row] # sending compartment object
                        ReceivingCompartment=comp_objects_dict[comp_col] # receiving compartment object                        
                        alg_instance=alg_class(Constants,containingScenario,currentChemical,SendingCompartment,ReceivingCompartment,dict_inputs)# instantiate algorithm class
                        transfer_factor=alg_instance.transferFactor # compute transfer factor
                        if type(transfer_factor)==float and alg_instance.doesTransformChemical=='false': # if tf is a float (not error) and algorithms does not involved transformation
                            print (comp_row,comp_col,transfer_factor)
                            tm[int(chem_index*ncomp+row_index)][int(chem_index*ncomp+row_index)]=tm[int(chem_index*ncomp+row_index)][int(chem_index*ncomp+row_index)]-transfer_factor # sending compartment tf is negative
                            tm[int(chem_index*col_index)][int(chem_index*ncomp+row_index)]=tm[int(chem_index*col_index)][int(chem_index*ncomp+row_index)]+transfer_factor # receiving compartment tf is positive                        
                        if type(transfer_factor)==float and alg_instance.doesTransformChemical=='true': # if tf is a float (not error) and algorithms does not involved transformation
                            receivingChemical_index=chem_list.index(alg_instance.receivingChemicalName) # index of receiving chemical
                            print ('Transforming ',comp_row,comp_col,transfer_factor)
                            tm[int(chem_index*ncomp+row_index)][int(chem_index*ncomp+row_index)]=tm[int(chem_index*ncomp+row_index)][int(chem_index*ncomp+row_index)]-transfer_factor # sending compartment tf is negative
                            tm[int(receivingChemical_index*ncomp+row_index)][int(chem_index*ncomp+row_index)]=tm[int(receivingChemical_index*ncomp+row_index)][int(chem_index*ncomp+row_index)]+transfer_factor # receiving compartment tf is positive
                        
            


        
        
    return(tm)

## FOR QA Only
#row_index=3
#col_index=4
#comp_row=comp_list[row_index]
#comp_col=comp_list[col_index]

#row_index=3
#col_index=0
#comp_row=comp_list[row_index]
#comp_col=comp_list[col_index]
#comp1_name=comp_row
#comp2_name=comp_col
#
#row_index=3
#col_index=3
#comp_row=comp_list[row_index]
#comp_col=comp_list[col_index]
#comp1_name=comp_row
#comp2_name=comp_col