# -*- coding: utf-8 -*-
"""
Created on Wed Mar 31 21:15:14 2021
@author: 13963

1) Parses volumen elements text file and pseudo volume elements text file
2) Stores point, parcel, volume elements, and pseudo volume elements data in dataframes
3) Auto writes scripts to instantiate volume element and pseudo volume element objects, specifically define_ve.py and define_pve.py

"""
import pandas as pd
import os
from shapely.geometry import Polygon, LineString
from shapely.ops import cascaded_union

def define_volume_elements(inputs):

    ifp=inputs['path_inputs']
    ifn=inputs['ve_file']    
    ifpn=os.path.join(ifp,ifn)
    
    def look_up_coords(point_name): # function to look up coordinates of a point from pre-defined df_points dataframe. support function for polygon_area function
        x=float(df_points['x'].loc[df_points['Point_ID']==point_name].values[0])
        y=float(df_points['y'].loc[df_points['Point_ID']==point_name].values[0])
        return (x,y)
    
    def polygon_area(point_string):  # function to compute polygon area based on eastings and northings in shapely
        points=point_string.split(' ')
        point_coords=[look_up_coords(p) for p in points]
        polygon = Polygon(point_coords)
        return(polygon.area)
        
    def find_outliers(df_parcels): # function to find outlying parcels and length of boundary
        pids=list(df_parcels['Point_IDs'])
        polygons=[] # list of Polygon objects
        ext_intersection=[] # list of external intersection for each parcel
        for pid in pids: # loop over parcels 
            points=pid.split(' ') # get parcel points
            poly_coords=[] # list of x,y tuples
            for point in points: # loop over points in parcel
                x_y_coords=look_up_coords(point) # get x,y
                poly_coords.append(x_y_coords) # add to parcel list            
            polygons.append(Polygon(poly_coords))# make a polygon and append it
        cascade = cascaded_union(polygons) # union of polygons
        x,y=cascade.exterior.coords.xy
        ext_coords=[p for p in zip (x,y)] # list of x,y coords of the exterior boundary of the layout  
        ext_lines=[] # list of exterior line objects
        for index, x in enumerate(ext_coords): # loop over exterior coords to create and populate exterior line objects list
            if index<len(ext_coords)-1:
                ext_lines.append(LineString([ext_coords[index],ext_coords[index+1]]))  # join successive points of outer polygon
            else:
                ext_lines.append(LineString([ext_coords[index],ext_coords[0]])) # join last and first
        for pid in pids: # loop over parcels 
            points=pid.split(' ') # get parcel points
            poly_coords=[] # list of x,y tuples
            for point in points: # loop over points in parcel
                x_y_coords=look_up_coords(point) # get x,y    
                poly_coords.append(x_y_coords) # add to parcel list 
            poly_lines=[] # list of LInes in Polygon
            for index, x in enumerate(poly_coords):  # loop over exterior coords to create and populate polygon line objects list
                if index<len(poly_coords)-1: 
                    poly_lines.append(LineString([poly_coords[index],poly_coords[index+1]]))# join successive points of outer polygon
                else:
                    poly_lines.append(LineString([poly_coords[index],poly_coords[0]])) # join last and first
            ext_len=0 # external length of polygon (parcel)
            for poly_line in poly_lines: # loop over polygon lines
                for ex_line in ext_lines:
                    if poly_line.intersects(ex_line):
                        ext_len=ext_len+poly_line.intersection(ex_line).length
    #            if cascade.intersects(line):
    #                ext_len=ext_len+cascade.intersection(line).length
    
    #            if cascade.intersects(line):
    #                ext_len=ext_len+cascade.intersection(line).length
            ext_intersection.append(ext_len)
        df_parcels['External_Boundary']=ext_intersection
        return (df_parcels)
    
    #polygon2 = Polygon(point_coords)
    #cascade = cascaded_union([polygon1,polygon2])
    #x,y=cascade.exterior.coords.xy
    #line=LineString([(629142.149632, 4901500.48091),(627252.066631, 4900953.9122)])
    #cascade.intersects(line)
    
    
    
    ve_file=open(ifpn,'r') 
    ve_lines=ve_file.readlines()
    
    #### Read Points
    
    point_lines=[] # initialize list for storing point lines
    copy=False # initialize copy condition
    for line in ve_lines: # loop over lines 
        if line.strip()=="start_points": # if start_points copy condition is true
            copy=True 
        elif line.strip()=="end_points": # if end_points copy condition is false
            copy=False
        elif copy==True: # if copy condition is true
            if line.strip()[:2]!=r'//' and line.strip()!='': # if not a comment
                line_nc=line.split("//")[0] # line stripped of comment
                point_lines.append(line_nc.strip().split(' ')) # append line after splitting it
    df_points=pd.DataFrame(point_lines,columns=['Point_ID','x','y']) # convert to dataframe
    
    
    #### Read Parcels
    parcel_lines=[] # initialize list for storing parcel lines
    copy=False # initialize copy condition
    for line in ve_lines: # loop over lines 
        if line.strip()=="start_parcels": # if start_points copy condition is true
            copy=True 
        elif line.strip()=="end_parcels": # if end_points copy condition is false
            copy=False
        elif copy==True: # if copy condition is true
            if line.strip()[:2]!=r'//' and line.strip()!='': # if not a comment
                line_nc=line.split("//")[0] # line stripped of comment
                parcel_lines.append(line_nc.strip().split(' ')) # append line after splitting it
    
    parcel_tuples=[] # initialize list of parcel tuples 
    for lin in parcel_lines: # loop over parcel lines 
        t=(lin[0],lin[1],' '.join(lin[2:])) # package as tuples with fixed dimension = parcel_name, #points, pointIDs
        parcel_tuples.append(t)
    df_parcels=pd.DataFrame(parcel_tuples,columns=['Parcel_Name','#Points','Point_IDs']) # convert to dataframe
    
    df_parcels['Parcel_Area']=df_parcels['Point_IDs'].apply(polygon_area)   # compute polygon area                                            
    
    df_parcels=find_outliers(df_parcels)
                                                  
    #### Read Volume Elements
    vol_ele_lines=[] # initialize list for storing parcel lines
    copy=False # initialize copy condition
    for line in ve_lines: # loop over lines 
        if line.strip()=="start_volume_elements": # if start_points copy condition is true
            copy=True 
        elif line.strip()=="end_volume_elements": # if end_points copy condition is false
            copy=False
        elif copy==True: # if copy condition is true
            if line.strip()[:2]!=r'//' and line.strip()!='': # if not a comment and not a blank
                line_nc=line.split("//")[0] # line stripped of comment
                vol_ele_lines.append(line_nc.strip()) # append line 
        ### Ugly, dirty solution to problem of having " Primary Abiotic Names" in quotes potentially with spacecs
    ve_list=[] # initialize list of cleaned up volume element items
    for lin in vol_ele_lines: # loop over vol_ele lines
        temp_list=lin.split(r'"') # split on " -- creates list of size 3 -- middle element is the primary abiotic name
        clean_list=temp_list[0].strip().split(' ')+[temp_list[1].strip()]+temp_list[2].strip().split(' ')
        ve_list.append(clean_list)
    
    df_ve=pd.DataFrame(ve_list,columns=['VE_Name', 'Parcel_Name', 'Primary_Abiotic', 'Bottom', 'Top']) # convert to dataframe
    
    
    
    #######Read pseudo VE
    
    
    ifn=inputs['pseudo_ve_file']
    ifpn=os.path.join(ifp,ifn)
    
    ve_file=open(ifpn,'r') 
    ve_lines=ve_file.readlines()
    
    
    
    vol_ele_lines=[] # initialize list for storing parcel lines
    copy=False # initialize copy condition
    for line in ve_lines: # loop over lines 
        if line.strip()=="start_volume_elements": # if start_points copy condition is true
            copy=True 
        elif line.strip()=="end_volume_elements": # if end_points copy condition is false
            copy=False
        elif copy==True: # if copy condition is true
            if line.strip()[:2]!=r'//' and line.strip()!='': # if not a comment and not a blank
                line_nc=line.split("//")[0] # line stripped of comment
                vol_ele_lines.append(line_nc.strip()) # append line 
        ### Ugly, dirty solution to problem of having " Primary Abiotic Names" in quotes potentially with spacecs
    ve_list=[] # initialize list of cleaned up volume element items
    for lin in vol_ele_lines: # loop over vol_ele lines
        temp_list=lin.split(r'"') # split on " -- creates list of size 3 -- middle element is the primary abiotic name
        clean_list=temp_list[0].strip().split(' ')+[temp_list[1].strip()]+temp_list[2].strip().split(' ')
        ve_list.append(clean_list)
    
    df_pve=pd.DataFrame(ve_list,columns=['VE_Name', 'Parcel_Name', 'Primary_Abiotic', 'Bottom', 'Top']) # convert to dataframe
    
    df_ve=df_ve.merge(df_parcels,how='left',on='Parcel_Name') # merge in parcel points
    df_pve=df_pve.merge(df_parcels,how='left',on='Parcel_Name') # merge in parcel points
    
    
    ################################# WRITE PYTHON SCRIPT TO INSTANTIATE VOLUME ELEMENTS 

#if __name__=='main':
#\tclass Volume_Element:
#\t\tdef __init__(self,VE_Name,Parcel_Name,Primary_Abiotic,Bottom,Top,Point_IDs,Height,Area,Volume):
#\t\t\tself.VE_Name=VE_Name
#\t\t\tself.Parcel_Name=Parcel_Name
#\t\t\tself.Primary_Abiotic=Primary_Abiotic
#\t\t\tself.Bottom=Bottom
#\t\t\tself.Top=Top
#\t\t\tself.Point_IDs=Point_IDs
#\t\t\tself.Height=Height
#\t\t\tself.Area=Area
#\t\t\tself.Volume=Volume

    
    ofp=inputs['path_code']
    ofn=r'define_ve.py'
    ofpn=os.path.join(ofp,ofn)
    
    with open(ofpn, 'w') as f:
        f.write('### Note: This is an auto generated script' +'\n')        
        f.write('''\
class Volume_Element:
    def __init__(self,VE_Name,Parcel_Name,Primary_Abiotic,Bottom,Top,Point_IDs,Height,Area,Volume):
        self.VE_Name=VE_Name
        self.Parcel_Name=Parcel_Name
        self.Primary_Abiotic=Primary_Abiotic
        self.Bottom=float(Bottom)
        self.Top=float(Top)
        self.Point_IDs=Point_IDs
        self.Height=float(Height)
        self.Area=float(Area)
        self.Volume=float(Volume)
''')
        for i in range(len(df_ve)):
            ve_name=df_ve.loc[i,'VE_Name'] # volume element name
            parcel_name=ve_name.split('_')[1] # parcel name
            parcel_points=df_parcels['Point_IDs'].loc[df_parcels['Parcel_Name']==parcel_name].values[0] # parcel points
            parcel_area=round(df_parcels['Parcel_Area'].loc[df_parcels['Parcel_Name']==parcel_name].values[0],2) # parcel area
            ve_height=round(abs(float(df_ve.loc[i,'Top'])-float(df_ve.loc[i,'Bottom'])),2)
            ve_volume=round(parcel_area*ve_height,2)
            f.write(str(df_ve.loc[i,'VE_Name'])+\
                    "=Volume_Element('"+\
                    str(df_ve.loc[i,'VE_Name'])+\
                    "','"+\
                    str(df_ve.loc[i,'Parcel_Name'])+\
                    "','"+\
                    str(df_ve.loc[i,'Primary_Abiotic'])+\
                    "','"+\
                    str(df_ve.loc[i,'Bottom'])+\
                    "','"+\
                    str(df_ve.loc[i,'Top'])+\
                    "','"+\
                    str(df_ve.loc[i,'Point_IDs'])+\
                    "','"+\
                    str(ve_height)+\
                    "','"+\
                    str(parcel_area)+\
                    "','"+\
                    str(ve_volume)+\
                    "')")
            f.write('\n')
            
                
                
    f.close()
    
    
    
    ################################# WRITE PYTHON SCRIPT TO INSTANTIATE PSEUDO-VOLUME ELEMENTS 
    
    ofn=r'define_pve.py'
    ofpn=os.path.join(ofp,ofn)
    
    with open(ofpn, 'w') as f:
        f.write('### Note: This is an auto generated script' +'\n')                
        f.write('''                
class Volume_Element:
    def __init__(self,VE_Name,Parcel_Name,Primary_Abiotic,Bottom,Top,Point_IDs,Height,Area,Volume):
        self.VE_Name=VE_Name
        self.Parcel_Name=Parcel_Name
        self.Primary_Abiotic=Primary_Abiotic
        self.Bottom=Bottom
        self.Top=Top
        self.Point_IDs=Point_IDs
        self.Height=Height
        self.Area=Area
        self.Volume=Volume
''')
        for i in range(len(df_pve)):
            ve_name=df_pve.loc[i,'VE_Name'] # volume element name
            parcel_name=ve_name.split('_')[1] # parcel name
            parcel_points=df_parcels['Point_IDs'].loc[df_parcels['Parcel_Name']==parcel_name].values[0] # parcel points
            parcel_area=round(df_parcels['Parcel_Area'].loc[df_parcels['Parcel_Name']==parcel_name].values[0],2) # parcel area
            ve_height=round(abs(float(df_ve.loc[i,'Top'])-float(df_ve.loc[i,'Bottom'])),2)
            ve_volume=round(parcel_area*ve_height,2)
            f.write(str(df_pve.loc[i,'VE_Name'])+\
                    "=Volume_Element('"+\
                    str(df_pve.loc[i,'VE_Name'])+\
                    "','"+\
                    str(df_pve.loc[i,'Parcel_Name'])+\
                    "','"+\
                    str(df_pve.loc[i,'Primary_Abiotic'])+\
                    "','"+\
                    str(df_pve.loc[i,'Bottom'])+\
                    "','"+\
                    str(df_pve.loc[i,'Top'])+\
                    "','"+\
                    str(df_pve.loc[i,'Point_IDs'])+\
                    "','"+\
                    str(ve_height)+\
                    "','"+\
                    str(parcel_area)+\
                    "','"+\
                    str(ve_volume)+\
                    "')")
            f.write('\n')
            
                
                
    f.close()
    
    return(df_points,df_parcels,df_ve,df_pve)
    
    
if __name__ == '__main__':
    df_points,df_parcels,df_ve,df_pve=define_volume_elements(inputs)