# -*- coding: utf-8 -*-
"""
created on tue jul 13 09:59:30 2021
@author: 13963

trim.fate backend runner script
"""

import os
import time

import convert_lc,mlib,plib,vol_elem,comp,prop,dep_rates,solve_ode,gen_conc,gen_avg # import supporting modules to process inputs and auto generate code to define objects
from util_functions import process_met

runner_full_path = os.path.realpath(__file__) # full path to this runner script
path_code = os.path.dirname(runner_full_path) # directory of the runner script (code)
path_legacy_inputs=os.path.abspath(os.path.join(path_code,'..', 'legacy_input_files')) # legacy inputs directory
path_inputs=os.path.abspath(os.path.join(path_code,'..', 'input_files')) # lower case inputs directory
path_output=os.path.abspath(os.path.join(path_code,'..','output')) # output directory

if not os.path.exists(path_inputs):
    os.makedirs(path_inputs)
if not os.path.exists(path_output):
    os.makedirs(path_output)


inputs={} # dictionary of scenario specific inputs
inputs['legacy_path_inputs']=path_legacy_inputs
inputs['path_inputs']=path_inputs
inputs['path_code']=path_code
inputs['path_output']=path_output
inputs['simulation_name']='foundries_ss'
inputs['master_library_file']=r'icf_master_library_03212016_propertyexporter.txt'
inputs['pseudo_library_file']=r'foundries_ss_1_pseudo_library_objects.txt'
inputs['met_file']=r'isf_met_mi_20181219.csv'
inputs['allowexchange_file']=r'allowexchange_foundries.csv'
inputs['litterfall_file']=r'litterfallrate_foundries.csv'
inputs['ve_file']=r'foundries_ss (2) volume elements.txt'
inputs['pseudo_ve_file']=r'foundries_ss_2_pseudo_volume_elements.txt'
inputs['comp_file']=r'foundries_ss (3) compartments.txt'
inputs['prop_file']=r'foundries_ss (4) properties.txt'
inputs['prop_file_2']=r'foundries_ss (5) other properties.txt'
inputs['prop_file_3']=r'foundries (6) customflushrate.txt'
inputs['plink_file']=r'foundries_ss_3_pseudo_link_properties.txt'
inputs['dep_rates_file']=r'foundries_ps_deprates_properties.txt'
inputs['simulation_chemicals']=['elemental mercury','divalent mercury','methylmercury']
inputs['simulation_start_date']='1/1/1990' # string format. assumes starting from 0000 hours
inputs['simulation_end_date']='1/1/2040' # string format. assumes ending at 0000  hours

convert_lc.convert_lc(inputs) # convert legacy input files to lower case and write into new location
met_dict=process_met(inputs) # get processed average met values    
inputs['met_dict']=met_dict # add processed met values to inputs

def read_inputs_write_classes(inputs): # function to to read inputs and auto generate code to define objects    
    df_lib,df_alg,df_alg_mat,df_chem=mlib.process_master_library(inputs) # reads master lib into these DataFrames and writes define_algs.py, define_chem_classes.py, define_comp_classes.py into code
    df_psalgs,df_psalg_mat,df_ps,df_pt=plib.process_pseudo_library(inputs) # reads master lib into these DataFrames and writes define_ps_algs.py
    df_points,df_parcels,df_ve,df_pve=vol_elem.define_volume_elements(inputs) # reads volume element inputs into these DataFrames and write define_ve.py and define_pve.py  
    df_props,df_props_2,df_links,df_plinks=prop.define_properties(inputs) # read properties files into these DataFrames and writes define_scenario.py and define_attributes_props.py
    df_dr=dep_rates.define_deposition_rates(inputs) # reads deposition rates into DataFrame and writes define_attributes_dep_rates.py
    df_comp,comp_dict=comp.define_compartments(inputs,df_parcels,df_ve,df_pve,df_props,df_props_2,df_dr) # reads compartments inputs into DataFrame and writes define_comp.py
    dict_inputs={'met_dict':inputs['met_dict'],'df_lib':df_lib,'df_alg':df_alg,'df_alg_mat':df_alg_mat,'df_chem':df_chem,'df_psalgs':df_psalgs,'df_psalg_mat':df_psalg_mat,'df_ps':df_ps,'df_pt':df_pt,'df_points':df_points,'df_parcels':df_parcels,'df_ve':df_ve,'df_comp':df_comp,'comp_dict':comp_dict,'df_props':df_props,'df_links':df_links,'df_plinks':df_plinks,'df_dr':df_dr}
    return(dict_inputs)
  
  

if __name__=='__main__':
    start=time.time()
    # convert_lc.convert_lc(inputs) # convert legacy input files to lower case and write into new location
    dict_inputs=read_inputs_write_classes(inputs) # call function to read inputs and auto generate code to define objects    
    import create_trans_mat # need to import here because supporting modules are not defined until this point 
    tm_start=time.time()
    tm,sm,vmu,df_tm,df_sm,df_vmu,df_n0=create_trans_mat.create_trans_mat(inputs,dict_inputs) # call function to generate transition matrix, sources, volume-mass-concentration_units matrix   
    ode_start=time.time()
    nt,df_nt=solve_ode.ode_sim(inputs,tm,df_tm,sm,df_sm,df_n0)
    ode_end=time.time()
    df_conc=gen_conc.compute_conc(nt,df_nt,vmu,df_vmu) # compute concentrations time series 
    conc_end=time.time()
    dfn_avg,dfc_avg=gen_avg.gen_avg(df_nt,df_conc,inputs) # compute annual average mass and conc time series
    av_end=time.time()
    ### output results (temp)
    ofpn=os.path.join(path_output,'results.csv')
    df_nt.to_csv(ofpn,index=False)
    ofpn=os.path.join(path_output,'tm.csv')
    df_tm.to_csv(ofpn,index=True)
    ofpn=os.path.join(path_output,'sm.csv')
    df_sm.to_csv(ofpn,index=True)
    ofpn=os.path.join(path_output,'results_conc.csv')
    df_conc.to_csv(ofpn,index=False) 
    ofpn=os.path.join(path_output,'time_series_mass.csv')
    dfn_avg.to_csv(ofpn,index=False) 
    ofpn=os.path.join(path_output,'time_series_conc.csv')
    dfc_avg.to_csv(ofpn,index=False) 
    output_end=time.time()
    analysis_time=round((time.time()-start),2)
    print ('time to run analysis in minutes = ',round(analysis_time/60,2))
    print ('% time to tm_start = ',round(100*(tm_start-start)/analysis_time,2),'%')
    print ('% time to create tm = ',round(100*(ode_start-tm_start)/analysis_time,2),'%')    
    print ('time to create tm in minutes = ',round((ode_start-tm_start)/60,2))  
    print ('% time to run odes = ',round(100*(ode_end-ode_start)/analysis_time,2),'%')
    print ('% time to calculate concentrations = ',round(100*(conc_end-ode_end)/analysis_time,2),'%')
    print ('% time to calculate averages = ',round(100*(av_end-conc_end)/analysis_time,2),'%')
    print ('% time to write output = ',round(100*(output_end-av_end)/analysis_time,2),'%')    

    
