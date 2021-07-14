# -*- coding: utf-8 -*-

#create the volume elements library import file.

from ..Classes.OutputFormatter import OutputFormatter
from ..Classes.Parcel import Parcel
import datetime

def GenerateVolumeElements(FileName, ScenarioName, ScenarioDescription, Parcels, Layout_Parceldf, Layout_Coordinatesdf, Parameters, Lakes, Land_ErosionParameters):
    
    Coordinate_sys = "UTM Zone 16N, WGS1984 Ellipsoid"
    Points = Layout_Coordinatesdf.index.tolist()
    XCol = Layout_Coordinatesdf.X.tolist()
    YCol = Layout_Coordinatesdf.Y.tolist()
    
    VEFormatter = OutputFormatter(FileName)
    VEFormatter.PrintLine("TRIM.FaTE scenario spatial layout", True)
    VEFormatter.PrintLine("Volume elements and primary abiotic compartments", True)  
    VEFormatter.PrintCell("")
    VEFormatter.PrintLine(ScenarioName, True)
    VEFormatter.PrintLine(ScenarioDescription, True)
    VEFormatter.PrintCell("")
    VEFormatter.LinePrint("Generated:", str(datetime.datetime.now()), True)
    VEFormatter.LinePrint("Coordinates:", Coordinate_sys, True)
    VEFormatter.PrintCell("")
    VEFormatter.PrintLine("start_volume_element_file")  
    VEFormatter.PrintLine("version 1")
    VEFormatter.PrintCell("")
    VEFormatter.PrintLine("start_points")  
    VEFormatter.PrintLine("PointID x y", True)  
    
    for i, point in enumerate(Points):
        VEFormatter.PrintLine(str(str(point) + " " + str(XCol[i]) + " " + str(YCol[i])))

    VEFormatter.PrintLine("end_points")  
    VEFormatter.PrintCell("")

    VEFormatter.PrintLine("start_parcels")  
    VEFormatter.PrintLine("parcel_name, #points, pointIDs", True)  

    for parcel in Parcels.All():
        VEFormatter.PrintLine(str(str(parcel.Name) + " " + str(Layout_Parceldf.NumPoints[Layout_Parceldf.index==parcel.Name][0]) + " " + str(Layout_Parceldf.Points[Layout_Parceldf.index==parcel.Name][0])))
    
    VEFormatter.PrintLine("end_parcels")   
    VEFormatter.PrintCell("")

    VEFormatter.PrintLine("start_volume_elements")
    VEFormatter.PrintLine("name, parcel, primary abiotic, bottom, top", True)  
    VEFormatter.PrintCell("")
    
    VEFormatter.Divider("Air", True)
    #air height line == 800
    VEFormatter.PrintCell("")
    
    for parcel in Parcels.AirParcels.All():
        VEFormatter.PrintLine(str("Air_" + str(parcel.Name) + " " + str(parcel.Name) + " " + VEFormatter._Quoted("Air") + " " + "0" + " " + str(Parameters["Formatted value"][Parameters["TRIM property name"]=="air_height"][0])))

        if parcel.IsSource:
            VEFormatter.PrintLine(str("UpperAir_" + str(parcel.Name) + " " + str(parcel.Name) + " " + VEFormatter._Quoted("Air") + " " + str(Parameters["Formatted value"][Parameters["TRIM property name"]=="air_height"][0]) + " " + "10000" + " // source-containing parcel"))
    
    VEFormatter.PrintCell("")    
    VEFormatter.Divider("Water", True)
    VEFormatter.PrintCell("")
    
    for parcel in Parcels.WaterParcels.All():
        CD = Lakes["SP_Computed depth (m)"][Lakes.index==parcel.Name][0]
        SD = Lakes["SP_Sediment depth (m)"][Lakes.index==parcel.Name][0]
        VEFormatter.PrintLine(str("SW_" + str(parcel.Name) + " " + str(parcel.Name) + " " + VEFormatter._Quoted("Surface water") + " " + str(0-CD) + " " + "0"))
        VEFormatter.PrintLine(str("Sed_" + str(parcel.Name) + " " + str(parcel.Name) + " " + VEFormatter._Quoted("Sediment") + " " + str(-CD-SD) + " " + str(-CD)))
        
    VEFormatter.PrintCell("")
    VEFormatter.Divider("Land", True)
    VEFormatter.PrintCell("")
    VEFormatter.PrintCell("")

    for parcel in Parcels.LandParcels.All():
        SST = float(Land_ErosionParameters["Surface soil thickness"][Land_ErosionParameters.index==parcel.LandUse][0])
        RST = float(Land_ErosionParameters["Root soil thickness"][Land_ErosionParameters.index==parcel.LandUse][0]) 
        VST = float(Land_ErosionParameters["Vadose soil thickness"][Land_ErosionParameters.index==parcel.LandUse][0])
        GWT = float(Land_ErosionParameters["Groundwater thickness"][Land_ErosionParameters.index==parcel.LandUse][0])

        VEFormatter.PrintLine(str("Parcel: " + str(parcel.Name) + " // Land use: " + str(parcel.LandUse)), True)
        VEFormatter.PrintLine(str("SurfSoil_" + str(parcel.Name) + " " + str(parcel.Name) + " " + VEFormatter._Quoted("Soil - Surface") + " " + str(0-SST) + " " + "0"))
        VEFormatter.PrintLine(str("RootSoil_" + str(parcel.Name) + " " + str(parcel.Name) + " " + VEFormatter._Quoted("Soil - Root Zone") + " " + str(-SST-RST) + " " + str(0-SST)))
        VEFormatter.PrintLine(str("VadoseSoil_" + str(parcel.Name) + " " + str(parcel.Name) + " " + VEFormatter._Quoted("Soil - Vadose Zone") + " " + str(-SST-RST-VST) + " " + str(-SST-RST)))
        VEFormatter.PrintLine(str("GW_" + str(parcel.Name) + " " + str(parcel.Name) + " " + VEFormatter._Quoted("Groundwater") + " " + str(-SST-RST-VST-GWT) + " " + str(-SST-RST-VST)))
        VEFormatter.PrintCell("")
        
    VEFormatter.PrintLine("end_volume_elements")
    VEFormatter.PrintCell("")
    VEFormatter.PrintLine("end_volume_element_file")
        

        
if __name__ == "__main__":
    GenerateVolumeElements(str(Out+"VolumeElements.txt"), "Foundries", "Testing", Parcels, Layout_Parceldf, Layout_Coordinatesdf, Parameters, Lakes, Land_ErosionParameters)
