### Note: This is an auto generated script

from math import log
from constants import *
from define_scenario import *
from define_attributes_props import *

class Chem_Divalent_Mercury:
	def __init__(self,Constants,containingScenario):
		self.containingScenario=containingScenario
		self.Constants=Constants
		self.Name='Chem_Divalent_Mercury'
		self.CAS='14302-87-5'
		self.category='Metals | Mercury | Divalent Mercury'
		self.D_pureair=0.478413366664244
		self.D_pureair_m2_s=self.D_pureair/86400
		self.D_purewater=5.53952319295441E-5
		self.D_purewater_m2_per_s=self.D_purewater/86400
		self.doesTransform='true'
		self.enabled='true'
		self.HenryLawConstant=7.193515704154E-5
		self.H_over_R_T=self.HenryLawConstant/(self.Constants.IdealGasConstant * self.containingScenario.AirTemperature_K)
		self.AirWaterPartitionCoefficient=self.H_over_R_T
		self.K_ow=3.33
		self.K_OA=self.K_ow*(self.Constants.IdealGasConstant * self.containingScenario.AirTemperature_K/ self.HenryLawConstant)
		self.K_oc=self.K_ow*0.48
		self.log10_K_OA=log(self.K_OA)/log(10.0)
		self.log10_K_ow=log(self.K_ow)/log(10.0)
		self.MeltingPoint=550.1
		self.molecularWeight=201.0
		self.Z_pureair=1 / (self.Constants.IdealGasConstant * self.containingScenario.AirTemperature_K)
		self.Z_purewater=1 / self.HenryLawConstant
		self.VaporWashoutRatio=1600000.0

class Chem_Elemental_Mercury:
	def __init__(self,Constants,containingScenario):
		self.containingScenario=containingScenario
		self.Constants=Constants
		self.Name='Chem_Elemental_Mercury'
		self.CAS='7439-97-6'
		self.category='Metals | Mercury | Elemental Mercury'
		self.D_pureair=0.478413366664244
		self.D_pureair_m2_s=self.D_pureair/86400
		self.D_purewater=5.53952319295441E-5
		self.D_purewater_m2_per_s=self.D_purewater/86400
		self.doesTransform='true'
		self.enabled='true'
		self.HenryLawConstant=719.3515704154
		self.H_over_R_T=self.HenryLawConstant/(self.Constants.IdealGasConstant * self.containingScenario.AirTemperature_K)
		self.AirWaterPartitionCoefficient=self.H_over_R_T
		self.K_ow=4.15
		self.K_OA=self.K_ow*(self.Constants.IdealGasConstant * self.containingScenario.AirTemperature_K/ self.HenryLawConstant)
		self.K_oc=self.K_ow*0.48
		self.log10_K_OA=log(self.K_OA)/log(10.0)
		self.log10_K_ow=log(self.K_ow)/log(10.0)
		self.MeltingPoint=234.23
		self.molecularWeight=201.0
		self.Z_pureair=1 / (self.Constants.IdealGasConstant * self.containingScenario.AirTemperature_K)
		self.Z_purewater=1 / self.HenryLawConstant
		self.VaporWashoutRatio=1200.0

class Chem_MethylMercury:
	def __init__(self,Constants,containingScenario):
		self.containingScenario=containingScenario
		self.Constants=Constants
		self.Name='Chem_MethylMercury'
		self.CAS='22967-92-6'
		self.category='Metals | Mercury | MethylMercury'
		self.D_pureair=0.456
		self.D_pureair_m2_s=self.D_pureair/86400
		self.D_purewater=5.28E-5
		self.D_purewater_m2_per_s=self.D_purewater/86400
		self.doesTransform='true'
		self.enabled='true'
		self.HenryLawConstant=0.0476190476190476
		self.H_over_R_T=self.HenryLawConstant/(self.Constants.IdealGasConstant * self.containingScenario.AirTemperature_K)
		self.AirWaterPartitionCoefficient=self.H_over_R_T
		self.K_ow=1.7
		self.K_OA=self.K_ow*(self.Constants.IdealGasConstant * self.containingScenario.AirTemperature_K/ self.HenryLawConstant)
		self.K_oc=self.K_ow*0.48
		self.log10_K_OA=log(self.K_OA)/log(10.0)
		self.log10_K_ow=log(self.K_ow)/log(10.0)
		self.MeltingPoint=443.0
		self.molecularWeight=216.0
		self.Z_pureair=1 / (self.Constants.IdealGasConstant * self.containingScenario.AirTemperature_K)
		self.Z_purewater=1 / self.HenryLawConstant
		self.VaporWashoutRatio=0.0
		self.reportAsOtherChemical='Hg'
		self.molesOfReportingChemicalPerMolesOfThisChemical=1
		self.reportingChemicalMW=201.0

chem_objects_dict={}
Chem_Divalent_Mercury=Chem_Divalent_Mercury(Constants,containingScenario)
chem_objects_dict["Chem_Divalent_Mercury"]=Chem_Divalent_Mercury
Chem_Elemental_Mercury=Chem_Elemental_Mercury(Constants,containingScenario)
chem_objects_dict["Chem_Elemental_Mercury"]=Chem_Elemental_Mercury
Chem_MethylMercury=Chem_MethylMercury(Constants,containingScenario)
chem_objects_dict["Chem_MethylMercury"]=Chem_MethylMercury
