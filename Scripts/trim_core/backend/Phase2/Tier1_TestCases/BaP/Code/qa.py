# -*- coding: utf-8 -*-
"""

Purpose: to compare pyTRIm against legacy output
Created on Mon Oct 18 10:00:51 2021

@author: 13963
"""

import pandas as pd
import csv
import os


runner_full_path = os.path.realpath(__file__) # full path to this runner script
path_code = os.path.dirname(runner_full_path) # directory of the runner script (code)
path_legacy_inputs=os.path.abspath(os.path.join(path_code,'..', 'legacy_input_files')) # legacy inputs directory
path_inputs=os.path.abspath(os.path.join(path_code,'..', 'input_files')) # lower case inputs directory
path_output=os.path.abspath(os.path.join(path_code,'..','output')) # output directory


cross_walk={'BaP':'benzo_a_pyrene'} # key is sheetname, value is corresponding chemical name in pytrim

leg_fp=os.path.join(path_output, 'LegacyRun_Results.xlsx') # legacy annual mass results text file read in and saved from excel. First 4 lines to be skipped.

pytrim_fp=os.path.join(path_output, 'results.csv') # path to pytrim results

### read legacy results

leg_df={}

for k,v in cross_walk.items():
    leg_df[v]=pd.read_excel(leg_fp,k,header=4)
    leg_df[v]=leg_df[v].tail(2) # keep second last line only
    leg_df[v]=leg_df[v].head(1) # keep second last line only
    header=leg_df[v].columns # old header
    new_header=[] 
    for hd in header: # loop over old column names 
        if hd in ['Date','Time','TimeZone']: # no change required for these
            new_header.append(hd)
            continue
        # head='chem_'+v+'_'+hd.replace(' ','_').replace('/','_') # convert to new trim convention
        head='chem_'+v+'_'+hd.replace(' ','_').replace('/','_').replace('-','_').replace('__','_').replace('___','_') # convert to new trim convention
        head=head.replace('__','_').replace('___','_') # convert to new trim convention
        head=head.lower()
        plant_types=['deciduous_forest_in_','coniferous_forest_in_','grasses_herbs_in_'] 
        for plant in plant_types:
            if plant in head:
                head=head.replace(plant+plant,plant) # replace double occurrence with single mention
        new_header.append(head)
    leg_df[v].columns=new_header
    

### read pytrim results and average last year only
    
with open(pytrim_fp, newline='') as f:
  reader = csv.reader(f)
  header = next(reader)  # gets the first line efficiently for header
df_py=pd.read_csv(pytrim_fp,skiprows=49*365*24) 
df_py.columns=header   
    
df_py=df_py.describe() # get means and summ stats

pyvars=list(df_py.loc['mean'].index) 

# pyvars=[x for x in pyvars if ('sink' not in x and 'source' not in x and 'air' not in x)] # cut out sinks and sources and air

#pyvars=[x for x in pyvars if ('sink' not in x and ('source' not in x or x.split('_')[-1]=='source') and 'air' not in x)] # cut out sinks and sources and air

pyvars=[x for x in pyvars if ('sink' not in x and ('source' not in x or x.split('_')[-1]=='source'))] # cut out sinks and sources and air


## create empty output data structures

op_dic={}

for k,v in cross_walk.items():
    op_dic[v]=[]


### loop over py variables and find ratio of corresponding value in legacy file


for var in pyvars[1:]: # loop over py variables and find ratio of corresponding value in legacy file
    for k,v in cross_walk.items(): # find chem_name by looking within variable
        if v in var:
            chem_name=v
    var_name=var.split('chem_'+chem_name+'_')[1]  # find var_name within variable
    print (var_name)
    if var in leg_df[chem_name].columns:
        print (var)
        leg_val=float(leg_df[chem_name][var].values[0])
        py_val=df_py[var].loc['mean']
        # print (py_val)
        
        if leg_val==py_val: # to catch 0/0
            ratio=1       
        else:
            ratio=py_val/leg_val
            # ratio=round(ratio,2)
        tup=(var_name,ratio)
        op_dic[chem_name].append(tup)
        
for k,v in op_dic.items():
    op_dic[k]=pd.DataFrame(v,columns=['Compartment','Ratio'])
 
### output comparison
           

ofn=r"PyTRIM_Results_Comparison_Mass.xlsx"

ofpn=os.path.join(path_output,ofn)
writer = pd.ExcelWriter(ofpn, engine='xlsxwriter')


for k,v in op_dic.items():
    v.to_excel(writer, sheet_name=k,index=False)
    for column in v: # format output column width
        column_length = max(v[column].astype(str).map(len).max(), len(column))
        col_idx = v.columns.get_loc(column)
        writer.sheets[k].set_column(col_idx, col_idx, column_length)    


writer.save()     
writer.close()

################## RUN QA OF CONCENTRATION RESULTS ###################


leg_fp=os.path.join(path_output, 'LegacyRun_Results_Conc.xlsx') # legacy annual conc results text file read in and saved from excel. First 4 lines to be skipped.

pytrim_fp=os.path.join(path_output, 'results_conc.csv') # path to pytrim results

### read legacy results

leg_df={}

for k,v in cross_walk.items():
    leg_df[v]=pd.read_excel(leg_fp,k,header=4)
    leg_df[v]=leg_df[v].tail(2) # keep second last line only
    leg_df[v]=leg_df[v].head(1) # keep second last line only
    header=leg_df[v].columns # old header
    new_header=[] 
    for hd in header: # loop over old column names 
        if hd in ['Date','Time','TimeZone']: # no change required for these
            new_header.append(hd)
            continue
        # head='chem_'+v+'_'+hd.replace(' ','_').replace('/','_') # convert to new trim convention
        head='chem_'+v+'_'+hd.replace(' ','_').replace('/','_').replace('-','_').replace('__','_').replace('___','_') # convert to new trim convention
        head=head.replace('__','_').replace('___','_') # convert to new trim convention
        head=head.lower()
        plant_types=['deciduous_forest_in_','coniferous_forest_in_','grasses_herbs_in_'] 
        for plant in plant_types:
            if plant in head:
                head=head.replace(plant+plant,plant) # replace double occurrence with single mention
        new_header.append(head)
    leg_df[v].columns=new_header
    

### read pytrim results and average last year only
    
with open(pytrim_fp, newline='') as f:
  reader = csv.reader(f)
  header = next(reader)  # gets the first line efficiently for header
df_py=pd.read_csv(pytrim_fp,skiprows=49*365*24) 
df_py.columns=header   
    
df_py=df_py.describe() # get means and summ stats

pyvars=list(df_py.loc['mean'].index) 

# pyvars=[x for x in pyvars if ('sink' not in x and 'source' not in x and 'air' not in x)] # cut out sinks and sources and air

# pyvars=[x for x in pyvars if ('sink' not in x and ('source' not in x or x.split('_')[-1]=='source') and 'air' not in x)] # cut out sinks and sources and air

pyvars=[x for x in pyvars if ('sink' not in x and ('source' not in x or x.split('_')[-1]=='source'))] # cut out sinks and sources and air

## create empty output data structures

op_dic={}

for k,v in cross_walk.items():
    op_dic[v]=[]


### loop over py variables and find ratio of corresponding value in legacy file


for var in pyvars: # loop over py variables and find ratio of corresponding value in legacy file
    for k,v in cross_walk.items(): # find chem_name by looking within variable
        if v in var:
            chem_name=v
    var_name=var.split('chem_'+chem_name+'_')[1]  # find var_name within variable
    print (var_name)
    if var in leg_df[chem_name].columns:
        print (var)
        leg_val=float(leg_df[chem_name][var].values[0])
        py_val=df_py[var].loc['mean']
        
        if leg_val==py_val: # to catch 0/0
            ratio=1       
        else:
            ratio=py_val/leg_val
            ratio=round(ratio,2)
            # if ratio<1e6:
            #     ratio=1
        tup=(var_name,ratio)
        op_dic[chem_name].append(tup)
        # if "leaf" in var:
        #     print (py_val, leg_val, py_val/leg_val)
        if "stem" in var:
            print (py_val, leg_val, py_val/leg_val)
for k,v in op_dic.items():
    op_dic[k]=pd.DataFrame(v,columns=['Compartment','Ratio'])
 
### output comparison
           

ofn=r"PyTRIM_Results_Comparison_Conc.xlsx"

ofpn=os.path.join(path_output,ofn)
writer = pd.ExcelWriter(ofpn, engine='xlsxwriter')


for k,v in op_dic.items():
    v.to_excel(writer, sheet_name=k,index=False)
    for column in v: # format output column width
        column_length = max(v[column].astype(str).map(len).max(), len(column))
        col_idx = v.columns.get_loc(column)
        writer.sheets[k].set_column(col_idx, col_idx, column_length)    


writer.save()     
writer.close()