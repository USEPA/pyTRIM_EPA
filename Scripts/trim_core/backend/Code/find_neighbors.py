# -*- coding: utf-8 -*-
"""
Created on Tue Apr 27 15:34:02 2021
@author: 13963

Defines class to determine if compartments are neighboring based on coordinates

"""
from shapely.geometry import Polygon,LineString
from shapely.ops import cascaded_union
from util_functions import * 
from constants import *
from define_ve import *
from define_pve import *
from define_attributes_props import *


def look_up_coords(point_name,df_points): # function to look up coordinates of a point from pre-defined df_points dataframe. support function for polygon_area function
    x=float(df_points['x'].loc[df_points['Point_ID']==point_name].values[0])
    y=float(df_points['y'].loc[df_points['Point_ID']==point_name].values[0])
    return (x,y)



class check_neighbor:
    def __init__(self, SendingCompartment, ReceivingCompartment,dict_inputs):
        self.SendingCompartment=SendingCompartment
        self.ReceivingCompartment=ReceivingCompartment
        self.dict_inputs=dict_inputs
        self.df_points=self.dict_inputs['df_points']
    def is_neighbor(self):
        VE_SC=self.SendingCompartment.containingVolumeElement
        Top_SC=float(eval(VE_SC).Top)  
        Bottom_SC=float(eval(VE_SC).Bottom) 
        PIDs_SC=eval(VE_SC).Point_IDs  
        PIDs_SC=PIDs_SC.split(' ')         
        VE_RC=self.ReceivingCompartment.containingVolumeElement
        Top_RC=float(eval(VE_RC).Top)  
        Bottom_RC=float(eval(VE_RC).Bottom)  
        PIDs_RC=eval(VE_RC).Point_IDs         
        PIDs_RC=PIDs_RC.split(' ')  
        
        coords_SC=[look_up_coords(p,self.df_points) for p in PIDs_SC]        
        coords_RC=[look_up_coords(p,self.df_points) for p in PIDs_RC]   
        polygon_SC = Polygon(coords_SC)
        polygon_RC = Polygon(coords_RC)
        parcel_neighbor=polygon_SC.intersects(polygon_RC)
        parcel_not_neighbor=polygon_SC.disjoint(polygon_RC)
        chk_overlap=False
        interfacial_area=0
        if parcel_neighbor:
            intersection_length=polygon_SC.intersection(polygon_RC).length
                
            if Top_SC >= Top_RC and Top_RC > Bottom_SC:
                z_overlap=Top_RC-Bottom_SC
                chk_overlap=True
                interfacial_area=z_overlap*intersection_length
                return(chk_overlap,interfacial_area)

            if Top_RC >=Top_SC and Top_SC > Bottom_RC: 
                chk_overlap=True
                z_overlap=Top_SC-Bottom_RC
                interfacial_area=z_overlap*intersection_length
                return(chk_overlap,interfacial_area)

            if Top_SC == Bottom_RC or Top_RC == Bottom_SC: # overlying parcels
                z_overlap=1
                chk_overlap=True
                interfacial_area=z_overlap*polygon_SC.area
                return(chk_overlap,interfacial_area)
                        

        return(chk_overlap,interfacial_area)
        
# 