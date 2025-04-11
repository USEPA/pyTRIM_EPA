# -*- coding: utf-8 -*-
"""
Created on Mon Jan 23 11:59:08 2023

@author: 13963
"""
from find_neighbors import *
from shapely.geometry import Polygon,LineString,Point
from numpy import sqrt,nan,log,exp,zeros,sin,cos,radians,ndarray,repeat,isnan,nanmean,where
from util_functions import *

sec_per_day=24*60*60
        
def look_up_coords(point_name,df_points): # function to look up coordinates of a point from pre-defined df_points DataFrame. support function for Polygon_area function
    x=float(df_points['x'].loc[df_points['point_id']==point_name].values[0])
    y=float(df_points['y'].loc[df_points['point_id']==point_name].values[0])
    return (x,y)

def angle_convert(theta): # convert clockwise to anticlockwise and rotates by 90 degrees. TRIM input is clockwise from north=0 (representing direction wind is coming from) whereas I want anticlockwise with zero=E (so that angle indicates where the wind is blowing).
    c=360-theta+90+180 # 360 minus theta converts clockwise to a/c; adding 90 rotates base to E; adding 180 changes blowing from to blowing to
    cmod=c%360
    return(cmod)

def find_external_lines(df_parcels,df_points,sending_parcel_points): # function to find outlying parcels and length of boundary
   
   pids=list(df_parcels['point_ids'])
   polys=[] # list of Polygon objects
   for pid in pids: # loop over parcels 
       points=pid.split(' ') # get parcel points
       poly_coords=[] # list of x,y tuples
       for point in points: # loop over points in parcel
           # x_y_coords=look_up_coords(point,self.df_points) # get x,y
           x_y_coords=look_up_coords(point,df_points) # get x,y

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
   points=sending_parcel_points.split(' ') # get parcel points
   poly_coords=[] # list of x,y tuples
   for point in points: # loop over points in parcel
       # x_y_coords=look_up_coords(point,self.df_points) # get x,y    
       x_y_coords=look_up_coords(point,df_points) # get x,y    

       poly_coords.append(x_y_coords) # add to parcel list 
   poly_lines=[] # list of lines in Polygon
   for index, x in enumerate(poly_coords):  # loop over exterior coords to create and populate Polygon line objects list
       if index<len(poly_coords)-1: 
           poly_lines.append(LineString([poly_coords[index],poly_coords[index+1]]))# join successive points of outer Polygon
       else:
           poly_lines.append(LineString([poly_coords[index],poly_coords[0]])) # join last and first
   parcel_ext_lines=[]
   for point_index,poly_line in enumerate(poly_lines): # loop over Polygon lines (point_index will track position in points list)
       for ex_line in ext_lines:
           if poly_line.intersects(ex_line) and poly_line.intersection(ex_line).length>0.1:
               if point_index<len(poly_lines)-1:
                   parcel_ext_lines.append((points[point_index],points[point_index+1])) # list of tuples of exterior facing lines (point 1, point 2)
               else:
                   parcel_ext_lines.append((points[point_index],points[0])) # list of tuples of exterior facing lines (last to first connection)

   
   return(parcel_ext_lines)     


def find_z_overlap(sc_rc_top_bottom,Polygon_sc,Polygon_rc): # function to determine z axis overlap between two volume elements. Inputs are list of [sc_top, sc_bottom, rc_top, rc_bottom] and polygons of sc and rc
    sc_top=sc_rc_top_bottom[0] # top of sc
    sc_bottom=sc_rc_top_bottom[1] # bottom of sc
    rc_top=sc_rc_top_bottom[2] # top of rc
    rc_bottom=sc_rc_top_bottom[3]    # bottom of rc 
    contains_array=[type(x)==ndarray for x in sc_rc_top_bottom] # list whose elements indicate of sc_rc list contains arrays or not    
    z_overlap=0

    if True in contains_array: # if any of the top bottom variables are arrays
        array_size=sc_rc_top_bottom[contains_array.index(True)].shape[0] # determine array size (assumed to be equal for all)
        sc_rc_top_bottom_array=[] # initialize array version of scrctopbottom 
        for index,x in enumerate(contains_array): # loop over four elements of list
            if x==True: # if an array
                # sc_rc_top_bottom_array.append(sc_rc_top_bottom[index]) # append as is if array
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
            return(z_overlap)
        if all(rc_top-sc_top>=0) and all(sc_top-rc_bottom>0): # if 1) all elements of rc top are greater than or equal to sc top and 2) all elements of sc top are greater than rc bottom
            z_overlap=sc_top-rc_bottom
            return(z_overlap)
        if (all(sc_top-rc_bottom==0) or all(rc_top-sc_bottom==0)) and Polygon_sc.intersection(Polygon_rc).area>0: ## overlying parcels
            z_overlap=0 
            return(z_overlap)

        
    else: # static not array conditions. Code below is same as pseudo source method
        if sc_top >= rc_top and rc_top > sc_bottom:
            z_overlap=rc_top-sc_bottom

        if rc_top >=sc_top and sc_top > rc_bottom: 
            z_overlap=sc_top-rc_bottom

        if (sc_top == rc_bottom or rc_top == sc_bottom) and Polygon_sc.intersection(Polygon_rc).area>0: # overlying parcels
            z_overlap=0#'Full' # neeed to figure out uppper air compartment plan
        
    return (z_overlap)


class advection_from_air_to_air_alginstid_4075:
    def __init__(self, constants,containingscenario,currentchemical,sendingcompartment, receivingcompartment,dict_inputs):
        self.name='advection from air to air(alginstid_4075)'
        self.constants=constants
        self.containingscenario=containingscenario
        self.currentchemical=currentchemical
        self.sendingcompartment=sendingcompartment
        self.receivingcompartment=receivingcompartment
        self.category='advection'
        self.chemicalcategory='all'
        self.doestransformchemical='False'
        self.transportchemical='True'
        self.enabled='True'
        self.isdefaultforcategory='True'
        self.mate='<unset>'
        self.receivingchemicalname='replaceme'
        self.receivingcompartmentcategory='abiotic | air | air - default'
        self.sendingcompartmentcategory='abiotic | air | air - default'
        self.sendingchemicalname='replaceme'
        self.dict_inputs=dict_inputs
        self.df_points=self.dict_inputs['df_points']
    @property
    def transferfactor(self):
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

        ## call function to find overlap
        sc_rc_top_bottom=[top_sc,bottom_sc,top_rc,bottom_rc]
        z_overlap=find_z_overlap(sc_rc_top_bottom, Polygon_sc, Polygon_rc)
        # if top_sc >= top_rc and top_rc > bottom_sc:
        #     z_overlap=top_rc-bottom_sc

        # if top_rc >=top_sc and top_sc > bottom_rc: 
        #     z_overlap=top_sc-bottom_rc

        # if (top_sc == bottom_rc or top_rc == bottom_sc) and Polygon_sc.intersection(Polygon_rc).area>0: # overlying parcels
        #     z_overlap=0#'Full' # neeed to figure out uppper air compartment plan
            

        tf_vector=zeros(len(self.dict_inputs['met_dict']['vector_horizontalwindspeed'])) # initialize tf_vector
        line_segments=Polygon_sc.boundary.intersection(Polygon_rc.boundary) # find line segments of intersection of the SC and RC polygons
        try:
            line_segments = list(line_segments) # list of multiple line segments if there are multiple
        except:
            line_segments=[line_segments] # list of single line segment if there is only one
        for ls in line_segments: # loop over each intersecting line segment
            if not ls.boundary.is_empty: # if the line segment is not an empty collection (dont know why it happens rarely)   
                int_length=ls.length # length of line segment
                p1,p2=ls.boundary # endpoints of line segment
                p1_x=p1.xy[0][0] # x coordinate of one end of line segment
                p1_y=p1.xy[1][0] # y coordinate of one end of line segment
                p2_x=p2.xy[0][0] # x coordinate of other end of line segment
                p2_y=p2.xy[1][0] # y coordinate of other end of line segment 
                midpoint_ls=((p1_x+p2_x)/2,(p1_y+p2_y)/2) # midpoint coordinates of line segment
                unit_normal_ls=((p2_y-p1_y)/int_length,-(p2_x-p1_x)/int_length) # tuple of unit normal vector u, v values where initial assumption is RC to the right of SC. 
                point_check=(midpoint_ls[0]+unit_normal_ls[0],midpoint_ls[1]+unit_normal_ls[1]) # coordinate of a point at the end of the unit normal vector from the midpoint 
                Test_Point=Point(point_check[0],point_check[1]) # create test point in shapely based on above
                if Polygon_rc.contains(Test_Point): # check if a point along the unit normal vector from the midpoint is within the RC
                    pass
                else:
                    unit_normal_ls=(-(p2_y-p1_y)/int_length,(p2_x-p1_x)/int_length) # flip the original unit normal vector because it was pointing the wrong way
                    point_check=(midpoint_ls[0]+unit_normal_ls[0],midpoint_ls[1]+unit_normal_ls[1])
                    Test_Point=Point(point_check[0],point_check[1])
                    if Polygon_rc.contains(Test_Point):
                        pass
                    else:
                        print ("Problem with air compartment unit normal vector direction")

                # wind_dir_dot=sin(radians(180+self.dict_inputs['met_dict']['vector_winddirection']))*unit_normal_ls[0]+cos(180+radians(self.dict_inputs['met_dict']['vector_winddirection']))*unit_normal_ls[1] # dot product of unit wind direction and unit normal to line segment pointing out. wind direction shows where wind is blowing from so add 180 to get direction blowing in.
                # wind_dir_dot=cos(radians(90+self.dict_inputs['met_dict']['vector_winddirection']))*unit_normal_ls[0]+sin(90+radians(self.dict_inputs['met_dict']['vector_winddirection']))*unit_normal_ls[1] # dot product of unit wind direction and unit normal to line segment pointing out. wind direction shows where wind is blowing from so add 180 to get direction blowing in.
                wind_dir_dot=cos(radians(angle_convert(self.dict_inputs['met_dict']['vector_winddirection'])))*unit_normal_ls[0]+sin(radians(angle_convert(self.dict_inputs['met_dict']['vector_winddirection'])))*unit_normal_ls[1] # dot product of unit wind direction and unit normal to line segment pointing out. wind direction shows where wind is blowing from so add 180 to get direction blowing in.



                tf_temp_vector=int_length*z_overlap*self.dict_inputs['met_dict']['vector_horizontalwindspeed']*wind_dir_dot/self.sendingcompartment.volume *sec_per_day              
                tf_temp_vector[tf_temp_vector<0]=0 # replace negatives with zero
                tf_vector=tf_vector+tf_temp_vector # cumulative sum of tfs               
        return(tf_vector)

class bulk_advection_from_air_to_advection_sink_general_alginstid_4095:
    def __init__(self, constants,containingscenario,currentchemical,sendingcompartment, receivingcompartment,dict_inputs):
        self.name='bulk advection from air to advection sink, general(alginstid_4095)'
        self.constants=constants
        self.containingscenario=containingscenario
        self.currentchemical=currentchemical
        self.sendingcompartment=sendingcompartment
        self.receivingcompartment=receivingcompartment
        self.category='advection'
        self.chemicalcategory='all'
        self.doestransformchemical='False'
        self.transportchemical='True'
        self.enabled='True'
        self.isdefaultforcategory='True'
        self.mate='<unset>'
        self.receivingchemicalname='replaceme'
        self.receivingcompartmentcategory='sink | abiotic | air | air - default'
        self.sendingcompartmentcategory='abiotic | air | air - default'
        self.sendingchemicalname='replaceme'
        self.dict_inputs=dict_inputs
        self.df_points=self.dict_inputs['df_points']
        self.df_parcels=self.dict_inputs['df_parcels']

   

    @property
    def transferfactor(self):

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
        
        coords_sc=[look_up_coords(p,self.df_points) for p in pids_sc]        
        Polygon_sc = Polygon(coords_sc)
        z_overlap=top_sc-bottom_sc
        

        ext_lines=find_external_lines(self.df_parcels,self.df_points,self.sendingcompartment.parcel_points)
        
        if ext_lines==[]:
            return(0.0)
        tf_vector=zeros(len(self.dict_inputs['met_dict']['vector_horizontalwindspeed'])) # initialize tf_vector
        line_segments=[]
        for exline in ext_lines: # loop over tuples of line endpoints 
            epoint1=look_up_coords(exline[0],self.df_points) # endpoint 1 x,y coords
            epoint2=look_up_coords(exline[1],self.df_points) # endpoint 1 x,y coords
            line_segments.append(LineString([epoint1,epoint2]))

        for ls in line_segments: # loop over each intersecting line segment
            if not ls.boundary.is_empty: # if the line segment is not an empty collection (dont know why it happens rarely)   
                int_length=ls.length # length of line segment
                p1,p2=ls.boundary # endpoings of line segment
                p1_x=p1.xy[0][0] # x coordinate of one end of line segment
                p1_y=p1.xy[1][0] # y coordinate of one end of line segment
                p2_x=p2.xy[0][0] # x coordinate of other end of line segment
                p2_y=p2.xy[1][0] # y coordinate of other end of line segment 
                midpoint_ls=((p1_x+p2_x)/2,(p1_y+p2_y)/2) # midpoint coordinates of line segment
                unit_normal_ls=((p2_y-p1_y)/int_length,-(p2_x-p1_x)/int_length) # tuple of unit normal vector u, v values where initial assumption is RC to the right of SC. 
                point_check=(midpoint_ls[0]+unit_normal_ls[0],midpoint_ls[1]+unit_normal_ls[1]) # coordinate of a point at the end of the unit normal vector from the midpoint 
                Test_Point=Point(point_check[0],point_check[1]) # create test point in shapely based on above
                if not Polygon_sc.contains(Test_Point): # check if a point along the unit normal vector from the midpoint is not within the SC. If external,okay.
                    pass
                else:
                    unit_normal_ls=(-(p2_y-p1_y)/int_length,(p2_x-p1_x)/int_length) # flip the original unit normal vector because it was pointing the wrong way
                    point_check=(midpoint_ls[0]+unit_normal_ls[0],midpoint_ls[1]+unit_normal_ls[1])
                    Test_Point=Point(point_check[0],point_check[1])
                    if not Polygon_sc.contains(Test_Point):
                        pass
                    else:
                        print ("Problem with air compartment unit normal vector direction")

            
                # wind_dir_dot=sin(radians(180+self.dict_inputs['met_dict']['vector_winddirection']))*unit_normal_ls[0]+cos(180+radians(self.dict_inputs['met_dict']['vector_winddirection']))*unit_normal_ls[1]*sec_per_day
               # dot product of unit wind direction and unit normal to line segment pointing out. wind direction shows where wind is blowing from so add 180 to get direction blowing in.
                # wind_dir_dot=cos(radians(90+self.dict_inputs['met_dict']['vector_winddirection']))*unit_normal_ls[0]+sin(90+radians(self.dict_inputs['met_dict']['vector_winddirection']))*unit_normal_ls[1] # dot product of unit wind direction and unit normal to line segment pointing out. wind direction shows where wind is blowing from so add 180 to get direction blowing in.
                wind_dir_dot=cos(radians(angle_convert(self.dict_inputs['met_dict']['vector_winddirection'])))*unit_normal_ls[0]+sin(radians(angle_convert(self.dict_inputs['met_dict']['vector_winddirection'])))*unit_normal_ls[1] # dot product of unit wind direction and unit normal to line segment pointing out.     
                tf_temp_vector=int_length*z_overlap*self.dict_inputs['met_dict']['vector_horizontalwindspeed']*wind_dir_dot/self.sendingcompartment.volume *sec_per_day               
                tf_temp_vector[tf_temp_vector<0]=0 # replace negatives with zero
                tf_vector=tf_vector+tf_temp_vector # cumulative sum of tfs               
        return(tf_vector)

        
 