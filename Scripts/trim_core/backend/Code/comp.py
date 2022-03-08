# -*- coding: utf-8 -*-
"""

created on wed mar 31 21:15:14 2021
@author: 13963

## added a single surface soil compartment n1
## added a few temporary if conditions to limit to sediment and surface water system

1) parses compartments text file and stores as DataFrame
2) auto write script to instantiate comparment objects, specifically define_comp.py


"""

import pandas as pd
import os
import required_elements_temp as req

parcel_list=['lakecadillac','lakemitchell','n1','nw1','sw1','w1','nw2','sw2','ne3','e2','e3','s1','se1','se2','e1','ne1','n2']

# parcel_list=['lakecadillac','lakemitchell','s1']



def define_compartments(inputs,df_parcels,df_ve,df_pve,df_props,df_dr):


    ifp=inputs['path_inputs']
    ifn=inputs['comp_file']    
    ifpn=os.path.join(ifp,ifn)
    
    
    comp_file=open(ifpn,'r') 
    comp_lines=comp_file.readlines()
    
    comp_dict={}
    counter=0
    #### read compartments
    
    comp_tuples=[] # initialize list for storing point lines
    
    for line in comp_lines: # loop over lines 
        line=line.strip()        
        line_nc=line.split("//")[0] # line stripped of comment
        if line_nc[:14]=="volumeelement:":
            ve=line_nc.split(":")[1].strip()
        elif line_nc[:12]=="compartment:":   
            comp=line_nc.split(":")[1].strip()
            c=(ve,comp,'')
            comp_tuples.append(c)
        elif line_nc[:21]=="compositecompartment:":   
            ccomp=line_nc.split(":")[1].strip()
            c=(ve,'',ccomp)
            comp_tuples.append(c)        
    df_comp=pd.DataFrame(comp_tuples,columns=['ve_name', 'compartment', 'compositecompartment'])
    df_comp=df_comp.merge(df_ve,how='left',on='ve_name') # merge in ve_fields


    required_comp_classes=req.required_compartments      
    required_comp_classes=[x.lower() for x in required_comp_classes]  
    
    ofp=inputs['path_code']
    ofn=r'define_comp.py'
    ofpn=os.path.join(ofp,ofn)


    ################################# append to python script to instantiate primary abiotic compartments -- must first have df_ve in memory (run vol_elem.py)
    
    with open(ofpn, 'w') as f:

        f.write('### note: this is an auto generated script' +'\n')        

        f.write('''\

from constants import *
from define_scenario import *
from define_ve import *
from define_pve import *
from define_chem_classes import *
from define_comp_classes import *
from define_attributes_props import *

def define_comp(currentchemical):

    ''')

        f.write('\n\t'+'comp_objects_dict={}'+'\n\t')               

        
        for i in range(len(df_ve)): # first write the primary abiotic compartments of each volume element
            ve_name=str(df_ve.loc[i,'ve_name'].replace(r'/','_').replace(r'-','_').replace(' ','_'))
            parcel_name=ve_name.split('_')[1] # parcel name
            parcel_points=df_parcels['point_ids'].loc[df_parcels['parcel_name']==parcel_name].values[0] # parcel points
            parcel_area=df_parcels['parcel_area'].loc[df_parcels['parcel_name']==parcel_name].values[0] # parcel area
            exterior_boundary=df_parcels['external_boundary'].loc[df_parcels['parcel_name']==parcel_name].values[0] # parcel exterior boundary
            primary_abiotic=str(df_ve.loc[i,'primary_abiotic']).lower() # temp
            if primary_abiotic not in required_comp_classes or (str(df_ve.loc[i,'parcel_name']) not in parcel_list): # temp: #  temp

            # if primary_abiotic not in required_comp_classes or (str(df_ve.loc[i,'parcel_name']) !='lakecadillac' and str(df_ve.loc[i,'parcel_name']) !='lakemitchell' and str(df_ve.loc[i,'parcel_name']) !='n1'): # temp: #  temp
               continue # temp           
            comp_name=str(df_ve.loc[i,'primary_abiotic'].replace(r'/','_').replace(r'-','_').replace(' ','_')) + '_in_' + str(df_ve.loc[i,'ve_name'].replace(r'/','_').replace(r'-','_').replace(' ','_')) 
            comp_name=str(comp_name.replace('___','_').replace('__','_'))
            comp_class=str(df_ve.loc[i,'primary_abiotic'].replace(r'/','_').replace(r'-','_').replace(' ','_'))
            comp_class=str(comp_class.replace('___','_').replace('__','_'))
            comp_dict[counter]=comp_name
            counter+=1
    
            f.write('\n\t'+\
                str(comp_name)+\
                '=' +\
                comp_class+\
                '(constants,containingscenario,currentchemical,'+\
                str(ve_name)+\
                ',comp_objects_dict'+\
                ')')
            f.write('\n\t'+\
                        str(comp_name)+\
                        '.'+\
                        'name='+\
                        '"'+ comp_name+'"'+\
                        '\n\t'+\
                        str(comp_name)+\
                        '.'+\
                        'containingvolumeelementname='+\
                         '"'+ve_name+'"'+\
                        '\n\t'+\
                        str(comp_name)+\
                        '.'+\
                        'parcel_name='+\
                        '"'+parcel_name+'"'+\
                        '\n\t'+\
                        str(comp_name)+\
                        '.'+\
                        'parcel_points='+\
                        '"'+parcel_points+'"'+\
                        '\n\t'+\
                        str(comp_name)+\
                        '.'+\
                        'parcel_area='+\
                        str(parcel_area)+\
                        '\n\t'+\
                        str(comp_name)+\
                        '.'+\
                        'exterior_boundary='+\
                        str(exterior_boundary))
            f.write('\n\t')
    
            f.write('\n\t'+'comp_objects_dict['+'"'+str(comp_name)+'"'+']='+comp_name+'\n')
    
    
    ################################# write python script to instantiate compartments 
    
    
    with open(ofpn, 'a') as f:     

        
        for i in range(len(df_comp)):
            
            if str(df_comp.loc[i,'primary_abiotic']).lower() not in required_comp_classes or (str(df_comp.loc[i,'parcel_name']) not in parcel_list):# temp

            # if str(df_comp.loc[i,'primary_abiotic']).lower() not in required_comp_classes or (str(df_comp.loc[i,'parcel_name']) !='lakecadillac' and str(df_comp.loc[i,'parcel_name']) !='lakemitchell'and str(df_comp.loc[i,'parcel_name']) !='n1'):# or str(df_comp.loc[i,'compositecompartment'])!="": # temp
               continue
            ve_name=df_comp.loc[i,'ve_name'] # volume element name
            parcel_name=ve_name.split('_')[1] # parcel name
            parcel_points=df_parcels['point_ids'].loc[df_parcels['parcel_name']==parcel_name].values[0] # parcel points
            parcel_area=df_parcels['parcel_area'].loc[df_parcels['parcel_name']==parcel_name].values[0] # parcel area
            exterior_boundary=df_parcels['external_boundary'].loc[df_parcels['parcel_name']==parcel_name].values[0] # parcel exterior boundary
            comp_names=[]
            if df_comp.loc[i,'compartment']!='': # if not a composite compartment
                if str(df_comp.loc[i,'compartment']).lower() not in required_comp_classes: # temp
                   continue

                comp_name=str(df_comp.loc[i,'compartment']).replace(r'/','_').replace(r'-','_').replace(' ','_')+'_in_'+str(df_comp.loc[i,'ve_name'])
                comp_class=str(df_comp.loc[i,'compartment']).replace(r'/','_').replace(r'-','_').replace(' ','_')
                comp_name_class=(comp_name,comp_class)
                comp_names.append(comp_name_class)
                
#                print (comp_name_class)
            elif df_comp.loc[i,'compositecompartment']!='':
                compo=str(df_comp.loc[i,'compositecompartment']).replace(r'/','_').replace(r'-','_').replace(' ','_')
                if compo in ['deciduous_forest','coniferous_forest']:
                    plant_parts=['leaf','leaf_particle'] # no root or stem -- not sure why this is so in trim
                else:
                    plant_parts=['leaf','leaf_particle','stem','root']
    
                for part in plant_parts:
                    comp_name=part+'_'+compo+'_in_'+str(df_comp.loc[i,'ve_name'])
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
                    '(constants,containingscenario,currentchemical,'+\
                    str(ve_name)+\
                ',comp_objects_dict'+\
                    ')')
                f.write('\n\t'+\
                        str(comp_name)+\
                        '.'+\
                        'name='+\
                        '"'+ comp_name+'"'+\
                        '\n\t'+\
                        str(comp_name)+\
                        '.'+\
                        'containingvolumeelementname='+\
                         '"'+ve_name+'"'+\
                        '\n\t'+\
                        str(comp_name)+\
                        '.'+\
                        'parcel_name='+\
                        '"'+parcel_name+'"'+\
                        '\n\t'+\
                        str(comp_name)+\
                        '.'+\
                        'parcel_points='+\
                        '"'+parcel_points+'"'+\
                        '\n\t'+\
                        str(comp_name)+\
                        '.'+\
                        'parcel_area='+\
                        str(parcel_area)+\
                        '\n\t'+\
                        str(comp_name)+\
                        '.'+\
                        'exterior_boundary='+\
                        str(exterior_boundary))
                f.write('\n\t')

## adding artefact to handle associated compartments for plant composites

                if 'leaf' in comp_name and 'particle' not in comp_name  and 'sink' not in comp_name: # applies to leaf composites only
                    soil_comp_name='soil_surface_in_'+comp_name.split('_in_')[1] # infer associated surface soil compartment name
                    f.write('\n\t'+\
                                    str(comp_name)+\
                                    '.'+\
                                    'associated_soil_comp='+\
                        			'comp_objects_dict['+'"'+str(soil_comp_name)+'"]'+'\n') 
                        
                        
                if 'particle' in comp_name and 'sink' not in comp_name: # applies to leaf particle composites only
                    soil_comp_name='soil_surface_in_'+comp_name.split('_in_')[1]
                    f.write('\n\t'+\
                        str(comp_name)+\
                        '.'+\
                        'associated_soil_comp='+\
             			'comp_objects_dict['+'"'+str(soil_comp_name)+'"]'+'\n')


                    leaf_comp_name=comp_name.split('_particle')[0]+comp_name.split('_particle')[1]
                    f.write('\n\t'+\
                        str(comp_name)+\
                        '.'+\
                        'associated_leaf_comp='+\
             			'comp_objects_dict['+'"'+str(leaf_comp_name)+'"]'+'\n')


                if 'stem' in comp_name and 'sink' not in comp_name: # applies to stem composites only
                    soil_comp_name='soil_surface_in_'+comp_name.split('_in_')[1]
                    f.write('\n\t'+\
                        str(comp_name)+\
                        '.'+\
                        'associated_soil_comp='+\
             			'comp_objects_dict['+'"'+str(soil_comp_name)+'"]'+'\n')


                    leaf_comp_name='leaf'+comp_name.split('stem')[1]
                    f.write('\n\t'+\
                        str(comp_name)+\
                        '.'+\
                        'associated_leaf_comp='+\
             			'comp_objects_dict['+'"'+str(leaf_comp_name)+'"]'+'\n')



                if 'root_' in comp_name and 'sink' not in comp_name: # applies to root composites only
                    soil_comp_name='soil_root_zone_in_rootsoil_'+comp_name.split('_in_')[1].split('_')[1] # pull out parcel name and attach to root soil
                    f.write('\n\t'+\
                        str(comp_name)+\
                        '.'+\
                        'associated_soil_comp='+\
             			'comp_objects_dict['+'"'+str(soil_comp_name)+'"]'+'\n')


                    stem_comp_name='stem'+comp_name.split('root')[1]
                    f.write('\n\t'+\
                        str(comp_name)+\
                        '.'+\
                        'associated_stem_comp='+\
             			'comp_objects_dict['+'"'+str(stem_comp_name)+'"]'+'\n')

                        
##     
                f.write('\n\t'+'comp_objects_dict['+'"'+str(comp_name)+'"'+']='+comp_name+'\n')    

### add leaf as associated compartment property of previously defined soil compartment

                if 'leaf' in comp_name and 'particle' not in comp_name  and 'sink' not in comp_name: # applies to leaf composites only
                    soil_comp_name='soil_surface_in_'+comp_name.split('_in_')[1] # infer associated surface soil compartment name
                    f.write('\n\t'+\
                                    str(soil_comp_name)+\
                                    '.'+\
                                    'associated_leaf_comp='+\
                        			'comp_objects_dict['+'"'+str(comp_name)+'"]'+'\n') 

                    f.write('\n\t'+'comp_objects_dict['+'"'+str(soil_comp_name)+'"'+']='+soil_comp_name+'\n')    
    
### add stem as associated compartment of previously defined soil compartment

                if 'stem' in comp_name and 'sink' not in comp_name:
                    soil_comp_name='soil_surface_in_'+comp_name.split('_in_')[1] # infer associated surface soil compartment name
                    f.write('\n\t'+\
                                    str(soil_comp_name)+\
                                    '.'+\
                                    'associated_stem_comp='+\
                        			'comp_objects_dict['+'"'+str(comp_name)+'"]'+'\n') 

                    f.write('\n\t'+'comp_objects_dict['+'"'+str(soil_comp_name)+'"'+']='+soil_comp_name+'\n')    
            
### add root as associated compartment of previously defined soil compartment

                if 'root' in comp_name and 'sink' not in comp_name:
                    soil_comp_name='soil_root_zone_in_rootsoil_'+comp_name.split('_in_')[1].split('_')[1] # pull out parcel name and attach to root soil
                    f.write('\n\t'+\
                                    str(soil_comp_name)+\
                                    '.'+\
                                    'associated_root_comp='+\
                        			'comp_objects_dict['+'"'+str(comp_name)+'"]'+'\n') 

                    f.write('\n\t'+'comp_objects_dict['+'"'+str(soil_comp_name)+'"'+']='+soil_comp_name+'\n')    
    
    
### add stem as associated compartment of previously defined leaf compartment

                if 'stem' in comp_name and 'sink' not in comp_name:
                    leaf_comp_name='leaf'+comp_name.split('stem')[1] # infer associated leaf compartment name
                    f.write('\n\t'+\
                                    str(leaf_comp_name)+\
                                    '.'+\
                                    'associated_stem_comp='+\
                        			'comp_objects_dict['+'"'+str(comp_name)+'"]'+'\n') 

                    f.write('\n\t'+'comp_objects_dict['+'"'+str(leaf_comp_name)+'"'+']='+leaf_comp_name+'\n')    


### add root as associated compartment of previously defined leaf compartment

                if 'root' in comp_name and 'sink' not in comp_name:
                    leaf_comp_name='leaf'+comp_name.split('root')[1] # infer associated leaf compartment name
                    f.write('\n\t'+\
                                    str(leaf_comp_name)+\
                                    '.'+\
                                    'associated_root_comp='+\
                        			'comp_objects_dict['+'"'+str(comp_name)+'"]'+'\n') 

                    f.write('\n\t'+'comp_objects_dict['+'"'+str(leaf_comp_name)+'"'+']='+leaf_comp_name+'\n')    



### add root as associated compartment of previously defined stem compartment

                if 'root' in comp_name and 'sink' not in comp_name:
                    stem_comp_name='stem'+comp_name.split('root')[1] # infer associated leaf compartment name
                    f.write('\n\t'+\
                                    str(stem_comp_name)+\
                                    '.'+\
                                    'associated_root_comp='+\
                        			'comp_objects_dict['+'"'+str(comp_name)+'"]'+'\n') 

                    f.write('\n\t'+'comp_objects_dict['+'"'+str(stem_comp_name)+'"'+']='+stem_comp_name+'\n')    

    
    ###### append code to auto define advection sinks
    
    # df_sinks=df_ve.loc[((df_ve.primary_abiotic=='air')|(df_ve.primary_abiotic=='soil - surface'))&(((df_ve.external_boundary>0) & (df_ve.parcel_name=='lakecadillac'))|((df_ve.external_boundary>0) & (df_ve.parcel_name=='lakemitchell'))|((df_ve.external_boundary>0) & (df_ve.parcel_name=='n1'))) ] # only air and surface soil compartments with an outer boundary need sinks
    df_sinks=df_ve.loc[((df_ve.primary_abiotic=='air')|(df_ve.primary_abiotic=='soil - surface'))&((df_ve.external_boundary>0) & (df_ve.parcel_name.isin(parcel_list))) ] # only air and surface soil compartments with an outer boundary need sinks

    
    with open(ofpn, 'a') as f:
        for i in df_sinks.index:
            primary_abiotic=str(df_sinks.loc[i,'primary_abiotic']).lower() # temp
            if primary_abiotic not in required_comp_classes: #  temp
               continue # temp    
            ve_name=str(df_sinks.loc[i,'ve_name'].replace(r'/','_').replace(r'-','_').replace(' ','_'))
            parcel_name=ve_name.split('_')[1] # parcel name
            parcel_points=df_parcels['point_ids'].loc[df_parcels['parcel_name']==parcel_name].values[0] # parcel points
            parcel_area=df_parcels['parcel_area'].loc[df_parcels['parcel_name']==parcel_name].values[0] # parcel area
            exterior_boundary=df_parcels['external_boundary'].loc[df_parcels['parcel_name']==parcel_name].values[0] # parcel exterior boundary
            comp_name='sink_in_sink_for_'+str(df_ve.loc[i,'primary_abiotic'].replace(r'/','_').replace(r'-','_').replace(' ','_')) + '_in_' + str(df_ve.loc[i,'ve_name'].replace(r'/','_').replace(r'-','_').replace(' ','_')) 
            comp_name=str(comp_name.replace('___','_').replace('__','_'))
            primary_abiotic=df_sinks.loc[i,'primary_abiotic']
            if primary_abiotic=='air':
                comp_class='advection_sink'
                comp_ct= 'sink | abiotic | air | air - default' # compartment category
            elif primary_abiotic=='soil - surface':
                # comp_class='soil_advection_sink'
                comp_class='advection_sink'
                comp_ct= 'sink | abiotic | soil | surface soil | soil advection sink' # compartment category

            comp_dict[counter]=comp_name
            counter+=1
            f.write('\n\t'+\
                str(comp_name)+\
                '=' +\
                comp_class+\
                '(constants,containingscenario,currentchemical,'+\
                str(ve_name)+\
                ',comp_objects_dict'+\
                ')')
            f.write('\n\t'+\
                        str(comp_name)+\
                        '.'+\
                        'name='+\
                        '"'+ comp_name+'"'+\
                        '\n\t'+\
                        str(comp_name)+\
                        '.'+\
                        'containingvolumeelementname='+\
                         '"'+ve_name+'"'+\
                        '\n\t'+\
                        str(comp_name)+\
                        '.'+\
                        'parcel_name='+\
                        '"'+parcel_name+'"'+\
                        '\n\t'+\
                        str(comp_name)+\
                        '.'+\
                        'parcel_points='+\
                        '"'+parcel_points+'"'+\
                        '\n\t'+\
                        str(comp_name)+\
                        '.'+\
                        'parcel_area='+\
                        str(parcel_area)+\
                        '\n\t'+\
                        str(comp_name)+\
                        '.'+\
                        'exterior_boundary='+\
                        str(exterior_boundary)+\
                        '\n\t'+\
                        str(comp_name)+\
                        '.'+\
                        'category='+\
                        '"'+str(comp_ct)+'"')
                        # '\n\t'+\
                        #  '@property'+\
                        # '\n\t'+\
                        # 'def category(self):'+\
                        #  '\n\t\t'+\
                        #  'return '+'"'+str(comp_ct)+'"')
            f.write('\n\t')
        
            f.write('\n\t'+'comp_objects_dict['+'"'+str(comp_name)+'"'+']='+comp_name+'\n')    
            f.write('\n\t')
    
    ################################# append python script to instantiate pseudo primary abiotic compartments -- must first have df_pve in memory (run vol_elem.py)
    
    with open(ofpn, 'a') as f:
        f.write('\n\t' + 'class pseudo_compartment:')
        f.write('\n\t\t' + 'pass' +'\n')


        for i in range(len(df_pve)):
            # if str(df_pve.loc[i,'parcel_name'])!="lakecadillac" and str(df_pve.loc[i,'parcel_name'])!="lakemitchell" and str(df_pve.loc[i,'parcel_name'])!="n1":  # temp
            if str(df_pve.loc[i,'parcel_name']) not in parcel_list:  # temp
                continue
        
            pve_name=str(df_pve.loc[i,'ve_name'].replace(r'/','_').replace(r'-','_').replace(' ','_'))
            parcel_name=pve_name.split('_')[1] # parcel name
            parcel_points=df_parcels['point_ids'].loc[df_parcels['parcel_name']==parcel_name].values[0] # parcel points
            parcel_area=df_parcels['parcel_area'].loc[df_parcels['parcel_name']==parcel_name].values[0] # parcel area
            exterior_boundary=df_parcels['external_boundary'].loc[df_parcels['parcel_name']==parcel_name].values[0] # parcel exterior boundary
            comp_name=str(df_pve.loc[i,'primary_abiotic'].replace(r'/','_').replace(r'-','_').replace(' ','_')) + '_in_' + str(df_pve.loc[i,'ve_name'].replace(r'/','_').replace(r'-','_').replace(' ','_')) 
            comp_name=str(comp_name.replace('___','_').replace('__','_'))
            comp_dict[counter]=comp_name
            counter+=1
            
            prim_abiotic_name=str(df_pve.loc[i,'primary_abiotic'].replace(r'/','_').replace(r'-','_').replace(' ','_'))
            if prim_abiotic_name=="dryvaporsource":
                comp_category="pseudosource | dry | vapor"
            if prim_abiotic_name=="wetvaporsource":
                comp_category="pseudosource | wet | vapor"
            if prim_abiotic_name=="dryparticlesource":
                comp_category="pseudosource | dry | particle"
            if prim_abiotic_name=="wetparticlesource":
                comp_category="pseudosource | wet | particle"

            f.write('\n\t'+\
                        str(comp_name)+'=pseudo_compartment()'+'\n\t'+\
                        str(comp_name)+\
                        '.'+\
                        'name='+\
                        '"'+ comp_name+'"'+\
                        '\n\t'+\
                        str(comp_name)+\
                        '.'+\
                        'containingvolumeelementname='+\
                         '"'+pve_name+'"'+\
                        '\n\t'+\
                        str(comp_name)+\
                        '.'+\
                        'parcel_name='+\
                        '"'+parcel_name+'"'+\
                        '\n\t'+\
                        str(comp_name)+\
                        '.'+\
                        'parcel_points='+\
                        '"'+parcel_points+'"'+\
                        '\n\t'+\
                        str(comp_name)+\
                        '.'+\
                        'parcel_area='+\
                        str(parcel_area)+\
                        '\n\t'+\
                        str(comp_name)+\
                        '.'+\
                        'exterior_boundary='+\
                        str(exterior_boundary)+\
                        '\n\t'+\
                        str(comp_name)+\
                        '.'+\
                        'deposition_rate={}'
                        )           
            f.write('\n\t'+str(comp_name)+'.category='+'"'+comp_category+'"')

            f.write('\n\t'+'comp_objects_dict['+'"'+str(comp_name)+'"'+']='+comp_name+'\n')
            
            ### add compartment properties
            f.write('\n\n')
            for i in range(len(df_props)):
                if str(df_props.loc[i,'prop_type'])!='compartment':
                    continue                
                if str(df_props.loc[i,'prop_owner']).split(' in ')[0].strip().lower() not in required_comp_classes: # temp -- this doesnt work for leaf composites because two " in " so added hack fix to required comps list
                   continue                
                
                obj=df_props.loc[i,'prop_owner_new']
                if True: # temporary. use condition below later.
        #        if obj in locals(): # may miss a few objects owing to name cleaning?
        #            print (obj)
                    f.write('\t'+'try:'+'\n\t\t')
                    f.write(str(obj)+\
                           "." +\
                           str(df_props.loc[i,'property_new'])+\
                           "="+\
                           str(df_props.loc[i,'value_new']))
                    f.write('\n'+'\t'+'except:'+'\n\t\t'+'pass') 
                    f.write('\n')            


    
    
        #### add deposition rates as properties of pseudo compartments
        f.write('\n'+'#add pseudo source dep rates to pseudo compartments'+'\n\n')

        for i in range(len(df_dr)):
            obj=df_dr.loc[i,'compartment']
            f.write('\t'+'try:'+'\n\t\t'+\
                    str(obj)+\
                   ".deposition_rate['" +\
                   str(df_dr.loc[i,'chemical'])+\
                  "']="+\
                   str(df_dr.loc[i,'surface deposition rate'])+\
                   '*'+\
                   obj+\
                   ".parcel_area"+'\n'\
                   '\t'+'except:'+'\n\t\t'+\
                   'pass')
            f.write('\n')            
    
                
                
        # write compartment objects dictionary        
#        f.write('\n\n\t'+'comp_objects_dict={}'+'\n\t')   
#        for k,v in comp_dict.items():
#            f.write('comp_objects_dict['+'"'+str(v)+'"'+']='+str(v)+'\n\t')
#            
        f.write('\n\t' +'return(comp_objects_dict)')

    f.close()
    
    return(df_comp,comp_dict)
    
if __name__ == '__main__':
    df_comp,comp_dict=define_compartments(inputs,df_parcels,df_ve,df_pve,df_props,df_dr)