# -*- coding: utf-8 -*-
"""
created on thu jul  8 15:39:50 2021
@author: 13963

reads and parse deposition rates file 
auto writes code to add deposition attributes to pseudo source compartments, specifically define_attributes_dep_rates.py

"""

import pandas as pd
import os
import re
from util_functions import * 
from shapely.geometry import Polygon,LineString,Point


def look_up_coords(point_name,df_points): # function to look up coordinates of a point from pre-defined df_points DataFrame. support function for Polygon_area function
    x=float(df_points['x'].loc[df_points['point_id']==point_name].values[0])
    y=float(df_points['y'].loc[df_points['point_id']==point_name].values[0])
    return (x,y)

def source_location(source_x,source_y,source_z,df_points,df_parcels,df_comp): # function to determine compartment name of source based on x,y,z coordinates of source
    source_point=Point(source_x,source_y) # create source point in shapely 
    parcel_name="" # initialize blank
    for i in range(0,len(df_parcels)):# loop over parcels
        pids_parcel=df_parcels['point_ids'].loc[i] # parcel points 
        pids_parcel=pids_parcel.split(' ')       # split into list
        coords_comp=[look_up_coords(p,df_points) for p in pids_parcel] # list of coordinates        
        Polygon_comp = Polygon(coords_comp)    # form parcel polygon
        if Polygon_comp.contains(source_point): # check if  point within the parcel
            parcel_name=df_parcels['parcel_name'].loc[i] # grab parcel name
        else:
            continue
    if parcel_name=="": # error if blank return nil
        print ("ERROR LOCATING SOURCE PARCEL")
        return ()
    dfc=df_comp[df_comp['parcel_name']==parcel_name].reset_index() # filter df_comp on specific parcel of source
    comp_name=""# initialize blank
    for i in range(0,len(dfc)):# loop over compartments corresponding to parcel
        bottom=float(dfc['bottom'].loc[i])  
        top=float(dfc['top'].loc[i])  
        if source_z>bottom and source_z<=top: # if within top and bottom of compartment
            ve_name=dfc['ve_name'].loc[i] # grab volume element name
            dfve=dfc[dfc['ve_name']==ve_name].reset_index().loc[0] # filter compartments on that volume element (can be more than one and keep just first (e.g. multiple sinks))
            comp_name=dfve['primary_abiotic'].replace(r'/','_').replace(r'-','_').replace(' ','_') + '_in_'+dfve['ve_name'] # build compartment name base3d on primary abiotic (sources are limited to primary abiotic) -- df_comp does not contain primary abiotic names
            comp_name=str(comp_name.replace('___','_').replace('__','_')) # clean up name
    if comp_name=="": # error if blank
        print ("ERROR LOCATING SOURCE COMPARTMENT") 
        return ()
    
    return(comp_name) # return comp_name of primary abiotic compartment in the volume element containing the source coordinates


def define_deposition_rates(inputs,df_points, df_parcels,df_comp):
    
    
    ifp=inputs['path_inputs']
    ifn=inputs['dep_rates_file']
    ifpn=os.path.join(ifp,ifn)
    
    dr_file=open(ifpn,'r') 
    dr_lines=dr_file.readlines()
    
    dr_tuples=[] # initialize list for storing point lines
    
    
    def clean_names(name): # function to replace certain special characters with underscore; leaves float values alone
        try:
            name=float(name) 
        except:
            pass
        if type(name)==str:
            cname = re.sub('[^0-9a-za-z]+', '_', name)
            return(cname)
        return(name)  
    
    
    def clean_props(prop): # function to convert properties to pythonic syntax, 
        if '?' in prop: # change java if then else syntax to pythonic syntax
            cond=prop.split('?')[0].strip()
            v1=prop.split('?')[1].strip().split(':')[0].strip()
            v2=prop.split('?')[1].strip().split(':')[1].strip()
            prop= v1+' if ' +cond.replace('&&',' and ')+' else ' +v2
        prop=prop.replace('constants','self.constants')
        prop=prop.replace('containingscenario','self.containingscenario')
        prop=prop.replace('chemical','self')
        prop=prop.replace('ln','log')
        prop=prop.replace('<unset>','"<unset>"')
        return (prop)
    

    for line in dr_lines: # loop over lines 
        line=line.strip()        
        line_nc=line.split("//")[0] # line stripped of comment
        if line_nc[:12]=="pointsource:":           
            source_name=line_nc.split(":")[1].strip()
            PropXFlag=False
            PropYFlag=False
            PropZFlag=False
            PropERFlag=False
        prop=""
        if line_nc[:9]=="property:":   
            prop=line_nc.split(":")[1].strip()
        if prop=='x':
            PropXFlag=True
        if prop=='y':
            PropYFlag=True
        if prop=='elevation':
            PropZFlag=True            
        if prop=='emissionrate':
            PropERFlag=True  

        if line_nc[:6]=="value:":   
            val=line_nc.split(":")[1].strip()
            if PropXFlag==True:
                X=val
                PropXFlag=False
            if PropYFlag==True:
                Y=val
                PropYFlag=False
            if PropZFlag==True:
                Z=val
                PropZFlag=False
            if PropERFlag and '{' in val: 
                chem=val.split("}")[0].strip().replace('{','')
                chem=clean_names(chem)
                dep=val.split("}")[1].strip()
                dep=float(dep)
                c=(source_name,X,Y,Z,chem,dep)
                print (c)
                dr_tuples.append(c)        
    df_dr=pd.DataFrame(dr_tuples,columns=['source_name','x', 'y', 'z','chemical','emission_rate'])
    df_dr['chemical']=df_dr['chemical'].apply(clean_chem_names)    
    df_dr=df_dr[df_dr['emission_rate'] > 0] # keep only dep rates greater than zero (drop zeros)
    df_dr['source_compartment']="" # to be filled in below 
    df_dr['x'] = df_dr['x'].astype(float)
    df_dr['y'] = df_dr['y'].astype(float)
    df_dr['z'] = df_dr['z'].astype(float)
    df_dr=df_dr.reset_index()
    
    df_ps=df_dr.groupby(['source_name','x','y','z']).size().reset_index().rename(columns={0:'count'}) # dataframe of point sources
    
    for i in range(0,len(df_ps)): # loop over dataframe of point source (x,y,z,and source name only):
        source_x=float(df_ps['x'].loc[i])
        source_y=float(df_ps['y'].loc[i])
        source_z=float(df_ps['z'].loc[i])
        source_name=df_ps['source_name'].loc[i]
        source_comp=source_location(source_x,source_y,source_z,df_points,df_parcels,df_comp)

        if source_comp!="":
            df_dr.loc[(df_dr.x==source_x)&(df_dr.y==source_y)&(df_dr.z==source_z),"source_compartment"]=source_comp ## add source comp name to df_dr
    #### write script to add deposition rates as properties of pseudo compartments
    
    ofp=inputs['path_code']
    ofn=r'define_attributes_dep_rates.py'
    ofpn=os.path.join(ofp,ofn)
    
    with open(ofpn, 'w') as f:
        f.write('### note: this is an auto generated script' +'\n')        
        for i in range(len(df_dr)):
            obj=df_dr.loc[i,'source_compartment']
            f.write('try:'+'\n\t'+\
                    'comp_objects_dict["'+str(obj)+'"]'+\
                   ".deposition_rate['" +\
                   str(df_dr.loc[i,'chemical'])+\
                  "']="+\
                   str(df_dr.loc[i,'emission_rate'])+'\n'\
                   'except:'+'\n\t'+\
                   'pass\n')
            f.write('\n')  

    f.close()

           
    ofp=inputs['path_code']
    ofn=r'define_comp.py'
    ofpn=os.path.join(ofp,ofn)
    with open(ofpn, 'a') as f:
    ### add deposition rates as properties of pseudo compartments
        f.write('\n'+'#add dep rates to compartments'+'\n\n')
    
        source_obj=""
        for i in range(len(df_dr)):
            obj=df_dr.loc[i,'source_compartment']
            if obj!=source_obj: # everytime there is a new source object, write line to initialize dictionary
                source_obj=obj
                f.write('\t'+str(obj)+'.deposition_rate={}'+'\n')
            f.write('\t'+'try:'+'\n\t\t'+\
                str(obj)+\
                ".deposition_rate['" +\
                str(df_dr.loc[i,'chemical'])+\
              "']="+\
                str(df_dr.loc[i,'emission_rate'])+'\n\t'+\
                    'except:'+'\n\t\t'+\
                'pass')
            f.write('\n')            
    
                
                
        f.write('\n\t' +'return(comp_objects_dict)')  ## COMMENTING OUT RETURN FOR TS VERSION. MORE WILL EB APPENDED BY DEP RATES FILE.
    
    f.close()
                
    return(df_dr)