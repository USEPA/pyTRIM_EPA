# -*- coding: utf-8 -*-
"""
created on wed mar 31 21:15:14 2021
@author: 13963

1) parses volumen elements text file and pseudo volume elements text file
2) stores point, parcel, volume elements, and pseudo volume elements data in DataFrames
3) auto writes scripts to instantiate volume element and pseudo volume element objects, specifically define_ve.py and define_pve.py

"""
import pandas as pd
import os
from shapely.geometry import Polygon, LineString
from shapely.ops import cascaded_union

def define_volume_elements(inputs):

    ifp=inputs['path_inputs']
    ifn=inputs['ve_file']    
    ifpn=os.path.join(ifp,ifn)
    
    def look_up_coords(point_name): # function to look up coordinates of a point from pre-defined df_points DataFrame. support function for Polygon_area function
        x=float(df_points['x'].loc[df_points['point_id']==point_name].values[0])
        y=float(df_points['y'].loc[df_points['point_id']==point_name].values[0])
        return (x,y)
    
    def Polygon_area(point_string):  # function to compute Polygon area based on eastings and northings in shapely
        points=point_string.split(' ')
        point_coords=[look_up_coords(p) for p in points]
        poly = Polygon(point_coords)
        return(poly.area)
        
    def find_outliers(df_parcels): # function to find outlying parcels and length of boundary
        pids=list(df_parcels['point_ids'])
        polys=[] # list of Polygon objects
        ext_intersection=[] # list of external intersection for each parcel
        for pid in pids: # loop over parcels 
            points=pid.split(' ') # get parcel points
            poly_coords=[] # list of x,y tuples
            for point in points: # loop over points in parcel
                x_y_coords=look_up_coords(point) # get x,y
                poly_coords.append(x_y_coords) # add to parcel list            
            polys.append(Polygon(poly_coords))# make a Polygon and append it
        cascade = cascaded_union(polys) # union of Polygons
        x,y=cascade.exterior.coords.xy
        ext_coords=[p for p in zip (x,y)] # list of x,y coords of the exterior boundary of the layout  
        ext_lines=[] # list of exterior line objects
        for index, x in enumerate(ext_coords): # loop over exterior coords to create and populate exterior line objects list
            if index<len(ext_coords)-1:
                ext_lines.append(LineString([ext_coords[index],ext_coords[index+1]]))  # join successive points of outer Polygon
            else:
                ext_lines.append(LineString([ext_coords[index],ext_coords[0]])) # join last and first
        for pid in pids: # loop over parcels 
            points=pid.split(' ') # get parcel points
            poly_coords=[] # list of x,y tuples
            for point in points: # loop over points in parcel
                x_y_coords=look_up_coords(point) # get x,y    
                poly_coords.append(x_y_coords) # add to parcel list 
            poly_lines=[] # list of lines in Polygon
            for index, x in enumerate(poly_coords):  # loop over exterior coords to create and populate Polygon line objects list
                if index<len(poly_coords)-1: 
                    poly_lines.append(LineString([poly_coords[index],poly_coords[index+1]]))# join successive points of outer Polygon
                else:
                    poly_lines.append(LineString([poly_coords[index],poly_coords[0]])) # join last and first
            ext_len=0 # external length of Polygon (parcel)
            for poly_line in poly_lines: # loop over Polygon lines
                for ex_line in ext_lines:
                    if poly_line.intersects(ex_line):
                        ext_len=ext_len+poly_line.intersection(ex_line).length
    #            if cascade.intersects(line):
    #                ext_len=ext_len+cascade.intersection(line).length
    
    #            if cascade.intersects(line):
    #                ext_len=ext_len+cascade.intersection(line).length
            ext_intersection.append(ext_len)
        df_parcels['external_boundary']=ext_intersection
        return (df_parcels)
    
    #Polygon2 = Polygon(point_coords)
    #cascade = cascaded_union([Polygon1,Polygon2])
    #x,y=cascade.exterior.coords.xy
    #line=LineString([(629142.149632, 4901500.48091),(627252.066631, 4900953.9122)])
    #cascade.intersects(line)
    
    
    
    ve_file=open(ifpn,'r') 
    ve_lines=ve_file.readlines()
    
    #### read points
    
    point_lines=[] # initialize list for storing point lines
    copy=False # initialize copy condition
    for line in ve_lines: # loop over lines 
        if line.strip()=="start_points": # if start_points copy condition is True
            copy=True 
        elif line.strip()=="end_points": # if end_points copy condition is False
            copy=False
        elif copy==True: # if copy condition is True
            if line.strip()[:2]!=r'//' and line.strip()!='': # if not a comment
                line_nc=line.split("//")[0] # line stripped of comment
                point_lines.append(line_nc.strip().split(' ')) # append line after splitting it
    df_points=pd.DataFrame(point_lines,columns=['point_id','x','y']) # convert to DataFrame
    
    
    #### read parcels
    parcel_lines=[] # initialize list for storing parcel lines
    copy=False # initialize copy condition
    for line in ve_lines: # loop over lines 
        if line.strip()=="start_parcels": # if start_points copy condition is True
            copy=True 
        elif line.strip()=="end_parcels": # if end_points copy condition is False
            copy=False
        elif copy==True: # if copy condition is True
            if line.strip()[:2]!=r'//' and line.strip()!='': # if not a comment
                line_nc=line.split("//")[0] # line stripped of comment
                parcel_lines.append(line_nc.strip().split(' ')) # append line after splitting it
    
    parcel_tuples=[] # initialize list of parcel tuples 
    for lin in parcel_lines: # loop over parcel lines 
        t=(lin[0],lin[1],' '.join(lin[2:])) # package as tuples with fixed dimension = parcel_name, #points, pointids
        parcel_tuples.append(t)
    df_parcels=pd.DataFrame(parcel_tuples,columns=['parcel_name','#points','point_ids']) # convert to DataFrame
    
    df_parcels['parcel_area']=df_parcels['point_ids'].apply(Polygon_area)   # compute Polygon area                                            
    
    df_parcels=find_outliers(df_parcels)
                                                  
    #### read volume elements
    vol_ele_lines=[] # initialize list for storing parcel lines
    copy=False # initialize copy condition
    for line in ve_lines: # loop over lines 
        if line.strip()=="start_volume_elements": # if start_points copy condition is True
            copy=True 
        elif line.strip()=="end_volume_elements": # if end_points copy condition is False
            copy=False
        elif copy==True: # if copy condition is True
            if line.strip()[:2]!=r'//' and line.strip()!='': # if not a comment and not a blank
                line_nc=line.split("//")[0] # line stripped of comment
                vol_ele_lines.append(line_nc.strip()) # append line 
        ### ugly, dirty solution to problem of having " primary abiotic names" in quotes potentially with spacecs
    ve_list=[] # initialize list of cleaned up volume element items
    for lin in vol_ele_lines: # loop over vol_ele lines
        temp_list=lin.split(r'"') # split on " -- creates list of size 3 -- middle element is the primary abiotic name
        clean_list=temp_list[0].strip().split(' ')+[temp_list[1].strip()]+temp_list[2].strip().split(' ')
        ve_list.append(clean_list)
    
    df_ve=pd.DataFrame(ve_list,columns=['ve_name', 'parcel_name', 'primary_abiotic', 'bottom', 'top']) # convert to DataFrame
    
    
    
    #######read pseudo ve
    
    
    ifn=inputs['pseudo_ve_file']
    ifpn=os.path.join(ifp,ifn)
    
    ve_file=open(ifpn,'r') 
    ve_lines=ve_file.readlines()
    
    
    
    vol_ele_lines=[] # initialize list for storing parcel lines
    copy=False # initialize copy condition
    for line in ve_lines: # loop over lines 
        if line.strip()=="start_volume_elements": # if start_points copy condition is True
            copy=True 
        elif line.strip()=="end_volume_elements": # if end_points copy condition is False
            copy=False
        elif copy==True: # if copy condition is True
            if line.strip()[:2]!=r'//' and line.strip()!='': # if not a comment and not a blank
                line_nc=line.split("//")[0] # line stripped of comment
                vol_ele_lines.append(line_nc.strip()) # append line 
        ### ugly, dirty solution to problem of having " primary abiotic names" in quotes potentially with spacecs
    ve_list=[] # initialize list of cleaned up volume element items
    for lin in vol_ele_lines: # loop over vol_ele lines
        temp_list=lin.split(r'"') # split on " -- creates list of size 3 -- middle element is the primary abiotic name
        clean_list=temp_list[0].strip().split(' ')+[temp_list[1].strip()]+temp_list[2].strip().split(' ')
        ve_list.append(clean_list)
    
    df_pve=pd.DataFrame(ve_list,columns=['ve_name', 'parcel_name', 'primary_abiotic', 'bottom', 'top']) # convert to DataFrame
    
    df_ve=df_ve.merge(df_parcels,how='left',on='parcel_name') # merge in parcel points
    df_pve=df_pve.merge(df_parcels,how='left',on='parcel_name') # merge in parcel points
    
    
    ################################# write python script to instantiate volume elements 

#if __name__=='main':
#\tclass volume_element:
#\t\tdef __init__(self,ve_name,parcel_name,primary_abiotic,bottom,top,point_ids,height,area,volume):
#\t\t\tself.ve_name=ve_name
#\t\t\tself.parcel_name=parcel_name
#\t\t\tself.primary_abiotic=primary_abiotic
#\t\t\tself.bottom=bottom
#\t\t\tself.top=top
#\t\t\tself.point_ids=point_ids
#\t\t\tself.height=height
#\t\t\tself.area=area
#\t\t\tself.volume=volume

    
    ofp=inputs['path_code']
    ofn=r'define_ve.py'
    ofpn=os.path.join(ofp,ofn)
    
    with open(ofpn, 'w') as f:
        f.write('### note: this is an auto generated script' +'\n')        
        f.write('''\
class volume_element:
    def __init__(self,ve_name,parcel_name,primary_abiotic,bottom,top,point_ids,height,area,volume):
        self.ve_name=ve_name
        self.parcel_name=parcel_name
        self.primary_abiotic=primary_abiotic
        self.bottom=float(bottom)
        self.top=float(top)
        self.point_ids=point_ids
        self.height=float(height)
        self.area=float(area)
        self.volume=float(volume)
''')
        for i in range(len(df_ve)):
            ve_name=df_ve.loc[i,'ve_name'] # volume element name
            parcel_name=ve_name.split('_')[1] # parcel name
            parcel_points=df_parcels['point_ids'].loc[df_parcels['parcel_name']==parcel_name].values[0] # parcel points
            parcel_area=round(df_parcels['parcel_area'].loc[df_parcels['parcel_name']==parcel_name].values[0],2) # parcel area
            ve_height=round(abs(float(df_ve.loc[i,'top'])-float(df_ve.loc[i,'bottom'])),2)
            ve_volume=round(parcel_area*ve_height,2)
            f.write(str(df_ve.loc[i,'ve_name'])+\
                    "=volume_element('"+\
                    str(df_ve.loc[i,'ve_name'])+\
                    "','"+\
                    str(df_ve.loc[i,'parcel_name'])+\
                    "','"+\
                    str(df_ve.loc[i,'primary_abiotic'])+\
                    "','"+\
                    str(df_ve.loc[i,'bottom'])+\
                    "','"+\
                    str(df_ve.loc[i,'top'])+\
                    "','"+\
                    str(df_ve.loc[i,'point_ids'])+\
                    "','"+\
                    str(ve_height)+\
                    "','"+\
                    str(parcel_area)+\
                    "','"+\
                    str(ve_volume)+\
                    "')")
            f.write('\n')
            
                
                
    f.close()
    
    
    
    ################################# write python script to instantiate pseudo-volume elements 
    
    ofn=r'define_pve.py'
    ofpn=os.path.join(ofp,ofn)
    
    with open(ofpn, 'w') as f:
        f.write('### note: this is an auto generated script' +'\n')                
        f.write('''                
class volume_element:
    def __init__(self,ve_name,parcel_name,primary_abiotic,bottom,top,point_ids,height,area,volume):
        self.ve_name=ve_name
        self.parcel_name=parcel_name
        self.primary_abiotic=primary_abiotic
        self.bottom=bottom
        self.top=top
        self.point_ids=point_ids
        self.height=height
        self.area=area
        self.volume=volume
''')
        for i in range(len(df_pve)):
            ve_name=df_pve.loc[i,'ve_name'] # volume element name
            parcel_name=ve_name.split('_')[1] # parcel name
            parcel_points=df_parcels['point_ids'].loc[df_parcels['parcel_name']==parcel_name].values[0] # parcel points
            parcel_area=round(df_parcels['parcel_area'].loc[df_parcels['parcel_name']==parcel_name].values[0],2) # parcel area
            ve_height=round(abs(float(df_ve.loc[i,'top'])-float(df_ve.loc[i,'bottom'])),2)
            ve_volume=round(parcel_area*ve_height,2)
            f.write(str(df_pve.loc[i,'ve_name'])+\
                    "=volume_element('"+\
                    str(df_pve.loc[i,'ve_name'])+\
                    "','"+\
                    str(df_pve.loc[i,'parcel_name'])+\
                    "','"+\
                    str(df_pve.loc[i,'primary_abiotic'])+\
                    "','"+\
                    str(df_pve.loc[i,'bottom'])+\
                    "','"+\
                    str(df_pve.loc[i,'top'])+\
                    "','"+\
                    str(df_pve.loc[i,'point_ids'])+\
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