# -*- coding: utf-8 -*-

#This script contains unit tests to automate various tests of the Parcel.py, ParcelCollection.py modules

import pandas as pd
import unittest
from .Parcel import Parcel
from .ParcelCollection import ParcelCollection



#data = pd.read_csv(r"C:\Users\39492\Documents\trim-builder\Test_ParcelCollection.csv")
#data.apply(lambda x: result.Add(x["Name"],x["Category"],x["Source"]),axis=1) #read in data into parcel collection

class TestParcelCollection(unittest.TestCase): #inherits from unittest.TestCase
    
    def setUp(self):
        #the set up before every test
        self.result = ParcelCollection()       
        
        self.result.Add("L1","Land", "grass", False)
        self.result.Add("L2","Land & Air", "deciduous forest", True)
        self.result.Add("LakeCadillac","Water", "", False)
        self.result.Add("LakeMitchell","Water & Air", "", False)        
        self.result.Add("A1","Air Only", "", False)
    
    def tearDown(self):
        #execute at the end of every test
        self.result.RemoveAll()
    
    def test_Instance(self): #HAS to be "test_*"  otherwise python won't test the method              
        #checks instance
        self.assertIsInstance(self.result, ParcelCollection)
        
    def test_AddandAll(self):
        #checks if parcels were added correctly. checks if All() works correctly in the process
        self.assertEqual(set([x.Name for x in self.result.All()]),set(["L1","L2","LakeCadillac","LakeMitchell","A1"]))
        
    def test_RemoveAll(self):
        #tests function RemoveAll()
        self.result.RemoveAll()
        self.assertEqual(len([x.Name for x in self.result.All()]),0) #length is expected to be = 0
    
    def test_Exists(self):
        #tests function Exists()
        self.assertEqual(self.result.Exists("L2"),True)
        self.assertEqual(self.result.Exists("X1"),False)
        
    def test_Remove(self):
        #tests function Remove()
        self.result.Remove("A1") #Remove parcel A1
        self.assertEqual(len([x.Name for x in self.result.All()]),4) #we have one less parcel
        self.assertEqual(self.result.Exists("A1"),False) #A1 shouldn't exist
        
        self.assertRaises(KeyError,self.result.Remove,"X1") #remove parcel X1, which doesn't exist and leads to KeyError
        self.assertEqual(len([x.Name for x in self.result.All()]),4) #no change after A1 above has been removed
        self.assertEqual(self.result.Exists("A1"),False) #X1 shouldn't exist
       
    def test_Count(self):
        #test count
        self.assertEqual(self.result.Count, 5)
        
    def test_LandParcels(self):
        #check land parcels
        LandPs = self.result.LandParcels
        self.assertIsInstance(LandPs, ParcelCollection)
        
        LandPsList = LandPs.All()
        self.assertEqual(set([x.Name for x in LandPsList]),set(["L1","L2"]))
        
    def test_WaterParcels(self):
        #check Water parcels
        WaterPs = self.result.WaterParcels
        self.assertIsInstance(WaterPs, ParcelCollection)
        
        WaterPsList = WaterPs.All()
        self.assertEqual(set([x.Name for x in WaterPsList]),set(["LakeCadillac","LakeMitchell"]))

    def test_AirParcels(self):
        #check Air parcels
        AirPs = self.result.AirParcels
        self.assertIsInstance(AirPs, ParcelCollection)
        
        AirPsList = AirPs.All()
        self.assertEqual(set([x.Name for x in AirPsList]),set(["L2","LakeMitchell","A1"]))

    def test_SurfaceParcels(self):
        #check Surface parcels
        SurfacePs = self.result.SurfaceParcels
        self.assertIsInstance(SurfacePs, ParcelCollection)
        
        SurfacePsList = SurfacePs.All()
        self.assertEqual(set([x.Name for x in SurfacePsList]),set(["L1","L2","LakeCadillac","LakeMitchell"]))

    def test_item(self):
        #test item function
        it = self.result.item("LakeCadillac")
        self.assertIsInstance(it, Parcel)
        self.assertEqual(it.Name,"LakeCadillac")
        
        #since the parent collection can be accessed from a single parcel...
        self.assertEqual(it.ParentCollection.Count,5)

    def test_ItemByName(self):
        #test item function
        itbn = self.result.ItemByName("LakeMitchell")
        self.assertIsInstance(itbn, Parcel)
        self.assertEqual(itbn.Name,"LakeMitchell")
        
        #since the parent collection can be accessed from a single parcel...
        self.assertEqual(itbn.ParentCollection.Count,5)
    
    def test_VolumeElements(self):
        #test VolumeElements function
        p_L1 = self.result.item("L1")
        p_L2 = self.result.item("L2")
        p_LakeCadillac = self.result.item("LakeCadillac")
        p_LakeMitchell = self.result.item("LakeMitchell")
        p_A1 = self.result.item("A1")
        
        self.assertEqual(set(p_L1.VolumeElements()),set(["SurfSoil_L1", "RootSoil_L1", "VadoseSoil_L1", "GW_L1"]))
        self.assertEqual(set(p_L2.VolumeElements()),set(["Air_L2","UpperAir_L2","SurfSoil_L2", "RootSoil_L2", "VadoseSoil_L2", "GW_L2"])) #Source = True
        self.assertEqual(set(p_LakeCadillac.VolumeElements()),set(["SW_LakeCadillac","Sed_LakeCadillac"]))
        self.assertEqual(set(p_LakeMitchell.VolumeElements()),set(["Air_LakeMitchell","SW_LakeMitchell","Sed_LakeMitchell"]))
        self.assertEqual(set(p_A1.VolumeElements()),set(["Air_A1"]))
        
        
    def test_Compartments(self):
        #tests the Compartments function and in the process tests, the Fish and Plants functions as well
        p_L1 = self.result.item("L1")
        p_L2 = self.result.item("L2")
        p_LakeCadillac = self.result.item("LakeCadillac")
        p_LakeMitchell = self.result.item("LakeMitchell")
        p_A1 = self.result.item("A1")
        
        LandUses = ["grass", "untilled soil",	"tilled soil", "coniferous forest", "deciduous forest", "agriculture"]
        PlantTypes = ["Grasses/Herbs", "", "", "Coniferous Forest", "Deciduous Forest", "Agriculture - General"]
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
        
        FishNames = ["Macrophyte",
                     "Zooplankton",
                     "Benthic Invertebrate",
                     "Water Column Herbivore",
                     "Benthic Omnivore",
                     "Water Column Omnivore",
                     "Benthic Carnivore",
                     "Water Column Carnivore"] * 2
        
        LakeNames = ["LakeCadillac"] * 8 + ["LakeMitchell"] * 8
        
        Locations = ["SW",
                     "SW",
                     "Sed",
                     "SW",
                     "Sed",
                     "SW",
                     "Sed",
                     "SW"] * 2
        
        #when all of the above is made into a GUI, things will look prettier and shorter
        self.assertEqual(set(p_L1.Compartments(LandUses, PlantTypes, CompositePlantComps, FishNames, LakeNames, Locations)),set(["Soil - Surface in SurfSoil_L1",
                                                                                                                                 "Soil Advection Sink in SurfSoil_L1",
                                                                                                                                 "Soil - Root Zone in RootSoil_L1",
                                                                                                                                 "Soil - Vadose Zone in VadoseSoil_L1",
                                                                                                                                 "Groundwater in GW_L1",
                                                                                                                                 "Degradation/Reaction Sink in SurfSoil_L1",
                                                                                                                                 "Degradation/Reaction Sink in RootSoil_L1",
                                                                                                                                 "Degradation/Reaction Sink in VadoseSoil_L1",
                                                                                                                                 "Degradation/Reaction Sink in GW_L1",
                                                                                                                                 "Leaf - Grasses/Herbs in Grasses/Herbs in SurfSoil_L1",
                                                                                                                                 "Leaf Particle - Grasses/Herbs in Grasses/Herbs in SurfSoil_L1",
                                                                                                                                 "Root - Grasses/Herbs in Grasses/Herbs in SurfSoil_L1",
                                                                                                                                 "Stem - Grasses/Herbs in Grasses/Herbs in SurfSoil_L1"
                                                                                                                                 ]))
        
        self.assertEqual(set(p_L2.Compartments(LandUses, PlantTypes, CompositePlantComps, FishNames, LakeNames, Locations)),set(["Air in Air_L2",
                                                                                                                                 "Degradation/Reaction Sink in Air_L2",
                                                                                                                                 "Soil - Surface in SurfSoil_L2",
                                                                                                                                 "Soil Advection Sink in SurfSoil_L2",
                                                                                                                                 "Soil - Root Zone in RootSoil_L2",
                                                                                                                                 "Soil - Vadose Zone in VadoseSoil_L2",
                                                                                                                                 "Groundwater in GW_L2",
                                                                                                                                 "Degradation/Reaction Sink in SurfSoil_L2",
                                                                                                                                 "Degradation/Reaction Sink in RootSoil_L2",
                                                                                                                                 "Degradation/Reaction Sink in VadoseSoil_L2",
                                                                                                                                 "Degradation/Reaction Sink in GW_L2",
                                                                                                                                 "Leaf - Deciduous Forest in Deciduous Forest in SurfSoil_L2",
                                                                                                                                 "Leaf Particle - Deciduous Forest in Deciduous Forest in SurfSoil_L2"]))
        
        self.assertEqual(set(p_LakeCadillac.Compartments(LandUses, PlantTypes, CompositePlantComps, FishNames, LakeNames, Locations)),set(["Surface water in SW_LakeCadillac",
                                                                                                                                           "Flush Rate Sink in SW_LakeCadillac",
                                                                                                                                           "Sediment in Sed_LakeCadillac",
                                                                                                                                           "Degradation/Reaction Sink in SW_LakeCadillac",
                                                                                                                                           "Macrophyte in SW_LakeCadillac",
                                                                                                                                           "Zooplankton in SW_LakeCadillac",
                                                                                                                                           "Water Column Herbivore in SW_LakeCadillac",
                                                                                                                                           "Water Column Omnivore in SW_LakeCadillac",
                                                                                                                                           "Water Column Carnivore in SW_LakeCadillac",
                                                                                                                                           "Degradation/Reaction Sink in Sed_LakeCadillac",
                                                                                                                                           "Benthic Invertebrate in Sed_LakeCadillac",
                                                                                                                                           "Benthic Omnivore in Sed_LakeCadillac",
                                                                                                                                           "Benthic Carnivore in Sed_LakeCadillac"]))
        
        self.assertEqual(set(p_LakeMitchell.Compartments(LandUses, PlantTypes, CompositePlantComps, FishNames, LakeNames, Locations)),set(["Air in Air_LakeMitchell",
                                                                                                                                           "Degradation/Reaction Sink in Air_LakeMitchell",
                                                                                                                                           "Surface water in SW_LakeMitchell",
                                                                                                                                           "Flush Rate Sink in SW_LakeMitchell",
                                                                                                                                           "Sediment in Sed_LakeMitchell",
                                                                                                                                           "Degradation/Reaction Sink in SW_LakeMitchell",
                                                                                                                                           "Macrophyte in SW_LakeMitchell",
                                                                                                                                           "Zooplankton in SW_LakeMitchell",
                                                                                                                                           "Water Column Herbivore in SW_LakeMitchell",
                                                                                                                                           "Water Column Omnivore in SW_LakeMitchell",
                                                                                                                                           "Water Column Carnivore in SW_LakeMitchell",
                                                                                                                                           "Degradation/Reaction Sink in Sed_LakeMitchell",
                                                                                                                                           "Benthic Invertebrate in Sed_LakeMitchell",
                                                                                                                                           "Benthic Omnivore in Sed_LakeMitchell",
                                                                                                                                           "Benthic Carnivore in Sed_LakeMitchell"]))
        
        self.assertEqual(set(p_A1.Compartments(LandUses, PlantTypes, CompositePlantComps, FishNames, LakeNames, Locations)),set(["Air in Air_A1",
                                                                                                                                 "Degradation/Reaction Sink in Air_A1"]))
        
        
        #...
        
if __name__ == '__main__':
    unittest.main()
    
    
    
    
    
    
    