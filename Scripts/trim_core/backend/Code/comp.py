# -*- coding: utf-8 -*-
"""

Created on Wed Mar 31 21:15:14 2021
@author: 13963

## Added a few temporary if conditions to limit to sediment and surface water system

1) Parses compartments text file and stores as dataframe
2) Auto write script to instantiate comparment objects, specifically define_comp.py


"""

import pandas as pd
import os
import required_elements_temp as req

def define_compartments(inputs,df_parcels,df_ve,df_pve,df_props,df_dr):


    ifp=inputs['path_inputs']
    ifn=inputs['comp_file']    
    ifpn=os.path.join(ifp,ifn)
    
    
    comp_file=open(ifpn,'r') 
    comp_lines=comp_file.readlines()
    
    comp_dict={}
    counter=0
    #### Read Compartments
    
    comp_tuples=[] # initialize list for storing point lines
    
    for line in comp_lines: # loop over lines 
        line=line.strip()        
        line_nc=line.split("//")[0] # line stripped of comment
        if line_nc[:14]=="VolumeElement:":
            ve=line_nc.split(":")[1].strip()
        elif line_nc[:12]=="Compartment:":   
            comp=line_nc.split(":")[1].strip()
            c=(ve,comp,'')
            comp_tuples.append(c)
        elif line_nc[:21]=="CompositeCompartment:":   
            ccomp=line_nc.split(":")[1].strip()
            c=(ve,'',ccomp)
            comp_tuples.append(c)        
    df_comp=pd.DataFrame(comp_tuples,columns=['VE_Name', 'Compartment', 'CompositeCompartment'])
    df_comp=df_comp.merge(df_ve,how='left',on='VE_Name') # merge in ve_fields

    
    
    ################################# WRITE PYTHON SCRIPT TO INSTANTIATE COMPARTMENTS 
    
    required_comp_classes=req.required_compartments      
    required_comp_classes=[x.lower() for x in required_comp_classes]  
    
    ofp=inputs['path_code']
    ofn=r'define_comp.py'
    ofpn=os.path.join(ofp,ofn)
    
    with open(ofpn, 'w') as f:     
        f.write('''\

from constants import *
from define_scenario import *
from define_ve import *
from define_pve import *
from define_chem_classes import *
from define_comp_classes import *
from define_attributes_props import *

def define_comp(currentChemical):

    ''')
        
        for i in range(len(df_comp)):
            if str(df_comp.loc[i,'Primary_Abiotic']).lower() not in required_comp_classes or str(df_comp.loc[i,'Parcel_Name']) !='LakeCadillac': # temp
               continue
            ve_name=df_comp.loc[i,'VE_Name'] # volume element name
            parcel_name=ve_name.split('_')[1] # parcel name
            parcel_points=df_parcels['Point_IDs'].loc[df_parcels['Parcel_Name']==parcel_name].values[0] # parcel points
            parcel_area=df_parcels['Parcel_Area'].loc[df_parcels['Parcel_Name']==parcel_name].values[0] # parcel area
            exterior_boundary=df_parcels['External_Boundary'].loc[df_parcels['Parcel_Name']==parcel_name].values[0] # parcel exterior boundary
            comp_names=[]
            if df_comp.loc[i,'Compartment']!='':
                if str(df_comp.loc[i,'Compartment']).lower() not in required_comp_classes: # temp
                   continue

                comp_name=str(df_comp.loc[i,'Compartment']).replace(r'/','_').replace(r'-','_').replace(' ','_')+'_in_'+str(df_comp.loc[i,'VE_Name'])
                comp_class=str(df_comp.loc[i,'Compartment']).replace(r'/','_').replace(r'-','_').replace(' ','_')
                comp_name_class=(comp_name,comp_class)
                comp_names.append(comp_name_class)
                
#                print (comp_name_class)
            elif df_comp.loc[i,'CompositeCompartment']!='':
                compo=str(df_comp.loc[i,'CompositeCompartment']).replace(r'/','_').replace(r'-','_').replace(' ','_')
                if compo in ['Deciduous_Forest','Coniferous_Forest']:
                    plant_parts=['Leaf','Leaf_Particle'] # no root or stem -- not sure why this is so in TRIM
                else:
                    plant_parts=['Leaf','Leaf_Particle','Root','Stem']
    
                for part in plant_parts:
                    comp_name=part+'_'+compo+'_in_'+str(df_comp.loc[i,'VE_Name'])
                    comp_class=part+'_'+compo+'_in_'+compo
                    comp_name_class=(comp_name,comp_class)
                    comp_names.append(comp_name_class)
#                    print (comp_name_class)
    
            for comp_name_cl in comp_names:            
                comp_name=comp_name_cl[0]
                comp_class=comp_name_cl[1]
    #            if comp_class in locals():
    #                print (comp_class)
                comp_dict[counter]=comp_name
                counter+=1
                f.write('\n\t'+\
                    str(comp_name)+\
                    '=' +\
                    comp_class+\
                    '(Constants,containingScenario,currentChemical,'+\
                    str(ve_name)+\
                    ')')
                f.write('\n\t'+\
                        str(comp_name)+\
                        '.'+\
                        'Name='+\
                        '"'+ comp_name+'"'+\
                        '\n\t'+\
                        str(comp_name)+\
                        '.'+\
                        'containingVolumeElement='+\
                         '"'+ve_name+'"'+\
                        '\n\t'+\
                        str(comp_name)+\
                        '.'+\
                        'Parcel_Name='+\
                        '"'+parcel_name+'"'+\
                        '\n\t'+\
                        str(comp_name)+\
                        '.'+\
                        'Parcel_Points='+\
                        '"'+parcel_points+'"'+\
                        '\n\t'+\
                        str(comp_name)+\
                        '.'+\
                        'Parcel_Area='+\
                        str(parcel_area)+\
                        '\n\t'+\
                        str(comp_name)+\
                        '.'+\
                        'Exterior_Boundary='+\
                        str(exterior_boundary))
                f.write('\n\t')
    
            
    
    ################################# APPEND TO PYTHON SCRIPT TO INSTANTIATE PRIMARY ABIOTIC COMPARTMENTS -- must first have df_ve in memory (run vol_elem.py)
    
    with open(ofpn, 'a') as f:
        f.write('### Note: This is an auto generated script' +'\n')        
        for i in range(len(df_ve)):
            ve_name=str(df_ve.loc[i,'VE_Name'].replace(r'/','_').replace(r'-','_').replace(' ','_'))
            parcel_name=ve_name.split('_')[1] # parcel name
            parcel_points=df_parcels['Point_IDs'].loc[df_parcels['Parcel_Name']==parcel_name].values[0] # parcel points
            parcel_area=df_parcels['Parcel_Area'].loc[df_parcels['Parcel_Name']==parcel_name].values[0] # parcel area
            exterior_boundary=df_parcels['External_Boundary'].loc[df_parcels['Parcel_Name']==parcel_name].values[0] # parcel exterior boundary
            primary_abiotic=str(df_ve.loc[i,'Primary_Abiotic']).lower() # temp
            if primary_abiotic not in required_comp_classes or str(df_ve.loc[i,'Parcel_Name']) !='LakeCadillac': # temp: #  temp
               continue # temp           
            comp_name=str(df_ve.loc[i,'Primary_Abiotic'].replace(r'/','_').replace(r'-','_').replace(' ','_')) + '_in_' + str(df_ve.loc[i,'VE_Name'].replace(r'/','_').replace(r'-','_').replace(' ','_')) 
            comp_name=str(comp_name.replace('___','_').replace('__','_'))
            comp_class=str(df_ve.loc[i,'Primary_Abiotic'].replace(r'/','_').replace(r'-','_').replace(' ','_'))
            comp_class=str(comp_class.replace('___','_').replace('__','_'))
            comp_dict[counter]=comp_name
            counter+=1
    
            f.write('\n\t'+\
                str(comp_name)+\
                '=' +\
                comp_class+\
                '(Constants,containingScenario,currentChemical,'+\
                str(ve_name)+\
                ')')
            f.write('\n\t'+\
                        str(comp_name)+\
                        '.'+\
                        'Name='+\
                        '"'+ comp_name+'"'+\
                        '\n\t'+\
                        str(comp_name)+\
                        '.'+\
                        'containingVolumeElement='+\
                         '"'+ve_name+'"'+\
                        '\n\t'+\
                        str(comp_name)+\
                        '.'+\
                        'Parcel_Name='+\
                        '"'+parcel_name+'"'+\
                        '\n\t'+\
                        str(comp_name)+\
                        '.'+\
                        'Parcel_Points='+\
                        '"'+parcel_points+'"'+\
                        '\n\t'+\
                        str(comp_name)+\
                        '.'+\
                        'Parcel_Area='+\
                        str(parcel_area)+\
                        '\n\t'+\
                        str(comp_name)+\
                        '.'+\
                        'Exterior_Boundary='+\
                        str(exterior_boundary))
            f.write('\n\t')
    
    
    
    
    
    ###### APPEND CODE TO AUTO DEFINE ADVECTION SINKS
    
    df_sinks=df_ve.loc[((df_ve.Primary_Abiotic=='Air')|(df_ve.Primary_Abiotic=='Soil - Surface'))&(df_ve.External_Boundary)>0] # only air and surface soil compartments with an outer boundary need sinks
    
    with open(ofpn, 'a') as f:
        for i in df_sinks.index:
            primary_abiotic=str(df_sinks.loc[i,'Primary_Abiotic']).lower() # temp
            if primary_abiotic not in required_comp_classes: #  temp
               continue # temp    
            ve_name=str(df_sinks.loc[i,'VE_Name'].replace(r'/','_').replace(r'-','_').replace(' ','_'))
            parcel_name=ve_name.split('_')[1] # parcel name
            parcel_points=df_parcels['Point_IDs'].loc[df_parcels['Parcel_Name']==parcel_name].values[0] # parcel points
            parcel_area=df_parcels['Parcel_Area'].loc[df_parcels['Parcel_Name']==parcel_name].values[0] # parcel area
            exterior_boundary=df_parcels['External_Boundary'].loc[df_parcels['Parcel_Name']==parcel_name].values[0] # parcel exterior boundary
            comp_name='Sink_in_Sink_for_'+str(df_ve.loc[i,'Primary_Abiotic'].replace(r'/','_').replace(r'-','_').replace(' ','_')) + '_in_' + str(df_ve.loc[i,'VE_Name'].replace(r'/','_').replace(r'-','_').replace(' ','_')) 
            comp_name=str(comp_name.replace('___','_').replace('__','_'))
            primary_abiotic=df_sinks.loc[i,'Primary_Abiotic']
            if primary_abiotic=='Air':
                comp_class='Advection_Sink'
            elif primary_abiotic=='Soil - Surface':
                comp_class='Soil_Advection_Sink'
            comp_dict[counter]=comp_name
            counter+=1
            f.write('\n\t'+\
                str(comp_name)+\
                '=' +\
                comp_class+\
                '(Constants,containingScenario,currentChemical,'+\
                str(ve_name)+\
                ')')
            f.write('\n\t'+\
                        str(comp_name)+\
                        '.'+\
                        'Name='+\
                        '"'+ comp_name+'"'+\
                        '\n\t'+\
                        str(comp_name)+\
                        '.'+\
                        'containingVolumeElement='+\
                         '"'+ve_name+'"'+\
                        '\n\t'+\
                        str(comp_name)+\
                        '.'+\
                        'Parcel_Name='+\
                        '"'+parcel_name+'"'+\
                        '\n\t'+\
                        str(comp_name)+\
                        '.'+\
                        'Parcel_Points='+\
                        '"'+parcel_points+'"'+\
                        '\n\t'+\
                        str(comp_name)+\
                        '.'+\
                        'Parcel_Area='+\
                        str(parcel_area)+\
                        '\n\t'+\
                        str(comp_name)+\
                        '.'+\
                        'Exterior_Boundary='+\
                        str(exterior_boundary))
            f.write('\n\t')
    
    
    
    
    ################################# APPEND PYTHON SCRIPT TO INSTANTIATE PSEUDO PRIMARY ABIOTIC COMPARTMENTS -- must first have df_pve in memory (run vol_elem.py)
    
    with open(ofpn, 'a') as f:
        f.write('\n\t' + 'class Pseudo_Compartment:')
        f.write('\n\t\t' + 'pass' +'\n')

        for i in range(len(df_pve)):
            if str(df_pve.loc[i,'Parcel_Name'])!="LakeCadillac":  # temp
                continue
        
            pve_name=str(df_pve.loc[i,'VE_Name'].replace(r'/','_').replace(r'-','_').replace(' ','_'))
            parcel_name=pve_name.split('_')[1] # parcel name
            parcel_points=df_parcels['Point_IDs'].loc[df_parcels['Parcel_Name']==parcel_name].values[0] # parcel points
            parcel_area=df_parcels['Parcel_Area'].loc[df_parcels['Parcel_Name']==parcel_name].values[0] # parcel area
            exterior_boundary=df_parcels['External_Boundary'].loc[df_parcels['Parcel_Name']==parcel_name].values[0] # parcel exterior boundary
            comp_name=str(df_pve.loc[i,'Primary_Abiotic'].replace(r'/','_').replace(r'-','_').replace(' ','_')) + '_in_' + str(df_pve.loc[i,'VE_Name'].replace(r'/','_').replace(r'-','_').replace(' ','_')) 
            comp_name=str(comp_name.replace('___','_').replace('__','_'))
            comp_dict[counter]=comp_name
            counter+=1
            
            prim_abiotic_name=str(df_pve.loc[i,'Primary_Abiotic'].replace(r'/','_').replace(r'-','_').replace(' ','_'))
            if prim_abiotic_name=="DryVaporSource":
                comp_category="Deposition | Dry | Vapor"
            if prim_abiotic_name=="WetVaporSource":
                comp_category="Deposition | Wet | Vapor"
            if prim_abiotic_name=="DryParticleSource":
                comp_category="Deposition | Dry | Particle"
            if prim_abiotic_name=="WetParticleSource":
                comp_category="Deposition | Wet | Particle"

            f.write('\n\t'+\
                        str(comp_name)+'=Pseudo_Compartment()'+'\n\t'+\
                        str(comp_name)+\
                        '.'+\
                        'Name='+\
                        '"'+ comp_name+'"'+\
                        '\n\t'+\
                        str(comp_name)+\
                        '.'+\
                        'containingVolumeElement='+\
                         '"'+pve_name+'"'+\
                        '\n\t'+\
                        str(comp_name)+\
                        '.'+\
                        'Parcel_Name='+\
                        '"'+parcel_name+'"'+\
                        '\n\t'+\
                        str(comp_name)+\
                        '.'+\
                        'Parcel_Points='+\
                        '"'+parcel_points+'"'+\
                        '\n\t'+\
                        str(comp_name)+\
                        '.'+\
                        'Parcel_Area='+\
                        str(parcel_area)+\
                        '\n\t'+\
                        str(comp_name)+\
                        '.'+\
                        'Exterior_Boundary='+\
                        str(exterior_boundary)+\
                        '\n\t'+\
                        str(comp_name)+\
                        '.'+\
                        'Deposition_Rate={}'
                        )           
            f.write('\n\t'+str(comp_name)+'.category='+'"'+comp_category+'"')
            
            ### add compartment properties
            f.write('\n\n')
            for i in range(len(df_props)):
                if str(df_props.loc[i,'Prop_Type'])!='Compartment':
                    continue                
                if str(df_props.loc[i,'Prop_Owner']).split(' in ')[0].strip().lower() not in required_comp_classes: # temp
                   continue                
                
                obj=df_props.loc[i,'Prop_Owner_New']
                if True: # temporary. use condition below later.
        #        if obj in locals(): # may miss a few objects owing to name cleaning?
        #            print (obj)
                    f.write('\t'+'try:'+'\n\t\t')
                    f.write(str(obj)+\
                           "." +\
                           str(df_props.loc[i,'Property_New'])+\
                           "="+\
                           str(df_props.loc[i,'Value_New']))
                    f.write('\n'+'\t'+'except:'+'\n\t\t'+'pass') 
                    f.write('\n')            


    
    
        #### ADD DEPOSITION RATES AS PROPERTIES OF PSEUDO COMPARTMENTS
        f.write('\n'+'#Add pseudo source dep rates to pseudo compartments'+'\n\n')

        for i in range(len(df_dr)):
            obj=df_dr.loc[i,'Compartment']
            f.write('\t'+'try:'+'\n\t\t'+\
                    str(obj)+\
                   ".Deposition_Rate['" +\
                   str(df_dr.loc[i,'Chemical'])+\
                  "']="+\
                   str(df_dr.loc[i,'Surface Deposition Rate'])+\
                   '*'+\
                   obj+\
                   ".Parcel_Area"+'\n'\
                   '\t'+'except:'+'\n\t\t'+\
                   'pass')
            f.write('\n')            
    
                
                
        # write compartment objects dictionary        
        f.write('\n\n\t'+'comp_objects_dict={}'+'\n\t')   
        for k,v in comp_dict.items():
            f.write('comp_objects_dict['+'"'+str(v)+'"'+']='+str(v)+'\n\t')
            
        f.write('\n\t' +'return(comp_objects_dict)')

    f.close()
    
    return(df_comp,comp_dict)
    
if __name__ == '__main__':
    df_comp=define_compartments(inputs,df_parcels,df_ve,df_pve,df_props,df_dr)