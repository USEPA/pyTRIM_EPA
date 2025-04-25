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
from define_attributes_props import *
from numpy import ndarray, repeat, all, nanmean, isnan,where

def look_up_coords(point_name,df_points): # function to look up coordinates of a point from pre-defined df_points DataFrame. support function for Polygon_area function
    x=float(df_points['x'].loc[df_points['point_id']==point_name].values[0])
    y=float(df_points['y'].loc[df_points['point_id']==point_name].values[0])
    return (x,y)


def find_interfacial_area(sc_rc_top_bottom,intersection_length,Polygon_sc,Polygon_rc): # function to determine z axis overlap between two volume elements. Inputs are list of [sc_top, sc_bottom, rc_top, rc_bottom] and polygons of sc and rc
    sc_top=sc_rc_top_bottom[0] # top of sc
    sc_bottom=sc_rc_top_bottom[1] # bottom of sc
    rc_top=sc_rc_top_bottom[2] # top of rc
    rc_bottom=sc_rc_top_bottom[3]    # bottom of rc 
    chk_overlap=False # default assumption
    interfacial_area=0         # default assumption
    flag=False
    contains_array=[type(x)==ndarray for x in sc_rc_top_bottom] # list whose elements indicate of sc_rc list contains arrays or not    
    if True in contains_array: # if any of the top bottom variables are arrays
        array_size=sc_rc_top_bottom[contains_array.index(True)].shape[0] # determine array size (assumed to be equal for all)
        sc_rc_top_bottom_array=[] # initialize array version of scrctopbottom 
        for index,x in enumerate(contains_array): # loop over four elements of list
            if x==True: # if an array
                arr=sc_rc_top_bottom[index] # the array element
                arrmean = nanmean(arr) # mean of arr ay ignroing nans
                idx = where(isnan(arr)) # nan location
                if len(idx)>0:
                    arr[idx] = arrmean # fill array with means
                sc_rc_top_bottom_array.append(arr) # append array after replacing nans with missing
            else:
                sc_rc_top_bottom_array.append(repeat(sc_rc_top_bottom[index],array_size)) # convert to array if not an array with consistent array size
        sc_top=sc_rc_top_bottom_array[0]    # array version of sc_top
        sc_bottom=sc_rc_top_bottom_array[1]  # array version of sc_bottom    
        rc_top=sc_rc_top_bottom_array[2]    # array version of rc_top
        rc_bottom=sc_rc_top_bottom_array[3] # array version of rc_bottom

        if all(sc_top-rc_top>=0) and all(rc_top-sc_bottom>0): # if 1) all elements of sc top are greater than or equal to rc top and 2) all elements of rc top are greater than sc bottom
            z_overlap=rc_top-sc_bottom
            chk_overlap=True
            interfacial_area=z_overlap*intersection_length
            flag=True
            return(chk_overlap,interfacial_area)

        if all(rc_top-sc_top>=0) and all(sc_top-rc_bottom>0): # if 1) all elements of rc top are greater than or equal to sc top and 2) all elements of sc top are greater than rc bottom
            z_overlap=sc_top-rc_bottom
            chk_overlap=True
            interfacial_area=z_overlap*intersection_length
            flag=True
            return(chk_overlap,interfacial_area)

        if (all(sc_top-rc_bottom==0) or all(rc_top-sc_bottom==0)) and Polygon_sc.intersection(Polygon_rc).area>0: ## overlying parcels
            z_overlap=1 
            chk_overlap=True
            interfacial_area=z_overlap*Polygon_sc.intersection(Polygon_rc).area        
            flag=True
            return(chk_overlap,interfacial_area)

        if not flag:
            print ("CONDITION NOT MET")

      
    else: # static not array conditions. Code below is same as pseudo source method                                            


        if sc_top >= rc_top and rc_top > sc_bottom:
            z_overlap=rc_top-sc_bottom
            chk_overlap=True
            interfacial_area=z_overlap*intersection_length
            return(chk_overlap,interfacial_area)

        if rc_top >=sc_top and sc_top > rc_bottom: 
            z_overlap=sc_top-rc_bottom
            chk_overlap=True
            interfacial_area=z_overlap*intersection_length
            return(chk_overlap,interfacial_area)

        if (sc_top == rc_bottom or rc_top == sc_bottom) and Polygon_sc.intersection(Polygon_rc).area>0: # overlying parcels
            z_overlap=1  # neeed to figure out uppper air compartment plan
            chk_overlap=True
            interfacial_area=z_overlap*Polygon_sc.intersection(Polygon_rc).area        
            return(chk_overlap,interfacial_area)

        if not flag:
            print ("CONDITION NOT MET")


    return(chk_overlap,interfacial_area)




class check_neighbor:
    def __init__(self, sendingcompartment, receivingcompartment,dict_inputs):
        self.sendingcompartment=sendingcompartment
        self.receivingcompartment=receivingcompartment
        self.dict_inputs=dict_inputs
        self.df_points=self.dict_inputs['df_points']
    def is_neighbor(self):
        ve_sc=self.sendingcompartment.containingvolumeelementname
        if type(eval(ve_sc).top)==str: 
            top_sc=float(eval(ve_sc).top)  
        else:
            top_sc=eval(ve_sc).top
        if type(eval(ve_sc).bottom)==str: 
            bottom_sc=float(eval(ve_sc).bottom)  
        else:
            bottom_sc=eval(ve_sc).bottom            
        pids_sc=eval(ve_sc).point_ids  
        pids_sc=pids_sc.split(' ')         
        ve_rc=self.receivingcompartment.containingvolumeelementname
        if type(eval(ve_rc).top)==str: 
            top_rc=float(eval(ve_rc).top)  
        else:
            top_rc=eval(ve_rc).top
        if type(eval(ve_rc).bottom)==str: 
            bottom_rc=float(eval(ve_rc).bottom)  
        else:
            bottom_rc=eval(ve_rc).bottom            
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
                
            # new for sediment burial sink 
            if Polygon_sc.intersection(Polygon_rc).area>0 and self.sendingcompartment.category=='abiotic | sediment | sediment - default' and self.receivingcompartment.category=='sink | abiotic | sediment | sediment - default': # overlying parcels
                z_overlap=1
                chk_overlap=True
                interfacial_area=z_overlap*Polygon_sc.intersection(Polygon_rc).area
                return(chk_overlap,interfacial_area)

            ## call function to find overlap
            sc_rc_top_bottom=[top_sc,bottom_sc,top_rc,bottom_rc]
            chk_overlap,interfacial_area=find_interfacial_area(sc_rc_top_bottom,intersection_length,Polygon_sc,Polygon_rc)
            print (eval(ve_sc).ve_name,eval(ve_rc).ve_name,chk_overlap,interfacial_area)

        return(chk_overlap,interfacial_area)
        
# 