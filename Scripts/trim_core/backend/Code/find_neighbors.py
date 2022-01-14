# -*- coding: utf-8 -*-
"""
created on tue apr 27 15:34:02 2021
@author: 13963

defines class to determine if compartments are neighboring based on coordinates

"""
from shapely.geometry import Polygon,LineString
from shapely.ops import cascaded_union
from util_functions import * 
from constants import *
from define_ve import *
from define_pve import *
from define_attributes_props import *


def look_up_coords(point_name,df_points): # function to look up coordinates of a point from pre-defined df_points DataFrame. support function for Polygon_area function
    x=float(df_points['x'].loc[df_points['point_id']==point_name].values[0])
    y=float(df_points['y'].loc[df_points['point_id']==point_name].values[0])
    return (x,y)



class check_neighbor:
    def __init__(self, sendingcompartment, receivingcompartment,dict_inputs):
        self.sendingcompartment=sendingcompartment
        self.receivingcompartment=receivingcompartment
        self.dict_inputs=dict_inputs
        self.df_points=self.dict_inputs['df_points']
    def is_neighbor(self):
        ve_sc=self.sendingcompartment.containingvolumeelementname
        top_sc=float(eval(ve_sc).top)  
        bottom_sc=float(eval(ve_sc).bottom) 
        pids_sc=eval(ve_sc).point_ids  
        pids_sc=pids_sc.split(' ')         
        ve_rc=self.receivingcompartment.containingvolumeelementname
        top_rc=float(eval(ve_rc).top)  
        bottom_rc=float(eval(ve_rc).bottom)  
        pids_rc=eval(ve_rc).point_ids         
        pids_rc=pids_rc.split(' ')  
        
        coords_sc=[look_up_coords(p,self.df_points) for p in pids_sc]        
        coords_rc=[look_up_coords(p,self.df_points) for p in pids_rc]   
        Polygon_sc = Polygon(coords_sc)
        Polygon_rc = Polygon(coords_rc)
        parcel_neighbor=Polygon_sc.intersects(Polygon_rc)
#        parcel_not_neighbor=Polygon_sc.disjoint(Polygon_rc)
        chk_overlap=False
        interfacial_area=0
        if parcel_neighbor:
            intersection_length=Polygon_sc.intersection(Polygon_rc).length
                
            if top_sc >= top_rc and top_rc > bottom_sc:
                z_overlap=top_rc-bottom_sc
                chk_overlap=True
                interfacial_area=z_overlap*intersection_length
                return(chk_overlap,interfacial_area)

            if top_rc >=top_sc and top_sc > bottom_rc: 
                chk_overlap=True
                z_overlap=top_sc-bottom_rc
                interfacial_area=z_overlap*intersection_length
                return(chk_overlap,interfacial_area)

            if top_sc == bottom_rc or top_rc == bottom_sc: # overlying parcels
                z_overlap=1
                chk_overlap=True
                interfacial_area=z_overlap*Polygon_sc.area
                return(chk_overlap,interfacial_area)
                        

        return(chk_overlap,interfacial_area)
        
# 