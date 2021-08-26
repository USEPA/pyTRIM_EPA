# -*- coding: utf-8 -*-
"""
Created on Tue Jul 13 09:59:30 2021
@author: 13963

TRIM.FaTE backend runner script
"""

import os
import time

import mlib,plib,vol_elem,comp,prop,dep_rates,solve_ode # import supporting modules to process inputs and auto generate code to define objects

 
runner_full_path = os.path.realpath(__file__) # full path to this runner script
path_code = os.path.dirname(runner_full_path) # directory of the runner script (Code)
path_inputs=os.path.abspath(os.path.join(path_code,'..', 'Input_Files')) # inputs directory
path_output=os.path.abspath(os.path.join(path_code,'..','Output')) # scripts directory

inputs={} # dictionary of scenario specific inputs
inputs['path_inputs']=path_inputs
inputs['path_code']=path_code
inputs['path_output']=path_output
inputs['simulation_name']='Foundries_SS'
inputs['master_library_file']=r'ICF_Master_Library_03212016_PropertyExporter.txt'
inputs['pseudo_library_file']=r'Foundries_SS_1_pseudo_library_objects.txt'
inputs['ve_file']=r'Foundries_SS (2) Volume Elements.txt'
inputs['pseudo_ve_file']=r'Foundries_SS_2_pseudo_volume_elements.txt'
inputs['comp_file']=r'Foundries_SS (3) Compartments.txt'
inputs['prop_file']=r'Foundries_SS (4) Properties.txt'
inputs['plink_file']=r'Foundries_SS_3_pseudo_link_properties.txt'
inputs['dep_rates_file']=r'Foundries_PS_DepRates_Properties.txt'
inputs['simulation_Chemicals']=['Elemental Mercury','Divalent Mercury','MethylMercury']


def read_inputs_write_classes(inputs): # function to to read inputs and auto generate code to define objects

    df_lib,df_alg,df_alg_mat,df_chem=mlib.process_master_library(inputs) # reads master lib into these dataframes AND writes define_algs.py, define_chem_classes.py, define_comp_classes.py into Code
    df_psalgs,df_ps,df_pt=plib.process_pseudo_library(inputs) # reads master lib into these dataframes AND writes define_ps_algs.py
    df_points,df_parcels,df_ve,df_pve=vol_elem.define_volume_elements(inputs) # reads volume element inputs into these dataframes and write define_ve.py and define_pve.py  
    df_props,df_links,df_plinks=prop.define_properties(inputs) # read properties files into these dataframes and writes define_scenario.py and define_attributes_props.py
    df_dr=dep_rates.define_deposition_rates(inputs) # reads deposition rates into dataframe and writes define_attributes_dep_rates.py
    df_comp,comp_dict=comp.define_compartments(inputs,df_parcels,df_ve,df_pve,df_props,df_dr) # reads compartments inputs into dataframe and writes define_comp.py
    dict_inputs={'df_lib':df_lib,'df_alg':df_alg,'df_alg_mat':df_alg_mat,'df_chem':df_chem,'df_psalgs':df_psalgs,'df_ps':df_ps,'df_pt':df_pt,'df_points':df_points,'df_parcels':df_parcels,'df_ve':df_ve,'df_comp':df_comp,'comp_dict':comp_dict,'df_props':df_props,'df_links':df_links,'df_plinks':df_plinks,'df_dr':df_dr}
    return(dict_inputs)

  

if __name__=='__main__':
    start=time.time()
    dict_inputs=read_inputs_write_classes(inputs) # call function to read inputs and auto generate code to define objects    
    import create_trans_mat # need to import here because supporting modules are not defined until this point 
    tm,sm,df_tm,df_sm=create_trans_mat.create_trans_mat(inputs,dict_inputs) # call function to generate transition matrix and sources matrix   
    Nt,df_Nt=solve_ode.ode_sim(tm,df_tm,sm,df_sm)
    ### output results (temp)
    ofpn=os.path.join(path_output,'Results.csv')
    df_Nt.to_csv(ofpn,index=False)
    ofpn=os.path.join(path_output,'TM.csv')
    df_tm.to_csv(ofpn,index=True)
    ofpn=os.path.join(path_output,'SM.csv')
    df_sm.to_csv(ofpn,index=True)
    
    print ('Time to run analysis in seconds = ',round((time.time()-start),2))
