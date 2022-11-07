### note: this is an auto generated script

from constants import *
from define_scenario import *
from define_ve import *
from define_pve import *
from define_chem_classes import *
from define_comp_classes import *
from define_attributes_props import *

def define_comp(currentchemical):

    
	comp_objects_dict={}
	
	air_in_air_source=air(constants,containingscenario,currentchemical,air_source,comp_objects_dict)
	air_in_air_source.name="air_in_air_source"
	air_in_air_source.containingvolumeelementname="air_source"
	air_in_air_source.parcel_name="source"
	air_in_air_source.parcel_points="p1 p2 p3 p4 p5"
	air_in_air_source.parcel_area=62500.0
	air_in_air_source.exterior_boundary=750.0
	
	comp_objects_dict["air_in_air_source"]=air_in_air_source

	air_in_upperair_source=air(constants,containingscenario,currentchemical,upperair_source,comp_objects_dict)
	air_in_upperair_source.name="air_in_upperair_source"
	air_in_upperair_source.containingvolumeelementname="upperair_source"
	air_in_upperair_source.parcel_name="source"
	air_in_upperair_source.parcel_points="p1 p2 p3 p4 p5"
	air_in_upperair_source.parcel_area=62500.0
	air_in_upperair_source.exterior_boundary=750.0
	
	comp_objects_dict["air_in_upperair_source"]=air_in_upperair_source

	air_in_air_n1=air(constants,containingscenario,currentchemical,air_n1,comp_objects_dict)
	air_in_air_n1.name="air_in_air_n1"
	air_in_air_n1.containingvolumeelementname="air_n1"
	air_in_air_n1.parcel_name="n1"
	air_in_air_n1.parcel_points="p5 p4 p7 p6"
	air_in_air_n1.parcel_area=58445.624999993015
	air_in_air_n1.exterior_boundary=380.0435818429189
	
	comp_objects_dict["air_in_air_n1"]=air_in_air_n1

	air_in_air_n6=air(constants,containingscenario,currentchemical,air_n6,comp_objects_dict)
	air_in_air_n6.name="air_in_air_n6"
	air_in_air_n6.containingvolumeelementname="air_n6"
	air_in_air_n6.parcel_name="n6"
	air_in_air_n6.parcel_points="p6 p7 p26 p25"
	air_in_air_n6.parcel_area=40633.00000000745
	air_in_air_n6.exterior_boundary=202.6895855736298
	
	comp_objects_dict["air_in_air_n6"]=air_in_air_n6

	air_in_air_n7=air(constants,containingscenario,currentchemical,air_n7,comp_objects_dict)
	air_in_air_n7.name="air_in_air_n7"
	air_in_air_n7.containingvolumeelementname="air_n7"
	air_in_air_n7.parcel_name="n7"
	air_in_air_n7.parcel_points="p25 p26 p10 p9"
	air_in_air_n7.parcel_area=73291.50000005029
	air_in_air_n7.exterior_boundary=304.035190232991
	
	comp_objects_dict["air_in_air_n7"]=air_in_air_n7

	air_in_air_n3=air(constants,containingscenario,currentchemical,air_n3,comp_objects_dict)
	air_in_air_n3.name="air_in_air_n3"
	air_in_air_n3.containingvolumeelementname="air_n3"
	air_in_air_n3.parcel_name="n3"
	air_in_air_n3.parcel_points="p9 p10 p14 p13"
	air_in_air_n3.parcel_area=351265.0000001304
	air_in_air_n3.exterior_boundary=1013.4479278679979
	
	comp_objects_dict["air_in_air_n3"]=air_in_air_n3

	air_in_air_n4=air(constants,containingscenario,currentchemical,air_n4,comp_objects_dict)
	air_in_air_n4.name="air_in_air_n4"
	air_in_air_n4.containingvolumeelementname="air_n4"
	air_in_air_n4.parcel_name="n4"
	air_in_air_n4.parcel_points="p13 p14 p18 p17"
	air_in_air_n4.parcel_area=2041139.9999996647
	air_in_air_n4.exterior_boundary=3040.3486547433513
	
	comp_objects_dict["air_in_air_n4"]=air_in_air_n4

	air_in_air_n5=air(constants,containingscenario,currentchemical,air_n5,comp_objects_dict)
	air_in_air_n5.name="air_in_air_n5"
	air_in_air_n5.containingvolumeelementname="air_n5"
	air_in_air_n5.parcel_name="n5"
	air_in_air_n5.parcel_points="p17 p18 p22 p21"
	air_in_air_n5.parcel_area=6693049.999999348
	air_in_air_n5.exterior_boundary=6817.244510421856
	
	comp_objects_dict["air_in_air_n5"]=air_in_air_n5

	air_in_air_s1=air(constants,containingscenario,currentchemical,air_s1,comp_objects_dict)
	air_in_air_s1.name="air_in_air_s1"
	air_in_air_s1.containingvolumeelementname="air_s1"
	air_in_air_s1.parcel_name="s1"
	air_in_air_s1.parcel_points="p4 p3 p8 p7"
	air_in_air_s1.parcel_area=58445.624999993015
	air_in_air_s1.exterior_boundary=380.0435818429189
	
	comp_objects_dict["air_in_air_s1"]=air_in_air_s1

	air_in_air_pond=air(constants,containingscenario,currentchemical,air_pond,comp_objects_dict)
	air_in_air_pond.name="air_in_air_pond"
	air_in_air_pond.containingvolumeelementname="air_pond"
	air_in_air_pond.parcel_name="pond"
	air_in_air_pond.parcel_points="p7 p8 p16 p14"
	air_in_air_pond.parcel_area=465187.5
	air_in_air_pond.exterior_boundary=1520.1727036425948
	
	comp_objects_dict["air_in_air_pond"]=air_in_air_pond

	air_in_air_s4=air(constants,containingscenario,currentchemical,air_s4,comp_objects_dict)
	air_in_air_s4.name="air_in_air_s4"
	air_in_air_s4.containingvolumeelementname="air_s4"
	air_in_air_s4.parcel_name="s4"
	air_in_air_s4.parcel_points="p14 p16 p20 p18"
	air_in_air_s4.parcel_area=2041139.9999996647
	air_in_air_s4.exterior_boundary=3040.3486547433513
	
	comp_objects_dict["air_in_air_s4"]=air_in_air_s4

	air_in_air_s5=air(constants,containingscenario,currentchemical,air_s5,comp_objects_dict)
	air_in_air_s5.name="air_in_air_s5"
	air_in_air_s5.containingvolumeelementname="air_s5"
	air_in_air_s5.parcel_name="s5"
	air_in_air_s5.parcel_points="p18 p20 p24 p22"
	air_in_air_s5.parcel_area=6693049.999999348
	air_in_air_s5.exterior_boundary=6817.244510421856
	
	comp_objects_dict["air_in_air_s5"]=air_in_air_s5

	surface_water_in_sw_pond=surface_water(constants,containingscenario,currentchemical,sw_pond,comp_objects_dict)
	surface_water_in_sw_pond.name="surface_water_in_sw_pond"
	surface_water_in_sw_pond.containingvolumeelementname="sw_pond"
	surface_water_in_sw_pond.parcel_name="pond"
	surface_water_in_sw_pond.parcel_points="p7 p8 p16 p14"
	surface_water_in_sw_pond.parcel_area=465187.5
	surface_water_in_sw_pond.exterior_boundary=1520.1727036425948
	
	comp_objects_dict["surface_water_in_sw_pond"]=surface_water_in_sw_pond

	sediment_in_sed_pond=sediment(constants,containingscenario,currentchemical,sed_pond,comp_objects_dict)
	sediment_in_sed_pond.name="sediment_in_sed_pond"
	sediment_in_sed_pond.containingvolumeelementname="sed_pond"
	sediment_in_sed_pond.parcel_name="pond"
	sediment_in_sed_pond.parcel_points="p7 p8 p16 p14"
	sediment_in_sed_pond.parcel_area=465187.5
	sediment_in_sed_pond.exterior_boundary=1520.1727036425948
	
	comp_objects_dict["sediment_in_sed_pond"]=sediment_in_sed_pond

	soil_surface_in_surfsoil_source=soil_surface(constants,containingscenario,currentchemical,surfsoil_source,comp_objects_dict)
	soil_surface_in_surfsoil_source.name="soil_surface_in_surfsoil_source"
	soil_surface_in_surfsoil_source.containingvolumeelementname="surfsoil_source"
	soil_surface_in_surfsoil_source.parcel_name="source"
	soil_surface_in_surfsoil_source.parcel_points="p1 p2 p3 p4 p5"
	soil_surface_in_surfsoil_source.parcel_area=62500.0
	soil_surface_in_surfsoil_source.exterior_boundary=750.0
	
	comp_objects_dict["soil_surface_in_surfsoil_source"]=soil_surface_in_surfsoil_source

	soil_root_zone_in_rootsoil_source=soil_root_zone(constants,containingscenario,currentchemical,rootsoil_source,comp_objects_dict)
	soil_root_zone_in_rootsoil_source.name="soil_root_zone_in_rootsoil_source"
	soil_root_zone_in_rootsoil_source.containingvolumeelementname="rootsoil_source"
	soil_root_zone_in_rootsoil_source.parcel_name="source"
	soil_root_zone_in_rootsoil_source.parcel_points="p1 p2 p3 p4 p5"
	soil_root_zone_in_rootsoil_source.parcel_area=62500.0
	soil_root_zone_in_rootsoil_source.exterior_boundary=750.0
	
	comp_objects_dict["soil_root_zone_in_rootsoil_source"]=soil_root_zone_in_rootsoil_source

	soil_vadose_zone_in_vadosesoil_source=soil_vadose_zone(constants,containingscenario,currentchemical,vadosesoil_source,comp_objects_dict)
	soil_vadose_zone_in_vadosesoil_source.name="soil_vadose_zone_in_vadosesoil_source"
	soil_vadose_zone_in_vadosesoil_source.containingvolumeelementname="vadosesoil_source"
	soil_vadose_zone_in_vadosesoil_source.parcel_name="source"
	soil_vadose_zone_in_vadosesoil_source.parcel_points="p1 p2 p3 p4 p5"
	soil_vadose_zone_in_vadosesoil_source.parcel_area=62500.0
	soil_vadose_zone_in_vadosesoil_source.exterior_boundary=750.0
	
	comp_objects_dict["soil_vadose_zone_in_vadosesoil_source"]=soil_vadose_zone_in_vadosesoil_source

	groundwater_in_gw_source=groundwater(constants,containingscenario,currentchemical,gw_source,comp_objects_dict)
	groundwater_in_gw_source.name="groundwater_in_gw_source"
	groundwater_in_gw_source.containingvolumeelementname="gw_source"
	groundwater_in_gw_source.parcel_name="source"
	groundwater_in_gw_source.parcel_points="p1 p2 p3 p4 p5"
	groundwater_in_gw_source.parcel_area=62500.0
	groundwater_in_gw_source.exterior_boundary=750.0
	
	comp_objects_dict["groundwater_in_gw_source"]=groundwater_in_gw_source

	soil_surface_in_surfsoil_n1=soil_surface(constants,containingscenario,currentchemical,surfsoil_n1,comp_objects_dict)
	soil_surface_in_surfsoil_n1.name="soil_surface_in_surfsoil_n1"
	soil_surface_in_surfsoil_n1.containingvolumeelementname="surfsoil_n1"
	soil_surface_in_surfsoil_n1.parcel_name="n1"
	soil_surface_in_surfsoil_n1.parcel_points="p5 p4 p7 p6"
	soil_surface_in_surfsoil_n1.parcel_area=58445.624999993015
	soil_surface_in_surfsoil_n1.exterior_boundary=380.0435818429189
	
	comp_objects_dict["soil_surface_in_surfsoil_n1"]=soil_surface_in_surfsoil_n1

	soil_root_zone_in_rootsoil_n1=soil_root_zone(constants,containingscenario,currentchemical,rootsoil_n1,comp_objects_dict)
	soil_root_zone_in_rootsoil_n1.name="soil_root_zone_in_rootsoil_n1"
	soil_root_zone_in_rootsoil_n1.containingvolumeelementname="rootsoil_n1"
	soil_root_zone_in_rootsoil_n1.parcel_name="n1"
	soil_root_zone_in_rootsoil_n1.parcel_points="p5 p4 p7 p6"
	soil_root_zone_in_rootsoil_n1.parcel_area=58445.624999993015
	soil_root_zone_in_rootsoil_n1.exterior_boundary=380.0435818429189
	
	comp_objects_dict["soil_root_zone_in_rootsoil_n1"]=soil_root_zone_in_rootsoil_n1

	soil_vadose_zone_in_vadosesoil_n1=soil_vadose_zone(constants,containingscenario,currentchemical,vadosesoil_n1,comp_objects_dict)
	soil_vadose_zone_in_vadosesoil_n1.name="soil_vadose_zone_in_vadosesoil_n1"
	soil_vadose_zone_in_vadosesoil_n1.containingvolumeelementname="vadosesoil_n1"
	soil_vadose_zone_in_vadosesoil_n1.parcel_name="n1"
	soil_vadose_zone_in_vadosesoil_n1.parcel_points="p5 p4 p7 p6"
	soil_vadose_zone_in_vadosesoil_n1.parcel_area=58445.624999993015
	soil_vadose_zone_in_vadosesoil_n1.exterior_boundary=380.0435818429189
	
	comp_objects_dict["soil_vadose_zone_in_vadosesoil_n1"]=soil_vadose_zone_in_vadosesoil_n1

	groundwater_in_gw_n1=groundwater(constants,containingscenario,currentchemical,gw_n1,comp_objects_dict)
	groundwater_in_gw_n1.name="groundwater_in_gw_n1"
	groundwater_in_gw_n1.containingvolumeelementname="gw_n1"
	groundwater_in_gw_n1.parcel_name="n1"
	groundwater_in_gw_n1.parcel_points="p5 p4 p7 p6"
	groundwater_in_gw_n1.parcel_area=58445.624999993015
	groundwater_in_gw_n1.exterior_boundary=380.0435818429189
	
	comp_objects_dict["groundwater_in_gw_n1"]=groundwater_in_gw_n1

	soil_surface_in_surfsoil_n6=soil_surface(constants,containingscenario,currentchemical,surfsoil_n6,comp_objects_dict)
	soil_surface_in_surfsoil_n6.name="soil_surface_in_surfsoil_n6"
	soil_surface_in_surfsoil_n6.containingvolumeelementname="surfsoil_n6"
	soil_surface_in_surfsoil_n6.parcel_name="n6"
	soil_surface_in_surfsoil_n6.parcel_points="p6 p7 p26 p25"
	soil_surface_in_surfsoil_n6.parcel_area=40633.00000000745
	soil_surface_in_surfsoil_n6.exterior_boundary=202.6895855736298
	
	comp_objects_dict["soil_surface_in_surfsoil_n6"]=soil_surface_in_surfsoil_n6

	soil_root_zone_in_rootsoil_n6=soil_root_zone(constants,containingscenario,currentchemical,rootsoil_n6,comp_objects_dict)
	soil_root_zone_in_rootsoil_n6.name="soil_root_zone_in_rootsoil_n6"
	soil_root_zone_in_rootsoil_n6.containingvolumeelementname="rootsoil_n6"
	soil_root_zone_in_rootsoil_n6.parcel_name="n6"
	soil_root_zone_in_rootsoil_n6.parcel_points="p6 p7 p26 p25"
	soil_root_zone_in_rootsoil_n6.parcel_area=40633.00000000745
	soil_root_zone_in_rootsoil_n6.exterior_boundary=202.6895855736298
	
	comp_objects_dict["soil_root_zone_in_rootsoil_n6"]=soil_root_zone_in_rootsoil_n6

	soil_vadose_zone_in_vadosesoil_n6=soil_vadose_zone(constants,containingscenario,currentchemical,vadosesoil_n6,comp_objects_dict)
	soil_vadose_zone_in_vadosesoil_n6.name="soil_vadose_zone_in_vadosesoil_n6"
	soil_vadose_zone_in_vadosesoil_n6.containingvolumeelementname="vadosesoil_n6"
	soil_vadose_zone_in_vadosesoil_n6.parcel_name="n6"
	soil_vadose_zone_in_vadosesoil_n6.parcel_points="p6 p7 p26 p25"
	soil_vadose_zone_in_vadosesoil_n6.parcel_area=40633.00000000745
	soil_vadose_zone_in_vadosesoil_n6.exterior_boundary=202.6895855736298
	
	comp_objects_dict["soil_vadose_zone_in_vadosesoil_n6"]=soil_vadose_zone_in_vadosesoil_n6

	groundwater_in_gw_n6=groundwater(constants,containingscenario,currentchemical,gw_n6,comp_objects_dict)
	groundwater_in_gw_n6.name="groundwater_in_gw_n6"
	groundwater_in_gw_n6.containingvolumeelementname="gw_n6"
	groundwater_in_gw_n6.parcel_name="n6"
	groundwater_in_gw_n6.parcel_points="p6 p7 p26 p25"
	groundwater_in_gw_n6.parcel_area=40633.00000000745
	groundwater_in_gw_n6.exterior_boundary=202.6895855736298
	
	comp_objects_dict["groundwater_in_gw_n6"]=groundwater_in_gw_n6

	soil_surface_in_surfsoil_n7=soil_surface(constants,containingscenario,currentchemical,surfsoil_n7,comp_objects_dict)
	soil_surface_in_surfsoil_n7.name="soil_surface_in_surfsoil_n7"
	soil_surface_in_surfsoil_n7.containingvolumeelementname="surfsoil_n7"
	soil_surface_in_surfsoil_n7.parcel_name="n7"
	soil_surface_in_surfsoil_n7.parcel_points="p25 p26 p10 p9"
	soil_surface_in_surfsoil_n7.parcel_area=73291.50000005029
	soil_surface_in_surfsoil_n7.exterior_boundary=304.035190232991
	
	comp_objects_dict["soil_surface_in_surfsoil_n7"]=soil_surface_in_surfsoil_n7

	soil_root_zone_in_rootsoil_n7=soil_root_zone(constants,containingscenario,currentchemical,rootsoil_n7,comp_objects_dict)
	soil_root_zone_in_rootsoil_n7.name="soil_root_zone_in_rootsoil_n7"
	soil_root_zone_in_rootsoil_n7.containingvolumeelementname="rootsoil_n7"
	soil_root_zone_in_rootsoil_n7.parcel_name="n7"
	soil_root_zone_in_rootsoil_n7.parcel_points="p25 p26 p10 p9"
	soil_root_zone_in_rootsoil_n7.parcel_area=73291.50000005029
	soil_root_zone_in_rootsoil_n7.exterior_boundary=304.035190232991
	
	comp_objects_dict["soil_root_zone_in_rootsoil_n7"]=soil_root_zone_in_rootsoil_n7

	soil_vadose_zone_in_vadosesoil_n7=soil_vadose_zone(constants,containingscenario,currentchemical,vadosesoil_n7,comp_objects_dict)
	soil_vadose_zone_in_vadosesoil_n7.name="soil_vadose_zone_in_vadosesoil_n7"
	soil_vadose_zone_in_vadosesoil_n7.containingvolumeelementname="vadosesoil_n7"
	soil_vadose_zone_in_vadosesoil_n7.parcel_name="n7"
	soil_vadose_zone_in_vadosesoil_n7.parcel_points="p25 p26 p10 p9"
	soil_vadose_zone_in_vadosesoil_n7.parcel_area=73291.50000005029
	soil_vadose_zone_in_vadosesoil_n7.exterior_boundary=304.035190232991
	
	comp_objects_dict["soil_vadose_zone_in_vadosesoil_n7"]=soil_vadose_zone_in_vadosesoil_n7

	groundwater_in_gw_n7=groundwater(constants,containingscenario,currentchemical,gw_n7,comp_objects_dict)
	groundwater_in_gw_n7.name="groundwater_in_gw_n7"
	groundwater_in_gw_n7.containingvolumeelementname="gw_n7"
	groundwater_in_gw_n7.parcel_name="n7"
	groundwater_in_gw_n7.parcel_points="p25 p26 p10 p9"
	groundwater_in_gw_n7.parcel_area=73291.50000005029
	groundwater_in_gw_n7.exterior_boundary=304.035190232991
	
	comp_objects_dict["groundwater_in_gw_n7"]=groundwater_in_gw_n7

	soil_surface_in_surfsoil_n3=soil_surface(constants,containingscenario,currentchemical,surfsoil_n3,comp_objects_dict)
	soil_surface_in_surfsoil_n3.name="soil_surface_in_surfsoil_n3"
	soil_surface_in_surfsoil_n3.containingvolumeelementname="surfsoil_n3"
	soil_surface_in_surfsoil_n3.parcel_name="n3"
	soil_surface_in_surfsoil_n3.parcel_points="p9 p10 p14 p13"
	soil_surface_in_surfsoil_n3.parcel_area=351265.0000001304
	soil_surface_in_surfsoil_n3.exterior_boundary=1013.4479278679979
	
	comp_objects_dict["soil_surface_in_surfsoil_n3"]=soil_surface_in_surfsoil_n3

	soil_root_zone_in_rootsoil_n3=soil_root_zone(constants,containingscenario,currentchemical,rootsoil_n3,comp_objects_dict)
	soil_root_zone_in_rootsoil_n3.name="soil_root_zone_in_rootsoil_n3"
	soil_root_zone_in_rootsoil_n3.containingvolumeelementname="rootsoil_n3"
	soil_root_zone_in_rootsoil_n3.parcel_name="n3"
	soil_root_zone_in_rootsoil_n3.parcel_points="p9 p10 p14 p13"
	soil_root_zone_in_rootsoil_n3.parcel_area=351265.0000001304
	soil_root_zone_in_rootsoil_n3.exterior_boundary=1013.4479278679979
	
	comp_objects_dict["soil_root_zone_in_rootsoil_n3"]=soil_root_zone_in_rootsoil_n3

	soil_vadose_zone_in_vadosesoil_n3=soil_vadose_zone(constants,containingscenario,currentchemical,vadosesoil_n3,comp_objects_dict)
	soil_vadose_zone_in_vadosesoil_n3.name="soil_vadose_zone_in_vadosesoil_n3"
	soil_vadose_zone_in_vadosesoil_n3.containingvolumeelementname="vadosesoil_n3"
	soil_vadose_zone_in_vadosesoil_n3.parcel_name="n3"
	soil_vadose_zone_in_vadosesoil_n3.parcel_points="p9 p10 p14 p13"
	soil_vadose_zone_in_vadosesoil_n3.parcel_area=351265.0000001304
	soil_vadose_zone_in_vadosesoil_n3.exterior_boundary=1013.4479278679979
	
	comp_objects_dict["soil_vadose_zone_in_vadosesoil_n3"]=soil_vadose_zone_in_vadosesoil_n3

	groundwater_in_gw_n3=groundwater(constants,containingscenario,currentchemical,gw_n3,comp_objects_dict)
	groundwater_in_gw_n3.name="groundwater_in_gw_n3"
	groundwater_in_gw_n3.containingvolumeelementname="gw_n3"
	groundwater_in_gw_n3.parcel_name="n3"
	groundwater_in_gw_n3.parcel_points="p9 p10 p14 p13"
	groundwater_in_gw_n3.parcel_area=351265.0000001304
	groundwater_in_gw_n3.exterior_boundary=1013.4479278679979
	
	comp_objects_dict["groundwater_in_gw_n3"]=groundwater_in_gw_n3

	soil_surface_in_surfsoil_n4=soil_surface(constants,containingscenario,currentchemical,surfsoil_n4,comp_objects_dict)
	soil_surface_in_surfsoil_n4.name="soil_surface_in_surfsoil_n4"
	soil_surface_in_surfsoil_n4.containingvolumeelementname="surfsoil_n4"
	soil_surface_in_surfsoil_n4.parcel_name="n4"
	soil_surface_in_surfsoil_n4.parcel_points="p13 p14 p18 p17"
	soil_surface_in_surfsoil_n4.parcel_area=2041139.9999996647
	soil_surface_in_surfsoil_n4.exterior_boundary=3040.3486547433513
	
	comp_objects_dict["soil_surface_in_surfsoil_n4"]=soil_surface_in_surfsoil_n4

	soil_root_zone_in_rootsoil_n4=soil_root_zone(constants,containingscenario,currentchemical,rootsoil_n4,comp_objects_dict)
	soil_root_zone_in_rootsoil_n4.name="soil_root_zone_in_rootsoil_n4"
	soil_root_zone_in_rootsoil_n4.containingvolumeelementname="rootsoil_n4"
	soil_root_zone_in_rootsoil_n4.parcel_name="n4"
	soil_root_zone_in_rootsoil_n4.parcel_points="p13 p14 p18 p17"
	soil_root_zone_in_rootsoil_n4.parcel_area=2041139.9999996647
	soil_root_zone_in_rootsoil_n4.exterior_boundary=3040.3486547433513
	
	comp_objects_dict["soil_root_zone_in_rootsoil_n4"]=soil_root_zone_in_rootsoil_n4

	soil_vadose_zone_in_vadosesoil_n4=soil_vadose_zone(constants,containingscenario,currentchemical,vadosesoil_n4,comp_objects_dict)
	soil_vadose_zone_in_vadosesoil_n4.name="soil_vadose_zone_in_vadosesoil_n4"
	soil_vadose_zone_in_vadosesoil_n4.containingvolumeelementname="vadosesoil_n4"
	soil_vadose_zone_in_vadosesoil_n4.parcel_name="n4"
	soil_vadose_zone_in_vadosesoil_n4.parcel_points="p13 p14 p18 p17"
	soil_vadose_zone_in_vadosesoil_n4.parcel_area=2041139.9999996647
	soil_vadose_zone_in_vadosesoil_n4.exterior_boundary=3040.3486547433513
	
	comp_objects_dict["soil_vadose_zone_in_vadosesoil_n4"]=soil_vadose_zone_in_vadosesoil_n4

	groundwater_in_gw_n4=groundwater(constants,containingscenario,currentchemical,gw_n4,comp_objects_dict)
	groundwater_in_gw_n4.name="groundwater_in_gw_n4"
	groundwater_in_gw_n4.containingvolumeelementname="gw_n4"
	groundwater_in_gw_n4.parcel_name="n4"
	groundwater_in_gw_n4.parcel_points="p13 p14 p18 p17"
	groundwater_in_gw_n4.parcel_area=2041139.9999996647
	groundwater_in_gw_n4.exterior_boundary=3040.3486547433513
	
	comp_objects_dict["groundwater_in_gw_n4"]=groundwater_in_gw_n4

	soil_surface_in_surfsoil_n5=soil_surface(constants,containingscenario,currentchemical,surfsoil_n5,comp_objects_dict)
	soil_surface_in_surfsoil_n5.name="soil_surface_in_surfsoil_n5"
	soil_surface_in_surfsoil_n5.containingvolumeelementname="surfsoil_n5"
	soil_surface_in_surfsoil_n5.parcel_name="n5"
	soil_surface_in_surfsoil_n5.parcel_points="p17 p18 p22 p21"
	soil_surface_in_surfsoil_n5.parcel_area=6693049.999999348
	soil_surface_in_surfsoil_n5.exterior_boundary=6817.244510421856
	
	comp_objects_dict["soil_surface_in_surfsoil_n5"]=soil_surface_in_surfsoil_n5

	soil_root_zone_in_rootsoil_n5=soil_root_zone(constants,containingscenario,currentchemical,rootsoil_n5,comp_objects_dict)
	soil_root_zone_in_rootsoil_n5.name="soil_root_zone_in_rootsoil_n5"
	soil_root_zone_in_rootsoil_n5.containingvolumeelementname="rootsoil_n5"
	soil_root_zone_in_rootsoil_n5.parcel_name="n5"
	soil_root_zone_in_rootsoil_n5.parcel_points="p17 p18 p22 p21"
	soil_root_zone_in_rootsoil_n5.parcel_area=6693049.999999348
	soil_root_zone_in_rootsoil_n5.exterior_boundary=6817.244510421856
	
	comp_objects_dict["soil_root_zone_in_rootsoil_n5"]=soil_root_zone_in_rootsoil_n5

	soil_vadose_zone_in_vadosesoil_n5=soil_vadose_zone(constants,containingscenario,currentchemical,vadosesoil_n5,comp_objects_dict)
	soil_vadose_zone_in_vadosesoil_n5.name="soil_vadose_zone_in_vadosesoil_n5"
	soil_vadose_zone_in_vadosesoil_n5.containingvolumeelementname="vadosesoil_n5"
	soil_vadose_zone_in_vadosesoil_n5.parcel_name="n5"
	soil_vadose_zone_in_vadosesoil_n5.parcel_points="p17 p18 p22 p21"
	soil_vadose_zone_in_vadosesoil_n5.parcel_area=6693049.999999348
	soil_vadose_zone_in_vadosesoil_n5.exterior_boundary=6817.244510421856
	
	comp_objects_dict["soil_vadose_zone_in_vadosesoil_n5"]=soil_vadose_zone_in_vadosesoil_n5

	groundwater_in_gw_n5=groundwater(constants,containingscenario,currentchemical,gw_n5,comp_objects_dict)
	groundwater_in_gw_n5.name="groundwater_in_gw_n5"
	groundwater_in_gw_n5.containingvolumeelementname="gw_n5"
	groundwater_in_gw_n5.parcel_name="n5"
	groundwater_in_gw_n5.parcel_points="p17 p18 p22 p21"
	groundwater_in_gw_n5.parcel_area=6693049.999999348
	groundwater_in_gw_n5.exterior_boundary=6817.244510421856
	
	comp_objects_dict["groundwater_in_gw_n5"]=groundwater_in_gw_n5

	soil_surface_in_surfsoil_s1=soil_surface(constants,containingscenario,currentchemical,surfsoil_s1,comp_objects_dict)
	soil_surface_in_surfsoil_s1.name="soil_surface_in_surfsoil_s1"
	soil_surface_in_surfsoil_s1.containingvolumeelementname="surfsoil_s1"
	soil_surface_in_surfsoil_s1.parcel_name="s1"
	soil_surface_in_surfsoil_s1.parcel_points="p4 p3 p8 p7"
	soil_surface_in_surfsoil_s1.parcel_area=58445.624999993015
	soil_surface_in_surfsoil_s1.exterior_boundary=380.0435818429189
	
	comp_objects_dict["soil_surface_in_surfsoil_s1"]=soil_surface_in_surfsoil_s1

	soil_root_zone_in_rootsoil_s1=soil_root_zone(constants,containingscenario,currentchemical,rootsoil_s1,comp_objects_dict)
	soil_root_zone_in_rootsoil_s1.name="soil_root_zone_in_rootsoil_s1"
	soil_root_zone_in_rootsoil_s1.containingvolumeelementname="rootsoil_s1"
	soil_root_zone_in_rootsoil_s1.parcel_name="s1"
	soil_root_zone_in_rootsoil_s1.parcel_points="p4 p3 p8 p7"
	soil_root_zone_in_rootsoil_s1.parcel_area=58445.624999993015
	soil_root_zone_in_rootsoil_s1.exterior_boundary=380.0435818429189
	
	comp_objects_dict["soil_root_zone_in_rootsoil_s1"]=soil_root_zone_in_rootsoil_s1

	soil_vadose_zone_in_vadosesoil_s1=soil_vadose_zone(constants,containingscenario,currentchemical,vadosesoil_s1,comp_objects_dict)
	soil_vadose_zone_in_vadosesoil_s1.name="soil_vadose_zone_in_vadosesoil_s1"
	soil_vadose_zone_in_vadosesoil_s1.containingvolumeelementname="vadosesoil_s1"
	soil_vadose_zone_in_vadosesoil_s1.parcel_name="s1"
	soil_vadose_zone_in_vadosesoil_s1.parcel_points="p4 p3 p8 p7"
	soil_vadose_zone_in_vadosesoil_s1.parcel_area=58445.624999993015
	soil_vadose_zone_in_vadosesoil_s1.exterior_boundary=380.0435818429189
	
	comp_objects_dict["soil_vadose_zone_in_vadosesoil_s1"]=soil_vadose_zone_in_vadosesoil_s1

	groundwater_in_gw_s1=groundwater(constants,containingscenario,currentchemical,gw_s1,comp_objects_dict)
	groundwater_in_gw_s1.name="groundwater_in_gw_s1"
	groundwater_in_gw_s1.containingvolumeelementname="gw_s1"
	groundwater_in_gw_s1.parcel_name="s1"
	groundwater_in_gw_s1.parcel_points="p4 p3 p8 p7"
	groundwater_in_gw_s1.parcel_area=58445.624999993015
	groundwater_in_gw_s1.exterior_boundary=380.0435818429189
	
	comp_objects_dict["groundwater_in_gw_s1"]=groundwater_in_gw_s1

	soil_surface_in_surfsoil_s4=soil_surface(constants,containingscenario,currentchemical,surfsoil_s4,comp_objects_dict)
	soil_surface_in_surfsoil_s4.name="soil_surface_in_surfsoil_s4"
	soil_surface_in_surfsoil_s4.containingvolumeelementname="surfsoil_s4"
	soil_surface_in_surfsoil_s4.parcel_name="s4"
	soil_surface_in_surfsoil_s4.parcel_points="p14 p16 p20 p18"
	soil_surface_in_surfsoil_s4.parcel_area=2041139.9999996647
	soil_surface_in_surfsoil_s4.exterior_boundary=3040.3486547433513
	
	comp_objects_dict["soil_surface_in_surfsoil_s4"]=soil_surface_in_surfsoil_s4

	soil_root_zone_in_rootsoil_s4=soil_root_zone(constants,containingscenario,currentchemical,rootsoil_s4,comp_objects_dict)
	soil_root_zone_in_rootsoil_s4.name="soil_root_zone_in_rootsoil_s4"
	soil_root_zone_in_rootsoil_s4.containingvolumeelementname="rootsoil_s4"
	soil_root_zone_in_rootsoil_s4.parcel_name="s4"
	soil_root_zone_in_rootsoil_s4.parcel_points="p14 p16 p20 p18"
	soil_root_zone_in_rootsoil_s4.parcel_area=2041139.9999996647
	soil_root_zone_in_rootsoil_s4.exterior_boundary=3040.3486547433513
	
	comp_objects_dict["soil_root_zone_in_rootsoil_s4"]=soil_root_zone_in_rootsoil_s4

	soil_vadose_zone_in_vadosesoil_s4=soil_vadose_zone(constants,containingscenario,currentchemical,vadosesoil_s4,comp_objects_dict)
	soil_vadose_zone_in_vadosesoil_s4.name="soil_vadose_zone_in_vadosesoil_s4"
	soil_vadose_zone_in_vadosesoil_s4.containingvolumeelementname="vadosesoil_s4"
	soil_vadose_zone_in_vadosesoil_s4.parcel_name="s4"
	soil_vadose_zone_in_vadosesoil_s4.parcel_points="p14 p16 p20 p18"
	soil_vadose_zone_in_vadosesoil_s4.parcel_area=2041139.9999996647
	soil_vadose_zone_in_vadosesoil_s4.exterior_boundary=3040.3486547433513
	
	comp_objects_dict["soil_vadose_zone_in_vadosesoil_s4"]=soil_vadose_zone_in_vadosesoil_s4

	groundwater_in_gw_s4=groundwater(constants,containingscenario,currentchemical,gw_s4,comp_objects_dict)
	groundwater_in_gw_s4.name="groundwater_in_gw_s4"
	groundwater_in_gw_s4.containingvolumeelementname="gw_s4"
	groundwater_in_gw_s4.parcel_name="s4"
	groundwater_in_gw_s4.parcel_points="p14 p16 p20 p18"
	groundwater_in_gw_s4.parcel_area=2041139.9999996647
	groundwater_in_gw_s4.exterior_boundary=3040.3486547433513
	
	comp_objects_dict["groundwater_in_gw_s4"]=groundwater_in_gw_s4

	soil_surface_in_surfsoil_s5=soil_surface(constants,containingscenario,currentchemical,surfsoil_s5,comp_objects_dict)
	soil_surface_in_surfsoil_s5.name="soil_surface_in_surfsoil_s5"
	soil_surface_in_surfsoil_s5.containingvolumeelementname="surfsoil_s5"
	soil_surface_in_surfsoil_s5.parcel_name="s5"
	soil_surface_in_surfsoil_s5.parcel_points="p18 p20 p24 p22"
	soil_surface_in_surfsoil_s5.parcel_area=6693049.999999348
	soil_surface_in_surfsoil_s5.exterior_boundary=6817.244510421856
	
	comp_objects_dict["soil_surface_in_surfsoil_s5"]=soil_surface_in_surfsoil_s5

	soil_root_zone_in_rootsoil_s5=soil_root_zone(constants,containingscenario,currentchemical,rootsoil_s5,comp_objects_dict)
	soil_root_zone_in_rootsoil_s5.name="soil_root_zone_in_rootsoil_s5"
	soil_root_zone_in_rootsoil_s5.containingvolumeelementname="rootsoil_s5"
	soil_root_zone_in_rootsoil_s5.parcel_name="s5"
	soil_root_zone_in_rootsoil_s5.parcel_points="p18 p20 p24 p22"
	soil_root_zone_in_rootsoil_s5.parcel_area=6693049.999999348
	soil_root_zone_in_rootsoil_s5.exterior_boundary=6817.244510421856
	
	comp_objects_dict["soil_root_zone_in_rootsoil_s5"]=soil_root_zone_in_rootsoil_s5

	soil_vadose_zone_in_vadosesoil_s5=soil_vadose_zone(constants,containingscenario,currentchemical,vadosesoil_s5,comp_objects_dict)
	soil_vadose_zone_in_vadosesoil_s5.name="soil_vadose_zone_in_vadosesoil_s5"
	soil_vadose_zone_in_vadosesoil_s5.containingvolumeelementname="vadosesoil_s5"
	soil_vadose_zone_in_vadosesoil_s5.parcel_name="s5"
	soil_vadose_zone_in_vadosesoil_s5.parcel_points="p18 p20 p24 p22"
	soil_vadose_zone_in_vadosesoil_s5.parcel_area=6693049.999999348
	soil_vadose_zone_in_vadosesoil_s5.exterior_boundary=6817.244510421856
	
	comp_objects_dict["soil_vadose_zone_in_vadosesoil_s5"]=soil_vadose_zone_in_vadosesoil_s5

	groundwater_in_gw_s5=groundwater(constants,containingscenario,currentchemical,gw_s5,comp_objects_dict)
	groundwater_in_gw_s5.name="groundwater_in_gw_s5"
	groundwater_in_gw_s5.containingvolumeelementname="gw_s5"
	groundwater_in_gw_s5.parcel_name="s5"
	groundwater_in_gw_s5.parcel_points="p18 p20 p24 p22"
	groundwater_in_gw_s5.parcel_area=6693049.999999348
	groundwater_in_gw_s5.exterior_boundary=6817.244510421856
	
	comp_objects_dict["groundwater_in_gw_s5"]=groundwater_in_gw_s5

	degradation_reaction_sink_in_air_source=degradation_reaction_sink(constants,containingscenario,currentchemical,air_source,comp_objects_dict)
	degradation_reaction_sink_in_air_source.name="degradation_reaction_sink_in_air_source"
	degradation_reaction_sink_in_air_source.containingvolumeelementname="air_source"
	degradation_reaction_sink_in_air_source.parcel_name="source"
	degradation_reaction_sink_in_air_source.parcel_points="p1 p2 p3 p4 p5"
	degradation_reaction_sink_in_air_source.parcel_area=62500.0
	degradation_reaction_sink_in_air_source.exterior_boundary=750.0
	
	comp_objects_dict["degradation_reaction_sink_in_air_source"]=degradation_reaction_sink_in_air_source

	degradation_reaction_sink_in_air_n1=degradation_reaction_sink(constants,containingscenario,currentchemical,air_n1,comp_objects_dict)
	degradation_reaction_sink_in_air_n1.name="degradation_reaction_sink_in_air_n1"
	degradation_reaction_sink_in_air_n1.containingvolumeelementname="air_n1"
	degradation_reaction_sink_in_air_n1.parcel_name="n1"
	degradation_reaction_sink_in_air_n1.parcel_points="p5 p4 p7 p6"
	degradation_reaction_sink_in_air_n1.parcel_area=58445.624999993015
	degradation_reaction_sink_in_air_n1.exterior_boundary=380.0435818429189
	
	comp_objects_dict["degradation_reaction_sink_in_air_n1"]=degradation_reaction_sink_in_air_n1

	degradation_reaction_sink_in_air_n6=degradation_reaction_sink(constants,containingscenario,currentchemical,air_n6,comp_objects_dict)
	degradation_reaction_sink_in_air_n6.name="degradation_reaction_sink_in_air_n6"
	degradation_reaction_sink_in_air_n6.containingvolumeelementname="air_n6"
	degradation_reaction_sink_in_air_n6.parcel_name="n6"
	degradation_reaction_sink_in_air_n6.parcel_points="p6 p7 p26 p25"
	degradation_reaction_sink_in_air_n6.parcel_area=40633.00000000745
	degradation_reaction_sink_in_air_n6.exterior_boundary=202.6895855736298
	
	comp_objects_dict["degradation_reaction_sink_in_air_n6"]=degradation_reaction_sink_in_air_n6

	degradation_reaction_sink_in_air_n7=degradation_reaction_sink(constants,containingscenario,currentchemical,air_n7,comp_objects_dict)
	degradation_reaction_sink_in_air_n7.name="degradation_reaction_sink_in_air_n7"
	degradation_reaction_sink_in_air_n7.containingvolumeelementname="air_n7"
	degradation_reaction_sink_in_air_n7.parcel_name="n7"
	degradation_reaction_sink_in_air_n7.parcel_points="p25 p26 p10 p9"
	degradation_reaction_sink_in_air_n7.parcel_area=73291.50000005029
	degradation_reaction_sink_in_air_n7.exterior_boundary=304.035190232991
	
	comp_objects_dict["degradation_reaction_sink_in_air_n7"]=degradation_reaction_sink_in_air_n7

	degradation_reaction_sink_in_air_n3=degradation_reaction_sink(constants,containingscenario,currentchemical,air_n3,comp_objects_dict)
	degradation_reaction_sink_in_air_n3.name="degradation_reaction_sink_in_air_n3"
	degradation_reaction_sink_in_air_n3.containingvolumeelementname="air_n3"
	degradation_reaction_sink_in_air_n3.parcel_name="n3"
	degradation_reaction_sink_in_air_n3.parcel_points="p9 p10 p14 p13"
	degradation_reaction_sink_in_air_n3.parcel_area=351265.0000001304
	degradation_reaction_sink_in_air_n3.exterior_boundary=1013.4479278679979
	
	comp_objects_dict["degradation_reaction_sink_in_air_n3"]=degradation_reaction_sink_in_air_n3

	degradation_reaction_sink_in_air_n4=degradation_reaction_sink(constants,containingscenario,currentchemical,air_n4,comp_objects_dict)
	degradation_reaction_sink_in_air_n4.name="degradation_reaction_sink_in_air_n4"
	degradation_reaction_sink_in_air_n4.containingvolumeelementname="air_n4"
	degradation_reaction_sink_in_air_n4.parcel_name="n4"
	degradation_reaction_sink_in_air_n4.parcel_points="p13 p14 p18 p17"
	degradation_reaction_sink_in_air_n4.parcel_area=2041139.9999996647
	degradation_reaction_sink_in_air_n4.exterior_boundary=3040.3486547433513
	
	comp_objects_dict["degradation_reaction_sink_in_air_n4"]=degradation_reaction_sink_in_air_n4

	degradation_reaction_sink_in_air_n5=degradation_reaction_sink(constants,containingscenario,currentchemical,air_n5,comp_objects_dict)
	degradation_reaction_sink_in_air_n5.name="degradation_reaction_sink_in_air_n5"
	degradation_reaction_sink_in_air_n5.containingvolumeelementname="air_n5"
	degradation_reaction_sink_in_air_n5.parcel_name="n5"
	degradation_reaction_sink_in_air_n5.parcel_points="p17 p18 p22 p21"
	degradation_reaction_sink_in_air_n5.parcel_area=6693049.999999348
	degradation_reaction_sink_in_air_n5.exterior_boundary=6817.244510421856
	
	comp_objects_dict["degradation_reaction_sink_in_air_n5"]=degradation_reaction_sink_in_air_n5

	degradation_reaction_sink_in_air_s1=degradation_reaction_sink(constants,containingscenario,currentchemical,air_s1,comp_objects_dict)
	degradation_reaction_sink_in_air_s1.name="degradation_reaction_sink_in_air_s1"
	degradation_reaction_sink_in_air_s1.containingvolumeelementname="air_s1"
	degradation_reaction_sink_in_air_s1.parcel_name="s1"
	degradation_reaction_sink_in_air_s1.parcel_points="p4 p3 p8 p7"
	degradation_reaction_sink_in_air_s1.parcel_area=58445.624999993015
	degradation_reaction_sink_in_air_s1.exterior_boundary=380.0435818429189
	
	comp_objects_dict["degradation_reaction_sink_in_air_s1"]=degradation_reaction_sink_in_air_s1

	degradation_reaction_sink_in_air_pond=degradation_reaction_sink(constants,containingscenario,currentchemical,air_pond,comp_objects_dict)
	degradation_reaction_sink_in_air_pond.name="degradation_reaction_sink_in_air_pond"
	degradation_reaction_sink_in_air_pond.containingvolumeelementname="air_pond"
	degradation_reaction_sink_in_air_pond.parcel_name="pond"
	degradation_reaction_sink_in_air_pond.parcel_points="p7 p8 p16 p14"
	degradation_reaction_sink_in_air_pond.parcel_area=465187.5
	degradation_reaction_sink_in_air_pond.exterior_boundary=1520.1727036425948
	
	comp_objects_dict["degradation_reaction_sink_in_air_pond"]=degradation_reaction_sink_in_air_pond

	degradation_reaction_sink_in_air_s4=degradation_reaction_sink(constants,containingscenario,currentchemical,air_s4,comp_objects_dict)
	degradation_reaction_sink_in_air_s4.name="degradation_reaction_sink_in_air_s4"
	degradation_reaction_sink_in_air_s4.containingvolumeelementname="air_s4"
	degradation_reaction_sink_in_air_s4.parcel_name="s4"
	degradation_reaction_sink_in_air_s4.parcel_points="p14 p16 p20 p18"
	degradation_reaction_sink_in_air_s4.parcel_area=2041139.9999996647
	degradation_reaction_sink_in_air_s4.exterior_boundary=3040.3486547433513
	
	comp_objects_dict["degradation_reaction_sink_in_air_s4"]=degradation_reaction_sink_in_air_s4

	degradation_reaction_sink_in_air_s5=degradation_reaction_sink(constants,containingscenario,currentchemical,air_s5,comp_objects_dict)
	degradation_reaction_sink_in_air_s5.name="degradation_reaction_sink_in_air_s5"
	degradation_reaction_sink_in_air_s5.containingvolumeelementname="air_s5"
	degradation_reaction_sink_in_air_s5.parcel_name="s5"
	degradation_reaction_sink_in_air_s5.parcel_points="p18 p20 p24 p22"
	degradation_reaction_sink_in_air_s5.parcel_area=6693049.999999348
	degradation_reaction_sink_in_air_s5.exterior_boundary=6817.244510421856
	
	comp_objects_dict["degradation_reaction_sink_in_air_s5"]=degradation_reaction_sink_in_air_s5

	degradation_reaction_sink_in_sw_pond=degradation_reaction_sink(constants,containingscenario,currentchemical,sw_pond,comp_objects_dict)
	degradation_reaction_sink_in_sw_pond.name="degradation_reaction_sink_in_sw_pond"
	degradation_reaction_sink_in_sw_pond.containingvolumeelementname="sw_pond"
	degradation_reaction_sink_in_sw_pond.parcel_name="pond"
	degradation_reaction_sink_in_sw_pond.parcel_points="p7 p8 p16 p14"
	degradation_reaction_sink_in_sw_pond.parcel_area=465187.5
	degradation_reaction_sink_in_sw_pond.exterior_boundary=1520.1727036425948
	
	comp_objects_dict["degradation_reaction_sink_in_sw_pond"]=degradation_reaction_sink_in_sw_pond

	flush_rate_sink_in_sw_pond=flush_rate_sink(constants,containingscenario,currentchemical,sw_pond,comp_objects_dict)
	flush_rate_sink_in_sw_pond.name="flush_rate_sink_in_sw_pond"
	flush_rate_sink_in_sw_pond.containingvolumeelementname="sw_pond"
	flush_rate_sink_in_sw_pond.parcel_name="pond"
	flush_rate_sink_in_sw_pond.parcel_points="p7 p8 p16 p14"
	flush_rate_sink_in_sw_pond.parcel_area=465187.5
	flush_rate_sink_in_sw_pond.exterior_boundary=1520.1727036425948
	
	comp_objects_dict["flush_rate_sink_in_sw_pond"]=flush_rate_sink_in_sw_pond

	macrophyte_in_sw_pond=macrophyte(constants,containingscenario,currentchemical,sw_pond,comp_objects_dict)
	macrophyte_in_sw_pond.name="macrophyte_in_sw_pond"
	macrophyte_in_sw_pond.containingvolumeelementname="sw_pond"
	macrophyte_in_sw_pond.parcel_name="pond"
	macrophyte_in_sw_pond.parcel_points="p7 p8 p16 p14"
	macrophyte_in_sw_pond.parcel_area=465187.5
	macrophyte_in_sw_pond.exterior_boundary=1520.1727036425948
	
	comp_objects_dict["macrophyte_in_sw_pond"]=macrophyte_in_sw_pond

	zooplankton_in_sw_pond=zooplankton(constants,containingscenario,currentchemical,sw_pond,comp_objects_dict)
	zooplankton_in_sw_pond.name="zooplankton_in_sw_pond"
	zooplankton_in_sw_pond.containingvolumeelementname="sw_pond"
	zooplankton_in_sw_pond.parcel_name="pond"
	zooplankton_in_sw_pond.parcel_points="p7 p8 p16 p14"
	zooplankton_in_sw_pond.parcel_area=465187.5
	zooplankton_in_sw_pond.exterior_boundary=1520.1727036425948
	
	comp_objects_dict["zooplankton_in_sw_pond"]=zooplankton_in_sw_pond

	water_column_herbivore_in_sw_pond=water_column_herbivore(constants,containingscenario,currentchemical,sw_pond,comp_objects_dict)
	water_column_herbivore_in_sw_pond.name="water_column_herbivore_in_sw_pond"
	water_column_herbivore_in_sw_pond.containingvolumeelementname="sw_pond"
	water_column_herbivore_in_sw_pond.parcel_name="pond"
	water_column_herbivore_in_sw_pond.parcel_points="p7 p8 p16 p14"
	water_column_herbivore_in_sw_pond.parcel_area=465187.5
	water_column_herbivore_in_sw_pond.exterior_boundary=1520.1727036425948
	
	comp_objects_dict["water_column_herbivore_in_sw_pond"]=water_column_herbivore_in_sw_pond

	water_column_omnivore_in_sw_pond=water_column_omnivore(constants,containingscenario,currentchemical,sw_pond,comp_objects_dict)
	water_column_omnivore_in_sw_pond.name="water_column_omnivore_in_sw_pond"
	water_column_omnivore_in_sw_pond.containingvolumeelementname="sw_pond"
	water_column_omnivore_in_sw_pond.parcel_name="pond"
	water_column_omnivore_in_sw_pond.parcel_points="p7 p8 p16 p14"
	water_column_omnivore_in_sw_pond.parcel_area=465187.5
	water_column_omnivore_in_sw_pond.exterior_boundary=1520.1727036425948
	
	comp_objects_dict["water_column_omnivore_in_sw_pond"]=water_column_omnivore_in_sw_pond

	water_column_carnivore_in_sw_pond=water_column_carnivore(constants,containingscenario,currentchemical,sw_pond,comp_objects_dict)
	water_column_carnivore_in_sw_pond.name="water_column_carnivore_in_sw_pond"
	water_column_carnivore_in_sw_pond.containingvolumeelementname="sw_pond"
	water_column_carnivore_in_sw_pond.parcel_name="pond"
	water_column_carnivore_in_sw_pond.parcel_points="p7 p8 p16 p14"
	water_column_carnivore_in_sw_pond.parcel_area=465187.5
	water_column_carnivore_in_sw_pond.exterior_boundary=1520.1727036425948
	
	comp_objects_dict["water_column_carnivore_in_sw_pond"]=water_column_carnivore_in_sw_pond

	degradation_reaction_sink_in_sed_pond=degradation_reaction_sink(constants,containingscenario,currentchemical,sed_pond,comp_objects_dict)
	degradation_reaction_sink_in_sed_pond.name="degradation_reaction_sink_in_sed_pond"
	degradation_reaction_sink_in_sed_pond.containingvolumeelementname="sed_pond"
	degradation_reaction_sink_in_sed_pond.parcel_name="pond"
	degradation_reaction_sink_in_sed_pond.parcel_points="p7 p8 p16 p14"
	degradation_reaction_sink_in_sed_pond.parcel_area=465187.5
	degradation_reaction_sink_in_sed_pond.exterior_boundary=1520.1727036425948
	
	comp_objects_dict["degradation_reaction_sink_in_sed_pond"]=degradation_reaction_sink_in_sed_pond

	benthic_invertebrate_in_sed_pond=benthic_invertebrate(constants,containingscenario,currentchemical,sed_pond,comp_objects_dict)
	benthic_invertebrate_in_sed_pond.name="benthic_invertebrate_in_sed_pond"
	benthic_invertebrate_in_sed_pond.containingvolumeelementname="sed_pond"
	benthic_invertebrate_in_sed_pond.parcel_name="pond"
	benthic_invertebrate_in_sed_pond.parcel_points="p7 p8 p16 p14"
	benthic_invertebrate_in_sed_pond.parcel_area=465187.5
	benthic_invertebrate_in_sed_pond.exterior_boundary=1520.1727036425948
	
	comp_objects_dict["benthic_invertebrate_in_sed_pond"]=benthic_invertebrate_in_sed_pond

	benthic_omnivore_in_sed_pond=benthic_omnivore(constants,containingscenario,currentchemical,sed_pond,comp_objects_dict)
	benthic_omnivore_in_sed_pond.name="benthic_omnivore_in_sed_pond"
	benthic_omnivore_in_sed_pond.containingvolumeelementname="sed_pond"
	benthic_omnivore_in_sed_pond.parcel_name="pond"
	benthic_omnivore_in_sed_pond.parcel_points="p7 p8 p16 p14"
	benthic_omnivore_in_sed_pond.parcel_area=465187.5
	benthic_omnivore_in_sed_pond.exterior_boundary=1520.1727036425948
	
	comp_objects_dict["benthic_omnivore_in_sed_pond"]=benthic_omnivore_in_sed_pond

	benthic_carnivore_in_sed_pond=benthic_carnivore(constants,containingscenario,currentchemical,sed_pond,comp_objects_dict)
	benthic_carnivore_in_sed_pond.name="benthic_carnivore_in_sed_pond"
	benthic_carnivore_in_sed_pond.containingvolumeelementname="sed_pond"
	benthic_carnivore_in_sed_pond.parcel_name="pond"
	benthic_carnivore_in_sed_pond.parcel_points="p7 p8 p16 p14"
	benthic_carnivore_in_sed_pond.parcel_area=465187.5
	benthic_carnivore_in_sed_pond.exterior_boundary=1520.1727036425948
	
	comp_objects_dict["benthic_carnivore_in_sed_pond"]=benthic_carnivore_in_sed_pond

	degradation_reaction_sink_in_gw_source=degradation_reaction_sink(constants,containingscenario,currentchemical,gw_source,comp_objects_dict)
	degradation_reaction_sink_in_gw_source.name="degradation_reaction_sink_in_gw_source"
	degradation_reaction_sink_in_gw_source.containingvolumeelementname="gw_source"
	degradation_reaction_sink_in_gw_source.parcel_name="source"
	degradation_reaction_sink_in_gw_source.parcel_points="p1 p2 p3 p4 p5"
	degradation_reaction_sink_in_gw_source.parcel_area=62500.0
	degradation_reaction_sink_in_gw_source.exterior_boundary=750.0
	
	comp_objects_dict["degradation_reaction_sink_in_gw_source"]=degradation_reaction_sink_in_gw_source

	degradation_reaction_sink_in_vadosesoil_source=degradation_reaction_sink(constants,containingscenario,currentchemical,vadosesoil_source,comp_objects_dict)
	degradation_reaction_sink_in_vadosesoil_source.name="degradation_reaction_sink_in_vadosesoil_source"
	degradation_reaction_sink_in_vadosesoil_source.containingvolumeelementname="vadosesoil_source"
	degradation_reaction_sink_in_vadosesoil_source.parcel_name="source"
	degradation_reaction_sink_in_vadosesoil_source.parcel_points="p1 p2 p3 p4 p5"
	degradation_reaction_sink_in_vadosesoil_source.parcel_area=62500.0
	degradation_reaction_sink_in_vadosesoil_source.exterior_boundary=750.0
	
	comp_objects_dict["degradation_reaction_sink_in_vadosesoil_source"]=degradation_reaction_sink_in_vadosesoil_source

	degradation_reaction_sink_in_rootsoil_source=degradation_reaction_sink(constants,containingscenario,currentchemical,rootsoil_source,comp_objects_dict)
	degradation_reaction_sink_in_rootsoil_source.name="degradation_reaction_sink_in_rootsoil_source"
	degradation_reaction_sink_in_rootsoil_source.containingvolumeelementname="rootsoil_source"
	degradation_reaction_sink_in_rootsoil_source.parcel_name="source"
	degradation_reaction_sink_in_rootsoil_source.parcel_points="p1 p2 p3 p4 p5"
	degradation_reaction_sink_in_rootsoil_source.parcel_area=62500.0
	degradation_reaction_sink_in_rootsoil_source.exterior_boundary=750.0
	
	comp_objects_dict["degradation_reaction_sink_in_rootsoil_source"]=degradation_reaction_sink_in_rootsoil_source

	degradation_reaction_sink_in_surfsoil_source=degradation_reaction_sink(constants,containingscenario,currentchemical,surfsoil_source,comp_objects_dict)
	degradation_reaction_sink_in_surfsoil_source.name="degradation_reaction_sink_in_surfsoil_source"
	degradation_reaction_sink_in_surfsoil_source.containingvolumeelementname="surfsoil_source"
	degradation_reaction_sink_in_surfsoil_source.parcel_name="source"
	degradation_reaction_sink_in_surfsoil_source.parcel_points="p1 p2 p3 p4 p5"
	degradation_reaction_sink_in_surfsoil_source.parcel_area=62500.0
	degradation_reaction_sink_in_surfsoil_source.exterior_boundary=750.0
	
	comp_objects_dict["degradation_reaction_sink_in_surfsoil_source"]=degradation_reaction_sink_in_surfsoil_source

	degradation_reaction_sink_in_gw_n1=degradation_reaction_sink(constants,containingscenario,currentchemical,gw_n1,comp_objects_dict)
	degradation_reaction_sink_in_gw_n1.name="degradation_reaction_sink_in_gw_n1"
	degradation_reaction_sink_in_gw_n1.containingvolumeelementname="gw_n1"
	degradation_reaction_sink_in_gw_n1.parcel_name="n1"
	degradation_reaction_sink_in_gw_n1.parcel_points="p5 p4 p7 p6"
	degradation_reaction_sink_in_gw_n1.parcel_area=58445.624999993015
	degradation_reaction_sink_in_gw_n1.exterior_boundary=380.0435818429189
	
	comp_objects_dict["degradation_reaction_sink_in_gw_n1"]=degradation_reaction_sink_in_gw_n1

	degradation_reaction_sink_in_vadosesoil_n1=degradation_reaction_sink(constants,containingscenario,currentchemical,vadosesoil_n1,comp_objects_dict)
	degradation_reaction_sink_in_vadosesoil_n1.name="degradation_reaction_sink_in_vadosesoil_n1"
	degradation_reaction_sink_in_vadosesoil_n1.containingvolumeelementname="vadosesoil_n1"
	degradation_reaction_sink_in_vadosesoil_n1.parcel_name="n1"
	degradation_reaction_sink_in_vadosesoil_n1.parcel_points="p5 p4 p7 p6"
	degradation_reaction_sink_in_vadosesoil_n1.parcel_area=58445.624999993015
	degradation_reaction_sink_in_vadosesoil_n1.exterior_boundary=380.0435818429189
	
	comp_objects_dict["degradation_reaction_sink_in_vadosesoil_n1"]=degradation_reaction_sink_in_vadosesoil_n1

	degradation_reaction_sink_in_rootsoil_n1=degradation_reaction_sink(constants,containingscenario,currentchemical,rootsoil_n1,comp_objects_dict)
	degradation_reaction_sink_in_rootsoil_n1.name="degradation_reaction_sink_in_rootsoil_n1"
	degradation_reaction_sink_in_rootsoil_n1.containingvolumeelementname="rootsoil_n1"
	degradation_reaction_sink_in_rootsoil_n1.parcel_name="n1"
	degradation_reaction_sink_in_rootsoil_n1.parcel_points="p5 p4 p7 p6"
	degradation_reaction_sink_in_rootsoil_n1.parcel_area=58445.624999993015
	degradation_reaction_sink_in_rootsoil_n1.exterior_boundary=380.0435818429189
	
	comp_objects_dict["degradation_reaction_sink_in_rootsoil_n1"]=degradation_reaction_sink_in_rootsoil_n1

	degradation_reaction_sink_in_surfsoil_n1=degradation_reaction_sink(constants,containingscenario,currentchemical,surfsoil_n1,comp_objects_dict)
	degradation_reaction_sink_in_surfsoil_n1.name="degradation_reaction_sink_in_surfsoil_n1"
	degradation_reaction_sink_in_surfsoil_n1.containingvolumeelementname="surfsoil_n1"
	degradation_reaction_sink_in_surfsoil_n1.parcel_name="n1"
	degradation_reaction_sink_in_surfsoil_n1.parcel_points="p5 p4 p7 p6"
	degradation_reaction_sink_in_surfsoil_n1.parcel_area=58445.624999993015
	degradation_reaction_sink_in_surfsoil_n1.exterior_boundary=380.0435818429189
	
	comp_objects_dict["degradation_reaction_sink_in_surfsoil_n1"]=degradation_reaction_sink_in_surfsoil_n1

	leaf_grasses_herbs_in_surfsoil_n1=leaf_grasses_herbs_in_grasses_herbs(constants,containingscenario,currentchemical,surfsoil_n1,comp_objects_dict)
	leaf_grasses_herbs_in_surfsoil_n1.name="leaf_grasses_herbs_in_surfsoil_n1"
	leaf_grasses_herbs_in_surfsoil_n1.containingvolumeelementname="surfsoil_n1"
	leaf_grasses_herbs_in_surfsoil_n1.parcel_name="n1"
	leaf_grasses_herbs_in_surfsoil_n1.parcel_points="p5 p4 p7 p6"
	leaf_grasses_herbs_in_surfsoil_n1.parcel_area=58445.624999993015
	leaf_grasses_herbs_in_surfsoil_n1.exterior_boundary=380.0435818429189
	
	leaf_grasses_herbs_in_surfsoil_n1.associated_soil_comp=comp_objects_dict["soil_surface_in_surfsoil_n1"]

	comp_objects_dict["leaf_grasses_herbs_in_surfsoil_n1"]=leaf_grasses_herbs_in_surfsoil_n1

	soil_surface_in_surfsoil_n1.associated_leaf_comp=comp_objects_dict["leaf_grasses_herbs_in_surfsoil_n1"]

	comp_objects_dict["soil_surface_in_surfsoil_n1"]=soil_surface_in_surfsoil_n1

	leaf_particle_grasses_herbs_in_surfsoil_n1=leaf_particle_grasses_herbs_in_grasses_herbs(constants,containingscenario,currentchemical,surfsoil_n1,comp_objects_dict)
	leaf_particle_grasses_herbs_in_surfsoil_n1.name="leaf_particle_grasses_herbs_in_surfsoil_n1"
	leaf_particle_grasses_herbs_in_surfsoil_n1.containingvolumeelementname="surfsoil_n1"
	leaf_particle_grasses_herbs_in_surfsoil_n1.parcel_name="n1"
	leaf_particle_grasses_herbs_in_surfsoil_n1.parcel_points="p5 p4 p7 p6"
	leaf_particle_grasses_herbs_in_surfsoil_n1.parcel_area=58445.624999993015
	leaf_particle_grasses_herbs_in_surfsoil_n1.exterior_boundary=380.0435818429189
	
	leaf_particle_grasses_herbs_in_surfsoil_n1.associated_soil_comp=comp_objects_dict["soil_surface_in_surfsoil_n1"]

	leaf_particle_grasses_herbs_in_surfsoil_n1.associated_leaf_comp=comp_objects_dict["leaf_grasses_herbs_in_surfsoil_n1"]

	comp_objects_dict["leaf_particle_grasses_herbs_in_surfsoil_n1"]=leaf_particle_grasses_herbs_in_surfsoil_n1

	stem_grasses_herbs_in_surfsoil_n1=stem_grasses_herbs_in_grasses_herbs(constants,containingscenario,currentchemical,surfsoil_n1,comp_objects_dict)
	stem_grasses_herbs_in_surfsoil_n1.name="stem_grasses_herbs_in_surfsoil_n1"
	stem_grasses_herbs_in_surfsoil_n1.containingvolumeelementname="surfsoil_n1"
	stem_grasses_herbs_in_surfsoil_n1.parcel_name="n1"
	stem_grasses_herbs_in_surfsoil_n1.parcel_points="p5 p4 p7 p6"
	stem_grasses_herbs_in_surfsoil_n1.parcel_area=58445.624999993015
	stem_grasses_herbs_in_surfsoil_n1.exterior_boundary=380.0435818429189
	
	stem_grasses_herbs_in_surfsoil_n1.associated_soil_comp=comp_objects_dict["soil_surface_in_surfsoil_n1"]

	stem_grasses_herbs_in_surfsoil_n1.associated_leaf_comp=comp_objects_dict["leaf_grasses_herbs_in_surfsoil_n1"]

	comp_objects_dict["stem_grasses_herbs_in_surfsoil_n1"]=stem_grasses_herbs_in_surfsoil_n1

	soil_surface_in_surfsoil_n1.associated_stem_comp=comp_objects_dict["stem_grasses_herbs_in_surfsoil_n1"]

	comp_objects_dict["soil_surface_in_surfsoil_n1"]=soil_surface_in_surfsoil_n1

	leaf_grasses_herbs_in_surfsoil_n1.associated_stem_comp=comp_objects_dict["stem_grasses_herbs_in_surfsoil_n1"]

	comp_objects_dict["leaf_grasses_herbs_in_surfsoil_n1"]=leaf_grasses_herbs_in_surfsoil_n1

	root_grasses_herbs_in_surfsoil_n1=root_grasses_herbs_in_grasses_herbs(constants,containingscenario,currentchemical,surfsoil_n1,comp_objects_dict)
	root_grasses_herbs_in_surfsoil_n1.name="root_grasses_herbs_in_surfsoil_n1"
	root_grasses_herbs_in_surfsoil_n1.containingvolumeelementname="surfsoil_n1"
	root_grasses_herbs_in_surfsoil_n1.parcel_name="n1"
	root_grasses_herbs_in_surfsoil_n1.parcel_points="p5 p4 p7 p6"
	root_grasses_herbs_in_surfsoil_n1.parcel_area=58445.624999993015
	root_grasses_herbs_in_surfsoil_n1.exterior_boundary=380.0435818429189
	
	root_grasses_herbs_in_surfsoil_n1.associated_soil_comp=comp_objects_dict["soil_root_zone_in_rootsoil_n1"]

	root_grasses_herbs_in_surfsoil_n1.associated_stem_comp=comp_objects_dict["stem_grasses_herbs_in_surfsoil_n1"]

	comp_objects_dict["root_grasses_herbs_in_surfsoil_n1"]=root_grasses_herbs_in_surfsoil_n1

	soil_root_zone_in_rootsoil_n1.associated_root_comp=comp_objects_dict["root_grasses_herbs_in_surfsoil_n1"]

	comp_objects_dict["soil_root_zone_in_rootsoil_n1"]=soil_root_zone_in_rootsoil_n1

	leaf_grasses_herbs_in_surfsoil_n1.associated_root_comp=comp_objects_dict["root_grasses_herbs_in_surfsoil_n1"]

	comp_objects_dict["leaf_grasses_herbs_in_surfsoil_n1"]=leaf_grasses_herbs_in_surfsoil_n1

	stem_grasses_herbs_in_surfsoil_n1.associated_root_comp=comp_objects_dict["root_grasses_herbs_in_surfsoil_n1"]

	comp_objects_dict["stem_grasses_herbs_in_surfsoil_n1"]=stem_grasses_herbs_in_surfsoil_n1

	degradation_reaction_sink_in_gw_n6=degradation_reaction_sink(constants,containingscenario,currentchemical,gw_n6,comp_objects_dict)
	degradation_reaction_sink_in_gw_n6.name="degradation_reaction_sink_in_gw_n6"
	degradation_reaction_sink_in_gw_n6.containingvolumeelementname="gw_n6"
	degradation_reaction_sink_in_gw_n6.parcel_name="n6"
	degradation_reaction_sink_in_gw_n6.parcel_points="p6 p7 p26 p25"
	degradation_reaction_sink_in_gw_n6.parcel_area=40633.00000000745
	degradation_reaction_sink_in_gw_n6.exterior_boundary=202.6895855736298
	
	comp_objects_dict["degradation_reaction_sink_in_gw_n6"]=degradation_reaction_sink_in_gw_n6

	degradation_reaction_sink_in_vadosesoil_n6=degradation_reaction_sink(constants,containingscenario,currentchemical,vadosesoil_n6,comp_objects_dict)
	degradation_reaction_sink_in_vadosesoil_n6.name="degradation_reaction_sink_in_vadosesoil_n6"
	degradation_reaction_sink_in_vadosesoil_n6.containingvolumeelementname="vadosesoil_n6"
	degradation_reaction_sink_in_vadosesoil_n6.parcel_name="n6"
	degradation_reaction_sink_in_vadosesoil_n6.parcel_points="p6 p7 p26 p25"
	degradation_reaction_sink_in_vadosesoil_n6.parcel_area=40633.00000000745
	degradation_reaction_sink_in_vadosesoil_n6.exterior_boundary=202.6895855736298
	
	comp_objects_dict["degradation_reaction_sink_in_vadosesoil_n6"]=degradation_reaction_sink_in_vadosesoil_n6

	degradation_reaction_sink_in_rootsoil_n6=degradation_reaction_sink(constants,containingscenario,currentchemical,rootsoil_n6,comp_objects_dict)
	degradation_reaction_sink_in_rootsoil_n6.name="degradation_reaction_sink_in_rootsoil_n6"
	degradation_reaction_sink_in_rootsoil_n6.containingvolumeelementname="rootsoil_n6"
	degradation_reaction_sink_in_rootsoil_n6.parcel_name="n6"
	degradation_reaction_sink_in_rootsoil_n6.parcel_points="p6 p7 p26 p25"
	degradation_reaction_sink_in_rootsoil_n6.parcel_area=40633.00000000745
	degradation_reaction_sink_in_rootsoil_n6.exterior_boundary=202.6895855736298
	
	comp_objects_dict["degradation_reaction_sink_in_rootsoil_n6"]=degradation_reaction_sink_in_rootsoil_n6

	degradation_reaction_sink_in_surfsoil_n6=degradation_reaction_sink(constants,containingscenario,currentchemical,surfsoil_n6,comp_objects_dict)
	degradation_reaction_sink_in_surfsoil_n6.name="degradation_reaction_sink_in_surfsoil_n6"
	degradation_reaction_sink_in_surfsoil_n6.containingvolumeelementname="surfsoil_n6"
	degradation_reaction_sink_in_surfsoil_n6.parcel_name="n6"
	degradation_reaction_sink_in_surfsoil_n6.parcel_points="p6 p7 p26 p25"
	degradation_reaction_sink_in_surfsoil_n6.parcel_area=40633.00000000745
	degradation_reaction_sink_in_surfsoil_n6.exterior_boundary=202.6895855736298
	
	comp_objects_dict["degradation_reaction_sink_in_surfsoil_n6"]=degradation_reaction_sink_in_surfsoil_n6

	degradation_reaction_sink_in_gw_n7=degradation_reaction_sink(constants,containingscenario,currentchemical,gw_n7,comp_objects_dict)
	degradation_reaction_sink_in_gw_n7.name="degradation_reaction_sink_in_gw_n7"
	degradation_reaction_sink_in_gw_n7.containingvolumeelementname="gw_n7"
	degradation_reaction_sink_in_gw_n7.parcel_name="n7"
	degradation_reaction_sink_in_gw_n7.parcel_points="p25 p26 p10 p9"
	degradation_reaction_sink_in_gw_n7.parcel_area=73291.50000005029
	degradation_reaction_sink_in_gw_n7.exterior_boundary=304.035190232991
	
	comp_objects_dict["degradation_reaction_sink_in_gw_n7"]=degradation_reaction_sink_in_gw_n7

	degradation_reaction_sink_in_vadosesoil_n7=degradation_reaction_sink(constants,containingscenario,currentchemical,vadosesoil_n7,comp_objects_dict)
	degradation_reaction_sink_in_vadosesoil_n7.name="degradation_reaction_sink_in_vadosesoil_n7"
	degradation_reaction_sink_in_vadosesoil_n7.containingvolumeelementname="vadosesoil_n7"
	degradation_reaction_sink_in_vadosesoil_n7.parcel_name="n7"
	degradation_reaction_sink_in_vadosesoil_n7.parcel_points="p25 p26 p10 p9"
	degradation_reaction_sink_in_vadosesoil_n7.parcel_area=73291.50000005029
	degradation_reaction_sink_in_vadosesoil_n7.exterior_boundary=304.035190232991
	
	comp_objects_dict["degradation_reaction_sink_in_vadosesoil_n7"]=degradation_reaction_sink_in_vadosesoil_n7

	degradation_reaction_sink_in_rootsoil_n7=degradation_reaction_sink(constants,containingscenario,currentchemical,rootsoil_n7,comp_objects_dict)
	degradation_reaction_sink_in_rootsoil_n7.name="degradation_reaction_sink_in_rootsoil_n7"
	degradation_reaction_sink_in_rootsoil_n7.containingvolumeelementname="rootsoil_n7"
	degradation_reaction_sink_in_rootsoil_n7.parcel_name="n7"
	degradation_reaction_sink_in_rootsoil_n7.parcel_points="p25 p26 p10 p9"
	degradation_reaction_sink_in_rootsoil_n7.parcel_area=73291.50000005029
	degradation_reaction_sink_in_rootsoil_n7.exterior_boundary=304.035190232991
	
	comp_objects_dict["degradation_reaction_sink_in_rootsoil_n7"]=degradation_reaction_sink_in_rootsoil_n7

	degradation_reaction_sink_in_surfsoil_n7=degradation_reaction_sink(constants,containingscenario,currentchemical,surfsoil_n7,comp_objects_dict)
	degradation_reaction_sink_in_surfsoil_n7.name="degradation_reaction_sink_in_surfsoil_n7"
	degradation_reaction_sink_in_surfsoil_n7.containingvolumeelementname="surfsoil_n7"
	degradation_reaction_sink_in_surfsoil_n7.parcel_name="n7"
	degradation_reaction_sink_in_surfsoil_n7.parcel_points="p25 p26 p10 p9"
	degradation_reaction_sink_in_surfsoil_n7.parcel_area=73291.50000005029
	degradation_reaction_sink_in_surfsoil_n7.exterior_boundary=304.035190232991
	
	comp_objects_dict["degradation_reaction_sink_in_surfsoil_n7"]=degradation_reaction_sink_in_surfsoil_n7

	leaf_grasses_herbs_in_surfsoil_n7=leaf_grasses_herbs_in_grasses_herbs(constants,containingscenario,currentchemical,surfsoil_n7,comp_objects_dict)
	leaf_grasses_herbs_in_surfsoil_n7.name="leaf_grasses_herbs_in_surfsoil_n7"
	leaf_grasses_herbs_in_surfsoil_n7.containingvolumeelementname="surfsoil_n7"
	leaf_grasses_herbs_in_surfsoil_n7.parcel_name="n7"
	leaf_grasses_herbs_in_surfsoil_n7.parcel_points="p25 p26 p10 p9"
	leaf_grasses_herbs_in_surfsoil_n7.parcel_area=73291.50000005029
	leaf_grasses_herbs_in_surfsoil_n7.exterior_boundary=304.035190232991
	
	leaf_grasses_herbs_in_surfsoil_n7.associated_soil_comp=comp_objects_dict["soil_surface_in_surfsoil_n7"]

	comp_objects_dict["leaf_grasses_herbs_in_surfsoil_n7"]=leaf_grasses_herbs_in_surfsoil_n7

	soil_surface_in_surfsoil_n7.associated_leaf_comp=comp_objects_dict["leaf_grasses_herbs_in_surfsoil_n7"]

	comp_objects_dict["soil_surface_in_surfsoil_n7"]=soil_surface_in_surfsoil_n7

	leaf_particle_grasses_herbs_in_surfsoil_n7=leaf_particle_grasses_herbs_in_grasses_herbs(constants,containingscenario,currentchemical,surfsoil_n7,comp_objects_dict)
	leaf_particle_grasses_herbs_in_surfsoil_n7.name="leaf_particle_grasses_herbs_in_surfsoil_n7"
	leaf_particle_grasses_herbs_in_surfsoil_n7.containingvolumeelementname="surfsoil_n7"
	leaf_particle_grasses_herbs_in_surfsoil_n7.parcel_name="n7"
	leaf_particle_grasses_herbs_in_surfsoil_n7.parcel_points="p25 p26 p10 p9"
	leaf_particle_grasses_herbs_in_surfsoil_n7.parcel_area=73291.50000005029
	leaf_particle_grasses_herbs_in_surfsoil_n7.exterior_boundary=304.035190232991
	
	leaf_particle_grasses_herbs_in_surfsoil_n7.associated_soil_comp=comp_objects_dict["soil_surface_in_surfsoil_n7"]

	leaf_particle_grasses_herbs_in_surfsoil_n7.associated_leaf_comp=comp_objects_dict["leaf_grasses_herbs_in_surfsoil_n7"]

	comp_objects_dict["leaf_particle_grasses_herbs_in_surfsoil_n7"]=leaf_particle_grasses_herbs_in_surfsoil_n7

	stem_grasses_herbs_in_surfsoil_n7=stem_grasses_herbs_in_grasses_herbs(constants,containingscenario,currentchemical,surfsoil_n7,comp_objects_dict)
	stem_grasses_herbs_in_surfsoil_n7.name="stem_grasses_herbs_in_surfsoil_n7"
	stem_grasses_herbs_in_surfsoil_n7.containingvolumeelementname="surfsoil_n7"
	stem_grasses_herbs_in_surfsoil_n7.parcel_name="n7"
	stem_grasses_herbs_in_surfsoil_n7.parcel_points="p25 p26 p10 p9"
	stem_grasses_herbs_in_surfsoil_n7.parcel_area=73291.50000005029
	stem_grasses_herbs_in_surfsoil_n7.exterior_boundary=304.035190232991
	
	stem_grasses_herbs_in_surfsoil_n7.associated_soil_comp=comp_objects_dict["soil_surface_in_surfsoil_n7"]

	stem_grasses_herbs_in_surfsoil_n7.associated_leaf_comp=comp_objects_dict["leaf_grasses_herbs_in_surfsoil_n7"]

	comp_objects_dict["stem_grasses_herbs_in_surfsoil_n7"]=stem_grasses_herbs_in_surfsoil_n7

	soil_surface_in_surfsoil_n7.associated_stem_comp=comp_objects_dict["stem_grasses_herbs_in_surfsoil_n7"]

	comp_objects_dict["soil_surface_in_surfsoil_n7"]=soil_surface_in_surfsoil_n7

	leaf_grasses_herbs_in_surfsoil_n7.associated_stem_comp=comp_objects_dict["stem_grasses_herbs_in_surfsoil_n7"]

	comp_objects_dict["leaf_grasses_herbs_in_surfsoil_n7"]=leaf_grasses_herbs_in_surfsoil_n7

	root_grasses_herbs_in_surfsoil_n7=root_grasses_herbs_in_grasses_herbs(constants,containingscenario,currentchemical,surfsoil_n7,comp_objects_dict)
	root_grasses_herbs_in_surfsoil_n7.name="root_grasses_herbs_in_surfsoil_n7"
	root_grasses_herbs_in_surfsoil_n7.containingvolumeelementname="surfsoil_n7"
	root_grasses_herbs_in_surfsoil_n7.parcel_name="n7"
	root_grasses_herbs_in_surfsoil_n7.parcel_points="p25 p26 p10 p9"
	root_grasses_herbs_in_surfsoil_n7.parcel_area=73291.50000005029
	root_grasses_herbs_in_surfsoil_n7.exterior_boundary=304.035190232991
	
	root_grasses_herbs_in_surfsoil_n7.associated_soil_comp=comp_objects_dict["soil_root_zone_in_rootsoil_n7"]

	root_grasses_herbs_in_surfsoil_n7.associated_stem_comp=comp_objects_dict["stem_grasses_herbs_in_surfsoil_n7"]

	comp_objects_dict["root_grasses_herbs_in_surfsoil_n7"]=root_grasses_herbs_in_surfsoil_n7

	soil_root_zone_in_rootsoil_n7.associated_root_comp=comp_objects_dict["root_grasses_herbs_in_surfsoil_n7"]

	comp_objects_dict["soil_root_zone_in_rootsoil_n7"]=soil_root_zone_in_rootsoil_n7

	leaf_grasses_herbs_in_surfsoil_n7.associated_root_comp=comp_objects_dict["root_grasses_herbs_in_surfsoil_n7"]

	comp_objects_dict["leaf_grasses_herbs_in_surfsoil_n7"]=leaf_grasses_herbs_in_surfsoil_n7

	stem_grasses_herbs_in_surfsoil_n7.associated_root_comp=comp_objects_dict["root_grasses_herbs_in_surfsoil_n7"]

	comp_objects_dict["stem_grasses_herbs_in_surfsoil_n7"]=stem_grasses_herbs_in_surfsoil_n7

	degradation_reaction_sink_in_gw_n3=degradation_reaction_sink(constants,containingscenario,currentchemical,gw_n3,comp_objects_dict)
	degradation_reaction_sink_in_gw_n3.name="degradation_reaction_sink_in_gw_n3"
	degradation_reaction_sink_in_gw_n3.containingvolumeelementname="gw_n3"
	degradation_reaction_sink_in_gw_n3.parcel_name="n3"
	degradation_reaction_sink_in_gw_n3.parcel_points="p9 p10 p14 p13"
	degradation_reaction_sink_in_gw_n3.parcel_area=351265.0000001304
	degradation_reaction_sink_in_gw_n3.exterior_boundary=1013.4479278679979
	
	comp_objects_dict["degradation_reaction_sink_in_gw_n3"]=degradation_reaction_sink_in_gw_n3

	degradation_reaction_sink_in_vadosesoil_n3=degradation_reaction_sink(constants,containingscenario,currentchemical,vadosesoil_n3,comp_objects_dict)
	degradation_reaction_sink_in_vadosesoil_n3.name="degradation_reaction_sink_in_vadosesoil_n3"
	degradation_reaction_sink_in_vadosesoil_n3.containingvolumeelementname="vadosesoil_n3"
	degradation_reaction_sink_in_vadosesoil_n3.parcel_name="n3"
	degradation_reaction_sink_in_vadosesoil_n3.parcel_points="p9 p10 p14 p13"
	degradation_reaction_sink_in_vadosesoil_n3.parcel_area=351265.0000001304
	degradation_reaction_sink_in_vadosesoil_n3.exterior_boundary=1013.4479278679979
	
	comp_objects_dict["degradation_reaction_sink_in_vadosesoil_n3"]=degradation_reaction_sink_in_vadosesoil_n3

	degradation_reaction_sink_in_rootsoil_n3=degradation_reaction_sink(constants,containingscenario,currentchemical,rootsoil_n3,comp_objects_dict)
	degradation_reaction_sink_in_rootsoil_n3.name="degradation_reaction_sink_in_rootsoil_n3"
	degradation_reaction_sink_in_rootsoil_n3.containingvolumeelementname="rootsoil_n3"
	degradation_reaction_sink_in_rootsoil_n3.parcel_name="n3"
	degradation_reaction_sink_in_rootsoil_n3.parcel_points="p9 p10 p14 p13"
	degradation_reaction_sink_in_rootsoil_n3.parcel_area=351265.0000001304
	degradation_reaction_sink_in_rootsoil_n3.exterior_boundary=1013.4479278679979
	
	comp_objects_dict["degradation_reaction_sink_in_rootsoil_n3"]=degradation_reaction_sink_in_rootsoil_n3

	degradation_reaction_sink_in_surfsoil_n3=degradation_reaction_sink(constants,containingscenario,currentchemical,surfsoil_n3,comp_objects_dict)
	degradation_reaction_sink_in_surfsoil_n3.name="degradation_reaction_sink_in_surfsoil_n3"
	degradation_reaction_sink_in_surfsoil_n3.containingvolumeelementname="surfsoil_n3"
	degradation_reaction_sink_in_surfsoil_n3.parcel_name="n3"
	degradation_reaction_sink_in_surfsoil_n3.parcel_points="p9 p10 p14 p13"
	degradation_reaction_sink_in_surfsoil_n3.parcel_area=351265.0000001304
	degradation_reaction_sink_in_surfsoil_n3.exterior_boundary=1013.4479278679979
	
	comp_objects_dict["degradation_reaction_sink_in_surfsoil_n3"]=degradation_reaction_sink_in_surfsoil_n3

	leaf_grasses_herbs_in_surfsoil_n3=leaf_grasses_herbs_in_grasses_herbs(constants,containingscenario,currentchemical,surfsoil_n3,comp_objects_dict)
	leaf_grasses_herbs_in_surfsoil_n3.name="leaf_grasses_herbs_in_surfsoil_n3"
	leaf_grasses_herbs_in_surfsoil_n3.containingvolumeelementname="surfsoil_n3"
	leaf_grasses_herbs_in_surfsoil_n3.parcel_name="n3"
	leaf_grasses_herbs_in_surfsoil_n3.parcel_points="p9 p10 p14 p13"
	leaf_grasses_herbs_in_surfsoil_n3.parcel_area=351265.0000001304
	leaf_grasses_herbs_in_surfsoil_n3.exterior_boundary=1013.4479278679979
	
	leaf_grasses_herbs_in_surfsoil_n3.associated_soil_comp=comp_objects_dict["soil_surface_in_surfsoil_n3"]

	comp_objects_dict["leaf_grasses_herbs_in_surfsoil_n3"]=leaf_grasses_herbs_in_surfsoil_n3

	soil_surface_in_surfsoil_n3.associated_leaf_comp=comp_objects_dict["leaf_grasses_herbs_in_surfsoil_n3"]

	comp_objects_dict["soil_surface_in_surfsoil_n3"]=soil_surface_in_surfsoil_n3

	leaf_particle_grasses_herbs_in_surfsoil_n3=leaf_particle_grasses_herbs_in_grasses_herbs(constants,containingscenario,currentchemical,surfsoil_n3,comp_objects_dict)
	leaf_particle_grasses_herbs_in_surfsoil_n3.name="leaf_particle_grasses_herbs_in_surfsoil_n3"
	leaf_particle_grasses_herbs_in_surfsoil_n3.containingvolumeelementname="surfsoil_n3"
	leaf_particle_grasses_herbs_in_surfsoil_n3.parcel_name="n3"
	leaf_particle_grasses_herbs_in_surfsoil_n3.parcel_points="p9 p10 p14 p13"
	leaf_particle_grasses_herbs_in_surfsoil_n3.parcel_area=351265.0000001304
	leaf_particle_grasses_herbs_in_surfsoil_n3.exterior_boundary=1013.4479278679979
	
	leaf_particle_grasses_herbs_in_surfsoil_n3.associated_soil_comp=comp_objects_dict["soil_surface_in_surfsoil_n3"]

	leaf_particle_grasses_herbs_in_surfsoil_n3.associated_leaf_comp=comp_objects_dict["leaf_grasses_herbs_in_surfsoil_n3"]

	comp_objects_dict["leaf_particle_grasses_herbs_in_surfsoil_n3"]=leaf_particle_grasses_herbs_in_surfsoil_n3

	stem_grasses_herbs_in_surfsoil_n3=stem_grasses_herbs_in_grasses_herbs(constants,containingscenario,currentchemical,surfsoil_n3,comp_objects_dict)
	stem_grasses_herbs_in_surfsoil_n3.name="stem_grasses_herbs_in_surfsoil_n3"
	stem_grasses_herbs_in_surfsoil_n3.containingvolumeelementname="surfsoil_n3"
	stem_grasses_herbs_in_surfsoil_n3.parcel_name="n3"
	stem_grasses_herbs_in_surfsoil_n3.parcel_points="p9 p10 p14 p13"
	stem_grasses_herbs_in_surfsoil_n3.parcel_area=351265.0000001304
	stem_grasses_herbs_in_surfsoil_n3.exterior_boundary=1013.4479278679979
	
	stem_grasses_herbs_in_surfsoil_n3.associated_soil_comp=comp_objects_dict["soil_surface_in_surfsoil_n3"]

	stem_grasses_herbs_in_surfsoil_n3.associated_leaf_comp=comp_objects_dict["leaf_grasses_herbs_in_surfsoil_n3"]

	comp_objects_dict["stem_grasses_herbs_in_surfsoil_n3"]=stem_grasses_herbs_in_surfsoil_n3

	soil_surface_in_surfsoil_n3.associated_stem_comp=comp_objects_dict["stem_grasses_herbs_in_surfsoil_n3"]

	comp_objects_dict["soil_surface_in_surfsoil_n3"]=soil_surface_in_surfsoil_n3

	leaf_grasses_herbs_in_surfsoil_n3.associated_stem_comp=comp_objects_dict["stem_grasses_herbs_in_surfsoil_n3"]

	comp_objects_dict["leaf_grasses_herbs_in_surfsoil_n3"]=leaf_grasses_herbs_in_surfsoil_n3

	root_grasses_herbs_in_surfsoil_n3=root_grasses_herbs_in_grasses_herbs(constants,containingscenario,currentchemical,surfsoil_n3,comp_objects_dict)
	root_grasses_herbs_in_surfsoil_n3.name="root_grasses_herbs_in_surfsoil_n3"
	root_grasses_herbs_in_surfsoil_n3.containingvolumeelementname="surfsoil_n3"
	root_grasses_herbs_in_surfsoil_n3.parcel_name="n3"
	root_grasses_herbs_in_surfsoil_n3.parcel_points="p9 p10 p14 p13"
	root_grasses_herbs_in_surfsoil_n3.parcel_area=351265.0000001304
	root_grasses_herbs_in_surfsoil_n3.exterior_boundary=1013.4479278679979
	
	root_grasses_herbs_in_surfsoil_n3.associated_soil_comp=comp_objects_dict["soil_root_zone_in_rootsoil_n3"]

	root_grasses_herbs_in_surfsoil_n3.associated_stem_comp=comp_objects_dict["stem_grasses_herbs_in_surfsoil_n3"]

	comp_objects_dict["root_grasses_herbs_in_surfsoil_n3"]=root_grasses_herbs_in_surfsoil_n3

	soil_root_zone_in_rootsoil_n3.associated_root_comp=comp_objects_dict["root_grasses_herbs_in_surfsoil_n3"]

	comp_objects_dict["soil_root_zone_in_rootsoil_n3"]=soil_root_zone_in_rootsoil_n3

	leaf_grasses_herbs_in_surfsoil_n3.associated_root_comp=comp_objects_dict["root_grasses_herbs_in_surfsoil_n3"]

	comp_objects_dict["leaf_grasses_herbs_in_surfsoil_n3"]=leaf_grasses_herbs_in_surfsoil_n3

	stem_grasses_herbs_in_surfsoil_n3.associated_root_comp=comp_objects_dict["root_grasses_herbs_in_surfsoil_n3"]

	comp_objects_dict["stem_grasses_herbs_in_surfsoil_n3"]=stem_grasses_herbs_in_surfsoil_n3

	degradation_reaction_sink_in_gw_n4=degradation_reaction_sink(constants,containingscenario,currentchemical,gw_n4,comp_objects_dict)
	degradation_reaction_sink_in_gw_n4.name="degradation_reaction_sink_in_gw_n4"
	degradation_reaction_sink_in_gw_n4.containingvolumeelementname="gw_n4"
	degradation_reaction_sink_in_gw_n4.parcel_name="n4"
	degradation_reaction_sink_in_gw_n4.parcel_points="p13 p14 p18 p17"
	degradation_reaction_sink_in_gw_n4.parcel_area=2041139.9999996647
	degradation_reaction_sink_in_gw_n4.exterior_boundary=3040.3486547433513
	
	comp_objects_dict["degradation_reaction_sink_in_gw_n4"]=degradation_reaction_sink_in_gw_n4

	degradation_reaction_sink_in_vadosesoil_n4=degradation_reaction_sink(constants,containingscenario,currentchemical,vadosesoil_n4,comp_objects_dict)
	degradation_reaction_sink_in_vadosesoil_n4.name="degradation_reaction_sink_in_vadosesoil_n4"
	degradation_reaction_sink_in_vadosesoil_n4.containingvolumeelementname="vadosesoil_n4"
	degradation_reaction_sink_in_vadosesoil_n4.parcel_name="n4"
	degradation_reaction_sink_in_vadosesoil_n4.parcel_points="p13 p14 p18 p17"
	degradation_reaction_sink_in_vadosesoil_n4.parcel_area=2041139.9999996647
	degradation_reaction_sink_in_vadosesoil_n4.exterior_boundary=3040.3486547433513
	
	comp_objects_dict["degradation_reaction_sink_in_vadosesoil_n4"]=degradation_reaction_sink_in_vadosesoil_n4

	degradation_reaction_sink_in_rootsoil_n4=degradation_reaction_sink(constants,containingscenario,currentchemical,rootsoil_n4,comp_objects_dict)
	degradation_reaction_sink_in_rootsoil_n4.name="degradation_reaction_sink_in_rootsoil_n4"
	degradation_reaction_sink_in_rootsoil_n4.containingvolumeelementname="rootsoil_n4"
	degradation_reaction_sink_in_rootsoil_n4.parcel_name="n4"
	degradation_reaction_sink_in_rootsoil_n4.parcel_points="p13 p14 p18 p17"
	degradation_reaction_sink_in_rootsoil_n4.parcel_area=2041139.9999996647
	degradation_reaction_sink_in_rootsoil_n4.exterior_boundary=3040.3486547433513
	
	comp_objects_dict["degradation_reaction_sink_in_rootsoil_n4"]=degradation_reaction_sink_in_rootsoil_n4

	degradation_reaction_sink_in_surfsoil_n4=degradation_reaction_sink(constants,containingscenario,currentchemical,surfsoil_n4,comp_objects_dict)
	degradation_reaction_sink_in_surfsoil_n4.name="degradation_reaction_sink_in_surfsoil_n4"
	degradation_reaction_sink_in_surfsoil_n4.containingvolumeelementname="surfsoil_n4"
	degradation_reaction_sink_in_surfsoil_n4.parcel_name="n4"
	degradation_reaction_sink_in_surfsoil_n4.parcel_points="p13 p14 p18 p17"
	degradation_reaction_sink_in_surfsoil_n4.parcel_area=2041139.9999996647
	degradation_reaction_sink_in_surfsoil_n4.exterior_boundary=3040.3486547433513
	
	comp_objects_dict["degradation_reaction_sink_in_surfsoil_n4"]=degradation_reaction_sink_in_surfsoil_n4

	leaf_coniferous_forest_in_surfsoil_n4=leaf_coniferous_forest_in_coniferous_forest(constants,containingscenario,currentchemical,surfsoil_n4,comp_objects_dict)
	leaf_coniferous_forest_in_surfsoil_n4.name="leaf_coniferous_forest_in_surfsoil_n4"
	leaf_coniferous_forest_in_surfsoil_n4.containingvolumeelementname="surfsoil_n4"
	leaf_coniferous_forest_in_surfsoil_n4.parcel_name="n4"
	leaf_coniferous_forest_in_surfsoil_n4.parcel_points="p13 p14 p18 p17"
	leaf_coniferous_forest_in_surfsoil_n4.parcel_area=2041139.9999996647
	leaf_coniferous_forest_in_surfsoil_n4.exterior_boundary=3040.3486547433513
	
	leaf_coniferous_forest_in_surfsoil_n4.associated_soil_comp=comp_objects_dict["soil_surface_in_surfsoil_n4"]

	comp_objects_dict["leaf_coniferous_forest_in_surfsoil_n4"]=leaf_coniferous_forest_in_surfsoil_n4

	soil_surface_in_surfsoil_n4.associated_leaf_comp=comp_objects_dict["leaf_coniferous_forest_in_surfsoil_n4"]

	comp_objects_dict["soil_surface_in_surfsoil_n4"]=soil_surface_in_surfsoil_n4

	leaf_particle_coniferous_forest_in_surfsoil_n4=leaf_particle_coniferous_forest_in_coniferous_forest(constants,containingscenario,currentchemical,surfsoil_n4,comp_objects_dict)
	leaf_particle_coniferous_forest_in_surfsoil_n4.name="leaf_particle_coniferous_forest_in_surfsoil_n4"
	leaf_particle_coniferous_forest_in_surfsoil_n4.containingvolumeelementname="surfsoil_n4"
	leaf_particle_coniferous_forest_in_surfsoil_n4.parcel_name="n4"
	leaf_particle_coniferous_forest_in_surfsoil_n4.parcel_points="p13 p14 p18 p17"
	leaf_particle_coniferous_forest_in_surfsoil_n4.parcel_area=2041139.9999996647
	leaf_particle_coniferous_forest_in_surfsoil_n4.exterior_boundary=3040.3486547433513
	
	leaf_particle_coniferous_forest_in_surfsoil_n4.associated_soil_comp=comp_objects_dict["soil_surface_in_surfsoil_n4"]

	leaf_particle_coniferous_forest_in_surfsoil_n4.associated_leaf_comp=comp_objects_dict["leaf_coniferous_forest_in_surfsoil_n4"]

	comp_objects_dict["leaf_particle_coniferous_forest_in_surfsoil_n4"]=leaf_particle_coniferous_forest_in_surfsoil_n4

	degradation_reaction_sink_in_gw_n5=degradation_reaction_sink(constants,containingscenario,currentchemical,gw_n5,comp_objects_dict)
	degradation_reaction_sink_in_gw_n5.name="degradation_reaction_sink_in_gw_n5"
	degradation_reaction_sink_in_gw_n5.containingvolumeelementname="gw_n5"
	degradation_reaction_sink_in_gw_n5.parcel_name="n5"
	degradation_reaction_sink_in_gw_n5.parcel_points="p17 p18 p22 p21"
	degradation_reaction_sink_in_gw_n5.parcel_area=6693049.999999348
	degradation_reaction_sink_in_gw_n5.exterior_boundary=6817.244510421856
	
	comp_objects_dict["degradation_reaction_sink_in_gw_n5"]=degradation_reaction_sink_in_gw_n5

	degradation_reaction_sink_in_vadosesoil_n5=degradation_reaction_sink(constants,containingscenario,currentchemical,vadosesoil_n5,comp_objects_dict)
	degradation_reaction_sink_in_vadosesoil_n5.name="degradation_reaction_sink_in_vadosesoil_n5"
	degradation_reaction_sink_in_vadosesoil_n5.containingvolumeelementname="vadosesoil_n5"
	degradation_reaction_sink_in_vadosesoil_n5.parcel_name="n5"
	degradation_reaction_sink_in_vadosesoil_n5.parcel_points="p17 p18 p22 p21"
	degradation_reaction_sink_in_vadosesoil_n5.parcel_area=6693049.999999348
	degradation_reaction_sink_in_vadosesoil_n5.exterior_boundary=6817.244510421856
	
	comp_objects_dict["degradation_reaction_sink_in_vadosesoil_n5"]=degradation_reaction_sink_in_vadosesoil_n5

	degradation_reaction_sink_in_rootsoil_n5=degradation_reaction_sink(constants,containingscenario,currentchemical,rootsoil_n5,comp_objects_dict)
	degradation_reaction_sink_in_rootsoil_n5.name="degradation_reaction_sink_in_rootsoil_n5"
	degradation_reaction_sink_in_rootsoil_n5.containingvolumeelementname="rootsoil_n5"
	degradation_reaction_sink_in_rootsoil_n5.parcel_name="n5"
	degradation_reaction_sink_in_rootsoil_n5.parcel_points="p17 p18 p22 p21"
	degradation_reaction_sink_in_rootsoil_n5.parcel_area=6693049.999999348
	degradation_reaction_sink_in_rootsoil_n5.exterior_boundary=6817.244510421856
	
	comp_objects_dict["degradation_reaction_sink_in_rootsoil_n5"]=degradation_reaction_sink_in_rootsoil_n5

	degradation_reaction_sink_in_surfsoil_n5=degradation_reaction_sink(constants,containingscenario,currentchemical,surfsoil_n5,comp_objects_dict)
	degradation_reaction_sink_in_surfsoil_n5.name="degradation_reaction_sink_in_surfsoil_n5"
	degradation_reaction_sink_in_surfsoil_n5.containingvolumeelementname="surfsoil_n5"
	degradation_reaction_sink_in_surfsoil_n5.parcel_name="n5"
	degradation_reaction_sink_in_surfsoil_n5.parcel_points="p17 p18 p22 p21"
	degradation_reaction_sink_in_surfsoil_n5.parcel_area=6693049.999999348
	degradation_reaction_sink_in_surfsoil_n5.exterior_boundary=6817.244510421856
	
	comp_objects_dict["degradation_reaction_sink_in_surfsoil_n5"]=degradation_reaction_sink_in_surfsoil_n5

	leaf_coniferous_forest_in_surfsoil_n5=leaf_coniferous_forest_in_coniferous_forest(constants,containingscenario,currentchemical,surfsoil_n5,comp_objects_dict)
	leaf_coniferous_forest_in_surfsoil_n5.name="leaf_coniferous_forest_in_surfsoil_n5"
	leaf_coniferous_forest_in_surfsoil_n5.containingvolumeelementname="surfsoil_n5"
	leaf_coniferous_forest_in_surfsoil_n5.parcel_name="n5"
	leaf_coniferous_forest_in_surfsoil_n5.parcel_points="p17 p18 p22 p21"
	leaf_coniferous_forest_in_surfsoil_n5.parcel_area=6693049.999999348
	leaf_coniferous_forest_in_surfsoil_n5.exterior_boundary=6817.244510421856
	
	leaf_coniferous_forest_in_surfsoil_n5.associated_soil_comp=comp_objects_dict["soil_surface_in_surfsoil_n5"]

	comp_objects_dict["leaf_coniferous_forest_in_surfsoil_n5"]=leaf_coniferous_forest_in_surfsoil_n5

	soil_surface_in_surfsoil_n5.associated_leaf_comp=comp_objects_dict["leaf_coniferous_forest_in_surfsoil_n5"]

	comp_objects_dict["soil_surface_in_surfsoil_n5"]=soil_surface_in_surfsoil_n5

	leaf_particle_coniferous_forest_in_surfsoil_n5=leaf_particle_coniferous_forest_in_coniferous_forest(constants,containingscenario,currentchemical,surfsoil_n5,comp_objects_dict)
	leaf_particle_coniferous_forest_in_surfsoil_n5.name="leaf_particle_coniferous_forest_in_surfsoil_n5"
	leaf_particle_coniferous_forest_in_surfsoil_n5.containingvolumeelementname="surfsoil_n5"
	leaf_particle_coniferous_forest_in_surfsoil_n5.parcel_name="n5"
	leaf_particle_coniferous_forest_in_surfsoil_n5.parcel_points="p17 p18 p22 p21"
	leaf_particle_coniferous_forest_in_surfsoil_n5.parcel_area=6693049.999999348
	leaf_particle_coniferous_forest_in_surfsoil_n5.exterior_boundary=6817.244510421856
	
	leaf_particle_coniferous_forest_in_surfsoil_n5.associated_soil_comp=comp_objects_dict["soil_surface_in_surfsoil_n5"]

	leaf_particle_coniferous_forest_in_surfsoil_n5.associated_leaf_comp=comp_objects_dict["leaf_coniferous_forest_in_surfsoil_n5"]

	comp_objects_dict["leaf_particle_coniferous_forest_in_surfsoil_n5"]=leaf_particle_coniferous_forest_in_surfsoil_n5

	degradation_reaction_sink_in_gw_s1=degradation_reaction_sink(constants,containingscenario,currentchemical,gw_s1,comp_objects_dict)
	degradation_reaction_sink_in_gw_s1.name="degradation_reaction_sink_in_gw_s1"
	degradation_reaction_sink_in_gw_s1.containingvolumeelementname="gw_s1"
	degradation_reaction_sink_in_gw_s1.parcel_name="s1"
	degradation_reaction_sink_in_gw_s1.parcel_points="p4 p3 p8 p7"
	degradation_reaction_sink_in_gw_s1.parcel_area=58445.624999993015
	degradation_reaction_sink_in_gw_s1.exterior_boundary=380.0435818429189
	
	comp_objects_dict["degradation_reaction_sink_in_gw_s1"]=degradation_reaction_sink_in_gw_s1

	degradation_reaction_sink_in_vadosesoil_s1=degradation_reaction_sink(constants,containingscenario,currentchemical,vadosesoil_s1,comp_objects_dict)
	degradation_reaction_sink_in_vadosesoil_s1.name="degradation_reaction_sink_in_vadosesoil_s1"
	degradation_reaction_sink_in_vadosesoil_s1.containingvolumeelementname="vadosesoil_s1"
	degradation_reaction_sink_in_vadosesoil_s1.parcel_name="s1"
	degradation_reaction_sink_in_vadosesoil_s1.parcel_points="p4 p3 p8 p7"
	degradation_reaction_sink_in_vadosesoil_s1.parcel_area=58445.624999993015
	degradation_reaction_sink_in_vadosesoil_s1.exterior_boundary=380.0435818429189
	
	comp_objects_dict["degradation_reaction_sink_in_vadosesoil_s1"]=degradation_reaction_sink_in_vadosesoil_s1

	degradation_reaction_sink_in_rootsoil_s1=degradation_reaction_sink(constants,containingscenario,currentchemical,rootsoil_s1,comp_objects_dict)
	degradation_reaction_sink_in_rootsoil_s1.name="degradation_reaction_sink_in_rootsoil_s1"
	degradation_reaction_sink_in_rootsoil_s1.containingvolumeelementname="rootsoil_s1"
	degradation_reaction_sink_in_rootsoil_s1.parcel_name="s1"
	degradation_reaction_sink_in_rootsoil_s1.parcel_points="p4 p3 p8 p7"
	degradation_reaction_sink_in_rootsoil_s1.parcel_area=58445.624999993015
	degradation_reaction_sink_in_rootsoil_s1.exterior_boundary=380.0435818429189
	
	comp_objects_dict["degradation_reaction_sink_in_rootsoil_s1"]=degradation_reaction_sink_in_rootsoil_s1

	degradation_reaction_sink_in_surfsoil_s1=degradation_reaction_sink(constants,containingscenario,currentchemical,surfsoil_s1,comp_objects_dict)
	degradation_reaction_sink_in_surfsoil_s1.name="degradation_reaction_sink_in_surfsoil_s1"
	degradation_reaction_sink_in_surfsoil_s1.containingvolumeelementname="surfsoil_s1"
	degradation_reaction_sink_in_surfsoil_s1.parcel_name="s1"
	degradation_reaction_sink_in_surfsoil_s1.parcel_points="p4 p3 p8 p7"
	degradation_reaction_sink_in_surfsoil_s1.parcel_area=58445.624999993015
	degradation_reaction_sink_in_surfsoil_s1.exterior_boundary=380.0435818429189
	
	comp_objects_dict["degradation_reaction_sink_in_surfsoil_s1"]=degradation_reaction_sink_in_surfsoil_s1

	leaf_grasses_herbs_in_surfsoil_s1=leaf_grasses_herbs_in_grasses_herbs(constants,containingscenario,currentchemical,surfsoil_s1,comp_objects_dict)
	leaf_grasses_herbs_in_surfsoil_s1.name="leaf_grasses_herbs_in_surfsoil_s1"
	leaf_grasses_herbs_in_surfsoil_s1.containingvolumeelementname="surfsoil_s1"
	leaf_grasses_herbs_in_surfsoil_s1.parcel_name="s1"
	leaf_grasses_herbs_in_surfsoil_s1.parcel_points="p4 p3 p8 p7"
	leaf_grasses_herbs_in_surfsoil_s1.parcel_area=58445.624999993015
	leaf_grasses_herbs_in_surfsoil_s1.exterior_boundary=380.0435818429189
	
	leaf_grasses_herbs_in_surfsoil_s1.associated_soil_comp=comp_objects_dict["soil_surface_in_surfsoil_s1"]

	comp_objects_dict["leaf_grasses_herbs_in_surfsoil_s1"]=leaf_grasses_herbs_in_surfsoil_s1

	soil_surface_in_surfsoil_s1.associated_leaf_comp=comp_objects_dict["leaf_grasses_herbs_in_surfsoil_s1"]

	comp_objects_dict["soil_surface_in_surfsoil_s1"]=soil_surface_in_surfsoil_s1

	leaf_particle_grasses_herbs_in_surfsoil_s1=leaf_particle_grasses_herbs_in_grasses_herbs(constants,containingscenario,currentchemical,surfsoil_s1,comp_objects_dict)
	leaf_particle_grasses_herbs_in_surfsoil_s1.name="leaf_particle_grasses_herbs_in_surfsoil_s1"
	leaf_particle_grasses_herbs_in_surfsoil_s1.containingvolumeelementname="surfsoil_s1"
	leaf_particle_grasses_herbs_in_surfsoil_s1.parcel_name="s1"
	leaf_particle_grasses_herbs_in_surfsoil_s1.parcel_points="p4 p3 p8 p7"
	leaf_particle_grasses_herbs_in_surfsoil_s1.parcel_area=58445.624999993015
	leaf_particle_grasses_herbs_in_surfsoil_s1.exterior_boundary=380.0435818429189
	
	leaf_particle_grasses_herbs_in_surfsoil_s1.associated_soil_comp=comp_objects_dict["soil_surface_in_surfsoil_s1"]

	leaf_particle_grasses_herbs_in_surfsoil_s1.associated_leaf_comp=comp_objects_dict["leaf_grasses_herbs_in_surfsoil_s1"]

	comp_objects_dict["leaf_particle_grasses_herbs_in_surfsoil_s1"]=leaf_particle_grasses_herbs_in_surfsoil_s1

	stem_grasses_herbs_in_surfsoil_s1=stem_grasses_herbs_in_grasses_herbs(constants,containingscenario,currentchemical,surfsoil_s1,comp_objects_dict)
	stem_grasses_herbs_in_surfsoil_s1.name="stem_grasses_herbs_in_surfsoil_s1"
	stem_grasses_herbs_in_surfsoil_s1.containingvolumeelementname="surfsoil_s1"
	stem_grasses_herbs_in_surfsoil_s1.parcel_name="s1"
	stem_grasses_herbs_in_surfsoil_s1.parcel_points="p4 p3 p8 p7"
	stem_grasses_herbs_in_surfsoil_s1.parcel_area=58445.624999993015
	stem_grasses_herbs_in_surfsoil_s1.exterior_boundary=380.0435818429189
	
	stem_grasses_herbs_in_surfsoil_s1.associated_soil_comp=comp_objects_dict["soil_surface_in_surfsoil_s1"]

	stem_grasses_herbs_in_surfsoil_s1.associated_leaf_comp=comp_objects_dict["leaf_grasses_herbs_in_surfsoil_s1"]

	comp_objects_dict["stem_grasses_herbs_in_surfsoil_s1"]=stem_grasses_herbs_in_surfsoil_s1

	soil_surface_in_surfsoil_s1.associated_stem_comp=comp_objects_dict["stem_grasses_herbs_in_surfsoil_s1"]

	comp_objects_dict["soil_surface_in_surfsoil_s1"]=soil_surface_in_surfsoil_s1

	leaf_grasses_herbs_in_surfsoil_s1.associated_stem_comp=comp_objects_dict["stem_grasses_herbs_in_surfsoil_s1"]

	comp_objects_dict["leaf_grasses_herbs_in_surfsoil_s1"]=leaf_grasses_herbs_in_surfsoil_s1

	root_grasses_herbs_in_surfsoil_s1=root_grasses_herbs_in_grasses_herbs(constants,containingscenario,currentchemical,surfsoil_s1,comp_objects_dict)
	root_grasses_herbs_in_surfsoil_s1.name="root_grasses_herbs_in_surfsoil_s1"
	root_grasses_herbs_in_surfsoil_s1.containingvolumeelementname="surfsoil_s1"
	root_grasses_herbs_in_surfsoil_s1.parcel_name="s1"
	root_grasses_herbs_in_surfsoil_s1.parcel_points="p4 p3 p8 p7"
	root_grasses_herbs_in_surfsoil_s1.parcel_area=58445.624999993015
	root_grasses_herbs_in_surfsoil_s1.exterior_boundary=380.0435818429189
	
	root_grasses_herbs_in_surfsoil_s1.associated_soil_comp=comp_objects_dict["soil_root_zone_in_rootsoil_s1"]

	root_grasses_herbs_in_surfsoil_s1.associated_stem_comp=comp_objects_dict["stem_grasses_herbs_in_surfsoil_s1"]

	comp_objects_dict["root_grasses_herbs_in_surfsoil_s1"]=root_grasses_herbs_in_surfsoil_s1

	soil_root_zone_in_rootsoil_s1.associated_root_comp=comp_objects_dict["root_grasses_herbs_in_surfsoil_s1"]

	comp_objects_dict["soil_root_zone_in_rootsoil_s1"]=soil_root_zone_in_rootsoil_s1

	leaf_grasses_herbs_in_surfsoil_s1.associated_root_comp=comp_objects_dict["root_grasses_herbs_in_surfsoil_s1"]

	comp_objects_dict["leaf_grasses_herbs_in_surfsoil_s1"]=leaf_grasses_herbs_in_surfsoil_s1

	stem_grasses_herbs_in_surfsoil_s1.associated_root_comp=comp_objects_dict["root_grasses_herbs_in_surfsoil_s1"]

	comp_objects_dict["stem_grasses_herbs_in_surfsoil_s1"]=stem_grasses_herbs_in_surfsoil_s1

	degradation_reaction_sink_in_gw_s4=degradation_reaction_sink(constants,containingscenario,currentchemical,gw_s4,comp_objects_dict)
	degradation_reaction_sink_in_gw_s4.name="degradation_reaction_sink_in_gw_s4"
	degradation_reaction_sink_in_gw_s4.containingvolumeelementname="gw_s4"
	degradation_reaction_sink_in_gw_s4.parcel_name="s4"
	degradation_reaction_sink_in_gw_s4.parcel_points="p14 p16 p20 p18"
	degradation_reaction_sink_in_gw_s4.parcel_area=2041139.9999996647
	degradation_reaction_sink_in_gw_s4.exterior_boundary=3040.3486547433513
	
	comp_objects_dict["degradation_reaction_sink_in_gw_s4"]=degradation_reaction_sink_in_gw_s4

	degradation_reaction_sink_in_vadosesoil_s4=degradation_reaction_sink(constants,containingscenario,currentchemical,vadosesoil_s4,comp_objects_dict)
	degradation_reaction_sink_in_vadosesoil_s4.name="degradation_reaction_sink_in_vadosesoil_s4"
	degradation_reaction_sink_in_vadosesoil_s4.containingvolumeelementname="vadosesoil_s4"
	degradation_reaction_sink_in_vadosesoil_s4.parcel_name="s4"
	degradation_reaction_sink_in_vadosesoil_s4.parcel_points="p14 p16 p20 p18"
	degradation_reaction_sink_in_vadosesoil_s4.parcel_area=2041139.9999996647
	degradation_reaction_sink_in_vadosesoil_s4.exterior_boundary=3040.3486547433513
	
	comp_objects_dict["degradation_reaction_sink_in_vadosesoil_s4"]=degradation_reaction_sink_in_vadosesoil_s4

	degradation_reaction_sink_in_rootsoil_s4=degradation_reaction_sink(constants,containingscenario,currentchemical,rootsoil_s4,comp_objects_dict)
	degradation_reaction_sink_in_rootsoil_s4.name="degradation_reaction_sink_in_rootsoil_s4"
	degradation_reaction_sink_in_rootsoil_s4.containingvolumeelementname="rootsoil_s4"
	degradation_reaction_sink_in_rootsoil_s4.parcel_name="s4"
	degradation_reaction_sink_in_rootsoil_s4.parcel_points="p14 p16 p20 p18"
	degradation_reaction_sink_in_rootsoil_s4.parcel_area=2041139.9999996647
	degradation_reaction_sink_in_rootsoil_s4.exterior_boundary=3040.3486547433513
	
	comp_objects_dict["degradation_reaction_sink_in_rootsoil_s4"]=degradation_reaction_sink_in_rootsoil_s4

	degradation_reaction_sink_in_surfsoil_s4=degradation_reaction_sink(constants,containingscenario,currentchemical,surfsoil_s4,comp_objects_dict)
	degradation_reaction_sink_in_surfsoil_s4.name="degradation_reaction_sink_in_surfsoil_s4"
	degradation_reaction_sink_in_surfsoil_s4.containingvolumeelementname="surfsoil_s4"
	degradation_reaction_sink_in_surfsoil_s4.parcel_name="s4"
	degradation_reaction_sink_in_surfsoil_s4.parcel_points="p14 p16 p20 p18"
	degradation_reaction_sink_in_surfsoil_s4.parcel_area=2041139.9999996647
	degradation_reaction_sink_in_surfsoil_s4.exterior_boundary=3040.3486547433513
	
	comp_objects_dict["degradation_reaction_sink_in_surfsoil_s4"]=degradation_reaction_sink_in_surfsoil_s4

	leaf_coniferous_forest_in_surfsoil_s4=leaf_coniferous_forest_in_coniferous_forest(constants,containingscenario,currentchemical,surfsoil_s4,comp_objects_dict)
	leaf_coniferous_forest_in_surfsoil_s4.name="leaf_coniferous_forest_in_surfsoil_s4"
	leaf_coniferous_forest_in_surfsoil_s4.containingvolumeelementname="surfsoil_s4"
	leaf_coniferous_forest_in_surfsoil_s4.parcel_name="s4"
	leaf_coniferous_forest_in_surfsoil_s4.parcel_points="p14 p16 p20 p18"
	leaf_coniferous_forest_in_surfsoil_s4.parcel_area=2041139.9999996647
	leaf_coniferous_forest_in_surfsoil_s4.exterior_boundary=3040.3486547433513
	
	leaf_coniferous_forest_in_surfsoil_s4.associated_soil_comp=comp_objects_dict["soil_surface_in_surfsoil_s4"]

	comp_objects_dict["leaf_coniferous_forest_in_surfsoil_s4"]=leaf_coniferous_forest_in_surfsoil_s4

	soil_surface_in_surfsoil_s4.associated_leaf_comp=comp_objects_dict["leaf_coniferous_forest_in_surfsoil_s4"]

	comp_objects_dict["soil_surface_in_surfsoil_s4"]=soil_surface_in_surfsoil_s4

	leaf_particle_coniferous_forest_in_surfsoil_s4=leaf_particle_coniferous_forest_in_coniferous_forest(constants,containingscenario,currentchemical,surfsoil_s4,comp_objects_dict)
	leaf_particle_coniferous_forest_in_surfsoil_s4.name="leaf_particle_coniferous_forest_in_surfsoil_s4"
	leaf_particle_coniferous_forest_in_surfsoil_s4.containingvolumeelementname="surfsoil_s4"
	leaf_particle_coniferous_forest_in_surfsoil_s4.parcel_name="s4"
	leaf_particle_coniferous_forest_in_surfsoil_s4.parcel_points="p14 p16 p20 p18"
	leaf_particle_coniferous_forest_in_surfsoil_s4.parcel_area=2041139.9999996647
	leaf_particle_coniferous_forest_in_surfsoil_s4.exterior_boundary=3040.3486547433513
	
	leaf_particle_coniferous_forest_in_surfsoil_s4.associated_soil_comp=comp_objects_dict["soil_surface_in_surfsoil_s4"]

	leaf_particle_coniferous_forest_in_surfsoil_s4.associated_leaf_comp=comp_objects_dict["leaf_coniferous_forest_in_surfsoil_s4"]

	comp_objects_dict["leaf_particle_coniferous_forest_in_surfsoil_s4"]=leaf_particle_coniferous_forest_in_surfsoil_s4

	degradation_reaction_sink_in_gw_s5=degradation_reaction_sink(constants,containingscenario,currentchemical,gw_s5,comp_objects_dict)
	degradation_reaction_sink_in_gw_s5.name="degradation_reaction_sink_in_gw_s5"
	degradation_reaction_sink_in_gw_s5.containingvolumeelementname="gw_s5"
	degradation_reaction_sink_in_gw_s5.parcel_name="s5"
	degradation_reaction_sink_in_gw_s5.parcel_points="p18 p20 p24 p22"
	degradation_reaction_sink_in_gw_s5.parcel_area=6693049.999999348
	degradation_reaction_sink_in_gw_s5.exterior_boundary=6817.244510421856
	
	comp_objects_dict["degradation_reaction_sink_in_gw_s5"]=degradation_reaction_sink_in_gw_s5

	degradation_reaction_sink_in_vadosesoil_s5=degradation_reaction_sink(constants,containingscenario,currentchemical,vadosesoil_s5,comp_objects_dict)
	degradation_reaction_sink_in_vadosesoil_s5.name="degradation_reaction_sink_in_vadosesoil_s5"
	degradation_reaction_sink_in_vadosesoil_s5.containingvolumeelementname="vadosesoil_s5"
	degradation_reaction_sink_in_vadosesoil_s5.parcel_name="s5"
	degradation_reaction_sink_in_vadosesoil_s5.parcel_points="p18 p20 p24 p22"
	degradation_reaction_sink_in_vadosesoil_s5.parcel_area=6693049.999999348
	degradation_reaction_sink_in_vadosesoil_s5.exterior_boundary=6817.244510421856
	
	comp_objects_dict["degradation_reaction_sink_in_vadosesoil_s5"]=degradation_reaction_sink_in_vadosesoil_s5

	degradation_reaction_sink_in_rootsoil_s5=degradation_reaction_sink(constants,containingscenario,currentchemical,rootsoil_s5,comp_objects_dict)
	degradation_reaction_sink_in_rootsoil_s5.name="degradation_reaction_sink_in_rootsoil_s5"
	degradation_reaction_sink_in_rootsoil_s5.containingvolumeelementname="rootsoil_s5"
	degradation_reaction_sink_in_rootsoil_s5.parcel_name="s5"
	degradation_reaction_sink_in_rootsoil_s5.parcel_points="p18 p20 p24 p22"
	degradation_reaction_sink_in_rootsoil_s5.parcel_area=6693049.999999348
	degradation_reaction_sink_in_rootsoil_s5.exterior_boundary=6817.244510421856
	
	comp_objects_dict["degradation_reaction_sink_in_rootsoil_s5"]=degradation_reaction_sink_in_rootsoil_s5

	degradation_reaction_sink_in_surfsoil_s5=degradation_reaction_sink(constants,containingscenario,currentchemical,surfsoil_s5,comp_objects_dict)
	degradation_reaction_sink_in_surfsoil_s5.name="degradation_reaction_sink_in_surfsoil_s5"
	degradation_reaction_sink_in_surfsoil_s5.containingvolumeelementname="surfsoil_s5"
	degradation_reaction_sink_in_surfsoil_s5.parcel_name="s5"
	degradation_reaction_sink_in_surfsoil_s5.parcel_points="p18 p20 p24 p22"
	degradation_reaction_sink_in_surfsoil_s5.parcel_area=6693049.999999348
	degradation_reaction_sink_in_surfsoil_s5.exterior_boundary=6817.244510421856
	
	comp_objects_dict["degradation_reaction_sink_in_surfsoil_s5"]=degradation_reaction_sink_in_surfsoil_s5

	leaf_coniferous_forest_in_surfsoil_s5=leaf_coniferous_forest_in_coniferous_forest(constants,containingscenario,currentchemical,surfsoil_s5,comp_objects_dict)
	leaf_coniferous_forest_in_surfsoil_s5.name="leaf_coniferous_forest_in_surfsoil_s5"
	leaf_coniferous_forest_in_surfsoil_s5.containingvolumeelementname="surfsoil_s5"
	leaf_coniferous_forest_in_surfsoil_s5.parcel_name="s5"
	leaf_coniferous_forest_in_surfsoil_s5.parcel_points="p18 p20 p24 p22"
	leaf_coniferous_forest_in_surfsoil_s5.parcel_area=6693049.999999348
	leaf_coniferous_forest_in_surfsoil_s5.exterior_boundary=6817.244510421856
	
	leaf_coniferous_forest_in_surfsoil_s5.associated_soil_comp=comp_objects_dict["soil_surface_in_surfsoil_s5"]

	comp_objects_dict["leaf_coniferous_forest_in_surfsoil_s5"]=leaf_coniferous_forest_in_surfsoil_s5

	soil_surface_in_surfsoil_s5.associated_leaf_comp=comp_objects_dict["leaf_coniferous_forest_in_surfsoil_s5"]

	comp_objects_dict["soil_surface_in_surfsoil_s5"]=soil_surface_in_surfsoil_s5

	leaf_particle_coniferous_forest_in_surfsoil_s5=leaf_particle_coniferous_forest_in_coniferous_forest(constants,containingscenario,currentchemical,surfsoil_s5,comp_objects_dict)
	leaf_particle_coniferous_forest_in_surfsoil_s5.name="leaf_particle_coniferous_forest_in_surfsoil_s5"
	leaf_particle_coniferous_forest_in_surfsoil_s5.containingvolumeelementname="surfsoil_s5"
	leaf_particle_coniferous_forest_in_surfsoil_s5.parcel_name="s5"
	leaf_particle_coniferous_forest_in_surfsoil_s5.parcel_points="p18 p20 p24 p22"
	leaf_particle_coniferous_forest_in_surfsoil_s5.parcel_area=6693049.999999348
	leaf_particle_coniferous_forest_in_surfsoil_s5.exterior_boundary=6817.244510421856
	
	leaf_particle_coniferous_forest_in_surfsoil_s5.associated_soil_comp=comp_objects_dict["soil_surface_in_surfsoil_s5"]

	leaf_particle_coniferous_forest_in_surfsoil_s5.associated_leaf_comp=comp_objects_dict["leaf_coniferous_forest_in_surfsoil_s5"]

	comp_objects_dict["leaf_particle_coniferous_forest_in_surfsoil_s5"]=leaf_particle_coniferous_forest_in_surfsoil_s5

	sink_in_sink_for_air_in_air_source=advection_sink(constants,containingscenario,currentchemical,air_source,comp_objects_dict)
	sink_in_sink_for_air_in_air_source.name="sink_in_sink_for_air_in_air_source"
	sink_in_sink_for_air_in_air_source.containingvolumeelementname="air_source"
	sink_in_sink_for_air_in_air_source.parcel_name="source"
	sink_in_sink_for_air_in_air_source.parcel_points="p1 p2 p3 p4 p5"
	sink_in_sink_for_air_in_air_source.parcel_area=62500.0
	sink_in_sink_for_air_in_air_source.exterior_boundary=750.0
	sink_in_sink_for_air_in_air_source.category="sink | abiotic | air | air - default"
	
	comp_objects_dict["sink_in_sink_for_air_in_air_source"]=sink_in_sink_for_air_in_air_source

	
	sink_in_sink_for_air_in_upperair_source=advection_sink(constants,containingscenario,currentchemical,upperair_source,comp_objects_dict)
	sink_in_sink_for_air_in_upperair_source.name="sink_in_sink_for_air_in_upperair_source"
	sink_in_sink_for_air_in_upperair_source.containingvolumeelementname="upperair_source"
	sink_in_sink_for_air_in_upperair_source.parcel_name="source"
	sink_in_sink_for_air_in_upperair_source.parcel_points="p1 p2 p3 p4 p5"
	sink_in_sink_for_air_in_upperair_source.parcel_area=62500.0
	sink_in_sink_for_air_in_upperair_source.exterior_boundary=750.0
	sink_in_sink_for_air_in_upperair_source.category="sink | abiotic | air | air - default"
	
	comp_objects_dict["sink_in_sink_for_air_in_upperair_source"]=sink_in_sink_for_air_in_upperair_source

	
	sink_in_sink_for_air_in_air_n1=advection_sink(constants,containingscenario,currentchemical,air_n1,comp_objects_dict)
	sink_in_sink_for_air_in_air_n1.name="sink_in_sink_for_air_in_air_n1"
	sink_in_sink_for_air_in_air_n1.containingvolumeelementname="air_n1"
	sink_in_sink_for_air_in_air_n1.parcel_name="n1"
	sink_in_sink_for_air_in_air_n1.parcel_points="p5 p4 p7 p6"
	sink_in_sink_for_air_in_air_n1.parcel_area=58445.624999993015
	sink_in_sink_for_air_in_air_n1.exterior_boundary=380.0435818429189
	sink_in_sink_for_air_in_air_n1.category="sink | abiotic | air | air - default"
	
	comp_objects_dict["sink_in_sink_for_air_in_air_n1"]=sink_in_sink_for_air_in_air_n1

	
	sink_in_sink_for_air_in_air_n6=advection_sink(constants,containingscenario,currentchemical,air_n6,comp_objects_dict)
	sink_in_sink_for_air_in_air_n6.name="sink_in_sink_for_air_in_air_n6"
	sink_in_sink_for_air_in_air_n6.containingvolumeelementname="air_n6"
	sink_in_sink_for_air_in_air_n6.parcel_name="n6"
	sink_in_sink_for_air_in_air_n6.parcel_points="p6 p7 p26 p25"
	sink_in_sink_for_air_in_air_n6.parcel_area=40633.00000000745
	sink_in_sink_for_air_in_air_n6.exterior_boundary=202.6895855736298
	sink_in_sink_for_air_in_air_n6.category="sink | abiotic | air | air - default"
	
	comp_objects_dict["sink_in_sink_for_air_in_air_n6"]=sink_in_sink_for_air_in_air_n6

	
	sink_in_sink_for_air_in_air_n7=advection_sink(constants,containingscenario,currentchemical,air_n7,comp_objects_dict)
	sink_in_sink_for_air_in_air_n7.name="sink_in_sink_for_air_in_air_n7"
	sink_in_sink_for_air_in_air_n7.containingvolumeelementname="air_n7"
	sink_in_sink_for_air_in_air_n7.parcel_name="n7"
	sink_in_sink_for_air_in_air_n7.parcel_points="p25 p26 p10 p9"
	sink_in_sink_for_air_in_air_n7.parcel_area=73291.50000005029
	sink_in_sink_for_air_in_air_n7.exterior_boundary=304.035190232991
	sink_in_sink_for_air_in_air_n7.category="sink | abiotic | air | air - default"
	
	comp_objects_dict["sink_in_sink_for_air_in_air_n7"]=sink_in_sink_for_air_in_air_n7

	
	sink_in_sink_for_air_in_air_n3=advection_sink(constants,containingscenario,currentchemical,air_n3,comp_objects_dict)
	sink_in_sink_for_air_in_air_n3.name="sink_in_sink_for_air_in_air_n3"
	sink_in_sink_for_air_in_air_n3.containingvolumeelementname="air_n3"
	sink_in_sink_for_air_in_air_n3.parcel_name="n3"
	sink_in_sink_for_air_in_air_n3.parcel_points="p9 p10 p14 p13"
	sink_in_sink_for_air_in_air_n3.parcel_area=351265.0000001304
	sink_in_sink_for_air_in_air_n3.exterior_boundary=1013.4479278679979
	sink_in_sink_for_air_in_air_n3.category="sink | abiotic | air | air - default"
	
	comp_objects_dict["sink_in_sink_for_air_in_air_n3"]=sink_in_sink_for_air_in_air_n3

	
	sink_in_sink_for_air_in_air_n4=advection_sink(constants,containingscenario,currentchemical,air_n4,comp_objects_dict)
	sink_in_sink_for_air_in_air_n4.name="sink_in_sink_for_air_in_air_n4"
	sink_in_sink_for_air_in_air_n4.containingvolumeelementname="air_n4"
	sink_in_sink_for_air_in_air_n4.parcel_name="n4"
	sink_in_sink_for_air_in_air_n4.parcel_points="p13 p14 p18 p17"
	sink_in_sink_for_air_in_air_n4.parcel_area=2041139.9999996647
	sink_in_sink_for_air_in_air_n4.exterior_boundary=3040.3486547433513
	sink_in_sink_for_air_in_air_n4.category="sink | abiotic | air | air - default"
	
	comp_objects_dict["sink_in_sink_for_air_in_air_n4"]=sink_in_sink_for_air_in_air_n4

	
	sink_in_sink_for_air_in_air_n5=advection_sink(constants,containingscenario,currentchemical,air_n5,comp_objects_dict)
	sink_in_sink_for_air_in_air_n5.name="sink_in_sink_for_air_in_air_n5"
	sink_in_sink_for_air_in_air_n5.containingvolumeelementname="air_n5"
	sink_in_sink_for_air_in_air_n5.parcel_name="n5"
	sink_in_sink_for_air_in_air_n5.parcel_points="p17 p18 p22 p21"
	sink_in_sink_for_air_in_air_n5.parcel_area=6693049.999999348
	sink_in_sink_for_air_in_air_n5.exterior_boundary=6817.244510421856
	sink_in_sink_for_air_in_air_n5.category="sink | abiotic | air | air - default"
	
	comp_objects_dict["sink_in_sink_for_air_in_air_n5"]=sink_in_sink_for_air_in_air_n5

	
	sink_in_sink_for_air_in_air_s1=advection_sink(constants,containingscenario,currentchemical,air_s1,comp_objects_dict)
	sink_in_sink_for_air_in_air_s1.name="sink_in_sink_for_air_in_air_s1"
	sink_in_sink_for_air_in_air_s1.containingvolumeelementname="air_s1"
	sink_in_sink_for_air_in_air_s1.parcel_name="s1"
	sink_in_sink_for_air_in_air_s1.parcel_points="p4 p3 p8 p7"
	sink_in_sink_for_air_in_air_s1.parcel_area=58445.624999993015
	sink_in_sink_for_air_in_air_s1.exterior_boundary=380.0435818429189
	sink_in_sink_for_air_in_air_s1.category="sink | abiotic | air | air - default"
	
	comp_objects_dict["sink_in_sink_for_air_in_air_s1"]=sink_in_sink_for_air_in_air_s1

	
	sink_in_sink_for_air_in_air_pond=advection_sink(constants,containingscenario,currentchemical,air_pond,comp_objects_dict)
	sink_in_sink_for_air_in_air_pond.name="sink_in_sink_for_air_in_air_pond"
	sink_in_sink_for_air_in_air_pond.containingvolumeelementname="air_pond"
	sink_in_sink_for_air_in_air_pond.parcel_name="pond"
	sink_in_sink_for_air_in_air_pond.parcel_points="p7 p8 p16 p14"
	sink_in_sink_for_air_in_air_pond.parcel_area=465187.5
	sink_in_sink_for_air_in_air_pond.exterior_boundary=1520.1727036425948
	sink_in_sink_for_air_in_air_pond.category="sink | abiotic | air | air - default"
	
	comp_objects_dict["sink_in_sink_for_air_in_air_pond"]=sink_in_sink_for_air_in_air_pond

	
	sink_in_sink_for_air_in_air_s4=advection_sink(constants,containingscenario,currentchemical,air_s4,comp_objects_dict)
	sink_in_sink_for_air_in_air_s4.name="sink_in_sink_for_air_in_air_s4"
	sink_in_sink_for_air_in_air_s4.containingvolumeelementname="air_s4"
	sink_in_sink_for_air_in_air_s4.parcel_name="s4"
	sink_in_sink_for_air_in_air_s4.parcel_points="p14 p16 p20 p18"
	sink_in_sink_for_air_in_air_s4.parcel_area=2041139.9999996647
	sink_in_sink_for_air_in_air_s4.exterior_boundary=3040.3486547433513
	sink_in_sink_for_air_in_air_s4.category="sink | abiotic | air | air - default"
	
	comp_objects_dict["sink_in_sink_for_air_in_air_s4"]=sink_in_sink_for_air_in_air_s4

	
	sink_in_sink_for_air_in_air_s5=advection_sink(constants,containingscenario,currentchemical,air_s5,comp_objects_dict)
	sink_in_sink_for_air_in_air_s5.name="sink_in_sink_for_air_in_air_s5"
	sink_in_sink_for_air_in_air_s5.containingvolumeelementname="air_s5"
	sink_in_sink_for_air_in_air_s5.parcel_name="s5"
	sink_in_sink_for_air_in_air_s5.parcel_points="p18 p20 p24 p22"
	sink_in_sink_for_air_in_air_s5.parcel_area=6693049.999999348
	sink_in_sink_for_air_in_air_s5.exterior_boundary=6817.244510421856
	sink_in_sink_for_air_in_air_s5.category="sink | abiotic | air | air - default"
	
	comp_objects_dict["sink_in_sink_for_air_in_air_s5"]=sink_in_sink_for_air_in_air_s5

	
	sink_in_sink_for_soil_surface_in_surfsoil_source=advection_sink(constants,containingscenario,currentchemical,surfsoil_source,comp_objects_dict)
	sink_in_sink_for_soil_surface_in_surfsoil_source.name="sink_in_sink_for_soil_surface_in_surfsoil_source"
	sink_in_sink_for_soil_surface_in_surfsoil_source.containingvolumeelementname="surfsoil_source"
	sink_in_sink_for_soil_surface_in_surfsoil_source.parcel_name="source"
	sink_in_sink_for_soil_surface_in_surfsoil_source.parcel_points="p1 p2 p3 p4 p5"
	sink_in_sink_for_soil_surface_in_surfsoil_source.parcel_area=62500.0
	sink_in_sink_for_soil_surface_in_surfsoil_source.exterior_boundary=750.0
	sink_in_sink_for_soil_surface_in_surfsoil_source.category="sink | abiotic | soil | surface soil | soil advection sink"
	
	comp_objects_dict["sink_in_sink_for_soil_surface_in_surfsoil_source"]=sink_in_sink_for_soil_surface_in_surfsoil_source

	
	sink_in_sink_for_soil_surface_in_surfsoil_n1=advection_sink(constants,containingscenario,currentchemical,surfsoil_n1,comp_objects_dict)
	sink_in_sink_for_soil_surface_in_surfsoil_n1.name="sink_in_sink_for_soil_surface_in_surfsoil_n1"
	sink_in_sink_for_soil_surface_in_surfsoil_n1.containingvolumeelementname="surfsoil_n1"
	sink_in_sink_for_soil_surface_in_surfsoil_n1.parcel_name="n1"
	sink_in_sink_for_soil_surface_in_surfsoil_n1.parcel_points="p5 p4 p7 p6"
	sink_in_sink_for_soil_surface_in_surfsoil_n1.parcel_area=58445.624999993015
	sink_in_sink_for_soil_surface_in_surfsoil_n1.exterior_boundary=380.0435818429189
	sink_in_sink_for_soil_surface_in_surfsoil_n1.category="sink | abiotic | soil | surface soil | soil advection sink"
	
	comp_objects_dict["sink_in_sink_for_soil_surface_in_surfsoil_n1"]=sink_in_sink_for_soil_surface_in_surfsoil_n1

	
	sink_in_sink_for_soil_surface_in_surfsoil_n6=advection_sink(constants,containingscenario,currentchemical,surfsoil_n6,comp_objects_dict)
	sink_in_sink_for_soil_surface_in_surfsoil_n6.name="sink_in_sink_for_soil_surface_in_surfsoil_n6"
	sink_in_sink_for_soil_surface_in_surfsoil_n6.containingvolumeelementname="surfsoil_n6"
	sink_in_sink_for_soil_surface_in_surfsoil_n6.parcel_name="n6"
	sink_in_sink_for_soil_surface_in_surfsoil_n6.parcel_points="p6 p7 p26 p25"
	sink_in_sink_for_soil_surface_in_surfsoil_n6.parcel_area=40633.00000000745
	sink_in_sink_for_soil_surface_in_surfsoil_n6.exterior_boundary=202.6895855736298
	sink_in_sink_for_soil_surface_in_surfsoil_n6.category="sink | abiotic | soil | surface soil | soil advection sink"
	
	comp_objects_dict["sink_in_sink_for_soil_surface_in_surfsoil_n6"]=sink_in_sink_for_soil_surface_in_surfsoil_n6

	
	sink_in_sink_for_soil_surface_in_surfsoil_n7=advection_sink(constants,containingscenario,currentchemical,surfsoil_n7,comp_objects_dict)
	sink_in_sink_for_soil_surface_in_surfsoil_n7.name="sink_in_sink_for_soil_surface_in_surfsoil_n7"
	sink_in_sink_for_soil_surface_in_surfsoil_n7.containingvolumeelementname="surfsoil_n7"
	sink_in_sink_for_soil_surface_in_surfsoil_n7.parcel_name="n7"
	sink_in_sink_for_soil_surface_in_surfsoil_n7.parcel_points="p25 p26 p10 p9"
	sink_in_sink_for_soil_surface_in_surfsoil_n7.parcel_area=73291.50000005029
	sink_in_sink_for_soil_surface_in_surfsoil_n7.exterior_boundary=304.035190232991
	sink_in_sink_for_soil_surface_in_surfsoil_n7.category="sink | abiotic | soil | surface soil | soil advection sink"
	
	comp_objects_dict["sink_in_sink_for_soil_surface_in_surfsoil_n7"]=sink_in_sink_for_soil_surface_in_surfsoil_n7

	
	sink_in_sink_for_soil_surface_in_surfsoil_n3=advection_sink(constants,containingscenario,currentchemical,surfsoil_n3,comp_objects_dict)
	sink_in_sink_for_soil_surface_in_surfsoil_n3.name="sink_in_sink_for_soil_surface_in_surfsoil_n3"
	sink_in_sink_for_soil_surface_in_surfsoil_n3.containingvolumeelementname="surfsoil_n3"
	sink_in_sink_for_soil_surface_in_surfsoil_n3.parcel_name="n3"
	sink_in_sink_for_soil_surface_in_surfsoil_n3.parcel_points="p9 p10 p14 p13"
	sink_in_sink_for_soil_surface_in_surfsoil_n3.parcel_area=351265.0000001304
	sink_in_sink_for_soil_surface_in_surfsoil_n3.exterior_boundary=1013.4479278679979
	sink_in_sink_for_soil_surface_in_surfsoil_n3.category="sink | abiotic | soil | surface soil | soil advection sink"
	
	comp_objects_dict["sink_in_sink_for_soil_surface_in_surfsoil_n3"]=sink_in_sink_for_soil_surface_in_surfsoil_n3

	
	sink_in_sink_for_soil_surface_in_surfsoil_n4=advection_sink(constants,containingscenario,currentchemical,surfsoil_n4,comp_objects_dict)
	sink_in_sink_for_soil_surface_in_surfsoil_n4.name="sink_in_sink_for_soil_surface_in_surfsoil_n4"
	sink_in_sink_for_soil_surface_in_surfsoil_n4.containingvolumeelementname="surfsoil_n4"
	sink_in_sink_for_soil_surface_in_surfsoil_n4.parcel_name="n4"
	sink_in_sink_for_soil_surface_in_surfsoil_n4.parcel_points="p13 p14 p18 p17"
	sink_in_sink_for_soil_surface_in_surfsoil_n4.parcel_area=2041139.9999996647
	sink_in_sink_for_soil_surface_in_surfsoil_n4.exterior_boundary=3040.3486547433513
	sink_in_sink_for_soil_surface_in_surfsoil_n4.category="sink | abiotic | soil | surface soil | soil advection sink"
	
	comp_objects_dict["sink_in_sink_for_soil_surface_in_surfsoil_n4"]=sink_in_sink_for_soil_surface_in_surfsoil_n4

	
	sink_in_sink_for_soil_surface_in_surfsoil_n5=advection_sink(constants,containingscenario,currentchemical,surfsoil_n5,comp_objects_dict)
	sink_in_sink_for_soil_surface_in_surfsoil_n5.name="sink_in_sink_for_soil_surface_in_surfsoil_n5"
	sink_in_sink_for_soil_surface_in_surfsoil_n5.containingvolumeelementname="surfsoil_n5"
	sink_in_sink_for_soil_surface_in_surfsoil_n5.parcel_name="n5"
	sink_in_sink_for_soil_surface_in_surfsoil_n5.parcel_points="p17 p18 p22 p21"
	sink_in_sink_for_soil_surface_in_surfsoil_n5.parcel_area=6693049.999999348
	sink_in_sink_for_soil_surface_in_surfsoil_n5.exterior_boundary=6817.244510421856
	sink_in_sink_for_soil_surface_in_surfsoil_n5.category="sink | abiotic | soil | surface soil | soil advection sink"
	
	comp_objects_dict["sink_in_sink_for_soil_surface_in_surfsoil_n5"]=sink_in_sink_for_soil_surface_in_surfsoil_n5

	
	sink_in_sink_for_soil_surface_in_surfsoil_s1=advection_sink(constants,containingscenario,currentchemical,surfsoil_s1,comp_objects_dict)
	sink_in_sink_for_soil_surface_in_surfsoil_s1.name="sink_in_sink_for_soil_surface_in_surfsoil_s1"
	sink_in_sink_for_soil_surface_in_surfsoil_s1.containingvolumeelementname="surfsoil_s1"
	sink_in_sink_for_soil_surface_in_surfsoil_s1.parcel_name="s1"
	sink_in_sink_for_soil_surface_in_surfsoil_s1.parcel_points="p4 p3 p8 p7"
	sink_in_sink_for_soil_surface_in_surfsoil_s1.parcel_area=58445.624999993015
	sink_in_sink_for_soil_surface_in_surfsoil_s1.exterior_boundary=380.0435818429189
	sink_in_sink_for_soil_surface_in_surfsoil_s1.category="sink | abiotic | soil | surface soil | soil advection sink"
	
	comp_objects_dict["sink_in_sink_for_soil_surface_in_surfsoil_s1"]=sink_in_sink_for_soil_surface_in_surfsoil_s1

	
	sink_in_sink_for_soil_surface_in_surfsoil_s4=advection_sink(constants,containingscenario,currentchemical,surfsoil_s4,comp_objects_dict)
	sink_in_sink_for_soil_surface_in_surfsoil_s4.name="sink_in_sink_for_soil_surface_in_surfsoil_s4"
	sink_in_sink_for_soil_surface_in_surfsoil_s4.containingvolumeelementname="surfsoil_s4"
	sink_in_sink_for_soil_surface_in_surfsoil_s4.parcel_name="s4"
	sink_in_sink_for_soil_surface_in_surfsoil_s4.parcel_points="p14 p16 p20 p18"
	sink_in_sink_for_soil_surface_in_surfsoil_s4.parcel_area=2041139.9999996647
	sink_in_sink_for_soil_surface_in_surfsoil_s4.exterior_boundary=3040.3486547433513
	sink_in_sink_for_soil_surface_in_surfsoil_s4.category="sink | abiotic | soil | surface soil | soil advection sink"
	
	comp_objects_dict["sink_in_sink_for_soil_surface_in_surfsoil_s4"]=sink_in_sink_for_soil_surface_in_surfsoil_s4

	
	sink_in_sink_for_soil_surface_in_surfsoil_s5=advection_sink(constants,containingscenario,currentchemical,surfsoil_s5,comp_objects_dict)
	sink_in_sink_for_soil_surface_in_surfsoil_s5.name="sink_in_sink_for_soil_surface_in_surfsoil_s5"
	sink_in_sink_for_soil_surface_in_surfsoil_s5.containingvolumeelementname="surfsoil_s5"
	sink_in_sink_for_soil_surface_in_surfsoil_s5.parcel_name="s5"
	sink_in_sink_for_soil_surface_in_surfsoil_s5.parcel_points="p18 p20 p24 p22"
	sink_in_sink_for_soil_surface_in_surfsoil_s5.parcel_area=6693049.999999348
	sink_in_sink_for_soil_surface_in_surfsoil_s5.exterior_boundary=6817.244510421856
	sink_in_sink_for_soil_surface_in_surfsoil_s5.category="sink | abiotic | soil | surface soil | soil advection sink"
	
	comp_objects_dict["sink_in_sink_for_soil_surface_in_surfsoil_s5"]=sink_in_sink_for_soil_surface_in_surfsoil_s5

	
	sediment_burial_sink_for_sediment_in_sed_pond=sediment_burial_sink(constants,containingscenario,currentchemical,sed_pond,comp_objects_dict)
	sediment_burial_sink_for_sediment_in_sed_pond.name="sediment_burial_sink_for_sediment_in_sed_pond"
	sediment_burial_sink_for_sediment_in_sed_pond.containingvolumeelementname="sed_pond"
	sediment_burial_sink_for_sediment_in_sed_pond.parcel_name="pond"
	sediment_burial_sink_for_sediment_in_sed_pond.parcel_points="p7 p8 p16 p14"
	sediment_burial_sink_for_sediment_in_sed_pond.parcel_area=465187.5
	sediment_burial_sink_for_sediment_in_sed_pond.exterior_boundary=1520.1727036425948
	
	comp_objects_dict["sediment_burial_sink_for_sediment_in_sed_pond"]=sediment_burial_sink_for_sediment_in_sed_pond

	
	class pseudo_compartment:
		pass

	dryvaporsource_in_dryvaporsource_s4=pseudo_compartment()
	dryvaporsource_in_dryvaporsource_s4.name="dryvaporsource_in_dryvaporsource_s4"
	dryvaporsource_in_dryvaporsource_s4.containingvolumeelementname="dryvaporsource_s4"
	dryvaporsource_in_dryvaporsource_s4.parcel_name="s4"
	dryvaporsource_in_dryvaporsource_s4.parcel_points="p14 p16 p20 p18"
	dryvaporsource_in_dryvaporsource_s4.parcel_area=2041139.9999996647
	dryvaporsource_in_dryvaporsource_s4.exterior_boundary=3040.3486547433513
	dryvaporsource_in_dryvaporsource_s4.deposition_rate={}
	dryvaporsource_in_dryvaporsource_s4.category="pseudosource | dry | vapor"
	comp_objects_dict["dryvaporsource_in_dryvaporsource_s4"]=dryvaporsource_in_dryvaporsource_s4

	wetvaporsource_in_wetvaporsource_s4=pseudo_compartment()
	wetvaporsource_in_wetvaporsource_s4.name="wetvaporsource_in_wetvaporsource_s4"
	wetvaporsource_in_wetvaporsource_s4.containingvolumeelementname="wetvaporsource_s4"
	wetvaporsource_in_wetvaporsource_s4.parcel_name="s4"
	wetvaporsource_in_wetvaporsource_s4.parcel_points="p14 p16 p20 p18"
	wetvaporsource_in_wetvaporsource_s4.parcel_area=2041139.9999996647
	wetvaporsource_in_wetvaporsource_s4.exterior_boundary=3040.3486547433513
	wetvaporsource_in_wetvaporsource_s4.deposition_rate={}
	wetvaporsource_in_wetvaporsource_s4.category="pseudosource | wet | vapor"
	comp_objects_dict["wetvaporsource_in_wetvaporsource_s4"]=wetvaporsource_in_wetvaporsource_s4

	dryparticlesource_in_dryparticlesource_s1=pseudo_compartment()
	dryparticlesource_in_dryparticlesource_s1.name="dryparticlesource_in_dryparticlesource_s1"
	dryparticlesource_in_dryparticlesource_s1.containingvolumeelementname="dryparticlesource_s1"
	dryparticlesource_in_dryparticlesource_s1.parcel_name="s1"
	dryparticlesource_in_dryparticlesource_s1.parcel_points="p4 p3 p8 p7"
	dryparticlesource_in_dryparticlesource_s1.parcel_area=58445.624999993015
	dryparticlesource_in_dryparticlesource_s1.exterior_boundary=380.0435818429189
	dryparticlesource_in_dryparticlesource_s1.deposition_rate={}
	dryparticlesource_in_dryparticlesource_s1.category="pseudosource | dry | particle"
	comp_objects_dict["dryparticlesource_in_dryparticlesource_s1"]=dryparticlesource_in_dryparticlesource_s1

	wetparticlesource_in_wetparticlesource_s1=pseudo_compartment()
	wetparticlesource_in_wetparticlesource_s1.name="wetparticlesource_in_wetparticlesource_s1"
	wetparticlesource_in_wetparticlesource_s1.containingvolumeelementname="wetparticlesource_s1"
	wetparticlesource_in_wetparticlesource_s1.parcel_name="s1"
	wetparticlesource_in_wetparticlesource_s1.parcel_points="p4 p3 p8 p7"
	wetparticlesource_in_wetparticlesource_s1.parcel_area=58445.624999993015
	wetparticlesource_in_wetparticlesource_s1.exterior_boundary=380.0435818429189
	wetparticlesource_in_wetparticlesource_s1.deposition_rate={}
	wetparticlesource_in_wetparticlesource_s1.category="pseudosource | wet | particle"
	comp_objects_dict["wetparticlesource_in_wetparticlesource_s1"]=wetparticlesource_in_wetparticlesource_s1

	dryparticlesource_in_dryparticlesource_source=pseudo_compartment()
	dryparticlesource_in_dryparticlesource_source.name="dryparticlesource_in_dryparticlesource_source"
	dryparticlesource_in_dryparticlesource_source.containingvolumeelementname="dryparticlesource_source"
	dryparticlesource_in_dryparticlesource_source.parcel_name="source"
	dryparticlesource_in_dryparticlesource_source.parcel_points="p1 p2 p3 p4 p5"
	dryparticlesource_in_dryparticlesource_source.parcel_area=62500.0
	dryparticlesource_in_dryparticlesource_source.exterior_boundary=750.0
	dryparticlesource_in_dryparticlesource_source.deposition_rate={}
	dryparticlesource_in_dryparticlesource_source.category="pseudosource | dry | particle"
	comp_objects_dict["dryparticlesource_in_dryparticlesource_source"]=dryparticlesource_in_dryparticlesource_source

	dryvaporsource_in_dryvaporsource_source=pseudo_compartment()
	dryvaporsource_in_dryvaporsource_source.name="dryvaporsource_in_dryvaporsource_source"
	dryvaporsource_in_dryvaporsource_source.containingvolumeelementname="dryvaporsource_source"
	dryvaporsource_in_dryvaporsource_source.parcel_name="source"
	dryvaporsource_in_dryvaporsource_source.parcel_points="p1 p2 p3 p4 p5"
	dryvaporsource_in_dryvaporsource_source.parcel_area=62500.0
	dryvaporsource_in_dryvaporsource_source.exterior_boundary=750.0
	dryvaporsource_in_dryvaporsource_source.deposition_rate={}
	dryvaporsource_in_dryvaporsource_source.category="pseudosource | dry | vapor"
	comp_objects_dict["dryvaporsource_in_dryvaporsource_source"]=dryvaporsource_in_dryvaporsource_source

	wetparticlesource_in_wetparticlesource_source=pseudo_compartment()
	wetparticlesource_in_wetparticlesource_source.name="wetparticlesource_in_wetparticlesource_source"
	wetparticlesource_in_wetparticlesource_source.containingvolumeelementname="wetparticlesource_source"
	wetparticlesource_in_wetparticlesource_source.parcel_name="source"
	wetparticlesource_in_wetparticlesource_source.parcel_points="p1 p2 p3 p4 p5"
	wetparticlesource_in_wetparticlesource_source.parcel_area=62500.0
	wetparticlesource_in_wetparticlesource_source.exterior_boundary=750.0
	wetparticlesource_in_wetparticlesource_source.deposition_rate={}
	wetparticlesource_in_wetparticlesource_source.category="pseudosource | wet | particle"
	comp_objects_dict["wetparticlesource_in_wetparticlesource_source"]=wetparticlesource_in_wetparticlesource_source

	wetvaporsource_in_wetvaporsource_source=pseudo_compartment()
	wetvaporsource_in_wetvaporsource_source.name="wetvaporsource_in_wetvaporsource_source"
	wetvaporsource_in_wetvaporsource_source.containingvolumeelementname="wetvaporsource_source"
	wetvaporsource_in_wetvaporsource_source.parcel_name="source"
	wetvaporsource_in_wetvaporsource_source.parcel_points="p1 p2 p3 p4 p5"
	wetvaporsource_in_wetvaporsource_source.parcel_area=62500.0
	wetvaporsource_in_wetvaporsource_source.exterior_boundary=750.0
	wetvaporsource_in_wetvaporsource_source.deposition_rate={}
	wetvaporsource_in_wetvaporsource_source.category="pseudosource | wet | vapor"
	comp_objects_dict["wetvaporsource_in_wetvaporsource_source"]=wetvaporsource_in_wetvaporsource_source

	dryparticlesource_in_dryparticlesource_n1=pseudo_compartment()
	dryparticlesource_in_dryparticlesource_n1.name="dryparticlesource_in_dryparticlesource_n1"
	dryparticlesource_in_dryparticlesource_n1.containingvolumeelementname="dryparticlesource_n1"
	dryparticlesource_in_dryparticlesource_n1.parcel_name="n1"
	dryparticlesource_in_dryparticlesource_n1.parcel_points="p5 p4 p7 p6"
	dryparticlesource_in_dryparticlesource_n1.parcel_area=58445.624999993015
	dryparticlesource_in_dryparticlesource_n1.exterior_boundary=380.0435818429189
	dryparticlesource_in_dryparticlesource_n1.deposition_rate={}
	dryparticlesource_in_dryparticlesource_n1.category="pseudosource | dry | particle"
	comp_objects_dict["dryparticlesource_in_dryparticlesource_n1"]=dryparticlesource_in_dryparticlesource_n1

	wetparticlesource_in_wetparticlesource_n1=pseudo_compartment()
	wetparticlesource_in_wetparticlesource_n1.name="wetparticlesource_in_wetparticlesource_n1"
	wetparticlesource_in_wetparticlesource_n1.containingvolumeelementname="wetparticlesource_n1"
	wetparticlesource_in_wetparticlesource_n1.parcel_name="n1"
	wetparticlesource_in_wetparticlesource_n1.parcel_points="p5 p4 p7 p6"
	wetparticlesource_in_wetparticlesource_n1.parcel_area=58445.624999993015
	wetparticlesource_in_wetparticlesource_n1.exterior_boundary=380.0435818429189
	wetparticlesource_in_wetparticlesource_n1.deposition_rate={}
	wetparticlesource_in_wetparticlesource_n1.category="pseudosource | wet | particle"
	comp_objects_dict["wetparticlesource_in_wetparticlesource_n1"]=wetparticlesource_in_wetparticlesource_n1

	dryparticlesource_in_dryparticlesource_n7=pseudo_compartment()
	dryparticlesource_in_dryparticlesource_n7.name="dryparticlesource_in_dryparticlesource_n7"
	dryparticlesource_in_dryparticlesource_n7.containingvolumeelementname="dryparticlesource_n7"
	dryparticlesource_in_dryparticlesource_n7.parcel_name="n7"
	dryparticlesource_in_dryparticlesource_n7.parcel_points="p25 p26 p10 p9"
	dryparticlesource_in_dryparticlesource_n7.parcel_area=73291.50000005029
	dryparticlesource_in_dryparticlesource_n7.exterior_boundary=304.035190232991
	dryparticlesource_in_dryparticlesource_n7.deposition_rate={}
	dryparticlesource_in_dryparticlesource_n7.category="pseudosource | dry | particle"
	comp_objects_dict["dryparticlesource_in_dryparticlesource_n7"]=dryparticlesource_in_dryparticlesource_n7

	wetparticlesource_in_wetparticlesource_n7=pseudo_compartment()
	wetparticlesource_in_wetparticlesource_n7.name="wetparticlesource_in_wetparticlesource_n7"
	wetparticlesource_in_wetparticlesource_n7.containingvolumeelementname="wetparticlesource_n7"
	wetparticlesource_in_wetparticlesource_n7.parcel_name="n7"
	wetparticlesource_in_wetparticlesource_n7.parcel_points="p25 p26 p10 p9"
	wetparticlesource_in_wetparticlesource_n7.parcel_area=73291.50000005029
	wetparticlesource_in_wetparticlesource_n7.exterior_boundary=304.035190232991
	wetparticlesource_in_wetparticlesource_n7.deposition_rate={}
	wetparticlesource_in_wetparticlesource_n7.category="pseudosource | wet | particle"
	comp_objects_dict["wetparticlesource_in_wetparticlesource_n7"]=wetparticlesource_in_wetparticlesource_n7

	dryparticlesource_in_dryparticlesource_n3=pseudo_compartment()
	dryparticlesource_in_dryparticlesource_n3.name="dryparticlesource_in_dryparticlesource_n3"
	dryparticlesource_in_dryparticlesource_n3.containingvolumeelementname="dryparticlesource_n3"
	dryparticlesource_in_dryparticlesource_n3.parcel_name="n3"
	dryparticlesource_in_dryparticlesource_n3.parcel_points="p9 p10 p14 p13"
	dryparticlesource_in_dryparticlesource_n3.parcel_area=351265.0000001304
	dryparticlesource_in_dryparticlesource_n3.exterior_boundary=1013.4479278679979
	dryparticlesource_in_dryparticlesource_n3.deposition_rate={}
	dryparticlesource_in_dryparticlesource_n3.category="pseudosource | dry | particle"
	comp_objects_dict["dryparticlesource_in_dryparticlesource_n3"]=dryparticlesource_in_dryparticlesource_n3

	wetparticlesource_in_wetparticlesource_n3=pseudo_compartment()
	wetparticlesource_in_wetparticlesource_n3.name="wetparticlesource_in_wetparticlesource_n3"
	wetparticlesource_in_wetparticlesource_n3.containingvolumeelementname="wetparticlesource_n3"
	wetparticlesource_in_wetparticlesource_n3.parcel_name="n3"
	wetparticlesource_in_wetparticlesource_n3.parcel_points="p9 p10 p14 p13"
	wetparticlesource_in_wetparticlesource_n3.parcel_area=351265.0000001304
	wetparticlesource_in_wetparticlesource_n3.exterior_boundary=1013.4479278679979
	wetparticlesource_in_wetparticlesource_n3.deposition_rate={}
	wetparticlesource_in_wetparticlesource_n3.category="pseudosource | wet | particle"
	comp_objects_dict["wetparticlesource_in_wetparticlesource_n3"]=wetparticlesource_in_wetparticlesource_n3

	dryvaporsource_in_dryvaporsource_s1=pseudo_compartment()
	dryvaporsource_in_dryvaporsource_s1.name="dryvaporsource_in_dryvaporsource_s1"
	dryvaporsource_in_dryvaporsource_s1.containingvolumeelementname="dryvaporsource_s1"
	dryvaporsource_in_dryvaporsource_s1.parcel_name="s1"
	dryvaporsource_in_dryvaporsource_s1.parcel_points="p4 p3 p8 p7"
	dryvaporsource_in_dryvaporsource_s1.parcel_area=58445.624999993015
	dryvaporsource_in_dryvaporsource_s1.exterior_boundary=380.0435818429189
	dryvaporsource_in_dryvaporsource_s1.deposition_rate={}
	dryvaporsource_in_dryvaporsource_s1.category="pseudosource | dry | vapor"
	comp_objects_dict["dryvaporsource_in_dryvaporsource_s1"]=dryvaporsource_in_dryvaporsource_s1

	wetvaporsource_in_wetvaporsource_s1=pseudo_compartment()
	wetvaporsource_in_wetvaporsource_s1.name="wetvaporsource_in_wetvaporsource_s1"
	wetvaporsource_in_wetvaporsource_s1.containingvolumeelementname="wetvaporsource_s1"
	wetvaporsource_in_wetvaporsource_s1.parcel_name="s1"
	wetvaporsource_in_wetvaporsource_s1.parcel_points="p4 p3 p8 p7"
	wetvaporsource_in_wetvaporsource_s1.parcel_area=58445.624999993015
	wetvaporsource_in_wetvaporsource_s1.exterior_boundary=380.0435818429189
	wetvaporsource_in_wetvaporsource_s1.deposition_rate={}
	wetvaporsource_in_wetvaporsource_s1.category="pseudosource | wet | vapor"
	comp_objects_dict["wetvaporsource_in_wetvaporsource_s1"]=wetvaporsource_in_wetvaporsource_s1

	dryparticlesource_in_dryparticlesource_s5=pseudo_compartment()
	dryparticlesource_in_dryparticlesource_s5.name="dryparticlesource_in_dryparticlesource_s5"
	dryparticlesource_in_dryparticlesource_s5.containingvolumeelementname="dryparticlesource_s5"
	dryparticlesource_in_dryparticlesource_s5.parcel_name="s5"
	dryparticlesource_in_dryparticlesource_s5.parcel_points="p18 p20 p24 p22"
	dryparticlesource_in_dryparticlesource_s5.parcel_area=6693049.999999348
	dryparticlesource_in_dryparticlesource_s5.exterior_boundary=6817.244510421856
	dryparticlesource_in_dryparticlesource_s5.deposition_rate={}
	dryparticlesource_in_dryparticlesource_s5.category="pseudosource | dry | particle"
	comp_objects_dict["dryparticlesource_in_dryparticlesource_s5"]=dryparticlesource_in_dryparticlesource_s5

	wetparticlesource_in_wetparticlesource_s5=pseudo_compartment()
	wetparticlesource_in_wetparticlesource_s5.name="wetparticlesource_in_wetparticlesource_s5"
	wetparticlesource_in_wetparticlesource_s5.containingvolumeelementname="wetparticlesource_s5"
	wetparticlesource_in_wetparticlesource_s5.parcel_name="s5"
	wetparticlesource_in_wetparticlesource_s5.parcel_points="p18 p20 p24 p22"
	wetparticlesource_in_wetparticlesource_s5.parcel_area=6693049.999999348
	wetparticlesource_in_wetparticlesource_s5.exterior_boundary=6817.244510421856
	wetparticlesource_in_wetparticlesource_s5.deposition_rate={}
	wetparticlesource_in_wetparticlesource_s5.category="pseudosource | wet | particle"
	comp_objects_dict["wetparticlesource_in_wetparticlesource_s5"]=wetparticlesource_in_wetparticlesource_s5

	dryparticlesource_in_dryparticlesource_s4=pseudo_compartment()
	dryparticlesource_in_dryparticlesource_s4.name="dryparticlesource_in_dryparticlesource_s4"
	dryparticlesource_in_dryparticlesource_s4.containingvolumeelementname="dryparticlesource_s4"
	dryparticlesource_in_dryparticlesource_s4.parcel_name="s4"
	dryparticlesource_in_dryparticlesource_s4.parcel_points="p14 p16 p20 p18"
	dryparticlesource_in_dryparticlesource_s4.parcel_area=2041139.9999996647
	dryparticlesource_in_dryparticlesource_s4.exterior_boundary=3040.3486547433513
	dryparticlesource_in_dryparticlesource_s4.deposition_rate={}
	dryparticlesource_in_dryparticlesource_s4.category="pseudosource | dry | particle"
	comp_objects_dict["dryparticlesource_in_dryparticlesource_s4"]=dryparticlesource_in_dryparticlesource_s4

	wetparticlesource_in_wetparticlesource_s4=pseudo_compartment()
	wetparticlesource_in_wetparticlesource_s4.name="wetparticlesource_in_wetparticlesource_s4"
	wetparticlesource_in_wetparticlesource_s4.containingvolumeelementname="wetparticlesource_s4"
	wetparticlesource_in_wetparticlesource_s4.parcel_name="s4"
	wetparticlesource_in_wetparticlesource_s4.parcel_points="p14 p16 p20 p18"
	wetparticlesource_in_wetparticlesource_s4.parcel_area=2041139.9999996647
	wetparticlesource_in_wetparticlesource_s4.exterior_boundary=3040.3486547433513
	wetparticlesource_in_wetparticlesource_s4.deposition_rate={}
	wetparticlesource_in_wetparticlesource_s4.category="pseudosource | wet | particle"
	comp_objects_dict["wetparticlesource_in_wetparticlesource_s4"]=wetparticlesource_in_wetparticlesource_s4

	dryvaporsource_in_dryvaporsource_s5=pseudo_compartment()
	dryvaporsource_in_dryvaporsource_s5.name="dryvaporsource_in_dryvaporsource_s5"
	dryvaporsource_in_dryvaporsource_s5.containingvolumeelementname="dryvaporsource_s5"
	dryvaporsource_in_dryvaporsource_s5.parcel_name="s5"
	dryvaporsource_in_dryvaporsource_s5.parcel_points="p18 p20 p24 p22"
	dryvaporsource_in_dryvaporsource_s5.parcel_area=6693049.999999348
	dryvaporsource_in_dryvaporsource_s5.exterior_boundary=6817.244510421856
	dryvaporsource_in_dryvaporsource_s5.deposition_rate={}
	dryvaporsource_in_dryvaporsource_s5.category="pseudosource | dry | vapor"
	comp_objects_dict["dryvaporsource_in_dryvaporsource_s5"]=dryvaporsource_in_dryvaporsource_s5

	wetvaporsource_in_wetvaporsource_s5=pseudo_compartment()
	wetvaporsource_in_wetvaporsource_s5.name="wetvaporsource_in_wetvaporsource_s5"
	wetvaporsource_in_wetvaporsource_s5.containingvolumeelementname="wetvaporsource_s5"
	wetvaporsource_in_wetvaporsource_s5.parcel_name="s5"
	wetvaporsource_in_wetvaporsource_s5.parcel_points="p18 p20 p24 p22"
	wetvaporsource_in_wetvaporsource_s5.parcel_area=6693049.999999348
	wetvaporsource_in_wetvaporsource_s5.exterior_boundary=6817.244510421856
	wetvaporsource_in_wetvaporsource_s5.deposition_rate={}
	wetvaporsource_in_wetvaporsource_s5.category="pseudosource | wet | vapor"
	comp_objects_dict["wetvaporsource_in_wetvaporsource_s5"]=wetvaporsource_in_wetvaporsource_s5

	dryvaporsource_in_dryvaporsource_n5=pseudo_compartment()
	dryvaporsource_in_dryvaporsource_n5.name="dryvaporsource_in_dryvaporsource_n5"
	dryvaporsource_in_dryvaporsource_n5.containingvolumeelementname="dryvaporsource_n5"
	dryvaporsource_in_dryvaporsource_n5.parcel_name="n5"
	dryvaporsource_in_dryvaporsource_n5.parcel_points="p17 p18 p22 p21"
	dryvaporsource_in_dryvaporsource_n5.parcel_area=6693049.999999348
	dryvaporsource_in_dryvaporsource_n5.exterior_boundary=6817.244510421856
	dryvaporsource_in_dryvaporsource_n5.deposition_rate={}
	dryvaporsource_in_dryvaporsource_n5.category="pseudosource | dry | vapor"
	comp_objects_dict["dryvaporsource_in_dryvaporsource_n5"]=dryvaporsource_in_dryvaporsource_n5

	wetvaporsource_in_wetvaporsource_n5=pseudo_compartment()
	wetvaporsource_in_wetvaporsource_n5.name="wetvaporsource_in_wetvaporsource_n5"
	wetvaporsource_in_wetvaporsource_n5.containingvolumeelementname="wetvaporsource_n5"
	wetvaporsource_in_wetvaporsource_n5.parcel_name="n5"
	wetvaporsource_in_wetvaporsource_n5.parcel_points="p17 p18 p22 p21"
	wetvaporsource_in_wetvaporsource_n5.parcel_area=6693049.999999348
	wetvaporsource_in_wetvaporsource_n5.exterior_boundary=6817.244510421856
	wetvaporsource_in_wetvaporsource_n5.deposition_rate={}
	wetvaporsource_in_wetvaporsource_n5.category="pseudosource | wet | vapor"
	comp_objects_dict["wetvaporsource_in_wetvaporsource_n5"]=wetvaporsource_in_wetvaporsource_n5

	dryvaporsource_in_dryvaporsource_n4=pseudo_compartment()
	dryvaporsource_in_dryvaporsource_n4.name="dryvaporsource_in_dryvaporsource_n4"
	dryvaporsource_in_dryvaporsource_n4.containingvolumeelementname="dryvaporsource_n4"
	dryvaporsource_in_dryvaporsource_n4.parcel_name="n4"
	dryvaporsource_in_dryvaporsource_n4.parcel_points="p13 p14 p18 p17"
	dryvaporsource_in_dryvaporsource_n4.parcel_area=2041139.9999996647
	dryvaporsource_in_dryvaporsource_n4.exterior_boundary=3040.3486547433513
	dryvaporsource_in_dryvaporsource_n4.deposition_rate={}
	dryvaporsource_in_dryvaporsource_n4.category="pseudosource | dry | vapor"
	comp_objects_dict["dryvaporsource_in_dryvaporsource_n4"]=dryvaporsource_in_dryvaporsource_n4

	wetvaporsource_in_wetvaporsource_n4=pseudo_compartment()
	wetvaporsource_in_wetvaporsource_n4.name="wetvaporsource_in_wetvaporsource_n4"
	wetvaporsource_in_wetvaporsource_n4.containingvolumeelementname="wetvaporsource_n4"
	wetvaporsource_in_wetvaporsource_n4.parcel_name="n4"
	wetvaporsource_in_wetvaporsource_n4.parcel_points="p13 p14 p18 p17"
	wetvaporsource_in_wetvaporsource_n4.parcel_area=2041139.9999996647
	wetvaporsource_in_wetvaporsource_n4.exterior_boundary=3040.3486547433513
	wetvaporsource_in_wetvaporsource_n4.deposition_rate={}
	wetvaporsource_in_wetvaporsource_n4.category="pseudosource | wet | vapor"
	comp_objects_dict["wetvaporsource_in_wetvaporsource_n4"]=wetvaporsource_in_wetvaporsource_n4

	dryvaporsource_in_dryvaporsource_n3=pseudo_compartment()
	dryvaporsource_in_dryvaporsource_n3.name="dryvaporsource_in_dryvaporsource_n3"
	dryvaporsource_in_dryvaporsource_n3.containingvolumeelementname="dryvaporsource_n3"
	dryvaporsource_in_dryvaporsource_n3.parcel_name="n3"
	dryvaporsource_in_dryvaporsource_n3.parcel_points="p9 p10 p14 p13"
	dryvaporsource_in_dryvaporsource_n3.parcel_area=351265.0000001304
	dryvaporsource_in_dryvaporsource_n3.exterior_boundary=1013.4479278679979
	dryvaporsource_in_dryvaporsource_n3.deposition_rate={}
	dryvaporsource_in_dryvaporsource_n3.category="pseudosource | dry | vapor"
	comp_objects_dict["dryvaporsource_in_dryvaporsource_n3"]=dryvaporsource_in_dryvaporsource_n3

	wetvaporsource_in_wetvaporsource_n3=pseudo_compartment()
	wetvaporsource_in_wetvaporsource_n3.name="wetvaporsource_in_wetvaporsource_n3"
	wetvaporsource_in_wetvaporsource_n3.containingvolumeelementname="wetvaporsource_n3"
	wetvaporsource_in_wetvaporsource_n3.parcel_name="n3"
	wetvaporsource_in_wetvaporsource_n3.parcel_points="p9 p10 p14 p13"
	wetvaporsource_in_wetvaporsource_n3.parcel_area=351265.0000001304
	wetvaporsource_in_wetvaporsource_n3.exterior_boundary=1013.4479278679979
	wetvaporsource_in_wetvaporsource_n3.deposition_rate={}
	wetvaporsource_in_wetvaporsource_n3.category="pseudosource | wet | vapor"
	comp_objects_dict["wetvaporsource_in_wetvaporsource_n3"]=wetvaporsource_in_wetvaporsource_n3

	dryvaporsource_in_dryvaporsource_n1=pseudo_compartment()
	dryvaporsource_in_dryvaporsource_n1.name="dryvaporsource_in_dryvaporsource_n1"
	dryvaporsource_in_dryvaporsource_n1.containingvolumeelementname="dryvaporsource_n1"
	dryvaporsource_in_dryvaporsource_n1.parcel_name="n1"
	dryvaporsource_in_dryvaporsource_n1.parcel_points="p5 p4 p7 p6"
	dryvaporsource_in_dryvaporsource_n1.parcel_area=58445.624999993015
	dryvaporsource_in_dryvaporsource_n1.exterior_boundary=380.0435818429189
	dryvaporsource_in_dryvaporsource_n1.deposition_rate={}
	dryvaporsource_in_dryvaporsource_n1.category="pseudosource | dry | vapor"
	comp_objects_dict["dryvaporsource_in_dryvaporsource_n1"]=dryvaporsource_in_dryvaporsource_n1

	wetvaporsource_in_wetvaporsource_n1=pseudo_compartment()
	wetvaporsource_in_wetvaporsource_n1.name="wetvaporsource_in_wetvaporsource_n1"
	wetvaporsource_in_wetvaporsource_n1.containingvolumeelementname="wetvaporsource_n1"
	wetvaporsource_in_wetvaporsource_n1.parcel_name="n1"
	wetvaporsource_in_wetvaporsource_n1.parcel_points="p5 p4 p7 p6"
	wetvaporsource_in_wetvaporsource_n1.parcel_area=58445.624999993015
	wetvaporsource_in_wetvaporsource_n1.exterior_boundary=380.0435818429189
	wetvaporsource_in_wetvaporsource_n1.deposition_rate={}
	wetvaporsource_in_wetvaporsource_n1.category="pseudosource | wet | vapor"
	comp_objects_dict["wetvaporsource_in_wetvaporsource_n1"]=wetvaporsource_in_wetvaporsource_n1

	dryvaporsource_in_dryvaporsource_n7=pseudo_compartment()
	dryvaporsource_in_dryvaporsource_n7.name="dryvaporsource_in_dryvaporsource_n7"
	dryvaporsource_in_dryvaporsource_n7.containingvolumeelementname="dryvaporsource_n7"
	dryvaporsource_in_dryvaporsource_n7.parcel_name="n7"
	dryvaporsource_in_dryvaporsource_n7.parcel_points="p25 p26 p10 p9"
	dryvaporsource_in_dryvaporsource_n7.parcel_area=73291.50000005029
	dryvaporsource_in_dryvaporsource_n7.exterior_boundary=304.035190232991
	dryvaporsource_in_dryvaporsource_n7.deposition_rate={}
	dryvaporsource_in_dryvaporsource_n7.category="pseudosource | dry | vapor"
	comp_objects_dict["dryvaporsource_in_dryvaporsource_n7"]=dryvaporsource_in_dryvaporsource_n7

	wetvaporsource_in_wetvaporsource_n7=pseudo_compartment()
	wetvaporsource_in_wetvaporsource_n7.name="wetvaporsource_in_wetvaporsource_n7"
	wetvaporsource_in_wetvaporsource_n7.containingvolumeelementname="wetvaporsource_n7"
	wetvaporsource_in_wetvaporsource_n7.parcel_name="n7"
	wetvaporsource_in_wetvaporsource_n7.parcel_points="p25 p26 p10 p9"
	wetvaporsource_in_wetvaporsource_n7.parcel_area=73291.50000005029
	wetvaporsource_in_wetvaporsource_n7.exterior_boundary=304.035190232991
	wetvaporsource_in_wetvaporsource_n7.deposition_rate={}
	wetvaporsource_in_wetvaporsource_n7.category="pseudosource | wet | vapor"
	comp_objects_dict["wetvaporsource_in_wetvaporsource_n7"]=wetvaporsource_in_wetvaporsource_n7

	dryparticlesource_in_dryparticlesource_n4=pseudo_compartment()
	dryparticlesource_in_dryparticlesource_n4.name="dryparticlesource_in_dryparticlesource_n4"
	dryparticlesource_in_dryparticlesource_n4.containingvolumeelementname="dryparticlesource_n4"
	dryparticlesource_in_dryparticlesource_n4.parcel_name="n4"
	dryparticlesource_in_dryparticlesource_n4.parcel_points="p13 p14 p18 p17"
	dryparticlesource_in_dryparticlesource_n4.parcel_area=2041139.9999996647
	dryparticlesource_in_dryparticlesource_n4.exterior_boundary=3040.3486547433513
	dryparticlesource_in_dryparticlesource_n4.deposition_rate={}
	dryparticlesource_in_dryparticlesource_n4.category="pseudosource | dry | particle"
	comp_objects_dict["dryparticlesource_in_dryparticlesource_n4"]=dryparticlesource_in_dryparticlesource_n4

	wetparticlesource_in_wetparticlesource_n4=pseudo_compartment()
	wetparticlesource_in_wetparticlesource_n4.name="wetparticlesource_in_wetparticlesource_n4"
	wetparticlesource_in_wetparticlesource_n4.containingvolumeelementname="wetparticlesource_n4"
	wetparticlesource_in_wetparticlesource_n4.parcel_name="n4"
	wetparticlesource_in_wetparticlesource_n4.parcel_points="p13 p14 p18 p17"
	wetparticlesource_in_wetparticlesource_n4.parcel_area=2041139.9999996647
	wetparticlesource_in_wetparticlesource_n4.exterior_boundary=3040.3486547433513
	wetparticlesource_in_wetparticlesource_n4.deposition_rate={}
	wetparticlesource_in_wetparticlesource_n4.category="pseudosource | wet | particle"
	comp_objects_dict["wetparticlesource_in_wetparticlesource_n4"]=wetparticlesource_in_wetparticlesource_n4

	dryparticlesource_in_dryparticlesource_n5=pseudo_compartment()
	dryparticlesource_in_dryparticlesource_n5.name="dryparticlesource_in_dryparticlesource_n5"
	dryparticlesource_in_dryparticlesource_n5.containingvolumeelementname="dryparticlesource_n5"
	dryparticlesource_in_dryparticlesource_n5.parcel_name="n5"
	dryparticlesource_in_dryparticlesource_n5.parcel_points="p17 p18 p22 p21"
	dryparticlesource_in_dryparticlesource_n5.parcel_area=6693049.999999348
	dryparticlesource_in_dryparticlesource_n5.exterior_boundary=6817.244510421856
	dryparticlesource_in_dryparticlesource_n5.deposition_rate={}
	dryparticlesource_in_dryparticlesource_n5.category="pseudosource | dry | particle"
	comp_objects_dict["dryparticlesource_in_dryparticlesource_n5"]=dryparticlesource_in_dryparticlesource_n5

	wetparticlesource_in_wetparticlesource_n5=pseudo_compartment()
	wetparticlesource_in_wetparticlesource_n5.name="wetparticlesource_in_wetparticlesource_n5"
	wetparticlesource_in_wetparticlesource_n5.containingvolumeelementname="wetparticlesource_n5"
	wetparticlesource_in_wetparticlesource_n5.parcel_name="n5"
	wetparticlesource_in_wetparticlesource_n5.parcel_points="p17 p18 p22 p21"
	wetparticlesource_in_wetparticlesource_n5.parcel_area=6693049.999999348
	wetparticlesource_in_wetparticlesource_n5.exterior_boundary=6817.244510421856
	wetparticlesource_in_wetparticlesource_n5.deposition_rate={}
	wetparticlesource_in_wetparticlesource_n5.category="pseudosource | wet | particle"
	comp_objects_dict["wetparticlesource_in_wetparticlesource_n5"]=wetparticlesource_in_wetparticlesource_n5

	dryparticlesource_in_dryparticlesource_n6=pseudo_compartment()
	dryparticlesource_in_dryparticlesource_n6.name="dryparticlesource_in_dryparticlesource_n6"
	dryparticlesource_in_dryparticlesource_n6.containingvolumeelementname="dryparticlesource_n6"
	dryparticlesource_in_dryparticlesource_n6.parcel_name="n6"
	dryparticlesource_in_dryparticlesource_n6.parcel_points="p6 p7 p26 p25"
	dryparticlesource_in_dryparticlesource_n6.parcel_area=40633.00000000745
	dryparticlesource_in_dryparticlesource_n6.exterior_boundary=202.6895855736298
	dryparticlesource_in_dryparticlesource_n6.deposition_rate={}
	dryparticlesource_in_dryparticlesource_n6.category="pseudosource | dry | particle"
	comp_objects_dict["dryparticlesource_in_dryparticlesource_n6"]=dryparticlesource_in_dryparticlesource_n6

	dryvaporsource_in_dryvaporsource_n6=pseudo_compartment()
	dryvaporsource_in_dryvaporsource_n6.name="dryvaporsource_in_dryvaporsource_n6"
	dryvaporsource_in_dryvaporsource_n6.containingvolumeelementname="dryvaporsource_n6"
	dryvaporsource_in_dryvaporsource_n6.parcel_name="n6"
	dryvaporsource_in_dryvaporsource_n6.parcel_points="p6 p7 p26 p25"
	dryvaporsource_in_dryvaporsource_n6.parcel_area=40633.00000000745
	dryvaporsource_in_dryvaporsource_n6.exterior_boundary=202.6895855736298
	dryvaporsource_in_dryvaporsource_n6.deposition_rate={}
	dryvaporsource_in_dryvaporsource_n6.category="pseudosource | dry | vapor"
	comp_objects_dict["dryvaporsource_in_dryvaporsource_n6"]=dryvaporsource_in_dryvaporsource_n6

	wetparticlesource_in_wetparticlesource_n6=pseudo_compartment()
	wetparticlesource_in_wetparticlesource_n6.name="wetparticlesource_in_wetparticlesource_n6"
	wetparticlesource_in_wetparticlesource_n6.containingvolumeelementname="wetparticlesource_n6"
	wetparticlesource_in_wetparticlesource_n6.parcel_name="n6"
	wetparticlesource_in_wetparticlesource_n6.parcel_points="p6 p7 p26 p25"
	wetparticlesource_in_wetparticlesource_n6.parcel_area=40633.00000000745
	wetparticlesource_in_wetparticlesource_n6.exterior_boundary=202.6895855736298
	wetparticlesource_in_wetparticlesource_n6.deposition_rate={}
	wetparticlesource_in_wetparticlesource_n6.category="pseudosource | wet | particle"
	comp_objects_dict["wetparticlesource_in_wetparticlesource_n6"]=wetparticlesource_in_wetparticlesource_n6

	wetvaporsource_in_wetvaporsource_n6=pseudo_compartment()
	wetvaporsource_in_wetvaporsource_n6.name="wetvaporsource_in_wetvaporsource_n6"
	wetvaporsource_in_wetvaporsource_n6.containingvolumeelementname="wetvaporsource_n6"
	wetvaporsource_in_wetvaporsource_n6.parcel_name="n6"
	wetvaporsource_in_wetvaporsource_n6.parcel_points="p6 p7 p26 p25"
	wetvaporsource_in_wetvaporsource_n6.parcel_area=40633.00000000745
	wetvaporsource_in_wetvaporsource_n6.exterior_boundary=202.6895855736298
	wetvaporsource_in_wetvaporsource_n6.deposition_rate={}
	wetvaporsource_in_wetvaporsource_n6.category="pseudosource | wet | vapor"
	comp_objects_dict["wetvaporsource_in_wetvaporsource_n6"]=wetvaporsource_in_wetvaporsource_n6

	dryparticlesource_in_dryparticlesource_pond=pseudo_compartment()
	dryparticlesource_in_dryparticlesource_pond.name="dryparticlesource_in_dryparticlesource_pond"
	dryparticlesource_in_dryparticlesource_pond.containingvolumeelementname="dryparticlesource_pond"
	dryparticlesource_in_dryparticlesource_pond.parcel_name="pond"
	dryparticlesource_in_dryparticlesource_pond.parcel_points="p7 p8 p16 p14"
	dryparticlesource_in_dryparticlesource_pond.parcel_area=465187.5
	dryparticlesource_in_dryparticlesource_pond.exterior_boundary=1520.1727036425948
	dryparticlesource_in_dryparticlesource_pond.deposition_rate={}
	dryparticlesource_in_dryparticlesource_pond.category="pseudosource | dry | particle"
	comp_objects_dict["dryparticlesource_in_dryparticlesource_pond"]=dryparticlesource_in_dryparticlesource_pond

	dryvaporsource_in_dryvaporsource_pond=pseudo_compartment()
	dryvaporsource_in_dryvaporsource_pond.name="dryvaporsource_in_dryvaporsource_pond"
	dryvaporsource_in_dryvaporsource_pond.containingvolumeelementname="dryvaporsource_pond"
	dryvaporsource_in_dryvaporsource_pond.parcel_name="pond"
	dryvaporsource_in_dryvaporsource_pond.parcel_points="p7 p8 p16 p14"
	dryvaporsource_in_dryvaporsource_pond.parcel_area=465187.5
	dryvaporsource_in_dryvaporsource_pond.exterior_boundary=1520.1727036425948
	dryvaporsource_in_dryvaporsource_pond.deposition_rate={}
	dryvaporsource_in_dryvaporsource_pond.category="pseudosource | dry | vapor"
	comp_objects_dict["dryvaporsource_in_dryvaporsource_pond"]=dryvaporsource_in_dryvaporsource_pond

	wetparticlesource_in_wetparticlesource_pond=pseudo_compartment()
	wetparticlesource_in_wetparticlesource_pond.name="wetparticlesource_in_wetparticlesource_pond"
	wetparticlesource_in_wetparticlesource_pond.containingvolumeelementname="wetparticlesource_pond"
	wetparticlesource_in_wetparticlesource_pond.parcel_name="pond"
	wetparticlesource_in_wetparticlesource_pond.parcel_points="p7 p8 p16 p14"
	wetparticlesource_in_wetparticlesource_pond.parcel_area=465187.5
	wetparticlesource_in_wetparticlesource_pond.exterior_boundary=1520.1727036425948
	wetparticlesource_in_wetparticlesource_pond.deposition_rate={}
	wetparticlesource_in_wetparticlesource_pond.category="pseudosource | wet | particle"
	comp_objects_dict["wetparticlesource_in_wetparticlesource_pond"]=wetparticlesource_in_wetparticlesource_pond

	wetvaporsource_in_wetvaporsource_pond=pseudo_compartment()
	wetvaporsource_in_wetvaporsource_pond.name="wetvaporsource_in_wetvaporsource_pond"
	wetvaporsource_in_wetvaporsource_pond.containingvolumeelementname="wetvaporsource_pond"
	wetvaporsource_in_wetvaporsource_pond.parcel_name="pond"
	wetvaporsource_in_wetvaporsource_pond.parcel_points="p7 p8 p16 p14"
	wetvaporsource_in_wetvaporsource_pond.parcel_area=465187.5
	wetvaporsource_in_wetvaporsource_pond.exterior_boundary=1520.1727036425948
	wetvaporsource_in_wetvaporsource_pond.deposition_rate={}
	wetvaporsource_in_wetvaporsource_pond.category="pseudosource | wet | vapor"
	comp_objects_dict["wetvaporsource_in_wetvaporsource_pond"]=wetvaporsource_in_wetvaporsource_pond


	try:
		soil_surface_in_surfsoil_source.totalerosionrate_kg_m2_day=1.13848064422184e-02
	except:
		pass
	try:
		soil_surface_in_surfsoil_n1.totalerosionrate_kg_m2_day=5.74032731904327e-03
	except:
		pass
	try:
		soil_surface_in_surfsoil_n6.totalerosionrate_kg_m2_day=1.20143641903568e-02
	except:
		pass
	try:
		soil_surface_in_surfsoil_n7.totalerosionrate_kg_m2_day=5.58018961632054e-03
	except:
		pass
	try:
		soil_surface_in_surfsoil_n3.totalerosionrate_kg_m2_day=4.15059734807294e-03
	except:
		pass
	try:
		soil_surface_in_surfsoil_n4.totalerosionrate_kg_m2_day=3.33104780095033e-03
	except:
		pass
	try:
		soil_surface_in_surfsoil_n5.totalerosionrate_kg_m2_day=2.11585737790382e-03
	except:
		pass
	try:
		soil_surface_in_surfsoil_s1.totalerosionrate_kg_m2_day=5.74032731904327e-03
	except:
		pass
	try:
		soil_surface_in_surfsoil_s4.totalerosionrate_kg_m2_day=3.33104780095033e-03
	except:
		pass
	try:
		soil_surface_in_surfsoil_s5.totalerosionrate_kg_m2_day=2.11585737790382e-03
	except:
		pass
	try:
		surface_water_in_sw_pond.algaedensityinwatercolumn_g_l=0.0025
	except:
		pass
	try:
		surface_water_in_sw_pond.chlorideconcentration_mg_l=8
	except:
		pass
	try:
		surface_water_in_sw_pond.chlorophyllconcentration_mg_l=0.0029
	except:
		pass
	try:
		surface_water_in_sw_pond.organiccarboncontent=0.02
	except:
		pass
	try:
		surface_water_in_sw_pond.ph=7.3
	except:
		pass
	try:
		surface_water_in_sw_pond.suspendedsedimentconcentration=0.05
	except:
		pass
	try:
		surface_water_in_sw_pond.watertemperature_k=298
	except:
		pass
	try:
		surface_water_in_sw_pond.flushes_per_year=12.1666666666667
	except:
		pass
	try:
		surface_water_in_sw_pond.isflowing=False
	except:
		pass
	try:
		surface_water_in_sw_pond.currentvelocity=0
	except:
		pass
	try:
		sediment_in_sed_pond.organiccarboncontent=0.02
	except:
		pass
	try:
		sediment_in_sed_pond.ph=7.3
	except:
		pass
	try:
		sediment_in_sed_pond.rho=2600
	except:
		pass
	try:
		sediment_in_sed_pond.sedimentresuspensionvelocity=6.68799700375953e-05
	except:
		pass
	try:
		macrophyte_in_sw_pond.biomassperarea_kg_m2=0.5
	except:
		pass
	try:
		macrophyte_in_sw_pond.fractiondietalgae=0
	except:
		pass
	try:
		macrophyte_in_sw_pond.fractiondietmacrophyte=0
	except:
		pass
	try:
		macrophyte_in_sw_pond.fractiondietzooplankton=0
	except:
		pass
	try:
		macrophyte_in_sw_pond.fractiondietbenthicinvertebrate=0
	except:
		pass
	try:
		macrophyte_in_sw_pond.fractiondietfishherbivore=0
	except:
		pass
	try:
		macrophyte_in_sw_pond.fractiondietfishbenthicomnivore=0
	except:
		pass
	try:
		macrophyte_in_sw_pond.fractiondietfishomnivore=0
	except:
		pass
	try:
		macrophyte_in_sw_pond.fractiondietfishbenthiccarnivore=0
	except:
		pass
	try:
		macrophyte_in_sw_pond.fractiondietfishcarnivore=0
	except:
		pass
	try:
		zooplankton_in_sw_pond.biomassperarea_kg_m2=0.00636
	except:
		pass
	try:
		zooplankton_in_sw_pond.bw=0.000000057
	except:
		pass
	try:
		zooplankton_in_sw_pond.fractiondietalgae=1
	except:
		pass
	try:
		zooplankton_in_sw_pond.fractiondietmacrophyte=0
	except:
		pass
	try:
		zooplankton_in_sw_pond.fractiondietzooplankton=0
	except:
		pass
	try:
		zooplankton_in_sw_pond.fractiondietbenthicinvertebrate=0
	except:
		pass
	try:
		zooplankton_in_sw_pond.fractiondietfishherbivore=0
	except:
		pass
	try:
		zooplankton_in_sw_pond.fractiondietfishbenthicomnivore=0
	except:
		pass
	try:
		zooplankton_in_sw_pond.fractiondietfishomnivore=0
	except:
		pass
	try:
		zooplankton_in_sw_pond.fractiondietfishbenthiccarnivore=0
	except:
		pass
	try:
		zooplankton_in_sw_pond.fractiondietfishcarnivore=0
	except:
		pass
	try:
		benthic_invertebrate_in_sed_pond.biomassperarea_kg_m2=0.02
	except:
		pass
	try:
		benthic_invertebrate_in_sed_pond.bw=0.000255
	except:
		pass
	try:
		benthic_invertebrate_in_sed_pond.fractiondietalgae=0
	except:
		pass
	try:
		benthic_invertebrate_in_sed_pond.fractiondietmacrophyte=0
	except:
		pass
	try:
		benthic_invertebrate_in_sed_pond.fractiondietzooplankton=0
	except:
		pass
	try:
		benthic_invertebrate_in_sed_pond.fractiondietbenthicinvertebrate=0
	except:
		pass
	try:
		benthic_invertebrate_in_sed_pond.fractiondietfishherbivore=0
	except:
		pass
	try:
		benthic_invertebrate_in_sed_pond.fractiondietfishbenthicomnivore=0
	except:
		pass
	try:
		benthic_invertebrate_in_sed_pond.fractiondietfishomnivore=0
	except:
		pass
	try:
		benthic_invertebrate_in_sed_pond.fractiondietfishbenthiccarnivore=0
	except:
		pass
	try:
		benthic_invertebrate_in_sed_pond.fractiondietfishcarnivore=0
	except:
		pass
	try:
		water_column_herbivore_in_sw_pond.biomassperarea_kg_m2=0.002
	except:
		pass
	try:
		water_column_herbivore_in_sw_pond.bw=0.025
	except:
		pass
	try:
		water_column_herbivore_in_sw_pond.fractiondietalgae=0
	except:
		pass
	try:
		water_column_herbivore_in_sw_pond.fractiondietmacrophyte=0
	except:
		pass
	try:
		water_column_herbivore_in_sw_pond.fractiondietzooplankton=1
	except:
		pass
	try:
		water_column_herbivore_in_sw_pond.fractiondietbenthicinvertebrate=0
	except:
		pass
	try:
		water_column_herbivore_in_sw_pond.fractiondietfishherbivore=0
	except:
		pass
	try:
		water_column_herbivore_in_sw_pond.fractiondietfishbenthicomnivore=0
	except:
		pass
	try:
		water_column_herbivore_in_sw_pond.fractiondietfishomnivore=0
	except:
		pass
	try:
		water_column_herbivore_in_sw_pond.fractiondietfishbenthiccarnivore=0
	except:
		pass
	try:
		water_column_herbivore_in_sw_pond.fractiondietfishcarnivore=0
	except:
		pass
	try:
		benthic_omnivore_in_sed_pond.biomassperarea_kg_m2=0.002
	except:
		pass
	try:
		benthic_omnivore_in_sed_pond.bw=0.25
	except:
		pass
	try:
		benthic_omnivore_in_sed_pond.fractiondietalgae=0
	except:
		pass
	try:
		benthic_omnivore_in_sed_pond.fractiondietmacrophyte=0
	except:
		pass
	try:
		benthic_omnivore_in_sed_pond.fractiondietzooplankton=0
	except:
		pass
	try:
		benthic_omnivore_in_sed_pond.fractiondietbenthicinvertebrate=1
	except:
		pass
	try:
		benthic_omnivore_in_sed_pond.fractiondietfishherbivore=0
	except:
		pass
	try:
		benthic_omnivore_in_sed_pond.fractiondietfishbenthicomnivore=0
	except:
		pass
	try:
		benthic_omnivore_in_sed_pond.fractiondietfishomnivore=0
	except:
		pass
	try:
		benthic_omnivore_in_sed_pond.fractiondietfishbenthiccarnivore=0
	except:
		pass
	try:
		benthic_omnivore_in_sed_pond.fractiondietfishcarnivore=0
	except:
		pass
	try:
		water_column_omnivore_in_sw_pond.biomassperarea_kg_m2=0.0005
	except:
		pass
	try:
		water_column_omnivore_in_sw_pond.bw=0.25
	except:
		pass
	try:
		water_column_omnivore_in_sw_pond.fractiondietalgae=0
	except:
		pass
	try:
		water_column_omnivore_in_sw_pond.fractiondietmacrophyte=0
	except:
		pass
	try:
		water_column_omnivore_in_sw_pond.fractiondietzooplankton=0
	except:
		pass
	try:
		water_column_omnivore_in_sw_pond.fractiondietbenthicinvertebrate=0
	except:
		pass
	try:
		water_column_omnivore_in_sw_pond.fractiondietfishherbivore=1
	except:
		pass
	try:
		water_column_omnivore_in_sw_pond.fractiondietfishbenthicomnivore=0
	except:
		pass
	try:
		water_column_omnivore_in_sw_pond.fractiondietfishomnivore=0
	except:
		pass
	try:
		water_column_omnivore_in_sw_pond.fractiondietfishbenthiccarnivore=0
	except:
		pass
	try:
		water_column_omnivore_in_sw_pond.fractiondietfishcarnivore=0
	except:
		pass
	try:
		benthic_carnivore_in_sed_pond.biomassperarea_kg_m2=0.001
	except:
		pass
	try:
		benthic_carnivore_in_sed_pond.bw=2
	except:
		pass
	try:
		benthic_carnivore_in_sed_pond.fractiondietalgae=0
	except:
		pass
	try:
		benthic_carnivore_in_sed_pond.fractiondietmacrophyte=0
	except:
		pass
	try:
		benthic_carnivore_in_sed_pond.fractiondietzooplankton=0
	except:
		pass
	try:
		benthic_carnivore_in_sed_pond.fractiondietbenthicinvertebrate=0.5
	except:
		pass
	try:
		benthic_carnivore_in_sed_pond.fractiondietfishherbivore=0
	except:
		pass
	try:
		benthic_carnivore_in_sed_pond.fractiondietfishbenthicomnivore=0.5
	except:
		pass
	try:
		benthic_carnivore_in_sed_pond.fractiondietfishomnivore=0
	except:
		pass
	try:
		benthic_carnivore_in_sed_pond.fractiondietfishbenthiccarnivore=0
	except:
		pass
	try:
		benthic_carnivore_in_sed_pond.fractiondietfishcarnivore=0
	except:
		pass
	try:
		water_column_carnivore_in_sw_pond.biomassperarea_kg_m2=0.0002
	except:
		pass
	try:
		water_column_carnivore_in_sw_pond.bw=2
	except:
		pass
	try:
		water_column_carnivore_in_sw_pond.fractiondietalgae=0
	except:
		pass
	try:
		water_column_carnivore_in_sw_pond.fractiondietmacrophyte=0
	except:
		pass
	try:
		water_column_carnivore_in_sw_pond.fractiondietzooplankton=0
	except:
		pass
	try:
		water_column_carnivore_in_sw_pond.fractiondietbenthicinvertebrate=0
	except:
		pass
	try:
		water_column_carnivore_in_sw_pond.fractiondietfishherbivore=0
	except:
		pass
	try:
		water_column_carnivore_in_sw_pond.fractiondietfishbenthicomnivore=0
	except:
		pass
	try:
		water_column_carnivore_in_sw_pond.fractiondietfishomnivore=1
	except:
		pass
	try:
		water_column_carnivore_in_sw_pond.fractiondietfishbenthiccarnivore=0
	except:
		pass
	try:
		water_column_carnivore_in_sw_pond.fractiondietfishcarnivore=0
	except:
		pass
	try:
		air_in_air_source.dustload=0.0000000615
	except:
		pass
	try:
		air_in_air_n1.dustload=0.0000000615
	except:
		pass
	try:
		air_in_air_n6.dustload=0.0000000615
	except:
		pass
	try:
		air_in_air_n7.dustload=0.0000000615
	except:
		pass
	try:
		air_in_air_n3.dustload=0.0000000615
	except:
		pass
	try:
		air_in_air_n4.dustload=0.0000000615
	except:
		pass
	try:
		air_in_air_n5.dustload=0.0000000615
	except:
		pass
	try:
		air_in_air_s1.dustload=0.0000000615
	except:
		pass
	try:
		air_in_air_pond.dustload=0.0000000615
	except:
		pass
	try:
		air_in_air_s4.dustload=0.0000000615
	except:
		pass
	try:
		air_in_air_s5.dustload=0.0000000615
	except:
		pass
	try:
		air_in_air_source.airdensity_g_cm3=0.0012
	except:
		pass
	try:
		air_in_air_n1.airdensity_g_cm3=0.0012
	except:
		pass
	try:
		air_in_air_n6.airdensity_g_cm3=0.0012
	except:
		pass
	try:
		air_in_air_n7.airdensity_g_cm3=0.0012
	except:
		pass
	try:
		air_in_air_n3.airdensity_g_cm3=0.0012
	except:
		pass
	try:
		air_in_air_n4.airdensity_g_cm3=0.0012
	except:
		pass
	try:
		air_in_air_n5.airdensity_g_cm3=0.0012
	except:
		pass
	try:
		air_in_air_s1.airdensity_g_cm3=0.0012
	except:
		pass
	try:
		air_in_air_pond.airdensity_g_cm3=0.0012
	except:
		pass
	try:
		air_in_air_s4.airdensity_g_cm3=0.0012
	except:
		pass
	try:
		air_in_air_s5.airdensity_g_cm3=0.0012
	except:
		pass
	try:
		air_in_air_source.dustdensity=1400
	except:
		pass
	try:
		air_in_air_n1.dustdensity=1400
	except:
		pass
	try:
		air_in_air_n6.dustdensity=1400
	except:
		pass
	try:
		air_in_air_n7.dustdensity=1400
	except:
		pass
	try:
		air_in_air_n3.dustdensity=1400
	except:
		pass
	try:
		air_in_air_n4.dustdensity=1400
	except:
		pass
	try:
		air_in_air_n5.dustdensity=1400
	except:
		pass
	try:
		air_in_air_s1.dustdensity=1400
	except:
		pass
	try:
		air_in_air_pond.dustdensity=1400
	except:
		pass
	try:
		air_in_air_s4.dustdensity=1400
	except:
		pass
	try:
		air_in_air_s5.dustdensity=1400
	except:
		pass
	try:
		air_in_air_source.fractionorganicmatteronparticulates=0.2
	except:
		pass
	try:
		air_in_air_n1.fractionorganicmatteronparticulates=0.2
	except:
		pass
	try:
		air_in_air_n6.fractionorganicmatteronparticulates=0.2
	except:
		pass
	try:
		air_in_air_n7.fractionorganicmatteronparticulates=0.2
	except:
		pass
	try:
		air_in_air_n3.fractionorganicmatteronparticulates=0.2
	except:
		pass
	try:
		air_in_air_n4.fractionorganicmatteronparticulates=0.2
	except:
		pass
	try:
		air_in_air_n5.fractionorganicmatteronparticulates=0.2
	except:
		pass
	try:
		air_in_air_s1.fractionorganicmatteronparticulates=0.2
	except:
		pass
	try:
		air_in_air_pond.fractionorganicmatteronparticulates=0.2
	except:
		pass
	try:
		air_in_air_s4.fractionorganicmatteronparticulates=0.2
	except:
		pass
	try:
		air_in_air_s5.fractionorganicmatteronparticulates=0.2
	except:
		pass
	try:
		soil_surface_in_surfsoil_source.volumefraction_vapor=0.28
	except:
		pass
	try:
		soil_surface_in_surfsoil_n1.volumefraction_vapor=0.28
	except:
		pass
	try:
		soil_surface_in_surfsoil_n6.volumefraction_vapor=0.28
	except:
		pass
	try:
		soil_surface_in_surfsoil_n7.volumefraction_vapor=0.28
	except:
		pass
	try:
		soil_surface_in_surfsoil_n3.volumefraction_vapor=0.28
	except:
		pass
	try:
		soil_surface_in_surfsoil_n4.volumefraction_vapor=0.28
	except:
		pass
	try:
		soil_surface_in_surfsoil_n5.volumefraction_vapor=0.28
	except:
		pass
	try:
		soil_surface_in_surfsoil_s1.volumefraction_vapor=0.28
	except:
		pass
	try:
		soil_surface_in_surfsoil_s4.volumefraction_vapor=0.28
	except:
		pass
	try:
		soil_surface_in_surfsoil_s5.volumefraction_vapor=0.28
	except:
		pass
	try:
		soil_surface_in_surfsoil_source.averageverticalvelocity=0.000821917808219178
	except:
		pass
	try:
		soil_surface_in_surfsoil_n1.averageverticalvelocity=0.000821917808219178
	except:
		pass
	try:
		soil_surface_in_surfsoil_n6.averageverticalvelocity=0.000821917808219178
	except:
		pass
	try:
		soil_surface_in_surfsoil_n7.averageverticalvelocity=0.000821917808219178
	except:
		pass
	try:
		soil_surface_in_surfsoil_n3.averageverticalvelocity=0.000821917808219178
	except:
		pass
	try:
		soil_surface_in_surfsoil_n4.averageverticalvelocity=0.000821917808219178
	except:
		pass
	try:
		soil_surface_in_surfsoil_n5.averageverticalvelocity=0.000821917808219178
	except:
		pass
	try:
		soil_surface_in_surfsoil_s1.averageverticalvelocity=0.000821917808219178
	except:
		pass
	try:
		soil_surface_in_surfsoil_s4.averageverticalvelocity=0.000821917808219178
	except:
		pass
	try:
		soil_surface_in_surfsoil_s5.averageverticalvelocity=0.000821917808219178
	except:
		pass
	try:
		soil_surface_in_surfsoil_source.airsoilboundarythickness=0.005
	except:
		pass
	try:
		soil_surface_in_surfsoil_n1.airsoilboundarythickness=0.005
	except:
		pass
	try:
		soil_surface_in_surfsoil_n6.airsoilboundarythickness=0.005
	except:
		pass
	try:
		soil_surface_in_surfsoil_n7.airsoilboundarythickness=0.005
	except:
		pass
	try:
		soil_surface_in_surfsoil_n3.airsoilboundarythickness=0.005
	except:
		pass
	try:
		soil_surface_in_surfsoil_n4.airsoilboundarythickness=0.005
	except:
		pass
	try:
		soil_surface_in_surfsoil_n5.airsoilboundarythickness=0.005
	except:
		pass
	try:
		soil_surface_in_surfsoil_s1.airsoilboundarythickness=0.005
	except:
		pass
	try:
		soil_surface_in_surfsoil_s4.airsoilboundarythickness=0.005
	except:
		pass
	try:
		soil_surface_in_surfsoil_s5.airsoilboundarythickness=0.005
	except:
		pass
	try:
		soil_surface_in_surfsoil_source.rho=2600
	except:
		pass
	try:
		soil_surface_in_surfsoil_n1.rho=2600
	except:
		pass
	try:
		soil_surface_in_surfsoil_n6.rho=2600
	except:
		pass
	try:
		soil_surface_in_surfsoil_n7.rho=2600
	except:
		pass
	try:
		soil_surface_in_surfsoil_n3.rho=2600
	except:
		pass
	try:
		soil_surface_in_surfsoil_n4.rho=2600
	except:
		pass
	try:
		soil_surface_in_surfsoil_n5.rho=2600
	except:
		pass
	try:
		soil_surface_in_surfsoil_s1.rho=2600
	except:
		pass
	try:
		soil_surface_in_surfsoil_s4.rho=2600
	except:
		pass
	try:
		soil_surface_in_surfsoil_s5.rho=2600
	except:
		pass
	try:
		soil_surface_in_surfsoil_source.fractionofareaavailableforerosion=1
	except:
		pass
	try:
		soil_surface_in_surfsoil_n1.fractionofareaavailableforerosion=1
	except:
		pass
	try:
		soil_surface_in_surfsoil_n6.fractionofareaavailableforerosion=1
	except:
		pass
	try:
		soil_surface_in_surfsoil_n7.fractionofareaavailableforerosion=1
	except:
		pass
	try:
		soil_surface_in_surfsoil_n3.fractionofareaavailableforerosion=1
	except:
		pass
	try:
		soil_surface_in_surfsoil_n4.fractionofareaavailableforerosion=1
	except:
		pass
	try:
		soil_surface_in_surfsoil_n5.fractionofareaavailableforerosion=1
	except:
		pass
	try:
		soil_surface_in_surfsoil_s1.fractionofareaavailableforerosion=1
	except:
		pass
	try:
		soil_surface_in_surfsoil_s4.fractionofareaavailableforerosion=1
	except:
		pass
	try:
		soil_surface_in_surfsoil_s5.fractionofareaavailableforerosion=1
	except:
		pass
	try:
		soil_surface_in_surfsoil_source.fractionofareaavailableforrunoff=1
	except:
		pass
	try:
		soil_surface_in_surfsoil_n1.fractionofareaavailableforrunoff=1
	except:
		pass
	try:
		soil_surface_in_surfsoil_n6.fractionofareaavailableforrunoff=1
	except:
		pass
	try:
		soil_surface_in_surfsoil_n7.fractionofareaavailableforrunoff=1
	except:
		pass
	try:
		soil_surface_in_surfsoil_n3.fractionofareaavailableforrunoff=1
	except:
		pass
	try:
		soil_surface_in_surfsoil_n4.fractionofareaavailableforrunoff=1
	except:
		pass
	try:
		soil_surface_in_surfsoil_n5.fractionofareaavailableforrunoff=1
	except:
		pass
	try:
		soil_surface_in_surfsoil_s1.fractionofareaavailableforrunoff=1
	except:
		pass
	try:
		soil_surface_in_surfsoil_s4.fractionofareaavailableforrunoff=1
	except:
		pass
	try:
		soil_surface_in_surfsoil_s5.fractionofareaavailableforrunoff=1
	except:
		pass
	try:
		soil_surface_in_surfsoil_source.fractionofareaavailableforverticaldiffusion=1
	except:
		pass
	try:
		soil_surface_in_surfsoil_n1.fractionofareaavailableforverticaldiffusion=1
	except:
		pass
	try:
		soil_surface_in_surfsoil_n6.fractionofareaavailableforverticaldiffusion=1
	except:
		pass
	try:
		soil_surface_in_surfsoil_n7.fractionofareaavailableforverticaldiffusion=1
	except:
		pass
	try:
		soil_surface_in_surfsoil_n3.fractionofareaavailableforverticaldiffusion=1
	except:
		pass
	try:
		soil_surface_in_surfsoil_n4.fractionofareaavailableforverticaldiffusion=1
	except:
		pass
	try:
		soil_surface_in_surfsoil_n5.fractionofareaavailableforverticaldiffusion=1
	except:
		pass
	try:
		soil_surface_in_surfsoil_s1.fractionofareaavailableforverticaldiffusion=1
	except:
		pass
	try:
		soil_surface_in_surfsoil_s4.fractionofareaavailableforverticaldiffusion=1
	except:
		pass
	try:
		soil_surface_in_surfsoil_s5.fractionofareaavailableforverticaldiffusion=1
	except:
		pass
	try:
		soil_surface_in_surfsoil_source.fractionsand=0.25
	except:
		pass
	try:
		soil_surface_in_surfsoil_n1.fractionsand=0.25
	except:
		pass
	try:
		soil_surface_in_surfsoil_n6.fractionsand=0.25
	except:
		pass
	try:
		soil_surface_in_surfsoil_n7.fractionsand=0.25
	except:
		pass
	try:
		soil_surface_in_surfsoil_n3.fractionsand=0.25
	except:
		pass
	try:
		soil_surface_in_surfsoil_n4.fractionsand=0.25
	except:
		pass
	try:
		soil_surface_in_surfsoil_n5.fractionsand=0.25
	except:
		pass
	try:
		soil_surface_in_surfsoil_s1.fractionsand=0.25
	except:
		pass
	try:
		soil_surface_in_surfsoil_s4.fractionsand=0.25
	except:
		pass
	try:
		soil_surface_in_surfsoil_s5.fractionsand=0.25
	except:
		pass
	try:
		soil_surface_in_surfsoil_source.organiccarboncontent=0.008
	except:
		pass
	try:
		soil_surface_in_surfsoil_n1.organiccarboncontent=0.008
	except:
		pass
	try:
		soil_surface_in_surfsoil_n6.organiccarboncontent=0.008
	except:
		pass
	try:
		soil_surface_in_surfsoil_n7.organiccarboncontent=0.008
	except:
		pass
	try:
		soil_surface_in_surfsoil_n3.organiccarboncontent=0.008
	except:
		pass
	try:
		soil_surface_in_surfsoil_n4.organiccarboncontent=0.008
	except:
		pass
	try:
		soil_surface_in_surfsoil_n5.organiccarboncontent=0.008
	except:
		pass
	try:
		soil_surface_in_surfsoil_s1.organiccarboncontent=0.008
	except:
		pass
	try:
		soil_surface_in_surfsoil_s4.organiccarboncontent=0.008
	except:
		pass
	try:
		soil_surface_in_surfsoil_s5.organiccarboncontent=0.008
	except:
		pass
	try:
		soil_surface_in_surfsoil_source.ph=6.8
	except:
		pass
	try:
		soil_surface_in_surfsoil_n1.ph=6.8
	except:
		pass
	try:
		soil_surface_in_surfsoil_n6.ph=6.8
	except:
		pass
	try:
		soil_surface_in_surfsoil_n7.ph=6.8
	except:
		pass
	try:
		soil_surface_in_surfsoil_n3.ph=6.8
	except:
		pass
	try:
		soil_surface_in_surfsoil_n4.ph=6.8
	except:
		pass
	try:
		soil_surface_in_surfsoil_n5.ph=6.8
	except:
		pass
	try:
		soil_surface_in_surfsoil_s1.ph=6.8
	except:
		pass
	try:
		soil_surface_in_surfsoil_s4.ph=6.8
	except:
		pass
	try:
		soil_surface_in_surfsoil_s5.ph=6.8
	except:
		pass
	try:
		soil_surface_in_surfsoil_source.totalrunoffrate_m3_m2_day=1.6438e-03
	except:
		pass
	try:
		soil_surface_in_surfsoil_n1.totalrunoffrate_m3_m2_day=1.6438e-03
	except:
		pass
	try:
		soil_surface_in_surfsoil_n6.totalrunoffrate_m3_m2_day=1.6438e-03
	except:
		pass
	try:
		soil_surface_in_surfsoil_n7.totalrunoffrate_m3_m2_day=1.6438e-03
	except:
		pass
	try:
		soil_surface_in_surfsoil_n3.totalrunoffrate_m3_m2_day=1.6438e-03
	except:
		pass
	try:
		soil_surface_in_surfsoil_n4.totalrunoffrate_m3_m2_day=1.6438e-03
	except:
		pass
	try:
		soil_surface_in_surfsoil_n5.totalrunoffrate_m3_m2_day=1.6438e-03
	except:
		pass
	try:
		soil_surface_in_surfsoil_s1.totalrunoffrate_m3_m2_day=1.6438e-03
	except:
		pass
	try:
		soil_surface_in_surfsoil_s4.totalrunoffrate_m3_m2_day=1.6438e-03
	except:
		pass
	try:
		soil_surface_in_surfsoil_s5.totalrunoffrate_m3_m2_day=1.6438e-03
	except:
		pass
	try:
		soil_surface_in_surfsoil_source.volumefraction_liquid=0.19
	except:
		pass
	try:
		soil_surface_in_surfsoil_n1.volumefraction_liquid=0.19
	except:
		pass
	try:
		soil_surface_in_surfsoil_n6.volumefraction_liquid=0.19
	except:
		pass
	try:
		soil_surface_in_surfsoil_n7.volumefraction_liquid=0.19
	except:
		pass
	try:
		soil_surface_in_surfsoil_n3.volumefraction_liquid=0.19
	except:
		pass
	try:
		soil_surface_in_surfsoil_n4.volumefraction_liquid=0.19
	except:
		pass
	try:
		soil_surface_in_surfsoil_n5.volumefraction_liquid=0.19
	except:
		pass
	try:
		soil_surface_in_surfsoil_s1.volumefraction_liquid=0.19
	except:
		pass
	try:
		soil_surface_in_surfsoil_s4.volumefraction_liquid=0.19
	except:
		pass
	try:
		soil_surface_in_surfsoil_s5.volumefraction_liquid=0.19
	except:
		pass
	try:
		soil_root_zone_in_rootsoil_source.volumefraction_vapor=0.25
	except:
		pass
	try:
		soil_root_zone_in_rootsoil_n1.volumefraction_vapor=0.25
	except:
		pass
	try:
		soil_root_zone_in_rootsoil_n6.volumefraction_vapor=0.25
	except:
		pass
	try:
		soil_root_zone_in_rootsoil_n7.volumefraction_vapor=0.25
	except:
		pass
	try:
		soil_root_zone_in_rootsoil_n3.volumefraction_vapor=0.25
	except:
		pass
	try:
		soil_root_zone_in_rootsoil_n4.volumefraction_vapor=0.25
	except:
		pass
	try:
		soil_root_zone_in_rootsoil_n5.volumefraction_vapor=0.25
	except:
		pass
	try:
		soil_root_zone_in_rootsoil_s1.volumefraction_vapor=0.25
	except:
		pass
	try:
		soil_root_zone_in_rootsoil_s4.volumefraction_vapor=0.25
	except:
		pass
	try:
		soil_root_zone_in_rootsoil_s5.volumefraction_vapor=0.25
	except:
		pass
	try:
		soil_root_zone_in_rootsoil_source.averageverticalvelocity=0.000821917808219178
	except:
		pass
	try:
		soil_root_zone_in_rootsoil_n1.averageverticalvelocity=0.000821917808219178
	except:
		pass
	try:
		soil_root_zone_in_rootsoil_n6.averageverticalvelocity=0.000821917808219178
	except:
		pass
	try:
		soil_root_zone_in_rootsoil_n7.averageverticalvelocity=0.000821917808219178
	except:
		pass
	try:
		soil_root_zone_in_rootsoil_n3.averageverticalvelocity=0.000821917808219178
	except:
		pass
	try:
		soil_root_zone_in_rootsoil_n4.averageverticalvelocity=0.000821917808219178
	except:
		pass
	try:
		soil_root_zone_in_rootsoil_n5.averageverticalvelocity=0.000821917808219178
	except:
		pass
	try:
		soil_root_zone_in_rootsoil_s1.averageverticalvelocity=0.000821917808219178
	except:
		pass
	try:
		soil_root_zone_in_rootsoil_s4.averageverticalvelocity=0.000821917808219178
	except:
		pass
	try:
		soil_root_zone_in_rootsoil_s5.averageverticalvelocity=0.000821917808219178
	except:
		pass
	try:
		soil_root_zone_in_rootsoil_source.rho=2600
	except:
		pass
	try:
		soil_root_zone_in_rootsoil_n1.rho=2600
	except:
		pass
	try:
		soil_root_zone_in_rootsoil_n6.rho=2600
	except:
		pass
	try:
		soil_root_zone_in_rootsoil_n7.rho=2600
	except:
		pass
	try:
		soil_root_zone_in_rootsoil_n3.rho=2600
	except:
		pass
	try:
		soil_root_zone_in_rootsoil_n4.rho=2600
	except:
		pass
	try:
		soil_root_zone_in_rootsoil_n5.rho=2600
	except:
		pass
	try:
		soil_root_zone_in_rootsoil_s1.rho=2600
	except:
		pass
	try:
		soil_root_zone_in_rootsoil_s4.rho=2600
	except:
		pass
	try:
		soil_root_zone_in_rootsoil_s5.rho=2600
	except:
		pass
	try:
		soil_root_zone_in_rootsoil_source.fractionsand=0.25
	except:
		pass
	try:
		soil_root_zone_in_rootsoil_n1.fractionsand=0.25
	except:
		pass
	try:
		soil_root_zone_in_rootsoil_n6.fractionsand=0.25
	except:
		pass
	try:
		soil_root_zone_in_rootsoil_n7.fractionsand=0.25
	except:
		pass
	try:
		soil_root_zone_in_rootsoil_n3.fractionsand=0.25
	except:
		pass
	try:
		soil_root_zone_in_rootsoil_n4.fractionsand=0.25
	except:
		pass
	try:
		soil_root_zone_in_rootsoil_n5.fractionsand=0.25
	except:
		pass
	try:
		soil_root_zone_in_rootsoil_s1.fractionsand=0.25
	except:
		pass
	try:
		soil_root_zone_in_rootsoil_s4.fractionsand=0.25
	except:
		pass
	try:
		soil_root_zone_in_rootsoil_s5.fractionsand=0.25
	except:
		pass
	try:
		soil_root_zone_in_rootsoil_source.organiccarboncontent=0.008
	except:
		pass
	try:
		soil_root_zone_in_rootsoil_n1.organiccarboncontent=0.008
	except:
		pass
	try:
		soil_root_zone_in_rootsoil_n6.organiccarboncontent=0.008
	except:
		pass
	try:
		soil_root_zone_in_rootsoil_n7.organiccarboncontent=0.008
	except:
		pass
	try:
		soil_root_zone_in_rootsoil_n3.organiccarboncontent=0.008
	except:
		pass
	try:
		soil_root_zone_in_rootsoil_n4.organiccarboncontent=0.008
	except:
		pass
	try:
		soil_root_zone_in_rootsoil_n5.organiccarboncontent=0.008
	except:
		pass
	try:
		soil_root_zone_in_rootsoil_s1.organiccarboncontent=0.008
	except:
		pass
	try:
		soil_root_zone_in_rootsoil_s4.organiccarboncontent=0.008
	except:
		pass
	try:
		soil_root_zone_in_rootsoil_s5.organiccarboncontent=0.008
	except:
		pass
	try:
		soil_root_zone_in_rootsoil_source.ph=6.8
	except:
		pass
	try:
		soil_root_zone_in_rootsoil_n1.ph=6.8
	except:
		pass
	try:
		soil_root_zone_in_rootsoil_n6.ph=6.8
	except:
		pass
	try:
		soil_root_zone_in_rootsoil_n7.ph=6.8
	except:
		pass
	try:
		soil_root_zone_in_rootsoil_n3.ph=6.8
	except:
		pass
	try:
		soil_root_zone_in_rootsoil_n4.ph=6.8
	except:
		pass
	try:
		soil_root_zone_in_rootsoil_n5.ph=6.8
	except:
		pass
	try:
		soil_root_zone_in_rootsoil_s1.ph=6.8
	except:
		pass
	try:
		soil_root_zone_in_rootsoil_s4.ph=6.8
	except:
		pass
	try:
		soil_root_zone_in_rootsoil_s5.ph=6.8
	except:
		pass
	try:
		soil_root_zone_in_rootsoil_source.volumefraction_liquid=0.21
	except:
		pass
	try:
		soil_root_zone_in_rootsoil_n1.volumefraction_liquid=0.21
	except:
		pass
	try:
		soil_root_zone_in_rootsoil_n6.volumefraction_liquid=0.21
	except:
		pass
	try:
		soil_root_zone_in_rootsoil_n7.volumefraction_liquid=0.21
	except:
		pass
	try:
		soil_root_zone_in_rootsoil_n3.volumefraction_liquid=0.21
	except:
		pass
	try:
		soil_root_zone_in_rootsoil_n4.volumefraction_liquid=0.21
	except:
		pass
	try:
		soil_root_zone_in_rootsoil_n5.volumefraction_liquid=0.21
	except:
		pass
	try:
		soil_root_zone_in_rootsoil_s1.volumefraction_liquid=0.21
	except:
		pass
	try:
		soil_root_zone_in_rootsoil_s4.volumefraction_liquid=0.21
	except:
		pass
	try:
		soil_root_zone_in_rootsoil_s5.volumefraction_liquid=0.21
	except:
		pass
	try:
		soil_vadose_zone_in_vadosesoil_source.volumefraction_vapor=0.22
	except:
		pass
	try:
		soil_vadose_zone_in_vadosesoil_n1.volumefraction_vapor=0.22
	except:
		pass
	try:
		soil_vadose_zone_in_vadosesoil_n6.volumefraction_vapor=0.22
	except:
		pass
	try:
		soil_vadose_zone_in_vadosesoil_n7.volumefraction_vapor=0.22
	except:
		pass
	try:
		soil_vadose_zone_in_vadosesoil_n3.volumefraction_vapor=0.22
	except:
		pass
	try:
		soil_vadose_zone_in_vadosesoil_n4.volumefraction_vapor=0.22
	except:
		pass
	try:
		soil_vadose_zone_in_vadosesoil_n5.volumefraction_vapor=0.22
	except:
		pass
	try:
		soil_vadose_zone_in_vadosesoil_s1.volumefraction_vapor=0.22
	except:
		pass
	try:
		soil_vadose_zone_in_vadosesoil_s4.volumefraction_vapor=0.22
	except:
		pass
	try:
		soil_vadose_zone_in_vadosesoil_s5.volumefraction_vapor=0.22
	except:
		pass
	try:
		soil_vadose_zone_in_vadosesoil_source.averageverticalvelocity=0.000821917808219178
	except:
		pass
	try:
		soil_vadose_zone_in_vadosesoil_n1.averageverticalvelocity=0.000821917808219178
	except:
		pass
	try:
		soil_vadose_zone_in_vadosesoil_n6.averageverticalvelocity=0.000821917808219178
	except:
		pass
	try:
		soil_vadose_zone_in_vadosesoil_n7.averageverticalvelocity=0.000821917808219178
	except:
		pass
	try:
		soil_vadose_zone_in_vadosesoil_n3.averageverticalvelocity=0.000821917808219178
	except:
		pass
	try:
		soil_vadose_zone_in_vadosesoil_n4.averageverticalvelocity=0.000821917808219178
	except:
		pass
	try:
		soil_vadose_zone_in_vadosesoil_n5.averageverticalvelocity=0.000821917808219178
	except:
		pass
	try:
		soil_vadose_zone_in_vadosesoil_s1.averageverticalvelocity=0.000821917808219178
	except:
		pass
	try:
		soil_vadose_zone_in_vadosesoil_s4.averageverticalvelocity=0.000821917808219178
	except:
		pass
	try:
		soil_vadose_zone_in_vadosesoil_s5.averageverticalvelocity=0.000821917808219178
	except:
		pass
	try:
		soil_vadose_zone_in_vadosesoil_source.rho=2600
	except:
		pass
	try:
		soil_vadose_zone_in_vadosesoil_n1.rho=2600
	except:
		pass
	try:
		soil_vadose_zone_in_vadosesoil_n6.rho=2600
	except:
		pass
	try:
		soil_vadose_zone_in_vadosesoil_n7.rho=2600
	except:
		pass
	try:
		soil_vadose_zone_in_vadosesoil_n3.rho=2600
	except:
		pass
	try:
		soil_vadose_zone_in_vadosesoil_n4.rho=2600
	except:
		pass
	try:
		soil_vadose_zone_in_vadosesoil_n5.rho=2600
	except:
		pass
	try:
		soil_vadose_zone_in_vadosesoil_s1.rho=2600
	except:
		pass
	try:
		soil_vadose_zone_in_vadosesoil_s4.rho=2600
	except:
		pass
	try:
		soil_vadose_zone_in_vadosesoil_s5.rho=2600
	except:
		pass
	try:
		soil_vadose_zone_in_vadosesoil_source.fractionsand=0.35
	except:
		pass
	try:
		soil_vadose_zone_in_vadosesoil_n1.fractionsand=0.35
	except:
		pass
	try:
		soil_vadose_zone_in_vadosesoil_n6.fractionsand=0.35
	except:
		pass
	try:
		soil_vadose_zone_in_vadosesoil_n7.fractionsand=0.35
	except:
		pass
	try:
		soil_vadose_zone_in_vadosesoil_n3.fractionsand=0.35
	except:
		pass
	try:
		soil_vadose_zone_in_vadosesoil_n4.fractionsand=0.35
	except:
		pass
	try:
		soil_vadose_zone_in_vadosesoil_n5.fractionsand=0.35
	except:
		pass
	try:
		soil_vadose_zone_in_vadosesoil_s1.fractionsand=0.35
	except:
		pass
	try:
		soil_vadose_zone_in_vadosesoil_s4.fractionsand=0.35
	except:
		pass
	try:
		soil_vadose_zone_in_vadosesoil_s5.fractionsand=0.35
	except:
		pass
	try:
		soil_vadose_zone_in_vadosesoil_source.organiccarboncontent=0.003
	except:
		pass
	try:
		soil_vadose_zone_in_vadosesoil_n1.organiccarboncontent=0.003
	except:
		pass
	try:
		soil_vadose_zone_in_vadosesoil_n6.organiccarboncontent=0.003
	except:
		pass
	try:
		soil_vadose_zone_in_vadosesoil_n7.organiccarboncontent=0.003
	except:
		pass
	try:
		soil_vadose_zone_in_vadosesoil_n3.organiccarboncontent=0.003
	except:
		pass
	try:
		soil_vadose_zone_in_vadosesoil_n4.organiccarboncontent=0.003
	except:
		pass
	try:
		soil_vadose_zone_in_vadosesoil_n5.organiccarboncontent=0.003
	except:
		pass
	try:
		soil_vadose_zone_in_vadosesoil_s1.organiccarboncontent=0.003
	except:
		pass
	try:
		soil_vadose_zone_in_vadosesoil_s4.organiccarboncontent=0.003
	except:
		pass
	try:
		soil_vadose_zone_in_vadosesoil_s5.organiccarboncontent=0.003
	except:
		pass
	try:
		soil_vadose_zone_in_vadosesoil_source.ph=6.8
	except:
		pass
	try:
		soil_vadose_zone_in_vadosesoil_n1.ph=6.8
	except:
		pass
	try:
		soil_vadose_zone_in_vadosesoil_n6.ph=6.8
	except:
		pass
	try:
		soil_vadose_zone_in_vadosesoil_n7.ph=6.8
	except:
		pass
	try:
		soil_vadose_zone_in_vadosesoil_n3.ph=6.8
	except:
		pass
	try:
		soil_vadose_zone_in_vadosesoil_n4.ph=6.8
	except:
		pass
	try:
		soil_vadose_zone_in_vadosesoil_n5.ph=6.8
	except:
		pass
	try:
		soil_vadose_zone_in_vadosesoil_s1.ph=6.8
	except:
		pass
	try:
		soil_vadose_zone_in_vadosesoil_s4.ph=6.8
	except:
		pass
	try:
		soil_vadose_zone_in_vadosesoil_s5.ph=6.8
	except:
		pass
	try:
		soil_vadose_zone_in_vadosesoil_source.volumefraction_liquid=0.21
	except:
		pass
	try:
		soil_vadose_zone_in_vadosesoil_n1.volumefraction_liquid=0.21
	except:
		pass
	try:
		soil_vadose_zone_in_vadosesoil_n6.volumefraction_liquid=0.21
	except:
		pass
	try:
		soil_vadose_zone_in_vadosesoil_n7.volumefraction_liquid=0.21
	except:
		pass
	try:
		soil_vadose_zone_in_vadosesoil_n3.volumefraction_liquid=0.21
	except:
		pass
	try:
		soil_vadose_zone_in_vadosesoil_n4.volumefraction_liquid=0.21
	except:
		pass
	try:
		soil_vadose_zone_in_vadosesoil_n5.volumefraction_liquid=0.21
	except:
		pass
	try:
		soil_vadose_zone_in_vadosesoil_s1.volumefraction_liquid=0.21
	except:
		pass
	try:
		soil_vadose_zone_in_vadosesoil_s4.volumefraction_liquid=0.21
	except:
		pass
	try:
		soil_vadose_zone_in_vadosesoil_s5.volumefraction_liquid=0.21
	except:
		pass
	try:
		groundwater_in_gw_source.fractionsand=0.4
	except:
		pass
	try:
		groundwater_in_gw_n1.fractionsand=0.4
	except:
		pass
	try:
		groundwater_in_gw_n6.fractionsand=0.4
	except:
		pass
	try:
		groundwater_in_gw_n7.fractionsand=0.4
	except:
		pass
	try:
		groundwater_in_gw_n3.fractionsand=0.4
	except:
		pass
	try:
		groundwater_in_gw_n4.fractionsand=0.4
	except:
		pass
	try:
		groundwater_in_gw_n5.fractionsand=0.4
	except:
		pass
	try:
		groundwater_in_gw_s1.fractionsand=0.4
	except:
		pass
	try:
		groundwater_in_gw_s4.fractionsand=0.4
	except:
		pass
	try:
		groundwater_in_gw_s5.fractionsand=0.4
	except:
		pass
	try:
		groundwater_in_gw_source.organiccarboncontent=0.004
	except:
		pass
	try:
		groundwater_in_gw_n1.organiccarboncontent=0.004
	except:
		pass
	try:
		groundwater_in_gw_n6.organiccarboncontent=0.004
	except:
		pass
	try:
		groundwater_in_gw_n7.organiccarboncontent=0.004
	except:
		pass
	try:
		groundwater_in_gw_n3.organiccarboncontent=0.004
	except:
		pass
	try:
		groundwater_in_gw_n4.organiccarboncontent=0.004
	except:
		pass
	try:
		groundwater_in_gw_n5.organiccarboncontent=0.004
	except:
		pass
	try:
		groundwater_in_gw_s1.organiccarboncontent=0.004
	except:
		pass
	try:
		groundwater_in_gw_s4.organiccarboncontent=0.004
	except:
		pass
	try:
		groundwater_in_gw_s5.organiccarboncontent=0.004
	except:
		pass
	try:
		groundwater_in_gw_source.ph=6.8
	except:
		pass
	try:
		groundwater_in_gw_n1.ph=6.8
	except:
		pass
	try:
		groundwater_in_gw_n6.ph=6.8
	except:
		pass
	try:
		groundwater_in_gw_n7.ph=6.8
	except:
		pass
	try:
		groundwater_in_gw_n3.ph=6.8
	except:
		pass
	try:
		groundwater_in_gw_n4.ph=6.8
	except:
		pass
	try:
		groundwater_in_gw_n5.ph=6.8
	except:
		pass
	try:
		groundwater_in_gw_s1.ph=6.8
	except:
		pass
	try:
		groundwater_in_gw_s4.ph=6.8
	except:
		pass
	try:
		groundwater_in_gw_s5.ph=6.8
	except:
		pass
	try:
		groundwater_in_gw_source.porosity=0.2
	except:
		pass
	try:
		groundwater_in_gw_n1.porosity=0.2
	except:
		pass
	try:
		groundwater_in_gw_n6.porosity=0.2
	except:
		pass
	try:
		groundwater_in_gw_n7.porosity=0.2
	except:
		pass
	try:
		groundwater_in_gw_n3.porosity=0.2
	except:
		pass
	try:
		groundwater_in_gw_n4.porosity=0.2
	except:
		pass
	try:
		groundwater_in_gw_n5.porosity=0.2
	except:
		pass
	try:
		groundwater_in_gw_s1.porosity=0.2
	except:
		pass
	try:
		groundwater_in_gw_s4.porosity=0.2
	except:
		pass
	try:
		groundwater_in_gw_s5.porosity=0.2
	except:
		pass
	try:
		groundwater_in_gw_source.rho=2600
	except:
		pass
	try:
		groundwater_in_gw_n1.rho=2600
	except:
		pass
	try:
		groundwater_in_gw_n6.rho=2600
	except:
		pass
	try:
		groundwater_in_gw_n7.rho=2600
	except:
		pass
	try:
		groundwater_in_gw_n3.rho=2600
	except:
		pass
	try:
		groundwater_in_gw_n4.rho=2600
	except:
		pass
	try:
		groundwater_in_gw_n5.rho=2600
	except:
		pass
	try:
		groundwater_in_gw_s1.rho=2600
	except:
		pass
	try:
		groundwater_in_gw_s4.rho=2600
	except:
		pass
	try:
		groundwater_in_gw_s5.rho=2600
	except:
		pass
	try:
		soil_surface_in_surfsoil_source.totalerosionrate_kg_m2_day=0
	except:
		pass
	try:
		soil_surface_in_surfsoil_source.totalrunoffrate_m3_m2_day=0
	except:
		pass

### note: this is to write other properties


#add pseudo source dep rates to pseudo compartments

	try:
		dryparticlesource_in_dryparticlesource_source.deposition_rate['chem_benzo_a_pyrene']=1e-11*dryparticlesource_in_dryparticlesource_source.parcel_area
	except:
		pass
	try:
		dryparticlesource_in_dryparticlesource_source.deposition_rate['chem_arsenic']=1e-11*dryparticlesource_in_dryparticlesource_source.parcel_area
	except:
		pass
	try:
		dryparticlesource_in_dryparticlesource_source.deposition_rate['chem_cadmium']=1e-11*dryparticlesource_in_dryparticlesource_source.parcel_area
	except:
		pass
	try:
		dryparticlesource_in_dryparticlesource_source.deposition_rate['chem_2_3_7_8_tcdd']=1e-11*dryparticlesource_in_dryparticlesource_source.parcel_area
	except:
		pass
	try:
		dryparticlesource_in_dryparticlesource_source.deposition_rate['chem_divalent_mercury']=1e-11*dryparticlesource_in_dryparticlesource_source.parcel_area
	except:
		pass
	try:
		dryparticlesource_in_dryparticlesource_source.deposition_rate['chem_methylmercury']=1e-11*dryparticlesource_in_dryparticlesource_source.parcel_area
	except:
		pass
	try:
		wetparticlesource_in_wetparticlesource_source.deposition_rate['chem_benzo_a_pyrene']=2e-11*wetparticlesource_in_wetparticlesource_source.parcel_area
	except:
		pass
	try:
		wetparticlesource_in_wetparticlesource_source.deposition_rate['chem_arsenic']=2e-11*wetparticlesource_in_wetparticlesource_source.parcel_area
	except:
		pass
	try:
		wetparticlesource_in_wetparticlesource_source.deposition_rate['chem_cadmium']=2e-11*wetparticlesource_in_wetparticlesource_source.parcel_area
	except:
		pass
	try:
		wetparticlesource_in_wetparticlesource_source.deposition_rate['chem_2_3_7_8_tcdd']=2e-11*wetparticlesource_in_wetparticlesource_source.parcel_area
	except:
		pass
	try:
		wetparticlesource_in_wetparticlesource_source.deposition_rate['chem_divalent_mercury']=2e-11*wetparticlesource_in_wetparticlesource_source.parcel_area
	except:
		pass
	try:
		wetparticlesource_in_wetparticlesource_source.deposition_rate['chem_methylmercury']=2e-11*wetparticlesource_in_wetparticlesource_source.parcel_area
	except:
		pass
	try:
		dryvaporsource_in_dryvaporsource_source.deposition_rate['chem_benzo_a_pyrene']=3e-11*dryvaporsource_in_dryvaporsource_source.parcel_area
	except:
		pass
	try:
		dryvaporsource_in_dryvaporsource_source.deposition_rate['chem_arsenic']=3e-11*dryvaporsource_in_dryvaporsource_source.parcel_area
	except:
		pass
	try:
		dryvaporsource_in_dryvaporsource_source.deposition_rate['chem_cadmium']=3e-11*dryvaporsource_in_dryvaporsource_source.parcel_area
	except:
		pass
	try:
		dryvaporsource_in_dryvaporsource_source.deposition_rate['chem_2_3_7_8_tcdd']=3e-11*dryvaporsource_in_dryvaporsource_source.parcel_area
	except:
		pass
	try:
		dryvaporsource_in_dryvaporsource_source.deposition_rate['chem_divalent_mercury']=3e-11*dryvaporsource_in_dryvaporsource_source.parcel_area
	except:
		pass
	try:
		dryvaporsource_in_dryvaporsource_source.deposition_rate['chem_methylmercury']=3e-11*dryvaporsource_in_dryvaporsource_source.parcel_area
	except:
		pass
	try:
		wetvaporsource_in_wetvaporsource_source.deposition_rate['chem_benzo_a_pyrene']=4e-11*wetvaporsource_in_wetvaporsource_source.parcel_area
	except:
		pass
	try:
		wetvaporsource_in_wetvaporsource_source.deposition_rate['chem_arsenic']=4e-11*wetvaporsource_in_wetvaporsource_source.parcel_area
	except:
		pass
	try:
		wetvaporsource_in_wetvaporsource_source.deposition_rate['chem_cadmium']=4e-11*wetvaporsource_in_wetvaporsource_source.parcel_area
	except:
		pass
	try:
		wetvaporsource_in_wetvaporsource_source.deposition_rate['chem_2_3_7_8_tcdd']=4e-11*wetvaporsource_in_wetvaporsource_source.parcel_area
	except:
		pass
	try:
		wetvaporsource_in_wetvaporsource_source.deposition_rate['chem_divalent_mercury']=4e-11*wetvaporsource_in_wetvaporsource_source.parcel_area
	except:
		pass
	try:
		wetvaporsource_in_wetvaporsource_source.deposition_rate['chem_methylmercury']=4e-11*wetvaporsource_in_wetvaporsource_source.parcel_area
	except:
		pass
	try:
		dryparticlesource_in_dryparticlesource_n1.deposition_rate['chem_benzo_a_pyrene']=1e-11*dryparticlesource_in_dryparticlesource_n1.parcel_area
	except:
		pass
	try:
		dryparticlesource_in_dryparticlesource_n1.deposition_rate['chem_arsenic']=1e-11*dryparticlesource_in_dryparticlesource_n1.parcel_area
	except:
		pass
	try:
		dryparticlesource_in_dryparticlesource_n1.deposition_rate['chem_cadmium']=1e-11*dryparticlesource_in_dryparticlesource_n1.parcel_area
	except:
		pass
	try:
		dryparticlesource_in_dryparticlesource_n1.deposition_rate['chem_2_3_7_8_tcdd']=1e-11*dryparticlesource_in_dryparticlesource_n1.parcel_area
	except:
		pass
	try:
		dryparticlesource_in_dryparticlesource_n1.deposition_rate['chem_divalent_mercury']=1e-11*dryparticlesource_in_dryparticlesource_n1.parcel_area
	except:
		pass
	try:
		dryparticlesource_in_dryparticlesource_n1.deposition_rate['chem_methylmercury']=1e-11*dryparticlesource_in_dryparticlesource_n1.parcel_area
	except:
		pass
	try:
		wetparticlesource_in_wetparticlesource_n1.deposition_rate['chem_benzo_a_pyrene']=2e-11*wetparticlesource_in_wetparticlesource_n1.parcel_area
	except:
		pass
	try:
		wetparticlesource_in_wetparticlesource_n1.deposition_rate['chem_arsenic']=2e-11*wetparticlesource_in_wetparticlesource_n1.parcel_area
	except:
		pass
	try:
		wetparticlesource_in_wetparticlesource_n1.deposition_rate['chem_cadmium']=2e-11*wetparticlesource_in_wetparticlesource_n1.parcel_area
	except:
		pass
	try:
		wetparticlesource_in_wetparticlesource_n1.deposition_rate['chem_2_3_7_8_tcdd']=2e-11*wetparticlesource_in_wetparticlesource_n1.parcel_area
	except:
		pass
	try:
		wetparticlesource_in_wetparticlesource_n1.deposition_rate['chem_divalent_mercury']=2e-11*wetparticlesource_in_wetparticlesource_n1.parcel_area
	except:
		pass
	try:
		wetparticlesource_in_wetparticlesource_n1.deposition_rate['chem_methylmercury']=2e-11*wetparticlesource_in_wetparticlesource_n1.parcel_area
	except:
		pass
	try:
		dryvaporsource_in_dryvaporsource_n1.deposition_rate['chem_benzo_a_pyrene']=3e-11*dryvaporsource_in_dryvaporsource_n1.parcel_area
	except:
		pass
	try:
		dryvaporsource_in_dryvaporsource_n1.deposition_rate['chem_arsenic']=3e-11*dryvaporsource_in_dryvaporsource_n1.parcel_area
	except:
		pass
	try:
		dryvaporsource_in_dryvaporsource_n1.deposition_rate['chem_cadmium']=3e-11*dryvaporsource_in_dryvaporsource_n1.parcel_area
	except:
		pass
	try:
		dryvaporsource_in_dryvaporsource_n1.deposition_rate['chem_2_3_7_8_tcdd']=3e-11*dryvaporsource_in_dryvaporsource_n1.parcel_area
	except:
		pass
	try:
		dryvaporsource_in_dryvaporsource_n1.deposition_rate['chem_divalent_mercury']=3e-11*dryvaporsource_in_dryvaporsource_n1.parcel_area
	except:
		pass
	try:
		dryvaporsource_in_dryvaporsource_n1.deposition_rate['chem_methylmercury']=3e-11*dryvaporsource_in_dryvaporsource_n1.parcel_area
	except:
		pass
	try:
		wetvaporsource_in_wetvaporsource_n1.deposition_rate['chem_benzo_a_pyrene']=4e-11*wetvaporsource_in_wetvaporsource_n1.parcel_area
	except:
		pass
	try:
		wetvaporsource_in_wetvaporsource_n1.deposition_rate['chem_arsenic']=4e-11*wetvaporsource_in_wetvaporsource_n1.parcel_area
	except:
		pass
	try:
		wetvaporsource_in_wetvaporsource_n1.deposition_rate['chem_cadmium']=4e-11*wetvaporsource_in_wetvaporsource_n1.parcel_area
	except:
		pass
	try:
		wetvaporsource_in_wetvaporsource_n1.deposition_rate['chem_2_3_7_8_tcdd']=4e-11*wetvaporsource_in_wetvaporsource_n1.parcel_area
	except:
		pass
	try:
		wetvaporsource_in_wetvaporsource_n1.deposition_rate['chem_divalent_mercury']=4e-11*wetvaporsource_in_wetvaporsource_n1.parcel_area
	except:
		pass
	try:
		wetvaporsource_in_wetvaporsource_n1.deposition_rate['chem_methylmercury']=4e-11*wetvaporsource_in_wetvaporsource_n1.parcel_area
	except:
		pass
	try:
		dryparticlesource_in_dryparticlesource_n6.deposition_rate['chem_benzo_a_pyrene']=1e-11*dryparticlesource_in_dryparticlesource_n6.parcel_area
	except:
		pass
	try:
		dryparticlesource_in_dryparticlesource_n6.deposition_rate['chem_arsenic']=1e-11*dryparticlesource_in_dryparticlesource_n6.parcel_area
	except:
		pass
	try:
		dryparticlesource_in_dryparticlesource_n6.deposition_rate['chem_cadmium']=1e-11*dryparticlesource_in_dryparticlesource_n6.parcel_area
	except:
		pass
	try:
		dryparticlesource_in_dryparticlesource_n6.deposition_rate['chem_2_3_7_8_tcdd']=1e-11*dryparticlesource_in_dryparticlesource_n6.parcel_area
	except:
		pass
	try:
		dryparticlesource_in_dryparticlesource_n6.deposition_rate['chem_divalent_mercury']=1e-11*dryparticlesource_in_dryparticlesource_n6.parcel_area
	except:
		pass
	try:
		dryparticlesource_in_dryparticlesource_n6.deposition_rate['chem_methylmercury']=1e-11*dryparticlesource_in_dryparticlesource_n6.parcel_area
	except:
		pass
	try:
		wetparticlesource_in_wetparticlesource_n6.deposition_rate['chem_benzo_a_pyrene']=2e-11*wetparticlesource_in_wetparticlesource_n6.parcel_area
	except:
		pass
	try:
		wetparticlesource_in_wetparticlesource_n6.deposition_rate['chem_arsenic']=2e-11*wetparticlesource_in_wetparticlesource_n6.parcel_area
	except:
		pass
	try:
		wetparticlesource_in_wetparticlesource_n6.deposition_rate['chem_cadmium']=2e-11*wetparticlesource_in_wetparticlesource_n6.parcel_area
	except:
		pass
	try:
		wetparticlesource_in_wetparticlesource_n6.deposition_rate['chem_2_3_7_8_tcdd']=2e-11*wetparticlesource_in_wetparticlesource_n6.parcel_area
	except:
		pass
	try:
		wetparticlesource_in_wetparticlesource_n6.deposition_rate['chem_divalent_mercury']=2e-11*wetparticlesource_in_wetparticlesource_n6.parcel_area
	except:
		pass
	try:
		wetparticlesource_in_wetparticlesource_n6.deposition_rate['chem_methylmercury']=2e-11*wetparticlesource_in_wetparticlesource_n6.parcel_area
	except:
		pass
	try:
		dryvaporsource_in_dryvaporsource_n6.deposition_rate['chem_benzo_a_pyrene']=3e-11*dryvaporsource_in_dryvaporsource_n6.parcel_area
	except:
		pass
	try:
		dryvaporsource_in_dryvaporsource_n6.deposition_rate['chem_arsenic']=3e-11*dryvaporsource_in_dryvaporsource_n6.parcel_area
	except:
		pass
	try:
		dryvaporsource_in_dryvaporsource_n6.deposition_rate['chem_cadmium']=3e-11*dryvaporsource_in_dryvaporsource_n6.parcel_area
	except:
		pass
	try:
		dryvaporsource_in_dryvaporsource_n6.deposition_rate['chem_2_3_7_8_tcdd']=3e-11*dryvaporsource_in_dryvaporsource_n6.parcel_area
	except:
		pass
	try:
		dryvaporsource_in_dryvaporsource_n6.deposition_rate['chem_divalent_mercury']=3e-11*dryvaporsource_in_dryvaporsource_n6.parcel_area
	except:
		pass
	try:
		dryvaporsource_in_dryvaporsource_n6.deposition_rate['chem_methylmercury']=3e-11*dryvaporsource_in_dryvaporsource_n6.parcel_area
	except:
		pass
	try:
		wetvaporsource_in_wetvaporsource_n6.deposition_rate['chem_benzo_a_pyrene']=4e-11*wetvaporsource_in_wetvaporsource_n6.parcel_area
	except:
		pass
	try:
		dryparticlesource_in_dryparticlesource_n7.deposition_rate['chem_benzo_a_pyrene']=1e-11*dryparticlesource_in_dryparticlesource_n7.parcel_area
	except:
		pass
	try:
		dryparticlesource_in_dryparticlesource_n7.deposition_rate['chem_arsenic']=2e-11*dryparticlesource_in_dryparticlesource_n7.parcel_area
	except:
		pass
	try:
		dryparticlesource_in_dryparticlesource_n7.deposition_rate['chem_cadmium']=2e-11*dryparticlesource_in_dryparticlesource_n7.parcel_area
	except:
		pass
	try:
		dryparticlesource_in_dryparticlesource_n7.deposition_rate['chem_2_3_7_8_tcdd']=2e-11*dryparticlesource_in_dryparticlesource_n7.parcel_area
	except:
		pass
	try:
		dryparticlesource_in_dryparticlesource_n7.deposition_rate['chem_divalent_mercury']=2e-11*dryparticlesource_in_dryparticlesource_n7.parcel_area
	except:
		pass
	try:
		dryparticlesource_in_dryparticlesource_n7.deposition_rate['chem_methylmercury']=2e-11*dryparticlesource_in_dryparticlesource_n7.parcel_area
	except:
		pass
	try:
		wetparticlesource_in_wetparticlesource_n7.deposition_rate['chem_benzo_a_pyrene']=2e-11*wetparticlesource_in_wetparticlesource_n7.parcel_area
	except:
		pass
	try:
		wetparticlesource_in_wetparticlesource_n7.deposition_rate['chem_arsenic']=4e-11*wetparticlesource_in_wetparticlesource_n7.parcel_area
	except:
		pass
	try:
		wetparticlesource_in_wetparticlesource_n7.deposition_rate['chem_cadmium']=4e-11*wetparticlesource_in_wetparticlesource_n7.parcel_area
	except:
		pass
	try:
		wetparticlesource_in_wetparticlesource_n7.deposition_rate['chem_2_3_7_8_tcdd']=4e-11*wetparticlesource_in_wetparticlesource_n7.parcel_area
	except:
		pass
	try:
		wetparticlesource_in_wetparticlesource_n7.deposition_rate['chem_divalent_mercury']=4e-11*wetparticlesource_in_wetparticlesource_n7.parcel_area
	except:
		pass
	try:
		wetparticlesource_in_wetparticlesource_n7.deposition_rate['chem_methylmercury']=4e-11*wetparticlesource_in_wetparticlesource_n7.parcel_area
	except:
		pass
	try:
		dryvaporsource_in_dryvaporsource_n7.deposition_rate['chem_benzo_a_pyrene']=3e-11*dryvaporsource_in_dryvaporsource_n7.parcel_area
	except:
		pass
	try:
		dryvaporsource_in_dryvaporsource_n7.deposition_rate['chem_arsenic']=3e-11*dryvaporsource_in_dryvaporsource_n7.parcel_area
	except:
		pass
	try:
		dryvaporsource_in_dryvaporsource_n7.deposition_rate['chem_cadmium']=3e-11*dryvaporsource_in_dryvaporsource_n7.parcel_area
	except:
		pass
	try:
		dryvaporsource_in_dryvaporsource_n7.deposition_rate['chem_2_3_7_8_tcdd']=3e-11*dryvaporsource_in_dryvaporsource_n7.parcel_area
	except:
		pass
	try:
		dryvaporsource_in_dryvaporsource_n7.deposition_rate['chem_divalent_mercury']=3e-11*dryvaporsource_in_dryvaporsource_n7.parcel_area
	except:
		pass
	try:
		dryvaporsource_in_dryvaporsource_n7.deposition_rate['chem_methylmercury']=3e-11*dryvaporsource_in_dryvaporsource_n7.parcel_area
	except:
		pass
	try:
		wetvaporsource_in_wetvaporsource_n7.deposition_rate['chem_benzo_a_pyrene']=4e-11*wetvaporsource_in_wetvaporsource_n7.parcel_area
	except:
		pass
	try:
		wetvaporsource_in_wetvaporsource_n7.deposition_rate['chem_arsenic']=4e-11*wetvaporsource_in_wetvaporsource_n7.parcel_area
	except:
		pass
	try:
		wetvaporsource_in_wetvaporsource_n7.deposition_rate['chem_cadmium']=4e-11*wetvaporsource_in_wetvaporsource_n7.parcel_area
	except:
		pass
	try:
		wetvaporsource_in_wetvaporsource_n7.deposition_rate['chem_2_3_7_8_tcdd']=4e-11*wetvaporsource_in_wetvaporsource_n7.parcel_area
	except:
		pass
	try:
		wetvaporsource_in_wetvaporsource_n7.deposition_rate['chem_divalent_mercury']=4e-11*wetvaporsource_in_wetvaporsource_n7.parcel_area
	except:
		pass
	try:
		wetvaporsource_in_wetvaporsource_n7.deposition_rate['chem_methylmercury']=4e-11*wetvaporsource_in_wetvaporsource_n7.parcel_area
	except:
		pass
	try:
		dryparticlesource_in_dryparticlesource_n3.deposition_rate['chem_benzo_a_pyrene']=1e-11*dryparticlesource_in_dryparticlesource_n3.parcel_area
	except:
		pass
	try:
		dryparticlesource_in_dryparticlesource_n3.deposition_rate['chem_arsenic']=2e-11*dryparticlesource_in_dryparticlesource_n3.parcel_area
	except:
		pass
	try:
		dryparticlesource_in_dryparticlesource_n3.deposition_rate['chem_cadmium']=2e-11*dryparticlesource_in_dryparticlesource_n3.parcel_area
	except:
		pass
	try:
		dryparticlesource_in_dryparticlesource_n3.deposition_rate['chem_2_3_7_8_tcdd']=2e-11*dryparticlesource_in_dryparticlesource_n3.parcel_area
	except:
		pass
	try:
		dryparticlesource_in_dryparticlesource_n3.deposition_rate['chem_divalent_mercury']=2e-11*dryparticlesource_in_dryparticlesource_n3.parcel_area
	except:
		pass
	try:
		dryparticlesource_in_dryparticlesource_n3.deposition_rate['chem_methylmercury']=2e-11*dryparticlesource_in_dryparticlesource_n3.parcel_area
	except:
		pass
	try:
		wetparticlesource_in_wetparticlesource_n3.deposition_rate['chem_benzo_a_pyrene']=2e-11*wetparticlesource_in_wetparticlesource_n3.parcel_area
	except:
		pass
	try:
		wetparticlesource_in_wetparticlesource_n3.deposition_rate['chem_arsenic']=2e-11*wetparticlesource_in_wetparticlesource_n3.parcel_area
	except:
		pass
	try:
		wetparticlesource_in_wetparticlesource_n3.deposition_rate['chem_cadmium']=2e-11*wetparticlesource_in_wetparticlesource_n3.parcel_area
	except:
		pass
	try:
		wetparticlesource_in_wetparticlesource_n3.deposition_rate['chem_2_3_7_8_tcdd']=2e-11*wetparticlesource_in_wetparticlesource_n3.parcel_area
	except:
		pass
	try:
		wetparticlesource_in_wetparticlesource_n3.deposition_rate['chem_divalent_mercury']=2e-11*wetparticlesource_in_wetparticlesource_n3.parcel_area
	except:
		pass
	try:
		wetparticlesource_in_wetparticlesource_n3.deposition_rate['chem_methylmercury']=2e-11*wetparticlesource_in_wetparticlesource_n3.parcel_area
	except:
		pass
	try:
		dryvaporsource_in_dryvaporsource_n3.deposition_rate['chem_benzo_a_pyrene']=3e-11*dryvaporsource_in_dryvaporsource_n3.parcel_area
	except:
		pass
	try:
		dryvaporsource_in_dryvaporsource_n3.deposition_rate['chem_arsenic']=3e-11*dryvaporsource_in_dryvaporsource_n3.parcel_area
	except:
		pass
	try:
		dryvaporsource_in_dryvaporsource_n3.deposition_rate['chem_cadmium']=3e-11*dryvaporsource_in_dryvaporsource_n3.parcel_area
	except:
		pass
	try:
		dryvaporsource_in_dryvaporsource_n3.deposition_rate['chem_2_3_7_8_tcdd']=3e-11*dryvaporsource_in_dryvaporsource_n3.parcel_area
	except:
		pass
	try:
		dryvaporsource_in_dryvaporsource_n3.deposition_rate['chem_divalent_mercury']=3e-11*dryvaporsource_in_dryvaporsource_n3.parcel_area
	except:
		pass
	try:
		dryvaporsource_in_dryvaporsource_n3.deposition_rate['chem_methylmercury']=3e-11*dryvaporsource_in_dryvaporsource_n3.parcel_area
	except:
		pass
	try:
		wetvaporsource_in_wetvaporsource_n3.deposition_rate['chem_benzo_a_pyrene']=4e-11*wetvaporsource_in_wetvaporsource_n3.parcel_area
	except:
		pass
	try:
		dryparticlesource_in_dryparticlesource_n4.deposition_rate['chem_benzo_a_pyrene']=1e-11*dryparticlesource_in_dryparticlesource_n4.parcel_area
	except:
		pass
	try:
		dryparticlesource_in_dryparticlesource_n4.deposition_rate['chem_arsenic']=1e-11*dryparticlesource_in_dryparticlesource_n4.parcel_area
	except:
		pass
	try:
		dryparticlesource_in_dryparticlesource_n4.deposition_rate['chem_cadmium']=1e-11*dryparticlesource_in_dryparticlesource_n4.parcel_area
	except:
		pass
	try:
		dryparticlesource_in_dryparticlesource_n4.deposition_rate['chem_2_3_7_8_tcdd']=1e-11*dryparticlesource_in_dryparticlesource_n4.parcel_area
	except:
		pass
	try:
		dryparticlesource_in_dryparticlesource_n4.deposition_rate['chem_divalent_mercury']=1e-11*dryparticlesource_in_dryparticlesource_n4.parcel_area
	except:
		pass
	try:
		dryparticlesource_in_dryparticlesource_n4.deposition_rate['chem_methylmercury']=1e-11*dryparticlesource_in_dryparticlesource_n4.parcel_area
	except:
		pass
	try:
		wetparticlesource_in_wetparticlesource_n4.deposition_rate['chem_benzo_a_pyrene']=2e-11*wetparticlesource_in_wetparticlesource_n4.parcel_area
	except:
		pass
	try:
		wetparticlesource_in_wetparticlesource_n4.deposition_rate['chem_arsenic']=2e-11*wetparticlesource_in_wetparticlesource_n4.parcel_area
	except:
		pass
	try:
		wetparticlesource_in_wetparticlesource_n4.deposition_rate['chem_cadmium']=2e-11*wetparticlesource_in_wetparticlesource_n4.parcel_area
	except:
		pass
	try:
		wetparticlesource_in_wetparticlesource_n4.deposition_rate['chem_2_3_7_8_tcdd']=2e-11*wetparticlesource_in_wetparticlesource_n4.parcel_area
	except:
		pass
	try:
		wetparticlesource_in_wetparticlesource_n4.deposition_rate['chem_divalent_mercury']=2e-11*wetparticlesource_in_wetparticlesource_n4.parcel_area
	except:
		pass
	try:
		wetparticlesource_in_wetparticlesource_n4.deposition_rate['chem_methylmercury']=2e-11*wetparticlesource_in_wetparticlesource_n4.parcel_area
	except:
		pass
	try:
		dryvaporsource_in_dryvaporsource_n4.deposition_rate['chem_benzo_a_pyrene']=3e-11*dryvaporsource_in_dryvaporsource_n4.parcel_area
	except:
		pass
	try:
		dryvaporsource_in_dryvaporsource_n4.deposition_rate['chem_arsenic']=3e-11*dryvaporsource_in_dryvaporsource_n4.parcel_area
	except:
		pass
	try:
		dryvaporsource_in_dryvaporsource_n4.deposition_rate['chem_cadmium']=3e-11*dryvaporsource_in_dryvaporsource_n4.parcel_area
	except:
		pass
	try:
		dryvaporsource_in_dryvaporsource_n4.deposition_rate['chem_2_3_7_8_tcdd']=3e-11*dryvaporsource_in_dryvaporsource_n4.parcel_area
	except:
		pass
	try:
		dryvaporsource_in_dryvaporsource_n4.deposition_rate['chem_divalent_mercury']=3e-11*dryvaporsource_in_dryvaporsource_n4.parcel_area
	except:
		pass
	try:
		dryvaporsource_in_dryvaporsource_n4.deposition_rate['chem_methylmercury']=3e-11*dryvaporsource_in_dryvaporsource_n4.parcel_area
	except:
		pass
	try:
		wetvaporsource_in_wetvaporsource_n4.deposition_rate['chem_benzo_a_pyrene']=4e-11*wetvaporsource_in_wetvaporsource_n4.parcel_area
	except:
		pass
	try:
		wetvaporsource_in_wetvaporsource_n4.deposition_rate['chem_arsenic']=4e-11*wetvaporsource_in_wetvaporsource_n4.parcel_area
	except:
		pass
	try:
		wetvaporsource_in_wetvaporsource_n4.deposition_rate['chem_cadmium']=4e-11*wetvaporsource_in_wetvaporsource_n4.parcel_area
	except:
		pass
	try:
		wetvaporsource_in_wetvaporsource_n4.deposition_rate['chem_2_3_7_8_tcdd']=4e-11*wetvaporsource_in_wetvaporsource_n4.parcel_area
	except:
		pass
	try:
		wetvaporsource_in_wetvaporsource_n4.deposition_rate['chem_divalent_mercury']=4e-11*wetvaporsource_in_wetvaporsource_n4.parcel_area
	except:
		pass
	try:
		wetvaporsource_in_wetvaporsource_n4.deposition_rate['chem_methylmercury']=4e-11*wetvaporsource_in_wetvaporsource_n4.parcel_area
	except:
		pass
	try:
		dryparticlesource_in_dryparticlesource_n5.deposition_rate['chem_benzo_a_pyrene']=1e-11*dryparticlesource_in_dryparticlesource_n5.parcel_area
	except:
		pass
	try:
		dryparticlesource_in_dryparticlesource_n5.deposition_rate['chem_arsenic']=1e-11*dryparticlesource_in_dryparticlesource_n5.parcel_area
	except:
		pass
	try:
		dryparticlesource_in_dryparticlesource_n5.deposition_rate['chem_cadmium']=1e-11*dryparticlesource_in_dryparticlesource_n5.parcel_area
	except:
		pass
	try:
		dryparticlesource_in_dryparticlesource_n5.deposition_rate['chem_2_3_7_8_tcdd']=1e-11*dryparticlesource_in_dryparticlesource_n5.parcel_area
	except:
		pass
	try:
		dryparticlesource_in_dryparticlesource_n5.deposition_rate['chem_divalent_mercury']=1e-11*dryparticlesource_in_dryparticlesource_n5.parcel_area
	except:
		pass
	try:
		dryparticlesource_in_dryparticlesource_n5.deposition_rate['chem_methylmercury']=1e-11*dryparticlesource_in_dryparticlesource_n5.parcel_area
	except:
		pass
	try:
		wetparticlesource_in_wetparticlesource_n5.deposition_rate['chem_benzo_a_pyrene']=2e-11*wetparticlesource_in_wetparticlesource_n5.parcel_area
	except:
		pass
	try:
		wetparticlesource_in_wetparticlesource_n5.deposition_rate['chem_arsenic']=2e-11*wetparticlesource_in_wetparticlesource_n5.parcel_area
	except:
		pass
	try:
		wetparticlesource_in_wetparticlesource_n5.deposition_rate['chem_cadmium']=2e-11*wetparticlesource_in_wetparticlesource_n5.parcel_area
	except:
		pass
	try:
		wetparticlesource_in_wetparticlesource_n5.deposition_rate['chem_2_3_7_8_tcdd']=2e-11*wetparticlesource_in_wetparticlesource_n5.parcel_area
	except:
		pass
	try:
		wetparticlesource_in_wetparticlesource_n5.deposition_rate['chem_divalent_mercury']=2e-11*wetparticlesource_in_wetparticlesource_n5.parcel_area
	except:
		pass
	try:
		wetparticlesource_in_wetparticlesource_n5.deposition_rate['chem_methylmercury']=2e-11*wetparticlesource_in_wetparticlesource_n5.parcel_area
	except:
		pass
	try:
		dryvaporsource_in_dryvaporsource_n5.deposition_rate['chem_benzo_a_pyrene']=3e-11*dryvaporsource_in_dryvaporsource_n5.parcel_area
	except:
		pass
	try:
		dryvaporsource_in_dryvaporsource_n5.deposition_rate['chem_arsenic']=3e-11*dryvaporsource_in_dryvaporsource_n5.parcel_area
	except:
		pass
	try:
		dryvaporsource_in_dryvaporsource_n5.deposition_rate['chem_cadmium']=3e-11*dryvaporsource_in_dryvaporsource_n5.parcel_area
	except:
		pass
	try:
		dryvaporsource_in_dryvaporsource_n5.deposition_rate['chem_2_3_7_8_tcdd']=3e-11*dryvaporsource_in_dryvaporsource_n5.parcel_area
	except:
		pass
	try:
		dryvaporsource_in_dryvaporsource_n5.deposition_rate['chem_divalent_mercury']=3e-11*dryvaporsource_in_dryvaporsource_n5.parcel_area
	except:
		pass
	try:
		dryvaporsource_in_dryvaporsource_n5.deposition_rate['chem_methylmercury']=3e-11*dryvaporsource_in_dryvaporsource_n5.parcel_area
	except:
		pass
	try:
		wetvaporsource_in_wetvaporsource_n5.deposition_rate['chem_benzo_a_pyrene']=4e-11*wetvaporsource_in_wetvaporsource_n5.parcel_area
	except:
		pass
	try:
		wetvaporsource_in_wetvaporsource_n5.deposition_rate['chem_arsenic']=4e-11*wetvaporsource_in_wetvaporsource_n5.parcel_area
	except:
		pass
	try:
		wetvaporsource_in_wetvaporsource_n5.deposition_rate['chem_cadmium']=4e-11*wetvaporsource_in_wetvaporsource_n5.parcel_area
	except:
		pass
	try:
		wetvaporsource_in_wetvaporsource_n5.deposition_rate['chem_2_3_7_8_tcdd']=4e-11*wetvaporsource_in_wetvaporsource_n5.parcel_area
	except:
		pass
	try:
		wetvaporsource_in_wetvaporsource_n5.deposition_rate['chem_divalent_mercury']=4e-11*wetvaporsource_in_wetvaporsource_n5.parcel_area
	except:
		pass
	try:
		wetvaporsource_in_wetvaporsource_n5.deposition_rate['chem_methylmercury']=4e-11*wetvaporsource_in_wetvaporsource_n5.parcel_area
	except:
		pass
	try:
		dryparticlesource_in_dryparticlesource_s1.deposition_rate['chem_benzo_a_pyrene']=1e-11*dryparticlesource_in_dryparticlesource_s1.parcel_area
	except:
		pass
	try:
		dryparticlesource_in_dryparticlesource_s1.deposition_rate['chem_arsenic']=1e-11*dryparticlesource_in_dryparticlesource_s1.parcel_area
	except:
		pass
	try:
		dryparticlesource_in_dryparticlesource_s1.deposition_rate['chem_cadmium']=1e-11*dryparticlesource_in_dryparticlesource_s1.parcel_area
	except:
		pass
	try:
		dryparticlesource_in_dryparticlesource_s1.deposition_rate['chem_2_3_7_8_tcdd']=1e-11*dryparticlesource_in_dryparticlesource_s1.parcel_area
	except:
		pass
	try:
		dryparticlesource_in_dryparticlesource_s1.deposition_rate['chem_divalent_mercury']=1e-11*dryparticlesource_in_dryparticlesource_s1.parcel_area
	except:
		pass
	try:
		dryparticlesource_in_dryparticlesource_s1.deposition_rate['chem_methylmercury']=1e-11*dryparticlesource_in_dryparticlesource_s1.parcel_area
	except:
		pass
	try:
		wetparticlesource_in_wetparticlesource_s1.deposition_rate['chem_benzo_a_pyrene']=2e-11*wetparticlesource_in_wetparticlesource_s1.parcel_area
	except:
		pass
	try:
		wetparticlesource_in_wetparticlesource_s1.deposition_rate['chem_arsenic']=2e-11*wetparticlesource_in_wetparticlesource_s1.parcel_area
	except:
		pass
	try:
		wetparticlesource_in_wetparticlesource_s1.deposition_rate['chem_cadmium']=2e-11*wetparticlesource_in_wetparticlesource_s1.parcel_area
	except:
		pass
	try:
		wetparticlesource_in_wetparticlesource_s1.deposition_rate['chem_2_3_7_8_tcdd']=2e-11*wetparticlesource_in_wetparticlesource_s1.parcel_area
	except:
		pass
	try:
		wetparticlesource_in_wetparticlesource_s1.deposition_rate['chem_divalent_mercury']=2e-11*wetparticlesource_in_wetparticlesource_s1.parcel_area
	except:
		pass
	try:
		wetparticlesource_in_wetparticlesource_s1.deposition_rate['chem_methylmercury']=2e-11*wetparticlesource_in_wetparticlesource_s1.parcel_area
	except:
		pass
	try:
		dryvaporsource_in_dryvaporsource_s1.deposition_rate['chem_benzo_a_pyrene']=3e-11*dryvaporsource_in_dryvaporsource_s1.parcel_area
	except:
		pass
	try:
		dryvaporsource_in_dryvaporsource_s1.deposition_rate['chem_arsenic']=3e-11*dryvaporsource_in_dryvaporsource_s1.parcel_area
	except:
		pass
	try:
		dryvaporsource_in_dryvaporsource_s1.deposition_rate['chem_cadmium']=3e-11*dryvaporsource_in_dryvaporsource_s1.parcel_area
	except:
		pass
	try:
		dryvaporsource_in_dryvaporsource_s1.deposition_rate['chem_2_3_7_8_tcdd']=3e-11*dryvaporsource_in_dryvaporsource_s1.parcel_area
	except:
		pass
	try:
		dryvaporsource_in_dryvaporsource_s1.deposition_rate['chem_divalent_mercury']=3e-11*dryvaporsource_in_dryvaporsource_s1.parcel_area
	except:
		pass
	try:
		dryvaporsource_in_dryvaporsource_s1.deposition_rate['chem_methylmercury']=3e-11*dryvaporsource_in_dryvaporsource_s1.parcel_area
	except:
		pass
	try:
		wetvaporsource_in_wetvaporsource_s1.deposition_rate['chem_benzo_a_pyrene']=4e-11*wetvaporsource_in_wetvaporsource_s1.parcel_area
	except:
		pass
	try:
		wetvaporsource_in_wetvaporsource_s1.deposition_rate['chem_arsenic']=4e-11*wetvaporsource_in_wetvaporsource_s1.parcel_area
	except:
		pass
	try:
		wetvaporsource_in_wetvaporsource_s1.deposition_rate['chem_cadmium']=4e-11*wetvaporsource_in_wetvaporsource_s1.parcel_area
	except:
		pass
	try:
		wetvaporsource_in_wetvaporsource_s1.deposition_rate['chem_2_3_7_8_tcdd']=4e-11*wetvaporsource_in_wetvaporsource_s1.parcel_area
	except:
		pass
	try:
		wetvaporsource_in_wetvaporsource_s1.deposition_rate['chem_divalent_mercury']=4e-11*wetvaporsource_in_wetvaporsource_s1.parcel_area
	except:
		pass
	try:
		wetvaporsource_in_wetvaporsource_s1.deposition_rate['chem_methylmercury']=4e-11*wetvaporsource_in_wetvaporsource_s1.parcel_area
	except:
		pass
	try:
		dryparticlesource_in_dryparticlesource_pond.deposition_rate['chem_benzo_a_pyrene']=1e-11*dryparticlesource_in_dryparticlesource_pond.parcel_area
	except:
		pass
	try:
		dryparticlesource_in_dryparticlesource_pond.deposition_rate['chem_arsenic']=1e-11*dryparticlesource_in_dryparticlesource_pond.parcel_area
	except:
		pass
	try:
		dryparticlesource_in_dryparticlesource_pond.deposition_rate['chem_cadmium']=1e-11*dryparticlesource_in_dryparticlesource_pond.parcel_area
	except:
		pass
	try:
		dryparticlesource_in_dryparticlesource_pond.deposition_rate['chem_2_3_7_8_tcdd']=1e-11*dryparticlesource_in_dryparticlesource_pond.parcel_area
	except:
		pass
	try:
		dryparticlesource_in_dryparticlesource_pond.deposition_rate['chem_divalent_mercury']=1e-11*dryparticlesource_in_dryparticlesource_pond.parcel_area
	except:
		pass
	try:
		dryparticlesource_in_dryparticlesource_pond.deposition_rate['chem_methylmercury']=1e-11*dryparticlesource_in_dryparticlesource_pond.parcel_area
	except:
		pass
	try:
		wetparticlesource_in_wetparticlesource_pond.deposition_rate['chem_benzo_a_pyrene']=2e-11*wetparticlesource_in_wetparticlesource_pond.parcel_area
	except:
		pass
	try:
		wetparticlesource_in_wetparticlesource_pond.deposition_rate['chem_arsenic']=2e-11*wetparticlesource_in_wetparticlesource_pond.parcel_area
	except:
		pass
	try:
		wetparticlesource_in_wetparticlesource_pond.deposition_rate['chem_cadmium']=2e-11*wetparticlesource_in_wetparticlesource_pond.parcel_area
	except:
		pass
	try:
		wetparticlesource_in_wetparticlesource_pond.deposition_rate['chem_2_3_7_8_tcdd']=2e-11*wetparticlesource_in_wetparticlesource_pond.parcel_area
	except:
		pass
	try:
		wetparticlesource_in_wetparticlesource_pond.deposition_rate['chem_divalent_mercury']=2e-11*wetparticlesource_in_wetparticlesource_pond.parcel_area
	except:
		pass
	try:
		wetparticlesource_in_wetparticlesource_pond.deposition_rate['chem_methylmercury']=2e-11*wetparticlesource_in_wetparticlesource_pond.parcel_area
	except:
		pass
	try:
		dryvaporsource_in_dryvaporsource_pond.deposition_rate['chem_benzo_a_pyrene']=3e-11*dryvaporsource_in_dryvaporsource_pond.parcel_area
	except:
		pass
	try:
		dryvaporsource_in_dryvaporsource_pond.deposition_rate['chem_arsenic']=3e-11*dryvaporsource_in_dryvaporsource_pond.parcel_area
	except:
		pass
	try:
		dryvaporsource_in_dryvaporsource_pond.deposition_rate['chem_cadmium']=3e-11*dryvaporsource_in_dryvaporsource_pond.parcel_area
	except:
		pass
	try:
		dryvaporsource_in_dryvaporsource_pond.deposition_rate['chem_2_3_7_8_tcdd']=3e-11*dryvaporsource_in_dryvaporsource_pond.parcel_area
	except:
		pass
	try:
		dryvaporsource_in_dryvaporsource_pond.deposition_rate['chem_divalent_mercury']=3e-11*dryvaporsource_in_dryvaporsource_pond.parcel_area
	except:
		pass
	try:
		dryvaporsource_in_dryvaporsource_pond.deposition_rate['chem_methylmercury']=3e-11*dryvaporsource_in_dryvaporsource_pond.parcel_area
	except:
		pass
	try:
		wetvaporsource_in_wetvaporsource_pond.deposition_rate['chem_benzo_a_pyrene']=4e-11*wetvaporsource_in_wetvaporsource_pond.parcel_area
	except:
		pass
	try:
		wetvaporsource_in_wetvaporsource_pond.deposition_rate['chem_arsenic']=4e-11*wetvaporsource_in_wetvaporsource_pond.parcel_area
	except:
		pass
	try:
		wetvaporsource_in_wetvaporsource_pond.deposition_rate['chem_cadmium']=4e-11*wetvaporsource_in_wetvaporsource_pond.parcel_area
	except:
		pass
	try:
		wetvaporsource_in_wetvaporsource_pond.deposition_rate['chem_2_3_7_8_tcdd']=4e-11*wetvaporsource_in_wetvaporsource_pond.parcel_area
	except:
		pass
	try:
		wetvaporsource_in_wetvaporsource_pond.deposition_rate['chem_divalent_mercury']=4e-11*wetvaporsource_in_wetvaporsource_pond.parcel_area
	except:
		pass
	try:
		wetvaporsource_in_wetvaporsource_pond.deposition_rate['chem_methylmercury']=4e-11*wetvaporsource_in_wetvaporsource_pond.parcel_area
	except:
		pass
	try:
		dryparticlesource_in_dryparticlesource_s4.deposition_rate['chem_benzo_a_pyrene']=1e-11*dryparticlesource_in_dryparticlesource_s4.parcel_area
	except:
		pass
	try:
		dryparticlesource_in_dryparticlesource_s4.deposition_rate['chem_arsenic']=1e-11*dryparticlesource_in_dryparticlesource_s4.parcel_area
	except:
		pass
	try:
		dryparticlesource_in_dryparticlesource_s4.deposition_rate['chem_cadmium']=1e-11*dryparticlesource_in_dryparticlesource_s4.parcel_area
	except:
		pass
	try:
		dryparticlesource_in_dryparticlesource_s4.deposition_rate['chem_2_3_7_8_tcdd']=1e-11*dryparticlesource_in_dryparticlesource_s4.parcel_area
	except:
		pass
	try:
		dryparticlesource_in_dryparticlesource_s4.deposition_rate['chem_divalent_mercury']=1e-11*dryparticlesource_in_dryparticlesource_s4.parcel_area
	except:
		pass
	try:
		dryparticlesource_in_dryparticlesource_s4.deposition_rate['chem_methylmercury']=1e-11*dryparticlesource_in_dryparticlesource_s4.parcel_area
	except:
		pass
	try:
		wetparticlesource_in_wetparticlesource_s4.deposition_rate['chem_benzo_a_pyrene']=2e-11*wetparticlesource_in_wetparticlesource_s4.parcel_area
	except:
		pass
	try:
		wetparticlesource_in_wetparticlesource_s4.deposition_rate['chem_arsenic']=2e-11*wetparticlesource_in_wetparticlesource_s4.parcel_area
	except:
		pass
	try:
		wetparticlesource_in_wetparticlesource_s4.deposition_rate['chem_cadmium']=2e-11*wetparticlesource_in_wetparticlesource_s4.parcel_area
	except:
		pass
	try:
		wetparticlesource_in_wetparticlesource_s4.deposition_rate['chem_2_3_7_8_tcdd']=2e-11*wetparticlesource_in_wetparticlesource_s4.parcel_area
	except:
		pass
	try:
		wetparticlesource_in_wetparticlesource_s4.deposition_rate['chem_divalent_mercury']=2e-11*wetparticlesource_in_wetparticlesource_s4.parcel_area
	except:
		pass
	try:
		wetparticlesource_in_wetparticlesource_s4.deposition_rate['chem_methylmercury']=2e-11*wetparticlesource_in_wetparticlesource_s4.parcel_area
	except:
		pass
	try:
		dryvaporsource_in_dryvaporsource_s4.deposition_rate['chem_benzo_a_pyrene']=3e-11*dryvaporsource_in_dryvaporsource_s4.parcel_area
	except:
		pass
	try:
		dryvaporsource_in_dryvaporsource_s4.deposition_rate['chem_arsenic']=3e-11*dryvaporsource_in_dryvaporsource_s4.parcel_area
	except:
		pass
	try:
		dryvaporsource_in_dryvaporsource_s4.deposition_rate['chem_cadmium']=3e-11*dryvaporsource_in_dryvaporsource_s4.parcel_area
	except:
		pass
	try:
		dryvaporsource_in_dryvaporsource_s4.deposition_rate['chem_2_3_7_8_tcdd']=3e-11*dryvaporsource_in_dryvaporsource_s4.parcel_area
	except:
		pass
	try:
		dryvaporsource_in_dryvaporsource_s4.deposition_rate['chem_divalent_mercury']=3e-11*dryvaporsource_in_dryvaporsource_s4.parcel_area
	except:
		pass
	try:
		dryvaporsource_in_dryvaporsource_s4.deposition_rate['chem_methylmercury']=3e-11*dryvaporsource_in_dryvaporsource_s4.parcel_area
	except:
		pass
	try:
		wetvaporsource_in_wetvaporsource_s4.deposition_rate['chem_benzo_a_pyrene']=4e-11*wetvaporsource_in_wetvaporsource_s4.parcel_area
	except:
		pass
	try:
		wetvaporsource_in_wetvaporsource_s4.deposition_rate['chem_arsenic']=4e-11*wetvaporsource_in_wetvaporsource_s4.parcel_area
	except:
		pass
	try:
		wetvaporsource_in_wetvaporsource_s4.deposition_rate['chem_cadmium']=4e-11*wetvaporsource_in_wetvaporsource_s4.parcel_area
	except:
		pass
	try:
		wetvaporsource_in_wetvaporsource_s4.deposition_rate['chem_2_3_7_8_tcdd']=4e-11*wetvaporsource_in_wetvaporsource_s4.parcel_area
	except:
		pass
	try:
		wetvaporsource_in_wetvaporsource_s4.deposition_rate['chem_divalent_mercury']=4e-11*wetvaporsource_in_wetvaporsource_s4.parcel_area
	except:
		pass
	try:
		wetvaporsource_in_wetvaporsource_s4.deposition_rate['chem_methylmercury']=4e-11*wetvaporsource_in_wetvaporsource_s4.parcel_area
	except:
		pass
	try:
		dryparticlesource_in_dryparticlesource_s5.deposition_rate['chem_benzo_a_pyrene']=1e-11*dryparticlesource_in_dryparticlesource_s5.parcel_area
	except:
		pass
	try:
		dryparticlesource_in_dryparticlesource_s5.deposition_rate['chem_arsenic']=1e-11*dryparticlesource_in_dryparticlesource_s5.parcel_area
	except:
		pass
	try:
		dryparticlesource_in_dryparticlesource_s5.deposition_rate['chem_cadmium']=1e-11*dryparticlesource_in_dryparticlesource_s5.parcel_area
	except:
		pass
	try:
		dryparticlesource_in_dryparticlesource_s5.deposition_rate['chem_2_3_7_8_tcdd']=1e-11*dryparticlesource_in_dryparticlesource_s5.parcel_area
	except:
		pass
	try:
		dryparticlesource_in_dryparticlesource_s5.deposition_rate['chem_divalent_mercury']=1e-11*dryparticlesource_in_dryparticlesource_s5.parcel_area
	except:
		pass
	try:
		dryparticlesource_in_dryparticlesource_s5.deposition_rate['chem_methylmercury']=1e-11*dryparticlesource_in_dryparticlesource_s5.parcel_area
	except:
		pass
	try:
		wetparticlesource_in_wetparticlesource_s5.deposition_rate['chem_benzo_a_pyrene']=2e-11*wetparticlesource_in_wetparticlesource_s5.parcel_area
	except:
		pass
	try:
		wetparticlesource_in_wetparticlesource_s5.deposition_rate['chem_arsenic']=2e-11*wetparticlesource_in_wetparticlesource_s5.parcel_area
	except:
		pass
	try:
		wetparticlesource_in_wetparticlesource_s5.deposition_rate['chem_cadmium']=2e-11*wetparticlesource_in_wetparticlesource_s5.parcel_area
	except:
		pass
	try:
		wetparticlesource_in_wetparticlesource_s5.deposition_rate['chem_2_3_7_8_tcdd']=2e-11*wetparticlesource_in_wetparticlesource_s5.parcel_area
	except:
		pass
	try:
		wetparticlesource_in_wetparticlesource_s5.deposition_rate['chem_divalent_mercury']=2e-11*wetparticlesource_in_wetparticlesource_s5.parcel_area
	except:
		pass
	try:
		wetparticlesource_in_wetparticlesource_s5.deposition_rate['chem_methylmercury']=2e-11*wetparticlesource_in_wetparticlesource_s5.parcel_area
	except:
		pass
	try:
		dryvaporsource_in_dryvaporsource_s5.deposition_rate['chem_benzo_a_pyrene']=3e-11*dryvaporsource_in_dryvaporsource_s5.parcel_area
	except:
		pass
	try:
		dryvaporsource_in_dryvaporsource_s5.deposition_rate['chem_arsenic']=3e-11*dryvaporsource_in_dryvaporsource_s5.parcel_area
	except:
		pass
	try:
		dryvaporsource_in_dryvaporsource_s5.deposition_rate['chem_cadmium']=3e-11*dryvaporsource_in_dryvaporsource_s5.parcel_area
	except:
		pass
	try:
		dryvaporsource_in_dryvaporsource_s5.deposition_rate['chem_2_3_7_8_tcdd']=3e-11*dryvaporsource_in_dryvaporsource_s5.parcel_area
	except:
		pass
	try:
		dryvaporsource_in_dryvaporsource_s5.deposition_rate['chem_divalent_mercury']=3e-11*dryvaporsource_in_dryvaporsource_s5.parcel_area
	except:
		pass
	try:
		dryvaporsource_in_dryvaporsource_s5.deposition_rate['chem_methylmercury']=3e-11*dryvaporsource_in_dryvaporsource_s5.parcel_area
	except:
		pass
	try:
		wetvaporsource_in_wetvaporsource_s5.deposition_rate['chem_benzo_a_pyrene']=4e-11*wetvaporsource_in_wetvaporsource_s5.parcel_area
	except:
		pass
	try:
		wetvaporsource_in_wetvaporsource_s5.deposition_rate['chem_arsenic']=4e-11*wetvaporsource_in_wetvaporsource_s5.parcel_area
	except:
		pass
	try:
		wetvaporsource_in_wetvaporsource_s5.deposition_rate['chem_cadmium']=4e-11*wetvaporsource_in_wetvaporsource_s5.parcel_area
	except:
		pass
	try:
		wetvaporsource_in_wetvaporsource_s5.deposition_rate['chem_2_3_7_8_tcdd']=4e-11*wetvaporsource_in_wetvaporsource_s5.parcel_area
	except:
		pass
	try:
		wetvaporsource_in_wetvaporsource_s5.deposition_rate['chem_divalent_mercury']=4e-11*wetvaporsource_in_wetvaporsource_s5.parcel_area
	except:
		pass
	try:
		wetvaporsource_in_wetvaporsource_s5.deposition_rate['chem_methylmercury']=4e-11*wetvaporsource_in_wetvaporsource_s5.parcel_area
	except:
		pass

	return(comp_objects_dict)