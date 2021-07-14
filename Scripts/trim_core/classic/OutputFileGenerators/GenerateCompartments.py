# -*- coding: utf-8 -*-

#builds the compartments file.

from ..Classes.OutputFormatter import OutputFormatter
from ..Classes.Parcel import Parcel
import datetime
import ipdb

def GenerateCompartments(FileName, ScenarioName, ScenarioDescription, Parcels, Fish, Land_ErosionParameters):
    
    CompFormatter = OutputFormatter(FileName)
    CompFormatter.PrintLine("TRIM.FaTE scenario compartments", True)
    CompFormatter.PrintLine("Biotic and non-primary abiotoc compartments", True)   
    CompFormatter.PrintCell("")
    CompFormatter.PrintLine(ScenarioName, True)
    CompFormatter.PrintLine(ScenarioDescription, True)
    CompFormatter.PrintCell("")
    CompFormatter.LinePrint("Generated:", str(datetime.datetime.now()), True) 
    CompFormatter.PrintCell("")
    CompFormatter.PrintLine("Version: 1")
    
    CompFormatter.PrintCell("")
    CompFormatter.Divider("Air", True)
    CompFormatter.PrintCell("")
    
    for parcel in Parcels.AirParcels.All():
        CompFormatter.PrintLine(str("VolumeElement: Air_" + parcel.Name))
        CompFormatter.PrintLine("Compartment: Degradation/Reaction Sink")
    
    CompFormatter.PrintCell("")
    CompFormatter.Divider("Water", True)
    CompFormatter.PrintCell("")
    
    for parcel in Parcels.WaterParcels.All(): 
        CompFormatter.PrintLine(str(parcel.Name), True)
        
        Fish_comp = parcel.Fish(Fish.index.tolist(), Fish["Aquatic Biota (Consuming Organism)"].tolist(), Fish.Location.tolist())
        
        for Prefix in ("SW", "Sed"):
            CompFormatter.PrintLine(str("VolumeElement: " + str(Prefix) + "_" + parcel.Name))
            CompFormatter.PrintLine("Compartment: Degradation/Reaction Sink")
            if Prefix == "SW":
                CompFormatter.PrintLine("Compartment: Flush Rate Sink")
                
            for item in Fish_comp[Prefix]:
                CompFormatter.PrintLine(str("Compartment: " + str(item)))
        CompFormatter.PrintCell("")

    CompFormatter.PrintCell("")       
    CompFormatter.Divider("Land", True)
    CompFormatter.PrintCell("")
    
    for parcel in Parcels.LandParcels.All():
        CompFormatter.PrintLine(str(str(parcel.Name) + " land use: " + str(parcel.LandUse)), True)
        
        for Prefix in ("GW_", "VadoseSoil_", "RootSoil_", "SurfSoil_"):
            CompFormatter.PrintLine(str("VolumeElement: " + str(Prefix) + str(parcel.Name)))
            CompFormatter.PrintLine("Compartment: Degradation/Reaction Sink")
            
        CompFormatter.PrintLine("Compartment: Soil Advection Sink") 
        
        AllLandUses = Land_ErosionParameters.index.tolist()[2:]
        
        if parcel.LandUse not in AllLandUses:
            CompFormatter.PrintLine("land use not found!", True) 
        else:
            plant_type = Land_ErosionParameters["Plant type"][Land_ErosionParameters.index == parcel.LandUse][0]
            CompFormatter.PrintLine(str("CompositeCompartment: " + str(plant_type))) 
        CompFormatter.PrintCell("")
      
        
if __name__ == "__main__":
    GenerateCompartments(str(Out+"Compartment.txt"), "Foundries", "Testing", Parcels, Fish, Land_ErosionParameters)        
        
        
        

