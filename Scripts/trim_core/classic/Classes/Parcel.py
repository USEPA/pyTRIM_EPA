# -*- coding: utf-8 -*-

#Builder Class Module - Parcel
#This class contains code relevant to the Parcel object

from enum import Enum
#import ipdb #for debugging

class ParcelCategory(Enum): #Enum is an organized way to keep track of a group of constants
    _NoCategory = 0         #_variable means private variable that is meant for internal use only
    Air         = 2**0
    Land        = 2**1
    Water       = 2**2
    
class ParcelInformation(Enum):
    _NoInformation = 0
    pName          = 2**0
    pCategory      = 2**1
    pLandUse       = 2**2
    pPointsList    = 2**3
    pPointCount    = 2**4
    pArea          = 2**5

#any custom exceptions? these classes go here

class Parcel:
    #any class specific variables?
    
    def __init__(self, ParcelName, ParentCollection, PCategory, LandUse, Source):
        #Parcel constructor - initialize the basic properties of a parcel object
        self.ParcelName = ParcelName
        self.ParentCollection = ParentCollection
        self.PCategory = PCategory
        self.LandUse = LandUse
        self.Source = Source
        
    def __repr__(self):        
        #__repr__ is needed to print object attributes nicely - try commenting out this dunder method and printing out an object
        return f"{self.__class__.__name__}({self.ParcelName}, {self.ParentCollection}, {self.PCategory}, {self.Source})"
    
    def __str__(self):
        #using __str__ to customize "print(obj)"
        return f'Parcel name: {self.ParcelName}; Parent collection: {self.ParentCollection}; Parcel category: {self.PCategory}; Source: {self.Source}'    

    @property #property decorator used to make this method a property of the class
    def Name(self):
        #check if parcel is an air parcel
        return (self.ParcelName)

    @property 
    def Category(self):
        #assign the listed PCategory to its appropriate constant
        Category = ParcelCategory._NoCategory.value
        #ipdb.set_trace()
        if "Air" in self.PCategory: #might want to do lower case only
            Category += ParcelCategory.Air.value
        if "Land" in self.PCategory:
            Category += ParcelCategory.Land.value
        if "Water" in self.PCategory:
            Category += ParcelCategory.Water.value
        return(Category)    

    @property
    def IsAir(self):
        #check if parcel is an air parcel
        #I see an easier way to do this that doesn't involve the enums but I'm implementing as is in the VBA just in case
        #enums were used for some reason that is not obvious early on.
        #could have just done if Air in self.Category and not used numbers, but I'm not sure why numbers were used in the VBA so implementing as is in VBA
        #the syntax below is doing bitwise comparisons (unsure why the equivalent syntax, which commented next to it and does not use bitwise comparisons, was not used)
        if self.Category & ParcelCategory.Air.value > 0: #if self.Category == (ParcelCategory.Air.value) or self.Category == (ParcelCategory.Air.value + ParcelCategory.Land.value) or self.Category == (ParcelCategory.Air.value + ParcelCategory.Water.value):
            return True
        else: #==0
            return False
    
    @property
    def IsLand(self):
        #check if parcel is a land parcel
        #ipdb.set_trace()
        if self.Category & ParcelCategory.Land.value > 0: #if self.Category == (ParcelCategory.Land.value) or self.Category == (ParcelCategory.Land.value + ParcelCategory.Air.value):
            return True
        else: #==0
            return False    
    
    @property
    def IsWater(self):
        #check if parcel is a water parcel
        if self.Category & ParcelCategory.Water.value > 0: #if self.Category == (ParcelCategory.Water.value) or self.Category == (ParcelCategory.Water.value + ParcelCategory.Air.value):
            return True
        else: #==0
            return False    

    @property
    def IsSurface(self):
        #check if parcel is a land or water parcel
        if self.Category & (ParcelCategory.Land.value | ParcelCategory.Water.value) > 0: #self.IsWater or self.IsLand:
            return True
        else: 
            return False
        
    @property
    def IsSource(self):
        #check if parcel is a source parcel
        if self.Source == True:
            return True
        else:
            return False
    
    def Fish(self, lakenames, fishnames, locations): 
        #returns a dictionary of this parcel's fish compartments, by SW and Sed, with their corresponding aquatic biota
        
        assert isinstance(lakenames, list)
        assert isinstance(fishnames, list)
        assert isinstance(locations, list)        
        assert len(lakenames) == len(fishnames) == len(locations) #making sure all three arguments MUST have the same length
        
        Fish = {}
                
        if self.IsWater:
            ParcelName = self.Name
            LakeNames = lakenames
            FishNames = fishnames
            Locations = locations
            
            Fish_SW_Vals = []
            Fish_Sed_Vals = []
            
            for i, lake in enumerate(LakeNames):
                if lake == ParcelName:
                    loc = Locations[i]
                    fish = FishNames[i]
                    
                    if loc == "SW":
                        Fish_SW_Vals.append(fish)
                    elif loc == "Sed":
                        Fish_Sed_Vals.append(fish)
                        
            Fish["SW"] = Fish_SW_Vals
            Fish["Sed"] = Fish_Sed_Vals
            
            return(Fish)
            
    def Plants(self, landuses, planttypes, compositeplantcomps): #compositeplantcomps - dictionary[Key] = [list]
        #returns a list of all this parcel's plant compartments
        
        assert len(landuses) == len(planttypes) #could use a dictionary instead of lists for these variables though
        assert isinstance(landuses, list)
        assert isinstance(planttypes, list)
        assert isinstance(compositeplantcomps, dict)
               
        Plants = []
        
        if self.IsLand:
            #ignoring check here for now
            PlantTypes = planttypes
            LandUses = landuses
            PlantType = PlantTypes[LandUses.index(self.LandUse)] #return the plant type for this parcel's specified land use type
            #ignoring check here for now
            CompositePlantComps = compositeplantcomps
            comps = CompositePlantComps[PlantType]
            
            for component in comps:
                #ipdb.set_trace()
                Plants.append(str(component + " in " + PlantType)) #e.g. "Leaf - Grasses/Herbs in Grasses/Herbs"
            
            return(Plants)
    
    def VolumeElements(self):
        #returns a list of all this parcel's volume elements
        #self.Name == self.ParcelName below (redundant and one could be removed)      
        Prefixes = [] #a list of prefixes
        
        if self.IsAir:
            Prefixes.append("Air_") #Add air prefix 
            
            if self.IsSource:
                Prefixes.append("UpperAir_") #Add source prefix
                
        if self.IsLand:
            Prefixes.extend(["SurfSoil_", "RootSoil_", "VadoseSoil_", "GW_"]) #Add land prefixes
            
        if self.IsWater:
            Prefixes.extend(["SW_", "Sed_"]) #Add water prefixes
        
        VolumeElements = [str(V+self.Name) for V in Prefixes]
        return(VolumeElements)
        
    def Compartments(self, landuses:list, planttypes:list, compositeplantcomps:dict, fishnames:list, lakenames:list, locations:list) -> list:
        #returns a list of all this parcel's compartments
        #illustrating how to do variable type and function type declarations in python
        
        Compartments = []
        Fish = {}
        Prefixes = []
        
        #plant compartment variables
        LandUses = landuses
        PlantTypes = planttypes
        CompositePlantComps = compositeplantcomps
        
        #fish compartment variables
        FishNames = fishnames
        LakeNames = lakenames
        Locations = locations
        
        ParcelName = self.Name
        
        if self.IsAir:
            Prefixes.extend(["Air in Air_",
                             "Degradation/Reaction Sink in Air_"]) #Air volume elements prefixes
            
        if self.IsWater:
            Prefixes.extend(["Surface water in SW_","Flush Rate Sink in SW_","Sediment in Sed_"]) #Water volume elements prefixes
            Fish = self.Fish(LakeNames, FishNames, Locations)
            
            for V in ["SW","Sed"]:
                Prefixes.append(str("Degradation/Reaction Sink in " + V + "_"))
                
                for fish in Fish[V]:
                    Prefixes.append(str(fish + " in " + V + "_"))
                
        if self.IsLand:
            Prefixes.extend(["Soil - Surface in SurfSoil_",
                             "Soil Advection Sink in SurfSoil_",
                             "Soil - Root Zone in RootSoil_",
                             "Soil - Vadose Zone in VadoseSoil_",
                             "Groundwater in GW_"])
            
            for V in ["SurfSoil_", "RootSoil_", "VadoseSoil_", "GW_"]:
                Prefixes.append(str("Degradation/Reaction Sink in ") + V)
            
            #ipdb.set_trace()
            for V in self.Plants(LandUses, PlantTypes, CompositePlantComps):
                Prefixes.append(str(V + " in SurfSoil_"))
        
        Compartments = [str(V + ParcelName) for V in Prefixes]
        
        return(Compartments)

#end of class
##################################################################################################################
        