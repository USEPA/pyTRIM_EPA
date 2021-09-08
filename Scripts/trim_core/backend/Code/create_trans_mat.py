# -*- coding: utf-8 -*-
"""
created on tue jul 20 10:01:24 2021
@author: 13963

includes function to create the simulation transition matrix.

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
import pandas as pd

def link_check (comp_objects_dict,comp1_name,comp2_name,dict_inputs,chem_list_clean,currentchemical): # function to check if two compartments are potentially linked and to return connecting algorithms
    link=False # does link exist
    app_algs=[] # list of applicable link algorithms
    if 'sink' in comp1_name: # sinks dont send chemical
        return (link, app_algs)
    comp1,comp2=comp_objects_dict[comp1_name],comp_objects_dict[comp2_name]    
    df_alg_mat,df_links=dict_inputs['df_alg_mat'],dict_inputs['df_links']
    cond1=check_neighbor(comp1,comp2,dict_inputs).is_neighbor()[0] # are the compartments in neighboring volume elements?
    if comp1.containingvolumeelementname==comp2.containingvolumeelementname: # are the compartments in the same volume element? 
        cond2=True
    else:
        cond2=False
    if ("vaporsource" in comp1.name or "particlesource" in comp1.name) and ("surface_water" in comp2.name or "surface_soil" in comp2.name):
        cond3=True # pseudo source compartment connected to surface water or surface soil
    else: 
        cond3=False
    if cond1 or cond2:    
        df_app=df_alg_mat.loc[(df_alg_mat['sendingcompartmentcategory']==comp1.category) & (df_alg_mat['receivingcompartmentcategory']==comp2.category) & (df_alg_mat['enabled']=='True')]
        if 'abiotic' in comp1.category and 'abiotic' in comp2.category:
            df_app2=df_alg_mat.loc[(df_alg_mat['sendingcompartmentcategory']=="abiotic") & (df_alg_mat['receivingcompartmentcategory']=='abiotic') & (df_alg_mat['enabled']=='True')]
            df_app=df_app.append(df_app2)
        if len (df_app)==0:
            return(link,app_algs)
        algs_non_chem=list(df_app.loc[(df_app['sendingchemicalname']=='replaceme')]['index']) # algorithms that are not chemical specific
        app_algs.append(algs_non_chem)
        df_app['sendingchemicalname']=df_app['sendingchemicalname'].apply(clean_chem_names) # clean chem names
        df_app['receivingchemicalname']=df_app['receivingchemicalname'].apply(clean_chem_names) # clean chem names
        algs_chem=list(df_app.loc[(df_app['sendingchemicalname']==currentchemical.name)&(df_app['receivingchemicalname'].isin(chem_list_clean))]['index']) # chemical specific algorithms 
        app_algs.append(algs_chem) # list of applicable algorithms (indices)
        app_algs=[y for x in app_algs for y in x]
        if cond1 or cond2:
            link=True
        return(link,app_algs)
    if cond3: # pseudo source algorithm
        df_psalgs=dict_inputs['df_psalgs']
        psalgs=list(df_psalgs['algorithm'])
        app_algs=[x for x in psalgs if ('surface_water' in comp2.name and 'surface water' in x)] # temp -- need to fix
        return(cond3,[-1]) # temp -1 indicates pseudo source algs to surface water        
    else:
        return(link, app_algs)
        

def create_trans_mat(inputs,dict_inputs): # function to create transition matrix
    chem_list=inputs['simulation_chemicals'] # simulation chemicals
    chem_list_clean=[clean_chem_names(x) for x in chem_list] # cleaned chemical names
    comp_list=list(dict_inputs['comp_dict'].values())# list of compartments in simulation
    ncomp=len(comp_list)
    nchem=len(chem_list)
    mat_dim= ncomp*nchem # number of rows or cols in the transition matrix
    tm=np.zeros((mat_dim,mat_dim), dtype=float) # create zero matrix     
    sm=np.zeros(mat_dim,dtype=float) # create zero sources matrix
    df_alg_mat=dict_inputs['df_alg_mat']      # DataFrame of applicable algorithms for combination of sending and receiving compartment types

    
    ind_name=[] # index name for tm, sm DataFrames
    for chem_index, chem in enumerate(chem_list_clean): # loop over chemicals
        currentchemical=chem_objects_dict[chem] # current chemical object
        comp_objects_dict=define_comp.define_comp(currentchemical) # create dictionary of compartment objects    
        print ('chemical is ', chem, 'kd is ',comp_objects_dict['surface_water_in_sw_lakecadillac'].chemical_kd)
        
        for row_index, comp_row in enumerate(comp_list): # loop over rows (sending compartments)
            ind_name.append(currentchemical.name+'_'+comp_objects_dict[comp_row].name) # index name for this element of the matrix                   
            if hasattr(comp_objects_dict[comp_row], 'deposition_rate'): # if sending compartment has deposition rate
                if currentchemical.name in comp_objects_dict[comp_row].deposition_rate.keys(): # if there is deposition of the current chemical:
                    sm[int(chem_index*ncomp+row_index)]=sm[int(chem_index*ncomp+row_index)]+comp_objects_dict[comp_row].deposition_rate[currentchemical.name] # add depostion rate

            for col_index, comp_col in enumerate (comp_list): # loop over columns (sending compartments)
                link,app_algs=link_check(comp_objects_dict,comp_row,comp_col,dict_inputs,chem_list_clean,currentchemical) # call function to check if compartments are linked and if so what algorithms apply
                if link: 
                    for alg in app_algs: # loop over applicable algorithms
                        if alg==-1: # temp
                            alg_name='direct_transfer_from_pseudosource_to_surface_water' # temp
                        else:    
                            alg_name=df_alg_mat.loc[df_alg_mat['index']==alg,'alg_name_new'].values[0]# lookup alg name by index in df_alg_mat
                        alg_class=eval(alg_name) # temporary -- get rid of eval eventually by placing algorithm objects in a dictionary
                        sendingcompartment=comp_objects_dict[comp_row] # sending compartment object
                        receivingcompartment=comp_objects_dict[comp_col] # receiving compartment object                        
                        alg_instance=alg_class(constants,containingscenario,currentchemical,sendingcompartment,receivingcompartment,dict_inputs)# instantiate algorithm class
                        transfer_factor=alg_instance.transferfactor # compute transfer factor
                        if (type(transfer_factor)==float or type(transfer_factor)==np.float64 or type(transfer_factor)==np.float32) and not np.isnan(transfer_factor) and alg_instance.doestransformchemical=='False': # if tf is a float (not error) and algorithms does not involved transformation
                            tm[int(chem_index*ncomp+row_index)][int(chem_index*ncomp+row_index)]=tm[int(chem_index*ncomp+row_index)][int(chem_index*ncomp+row_index)]-transfer_factor # sending compartment tf is negative
                            tm[int(chem_index*ncomp+col_index)][int(chem_index*ncomp+row_index)]=tm[int(chem_index*ncomp+col_index)][int(chem_index*ncomp+row_index)]+transfer_factor # receiving compartment tf is positive                        
                        if row_index==col_index and (type(transfer_factor)==float or type(transfer_factor)==np.float64 or type(transfer_factor)==np.float32) and not np.isnan(transfer_factor) and alg_instance.doestransformchemical=='True': # if tf is a float (not error) and algorithms does involve transformation
                            receivingchemical_index=chem_list.index(alg_instance.receivingchemicalname) # index of receiving chemical
                            tm[int(chem_index*ncomp+row_index)][int(chem_index*ncomp+row_index)]=tm[int(chem_index*ncomp+row_index)][int(chem_index*ncomp+row_index)]-transfer_factor # sending compartment tf is negative
                            tm[int(receivingchemical_index*ncomp+row_index)][int(chem_index*ncomp+row_index)]=tm[int(receivingchemical_index*ncomp+row_index)][int(chem_index*ncomp+row_index)]+transfer_factor # receiving compartment tf is positive                    
           
    df_tm=pd.DataFrame(tm,index=ind_name,columns=ind_name)
    df_sm=pd.DataFrame(sm,index=ind_name,columns=['deposition_rate_g_day-1'])
              
    return(tm,sm,df_tm,df_sm)

## for qa only
     
    
#row_index=5
#col_index=4
#comp_row=comp_list[row_index]
#comp_col=comp_list[col_index]
#comp1_name=comp_row
#comp2_name=comp_col        
#    
