# -*- coding: utf-8 -*-

#Builder Class Module - ParcelCollection
#This class contains code relevant to a Parcel collection object

from .Parcel import Parcel
import ipdb #for debugging

#any custom exceptions? These go here

class ParcelCollection:
    #any class specific variables?
    
    def __init__(self):
        #ParcelCollection constructor - initialize the basic properties of the parcel collector object
        self.pParcelDictionary = {}
        self.pParcelsByName = {}

    def __repr__(self):        
        #__repr__ is needed to print object attributes nicely - try commenting out this dunder method and printing out an object
        return f"{self.__class__.__name__}({self.pParcelDictionary} AND {self.pParcelsByName})"
    
    def __str__(self):
        #using __str__ to customize "print(obj)"
        return f'Parcel dictionary: {self.pParcelDictionary} & Parcels by name: {self.pParcelsByName}'    
    
    def Exists(self, ParcelName):
        #checks if a parcel exists in the parcel collection
        if ParcelName in self.pParcelDictionary and ParcelName in self.pParcelsByName:
            return True
        else:
            return False
    
    def Add(self, ParcelName, PCategory, LandUse, Source):
        #ipdb.set_trace()
        #parcel name must be unique for there to be an addition
        if not self.Exists(ParcelName):
            Temp = Parcel(ParcelName, self, PCategory, LandUse, Source) #self.__class__.__name__ #"self.__class__.__name__" is just another way of saying 
            #"ParcelCollection" without repeating the name. In case we decide to change the name later, we have one less place to make edits
        else:
            #to avoid making duplicates, first remove the entry (will add back later)
            Temp = self.pParcelDictionary[ParcelName]
            self.pParcelDictionary.pop(ParcelName)
            self.pParcelsByName.pop(Temp.Name)
        
        #add entry
        self.pParcelDictionary[ParcelName] = Temp
        self.pParcelsByName[Temp.Name] = Temp
    
    def Remove(self,ParcelName):
        if self.Exists(ParcelName):
            self.pParcelDictionary.pop(ParcelName) #if ParcelName exist, then remove. Otherwise return KeyError
            self.pParcelsByName.pop(ParcelName)
        else:
            raise KeyError('Parcel does not exist')       
    
    def All(self):
        #returns a collection (list) of parcel objects, which can be iterated
        All = []
        for p in self.pParcelDictionary:
            All.append(self.pParcelDictionary[p])
        return(All)
        
    @property
    def Count(self):
        Count = len(self.All())
        return(Count)        
        
    @property
    def LandParcels(self):
        #a parcel collection of all land parcels (Land only and Land and Air)
        LandParcels = ParcelCollection() 
        for Parcel_ in self.All(): #var_ is just a variable with an underscore (no deeper meaning); used it so I can get to use "Parcel" to make code readable
            if Parcel_.IsLand:
                LandParcels.Add(Parcel_.Name, Parcel_.PCategory, Parcel_.LandUse, Parcel_.Source)
        return(LandParcels)
#                
    @property
    def WaterParcels(self):
        #a parcel collection of all water parcels (water only and Water and Air)
        WaterParcels = ParcelCollection()
        for Parcel_ in self.All():
            if Parcel_.IsWater:
                WaterParcels.Add(Parcel_.Name, Parcel_.PCategory, Parcel_.LandUse, Parcel_.Source)
        return(WaterParcels)
    
    @property
    def AirParcels(self):
        #a parcel collection of all air parcels (air only, water and air, and land and air)
        AirParcels = ParcelCollection()
        for Parcel_ in self.All():
            if Parcel_.IsAir:
                AirParcels.Add(Parcel_.Name, Parcel_.PCategory, Parcel_.LandUse, Parcel_.Source)
        return(AirParcels)
        
    @property
    def SurfaceParcels(self):
        #a parcel collection of all surface parcels (Land only and Land and Air AND water only and water and Air)
        SurfaceParcels = ParcelCollection()
        for Parcel_ in self.All():
            if Parcel_.IsSurface:
                SurfaceParcels.Add(Parcel_.Name, Parcel_.PCategory, Parcel_.LandUse, Parcel_.Source)
        return(SurfaceParcels)
        
    def item(self,ParcelName):
        #return the value of a key using pParcelDictionary
        if self.Exists(ParcelName):
            item = self.pParcelDictionary[ParcelName]
        else:
            item = "Does not exist" #we could have a formal exception raised here if we build a custom exception class. Ignoring that for now
        return(item)
        
    def ItemByName(self,Name):
        #return the value of a key using pParcelsByName
        if Name in self.pParcelsByName:
            ItemByName = self.pParcelsByName[Name]
        else:
            ItemByName = "Does not exist"
        return(ItemByName)
    
    def RemoveAll(self):
        #remove all entries from a collection
        self.pParcelDictionary.clear()
        self.pParcelsByName.clear()

#end of class
##################################################################################################################
        