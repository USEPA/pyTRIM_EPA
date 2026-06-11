# -*- coding: utf-8 -*-
"""

To compare gold standard transfer matrix with py production transfer matrix

Created on Wed May 17 14:16:00 2023

@author: 13963
"""

import pandas as pd
import os

ifp_gs = r'/Users/55284/Library/CloudStorage/OneDrive-ICF/Desktop/RTR_TRIM-FaTE/TRIM_builder_mac_2/TRIM_builder_new/Scripts/' # path to gold standard output
ifn_gs = 'tm.csv' 

ifp_py = r'/Users/55284/Library/CloudStorage/OneDrive-ICF/Desktop/RTR_TRIM-FaTE/TRIM_builder_mac_2/TRIM_builder_new/Scripts/' # path to pytrim fe based output
ifn_py = 'Transfer_Matrix_test.csv' 

df_gs = pd.read_csv(os.path.join(ifp_gs, ifn_gs))  # gs matrix as df
df_py = pd.read_csv(os.path.join(ifp_py, ifn_py))  # py matrix as df


def process_cnames(text): # to convert py matrix colnames to gs format
    text=text.replace(' ','_')
    text=text.lower()
    text=text.replace('soil_advection_sink','sink_in_sink_for_soil_surface')  # soil advection sinks are called sink in sink
    text='chem_'+text
    return text 


df_py.iloc[:,0]=df_py.iloc[:,0].apply(process_cnames) # convert column 0 names (receiving compartment names)
df_py.columns=[process_cnames(x) for x in df_py.columns] # convert py matrix column names (sending compartment names)

comps_gs=list(df_gs.iloc[:,0]) # list of comps in gs
comps_py=list(df_py.iloc[:,0]) # list of comps in py

op=[] 
for comp_gs_index, rc in enumerate(comps_gs): # loop over comps_gs
    receiving_comp=rc # receiving compartment name
    print ('Processing ', rc) 
    py_rc_index=comps_py.index(rc) if rc in comps_py else -1  # index of receiving comp in py matrix 
    for sc in df_gs.columns[1:]: # loop over sending compartments
        py_sc_index=comps_py.index(sc) if sc in comps_py else -1         # index of sending comp in py matrix
        sending_comp=sc
        if py_rc_index==-1:
            r=(receiving_comp,sending_comp,'NA','NA','Receiving compartment not found')            
        elif py_sc_index==-1:
            r=(receiving_comp,sending_comp,'NA','NA','Sending compartment not found')            
        else:
            tf_gs=df_gs.iloc[comp_gs_index][sc] # gs transfer factor
            tf_py=df_py.iloc[py_rc_index][sc] # py transfer factor
            if tf_gs==0 and tf_py==0:
                r=(receiving_comp,sending_comp,0,0,'Both Zero')
            if tf_gs!=0 and tf_py==0:
                r=(receiving_comp,sending_comp,tf_gs,tf_py,'Py TF Incorrectly Has Zero Value') 
            if tf_gs==0 and tf_py!=0:
                r=(receiving_comp,sending_comp,tf_gs,tf_py,'Py TF Incorrectly Has NonZero Value')
            if tf_gs!=0 and tf_py!=0:
                r=(receiving_comp,sending_comp,tf_gs,tf_py,tf_gs/tf_py)
                
        op.append(r)
        
df_op=pd.DataFrame(op,columns=['Receiving Compartment','Sending Compartment','GS_TF','Py_TF','Ratio']) 

# df_op.to_excel(os.path.join(ifp_py,'TransferMatrix_Comparsion.xlsx'),index=False)
                
               
missing_comps=pd.DataFrame(set(comps_gs)-set(comps_py),columns=['Present in GS but not in Py'])

extra_comps=pd.DataFrame(set(comps_py)-set(comps_gs),columns=['Present in Py but not in GS'])

rc_not_found=pd.DataFrame(df_op.loc[df_op.Ratio=='Receiving compartment not found']['Receiving Compartment'].unique(),columns=['GS Receiving Comp Not Found'])
            
sc_not_found=pd.DataFrame(df_op.loc[df_op.Ratio=='Sending compartment not found']['Sending Compartment'].unique(),columns=['GS Sending Comp Not Found'])
            
zero_vals=df_op.loc[df_op.Ratio=='Py TF Incorrectly Has Zero Value']    

nonzero_vals=df_op.loc[df_op.Ratio=='Py TF Incorrectly Has NonZero Value']    

dft=df_op[pd.to_numeric(df_op.Ratio, errors='coerce').notnull()] # numeric only

inaccurate_vals=dft.loc[(dft.Ratio>1.05) | (dft.Ratio<0.95)]    

accurate_vals=dft.loc[(dft.Ratio<=1.05) & (dft.Ratio>=0.95)]    

writer = pd.ExcelWriter(os.path.join(ifp_py,'TransferMatrix_Comparsion.xlsx'), engine="xlsxwriter")
df_op.to_excel(writer, sheet_name="Verbose",index=False)
missing_comps.to_excel(writer, sheet_name="Missing Comps",index=False)
extra_comps.to_excel(writer, sheet_name="Extra Comps",index=False)
rc_not_found.to_excel(writer, sheet_name="Receiving Comp Not Found",index=False)
sc_not_found.to_excel(writer, sheet_name="Sending Comp Not Found",index=False)
zero_vals.to_excel(writer, sheet_name="Incorrect Zero TFs",index=False)
nonzero_vals.to_excel(writer, sheet_name="Incorrect NonZero TFs",index=False)
inaccurate_vals.to_excel(writer, sheet_name="Inaccurate TFs",index=False)
accurate_vals.to_excel(writer, sheet_name="Accurate TFs",index=False)

writer.close()
