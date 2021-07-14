# -*- coding: utf-8 -*-

#Builder Module - Layout
 
#This module contains functions for updating and getting information about the
#scenario's layout.
import numpy as np
import pandas as pd
from ..Classes.Parcel import Parcel
from ..Classes.ParcelCollection import ParcelCollection

def LoadParcels(Parcel_names:list, Parcel_category:list, Land_use:list, Source:list):
    """
    loads the current parcels from the Layout sheet, saving for access later
    """
    assert len(Parcel_names) == len(Parcel_category) == len(Land_use) == len(Source)
    
    pParcels = ParcelCollection()
    
    for i, rng in enumerate(Parcel_names):
        pParcels.Add(rng, Parcel_category[i], Land_use[i], Source[i])
    
    return(pParcels)
    
def UpdateLayout(Parcel_names:list, Parcel_category:list, Land_use:list, Source:list):
    """This is the handler for when the Layout sheet changes.
    Updates lists of surface/water/land parcels so other tabs are up to date
    """    
    #GUI supplies list of user-specified parcel information as list
  
    Parcels = LoadParcels(Parcel_names, Parcel_category, Land_use, Source)
    
    Collections = [Parcels.SurfaceParcels, Parcels.WaterParcels, Parcels.LandParcels, Parcels.AirParcels]
    
    return(Collections)   

def MergeSpaces(Text:str) -> str:
    """
    recursive function to combine consecutive spaces within a string
    """
    Text = Text.strip()
    pos = Text.find(" ")
    Merge = ""
    if pos > 0:
        Merge = str(Text[:pos]) + " " + MergeSpaces(Text[pos+1:])
    else:
        Merge = Text
    return(Merge)    
    
def GetPoints(PointList:str) -> list:
    """
    parses a user-supplied string of points into list of points 
    """
    PointList = PointList.replace(","," ")
    PointList = PointList.replace(";"," ")
    PointList = MergeSpaces(PointList)
    PointList = PointList.split(" ")
    return(PointList)
    
def CountPoints(ParcelPoints:str) -> int:
    if len(ParcelPoints) == 0:
        CountPoints = 0
    else:
        Points = GetPoints(ParcelPoints)
        CountPoints = len(Points)
    return(CountPoints)

def PolyArea(x,y):#QA
    #https://stackoverflow.com/questions/24467972/calculate-area-of-polygon-given-x-y-coordinates
    return 0.5*(np.dot(x,np.roll(y,1))-np.dot(y,np.roll(x,1)))

def SignedArea(PointList:str, Coordinatesdf):
    """
    computes the signed (directional) area enclosed within the give vertex points
    """
    
    #adapted from http://local.wasp.uwa.edu.au/~pbourke/geometry/polyarea/
    
    if CountPoints(PointList) < 3: raise KeyError("Not enough points were given") #break with KeyError rather than return a SignedArea = 0
    
    Points = GetPoints(PointList)    
    Pointsdf = Coordinatesdf.loc[Points,["X","Y"]]
    XCoordinates = list(Pointsdf.loc[:,"X"])
    YCoordinates = list(Pointsdf.loc[:,"Y"])
    
    assert len(Points) == len(XCoordinates) == len(YCoordinates)
    
    Min_x = min(Coordinatesdf.loc[:,"X"])
    Min_y = min(Coordinatesdf.loc[:,"Y"])
    
    #connect the last to the first
    Previous = Points[len(Points)-1]
    Previous_x = XCoordinates[len(Points)-1]
    Previous_y = YCoordinates[len(Points)-1]
    
    #offset by minimums so the multiplication doesn't get out of hand
    Previous_x = Previous_x - Min_x
    Previous_y = Previous_y - Min_y
    
    Area = 0
    
    for Point in Points:
        #get coordinates of the point using its position
        Point_x = XCoordinates[Points.index(Point)]
        Point_y = YCoordinates[Points.index(Point)]
        
        #offset by minimums so the multiplication doesn't get out of hand
        Point_x = Point_x - Min_x
        Point_y = Point_y - Min_y

        Area = Area + (Previous_x * Point_y - Point_x * Previous_y)
        
        #connect this point to the next
        Previous = Point
        Previous_x = Point_x
        Previous_y = Point_y

    Area = (Area) * 0.5
    QA_Area = PolyArea(XCoordinates,YCoordinates) #QA Eventually this will be used but need to be sure if it handles calculation the same way
    diff = (((Area)-QA_Area)/QA_Area)*100#temp
    
    if diff > 3.09798939804452e-08: raise KeyError("wrong area calculation")#temp
    return(Area,QA_Area,diff)
    
def ComputeEnclosedArea(PointList:str, Coordinatesdf):
    """
    returns the total area enclosed within the given vertex points (unsigned)  
    """
    Area = SignedArea(PointList, Coordinatesdf)
    return(abs(Area[0]))
    
def ParcelPointsArea(ParcelName:str, Parceldf) -> float:
    """
    returns the number of points and the area of a parcel
    """
    assert len(Parceldf.loc[ParcelName,["ParcelCategory"]]) == 1 #make sure there's only one parcel with this name
    
    ParcelPoints = Parceldf.loc[ParcelName,["Points"]][0]
    NumPoints = CountPoints(ParcelPoints)
    
    Area = ComputeEnclosedArea(ParcelPoints)
    
    return (NumPoints, Area)
    
def ComputeCentroid(PointList:str, Coordinatesdf):
    """
    returns the geometric center of the given points, length 2 array with x, y coordinates.    
    """
    if CountPoints(PointList) < 3: raise KeyError("Not enough points were given")
    
    Points = GetPoints(PointList)
    Pointsdf = Coordinatesdf.loc[Points,["X","Y"]]
    XCoordinates = list(Pointsdf.loc[:,"X"])
    YCoordinates = list(Pointsdf.loc[:,"Y"])
    
    assert len(Points) == len(XCoordinates) == len(YCoordinates)
    
    Min_x = min(Coordinatesdf.loc[:,"X"])
    Min_y = min(Coordinatesdf.loc[:,"Y"])
    Origin = [Min_x, Min_y] 
    
    Center = [0,0]
    #ALL GOOD UP
    
    #connect the last to the first
    Previous = Points[len(Points)-1]
    Previous_x = XCoordinates[len(Points)-1]
    Previous_y = YCoordinates[len(Points)-1]
    
    Previous = [Previous_x - Min_x, Previous_y - Min_y]

    for Point in Points:    
        Current = [(XCoordinates[Points.index(Point)]) - Min_x, (YCoordinates[Points.index(Point)]) - Min_y]
    
        Factor = Previous[0] * Current[1] - Current[0] * Previous[1]
        
        for i in range(2):
            Center[i] = Center[i] + Factor * (Previous[i] + Current[i])
        
        Previous = Current
    
    Area = SignedArea(PointList, Coordinatesdf)[0] #area could be negative
    
    Factor = 1/6/Area #factor could be negative
    
    #need to make sure this was the intended implementation: factor could be negative, leading to a negative Center[0]*Factor being added to Min_x
    #Compare that with area always being positive so factor is always positive which leads to a positive Center[0]*Factor being added to Min_x
    Center = [Center[0]*Factor + Min_x, Center[1] * Factor + Min_y] #Factor could be negative!
    
    #alternative: https://stackoverflow.com/questions/19684995/how-to-calculate-centroid-of-x-y-coordinates-in-python
    Center2 = [sum(XCoordinates)/len(XCoordinates), sum(YCoordinates)/len(YCoordinates)]    
    diff = [((Center[0] - Center2[0])/Center2[0])*100, ((Center[1] - Center2[1])/Center2[1])*100]
    avg_diff = (diff[0]+diff[1])/2
    
    if avg_diff > 0.04: raise KeyError("wrong centroid calculation")
    
    return(Center[0],Center[1],Center2[0],Center2[1],diff[0],diff[1],avg_diff)   

def ComputeCentroidX(ParcelName:str, Parceldf, Coordinatesdf):
    ParcelPoints = Parceldf.loc[ParcelName,["Points"]][0]  
    CentroidX = ComputeCentroid(ParcelPoints, Coordinatesdf)[0]
    return(CentroidX)
    
def ComputeCentroidY(ParcelName:str, Parceldf, Coordinatesdf):
    ParcelPoints = Parceldf.loc[ParcelName,["Points"]][0]    
    CentroidY = ComputeCentroid(ParcelPoints, Coordinatesdf)[1]
    return(CentroidY)    
    
def ConcatenateWithSpaces(*args:str) -> str:
    """
    concatenates a number of str arguments with space
    """
    concat = ""
    for i in args:
        concat += i.strip() + " "
    concat = concat.strip()
    return(concat)
   
def MMultPower(SquareMatrix, Power:int):
    """
    Multiplies a square matrix by itself <Power> times, or until steady-state.
    """
#this function is used to find tributary_termination_matrix and runoff_termination_matrix

#runoff_termination_matrix	=MMultPower(watershed_matrix, 300)
#tributary_termination_matrix	=MMultPower(tributary_matrix, 300)

    
#this function is probably not being used for anything because I put a stop in the function and all code run without stop

    Previous = SquareMatrix
    Power -= 1
    while Power > 0:
        try:#try running the code below
            Product = Previous @ SquareMatrix
        except Exception:#if an exception is raised
            #MMultPower = Product #unsure about this line
            return("There was an error.")
        else:#if no exception is raised
            if Product == Previous:
                return(Product)
            else: 
                Previous = Product
                Power -= 1
    return(Product)

#=data.apply(lambda x: result.Add(x["Name"],x["Category"],x["Source"]),axis=1)

#Parceldf["NumPoints"] = Parceldf.apply(lambda x: ParcelPointsArea(x.index)[0],axis=1)
#Parceldf["Area"] = Parceldf.apply(lambda x: ParcelPointsArea(x.index)[1],axis=1)
