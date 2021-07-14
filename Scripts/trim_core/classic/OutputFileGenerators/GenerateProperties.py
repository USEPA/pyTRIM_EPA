# -*- coding: utf-8 -*-

#create the sources library import file.
import numpy as np
from ..Classes.OutputFormatter import OutputFormatter
import datetime
import math
import ipdb
import re

def GenerateProperties(FileName, ScenarioName, ScenarioDescription, Parcels, Parameters, Land_SedDeliv, Lakes, Fish, Soil, Land_ErosionParameters, Watersheds):
    #bulds the properties file 
    
    PropFormatter = OutputFormatter(FileName)
    PropFormatter.PrintLine("TRIM.FaTE scenario properties", True)
    PropFormatter.PrintCell("")
    PropFormatter.PrintLine(ScenarioName, True)
    PropFormatter.PrintLine(ScenarioDescription, True)
    PropFormatter.PrintCell("")
    PropFormatter.LinePrint("Generated:", str(datetime.datetime.now()), True)
    PropFormatter.PrintCell("")
    PropFormatter.PrintLine("*****************************************************", True)  
    PropFormatter.PrintLine("NOTE: You must use the TRIM.FaTE interface to perform", True)
    PropFormatter.PrintLine("  a smart link BEFORE importing this properties file!", True)
    PropFormatter.PrintLine("*****************************************************", True)
    PropFormatter.PrintCell("")    
    PropFormatter.PrintLine("Version:1")
    PropFormatter.LinePrint("Scenario:", ScenarioName)
    PropFormatter.PrintLine("Run: BaseRun")
    PropFormatter.PrintCell("")
    PropFormatter.PrintCell("")
    
    FormatSurfaceWater(PropFormatter, Lakes)
    FormatSediment(PropFormatter, Lakes)
    FormatFish(PropFormatter, Fish)
    FormatSurfaceSoil(PropFormatter, Soil)
    FormatRootSoil(PropFormatter, Soil)
    FormatVadoseSoil(PropFormatter, Soil)
    FormatGroundwater(PropFormatter, Soil)
    FormatGlobals(PropFormatter, Parcels, ScenarioName, Parameters, Land_ErosionParameters, Fish)
    FormatLinks(PropFormatter, Parcels, Watersheds)
    
    
    
def GenerateOtherProperties(FileName, ScenarioName, ScenarioDescription):
    #builds the manual properties file
    
    #OtherPropFormatter = OutputFormatter(FileName)

    #not needed
    pass    
    
def FormatErosion(PropFormatter):
    #writes total adjusted erosion rates
    
    ErosionParcels = Land_SedDeliv.index.tolist()[1:]
    ErosionRateColumn = Land_SedDeliv.iloc[1:,-2].tolist()
    PropFormatter.Divider("Erosion rates", True)
    
    for i, parcel in enumerate(ErosionParcels):
        PropFormatter.PrintLine("Compartment: Soil - Surface in SurfSoil_" + str(parcel))
        PropFormatter.PropertyValue("TotalErosionRate_kg_m2_day", "Constant", str(ErosionRateColumn[i]), "")

def FormatSurfaceWater(PropFormatter, Lakes):
    #surface water parameters
    
    LakeNames = Lakes.index.tolist()[1:]
    
    RangeNames = ["SW_Algae density in water column (g[algae]/L[water])",
                  "SW_Chloride concentration (mg/L)",
                  "SW_Chlorophyll concentration (mg/L)",
                  "SW_Organic carbon fraction in suspended sediments (unitless)",
                  "SW_pH (unitless)",
                  "SW_Suspended sed. conc. (kg[sed] / m3[water])",
                  "SW_Water temperature (degrees K)",
                  "SP_Computed flush rate (time in yr for 1 flush)" #"SW_Water retention time (d)",
                  ]
                  
    PropNames = ["AlgaeDensityInWaterColumn_g_L",
                      "ChlorideConcentration_mg_L",
                      "ChlorophyllConcentration_mg_L",
                      "OrganicCarbonContent",
                      "pH",
                      "SuspendedSedimentConcentration",
                      "WaterTemperature_K",
                      "Flushes_per_year",
                      ]
    
    PropFormatter.Divider("Surface water properties", True)
    PropFormatter.PrintCell("")
    
    for i, lake in enumerate(LakeNames):
        
        PropFormatter.PrintLine("VolumeElement: SW_" + str(lake))
        PropFormatter.PropertyValue("WaterTemperature_K", "Constant", str(Lakes[RangeNames[6]][Lakes.index==lake][0]),"")
        PropFormatter.PrintCell("")
        PropFormatter.PrintLine("Compartment: Surface water in SW_" + str(lake))
        
        for r, rng in enumerate(RangeNames):
            PropFormatter.PropertyValue(str(PropNames[r]), "Constant", str(Lakes[rng][Lakes.index==lake][0]), "")
        
        PropFormatter.PrintLine("Flowing water bodies currently unsupported in this workbook.", True)
        PropFormatter.PropertyValue("IsFlowing", "Constant", "False","")
        PropFormatter.PropertyValue("CurrentVelocity", "Constant", "0","")
        
        PropFormatter.PrintCell("")
    PropFormatter.PrintCell("")
        
def FormatSediment(PropFormatter, Lakes):
    #pass
    #sediment parameters
    LakeNames = Lakes.index.tolist()[1:]
    
    RangeNames = ["SP_Organic carbon fraction (unitless)",
                  "SP_pH (unitless)",
                  "SP_Sediment density / rho (suspended and bed sediment) (kg[sed]/m3[sed])",
                  "SP_Resuspension velocity (m[sed cmpt]/day)"]
    
    PropNames = ["OrganicCarbonContent",
                 "pH",
                 "rho",
                 "SedimentResuspensionVelocity"]
    
    PropFormatter.Divider("Sediment properties", True)
    PropFormatter.PrintCell("")        

    for i, lake in enumerate(LakeNames):
        
        PropFormatter.PrintLine(str("Compartment: Sediment in Sed_" + str(lake)))
        
        for i, rng in enumerate(RangeNames):
            PropFormatter.PropertyValue(str(PropNames[i]), "Constant", str(Lakes[rng][Lakes.index==lake][0]), "")
        
        PropFormatter.PrintCell("")
        
    PropFormatter.PrintCell("")
    
def FormatFish(PropFormatter, Fish):
    
    FishNames = Fish["Aquatic Biota (Consuming Organism)"].tolist()
    FishFoods = ["FractionDietAlgae",	
                 "FractionDietMacrophyte", 
                 "FractionDietZooplankton"	, 
                 "FractionDietBenthicInvertebrate", 
                 "FractionDietFishHerbivore", 
                 "FractionDietFishBenthicOmnivore", 
                 "FractionDietFishOmnivore", 
                 "FractionDietFishBenthicCarnivore", 
                 "FractionDietFishCarnivore"]
    FishLakeColumn = Fish.index.tolist()
    FishLocationColumn = Fish.Location.tolist()
    FishBiomassColumn = Fish["Biomass(kg ww/m2)"].tolist()
    FishBWColumn = Fish["Single Organism Body Weight(kg)"].tolist()
    FishBWColumn = Fish["Single Organism Body Weight(kg)"].replace(np.nan, 0, regex=True).tolist()

    PropFormatter.Divider("Fish food web(s)", True)
    PropFormatter.PrintCell("")
    PropFormatter.PrintCell("")
    
    for i, fish in enumerate(FishNames):
        lake = FishLakeColumn[i]
        location = FishLocationColumn[i]
        
        PropFormatter.PrintLine(str("Compartment: " + fish + " in " + location + "_" + lake))
        
        PropFormatter.PropertyValue("BiomassPerArea_kg_m2", "Constant", str(FishBiomassColumn[i]), "")
        
        if FishBWColumn[i] > 0:
            PropFormatter.PropertyValue("BW", "Constant", str(FishBWColumn[i]), "")
        
        for p, rng in enumerate(FishFoods):
            PropFormatter.PropertyValue(rng, "Constant", str(1*float(Fish.iloc[i,p+3])), "")
        PropFormatter.PrintCell("")
   

def FormatSurfaceSoil(PropFormatter, Soil):
    LandParcelNames = list(Soil)
    
    RangeNames = ["SSAir content",
                    "SSAverage vertical velocity of water (percolation)",
                    "SSBoundary layer thickness above surface soil",
                    "SSDensity of soil solids (dry weight)",
                    "SSFraction of area available for erosion",
                    "SSFraction of area available for runoff",
                    "SSFraction of area availabe for vertical diffusion",
                    "SSFraction Sand",
                    "SSOrganic carbon fraction",
                    "SSpH",
                    "SSTotal runoff rate",
                    "SSTotal erosion rate",
                    "SSWater content"]
    
    PropNames = ["VolumeFraction_vapor",
                      "AverageVerticalVelocity",
                      "AirSoilBoundaryThickness",
                      "rho",
                      "Fractionofareaavailableforerosion",
                      "FractionofAreaAvailableforRunoff",
                      "Fractionofareaavailableforverticaldiffusion",
                      "FractionSand",
                      "OrganicCarbonContent",
                      "pH",
                      "TotalRunoffRate_m3_m2_day",
                      "TotalErosionRate_kg_m2_day",
                      "VolumeFraction_liquid"]

    PropFormatter.Divider("Surface soil properties", True)
    PropFormatter.PrintCell("")
    
    for i, LandParcel in enumerate(LandParcelNames):
        PropFormatter.PrintLine(str("Compartment: " + "Soil - Surface in SurfSoil_" + LandParcel))
        
        for p, rng in enumerate(RangeNames):
            PropFormatter.PropertyValue(PropNames[p], "Constant", str(float(Soil.iloc[p,i])), "")
        PropFormatter.PrintCell("")        
    PropFormatter.PrintCell("")        
    
def FormatRootSoil(PropFormatter, Soil):
    
    LandParcelNames = list(Soil)
    
    RangeNames = ["RZAir content",
                    "RZAverage vertical velocity of water (percolation)",
                    "RZDensity of soil solids (dry weight)",
                    "RZFraction Sand",
                    "RZOrganic carbon fraction",
                    "RZpH",
                    "RZWater content",]
    
    PropNames = ["VolumeFraction_vapor",
                      "AverageVerticalVelocity",
                      "rho",
                      "FractionSand",
                      "OrganicCarbonContent",
                      "pH",
                      "VolumeFraction_liquid"]
    
    PropFormatter.Divider("Root soil properties", True)
    PropFormatter.PrintCell("")
    
    for i, LandParcel in enumerate(LandParcelNames):
        PropFormatter.PrintLine(str("Compartment: Soil - Root Zone in RootSoil_" + LandParcel))
        
        for p, rng in enumerate(RangeNames):
            PropFormatter.PropertyValue(PropNames[p], "Constant", str(float(Soil.iloc[13+p,i])), "")
        PropFormatter.PrintCell("")
    PropFormatter.PrintCell("")

def FormatVadoseSoil(PropFormatter, Soil):
    
    LandParcelNames = list(Soil)
    
    RangeNames = ["VZAir content",
                    "VZAverage vertical velocity of water (percolation)",
                    "VZDensity of soil solids (dry weight)",
                    "VZFraction Sand",
                    "VZOrganic carbon fraction",
                    "VZpH",
                    "VZWater content"]
    
    PropNames = ["VolumeFraction_vapor",
                      "AverageVerticalVelocity",
                      "rho",
                      "FractionSand",
                      "OrganicCarbonContent",
                      "pH",
                      "VolumeFraction_liquid"]
    
    PropFormatter.Divider("Vadose soil properties", True)
    PropFormatter.PrintCell("")
    
    for i, LandParcel in enumerate(LandParcelNames):
        PropFormatter.PrintLine(str("Compartment: Soil - Vadose Zone in VadoseSoil_" + LandParcel))
        
        for p, rng in enumerate(RangeNames):
            PropFormatter.PropertyValue(PropNames[p], "Constant", str(float(Soil.iloc[20+p,i])), "")
        PropFormatter.PrintCell("")
    PropFormatter.PrintCell("")

def FormatGroundwater(PropFormatter, Soil):
        
    LandParcelNames = list(Soil)
    
    RangeNames = ["GWFraction Sand",
                    "GWOrganic carbon fraction",
                    "GWpH",
                    "GWPorosity",
                    "GWDensity of Solid material in aquifer"]
    
    PropNames = ["FractionSand",
                      "OrganicCarbonContent",
                      "pH",
                      "Porosity",
                      "rho"]
    
    PropFormatter.Divider("Groundwater properties", True)
    PropFormatter.PrintCell("")
    
    for i, LandParcel in enumerate(LandParcelNames):
        PropFormatter.PrintLine(str("Compartment: Groundwater in GW_" + LandParcel))
        
        for p, rng in enumerate(RangeNames):
            PropFormatter.PropertyValue(PropNames[p], "Constant", str(float(Soil.iloc[27+p,i])), "")
        PropFormatter.PrintCell("")
    #PropFormatter.PrintCell("")

def FormatGlobals(PropFormatter, Parcels, ScenarioName, Parameters, Land_ErosionParameters, Fish):
    #scope filters match which keywords each property should go with
    Scopes = Parameters.index.tolist()
    NameColumn = 0#Parameters["TRIM property name"].tolist()
    FormColumn = 1#Parameters["TRIM property form"].tolist()
    ValueColumn = 2#Parameters["Formatted value"].tolist()
    SourceColumn = 3#Parameters["Description/Source"].tolist()
    
    Keywords = []
    PreviousScope = ""
    PrintProperty = False
    #'build array of keywords to check against scope filters.
    
    LandUses = Land_ErosionParameters.index.tolist()[2:]
    PlantTypes = Land_ErosionParameters["Plant type"].tolist()[2:]
    CompositePlantComps = {"Grasses/Herbs":["Leaf - Grasses/Herbs",
                                            "Leaf Particle - Grasses/Herbs",
                                            "Root - Grasses/Herbs",
                                            "Stem - Grasses/Herbs"],
                       "Coniferous Forest":["Leaf - Coniferous Forest",
                                            "Leaf Particle - Coniferous Forest"],
                        "Deciduous Forest":["Leaf - Deciduous Forest",
                                            "Leaf Particle - Deciduous Forest"],
                   "Agriculture - General":["Leaf - Agriculture - General",
                                            "Leaf Particle - Agriculture - General",
                                            "Root - Agriculture - General",
                                            "Stem - Agriculture - General",]
                           }
    FishNames = Fish["Aquatic Biota (Consuming Organism)"].tolist()
    LakeNames = Fish.index.tolist()
    Locations = Fish.Location.tolist()
    
    Keywords.append(str("Scenario: " + ScenarioName))
    
    for parcel in Parcels.All():
        for V in parcel.VolumeElements():
            Keywords.append(str("VolumeElement: " + V))
        
        for V in parcel.Compartments(LandUses, PlantTypes, CompositePlantComps, FishNames, LakeNames, Locations):
            Keywords.append(str("Compartment: " + V))
            
    for i, scope in enumerate(Scopes):
        #ipdb.set_trace()
        #print(scope)
        if str(scope)=="nan":
            continue
        if scope != PreviousScope:
            PrintProperty = False
            
            for V in Keywords:
                Keyword = V
                #print(V)
                #print(str(str(Keyword) + " " + str(scope)))
                if re.search((scope.strip().lower()).replace("*",".*"), Keyword.strip().lower()):
                    if not PrintProperty:
                        PropFormatter.PrintCell("")
                        PropFormatter.Divider(str("Parameters for " + PropFormatter._Quoted(scope)), True)
                        PrintProperty = True
                    PropFormatter.PrintLine(str(Keyword))
            PreviousScope = scope
        
        if PrintProperty:
            #this scope matched at least one keyword, or is continuing from before
            rng = Parameters.iloc[i, NameColumn]
            if str(rng) =="":
                continue
            PropFormatter.PrintLine(str("Property: " + rng))
            
            #check value type for InputFromFile/Constant/Formula
            rng = Parameters.iloc[i, FormColumn]
            if not str(rng) == "":
                PropFormatter.PrintLine(str("Form: " + rng))

            rng = Parameters.iloc[i, ValueColumn]
            if not str(rng) == "":
                PropFormatter.PrintLine(str("Value: " + rng))
            
            rng = Parameters.iloc[i, SourceColumn]
            if not str(rng) == "":
                #ipdb.set_trace()
                PropFormatter.PrintLine(str("Description: [[ " + str(rng) + " ]]"), True)
    PropFormatter.PrintCell("")
    PropFormatter.PrintCell("")
                
def FormatLinks(PropFormatter, Parcels, Watersheds):
                
    SendingParcels = Watersheds.index.tolist()
    ReceivingParcels = list(Watersheds)[5:]
    LandParcels = [p.Name for p in Parcels.LandParcels.All()]
    SinkColumn = 4
    
    PropFormatter.Divider("Watershed links", True)
    PropFormatter.PrintCell("")
    
    for s, sender in enumerate(SendingParcels):
        #check if sender is land
        if sender in LandParcels:
            PropFormatter.PrintLine(str("Originating from " + sender), True)
            PropFormatter.PrintCell("")
            PropFormatter.PrintLine(str("NewLink:"))
            PropFormatter.PrintLine(str("SendingCompartment: Soil - Surface in Surfsoil_" + sender))
            PropFormatter.PrintLine(str("ReceivingCompartment: Soil Advection Sink in SurfSoil_" + sender))
            PropFormatter.PrintLine(str("Algorithm: Erosion from Surface Soil to Soil Advection Sink"))
            PropFormatter.PrintLine(str("Algorithm: Runoff from Surface Soil to Soil Advection Sink"))
            PropFormatter.PrintCell("")
            
            #'specify erosion/runoff fractions
            rng = Watersheds.iloc[s, SinkColumn]
            FormatLinkFraction(PropFormatter, str("Soil - Surface in Surfsoil_"+sender), str("Soil Advection Sink in SurfSoil_"+sender), rng)
            
            for r, receiver in enumerate(ReceivingParcels):
                rng = Watersheds.iloc[s, 5+r]
                
                #ipdb.set_trace()
                #'If True Then 'TODO: clean this up. still deciding between all and all non-zero
                if rng > 0 :
                    PropFormatter.PrintLine(str("NewLink:"))
                    send = str("Soil - Surface in Surfsoil_"+sender)
                    PropFormatter.PrintLine(str("SendingCompartment: " + send))
                    
                    if receiver in LandParcels:
                        #'land parcel receiver
                        receive = str("Soil - Surface in SurfSoil_"+receiver)
                        PropFormatter.PrintLine(str("ReceivingCompartment: " + receive))
                        PropFormatter.PrintLine(str("Algorithm: Erosion from Surface Soil to Surface Soil, General(AlgInstID_2460)"))
                        PropFormatter.PrintLine(str("Algorithm: Runoff from Surface Soil to Surface Soil, General(AlgInstID_2465)"))
                    else:
                        #'surface water parcel receiver
                        receive = str("Surface water in SW_"+receiver)
                        PropFormatter.PrintLine(str("ReceivingCompartment: " + receive))
                        PropFormatter.PrintLine(str("Algorithm: Erosion from Surface Soil to Surface Water, General(AlgInstID_3515)"))
                        PropFormatter.PrintLine(str("Algorithm: Runoff from Surface Soil to Surface Water, General(AlgInstID_3520)"))
                    
                    PropFormatter.PrintCell("")
                    FormatLinkFraction(PropFormatter, send, receive, rng)
        PropFormatter.PrintCell("")


def FormatLinkFraction(PropFormatter, SendingCompartment, ReceivingCompartment, Fraction):
    
    PropFormatter.PrintLine(str("Link: " + SendingCompartment + " to " + ReceivingCompartment))
    PropFormatter.PropertyValue("FractionOfTotalErosion", "Constant", str(1*Fraction), "")
    PropFormatter.PropertyValue("FractionOfTotalRunoff", "Constant", str(1*Fraction), "")
    PropFormatter.PropertyValue("Enabled", "Constant", str(True) if Fraction > 0 else str(False), "")
    PropFormatter.PrintCell("")
    
def asdf(Parcels, Land_ErosionParameters, Fish):
#debugging    
    LandUses = Land_ErosionParameters.index.tolist()[2:]
    PlantTypes = Land_ErosionParameters["Plant type"].tolist()[2:]
    CompositePlantComps = {"Grasses/Herbs":["Leaf - Grasses/Herbs",
                                            "Leaf Particle - Grasses/Herbs",
                                            "Root - Grasses/Herbs",
                                            "Stem - Grasses/Herbs"],
                       "Coniferous Forest":["Leaf - Coniferous Forest",
                                            "Leaf Particle - Coniferous Forest"],
                        "Deciduous Forest":["Leaf - Deciduous Forest",
                                            "Leaf Particle - Deciduous Forest"],
                   "Agriculture - General":["Leaf - Agriculture - General",
                                            "Leaf Particle - Agriculture - General",
                                            "Root - Agriculture - General",
                                            "Stem - Agriculture - General",]
                           }
    FishNames = Fish["Aquatic Biota (Consuming Organism)"].tolist()
    LakeNames = Fish.index.tolist()
    Locations = Fish.Location.tolist()        
    
    for parcel in Parcels.All():
        print(str("Volume Elements in " + parcel.Name + ": "))
        for elmt in parcel.VolumeElements:
            print(str(" " + elmt))
        print(str("Compartments in " + parcel.Name + ": "))
        for elmt in parcel.Compartments(LandUses, PlantTypes, CompositePlantComps, FishNames, LakeNames, Locations):
            print(str(" " + elmt))
            
            
if __name__ == "__main__":
        GenerateProperties(str(Out+"Properties.txt"), "Foundries_SS", "Site-specific scenario for Int Iron Steel Foundries in Wexford County, MI", Parcels, Parameters, Land_SedDeliv, Lakes, Fish, Soil, Land_ErosionParameters, Watersheds)

