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

    if 'sink' in comp1_name: # sinks dont send chemical. Make this more robust to cover names like Helsinki
        return (link, app_algs)

    if 'air' in comp1_name: # air compartment only receive dont send chemical. Make this more robust to cover names like Clair
        return (link, app_algs)

    comp1,comp2=comp_objects_dict[comp1_name],comp_objects_dict[comp2_name]    
    df_alg_mat,df_psalg_mat,df_links=dict_inputs['df_alg_mat'],dict_inputs['df_psalg_mat'],dict_inputs['df_links']


    # ## check if pseudo source sending comparting and surface receiving compartment (cond3)
    # if ("vaporsource" in comp1.name or "particlesource" in comp1.name) and ("surface_water" in comp2.name or "surface_soil" in comp2.name) and (comp1.name.split('_')[-1]==comp2.name.split('_')[-1]): # final 'and' condition tests for identical parcel names
    #     cond3=True # pseudo source compartment connected to surface water or surface soil
    # else: 
    #     cond3=False
    # if cond3: # check if pseudo source algorithm -- mutually exclusive from conditions 1,2 and 4
    #     df_psalgs=dict_inputs['df_psalgs']
    #     psalgs=list(df_psalgs['algorithm'])
    #     app_algs=[x for x in psalgs if ('surface_water' in comp2.name and 'surface water' in x)] # temp -- need to fix
    #     return(cond3,[-1]) # temp -1 indicates pseudo source algs to surface water        

    ## check if pseudo source sending comparting and surface receiving compartment (cond3) -- mutually exclusive from conditions 1,2 and 4
    if ("vaporsource" in comp1.name or "particlesource" in comp1.name) and ("surface_water" in comp2.name or "soil_surface" in comp2.name) and (comp1.name.split('_')[-1]==comp2.name.split('_')[-1]): # final 'and' condition tests for identical parcel names
        cond3=True # pseudo source compartment connected to surface water or surface soil in same parcel
    elif ("vaporsource" in comp1.name) and ("leaf" in comp2.name and "particle" not in comp2.name ) and (comp1.name.split('_')[-1]==comp2.name.split('_')[-1]):
        cond3=True # vapor sources connected to leaf compartments in same parcel
    elif ("particlesource" in comp1.name) and ("particle" in comp2.name ) and (comp1.name.split('_')[-1]==comp2.name.split('_')[-1]):
        cond3=True # particle sources connected to leaf particle compartments in same parcel
    else: 
        cond3=False
    if cond3: # check which ps algorithms apply 
        if "surface_water" in comp2.name:  # algorithm sending compartment for surface water is just pseudosource unlike others          
            df_ps_app=df_psalg_mat.loc[(df_psalg_mat['sendingcompartmentcategory'].str.contains("pseudosource")) & (df_psalg_mat['receivingcompartmentcategory']==comp2.category) & (df_psalg_mat['enabled']=='True')] # if the algorithm's compartment categories equal the sending and receiving compartment categories and alg is enabled, then include
            # df_ps_app=df_psalg_mat.loc[(df_psalg_mat['sendingcompartmentcategory']=="pseudosource") & (df_psalg_mat['receivingcompartmentcategory']==comp2.category) & (df_psalg_mat['enabled']=='True')] # if the algorithm's compartment categories equal the sending and receiving compartment categories and alg is enabled, then include
        elif ("leaf" in comp2.name and "particle" not in comp2.name): # filter for leaf algorithms
            df_ps_app=df_psalg_mat.loc[(df_psalg_mat['sendingcompartmentcategory'].str.contains("vapor")) & (df_psalg_mat['receivingcompartmentcategory']=='terrestrial plant | leaf') & (df_psalg_mat['enabled']=='True')] # if the algorithm's compartment categories equal the sending and receiving compartment categories and alg is enabled, then include
        elif ("particle" in comp2.name): # filter for leaf particle algorithms 
            df_ps_app=df_psalg_mat.loc[(df_psalg_mat['sendingcompartmentcategory'].str.contains("particle")) & (df_psalg_mat['receivingcompartmentcategory']=='terrestrial plant | leaf particle') & (df_psalg_mat['enabled']=='True')] # if the algorithm's compartment categories equal the sending and receiving compartment categories and alg is enabled, then include
            
        else:
            df_ps_app=df_psalg_mat.loc[(df_psalg_mat['sendingcompartmentcategory']==comp1.category) & (df_psalg_mat['receivingcompartmentcategory']==comp2.category) & (df_psalg_mat['enabled']=='True')] # if the algorithm's compartment categories equal the sending and receiving compartment categories and alg is enabled, then include

        ## additional condition to match dry to dry and wet to wet only
        if ('dryvapor' in comp1.name and ('leaf' in comp2.name or 'soil' in comp2.name)):
            df_ps_app=df_ps_app.loc[df_ps_app['sendingcompartmentcategory']=="pseudosource | dry | vapor"]
        elif ('wetvapor' in comp1.name and ('leaf' in comp2.name or 'soil' in comp2.name)):
            df_ps_app=df_ps_app.loc[df_ps_app['sendingcompartmentcategory']=="pseudosource | wet | vapor"]
        if ('dryparticle' in comp1.name and ('leaf' in comp2.name or 'soil' in comp2.name)):
            df_ps_app=df_ps_app.loc[df_ps_app['sendingcompartmentcategory']=="pseudosource | dry | particle"]
        elif ('wetparticle' in comp1.name and ('leaf' in comp2.name or 'soil' in comp2.name)):
            df_ps_app=df_ps_app.loc[df_ps_app['sendingcompartmentcategory']=="pseudosource | wet | particle"]

            
        
        ps_app_algs=[] 

        if len (df_ps_app)>0:
            psalgs_non_chem1=list(df_ps_app.loc[(df_ps_app['chemical_category']=='all')]['index']) # ps algorithms that apply to all
            ps_app_algs.append(psalgs_non_chem1)
            
            chemcat=currentchemical.category.split('|')[0].strip() # get chemical category of current chemical
            if chemcat[-1]=='s':
                chemcat=chemcat[:-1] # strip s plural
            psalgs_non_chem2=list(df_ps_app.loc[(df_ps_app['sendingchemicalname']=='')&(df_ps_app['receivingchemicalname']=='')&(df_ps_app['chemical_category'].str.contains(chemcat))]['index']) # ps algorithms that are chemical category specific (not a robust solution)
            ps_app_algs.append(psalgs_non_chem2)

            df_ps_app['sendingchemicalname']=df_ps_app['sendingchemicalname'].apply(clean_chem_names) # clean chem names
            df_ps_app['receivingchemicalname']=df_ps_app['receivingchemicalname'].apply(clean_chem_names) # clean chem names
            psalgs_chem=list(df_ps_app.loc[(df_ps_app['sendingchemicalname']==currentchemical.name)&(df_ps_app['receivingchemicalname']==currentchemical.name)]['index']) # chemical specific ps algorithms 
            ps_app_algs.append(psalgs_chem) # list of applicable algorithms (indices)
            ps_app_algs=[y for x in ps_app_algs for y in x] # flatten list
            ps_app_algs=list(set(ps_app_algs)) # unique algorithm list in case of double counts
            ps_app_algs=[-1*x for x in ps_app_algs] # negative value for ps algs
            
        return(cond3,ps_app_algs) #        


    ## checki if compartments are in the same volume element (cond2) (but dont determine applicable algorithms yet)
    if comp1.containingvolumeelementname==comp2.containingvolumeelementname: # are the compartments in the same volume element? 
        cond2=True
    else:
        cond2=False
        
    ## check if manual links  exist    
    df_mlinks=df_links.loc[(df_links['sending_compartment_new']==comp1_name) & (df_links['receiving_compartment_new']==comp2_name)] # filter links dataframe to see if any rows correspond
    if len(df_mlinks)>0: # if there are connecting algorithms
        man_alg_names=list(df_mlinks['algorithm_new'].unique()) # get list of unique connecting algorithms names
        man_algs=[] # list of manual algorithm indices
        for al in man_alg_names:
            alg_ind=df_alg_mat.loc[(df_alg_mat['alg_name_new']==al) & (df_alg_mat['enabled']=='True'),'index'].values[0]
            man_algs.append(alg_ind)       
        cond4=True 
    else:
        cond4=False
    if cond4: # if there are manual connections determine algorithms that apply
        app_algs=app_algs+man_algs # add manual connections
        app_algs=list(set(app_algs)) # unique algorithm list in case of double counts


    if cond2 or cond3 or cond4: # only if cond2,3,4 do not apply, check if compartments are in neighboring vol elements. (in some cases, physically contiguous compartments wont be checked because they are already manually connected -- not sure if this is restrictive)
        cond1=False
    else:
        cond1=check_neighbor(comp1,comp2,dict_inputs).is_neighbor()[0] # are the compartments in neighboring volume elements?
        if cond1:
            if ('leaf' in comp1.name or 'soil' in comp1.name or 'surface_water' in comp1.name) and 'air' in comp2.name and  (comp1.name.split('_')[-1]!=comp2.name.split('_')[-1]): # leaf components should connect only to overlying air parcels not neighboring air parcels. This may be too restrictive -- replace with is above approach
                cond1=False
            if ('leaf' in comp1.name or 'particle' in comp1.name) and 'soil_surface' in comp2.name and  (comp1.name.split('_')[-1]!=comp2.name.split('_')[-1]): # leaf components should connect only to underlying surface soil parcels not neighboring air parcels. This may be too restrictive -- replace with is above approach
                cond1=False


    ### make list of applicable algorithms based on conditions 1 and 2 

    if cond1 or cond2:    ### THIS NEEDS A MORE ROBUST FILTERING APPROACH. TOO MANY IFS.
        df_app=df_alg_mat.loc[(df_alg_mat['sendingcompartmentcategory']==comp1.category) & (df_alg_mat['receivingcompartmentcategory']==comp2.category) & (df_alg_mat['enabled']=='True')] # if the algorithm's compartment categories equal the sending and receiving compartment categories and alg is enabled, then include
        if 'abiotic' in comp1.category and 'abiotic' in comp2.category: # to cover exception where comp1 category is abiotic | something but alg sending category is just abiotic
            df_app2=df_alg_mat.loc[(df_alg_mat['sendingcompartmentcategory']=="abiotic") & (df_alg_mat['receivingcompartmentcategory']=='abiotic') & (df_alg_mat['enabled']=='True')]
            df_app=df_app.append(df_app2)
        if 'fish' in comp1.category and 'abiotic' in comp2.category: # to cover cases where comp1 category = fish | something but sending algorithm category is just fish
            df_app2=df_alg_mat.loc[(df_alg_mat['sendingcompartmentcategory']=="fish") & (df_alg_mat['receivingcompartmentcategory']==comp2.category) & (df_alg_mat['enabled']=='True')]
            df_app=df_app.append(df_app2)
        if 'fish' in comp2.category and 'abiotic' in comp1.category: # to cover cases where comp2 category = fish | something but algorithm receiving comp category is just fish
            df_app2=df_alg_mat.loc[(df_alg_mat['receivingcompartmentcategory']=="fish") & (df_alg_mat['sendingcompartmentcategory']==comp2.category) & (df_alg_mat['enabled']=='True')]
            df_app=df_app.append(df_app2)   
        if 'leaf' in comp1.category and 'particle' not in comp1.category: # to cover cases where comp1 category is terrestrial plant | leaf | something but algorithm receiving comp category is just terrestrial plant | leaf |
            df_app2=df_alg_mat.loc[(df_alg_mat['sendingcompartmentcategory']=="terrestrial plant | leaf") & (df_alg_mat['receivingcompartmentcategory']==comp2.category) & (df_alg_mat['enabled']=='True')]
            df_app=df_app.append(df_app2) 
        if 'particle' in comp1.category: # to cover cases where comp1 category is terrestrial plant | leaf particle| something but algorithm receiving comp category is just terrestrial plant | leaf particle|
            df_app2=df_alg_mat.loc[(df_alg_mat['sendingcompartmentcategory']=="terrestrial plant | leaf particle") & (df_alg_mat['receivingcompartmentcategory']==comp2.category) & (df_alg_mat['enabled']=='True')]
            df_app=df_app.append(df_app2) 
        if 'leaf' in comp1.category and 'particle' in comp2.category: # to cover cases where comp1 category is terrestrial plant | leaf | something and comp2 category is terrestrial plant | leaf particle|
            df_app2=df_alg_mat.loc[(df_alg_mat['sendingcompartmentcategory']=="terrestrial plant | leaf") &(df_alg_mat['receivingcompartmentcategory']=="terrestrial plant | leaf particle") & (df_alg_mat['enabled']=='True')]
            df_app=df_app.append(df_app2) 
        if 'particle' in comp1.category and 'leaf' in comp2.category: # to cover cases where comp1 category is terrestrial plant | leaf particle| something and comp2 category is terrestrial plant | leaf | something
            df_app2=df_alg_mat.loc[(df_alg_mat['sendingcompartmentcategory']=="terrestrial plant | leaf particle") &(df_alg_mat['receivingcompartmentcategory']=="terrestrial plant | leaf") & (df_alg_mat['enabled']=='True')]
            df_app=df_app.append(df_app2) 
        if 'leaf' in comp1.category and 'leaf' in comp2.category: # to cover cases where comp1 category is terrestrial plant | leaf | something and comp2 category is terrestrial plant | leaf |
            df_app2=df_alg_mat.loc[(df_alg_mat['sendingcompartmentcategory']=="terrestrial plant | leaf") &(df_alg_mat['receivingcompartmentcategory']=="terrestrial plant | leaf") & (df_alg_mat['enabled']=='True')]
            df_app=df_app.append(df_app2) 
        if 'particle' in comp1.category and 'particle' in comp2.category: # to cover cases where comp1 category is terrestrial plant | leaf particle| something and comp2 category is terrestrial plant | leaf | something
            df_app2=df_alg_mat.loc[(df_alg_mat['sendingcompartmentcategory']=="terrestrial plant | leaf particle") &(df_alg_mat['receivingcompartmentcategory']=="terrestrial plant | leaf particle") & (df_alg_mat['enabled']=='True')]
            df_app=df_app.append(df_app2) 



        
        # if len (df_app)>0:
        #     algs_non_chem=list(df_app.loc[(df_app['sendingchemicalname']=='replaceme') | (df_app['chemical_category']=='all')]['index']) # algorithms that are not chemical specific --not a robust filter
        #     app_algs.append(algs_non_chem)
        #     df_app['sendingchemicalname']=df_app['sendingchemicalname'].apply(clean_chem_names) # clean chem names
        #     df_app['receivingchemicalname']=df_app['receivingchemicalname'].apply(clean_chem_names) # clean chem names
        #     algs_chem=list(df_app.loc[(df_app['sendingchemicalname']==currentchemical.name)&(df_app['receivingchemicalname'].isin(chem_list_clean))]['index']) # chemical specific algorithms 
        #     app_algs.append(algs_chem) # list of applicable algorithms (indices)
        #     chemcat_parse=currentchemical.category.split('|') # parse chemical category
        #     if len(chemcat_parse)>1:
        #         chemcat_filter1=currentchemical.category
        #         algs_chem1=list(df_app.loc[df_app['chemical_category']==chemcat_filter1]['index']) # chemical category specific algorithms e.g. metals
        #         app_algs.append(algs_chem1) # list of applicable algorithms (indices)
        #     if len(chemcat_parse)>2:
        #         chemcat_filter2=chemcat_parse[0]+" | "+ chemcat_parse[0] #(e.g. to get 'metals | mercury')
        #         algs_chem2=list(df_app.loc[df_app['chemical_category']==chemcat_filter2]['index']) # chemical category specific algorithms e.g. metals | mercury
        #         app_algs.append(algs_chem2) # list of applicable algorithms (indices) 
        #     app_algs=[y for x in app_algs for y in x] # flatten list
        #     app_algs=list(set(app_algs)) # unique algorithm list in case of double counts

        # reworking chemical specific filter above -- needs more robust approach

        if len (df_app)>0:
            df_app['sendingchemicalname'] = df_app['sendingchemicalname'].str.replace(r'benzo\(a\)pyrene','replaceme')# fix to handle litterfall algorithm which for some reason is limited to BaP
            df_app['receivingchemicalname'] = df_app['receivingchemicalname'].str.replace(r'benzo\(a\)pyrene','replaceme')# fix to handle litterfall algorithm which for some reason is limited to BaP

            algs_non_chem=list(df_app.loc[(df_app['sendingchemicalname']=='replaceme') & (df_app['chemical_category']=='all')]['index']) # algorithms that are not chemical specific --not a robust filter
            app_algs.append(algs_non_chem)
            df_app['sendingchemicalname']=df_app['sendingchemicalname'].apply(clean_chem_names) # clean chem names
            df_app['receivingchemicalname']=df_app['receivingchemicalname'].apply(clean_chem_names) # clean chem names
            algs_chem=list(df_app.loc[(df_app['sendingchemicalname']==currentchemical.name)&(df_app['receivingchemicalname'].isin(chem_list_clean))]['index']) # chemical specific algorithms  filtered by receiving and sending categories
            app_algs.append(algs_chem) # list of applicable algorithms (indices)
            chemcat_parse=currentchemical.category.split('|') # parse chemical category
            chemcat_parse=[c.strip() for c in chemcat_parse]
            if len(chemcat_parse)>1: # if multiple terms separated by |
                chemcat_filter1=currentchemical.category # first filter on the whole category as is
                algs_chem1=list(df_app.loc[df_app['chemical_category']==chemcat_parse[0]]['index']) # Filter on first term e.g. metals
                app_algs.append(algs_chem1) # list of applicable algorithms (indices)
            if len(chemcat_parse)>=2: # e.g. metals | mercury
                chemcat_filter2=chemcat_parse[0]+" | "+ chemcat_parse[1] #(e.g. to get 'metals | mercury')
                algs_chem2=list(df_app.loc[df_app['chemical_category']==chemcat_filter2]['index']) # filter on first and second terms e.g. metals | mercury
                app_algs.append(algs_chem2) # list of applicable algorithms (indices) 
            
            algs_chem3=list(df_app.loc[df_app['chemical_category']==currentchemical.category]['index']) #   filter on the whole category e.g. metals | mercury | elemental mercury  
            app_algs.append(algs_chem3)
            
            app_algs=[y for x in app_algs for y in x] # flatten list
            app_algs=list(set(app_algs)) # unique algorithm list in case of double counts

    ## check if there are manual links
    

    if len(app_algs)>0: 
        return(True,app_algs)
    else:
        return(False, app_algs)        

        

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
    df_psalg_mat=dict_inputs['df_psalg_mat']      # DataFrame of applicable algorithms for combination of sending and receiving compartment types

    
    ind_name=[] # index name for tm, sm DataFrames
#    for chem_index, chem in enumerate(chem_list_clean[:1]): # loop over chemicals
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
                        # if alg==-1: # temp
                        #     alg_name='direct_transfer_from_pseudosource_to_surface_water' # temp
                        # else:    
                        #     alg_name=df_alg_mat.loc[df_alg_mat['index']==alg,'alg_name_new'].values[0]# lookup alg name by index in df_alg_mat
                        if alg<0: # ps algorithm
                            alg_name=df_psalg_mat.loc[df_psalg_mat['index']==-1*alg,'alg_name_new'].values[0]# lookup alg name by index in df_alg_mat
                        else:    
                            alg_name=df_alg_mat.loc[df_alg_mat['index']==alg,'alg_name_new'].values[0]# lookup alg name by index in df_alg_mat

                        alg_class=eval(alg_name) # temporary -- get rid of eval eventually by placing algorithm objects in a dictionary
                        sendingcompartment=comp_objects_dict[comp_row] # sending compartment object
                        receivingcompartment=comp_objects_dict[comp_col] # receiving compartment object     
                        # print (sendingcompartment.name,receivingcompartment.name)
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
     

# row_index=27
# col_index=24
# comp_row=comp_list[row_index]
# comp_col=comp_list[col_index]
# comp1_name=comp_row
# comp2_name=comp_col   

# row_index=56
# col_index=52
# comp_row=comp_list[row_index]
# comp_col=comp_list[col_index]
# comp1_name=comp_row
# comp2_name=comp_col  

# row_index=125
# col_index=22
# comp_row=comp_list[row_index]
# comp_col=comp_list[col_index]
# comp1_name=comp_row
# comp2_name=comp_col  