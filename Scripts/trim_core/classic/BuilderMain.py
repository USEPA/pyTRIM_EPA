# -*- coding: utf-8 -*-
import numpy as np
import pandas as pd
import sys
import os

from .Classes.Parcel import Parcel
from .Classes.ParcelCollection import ParcelCollection
from .Classes.OutputFormatter import OutputFormatter
from .HelperFunctions.Layout import LoadParcels, CountPoints, ComputeEnclosedArea, ComputeCentroidX, ComputeCentroidY
from .OutputFileGenerators.GenerateSources import GenerateSources
from .OutputFileGenerators.GenerateVolumeElements import GenerateVolumeElements
from .OutputFileGenerators.GenerateCompartments import GenerateCompartments
from .OutputFileGenerators.GenerateProperties import GenerateProperties

def BuilderMain(PA, LP, LC, LE, PL, US, LCO, LEP, LSDC, LSD, SO, WA, LA, FI, Out):
    """
    main function
    """
    #read in inputs from tables (or GUI)
    
            
    
    Parameters = pd.read_csv(PA, index_col=0)
    Parameters = Parameters.replace(np.nan, "", regex=True)
    #Parameters = Parameters.replace(" " , "", regex=True)
    #Parameters = Parameters.replace("  ", "", regex=True)
    
    Layout_Parceldf = pd.read_csv(LP, index_col=0)
    Layout_Coordinatesdf = pd.read_csv(LC, index_col=0,dtype={'X':float, 'Y':float})
    Layout_EmissionSources = pd.read_csv(LE,index_col=0)
    Layout_EmissionSources = Layout_EmissionSources.transpose()
    Layout_Sources = Layout_EmissionSources.Location.tolist()
    Sources = [True if p in Layout_Sources else False for p in Layout_Parceldf.index.tolist()]
    #load parcels here
    Parcels = LoadParcels(Layout_Parceldf.index.tolist(), Layout_Parceldf.ParcelCategory.tolist(), Layout_Parceldf.LandUse.tolist(),Sources)
    #data.apply(lambda x: result.Add(x["Name"],x["Category"],x["Source"]),axis=1) #read in data into parcel collection
    
    Plants = pd.read_csv(PL,index_col=0)
    
    Plants = Plants.transpose()
    
    USLECalcs = pd.read_csv(US,index_col=0)
    
    Land_Constants = pd.read_csv(LCO,index_col=0)
    Land_ErosionParameters = pd.read_csv(LEP,index_col=0)
    Land_ErosionParameters = Land_ErosionParameters.transpose()
    Land_SedDelivCoeff = pd.read_csv(LSDC,index_col=0)
    Land_SedDeliv = pd.read_csv(LSD,index_col=0)
    
    Soil = pd.read_csv(SO,index_col=0)
    
    Watersheds = pd.read_csv(WA,index_col=0)
    
    Lakes = pd.read_csv(LA,index_col=0)
    Lakes = Lakes.transpose()
    
    Fish = pd.read_csv(FI,index_col=0)
    
    #calculate parameters
    Layout_Parceldf["NumPoints"] = Layout_Parceldf["Points"].map(CountPoints)
    Layout_Parceldf["Area_m2"] = Layout_Parceldf.apply(lambda x: ComputeEnclosedArea(x["Points"], Layout_Coordinatesdf), axis=1)
    Layout_Parceldf["Area_km2"] = Layout_Parceldf["Area_m2"]/1000000
    Layout_Parceldf["Area_hectares"] = Layout_Parceldf["Area_m2"]/10000
    Layout_Parceldf["Area_acres"] = Layout_Parceldf["Area_m2"]/4046.85642
    Layout_Parceldf["side_if_sq_m2"] = (Layout_Parceldf["Area_m2"])**0.5
    
    #for each emissions source, assert that the Parcel IsSource before below
    Layout_EmissionSources["X coordinate"] = Layout_EmissionSources.apply(lambda x: ComputeCentroidX(x["Location"], Layout_Parceldf, Layout_Coordinatesdf), axis=1)
    Layout_EmissionSources["Y coordinate"] = Layout_EmissionSources.apply(lambda x: ComputeCentroidY(x["Location"], Layout_Parceldf, Layout_Coordinatesdf), axis=1)
    
    #Set uniform offset
    #should these be the avg? currently these variables are assigned to the x/y centroids of just one source if there are multiple sources.
    layout_offset_E = Layout_EmissionSources["X coordinate"][0]
    layout_offset_N = Layout_EmissionSources["Y coordinate"][0]
    
    Layout_Coordinatesdf["Base X"] = Layout_Coordinatesdf["X"]-layout_offset_E
    Layout_Coordinatesdf["Base Y"] = Layout_Coordinatesdf["Y"]-layout_offset_N

    #Generate files
    GenerateSources(str(Out+"Sources.txt"), "Foundries_SS", "Testing", Layout_EmissionSources)
    GenerateVolumeElements(str(Out+"VolumeElements.txt"), "Foundries", "Testing", Parcels, Layout_Parceldf, Layout_Coordinatesdf, Parameters, Lakes, Land_ErosionParameters)
    GenerateCompartments(str(Out+"Compartment.txt"), "Foundries", "Testing", Parcels, Fish, Land_ErosionParameters)        
    GenerateProperties(str(Out+"Properties.txt"), "Foundries_SS", "Site-specific scenario for Int Iron Steel Foundries in Wexford County, MI", Parcels, Parameters, Land_SedDeliv, Lakes, Fish, Soil, Land_ErosionParameters, Watersheds)
