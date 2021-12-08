### note: this is an auto generated script
from math import log, log10
from numpy import nan, sqrt, exp

def linkedCompartmentvalue(containingvolumeelement,comp_objects_dict,primary_abiotic,prop_name):
    ve_name=containingvolumeelement.ve_name
    if primary_abiotic==containingvolumeelement.primary_abiotic.replace(' ','_'): # if else is a dirty hack in place of a robust link checking process       
        comp_name=primary_abiotic+'_in_'+ve_name
    else:
        if containingvolumeelement.primary_abiotic=='sediment' and primary_abiotic=='surface_water':
             comp_name='surface_water'+'_in_sw_'+containingvolumeelement.parcel_name    
    val_str='comp_objects_dict["'+comp_name+'"].'+prop_name
    val=eval(val_str)
    return(val)  
    
class advection_sink:
	def __init__(self,constants,containingscenario,currentchemical,containingvolumeelement,comp_objects_dict):
		self.containingscenario=containingscenario
		self.currentchemical=currentchemical
		self.constants=constants
		self.containingvolumeelement=containingvolumeelement
		self.comp_objects_dict=comp_objects_dict
	@property
	def isbiotic(self):
		return (False)
	
	@property
	def category(self):
		return ("sink | abiotic | air | air - default")
	
	@property
	def acceptableabiotic(self):
		return ("nan")
	
	_concentrationoutputfactor=1.0
	@property
	def concentrationoutputfactor(self):
		return self._concentrationoutputfactor
	@concentrationoutputfactor.setter
	def concentrationoutputfactor(self,value):
		self._concentrationoutputfactor=value

	@property
	def concentrationoutputunits(self):
		return ("0.01")
	
class air:
	def __init__(self,constants,containingscenario,currentchemical,containingvolumeelement,comp_objects_dict):
		self.containingscenario=containingscenario
		self.currentchemical=currentchemical
		self.constants=constants
		self.containingvolumeelement=containingvolumeelement
		self.comp_objects_dict=comp_objects_dict
	_fractionorganicmatteronparticulates=0.2
	@property
	def fractionorganicmatteronparticulates(self):
		return self._fractionorganicmatteronparticulates
	@fractionorganicmatteronparticulates.setter
	def fractionorganicmatteronparticulates(self,value):
		self._fractionorganicmatteronparticulates=value

	@property
	def generaldegradationrate(self):
		cdict={}
		return cdict

	@property
	def chemical_generaldegradationrate(self):
		return self.generaldegradationrate[self.currentchemical.name]
	_airdensity_g_cm3=0.0012
	@property
	def airdensity_g_cm3(self):
		return self._airdensity_g_cm3
	@airdensity_g_cm3.setter
	def airdensity_g_cm3(self,value):
		self._airdensity_g_cm3=value

	@property
	def acceptableabiotic(self):
		return ("nan")
	
	@property
	def airdensity_kg_m3(self):
		return (self.airdensity_g_cm3 * 1000.0)
	
	@property
	def vaporwashoutratio(self):
		cdict={}
		try:
			cdict["chem_divalent_mercury"]=self.currentchemical.vaporwashoutratio
		except:
			cdict["chem_divalent_mercury"]=nan
		
		try:
			cdict["chem_elemental_mercury"]=self.currentchemical.vaporwashoutratio
		except:
			cdict["chem_elemental_mercury"]=nan
		
		try:
			cdict["chem_methylmercury"]=self.currentchemical.vaporwashoutratio
		except:
			cdict["chem_methylmercury"]=nan
		
		return cdict

	@property
	def chemical_vaporwashoutratio(self):
		return self.vaporwashoutratio[self.currentchemical.name]
	_dustdensity=1400.0
	@property
	def dustdensity(self):
		return self._dustdensity
	@dustdensity.setter
	def dustdensity(self,value):
		self._dustdensity=value

	@property
	def fractionmass_sorbed(self):
		cdict={}
		try:
			cdict["chem_divalent_mercury"]=1 - 1/(1+self.chemical_particlegaspartitioncoefficient * self.dustload* self.constants.ug_per_kg)
		except:
			cdict["chem_divalent_mercury"]=nan
		
		try:
			cdict["chem_elemental_mercury"]=1 - 1/(1+self.chemical_particlegaspartitioncoefficient * self.dustload* self.constants.ug_per_kg)
		except:
			cdict["chem_elemental_mercury"]=nan
		
		try:
			cdict["chem_methylmercury"]=1 - 1/(1+self.chemical_particlegaspartitioncoefficient * self.dustload* self.constants.ug_per_kg)
		except:
			cdict["chem_methylmercury"]=nan
		
		return cdict

	@property
	def chemical_fractionmass_sorbed(self):
		return self.fractionmass_sorbed[self.currentchemical.name]
	@property
	def reductionrate(self):
		cdict={}
		try:
			cdict["chem_divalent_mercury"]=0.0
		except:
			cdict["chem_divalent_mercury"]=nan
		
		return cdict

	@property
	def chemical_reductionrate(self):
		return self.reductionrate[self.currentchemical.name]
	@property
	def halflife(self):
		cdict={}
		return cdict

	@property
	def chemical_halflife(self):
		return self.halflife[self.currentchemical.name]
	@property
	def initialconcentration_g_per_m3_usersupplied(self):
		cdict={}
		try:
			cdict["chem_divalent_mercury"]=0.0
		except:
			cdict["chem_divalent_mercury"]=nan
		
		try:
			cdict["chem_elemental_mercury"]=0.0
		except:
			cdict["chem_elemental_mercury"]=nan
		
		try:
			cdict["chem_methylmercury"]=0.0
		except:
			cdict["chem_methylmercury"]=nan
		
		return cdict

	@property
	def chemical_initialconcentration_g_per_m3_usersupplied(self):
		return self.initialconcentration_g_per_m3_usersupplied[self.currentchemical.name]
	@property
	def volumefraction_solid(self):
		return (self.volumetricairparticlecontent)
	
	@property
	def isbiotic(self):
		return (False)
	
	@property
	def particlevolumetricwetdepositionrate(self):
		cdict={}
		try:
			cdict["chem_divalent_mercury"]=self.chemical_washoutratio * self.containingscenario.rain * (self.dustload / self.dustdensity)
		except:
			cdict["chem_divalent_mercury"]=nan
		
		try:
			cdict["chem_elemental_mercury"]=self.chemical_washoutratio * self.containingscenario.rain * (self.dustload / self.dustdensity)
		except:
			cdict["chem_elemental_mercury"]=nan
		
		try:
			cdict["chem_methylmercury"]=self.chemical_washoutratio * self.containingscenario.rain * (self.dustload / self.dustdensity)
		except:
			cdict["chem_methylmercury"]=nan
		
		return cdict

	@property
	def chemical_particlevolumetricwetdepositionrate(self):
		return self.particlevolumetricwetdepositionrate[self.currentchemical.name]
	@property
	def volumetricairaircontent(self):
		return (1 - self.dustload / self.dustdensity)
	
	@property
	def methylationrate(self):
		cdict={}
		try:
			cdict["chem_divalent_mercury"]=0.0
		except:
			cdict["chem_divalent_mercury"]=nan
		
		return cdict

	@property
	def chemical_methylationrate(self):
		return self.methylationrate[self.currentchemical.name]
	@property
	def washoutratio(self):
		cdict={}
		try:
			cdict["chem_divalent_mercury"]=200000.0
		except:
			cdict["chem_divalent_mercury"]=nan
		
		try:
			cdict["chem_elemental_mercury"]=200000.0
		except:
			cdict["chem_elemental_mercury"]=nan
		
		try:
			cdict["chem_methylmercury"]=200000.0
		except:
			cdict["chem_methylmercury"]=nan
		
		return cdict

	@property
	def chemical_washoutratio(self):
		return self.washoutratio[self.currentchemical.name]
	@property
	def genericdenominatorforcalculatingfractioninphases(self):
		cdict={}
		return cdict

	@property
	def chemical_genericdenominatorforcalculatingfractioninphases(self):
		return self.genericdenominatorforcalculatingfractioninphases[self.currentchemical.name]
	@property
	def airschmidtnumber(self):
		cdict={}
		try:
			cdict["chem_divalent_mercury"]=self.dynamicairviscosity_m2_per_sec/self.currentchemical.d_pureair_m2_s
		except:
			cdict["chem_divalent_mercury"]=nan
		
		try:
			cdict["chem_elemental_mercury"]=self.dynamicairviscosity_m2_per_sec/self.currentchemical.d_pureair_m2_s
		except:
			cdict["chem_elemental_mercury"]=nan
		
		try:
			cdict["chem_methylmercury"]=self.dynamicairviscosity_m2_per_sec/self.currentchemical.d_pureair_m2_s
		except:
			cdict["chem_methylmercury"]=nan
		
		return cdict

	@property
	def chemical_airschmidtnumber(self):
		return self.airschmidtnumber[self.currentchemical.name]
	@property
	def vdep(self):
		cdict={}
		try:
			cdict["chem_divalent_mercury"]=500.0
		except:
			cdict["chem_divalent_mercury"]=nan
		
		try:
			cdict["chem_elemental_mercury"]=500.0
		except:
			cdict["chem_elemental_mercury"]=nan
		
		try:
			cdict["chem_methylmercury"]=500.0
		except:
			cdict["chem_methylmercury"]=nan
		
		return cdict

	@property
	def chemical_vdep(self):
		return self.vdep[self.currentchemical.name]
	@property
	def volumetricairparticlecontent(self):
		return (self.dustload / self.dustdensity)
	
	@property
	def z_liquid(self):
		cdict={}
		try:
			cdict["chem_divalent_mercury"]=self.currentchemical.z_purewater
		except:
			cdict["chem_divalent_mercury"]=nan
		
		try:
			cdict["chem_elemental_mercury"]=self.currentchemical.z_purewater
		except:
			cdict["chem_elemental_mercury"]=nan
		
		try:
			cdict["chem_methylmercury"]=self.currentchemical.z_purewater
		except:
			cdict["chem_methylmercury"]=nan
		
		return cdict

	@property
	def chemical_z_liquid(self):
		return self.z_liquid[self.currentchemical.name]
	@property
	def category(self):
		return ("abiotic | air | air - default")
	
	@property
	def particlegaspartitioncoefficient(self):
		cdict={}
		try:
			cdict["chem_divalent_mercury"]=10** ( self.currentchemical.log10_k_oa  + log(self.fractionorganicmatteronparticulates+1.0e-10)/log(10) - 11.91)
		except:
			cdict["chem_divalent_mercury"]=nan
		
		try:
			cdict["chem_elemental_mercury"]=10** ( self.currentchemical.log10_k_oa  + log(self.fractionorganicmatteronparticulates+1.0e-10)/log(10) - 11.91)
		except:
			cdict["chem_elemental_mercury"]=nan
		
		try:
			cdict["chem_methylmercury"]=10** ( self.currentchemical.log10_k_oa  + log(self.fractionorganicmatteronparticulates+1.0e-10)/log(10) - 11.91)
		except:
			cdict["chem_methylmercury"]=nan
		
		return cdict

	@property
	def chemical_particlegaspartitioncoefficient(self):
		return self.particlegaspartitioncoefficient[self.currentchemical.name]
	@property
	def z_solid(self):
		cdict={}
		try:
			cdict["chem_divalent_mercury"]=self.chemical_z_vapor * (self.chemical_fractionmass_sorbed/self.volumetricairparticlecontent)/(self.chemical_fractionmass_vapor/self.volumetricairaircontent)
		except:
			cdict["chem_divalent_mercury"]=nan
		
		try:
			cdict["chem_elemental_mercury"]=self.chemical_z_vapor * (self.chemical_fractionmass_sorbed/self.volumetricairparticlecontent)/(self.chemical_fractionmass_vapor/self.volumetricairaircontent)
		except:
			cdict["chem_elemental_mercury"]=nan
		
		try:
			cdict["chem_methylmercury"]=self.chemical_z_vapor * (self.chemical_fractionmass_sorbed/self.volumetricairparticlecontent)/(self.chemical_fractionmass_vapor/self.volumetricairaircontent)
		except:
			cdict["chem_methylmercury"]=nan
		
		return cdict

	@property
	def chemical_z_solid(self):
		return self.z_solid[self.currentchemical.name]
	@property
	def fractionmass_vapor(self):
		cdict={}
		try:
			cdict["chem_divalent_mercury"]=1 -self.chemical_fractionmass_sorbed
		except:
			cdict["chem_divalent_mercury"]=nan
		
		try:
			cdict["chem_elemental_mercury"]=1 -self.chemical_fractionmass_sorbed
		except:
			cdict["chem_elemental_mercury"]=nan
		
		try:
			cdict["chem_methylmercury"]=1 -self.chemical_fractionmass_sorbed
		except:
			cdict["chem_methylmercury"]=nan
		
		return cdict

	@property
	def chemical_fractionmass_vapor(self):
		return self.fractionmass_vapor[self.currentchemical.name]
	@property
	def z_total(self):
		cdict={}
		try:
			cdict["chem_divalent_mercury"]=self.chemical_z_solid * (self.dustload /self.dustdensity) +self.chemical_z_vapor * (1 - (self.dustload /self.dustdensity))
		except:
			cdict["chem_divalent_mercury"]=nan
		
		try:
			cdict["chem_elemental_mercury"]=self.chemical_z_solid * (self.dustload /self.dustdensity) +self.chemical_z_vapor * (1 - (self.dustload /self.dustdensity))
		except:
			cdict["chem_elemental_mercury"]=nan
		
		try:
			cdict["chem_methylmercury"]=self.chemical_z_solid * (self.dustload /self.dustdensity) +self.chemical_z_vapor * (1 - (self.dustload /self.dustdensity))
		except:
			cdict["chem_methylmercury"]=nan
		
		return cdict

	@property
	def chemical_z_total(self):
		return self.z_total[self.currentchemical.name]
	@property
	def concentrationoutputunits(self):
		return ("ug/m3")
	
	@property
	def dynamicairviscosity_cm2_per_sec(self):
		return ((1.32 + 0.009 * self.airtemperature_c)/10.0)
	
	@property
	def area(self):
		return (self.containingvolumeelement.area)
	
	@property
	def initialconcentration_g_per_m3(self):
		cdict={}
		try:
			cdict["chem_divalent_mercury"]=self.containingscenario.fractioninitialconcentrations * self.chemical_initialconcentration_g_per_m3_usersupplied
		except:
			cdict["chem_divalent_mercury"]=nan
		
		try:
			cdict["chem_elemental_mercury"]=self.containingscenario.fractioninitialconcentrations * self.chemical_initialconcentration_g_per_m3_usersupplied
		except:
			cdict["chem_elemental_mercury"]=nan
		
		try:
			cdict["chem_methylmercury"]=self.containingscenario.fractioninitialconcentrations * self.chemical_initialconcentration_g_per_m3_usersupplied
		except:
			cdict["chem_methylmercury"]=nan
		
		return cdict

	@property
	def chemical_initialconcentration_g_per_m3(self):
		return self.initialconcentration_g_per_m3[self.currentchemical.name]
	@property
	def z_vapor(self):
		cdict={}
		try:
			cdict["chem_divalent_mercury"]=self.currentchemical.z_pureair
		except:
			cdict["chem_divalent_mercury"]=nan
		
		try:
			cdict["chem_elemental_mercury"]=self.currentchemical.z_pureair
		except:
			cdict["chem_elemental_mercury"]=nan
		
		try:
			cdict["chem_methylmercury"]=self.currentchemical.z_pureair
		except:
			cdict["chem_methylmercury"]=nan
		
		return cdict

	@property
	def chemical_z_vapor(self):
		return self.z_vapor[self.currentchemical.name]
	@property
	def particlevolumetricdrydepositionrate(self):
		cdict={}
		try:
			cdict["chem_divalent_mercury"]=self.chemical_vdep * (self.dustload / self.dustdensity)
		except:
			cdict["chem_divalent_mercury"]=nan
		
		try:
			cdict["chem_elemental_mercury"]=self.chemical_vdep * (self.dustload / self.dustdensity)
		except:
			cdict["chem_elemental_mercury"]=nan
		
		try:
			cdict["chem_methylmercury"]=self.chemical_vdep * (self.dustload / self.dustdensity)
		except:
			cdict["chem_methylmercury"]=nan
		
		return cdict

	@property
	def chemical_particlevolumetricdrydepositionrate(self):
		return self.particlevolumetricdrydepositionrate[self.currentchemical.name]
	_dustload=6.15e-8
	@property
	def dustload(self):
		return self._dustload
	@dustload.setter
	def dustload(self,value):
		self._dustload=value

	_concentrationoutputfactor=1000000.0
	@property
	def concentrationoutputfactor(self):
		return self._concentrationoutputfactor
	@concentrationoutputfactor.setter
	def concentrationoutputfactor(self,value):
		self._concentrationoutputfactor=value

	@property
	def oxidationrate(self):
		cdict={}
		try:
			cdict["chem_elemental_mercury"]=0.00385081766977747
		except:
			cdict["chem_elemental_mercury"]=nan
		
		return cdict

	@property
	def chemical_oxidationrate(self):
		return self.oxidationrate[self.currentchemical.name]
	@property
	def demethylationrate(self):
		cdict={}
		try:
			cdict["chem_methylmercury"]=0.0
		except:
			cdict["chem_methylmercury"]=nan
		
		return cdict

	@property
	def chemical_demethylationrate(self):
		return self.demethylationrate[self.currentchemical.name]
	@property
	def dynamicairviscosity_m2_per_sec(self):
		return (self.dynamicairviscosity_cm2_per_sec/1e4)
	
	@property
	def airtemperature_c(self):
		return (self.containingscenario.airtemperature_k - 273)
	
	@property
	def dustresuspensionrate(self):
		cdict={}
		try:
			cdict["chem_divalent_mercury"]=self.chemical_particlevolumetricdrydepositionrate
		except:
			cdict["chem_divalent_mercury"]=nan
		
		try:
			cdict["chem_elemental_mercury"]=self.chemical_particlevolumetricdrydepositionrate
		except:
			cdict["chem_elemental_mercury"]=nan
		
		try:
			cdict["chem_methylmercury"]=self.chemical_particlevolumetricdrydepositionrate
		except:
			cdict["chem_methylmercury"]=nan
		
		return cdict

	@property
	def chemical_dustresuspensionrate(self):
		return self.dustresuspensionrate[self.currentchemical.name]
	@property
	def height(self):
		return (self.containingvolumeelement.height)
	
	@property
	def volume(self):
		return (self.containingvolumeelement.volume)
	
	@property
	def volumefraction_vapor(self):
		return (self.volumetricairaircontent)
	
class benthic_carnivore:
	def __init__(self,constants,containingscenario,currentchemical,containingvolumeelement,comp_objects_dict):
		self.containingscenario=containingscenario
		self.currentchemical=currentchemical
		self.constants=constants
		self.containingvolumeelement=containingvolumeelement
		self.comp_objects_dict=comp_objects_dict
	@property
	def generaldegradationrate(self):
		cdict={}
		return cdict

	@property
	def chemical_generaldegradationrate(self):
		return self.generaldegradationrate[self.currentchemical.name]
	@property
	def initialconcentration_g_per_kg_usersupplied(self):
		cdict={}
		try:
			cdict["chem_divalent_mercury"]=0.0
		except:
			cdict["chem_divalent_mercury"]=nan
		
		try:
			cdict["chem_elemental_mercury"]=0.0
		except:
			cdict["chem_elemental_mercury"]=nan
		
		try:
			cdict["chem_methylmercury"]=0.0
		except:
			cdict["chem_methylmercury"]=nan
		
		return cdict

	@property
	def chemical_initialconcentration_g_per_kg_usersupplied(self):
		return self.initialconcentration_g_per_kg_usersupplied[self.currentchemical.name]
	@property
	def assimilationefficiencyfromfood(self):
		cdict={}
		try:
			cdict["chem_divalent_mercury"]=0.06
		except:
			cdict["chem_divalent_mercury"]=nan
		
		try:
			cdict["chem_elemental_mercury"]=0.06
		except:
			cdict["chem_elemental_mercury"]=nan
		
		try:
			cdict["chem_methylmercury"]=0.5
		except:
			cdict["chem_methylmercury"]=nan
		
		return cdict

	@property
	def chemical_assimilationefficiencyfromfood(self):
		return self.assimilationefficiencyfromfood[self.currentchemical.name]
	@property
	def acceptableabiotic(self):
		return ("abiotic | sediment | sediment - default")
	
	@property
	def foodingestionrate(self):
		return (self.feedingrate/self.bw)
	
	@property
	def reductionrate(self):
		cdict={}
		try:
			cdict["chem_divalent_mercury"]=0.0
		except:
			cdict["chem_divalent_mercury"]=nan
		
		return cdict

	@property
	def chemical_reductionrate(self):
		return self.reductionrate[self.currentchemical.name]
	_fishlipidfraction=0.057
	@property
	def fishlipidfraction(self):
		return self._fishlipidfraction
	@fishlipidfraction.setter
	def fishlipidfraction(self,value):
		self._fishlipidfraction=value

	@property
	def image(self):
		return ("c:\models\trim\data\images\creekchub.gif")
	
	_bw=2.0
	@property
	def bw(self):
		return self._bw
	@bw.setter
	def bw(self,value):
		self._bw=value

	@property
	def halflife(self):
		cdict={}
		return cdict

	@property
	def chemical_halflife(self):
		return self.halflife[self.currentchemical.name]
	@property
	def feedingrate(self):
		return (0.022 * self.bw ** (0.85) * exp(0.06 * linkedCompartmentvalue(self.containingvolumeelement,self.comp_objects_dict,"surface_water","watertemperature_c")))
	
	@property
	def initialconcentration_g_per_kg(self):
		cdict={}
		try:
			cdict["chem_divalent_mercury"]=self.containingscenario.fractioninitialconcentrations * self.chemical_initialconcentration_g_per_kg_usersupplied
		except:
			cdict["chem_divalent_mercury"]=nan
		
		try:
			cdict["chem_elemental_mercury"]=self.containingscenario.fractioninitialconcentrations * self.chemical_initialconcentration_g_per_kg_usersupplied
		except:
			cdict["chem_elemental_mercury"]=nan
		
		try:
			cdict["chem_methylmercury"]=self.containingscenario.fractioninitialconcentrations * self.chemical_initialconcentration_g_per_kg_usersupplied
		except:
			cdict["chem_methylmercury"]=nan
		
		return cdict

	@property
	def chemical_initialconcentration_g_per_kg(self):
		return self.initialconcentration_g_per_kg[self.currentchemical.name]
	@property
	def isbiotic(self):
		return (True)
	
	@property
	def methylationrate(self):
		cdict={}
		try:
			cdict["chem_divalent_mercury"]=0.0
		except:
			cdict["chem_divalent_mercury"]=nan
		
		return cdict

	@property
	def chemical_methylationrate(self):
		return self.methylationrate[self.currentchemical.name]
	@property
	def gilleliminationrate(self):
		cdict={}
		return cdict

	@property
	def chemical_gilleliminationrate(self):
		return self.gilleliminationrate[self.currentchemical.name]
	@property
	def eliminationrateconstant(self):
		cdict={}
		try:
			cdict["chem_divalent_mercury"]=self.chemical_howmuchfasterhgeliminationisthanformhg * exp(0.066*linkedCompartmentvalue(self.containingvolumeelement,self.comp_objects_dict,"surface_water","watertemperature_c") - 0.20 * log(1000.0*self.bw) - 5.83)
		except:
			cdict["chem_divalent_mercury"]=nan
		
		try:
			cdict["chem_elemental_mercury"]=self.chemical_howmuchfasterhgeliminationisthanformhg * exp(0.066*linkedCompartmentvalue(self.containingvolumeelement,self.comp_objects_dict,"surface_water","watertemperature_c") - 0.20 * log(1000.0*self.bw) -5.83)
		except:
			cdict["chem_elemental_mercury"]=nan
		
		try:
			cdict["chem_methylmercury"]=self.chemical_howmuchfasterhgeliminationisthanformhg * exp(0.066*linkedCompartmentvalue(self.containingvolumeelement,self.comp_objects_dict,"surface_water","watertemperature_c") - 0.20 * log(1000.0*self.bw) -5.83)
		except:
			cdict["chem_methylmercury"]=nan
		
		return cdict

	@property
	def chemical_eliminationrateconstant(self):
		return self.eliminationrateconstant[self.currentchemical.name]
	@property
	def gamma_fish(self):
		cdict={}
		return cdict

	@property
	def chemical_gamma_fish(self):
		return self.gamma_fish[self.currentchemical.name]
	@property
	def absorptionrateconstant(self):
		cdict={}
		return cdict

	@property
	def chemical_absorptionrateconstant(self):
		return self.absorptionrateconstant[self.currentchemical.name]
	@property
	def category(self):
		return ("fish | benthic carnivore")
	
	_fractiondietfishbenthicomnivore=0.01
	@property
	def fractiondietfishbenthicomnivore(self):
		return self._fractiondietfishbenthicomnivore
	@fractiondietfishbenthicomnivore.setter
	def fractiondietfishbenthicomnivore(self,value):
		self._fractiondietfishbenthicomnivore=value

	_fractiondietfishomnivore=0.01
	@property
	def fractiondietfishomnivore(self):
		return self._fractiondietfishomnivore
	@fractiondietfishomnivore.setter
	def fractiondietfishomnivore(self,value):
		self._fractiondietfishomnivore=value

	@property
	def concentrationoutputunits(self):
		return ("mg/kg wet weight")
	
	@property
	def fishchemicaluptakerateviagill(self):
		cdict={}
		return cdict

	@property
	def chemical_fishchemicaluptakerateviagill(self):
		return self.fishchemicaluptakerateviagill[self.currentchemical.name]
	@property
	def numberoffishpersquaremeter(self):
		return (self.biomassperarea_kg_m2/self.bw)
	
	_biomassperarea_kg_m2=0.01
	@property
	def biomassperarea_kg_m2(self):
		return self._biomassperarea_kg_m2
	@biomassperarea_kg_m2.setter
	def biomassperarea_kg_m2(self,value):
		self._biomassperarea_kg_m2=value

	@property
	def howmuchfasterhgeliminationisthanformhg(self):
		cdict={}
		try:
			cdict["chem_divalent_mercury"]=3.0
		except:
			cdict["chem_divalent_mercury"]=nan
		
		try:
			cdict["chem_elemental_mercury"]=3.0
		except:
			cdict["chem_elemental_mercury"]=nan
		
		try:
			cdict["chem_methylmercury"]=1.0
		except:
			cdict["chem_methylmercury"]=nan
		
		return cdict

	@property
	def chemical_howmuchfasterhgeliminationisthanformhg(self):
		return self.howmuchfasterhgeliminationisthanformhg[self.currentchemical.name]
	_concentrationoutputfactor=1000.0
	@property
	def concentrationoutputfactor(self):
		return self._concentrationoutputfactor
	@concentrationoutputfactor.setter
	def concentrationoutputfactor(self,value):
		self._concentrationoutputfactor=value

	@property
	def oxidationrate(self):
		cdict={}
		try:
			cdict["chem_elemental_mercury"]=1000000.0
		except:
			cdict["chem_elemental_mercury"]=nan
		
		return cdict

	@property
	def chemical_oxidationrate(self):
		return self.oxidationrate[self.currentchemical.name]
	@property
	def demethylationrate(self):
		cdict={}
		try:
			cdict["chem_methylmercury"]=0.0
		except:
			cdict["chem_methylmercury"]=nan
		
		return cdict

	@property
	def chemical_demethylationrate(self):
		return self.demethylationrate[self.currentchemical.name]
	_fractiondietfishcarnivore=0.01
	@property
	def fractiondietfishcarnivore(self):
		return self._fractiondietfishcarnivore
	@fractiondietfishcarnivore.setter
	def fractiondietfishcarnivore(self,value):
		self._fractiondietfishcarnivore=value

	@property
	def chemicaltransferefficiencyinfish(self):
		cdict={}
		return cdict

	@property
	def chemical_chemicaltransferefficiencyinfish(self):
		return self.chemicaltransferefficiencyinfish[self.currentchemical.name]
	_fractiondietalgae=0.01
	@property
	def fractiondietalgae(self):
		return self._fractiondietalgae
	@fractiondietalgae.setter
	def fractiondietalgae(self,value):
		self._fractiondietalgae=value

	@property
	def populationsize(self):
		return (self.numberoffishpersquaremeter * self.containingvolumeelement.area)
	
	@property
	def totalmass(self):
		return (self.populationsize  * self.bw)
	
	_fractiondietbenthicinvertebrate=0.01
	@property
	def fractiondietbenthicinvertebrate(self):
		return self._fractiondietbenthicinvertebrate
	@fractiondietbenthicinvertebrate.setter
	def fractiondietbenthicinvertebrate(self,value):
		self._fractiondietbenthicinvertebrate=value

	_fractiondietfishherbivore=0.01
	@property
	def fractiondietfishherbivore(self):
		return self._fractiondietfishherbivore
	@fractiondietfishherbivore.setter
	def fractiondietfishherbivore(self,value):
		self._fractiondietfishherbivore=value

class benthic_invertebrate:
	def __init__(self,constants,containingscenario,currentchemical,containingvolumeelement,comp_objects_dict):
		self.containingscenario=containingscenario
		self.currentchemical=currentchemical
		self.constants=constants
		self.containingvolumeelement=containingvolumeelement
		self.comp_objects_dict=comp_objects_dict
	@property
	def generaldegradationrate(self):
		cdict={}
		return cdict

	@property
	def chemical_generaldegradationrate(self):
		return self.generaldegradationrate[self.currentchemical.name]
	@property
	def initialconcentration_g_per_kg_usersupplied(self):
		cdict={}
		try:
			cdict["chem_divalent_mercury"]=0.0
		except:
			cdict["chem_divalent_mercury"]=nan
		
		try:
			cdict["chem_elemental_mercury"]=0.0
		except:
			cdict["chem_elemental_mercury"]=nan
		
		try:
			cdict["chem_methylmercury"]=0.0
		except:
			cdict["chem_methylmercury"]=nan
		
		return cdict

	@property
	def chemical_initialconcentration_g_per_kg_usersupplied(self):
		return self.initialconcentration_g_per_kg_usersupplied[self.currentchemical.name]
	@property
	def acceptableabiotic(self):
		return ("abiotic | sediment | sediment - default")
	
	@property
	def image(self):
		return ("c:\models\trim\data\images\mayfly.gif")
	
	_bw=2.55e-4
	@property
	def bw(self):
		return self._bw
	@bw.setter
	def bw(self,value):
		self._bw=value

	@property
	def halflife(self):
		cdict={}
		return cdict

	@property
	def chemical_halflife(self):
		return self.halflife[self.currentchemical.name]
	@property
	def initialconcentration_g_per_kg(self):
		cdict={}
		try:
			cdict["chem_divalent_mercury"]=self.containingscenario.fractioninitialconcentrations * self.chemical_initialconcentration_g_per_kg_usersupplied
		except:
			cdict["chem_divalent_mercury"]=nan
		
		try:
			cdict["chem_elemental_mercury"]=self.containingscenario.fractioninitialconcentrations * self.chemical_initialconcentration_g_per_kg_usersupplied
		except:
			cdict["chem_elemental_mercury"]=nan
		
		try:
			cdict["chem_methylmercury"]=self.containingscenario.fractioninitialconcentrations * self.chemical_initialconcentration_g_per_kg_usersupplied
		except:
			cdict["chem_methylmercury"]=nan
		
		return cdict

	@property
	def chemical_initialconcentration_g_per_kg(self):
		return self.initialconcentration_g_per_kg[self.currentchemical.name]
	@property
	def isbiotic(self):
		return (True)
	
	@property
	def sedimentpartitioning_alphaofequilibrium(self):
		cdict={}
		try:
			cdict["chem_divalent_mercury"]=0.95
		except:
			cdict["chem_divalent_mercury"]=nan
		
		try:
			cdict["chem_elemental_mercury"]=0.95
		except:
			cdict["chem_elemental_mercury"]=nan
		
		try:
			cdict["chem_methylmercury"]=0.95
		except:
			cdict["chem_methylmercury"]=nan
		
		return cdict

	@property
	def chemical_sedimentpartitioning_alphaofequilibrium(self):
		return self.sedimentpartitioning_alphaofequilibrium[self.currentchemical.name]
	@property
	def clearanceconstant(self):
		cdict={}
		return cdict

	@property
	def chemical_clearanceconstant(self):
		return self.clearanceconstant[self.currentchemical.name]
	@property
	def category(self):
		return ("insect | benthic invertebrate")
	
	@property
	def uptakeconstant(self):
		cdict={}
		return cdict

	@property
	def chemical_uptakeconstant(self):
		return self.uptakeconstant[self.currentchemical.name]
	@property
	def sedimentpartitioning_partitioncoefficient(self):
		cdict={}
		try:
			cdict["chem_divalent_mercury"]=0.0824
		except:
			cdict["chem_divalent_mercury"]=nan
		
		try:
			cdict["chem_elemental_mercury"]=0.0824
		except:
			cdict["chem_elemental_mercury"]=nan
		
		try:
			cdict["chem_methylmercury"]=5.04
		except:
			cdict["chem_methylmercury"]=nan
		
		return cdict

	@property
	def chemical_sedimentpartitioning_partitioncoefficient(self):
		return self.sedimentpartitioning_partitioncoefficient[self.currentchemical.name]
	@property
	def concentrationoutputunits(self):
		return ("mg/kg wet weight")
	
	_biomassperarea_kg_m2=0.02
	@property
	def biomassperarea_kg_m2(self):
		return self._biomassperarea_kg_m2
	@biomassperarea_kg_m2.setter
	def biomassperarea_kg_m2(self,value):
		self._biomassperarea_kg_m2=value

	@property
	def abbreviation(self):
		cdict={}
		return cdict

	@property
	def chemical_abbreviation(self):
		return self.abbreviation[self.currentchemical.name]
	_concentrationoutputfactor=1000.0
	@property
	def concentrationoutputfactor(self):
		return self._concentrationoutputfactor
	@concentrationoutputfactor.setter
	def concentrationoutputfactor(self,value):
		self._concentrationoutputfactor=value

	@property
	def populationsize(self):
		return (self.totalmass/self.bw)
	
	@property
	def totalmass(self):
		return (self.biomassperarea_kg_m2 * self.containingvolumeelement.area)
	
	@property
	def sedimentpartitioning_timetoreachalphaofequilibrium(self):
		cdict={}
		try:
			cdict["chem_divalent_mercury"]=14.0
		except:
			cdict["chem_divalent_mercury"]=nan
		
		try:
			cdict["chem_elemental_mercury"]=14.0
		except:
			cdict["chem_elemental_mercury"]=nan
		
		try:
			cdict["chem_methylmercury"]=14.0
		except:
			cdict["chem_methylmercury"]=nan
		
		return cdict

	@property
	def chemical_sedimentpartitioning_timetoreachalphaofequilibrium(self):
		return self.sedimentpartitioning_timetoreachalphaofequilibrium[self.currentchemical.name]
	@property
	def v_d(self):
		cdict={}
		return cdict

	@property
	def chemical_v_d(self):
		return self.v_d[self.currentchemical.name]
class benthic_omnivore:
	def __init__(self,constants,containingscenario,currentchemical,containingvolumeelement,comp_objects_dict):
		self.containingscenario=containingscenario
		self.currentchemical=currentchemical
		self.constants=constants
		self.containingvolumeelement=containingvolumeelement
		self.comp_objects_dict=comp_objects_dict
	@property
	def generaldegradationrate(self):
		cdict={}
		return cdict

	@property
	def chemical_generaldegradationrate(self):
		return self.generaldegradationrate[self.currentchemical.name]
	@property
	def initialconcentration_g_per_kg_usersupplied(self):
		cdict={}
		try:
			cdict["chem_divalent_mercury"]=0.0
		except:
			cdict["chem_divalent_mercury"]=nan
		
		try:
			cdict["chem_elemental_mercury"]=0.0
		except:
			cdict["chem_elemental_mercury"]=nan
		
		try:
			cdict["chem_methylmercury"]=0.0
		except:
			cdict["chem_methylmercury"]=nan
		
		return cdict

	@property
	def chemical_initialconcentration_g_per_kg_usersupplied(self):
		return self.initialconcentration_g_per_kg_usersupplied[self.currentchemical.name]
	@property
	def assimilationefficiencyfromfood(self):
		cdict={}
		try:
			cdict["chem_divalent_mercury"]=0.06
		except:
			cdict["chem_divalent_mercury"]=nan
		
		try:
			cdict["chem_elemental_mercury"]=0.06
		except:
			cdict["chem_elemental_mercury"]=nan
		
		try:
			cdict["chem_methylmercury"]=0.5
		except:
			cdict["chem_methylmercury"]=nan
		
		return cdict

	@property
	def chemical_assimilationefficiencyfromfood(self):
		return self.assimilationefficiencyfromfood[self.currentchemical.name]
	@property
	def acceptableabiotic(self):
		return ("abiotic | sediment | sediment - default")
	
	@property
	def foodingestionrate(self):
		return (self.feedingrate/self.bw)
	
	@property
	def reductionrate(self):
		cdict={}
		try:
			cdict["chem_divalent_mercury"]=0.0
		except:
			cdict["chem_divalent_mercury"]=nan
		
		return cdict

	@property
	def chemical_reductionrate(self):
		return self.reductionrate[self.currentchemical.name]
	_fishlipidfraction=0.07
	@property
	def fishlipidfraction(self):
		return self._fishlipidfraction
	@fishlipidfraction.setter
	def fishlipidfraction(self,value):
		self._fishlipidfraction=value

	@property
	def image(self):
		return ("c:\models\trim\data\images\catfish.gif")
	
	_bw=2.0
	@property
	def bw(self):
		return self._bw
	@bw.setter
	def bw(self,value):
		self._bw=value

	@property
	def halflife(self):
		cdict={}
		return cdict

	@property
	def chemical_halflife(self):
		return self.halflife[self.currentchemical.name]
	_fractiondietfishbenthiccarnivore=0.01
	@property
	def fractiondietfishbenthiccarnivore(self):
		return self._fractiondietfishbenthiccarnivore
	@fractiondietfishbenthiccarnivore.setter
	def fractiondietfishbenthiccarnivore(self,value):
		self._fractiondietfishbenthiccarnivore=value

	@property
	def feedingrate(self):
		return (0.022 * self.bw ** (0.85) * exp(0.06 * linkedCompartmentvalue(self.containingvolumeelement,self.comp_objects_dict,"surface_water","watertemperature_c")))
	
	@property
	def initialconcentration_g_per_kg(self):
		cdict={}
		try:
			cdict["chem_divalent_mercury"]=self.containingscenario.fractioninitialconcentrations * self.chemical_initialconcentration_g_per_kg_usersupplied
		except:
			cdict["chem_divalent_mercury"]=nan
		
		try:
			cdict["chem_elemental_mercury"]=self.containingscenario.fractioninitialconcentrations * self.chemical_initialconcentration_g_per_kg_usersupplied
		except:
			cdict["chem_elemental_mercury"]=nan
		
		try:
			cdict["chem_methylmercury"]=self.containingscenario.fractioninitialconcentrations * self.chemical_initialconcentration_g_per_kg_usersupplied
		except:
			cdict["chem_methylmercury"]=nan
		
		return cdict

	@property
	def chemical_initialconcentration_g_per_kg(self):
		return self.initialconcentration_g_per_kg[self.currentchemical.name]
	@property
	def isbiotic(self):
		return (True)
	
	@property
	def methylationrate(self):
		cdict={}
		try:
			cdict["chem_divalent_mercury"]=0.0
		except:
			cdict["chem_divalent_mercury"]=nan
		
		return cdict

	@property
	def chemical_methylationrate(self):
		return self.methylationrate[self.currentchemical.name]
	@property
	def gilleliminationrate(self):
		cdict={}
		return cdict

	@property
	def chemical_gilleliminationrate(self):
		return self.gilleliminationrate[self.currentchemical.name]
	@property
	def eliminationrateconstant(self):
		cdict={}
		try:
			cdict["chem_divalent_mercury"]=self.chemical_howmuchfasterhgeliminationisthanformhg * exp(0.066*linkedCompartmentvalue(self.containingvolumeelement,self.comp_objects_dict,"surface_water","watertemperature_c") - 0.20 * log(1000.0*self.bw) - 5.83)
		except:
			cdict["chem_divalent_mercury"]=nan
		
		try:
			cdict["chem_elemental_mercury"]=self.chemical_howmuchfasterhgeliminationisthanformhg * exp(0.066*linkedCompartmentvalue(self.containingvolumeelement,self.comp_objects_dict,"surface_water","watertemperature_c") - 0.20 * log(1000.0*self.bw) -5.83)
		except:
			cdict["chem_elemental_mercury"]=nan
		
		try:
			cdict["chem_methylmercury"]=self.chemical_howmuchfasterhgeliminationisthanformhg * exp(0.066*linkedCompartmentvalue(self.containingvolumeelement,self.comp_objects_dict,"surface_water","watertemperature_c") - 0.20 * log(1000.0*self.bw) -5.83)
		except:
			cdict["chem_methylmercury"]=nan
		
		return cdict

	@property
	def chemical_eliminationrateconstant(self):
		return self.eliminationrateconstant[self.currentchemical.name]
	@property
	def gamma_fish(self):
		cdict={}
		return cdict

	@property
	def chemical_gamma_fish(self):
		return self.gamma_fish[self.currentchemical.name]
	@property
	def absorptionrateconstant(self):
		cdict={}
		return cdict

	@property
	def chemical_absorptionrateconstant(self):
		return self.absorptionrateconstant[self.currentchemical.name]
	@property
	def category(self):
		return ("fish | benthic omnivore")
	
	_fractiondietfishomnivore=0.01
	@property
	def fractiondietfishomnivore(self):
		return self._fractiondietfishomnivore
	@fractiondietfishomnivore.setter
	def fractiondietfishomnivore(self,value):
		self._fractiondietfishomnivore=value

	@property
	def concentrationoutputunits(self):
		return ("mg/kg wet weight")
	
	@property
	def fishchemicaluptakerateviagill(self):
		cdict={}
		return cdict

	@property
	def chemical_fishchemicaluptakerateviagill(self):
		return self.fishchemicaluptakerateviagill[self.currentchemical.name]
	@property
	def numberoffishpersquaremeter(self):
		return (self.biomassperarea_kg_m2/self.bw)
	
	_biomassperarea_kg_m2=0.01
	@property
	def biomassperarea_kg_m2(self):
		return self._biomassperarea_kg_m2
	@biomassperarea_kg_m2.setter
	def biomassperarea_kg_m2(self,value):
		self._biomassperarea_kg_m2=value

	@property
	def howmuchfasterhgeliminationisthanformhg(self):
		cdict={}
		try:
			cdict["chem_divalent_mercury"]=3.0
		except:
			cdict["chem_divalent_mercury"]=nan
		
		try:
			cdict["chem_elemental_mercury"]=3.0
		except:
			cdict["chem_elemental_mercury"]=nan
		
		try:
			cdict["chem_methylmercury"]=1.0
		except:
			cdict["chem_methylmercury"]=nan
		
		return cdict

	@property
	def chemical_howmuchfasterhgeliminationisthanformhg(self):
		return self.howmuchfasterhgeliminationisthanformhg[self.currentchemical.name]
	_concentrationoutputfactor=1000.0
	@property
	def concentrationoutputfactor(self):
		return self._concentrationoutputfactor
	@concentrationoutputfactor.setter
	def concentrationoutputfactor(self,value):
		self._concentrationoutputfactor=value

	@property
	def oxidationrate(self):
		cdict={}
		try:
			cdict["chem_elemental_mercury"]=1000000.0
		except:
			cdict["chem_elemental_mercury"]=nan
		
		return cdict

	@property
	def chemical_oxidationrate(self):
		return self.oxidationrate[self.currentchemical.name]
	@property
	def demethylationrate(self):
		cdict={}
		try:
			cdict["chem_methylmercury"]=0.0
		except:
			cdict["chem_methylmercury"]=nan
		
		return cdict

	@property
	def chemical_demethylationrate(self):
		return self.demethylationrate[self.currentchemical.name]
	_fractiondietfishcarnivore=0.01
	@property
	def fractiondietfishcarnivore(self):
		return self._fractiondietfishcarnivore
	@fractiondietfishcarnivore.setter
	def fractiondietfishcarnivore(self,value):
		self._fractiondietfishcarnivore=value

	@property
	def chemicaltransferefficiencyinfish(self):
		cdict={}
		return cdict

	@property
	def chemical_chemicaltransferefficiencyinfish(self):
		return self.chemicaltransferefficiencyinfish[self.currentchemical.name]
	_fractiondietalgae=0.01
	@property
	def fractiondietalgae(self):
		return self._fractiondietalgae
	@fractiondietalgae.setter
	def fractiondietalgae(self,value):
		self._fractiondietalgae=value

	@property
	def populationsize(self):
		return (self.numberoffishpersquaremeter * self.containingvolumeelement.area)
	
	@property
	def totalmass(self):
		return (self.populationsize  * self.bw)
	
	_fractiondietbenthicinvertebrate=0.01
	@property
	def fractiondietbenthicinvertebrate(self):
		return self._fractiondietbenthicinvertebrate
	@fractiondietbenthicinvertebrate.setter
	def fractiondietbenthicinvertebrate(self,value):
		self._fractiondietbenthicinvertebrate=value

	_fractiondietfishherbivore=0.01
	@property
	def fractiondietfishherbivore(self):
		return self._fractiondietfishherbivore
	@fractiondietfishherbivore.setter
	def fractiondietfishherbivore(self,value):
		self._fractiondietfishherbivore=value

class degradation_reaction_sink:
	def __init__(self,constants,containingscenario,currentchemical,containingvolumeelement,comp_objects_dict):
		self.containingscenario=containingscenario
		self.currentchemical=currentchemical
		self.constants=constants
		self.containingvolumeelement=containingvolumeelement
		self.comp_objects_dict=comp_objects_dict
	@property
	def isbiotic(self):
		return (False)
	
	@property
	def category(self):
		return ("sink | degradation/reaction sink")
	
	@property
	def acceptableabiotic(self):
		return ("nan")
	
	_concentrationoutputfactor=1.0
	@property
	def concentrationoutputfactor(self):
		return self._concentrationoutputfactor
	@concentrationoutputfactor.setter
	def concentrationoutputfactor(self,value):
		self._concentrationoutputfactor=value

	@property
	def concentrationoutputunits(self):
		return ("0.01")
	
class flush_rate_sink:
	def __init__(self,constants,containingscenario,currentchemical,containingvolumeelement,comp_objects_dict):
		self.containingscenario=containingscenario
		self.currentchemical=currentchemical
		self.constants=constants
		self.containingvolumeelement=containingvolumeelement
		self.comp_objects_dict=comp_objects_dict
	@property
	def isbiotic(self):
		return (False)
	
	@property
	def category(self):
		return ("sink | abiotic | surface water | surface water - default")
	
	@property
	def acceptableabiotic(self):
		return ("abiotic | surface water | surface water - default")
	
	_concentrationoutputfactor=1.0
	@property
	def concentrationoutputfactor(self):
		return self._concentrationoutputfactor
	@concentrationoutputfactor.setter
	def concentrationoutputfactor(self,value):
		self._concentrationoutputfactor=value

	@property
	def concentrationoutputunits(self):
		return ("0.01")
	
class macrophyte:
	def __init__(self,constants,containingscenario,currentchemical,containingvolumeelement,comp_objects_dict):
		self.containingscenario=containingscenario
		self.currentchemical=currentchemical
		self.constants=constants
		self.containingvolumeelement=containingvolumeelement
		self.comp_objects_dict=comp_objects_dict
	@property
	def generaldegradationrate(self):
		cdict={}
		return cdict

	@property
	def chemical_generaldegradationrate(self):
		return self.generaldegradationrate[self.currentchemical.name]
	@property
	def initialconcentration_g_per_kg_usersupplied(self):
		cdict={}
		try:
			cdict["chem_divalent_mercury"]=0.0
		except:
			cdict["chem_divalent_mercury"]=nan
		
		try:
			cdict["chem_elemental_mercury"]=0.0
		except:
			cdict["chem_elemental_mercury"]=nan
		
		try:
			cdict["chem_methylmercury"]=0.0
		except:
			cdict["chem_methylmercury"]=nan
		
		return cdict

	@property
	def chemical_initialconcentration_g_per_kg_usersupplied(self):
		return self.initialconcentration_g_per_kg_usersupplied[self.currentchemical.name]
	@property
	def acceptableabiotic(self):
		return ("abiotic | surface water | surface water - default")
	
	@property
	def watercolumndissolvedpartitioning_alphaofequilibrium(self):
		cdict={}
		try:
			cdict["chem_divalent_mercury"]=0.95
		except:
			cdict["chem_divalent_mercury"]=nan
		
		try:
			cdict["chem_elemental_mercury"]=0.95
		except:
			cdict["chem_elemental_mercury"]=nan
		
		try:
			cdict["chem_methylmercury"]=0.95
		except:
			cdict["chem_methylmercury"]=nan
		
		return cdict

	@property
	def chemical_watercolumndissolvedpartitioning_alphaofequilibrium(self):
		return self.watercolumndissolvedpartitioning_alphaofequilibrium[self.currentchemical.name]
	@property
	def halflife(self):
		cdict={}
		return cdict

	@property
	def chemical_halflife(self):
		return self.halflife[self.currentchemical.name]
	@property
	def initialconcentration_g_per_kg(self):
		cdict={}
		try:
			cdict["chem_divalent_mercury"]=self.containingscenario.fractioninitialconcentrations * self.chemical_initialconcentration_g_per_kg_usersupplied
		except:
			cdict["chem_divalent_mercury"]=nan
		
		try:
			cdict["chem_elemental_mercury"]=self.containingscenario.fractioninitialconcentrations * self.chemical_initialconcentration_g_per_kg_usersupplied
		except:
			cdict["chem_elemental_mercury"]=nan
		
		try:
			cdict["chem_methylmercury"]=self.containingscenario.fractioninitialconcentrations * self.chemical_initialconcentration_g_per_kg_usersupplied
		except:
			cdict["chem_methylmercury"]=nan
		
		return cdict

	@property
	def chemical_initialconcentration_g_per_kg(self):
		return self.initialconcentration_g_per_kg[self.currentchemical.name]
	@property
	def isbiotic(self):
		return (True)
	
	@property
	def watercolumndissolvedpartitioning_timetoreachalphaofequilibrium(self):
		cdict={}
		try:
			cdict["chem_divalent_mercury"]=18.0
		except:
			cdict["chem_divalent_mercury"]=nan
		
		try:
			cdict["chem_elemental_mercury"]=18.0
		except:
			cdict["chem_elemental_mercury"]=nan
		
		try:
			cdict["chem_methylmercury"]=18.0
		except:
			cdict["chem_methylmercury"]=nan
		
		return cdict

	@property
	def chemical_watercolumndissolvedpartitioning_timetoreachalphaofequilibrium(self):
		return self.watercolumndissolvedpartitioning_timetoreachalphaofequilibrium[self.currentchemical.name]
	@property
	def watercolumndissolvedpartitioning_partitioncoefficient(self):
		cdict={}
		try:
			cdict["chem_divalent_mercury"]=0.883
		except:
			cdict["chem_divalent_mercury"]=nan
		
		try:
			cdict["chem_elemental_mercury"]=0.883
		except:
			cdict["chem_elemental_mercury"]=nan
		
		try:
			cdict["chem_methylmercury"]=4.4
		except:
			cdict["chem_methylmercury"]=nan
		
		return cdict

	@property
	def chemical_watercolumndissolvedpartitioning_partitioncoefficient(self):
		return self.watercolumndissolvedpartitioning_partitioncoefficient[self.currentchemical.name]
	@property
	def category(self):
		return ("aquatic plant | macrophyte")
	
	@property
	def bioaccumulationrate(self):
		cdict={}
		return cdict

	@property
	def chemical_bioaccumulationrate(self):
		return self.bioaccumulationrate[self.currentchemical.name]
	@property
	def concentrationoutputunits(self):
		return ("mg/kg wet weight")
	
	_density=1.0
	@property
	def density(self):
		return self._density
	@density.setter
	def density(self,value):
		self._density=value

	_biomassperarea_kg_m2=0.6
	@property
	def biomassperarea_kg_m2(self):
		return self._biomassperarea_kg_m2
	@biomassperarea_kg_m2.setter
	def biomassperarea_kg_m2(self,value):
		self._biomassperarea_kg_m2=value

	@property
	def abbreviation(self):
		cdict={}
		return cdict

	@property
	def chemical_abbreviation(self):
		return self.abbreviation[self.currentchemical.name]
	_concentrationoutputfactor=1000.0
	@property
	def concentrationoutputfactor(self):
		return self._concentrationoutputfactor
	@concentrationoutputfactor.setter
	def concentrationoutputfactor(self,value):
		self._concentrationoutputfactor=value

	@property
	def oxidationrate(self):
		cdict={}
		try:
			cdict["chem_elemental_mercury"]=1.0e9
		except:
			cdict["chem_elemental_mercury"]=nan
		
		return cdict

	@property
	def chemical_oxidationrate(self):
		return self.oxidationrate[self.currentchemical.name]
	@property
	def depurationrate(self):
		cdict={}
		return cdict

	@property
	def chemical_depurationrate(self):
		return self.depurationrate[self.currentchemical.name]
	@property
	def volume(self):
		return (self.totalmass / (self.density*1000))
	
	@property
	def totalmass(self):
		return (self.biomassperarea_kg_m2 * self.containingvolumeelement.area)
	
class sediment:
	def __init__(self,constants,containingscenario,currentchemical,containingvolumeelement,comp_objects_dict):
		self.containingscenario=containingscenario
		self.currentchemical=currentchemical
		self.constants=constants
		self.containingvolumeelement=containingvolumeelement
		self.comp_objects_dict=comp_objects_dict
	@property
	def generaldegradationrate(self):
		cdict={}
		return cdict

	@property
	def chemical_generaldegradationrate(self):
		return self.generaldegradationrate[self.currentchemical.name]
	@property
	def sedimentresuspensionrate_m3_m2_day(self):
		return (self.sedimentresuspensionrate_kg_m2_day / self.rho)
	
	@property
	def acceptableabiotic(self):
		return ("nan")
	
	@property
	def sedimentburialratetohavezeronetdeposition_m3_m2_day(self):
		return (0.01)
	
	@property
	def fractionmass_sorbed(self):
		cdict={}
		try:
			cdict["chem_divalent_mercury"]=self.containingvolumeelement.volume * self.volumefraction_solid * self.chemical_kd * self.rho * self.constants.m3_per_l  /self.chemical_genericdenominatorforcalculatingfractioninphases
		except:
			cdict["chem_divalent_mercury"]=nan
		
		try:
			cdict["chem_elemental_mercury"]=self.containingvolumeelement.volume * self.volumefraction_solid * self.chemical_kd * self.rho * self.constants.m3_per_l  /self.chemical_genericdenominatorforcalculatingfractioninphases
		except:
			cdict["chem_elemental_mercury"]=nan
		
		try:
			cdict["chem_methylmercury"]=self.containingvolumeelement.volume * self.volumefraction_solid * self.chemical_kd * self.rho * self.constants.m3_per_l  /self.chemical_genericdenominatorforcalculatingfractioninphases
		except:
			cdict["chem_methylmercury"]=nan
		
		return cdict

	@property
	def chemical_fractionmass_sorbed(self):
		return self.fractionmass_sorbed[self.currentchemical.name]
	@property
	def reductionrate(self):
		cdict={}
		try:
			cdict["chem_divalent_mercury"]=1.0e-6
		except:
			cdict["chem_divalent_mercury"]=nan
		
		return cdict

	@property
	def chemical_reductionrate(self):
		return self.reductionrate[self.currentchemical.name]
	_rho=2600.0
	@property
	def rho(self):
		return self._rho
	@rho.setter
	def rho(self,value):
		self._rho=value

	@property
	def halflife(self):
		cdict={}
		return cdict

	@property
	def chemical_halflife(self):
		return self.halflife[self.currentchemical.name]
	@property
	def initialconcentration_g_per_m3_usersupplied(self):
		cdict={}
		try:
			cdict["chem_divalent_mercury"]=0.0
		except:
			cdict["chem_divalent_mercury"]=nan
		
		try:
			cdict["chem_elemental_mercury"]=0.0
		except:
			cdict["chem_elemental_mercury"]=nan
		
		try:
			cdict["chem_methylmercury"]=0.0
		except:
			cdict["chem_methylmercury"]=nan
		
		return cdict

	@property
	def chemical_initialconcentration_g_per_m3_usersupplied(self):
		return self.initialconcentration_g_per_m3_usersupplied[self.currentchemical.name]
	_sedimentresuspensionvelocity=9.64763202734353e-05
	@property
	def sedimentresuspensionvelocity(self):
		return self._sedimentresuspensionvelocity
	@sedimentresuspensionvelocity.setter
	def sedimentresuspensionvelocity(self,value):
		self._sedimentresuspensionvelocity=value

	@property
	def volumefraction_solid(self):
		return (1 - self.volumefraction_liquid)
	
	@property
	def isbiotic(self):
		return (False)
	
	@property
	def wetconcoutputfactor(self):
		return ((self.volumefraction_solid * self.rho) / (self.volumefraction_solid * self.rho + self.volumefraction_liquid * self.constants.kg_per_m3_water))
	
	@property
	def benthic_solids_concentration(self):
		return (self.rho * (1 - self.porosity))
	
	@property
	def methylationrate(self):
		cdict={}
		try:
			cdict["chem_divalent_mercury"]=1.0e-4
		except:
			cdict["chem_divalent_mercury"]=nan
		
		return cdict

	@property
	def chemical_methylationrate(self):
		return self.methylationrate[self.currentchemical.name]
	@property
	def genericdenominatorforcalculatingfractioninphases(self):
		cdict={}
		try:
			cdict["chem_divalent_mercury"]=self.containingvolumeelement.volume * self.volumefraction_solid * self.chemical_kd * self.rho * self.constants.m3_per_l + self.containingvolumeelement.volume * self.volumefraction_liquid
		except:
			cdict["chem_divalent_mercury"]=nan
		
		try:
			cdict["chem_elemental_mercury"]=self.containingvolumeelement.volume * self.volumefraction_solid * self.chemical_kd * self.rho * self.constants.m3_per_l + self.containingvolumeelement.volume * self.volumefraction_liquid
		except:
			cdict["chem_elemental_mercury"]=nan
		
		try:
			cdict["chem_methylmercury"]=self.containingvolumeelement.volume * self.volumefraction_solid * self.chemical_kd * self.rho * self.constants.m3_per_l + self.containingvolumeelement.volume * self.volumefraction_liquid
		except:
			cdict["chem_methylmercury"]=nan
		
		return cdict

	@property
	def chemical_genericdenominatorforcalculatingfractioninphases(self):
		return self.genericdenominatorforcalculatingfractioninphases[self.currentchemical.name]
	_porosity=0.6
	@property
	def porosity(self):
		return self._porosity
	@porosity.setter
	def porosity(self,value):
		self._porosity=value

	@property
	def boundarylayerthicknessbelowwater(self):
		cdict={}
		try:
			cdict["chem_divalent_mercury"]=318 * self.chemical_d_effective ** (0.683)
		except:
			cdict["chem_divalent_mercury"]=nan
		
		try:
			cdict["chem_elemental_mercury"]=318 * self.chemical_d_effective ** (0.683)
		except:
			cdict["chem_elemental_mercury"]=nan
		
		try:
			cdict["chem_methylmercury"]=318 * self.chemical_d_effective ** (0.683)
		except:
			cdict["chem_methylmercury"]=nan
		
		return cdict

	@property
	def chemical_boundarylayerthicknessbelowwater(self):
		return self.boundarylayerthicknessbelowwater[self.currentchemical.name]
	@property
	def z_liquid(self):
		cdict={}
		try:
			cdict["chem_divalent_mercury"]=self.currentchemical.z_purewater
		except:
			cdict["chem_divalent_mercury"]=nan
		
		try:
			cdict["chem_elemental_mercury"]=self.currentchemical.z_purewater
		except:
			cdict["chem_elemental_mercury"]=nan
		
		try:
			cdict["chem_methylmercury"]=self.currentchemical.z_purewater
		except:
			cdict["chem_methylmercury"]=nan
		
		return cdict

	@property
	def chemical_z_liquid(self):
		return self.z_liquid[self.currentchemical.name]
	_organiccarboncontent=0.01
	@property
	def organiccarboncontent(self):
		return self._organiccarboncontent
	@organiccarboncontent.setter
	def organiccarboncontent(self,value):
		self._organiccarboncontent=value

	@property
	def category(self):
		return ("abiotic | sediment | sediment - default")
	
	@property
	def wetconcoutputunits(self):
		return ("ug/g wet weight")
	
	@property
	def sedimentresuspensionrate_kg_m2_day(self):
		return (self.sedimentresuspensionvelocity*self.benthic_solids_concentration)
	
	@property
	def z_solid(self):
		cdict={}
		try:
			cdict["chem_divalent_mercury"]=self.chemical_kd * (self.rho / 1000) * self.currentchemical.z_purewater
		except:
			cdict["chem_divalent_mercury"]=nan
		
		try:
			cdict["chem_elemental_mercury"]=self.chemical_kd * (self.rho / 1000) * self.currentchemical.z_purewater
		except:
			cdict["chem_elemental_mercury"]=nan
		
		try:
			cdict["chem_methylmercury"]=self.chemical_kd * (self.rho / 1000) * self.currentchemical.z_purewater
		except:
			cdict["chem_methylmercury"]=nan
		
		return cdict

	@property
	def chemical_z_solid(self):
		return self.z_solid[self.currentchemical.name]
	@property
	def z_total(self):
		cdict={}
		try:
			cdict["chem_divalent_mercury"]=self.chemical_z_liquid * self.porosity + self.chemical_z_solid * (1 - self.porosity)
		except:
			cdict["chem_divalent_mercury"]=nan
		
		try:
			cdict["chem_elemental_mercury"]=self.chemical_z_liquid * self.porosity + self.chemical_z_solid * (1 - self.porosity)
		except:
			cdict["chem_elemental_mercury"]=nan
		
		try:
			cdict["chem_methylmercury"]=self.chemical_z_liquid * self.porosity + self.chemical_z_solid * (1 - self.porosity)
		except:
			cdict["chem_methylmercury"]=nan
		
		return cdict

	@property
	def chemical_z_total(self):
		return self.z_total[self.currentchemical.name]
	@property
	def concentrationoutputunits(self):
		return ("ug/g dry weight")
	
	@property
	def d_effective(self):
		cdict={}
		try:
			cdict["chem_divalent_mercury"]=self.porosity ** (4 / 3) * self.currentchemical.d_purewater
		except:
			cdict["chem_divalent_mercury"]=nan
		
		try:
			cdict["chem_elemental_mercury"]=self.porosity ** (4 / 3) * self.currentchemical.d_purewater
		except:
			cdict["chem_elemental_mercury"]=nan
		
		try:
			cdict["chem_methylmercury"]=self.porosity ** (4 / 3) * self.currentchemical.d_purewater
		except:
			cdict["chem_methylmercury"]=nan
		
		return cdict

	@property
	def chemical_d_effective(self):
		return self.d_effective[self.currentchemical.name]
	@property
	def depth(self):
		return (self.containingvolumeelement.height)
	
	@property
	def kd(self):
		cdict={}
		try:
			cdict["chem_divalent_mercury"]=50000.0
		except:
			cdict["chem_divalent_mercury"]=nan
		
		try:
			cdict["chem_elemental_mercury"]=3000.0
		except:
			cdict["chem_elemental_mercury"]=nan
		
		try:
			cdict["chem_methylmercury"]=3000.0
		except:
			cdict["chem_methylmercury"]=nan
		
		return cdict

	@property
	def chemical_kd(self):
		return self.kd[self.currentchemical.name]
	@property
	def area(self):
		return (self.containingvolumeelement.area)
	
	@property
	def initialconcentration_g_per_m3(self):
		cdict={}
		try:
			cdict["chem_divalent_mercury"]=self.containingscenario.fractioninitialconcentrations * self.chemical_initialconcentration_g_per_m3_usersupplied
		except:
			cdict["chem_divalent_mercury"]=nan
		
		try:
			cdict["chem_elemental_mercury"]=self.containingscenario.fractioninitialconcentrations * self.chemical_initialconcentration_g_per_m3_usersupplied
		except:
			cdict["chem_elemental_mercury"]=nan
		
		try:
			cdict["chem_methylmercury"]=self.containingscenario.fractioninitialconcentrations * self.chemical_initialconcentration_g_per_m3_usersupplied
		except:
			cdict["chem_methylmercury"]=nan
		
		return cdict

	@property
	def chemical_initialconcentration_g_per_m3(self):
		return self.initialconcentration_g_per_m3[self.currentchemical.name]
	_ph=0.01
	@property
	def ph(self):
		return self._ph
	@ph.setter
	def ph(self,value):
		self._ph=value

	_fractionsand=0.25
	@property
	def fractionsand(self):
		return self._fractionsand
	@fractionsand.setter
	def fractionsand(self,value):
		self._fractionsand=value

	@property
	def concentrationoutputfactor(self):
		return (1000/(self.volumefraction_solid * self.rho))
	
	@property
	def oxidationrate(self):
		cdict={}
		try:
			cdict["chem_elemental_mercury"]=0.0
		except:
			cdict["chem_elemental_mercury"]=nan
		
		return cdict

	@property
	def chemical_oxidationrate(self):
		return self.oxidationrate[self.currentchemical.name]
	@property
	def demethylationrate(self):
		cdict={}
		try:
			cdict["chem_methylmercury"]=0.0501
		except:
			cdict["chem_methylmercury"]=nan
		
		return cdict

	@property
	def chemical_demethylationrate(self):
		return self.demethylationrate[self.currentchemical.name]
	@property
	def fractionmass_dissolved(self):
		cdict={}
		try:
			cdict["chem_divalent_mercury"]=self.containingvolumeelement.volume * self.volumefraction_liquid /self.chemical_genericdenominatorforcalculatingfractioninphases
		except:
			cdict["chem_divalent_mercury"]=nan
		
		try:
			cdict["chem_elemental_mercury"]=self.containingvolumeelement.volume * self.volumefraction_liquid /self.chemical_genericdenominatorforcalculatingfractioninphases
		except:
			cdict["chem_elemental_mercury"]=nan
		
		try:
			cdict["chem_methylmercury"]=self.containingvolumeelement.volume * self.volumefraction_liquid /self.chemical_genericdenominatorforcalculatingfractioninphases
		except:
			cdict["chem_methylmercury"]=nan
		
		return cdict

	@property
	def chemical_fractionmass_dissolved(self):
		return self.fractionmass_dissolved[self.currentchemical.name]
	@property
	def height(self):
		return (self.containingvolumeelement.height)
	
	@property
	def volume(self):
		return (self.containingvolumeelement.volume)
	
	@property
	def volumefraction_liquid(self):
		return (self.porosity)
	
	@property
	def totalmass(self):
		return (self.containingvolumeelement.volume*(self.volumefraction_solid*self.rho + self.volumefraction_liquid*self.constants.kg_per_m3_water))
	
class sediment_burial_sink:
	def __init__(self,constants,containingscenario,currentchemical,containingvolumeelement,comp_objects_dict):
		self.containingscenario=containingscenario
		self.currentchemical=currentchemical
		self.constants=constants
		self.containingvolumeelement=containingvolumeelement
		self.comp_objects_dict=comp_objects_dict
	@property
	def isbiotic(self):
		return (False)
	
	@property
	def category(self):
		return ("sink | abiotic | sediment | sediment - default")
	
	@property
	def acceptableabiotic(self):
		return ("nan")
	
	_concentrationoutputfactor=1.0
	@property
	def concentrationoutputfactor(self):
		return self._concentrationoutputfactor
	@concentrationoutputfactor.setter
	def concentrationoutputfactor(self,value):
		self._concentrationoutputfactor=value

	@property
	def concentrationoutputunits(self):
		return ("0.01")
	
class surface_water:
	def __init__(self,constants,containingscenario,currentchemical,containingvolumeelement,comp_objects_dict):
		self.containingscenario=containingscenario
		self.currentchemical=currentchemical
		self.constants=constants
		self.containingvolumeelement=containingvolumeelement
		self.comp_objects_dict=comp_objects_dict
	@property
	def generaldegradationrate(self):
		cdict={}
		return cdict

	@property
	def chemical_generaldegradationrate(self):
		return self.generaldegradationrate[self.currentchemical.name]
	_algaedensity_g_m3=1000000.0
	@property
	def algaedensity_g_m3(self):
		return self._algaedensity_g_m3
	@algaedensity_g_m3.setter
	def algaedensity_g_m3(self,value):
		self._algaedensity_g_m3=value

	@property
	def waterschmidtnumber(self):
		cdict={}
		try:
			cdict["chem_divalent_mercury"]=self.waterviscosity/(self.waterdensity * self.currentchemical.d_purewater_m2_per_s)
		except:
			cdict["chem_divalent_mercury"]=nan
		
		try:
			cdict["chem_elemental_mercury"]=self.waterviscosity/(self.waterdensity * self.currentchemical.d_purewater_m2_per_s)
		except:
			cdict["chem_elemental_mercury"]=nan
		
		try:
			cdict["chem_methylmercury"]=self.waterviscosity/(self.waterdensity * self.currentchemical.d_purewater_m2_per_s)
		except:
			cdict["chem_methylmercury"]=nan
		
		return cdict

	@property
	def chemical_waterschmidtnumber(self):
		return self.waterschmidtnumber[self.currentchemical.name]
	_boundarylayerthicknessabovesediment=0.02
	@property
	def boundarylayerthicknessabovesediment(self):
		return self._boundarylayerthicknessabovesediment
	@boundarylayerthicknessabovesediment.setter
	def boundarylayerthicknessabovesediment(self,value):
		self._boundarylayerthicknessabovesediment=value

	_algaewatercontent=0.9
	@property
	def algaewatercontent(self):
		return self._algaewatercontent
	@algaewatercontent.setter
	def algaewatercontent(self,value):
		self._algaewatercontent=value

	@property
	def reductionrate(self):
		cdict={}
		try:
			cdict["chem_divalent_mercury"]=0.0075
		except:
			cdict["chem_divalent_mercury"]=nan
		
		return cdict

	@property
	def chemical_reductionrate(self):
		return self.reductionrate[self.currentchemical.name]
	@property
	def halflife(self):
		cdict={}
		return cdict

	@property
	def chemical_halflife(self):
		return self.halflife[self.currentchemical.name]
	_algaecarboncontentdrywt=0.465
	@property
	def algaecarboncontentdrywt(self):
		return self._algaecarboncontentdrywt
	@algaecarboncontentdrywt.setter
	def algaecarboncontentdrywt(self,value):
		self._algaecarboncontentdrywt=value

	@property
	def isbiotic(self):
		return (False)
	
	@property
	def d_owforhg2_ph4(self):
		cdict={}
		try:
			cdict["chem_divalent_mercury"]=0.875 if self.chlorideconcentration_mg_l<= 0.112111281202651 else 0.925 if self.chlorideconcentration_mg_l<= 0.141139740854819 else 1.075 if self.chlorideconcentration_mg_l<= 0.177684406376176 else 1.225 if self.chlorideconcentration_mg_l<= 0.223691414466529 else 1.275 if self.chlorideconcentration_mg_l<= 0.281610806072095 else 1.4 if self.chlorideconcentration_mg_l<= 0.354527 else 1.45 if self.chlorideconcentration_mg_l<= 0.44632304946715 else 1.475 if self.chlorideconcentration_mg_l<= 0.561887428843661 else 1.5 if self.chlorideconcentration_mg_l<= 0.707374362738971 else 1.525 if self.chlorideconcentration_mg_l<= 0.890531560903796 else 1.55 if self.chlorideconcentration_mg_l<= 1.12111281202651 else 1.575 if self.chlorideconcentration_mg_l<= 1.41139740854819 else 1.625 if self.chlorideconcentration_mg_l<= 1.77684406376176 else 1.625 if self.chlorideconcentration_mg_l<= 2.23691414466529 else 1.625 if self.chlorideconcentration_mg_l<= 2.81610806072095 else 1.625 if self.chlorideconcentration_mg_l<= 3.54526999999991 else 1.625 if self.chlorideconcentration_mg_l<= 4.4632304946714 else 1.625 if self.chlorideconcentration_mg_l<= 5.61887428843648 else 1.625 if self.chlorideconcentration_mg_l<= 7.07374362738955 else 1.625 if self.chlorideconcentration_mg_l<= 8.90531560903775 else 1.625 if self.chlorideconcentration_mg_l<= 11.2111281202649 else 1.625 if self.chlorideconcentration_mg_l<= 14.1139740854816 else 1.625 if self.chlorideconcentration_mg_l<= 17.7684406376172 else 1.625 if self.chlorideconcentration_mg_l<= 22.3691414466524 else 1.625 if self.chlorideconcentration_mg_l<= 28.1610806072089 else 1.625 if self.chlorideconcentration_mg_l<= 35.4526999999992 else 1.625 if self.chlorideconcentration_mg_l<= 44.632304946714 else 1.625 if self.chlorideconcentration_mg_l<= 56.1887428843648 else 1.625 if self.chlorideconcentration_mg_l<= 70.7374362738956 else 1.6 if self.chlorideconcentration_mg_l<= 89.0531560903776 else 1.6 if self.chlorideconcentration_mg_l<= 112.111281202649 else 1.6 if self.chlorideconcentration_mg_l<= 141.139740854816 else 1.575 if self.chlorideconcentration_mg_l<= 177.684406376172 else 1.575 if self.chlorideconcentration_mg_l<= 223.691414466524 else 1.55 if self.chlorideconcentration_mg_l<= 281.610806072089 else 1.525 if self.chlorideconcentration_mg_l<= 354.526999999992 else 1.475 if self.chlorideconcentration_mg_l<= 446.32304946714 else 1.375 if self.chlorideconcentration_mg_l<= 561.887428843648 else 1.3 if self.chlorideconcentration_mg_l<= 707.374362738955 else 1.2 if self.chlorideconcentration_mg_l<= 890.531560903776 else 1.15 if self.chlorideconcentration_mg_l<= 1121.11281202649 else 1.025 if self.chlorideconcentration_mg_l<= 1411.39740854816 else 0.95 if self.chlorideconcentration_mg_l<= 1776.84406376172 else 0.85 if self.chlorideconcentration_mg_l<= 2236.91414466519 else 0.8 if self.chlorideconcentration_mg_l<= 2816.10806072082 else 0.7 if self.chlorideconcentration_mg_l<= 3545.26999999984 else 0.6 if self.chlorideconcentration_mg_l<= 4463.2304946713 else 0.525 if self.chlorideconcentration_mg_l<= 5618.87428843635 else 0.425 if self.chlorideconcentration_mg_l<= 7073.74362738939 else 0.325 if self.chlorideconcentration_mg_l<= 8905.31560903756 else 0.25 if self.chlorideconcentration_mg_l<= 11211.1281202646 else 0.175 if self.chlorideconcentration_mg_l<= 14113.9740854813 else 0.1
		except:
			cdict["chem_divalent_mercury"]=nan
		
		return cdict

	@property
	def chemical_d_owforhg2_ph4(self):
		return self.d_owforhg2_ph4[self.currentchemical.name]
	@property
	def z_liquid(self):
		cdict={}
		try:
			cdict["chem_divalent_mercury"]=self.currentchemical.z_purewater
		except:
			cdict["chem_divalent_mercury"]=nan
		
		try:
			cdict["chem_elemental_mercury"]=self.currentchemical.z_purewater
		except:
			cdict["chem_elemental_mercury"]=nan
		
		try:
			cdict["chem_methylmercury"]=self.currentchemical.z_purewater
		except:
			cdict["chem_methylmercury"]=nan
		
		return cdict

	@property
	def chemical_z_liquid(self):
		return self.z_liquid[self.currentchemical.name]
	_watertemperature_k=0.01
	@property
	def watertemperature_k(self):
		return self._watertemperature_k
	@watertemperature_k.setter
	def watertemperature_k(self,value):
		self._watertemperature_k=value

	@property
	def category(self):
		return ("abiotic | surface water | surface water - default")
	
	_currentvelocity=0.01
	@property
	def currentvelocity(self):
		return self._currentvelocity
	@currentvelocity.setter
	def currentvelocity(self,value):
		self._currentvelocity=value

	@property
	def d_effective(self):
		cdict={}
		try:
			cdict["chem_divalent_mercury"]=self.currentchemical.d_purewater
		except:
			cdict["chem_divalent_mercury"]=nan
		
		try:
			cdict["chem_elemental_mercury"]=self.currentchemical.d_purewater
		except:
			cdict["chem_elemental_mercury"]=nan
		
		try:
			cdict["chem_methylmercury"]=self.currentchemical.d_purewater
		except:
			cdict["chem_methylmercury"]=nan
		
		return cdict

	@property
	def chemical_d_effective(self):
		return self.d_effective[self.currentchemical.name]
	@property
	def depth(self):
		return (self.containingvolumeelement.height)
	
	@property
	def fractionmass_algae(self):
		cdict={}
		try:
			cdict["chem_divalent_mercury"]=self.containingvolumeelement.volume * (self.volumefraction_algae) * self.chemical_ratioofconcinalgaetoconcdissolvedinwater * self.algaedensity_g_m3 * (self.constants.m3_per_l) / self.chemical_genericdenominatorforcalculatingfractioninphases
		except:
			cdict["chem_divalent_mercury"]=nan
		
		try:
			cdict["chem_elemental_mercury"]=self.containingvolumeelement.volume * (self.volumefraction_algae) * self.chemical_ratioofconcinalgaetoconcdissolvedinwater * self.algaedensity_g_m3 * (self.constants.m3_per_l) / self.chemical_genericdenominatorforcalculatingfractioninphases
		except:
			cdict["chem_elemental_mercury"]=nan
		
		try:
			cdict["chem_methylmercury"]=self.containingvolumeelement.volume * (self.volumefraction_algae) * self.chemical_ratioofconcinalgaetoconcdissolvedinwater * self.algaedensity_g_m3 * (self.constants.m3_per_l) / self.chemical_genericdenominatorforcalculatingfractioninphases
		except:
			cdict["chem_methylmercury"]=nan
		
		return cdict

	@property
	def chemical_fractionmass_algae(self):
		return self.fractionmass_algae[self.currentchemical.name]
	@property
	def oxidationrate(self):
		cdict={}
		try:
			cdict["chem_elemental_mercury"]=0.0
		except:
			cdict["chem_elemental_mercury"]=nan
		
		return cdict

	@property
	def chemical_oxidationrate(self):
		return self.oxidationrate[self.currentchemical.name]
	@property
	def demethylationrate(self):
		cdict={}
		try:
			cdict["chem_methylmercury"]=0.013
		except:
			cdict["chem_methylmercury"]=nan
		
		return cdict

	@property
	def chemical_demethylationrate(self):
		return self.demethylationrate[self.currentchemical.name]
	@property
	def volumefraction_liquid(self):
		return (1 - self.volumefraction_solid - self.volumefraction_algae)
	
	@property
	def shearvelocity_m_per_day(self):
		return (self.shearvelocity*86400)
	
	@property
	def shearvelocity(self):
		return (sqrt(self.dragcoefficient) * self.containingscenario.horizontalwindspeed)
	
	@property
	def acceptableabiotic(self):
		return ("nan")
	
	@property
	def d_owforhg2_ph7(self):
		cdict={}
		try:
			cdict["chem_divalent_mercury"]=0.025 if self.chlorideconcentration_mg_l<= 1.77684406376176 else 0.025 if self.chlorideconcentration_mg_l<= 2.23691414466529 else 0.025 if self.chlorideconcentration_mg_l<= 2.81610806072095 else 0.025 if self.chlorideconcentration_mg_l<= 3.54526999999991 else 0.025 if self.chlorideconcentration_mg_l<= 4.4632304946714 else 0.05 if self.chlorideconcentration_mg_l<= 5.61887428843648 else 0.075 if self.chlorideconcentration_mg_l<= 7.07374362738955 else 0.075 if self.chlorideconcentration_mg_l<= 8.90531560903775 else 0.075 if self.chlorideconcentration_mg_l<= 11.2111281202649 else 0.075 if self.chlorideconcentration_mg_l<= 14.1139740854816 else 0.1 if self.chlorideconcentration_mg_l<= 17.7684406376172 else 0.125 if self.chlorideconcentration_mg_l<= 22.3691414466524 else 0.175 if self.chlorideconcentration_mg_l<= 28.1610806072089 else 0.2 if self.chlorideconcentration_mg_l<= 35.4526999999992 else 0.325 if self.chlorideconcentration_mg_l<= 44.632304946714 else 0.45 if self.chlorideconcentration_mg_l<= 56.1887428843648 else 0.575 if self.chlorideconcentration_mg_l<= 70.7374362738956 else 0.7 if self.chlorideconcentration_mg_l<= 89.0531560903776 else 0.85 if self.chlorideconcentration_mg_l<= 112.111281202649 else 0.95 if self.chlorideconcentration_mg_l<= 141.139740854816 else 1.1 if self.chlorideconcentration_mg_l<= 177.684406376172 else 1.175 if self.chlorideconcentration_mg_l<= 223.691414466524 else 1.25 if self.chlorideconcentration_mg_l<= 281.610806072089 else 1.325 if self.chlorideconcentration_mg_l<= 354.526999999992 else 1.3 if self.chlorideconcentration_mg_l<= 446.32304946714 else 1.275 if self.chlorideconcentration_mg_l<= 561.887428843648 else 1.225 if self.chlorideconcentration_mg_l<= 707.374362738955 else 1.2 if self.chlorideconcentration_mg_l<= 890.531560903776 else 1.15 if self.chlorideconcentration_mg_l<= 1121.11281202649 else 1.1 if self.chlorideconcentration_mg_l<= 1411.39740854816 else 1.075 if self.chlorideconcentration_mg_l<= 1776.84406376172 else 0.95 if self.chlorideconcentration_mg_l<= 2236.91414466519 else 0.8 if self.chlorideconcentration_mg_l<= 2816.10806072082 else 0.7 if self.chlorideconcentration_mg_l<= 3545.26999999984 else 0.6 if self.chlorideconcentration_mg_l<= 4463.2304946713 else 0.525 if self.chlorideconcentration_mg_l<= 5618.87428843635 else 0.425 if self.chlorideconcentration_mg_l<= 7073.74362738939 else 0.325 if self.chlorideconcentration_mg_l<= 8905.31560903756 else 0.25 if self.chlorideconcentration_mg_l<= 11211.1281202646 else 0.175 if self.chlorideconcentration_mg_l<= 14113.9740854813 else 0.1
		except:
			cdict["chem_divalent_mercury"]=nan
		
		return cdict

	@property
	def chemical_d_owforhg2_ph7(self):
		return self.d_owforhg2_ph7[self.currentchemical.name]
	@property
	def d_owforhg2_ph5(self):
		cdict={}
		try:
			cdict["chem_divalent_mercury"]=0.075 if self.chlorideconcentration_mg_l<= 0.112111281202651 else 0.075 if self.chlorideconcentration_mg_l<= 0.141139740854819 else 0.075 if self.chlorideconcentration_mg_l<= 0.177684406376176 else 0.125 if self.chlorideconcentration_mg_l<= 0.223691414466529 else 0.175 if self.chlorideconcentration_mg_l<= 0.281610806072095 else 0.2 if self.chlorideconcentration_mg_l<= 0.354527 else 0.325 if self.chlorideconcentration_mg_l<= 0.44632304946715 else 0.45 if self.chlorideconcentration_mg_l<= 0.561887428843661 else 0.575 if self.chlorideconcentration_mg_l<= 0.707374362738971 else 0.725 if self.chlorideconcentration_mg_l<= 0.890531560903796 else 0.85 if self.chlorideconcentration_mg_l<= 1.12111281202651 else 0.975 if self.chlorideconcentration_mg_l<= 1.41139740854819 else 1.125 if self.chlorideconcentration_mg_l<= 1.77684406376176 else 1.225 if self.chlorideconcentration_mg_l<= 2.23691414466529 else 1.325 if self.chlorideconcentration_mg_l<= 2.81610806072095 else 1.425 if self.chlorideconcentration_mg_l<= 3.54526999999991 else 1.475 if self.chlorideconcentration_mg_l<= 4.4632304946714 else 1.5 if self.chlorideconcentration_mg_l<= 5.61887428843648 else 1.525 if self.chlorideconcentration_mg_l<= 7.07374362738955 else 1.55 if self.chlorideconcentration_mg_l<= 8.90531560903775 else 1.575 if self.chlorideconcentration_mg_l<= 11.2111281202649 else 1.6 if self.chlorideconcentration_mg_l<= 14.1139740854816 else 1.625 if self.chlorideconcentration_mg_l<= 17.7684406376172 else 1.625 if self.chlorideconcentration_mg_l<= 22.3691414466524 else 1.625 if self.chlorideconcentration_mg_l<= 28.1610806072089 else 1.625 if self.chlorideconcentration_mg_l<= 35.4526999999992 else 1.625 if self.chlorideconcentration_mg_l<= 44.632304946714 else 1.625 if self.chlorideconcentration_mg_l<= 56.1887428843648 else 1.625 if self.chlorideconcentration_mg_l<= 70.7374362738956 else 1.6 if self.chlorideconcentration_mg_l<= 89.0531560903776 else 1.6 if self.chlorideconcentration_mg_l<= 112.111281202649 else 1.6 if self.chlorideconcentration_mg_l<= 141.139740854816 else 1.575 if self.chlorideconcentration_mg_l<= 177.684406376172 else 1.575 if self.chlorideconcentration_mg_l<= 223.691414466524 else 1.55 if self.chlorideconcentration_mg_l<= 281.610806072089 else 1.525 if self.chlorideconcentration_mg_l<= 354.526999999992 else 1.475 if self.chlorideconcentration_mg_l<= 446.32304946714 else 1.425 if self.chlorideconcentration_mg_l<= 561.887428843648 else 1.35 if self.chlorideconcentration_mg_l<= 707.374362738955 else 1.275 if self.chlorideconcentration_mg_l<= 890.531560903776 else 1.225 if self.chlorideconcentration_mg_l<= 1121.11281202649 else 1.15 if self.chlorideconcentration_mg_l<= 1411.39740854816 else 1.1 if self.chlorideconcentration_mg_l<= 1776.84406376172 else 0.95 if self.chlorideconcentration_mg_l<= 2236.91414466519 else 0.8 if self.chlorideconcentration_mg_l<= 2816.10806072082 else 0.7 if self.chlorideconcentration_mg_l<= 3545.26999999984 else 0.6 if self.chlorideconcentration_mg_l<= 4463.2304946713 else 0.525 if self.chlorideconcentration_mg_l<= 5618.87428843635 else 0.425 if self.chlorideconcentration_mg_l<= 7073.74362738939 else 0.325 if self.chlorideconcentration_mg_l<= 8905.31560903756 else 0.25 if self.chlorideconcentration_mg_l<= 11211.1281202646 else 0.175 if self.chlorideconcentration_mg_l<= 14113.9740854813 else 0.1
		except:
			cdict["chem_divalent_mercury"]=nan
		
		return cdict

	@property
	def chemical_d_owforhg2_ph5(self):
		return self.d_owforhg2_ph5[self.currentchemical.name]
	@property
	def z_algae(self):
		cdict={}
		try:
			cdict["chem_divalent_mercury"]=(self.chemical_ratioofconcinalgaetoconcdissolvedinwater*self.algaedensity_g_m3/1000.0)*self.currentchemical.z_purewater
		except:
			cdict["chem_divalent_mercury"]=nan
		
		try:
			cdict["chem_elemental_mercury"]=(self.chemical_ratioofconcinalgaetoconcdissolvedinwater*self.algaedensity_g_m3/1000.0)*self.currentchemical.z_purewater
		except:
			cdict["chem_elemental_mercury"]=nan
		
		try:
			cdict["chem_methylmercury"]=(self.chemical_ratioofconcinalgaetoconcdissolvedinwater*self.algaedensity_g_m3/1000.0)*self.currentchemical.z_purewater
		except:
			cdict["chem_methylmercury"]=nan
		
		return cdict

	@property
	def chemical_z_algae(self):
		return self.z_algae[self.currentchemical.name]
	_dragcoefficient=0.0011
	@property
	def dragcoefficient(self):
		return self._dragcoefficient
	@dragcoefficient.setter
	def dragcoefficient(self,value):
		self._dragcoefficient=value

	_sedimentdepositionvelocity=2.0
	@property
	def sedimentdepositionvelocity(self):
		return self._sedimentdepositionvelocity
	@sedimentdepositionvelocity.setter
	def sedimentdepositionvelocity(self,value):
		self._sedimentdepositionvelocity=value

	@property
	def volumefraction_solid(self):
		return (self.suspendedsedimentconcentration / self.rho)
	
	@property
	def d_ow(self):
		cdict={}
		try:
			cdict["chem_divalent_mercury"]=self.chemical_d_owforhg2_ph4 if self.ph <=4 else self.chemical_d_owforhg2_ph5 if self.ph <=5 else self.chemical_d_owforhg2_ph6 if self.ph <=6 else self.chemical_d_owforhg2_ph7 if self.ph <=7 else self.chemical_d_owforhg2_ph8
		except:
			cdict["chem_divalent_mercury"]=nan
		
		try:
			cdict["chem_elemental_mercury"]=0.0
		except:
			cdict["chem_elemental_mercury"]=nan
		
		try:
			cdict["chem_methylmercury"]=self.chemical_d_owformhg_ph4 if self.ph <=4 else self.chemical_d_owformhg_ph5 if self.ph <=5 else self.chemical_d_owformhg_ph6 if self.ph <=6 else self.chemical_d_owformhg_ph7 if self.ph <=7 else self.chemical_d_owformhg_ph8
		except:
			cdict["chem_methylmercury"]=nan
		
		return cdict

	@property
	def chemical_d_ow(self):
		return self.d_ow[self.currentchemical.name]
	@property
	def waterviscosity(self):
		return (10**(-3.30233 + 1301 / (998.333 + 8.1855 * (self.watertemperature_c -20) + 0.00585 * (self.watertemperature_c - 20)**2.0)))
	
	@property
	def methylationrate(self):
		cdict={}
		try:
			cdict["chem_divalent_mercury"]=0.001
		except:
			cdict["chem_divalent_mercury"]=nan
		
		return cdict

	@property
	def chemical_methylationrate(self):
		return self.methylationrate[self.currentchemical.name]
	_algaegrowthrate=0.7
	@property
	def algaegrowthrate(self):
		return self._algaegrowthrate
	@algaegrowthrate.setter
	def algaegrowthrate(self,value):
		self._algaegrowthrate=value

	@property
	def initialconcentration_g_per_l_usersupplied(self):
		cdict={}
		try:
			cdict["chem_divalent_mercury"]=0.0
		except:
			cdict["chem_divalent_mercury"]=nan
		
		try:
			cdict["chem_elemental_mercury"]=0.0
		except:
			cdict["chem_elemental_mercury"]=nan
		
		try:
			cdict["chem_methylmercury"]=0.0
		except:
			cdict["chem_methylmercury"]=nan
		
		return cdict

	@property
	def chemical_initialconcentration_g_per_l_usersupplied(self):
		return self.initialconcentration_g_per_l_usersupplied[self.currentchemical.name]
	@property
	def genericdenominatorforcalculatingfractioninphases(self):
		cdict={}
		try:
			cdict["chem_divalent_mercury"]=self.containingvolumeelement.volume * (self.volumefraction_algae * self.chemical_ratioofconcinalgaetoconcdissolvedinwater * self.algaedensity_g_m3 * (self.constants.m3_per_l)  + self.volumefraction_solid * self.chemical_kd * self.constants.m3_per_l * self.rho + self.volumefraction_liquid )
		except:
			cdict["chem_divalent_mercury"]=nan
		
		try:
			cdict["chem_elemental_mercury"]=self.containingvolumeelement.volume * (self.volumefraction_algae * self.chemical_ratioofconcinalgaetoconcdissolvedinwater * self.algaedensity_g_m3 * (self.constants.m3_per_l)  + self.volumefraction_solid * self.chemical_kd * self.constants.m3_per_l * self.rho + self.volumefraction_liquid )
		except:
			cdict["chem_elemental_mercury"]=nan
		
		try:
			cdict["chem_methylmercury"]=self.containingvolumeelement.volume * (self.volumefraction_algae * self.chemical_ratioofconcinalgaetoconcdissolvedinwater * self.algaedensity_g_m3 * (self.constants.m3_per_l)  + self.volumefraction_solid * self.chemical_kd * self.constants.m3_per_l * self.rho + self.volumefraction_liquid )
		except:
			cdict["chem_methylmercury"]=nan
		
		return cdict

	@property
	def chemical_genericdenominatorforcalculatingfractioninphases(self):
		return self.genericdenominatorforcalculatingfractioninphases[self.currentchemical.name]
	_suspendedsedimentconcentration=0.01
	@property
	def suspendedsedimentconcentration(self):
		return self._suspendedsedimentconcentration
	@suspendedsedimentconcentration.setter
	def suspendedsedimentconcentration(self,value):
		self._suspendedsedimentconcentration=value

	@property
	def algaesedimentationrate_g_m2_day(self):
		return (self.carbonsedimentationrate_g_m2_day/ (self.algaecarboncontentdrywt *(1-self.algaewatercontent)))
	
	_chlorophyllconcentration_mg_l=0.01
	@property
	def chlorophyllconcentration_mg_l(self):
		return self._chlorophyllconcentration_mg_l
	@chlorophyllconcentration_mg_l.setter
	def chlorophyllconcentration_mg_l(self,value):
		self._chlorophyllconcentration_mg_l=value

	@property
	def boundarylayerthicknessbelowwater(self):
		cdict={}
		try:
			cdict["chem_divalent_mercury"]=318 * self.chemical_d_effective ** (0.683)
		except:
			cdict["chem_divalent_mercury"]=nan
		
		try:
			cdict["chem_elemental_mercury"]=318 * self.chemical_d_effective ** (0.683)
		except:
			cdict["chem_elemental_mercury"]=nan
		
		try:
			cdict["chem_methylmercury"]=318 * self.chemical_d_effective ** (0.683)
		except:
			cdict["chem_methylmercury"]=nan
		
		return cdict

	@property
	def chemical_boundarylayerthicknessbelowwater(self):
		return self.boundarylayerthicknessbelowwater[self.currentchemical.name]
	_organiccarboncontent=0.01
	@property
	def organiccarboncontent(self):
		return self._organiccarboncontent
	@organiccarboncontent.setter
	def organiccarboncontent(self,value):
		self._organiccarboncontent=value

	@property
	def suspendedsedimentconcentration_mg_l(self):
		return (self.suspendedsedimentconcentration*1000000/self.constants.l_per_m3)
	
	@property
	def d_owformhg_ph8(self):
		cdict={}
		try:
			cdict["chem_methylmercury"]=0.075 if self.chlorideconcentration_mg_l<= 0.112111281202651 else 0.075 if self.chlorideconcentration_mg_l<= 0.141139740854819 else 0.075 if self.chlorideconcentration_mg_l<= 0.177684406376176 else 0.075 if self.chlorideconcentration_mg_l<= 0.223691414466529 else 0.075 if self.chlorideconcentration_mg_l<= 0.281610806072095 else 0.075 if self.chlorideconcentration_mg_l<= 0.354527 else 0.075 if self.chlorideconcentration_mg_l<= 0.44632304946715 else 0.075 if self.chlorideconcentration_mg_l<= 0.561887428843661 else 0.075 if self.chlorideconcentration_mg_l<= 0.707374362738971 else 0.075 if self.chlorideconcentration_mg_l<= 0.890531560903796 else 0.075 if self.chlorideconcentration_mg_l<= 1.12111281202651 else 0.075 if self.chlorideconcentration_mg_l<= 1.41139740854819 else 0.075 if self.chlorideconcentration_mg_l<= 1.77684406376176 else 0.075 if self.chlorideconcentration_mg_l<= 2.23691414466529 else 0.075 if self.chlorideconcentration_mg_l<= 2.81610806072095 else 0.075 if self.chlorideconcentration_mg_l<= 3.54526999999991 else 0.075 if self.chlorideconcentration_mg_l<= 4.4632304946714 else 0.1 if self.chlorideconcentration_mg_l<= 5.61887428843648 else 0.1 if self.chlorideconcentration_mg_l<= 7.07374362738955 else 0.125 if self.chlorideconcentration_mg_l<= 8.90531560903775 else 0.125 if self.chlorideconcentration_mg_l<= 11.2111281202649 else 0.125 if self.chlorideconcentration_mg_l<= 14.1139740854816 else 0.125 if self.chlorideconcentration_mg_l<= 17.7684406376172 else 0.125 if self.chlorideconcentration_mg_l<= 22.3691414466524 else 0.15 if self.chlorideconcentration_mg_l<= 28.1610806072089 else 0.175 if self.chlorideconcentration_mg_l<= 35.4526999999992 else 0.225 if self.chlorideconcentration_mg_l<= 44.632304946714 else 0.25 if self.chlorideconcentration_mg_l<= 56.1887428843648 else 0.3 if self.chlorideconcentration_mg_l<= 70.7374362738956 else 0.325 if self.chlorideconcentration_mg_l<= 89.0531560903776 else 0.375 if self.chlorideconcentration_mg_l<= 112.111281202649 else 0.425 if self.chlorideconcentration_mg_l<= 141.139740854816 else 0.475 if self.chlorideconcentration_mg_l<= 177.684406376172 else 0.55 if self.chlorideconcentration_mg_l<= 223.691414466524 else 0.625 if self.chlorideconcentration_mg_l<= 281.610806072089 else 0.7 if self.chlorideconcentration_mg_l<= 354.526999999992 else 0.8 if self.chlorideconcentration_mg_l<= 446.32304946714 else 0.875 if self.chlorideconcentration_mg_l<= 561.887428843648 else 0.95 if self.chlorideconcentration_mg_l<= 707.374362738955 else 1.025 if self.chlorideconcentration_mg_l<= 890.531560903776 else 1.125 if self.chlorideconcentration_mg_l<= 1121.11281202649 else 1.175 if self.chlorideconcentration_mg_l<= 1411.39740854816 else 1.25 if self.chlorideconcentration_mg_l<= 1776.84406376172 else 1.325 if self.chlorideconcentration_mg_l<= 2236.91414466519 else 1.375 if self.chlorideconcentration_mg_l<= 2816.10806072082 else 1.425 if self.chlorideconcentration_mg_l<= 3545.26999999984 else 1.45 if self.chlorideconcentration_mg_l<= 4463.2304946713 else 1.5 if self.chlorideconcentration_mg_l<= 5618.87428843635 else 1.525 if self.chlorideconcentration_mg_l<= 7073.74362738939 else 1.575 if self.chlorideconcentration_mg_l<= 8905.31560903756 else 1.6 if self.chlorideconcentration_mg_l<= 11211.1281202646 else 1.65
		except:
			cdict["chem_methylmercury"]=nan
		
		return cdict

	@property
	def chemical_d_owformhg_ph8(self):
		return self.d_owformhg_ph8[self.currentchemical.name]
	@property
	def concentrationoutputunits(self):
		return ("mg/l")
	
	@property
	def d_owforhg2_ph8(self):
		cdict={}
		try:
			cdict["chem_divalent_mercury"]=0.025 if self.chlorideconcentration_mg_l<= 1.77684406376176 else 0.025 if self.chlorideconcentration_mg_l<= 2.23691414466529 else 0.025 if self.chlorideconcentration_mg_l<= 2.81610806072095 else 0.025 if self.chlorideconcentration_mg_l<= 3.54526999999991 else 0.025 if self.chlorideconcentration_mg_l<= 4.4632304946714 else 0.025 if self.chlorideconcentration_mg_l<= 5.61887428843648 else 0.025 if self.chlorideconcentration_mg_l<= 7.07374362738955 else 0.025 if self.chlorideconcentration_mg_l<= 8.90531560903775 else 0.025 if self.chlorideconcentration_mg_l<= 11.2111281202649 else 0.025 if self.chlorideconcentration_mg_l<= 14.1139740854816 else 0.025 if self.chlorideconcentration_mg_l<= 17.7684406376172 else 0.025 if self.chlorideconcentration_mg_l<= 22.3691414466524 else 0.025 if self.chlorideconcentration_mg_l<= 28.1610806072089 else 0.05 if self.chlorideconcentration_mg_l<= 35.4526999999992 else 0.05 if self.chlorideconcentration_mg_l<= 44.632304946714 else 0.05 if self.chlorideconcentration_mg_l<= 56.1887428843648 else 0.075 if self.chlorideconcentration_mg_l<= 70.7374362738956 else 0.075 if self.chlorideconcentration_mg_l<= 89.0531560903776 else 0.075 if self.chlorideconcentration_mg_l<= 112.111281202649 else 0.075 if self.chlorideconcentration_mg_l<= 141.139740854816 else 0.1 if self.chlorideconcentration_mg_l<= 177.684406376172 else 0.125 if self.chlorideconcentration_mg_l<= 223.691414466524 else 0.175 if self.chlorideconcentration_mg_l<= 281.610806072089 else 0.2 if self.chlorideconcentration_mg_l<= 354.526999999992 else 0.275 if self.chlorideconcentration_mg_l<= 446.32304946714 else 0.35 if self.chlorideconcentration_mg_l<= 561.887428843648 else 0.45 if self.chlorideconcentration_mg_l<= 707.374362738955 else 0.525 if self.chlorideconcentration_mg_l<= 890.531560903776 else 0.6 if self.chlorideconcentration_mg_l<= 1121.11281202649 else 0.675 if self.chlorideconcentration_mg_l<= 1411.39740854816 else 0.775 if self.chlorideconcentration_mg_l<= 1776.84406376172 else 0.725 if self.chlorideconcentration_mg_l<= 2236.91414466519 else 0.675 if self.chlorideconcentration_mg_l<= 2816.10806072082 else 0.625 if self.chlorideconcentration_mg_l<= 3545.26999999984 else 0.55 if self.chlorideconcentration_mg_l<= 4463.2304946713 else 0.475 if self.chlorideconcentration_mg_l<= 5618.87428843635 else 0.4 if self.chlorideconcentration_mg_l<= 7073.74362738939 else 0.325 if self.chlorideconcentration_mg_l<= 8905.31560903756 else 0.25 if self.chlorideconcentration_mg_l<= 11211.1281202646 else 0.175 if self.chlorideconcentration_mg_l<= 14113.9740854813 else 0.1
		except:
			cdict["chem_divalent_mercury"]=nan
		
		return cdict

	@property
	def chemical_d_owforhg2_ph8(self):
		return self.d_owforhg2_ph8[self.currentchemical.name]
	_concentrationoutputfactor=1000.0
	@property
	def concentrationoutputfactor(self):
		return self._concentrationoutputfactor
	@concentrationoutputfactor.setter
	def concentrationoutputfactor(self,value):
		self._concentrationoutputfactor=value

	@property
	def waterdensity(self):
		return (1000)
	
	@property
	def fractionmass_dissolved(self):
		cdict={}
		try:
			cdict["chem_divalent_mercury"]=self.containingvolumeelement.volume * (self.volumefraction_liquid) / self.chemical_genericdenominatorforcalculatingfractioninphases
		except:
			cdict["chem_divalent_mercury"]=nan
		
		try:
			cdict["chem_elemental_mercury"]=self.containingvolumeelement.volume * (self.volumefraction_liquid) / self.chemical_genericdenominatorforcalculatingfractioninphases
		except:
			cdict["chem_elemental_mercury"]=nan
		
		try:
			cdict["chem_methylmercury"]=self.containingvolumeelement.volume * (self.volumefraction_liquid) / self.chemical_genericdenominatorforcalculatingfractioninphases
		except:
			cdict["chem_methylmercury"]=nan
		
		return cdict

	@property
	def chemical_fractionmass_dissolved(self):
		return self.fractionmass_dissolved[self.currentchemical.name]
	@property
	def height(self):
		return (self.containingvolumeelement.height)
	
	@property
	def d_owforhg2_ph6(self):
		cdict={}
		try:
			cdict["chem_divalent_mercury"]=0.1 if self.chlorideconcentration_mg_l<= 1.77684406376176 else 0.125 if self.chlorideconcentration_mg_l<= 2.23691414466529 else 0.175 if self.chlorideconcentration_mg_l<= 2.81610806072095 else 0.2 if self.chlorideconcentration_mg_l<= 3.54526999999991 else 0.325 if self.chlorideconcentration_mg_l<= 4.4632304946714 else 0.45 if self.chlorideconcentration_mg_l<= 5.61887428843648 else 0.575 if self.chlorideconcentration_mg_l<= 7.07374362738955 else 0.7 if self.chlorideconcentration_mg_l<= 8.90531560903775 else 0.825 if self.chlorideconcentration_mg_l<= 11.2111281202649 else 0.975 if self.chlorideconcentration_mg_l<= 14.1139740854816 else 1.1 if self.chlorideconcentration_mg_l<= 17.7684406376172 else 1.2 if self.chlorideconcentration_mg_l<= 22.3691414466524 else 1.3 if self.chlorideconcentration_mg_l<= 28.1610806072089 else 1.4 if self.chlorideconcentration_mg_l<= 35.4526999999992 else 1.45 if self.chlorideconcentration_mg_l<= 44.632304946714 else 1.475 if self.chlorideconcentration_mg_l<= 56.1887428843648 else 1.475 if self.chlorideconcentration_mg_l<= 70.7374362738956 else 1.5 if self.chlorideconcentration_mg_l<= 89.0531560903776 else 1.525 if self.chlorideconcentration_mg_l<= 112.111281202649 else 1.55 if self.chlorideconcentration_mg_l<= 141.139740854816 else 1.575 if self.chlorideconcentration_mg_l<= 177.684406376172 else 1.575 if self.chlorideconcentration_mg_l<= 223.691414466524 else 1.55 if self.chlorideconcentration_mg_l<= 281.610806072089 else 1.525 if self.chlorideconcentration_mg_l<= 354.526999999992 else 1.475 if self.chlorideconcentration_mg_l<= 446.32304946714 else 1.425 if self.chlorideconcentration_mg_l<= 561.887428843648 else 1.35 if self.chlorideconcentration_mg_l<= 707.374362738955 else 1.275 if self.chlorideconcentration_mg_l<= 890.531560903776 else 1.225 if self.chlorideconcentration_mg_l<= 1121.11281202649 else 1.15 if self.chlorideconcentration_mg_l<= 1411.39740854816 else 1.1 if self.chlorideconcentration_mg_l<= 1776.84406376172 else 0.95 if self.chlorideconcentration_mg_l<= 2236.91414466519 else 0.8 if self.chlorideconcentration_mg_l<= 2816.10806072082 else 0.7 if self.chlorideconcentration_mg_l<= 3545.26999999984 else 0.6 if self.chlorideconcentration_mg_l<= 4463.2304946713 else 0.525 if self.chlorideconcentration_mg_l<= 5618.87428843635 else 0.425 if self.chlorideconcentration_mg_l<= 7073.74362738939 else 0.325 if self.chlorideconcentration_mg_l<= 8905.31560903756 else 0.25 if self.chlorideconcentration_mg_l<= 11211.1281202646 else 0.175 if self.chlorideconcentration_mg_l<= 14113.9740854813 else 0.1
		except:
			cdict["chem_divalent_mercury"]=nan
		
		return cdict

	@property
	def chemical_d_owforhg2_ph6(self):
		return self.d_owforhg2_ph6[self.currentchemical.name]
	@property
	def sedimentdepositionrate_m3_m2_day(self):
		return (self.sedimentdepositionrate_kg_m2_day / self.rho)
	
	@property
	def algaesedimentationrate_m3_m2_day(self):
		return (self.algaesedimentationrate_g_m2_day/self.algaedensity_g_m3)
	
	@property
	def meandepth_m(self):
		return ((self.containingvolumeelement.top + self.containingvolumeelement.bottom)/2.0)
	
	@property
	def d_owformhg_ph6(self):
		cdict={}
		try:
			cdict["chem_methylmercury"]=0.125 if self.chlorideconcentration_mg_l<= 0.112111281202651 else 0.125 if self.chlorideconcentration_mg_l<= 0.141139740854819 else 0.125 if self.chlorideconcentration_mg_l<= 0.177684406376176 else 0.125 if self.chlorideconcentration_mg_l<= 0.223691414466529 else 0.15 if self.chlorideconcentration_mg_l<= 0.281610806072095 else 0.175 if self.chlorideconcentration_mg_l<= 0.354527 else 0.2 if self.chlorideconcentration_mg_l<= 0.44632304946715 else 0.25 if self.chlorideconcentration_mg_l<= 0.561887428843661 else 0.3 if self.chlorideconcentration_mg_l<= 0.707374362738971 else 0.325 if self.chlorideconcentration_mg_l<= 0.890531560903796 else 0.375 if self.chlorideconcentration_mg_l<= 1.12111281202651 else 0.4 if self.chlorideconcentration_mg_l<= 1.41139740854819 else 0.45 if self.chlorideconcentration_mg_l<= 1.77684406376176 else 0.5 if self.chlorideconcentration_mg_l<= 2.23691414466529 else 0.575 if self.chlorideconcentration_mg_l<= 2.81610806072095 else 0.675 if self.chlorideconcentration_mg_l<= 3.54526999999991 else 0.775 if self.chlorideconcentration_mg_l<= 4.4632304946714 else 0.85 if self.chlorideconcentration_mg_l<= 5.61887428843648 else 0.925 if self.chlorideconcentration_mg_l<= 7.07374362738955 else 1.05 if self.chlorideconcentration_mg_l<= 8.90531560903775 else 1.125 if self.chlorideconcentration_mg_l<= 11.2111281202649 else 1.2 if self.chlorideconcentration_mg_l<= 14.1139740854816 else 1.275 if self.chlorideconcentration_mg_l<= 17.7684406376172 else 1.375 if self.chlorideconcentration_mg_l<= 22.3691414466524 else 1.45 if self.chlorideconcentration_mg_l<= 28.1610806072089 else 1.475 if self.chlorideconcentration_mg_l<= 35.4526999999992 else 1.5 if self.chlorideconcentration_mg_l<= 44.632304946714 else 1.525 if self.chlorideconcentration_mg_l<= 56.1887428843648 else 1.55 if self.chlorideconcentration_mg_l<= 70.7374362738956 else 1.575 if self.chlorideconcentration_mg_l<= 89.0531560903776 else 1.6 if self.chlorideconcentration_mg_l<= 112.111281202649 else 1.675 if self.chlorideconcentration_mg_l<= 141.139740854816 else 1.65 if self.chlorideconcentration_mg_l<= 177.684406376172 else 1.675 if self.chlorideconcentration_mg_l<= 223.691414466524 else 1.675 if self.chlorideconcentration_mg_l<= 281.610806072089 else 1.675 if self.chlorideconcentration_mg_l<= 354.526999999992 else 1.675 if self.chlorideconcentration_mg_l<= 446.32304946714 else 1.7 if self.chlorideconcentration_mg_l<= 561.887428843648 else 1.7 if self.chlorideconcentration_mg_l<= 707.374362738955 else 1.7 if self.chlorideconcentration_mg_l<= 890.531560903776 else 1.7 if self.chlorideconcentration_mg_l<= 1121.11281202649 else 1.7 if self.chlorideconcentration_mg_l<= 1411.39740854816 else 1.7 if self.chlorideconcentration_mg_l<= 1776.84406376172 else 1.7 if self.chlorideconcentration_mg_l<= 2236.91414466519 else 1.7 if self.chlorideconcentration_mg_l<= 2816.10806072082 else 1.7 if self.chlorideconcentration_mg_l<= 3545.26999999984 else 1.7 if self.chlorideconcentration_mg_l<= 4463.2304946713 else 1.7 if self.chlorideconcentration_mg_l<= 5618.87428843635 else 1.7 if self.chlorideconcentration_mg_l<= 7073.74362738939 else 1.7 if self.chlorideconcentration_mg_l<= 8905.31560903756 else 1.7 if self.chlorideconcentration_mg_l<= 11211.1281202646 else 1.7
		except:
			cdict["chem_methylmercury"]=nan
		
		return cdict

	@property
	def chemical_d_owformhg_ph6(self):
		return self.d_owformhg_ph6[self.currentchemical.name]
	_rho=2600.0
	@property
	def rho(self):
		return self._rho
	@rho.setter
	def rho(self,value):
		self._rho=value

	_algaedensityinwatercolumn_g_l=0.01
	@property
	def algaedensityinwatercolumn_g_l(self):
		return self._algaedensityinwatercolumn_g_l
	@algaedensityinwatercolumn_g_l.setter
	def algaedensityinwatercolumn_g_l(self,value):
		self._algaedensityinwatercolumn_g_l=value

	@property
	def volumefraction_algae(self):
		return ((self.algaedensityinwatercolumn_g_l * self.constants.l_per_m3)/(self.algaedensity_g_m3))
	
	_dimensionlessviscoussublayerthickness=4.0
	@property
	def dimensionlessviscoussublayerthickness(self):
		return self._dimensionlessviscoussublayerthickness
	@dimensionlessviscoussublayerthickness.setter
	def dimensionlessviscoussublayerthickness(self,value):
		self._dimensionlessviscoussublayerthickness=value

	@property
	def sedimentdepositionrate_kg_m2_day(self):
		return (self.sedimentdepositionvelocity*self.suspendedsedimentconcentration)
	
	@property
	def carbonsedimentationrate_g_m2_day(self):
		return ((10**(1.82 + (0.62 * log(self.chlorophyllconcentration_mg_m3)/log(10)))/1000))
	
	@property
	def algaedensity_g_um3(self):
		return (self.algaedensity_g_m3 / self.constants.um3_per_m3)
	
	_flushes_per_year=0.01
	@property
	def flushes_per_year(self):
		return self._flushes_per_year
	@flushes_per_year.setter
	def flushes_per_year(self,value):
		self._flushes_per_year=value

	@property
	def ratioofconcinalgaetoconcdissolvedinwater(self):
		cdict={}
		try:
			cdict["chem_divalent_mercury"]=(self.chemical_d_ow * self.chemical_algaeuptakerate * 3 / (self.algaeradius * self.algaedensity_g_um3 * self.algaegrowthrate))
		except:
			cdict["chem_divalent_mercury"]=nan
		
		try:
			cdict["chem_elemental_mercury"]=(self.chemical_d_ow * self.chemical_algaeuptakerate * 3 / (self.algaeradius * self.algaedensity_g_um3 * self.algaegrowthrate))
		except:
			cdict["chem_elemental_mercury"]=nan
		
		try:
			cdict["chem_methylmercury"]=(self.chemical_d_ow * self.chemical_algaeuptakerate * 3 / (self.algaeradius * self.algaedensity_g_um3 * self.algaegrowthrate))
		except:
			cdict["chem_methylmercury"]=nan
		
		return cdict

	@property
	def chemical_ratioofconcinalgaetoconcdissolvedinwater(self):
		return self.ratioofconcinalgaetoconcdissolvedinwater[self.currentchemical.name]
	_algaeradius=2.5
	@property
	def algaeradius(self):
		return self._algaeradius
	@algaeradius.setter
	def algaeradius(self,value):
		self._algaeradius=value

	@property
	def area(self):
		return (self.containingvolumeelement.area)
	
	_ph=0.01
	@property
	def ph(self):
		return self._ph
	@ph.setter
	def ph(self,value):
		self._ph=value

	@property
	def algaeuptakerate(self):
		cdict={}
		try:
			cdict["chem_divalent_mercury"]=2.04e-10
		except:
			cdict["chem_divalent_mercury"]=nan
		
		try:
			cdict["chem_elemental_mercury"]=0.0
		except:
			cdict["chem_elemental_mercury"]=nan
		
		try:
			cdict["chem_methylmercury"]=3.6e-10
		except:
			cdict["chem_methylmercury"]=nan
		
		return cdict

	@property
	def chemical_algaeuptakerate(self):
		return self.algaeuptakerate[self.currentchemical.name]
	_fractionsand=0.25
	@property
	def fractionsand(self):
		return self._fractionsand
	@fractionsand.setter
	def fractionsand(self,value):
		self._fractionsand=value

	@property
	def totalalgaemass(self):
		return (self.containingvolumeelement.volume*self.volumefraction_algae*self.algaedensity_g_m3 * self.constants.kg_per_g)
	
	@property
	def watertemperature_c(self):
		return (self.containingvolumeelement.watertemperature_k - 273)
	
	@property
	def initialconcentration_g_per_l(self):
		cdict={}
		try:
			cdict["chem_divalent_mercury"]=self.containingscenario.fractioninitialconcentrations * self.chemical_initialconcentration_g_per_l_usersupplied
		except:
			cdict["chem_divalent_mercury"]=nan
		
		try:
			cdict["chem_elemental_mercury"]=self.containingscenario.fractioninitialconcentrations * self.chemical_initialconcentration_g_per_l_usersupplied
		except:
			cdict["chem_elemental_mercury"]=nan
		
		try:
			cdict["chem_methylmercury"]=self.containingscenario.fractioninitialconcentrations * self.chemical_initialconcentration_g_per_l_usersupplied
		except:
			cdict["chem_methylmercury"]=nan
		
		return cdict

	@property
	def chemical_initialconcentration_g_per_l(self):
		return self.initialconcentration_g_per_l[self.currentchemical.name]
	@property
	def fractionmass_sorbed(self):
		cdict={}
		try:
			cdict["chem_divalent_mercury"]=self.containingvolumeelement.volume * (self.volumefraction_solid) * self.chemical_kd * self.constants.m3_per_l * self.rho / self.chemical_genericdenominatorforcalculatingfractioninphases
		except:
			cdict["chem_divalent_mercury"]=nan
		
		try:
			cdict["chem_elemental_mercury"]=self.containingvolumeelement.volume * (self.volumefraction_solid) * self.chemical_kd * self.constants.m3_per_l * self.rho / self.chemical_genericdenominatorforcalculatingfractioninphases
		except:
			cdict["chem_elemental_mercury"]=nan
		
		try:
			cdict["chem_methylmercury"]=self.containingvolumeelement.volume * (self.volumefraction_solid) * self.chemical_kd * self.constants.m3_per_l * self.rho / self.chemical_genericdenominatorforcalculatingfractioninphases
		except:
			cdict["chem_methylmercury"]=nan
		
		return cdict

	@property
	def chemical_fractionmass_sorbed(self):
		return self.fractionmass_sorbed[self.currentchemical.name]
	@property
	def isflowing(self):
		return (False)
	
	@property
	def d_owformhg_ph4(self):
		cdict={}
		try:
			cdict["chem_methylmercury"]=0.5 if self.chlorideconcentration_mg_l<= 0.112111281202651 else 0.55 if self.chlorideconcentration_mg_l<= 0.141139740854819 else 0.625 if self.chlorideconcentration_mg_l<= 0.177684406376176 else 0.725 if self.chlorideconcentration_mg_l<= 0.223691414466529 else 0.825 if self.chlorideconcentration_mg_l<= 0.281610806072095 else 0.9 if self.chlorideconcentration_mg_l<= 0.354527 else 1 if self.chlorideconcentration_mg_l<= 0.44632304946715 else 1.075 if self.chlorideconcentration_mg_l<= 0.561887428843661 else 1.15 if self.chlorideconcentration_mg_l<= 0.707374362738971 else 1.25 if self.chlorideconcentration_mg_l<= 0.890531560903796 else 1.3 if self.chlorideconcentration_mg_l<= 1.12111281202651 else 1.375 if self.chlorideconcentration_mg_l<= 1.41139740854819 else 1.45 if self.chlorideconcentration_mg_l<= 1.77684406376176 else 1.5 if self.chlorideconcentration_mg_l<= 2.23691414466529 else 1.55 if self.chlorideconcentration_mg_l<= 2.81610806072095 else 1.575 if self.chlorideconcentration_mg_l<= 3.54526999999991 else 1.6 if self.chlorideconcentration_mg_l<= 4.4632304946714 else 1.6 if self.chlorideconcentration_mg_l<= 5.61887428843648 else 1.625 if self.chlorideconcentration_mg_l<= 7.07374362738955 else 1.625 if self.chlorideconcentration_mg_l<= 8.90531560903775 else 1.65 if self.chlorideconcentration_mg_l<= 11.2111281202649 else 1.65 if self.chlorideconcentration_mg_l<= 14.1139740854816 else 1.675 if self.chlorideconcentration_mg_l<= 17.7684406376172 else 1.675 if self.chlorideconcentration_mg_l<= 22.3691414466524 else 1.7 if self.chlorideconcentration_mg_l<= 28.1610806072089 else 1.7 if self.chlorideconcentration_mg_l<= 35.4526999999992 else 1.7 if self.chlorideconcentration_mg_l<= 44.632304946714 else 1.7 if self.chlorideconcentration_mg_l<= 56.1887428843648 else 1.7 if self.chlorideconcentration_mg_l<= 70.7374362738956 else 1.7 if self.chlorideconcentration_mg_l<= 89.0531560903776 else 1.7 if self.chlorideconcentration_mg_l<= 112.111281202649 else 1.7 if self.chlorideconcentration_mg_l<= 141.139740854816 else 1.7 if self.chlorideconcentration_mg_l<= 177.684406376172 else 1.7 if self.chlorideconcentration_mg_l<= 223.691414466524 else 1.7 if self.chlorideconcentration_mg_l<= 281.610806072089 else 1.7 if self.chlorideconcentration_mg_l<= 354.526999999992 else 1.7 if self.chlorideconcentration_mg_l<= 446.32304946714 else 1.7 if self.chlorideconcentration_mg_l<= 561.887428843648 else 1.7 if self.chlorideconcentration_mg_l<= 707.374362738955 else 1.7 if self.chlorideconcentration_mg_l<= 890.531560903776 else 1.7 if self.chlorideconcentration_mg_l<= 1121.11281202649 else 1.7 if self.chlorideconcentration_mg_l<= 1411.39740854816 else 1.7 if self.chlorideconcentration_mg_l<= 1776.84406376172 else 1.7 if self.chlorideconcentration_mg_l<= 2236.91414466519 else 1.7 if self.chlorideconcentration_mg_l<= 2816.10806072082 else 1.7 if self.chlorideconcentration_mg_l<= 3545.26999999984 else 1.7 if self.chlorideconcentration_mg_l<= 4463.2304946713 else 1.7 if self.chlorideconcentration_mg_l<= 5618.87428843635 else 1.7 if self.chlorideconcentration_mg_l<= 7073.74362738939 else 1.7 if self.chlorideconcentration_mg_l<= 8905.31560903756 else 1.7 if self.chlorideconcentration_mg_l<= 11211.1281202646 else 1.7
		except:
			cdict["chem_methylmercury"]=nan
		
		return cdict

	@property
	def chemical_d_owformhg_ph4(self):
		return self.d_owformhg_ph4[self.currentchemical.name]
	@property
	def d_owformhg_ph5(self):
		cdict={}
		try:
			cdict["chem_methylmercury"]=0.15 if self.chlorideconcentration_mg_l<= 0.112111281202651 else 0.15 if self.chlorideconcentration_mg_l<= 0.141139740854819 else 0.2 if self.chlorideconcentration_mg_l<= 0.177684406376176 else 0.25 if self.chlorideconcentration_mg_l<= 0.223691414466529 else 0.4 if self.chlorideconcentration_mg_l<= 0.281610806072095 else 0.55 if self.chlorideconcentration_mg_l<= 0.354527 else 0.65 if self.chlorideconcentration_mg_l<= 0.44632304946715 else 0.75 if self.chlorideconcentration_mg_l<= 0.561887428843661 else 0.85 if self.chlorideconcentration_mg_l<= 0.707374362738971 else 0.925 if self.chlorideconcentration_mg_l<= 0.890531560903796 else 1.025 if self.chlorideconcentration_mg_l<= 1.12111281202651 else 1.1 if self.chlorideconcentration_mg_l<= 1.41139740854819 else 1.2 if self.chlorideconcentration_mg_l<= 1.77684406376176 else 1.275 if self.chlorideconcentration_mg_l<= 2.23691414466529 else 1.35 if self.chlorideconcentration_mg_l<= 2.81610806072095 else 1.4 if self.chlorideconcentration_mg_l<= 3.54526999999991 else 1.45 if self.chlorideconcentration_mg_l<= 4.4632304946714 else 1.475 if self.chlorideconcentration_mg_l<= 5.61887428843648 else 1.5 if self.chlorideconcentration_mg_l<= 7.07374362738955 else 1.525 if self.chlorideconcentration_mg_l<= 8.90531560903775 else 1.575 if self.chlorideconcentration_mg_l<= 11.2111281202649 else 1.6 if self.chlorideconcentration_mg_l<= 14.1139740854816 else 1.625 if self.chlorideconcentration_mg_l<= 17.7684406376172 else 1.65 if self.chlorideconcentration_mg_l<= 22.3691414466524 else 1.65 if self.chlorideconcentration_mg_l<= 28.1610806072089 else 1.65 if self.chlorideconcentration_mg_l<= 35.4526999999992 else 1.65 if self.chlorideconcentration_mg_l<= 44.632304946714 else 1.675 if self.chlorideconcentration_mg_l<= 56.1887428843648 else 1.675 if self.chlorideconcentration_mg_l<= 70.7374362738956 else 1.675 if self.chlorideconcentration_mg_l<= 89.0531560903776 else 1.675 if self.chlorideconcentration_mg_l<= 112.111281202649 else 1.675 if self.chlorideconcentration_mg_l<= 141.139740854816 else 1.675 if self.chlorideconcentration_mg_l<= 177.684406376172 else 1.675 if self.chlorideconcentration_mg_l<= 223.691414466524 else 1.675 if self.chlorideconcentration_mg_l<= 281.610806072089 else 1.7 if self.chlorideconcentration_mg_l<= 354.526999999992 else 1.7 if self.chlorideconcentration_mg_l<= 446.32304946714 else 1.7 if self.chlorideconcentration_mg_l<= 561.887428843648 else 1.7 if self.chlorideconcentration_mg_l<= 707.374362738955 else 1.7 if self.chlorideconcentration_mg_l<= 890.531560903776 else 1.7 if self.chlorideconcentration_mg_l<= 1121.11281202649 else 1.7 if self.chlorideconcentration_mg_l<= 1411.39740854816 else 1.7 if self.chlorideconcentration_mg_l<= 1776.84406376172 else 1.7 if self.chlorideconcentration_mg_l<= 2236.91414466519 else 1.7 if self.chlorideconcentration_mg_l<= 2816.10806072082 else 1.7 if self.chlorideconcentration_mg_l<= 3545.26999999984 else 1.7 if self.chlorideconcentration_mg_l<= 4463.2304946713 else 1.7 if self.chlorideconcentration_mg_l<= 5618.87428843635 else 1.7 if self.chlorideconcentration_mg_l<= 7073.74362738939 else 1.7 if self.chlorideconcentration_mg_l<= 8905.31560903756 else 1.7 if self.chlorideconcentration_mg_l<= 11211.1281202646 else 1.7
		except:
			cdict["chem_methylmercury"]=nan
		
		return cdict

	@property
	def chemical_d_owformhg_ph5(self):
		return self.d_owformhg_ph5[self.currentchemical.name]
	@property
	def d_owformhg_ph7(self):
		cdict={}
		try:
			cdict["chem_methylmercury"]=0.075 if self.chlorideconcentration_mg_l<= 0.112111281202651 else 0.075 if self.chlorideconcentration_mg_l<= 0.141139740854819 else 0.075 if self.chlorideconcentration_mg_l<= 0.177684406376176 else 0.075 if self.chlorideconcentration_mg_l<= 0.223691414466529 else 0.075 if self.chlorideconcentration_mg_l<= 0.281610806072095 else 0.075 if self.chlorideconcentration_mg_l<= 0.354527 else 0.075 if self.chlorideconcentration_mg_l<= 0.44632304946715 else 0.075 if self.chlorideconcentration_mg_l<= 0.561887428843661 else 0.1 if self.chlorideconcentration_mg_l<= 0.707374362738971 else 0.1 if self.chlorideconcentration_mg_l<= 0.890531560903796 else 0.125 if self.chlorideconcentration_mg_l<= 1.12111281202651 else 0.125 if self.chlorideconcentration_mg_l<= 1.41139740854819 else 0.125 if self.chlorideconcentration_mg_l<= 1.77684406376176 else 0.15 if self.chlorideconcentration_mg_l<= 2.23691414466529 else 0.175 if self.chlorideconcentration_mg_l<= 2.81610806072095 else 0.2 if self.chlorideconcentration_mg_l<= 3.54526999999991 else 0.225 if self.chlorideconcentration_mg_l<= 4.4632304946714 else 0.275 if self.chlorideconcentration_mg_l<= 5.61887428843648 else 0.3 if self.chlorideconcentration_mg_l<= 7.07374362738955 else 0.35 if self.chlorideconcentration_mg_l<= 8.90531560903775 else 0.375 if self.chlorideconcentration_mg_l<= 11.2111281202649 else 0.425 if self.chlorideconcentration_mg_l<= 14.1139740854816 else 0.45 if self.chlorideconcentration_mg_l<= 17.7684406376172 else 0.525 if self.chlorideconcentration_mg_l<= 22.3691414466524 else 0.6 if self.chlorideconcentration_mg_l<= 28.1610806072089 else 0.675 if self.chlorideconcentration_mg_l<= 35.4526999999992 else 0.8 if self.chlorideconcentration_mg_l<= 44.632304946714 else 0.875 if self.chlorideconcentration_mg_l<= 56.1887428843648 else 0.975 if self.chlorideconcentration_mg_l<= 70.7374362738956 else 1.075 if self.chlorideconcentration_mg_l<= 89.0531560903776 else 1.175 if self.chlorideconcentration_mg_l<= 112.111281202649 else 1.225 if self.chlorideconcentration_mg_l<= 141.139740854816 else 1.325 if self.chlorideconcentration_mg_l<= 177.684406376172 else 1.4 if self.chlorideconcentration_mg_l<= 223.691414466524 else 1.45 if self.chlorideconcentration_mg_l<= 281.610806072089 else 1.475 if self.chlorideconcentration_mg_l<= 354.526999999992 else 1.5 if self.chlorideconcentration_mg_l<= 446.32304946714 else 1.525 if self.chlorideconcentration_mg_l<= 561.887428843648 else 1.55 if self.chlorideconcentration_mg_l<= 707.374362738955 else 1.575 if self.chlorideconcentration_mg_l<= 890.531560903776 else 1.625 if self.chlorideconcentration_mg_l<= 1121.11281202649 else 1.65 if self.chlorideconcentration_mg_l<= 1411.39740854816 else 1.675 if self.chlorideconcentration_mg_l<= 1776.84406376172 else 1.675 if self.chlorideconcentration_mg_l<= 2236.91414466519 else 1.675 if self.chlorideconcentration_mg_l<= 2816.10806072082 else 1.675 if self.chlorideconcentration_mg_l<= 3545.26999999984 else 1.675 if self.chlorideconcentration_mg_l<= 4463.2304946713 else 1.675 if self.chlorideconcentration_mg_l<= 5618.87428843635 else 1.675 if self.chlorideconcentration_mg_l<= 7073.74362738939 else 1.675 if self.chlorideconcentration_mg_l<= 8905.31560903756 else 1.7 if self.chlorideconcentration_mg_l<= 11211.1281202646 else 1.7
		except:
			cdict["chem_methylmercury"]=nan
		
		return cdict

	@property
	def chemical_d_owformhg_ph7(self):
		return self.d_owformhg_ph7[self.currentchemical.name]
	@property
	def chlorideconcentration_mg_m3(self):
		return (self.chlorideconcentration_mg_l*1000)
	
	@property
	def z_solid(self):
		cdict={}
		try:
			cdict["chem_divalent_mercury"]=self.chemical_kd * (self.rho / 1000) * self.currentchemical.z_purewater
		except:
			cdict["chem_divalent_mercury"]=nan
		
		try:
			cdict["chem_elemental_mercury"]=self.chemical_kd * (self.rho / 1000) * self.currentchemical.z_purewater
		except:
			cdict["chem_elemental_mercury"]=nan
		
		try:
			cdict["chem_methylmercury"]=self.chemical_kd * (self.rho / 1000) * self.currentchemical.z_purewater
		except:
			cdict["chem_methylmercury"]=nan
		
		return cdict

	@property
	def chemical_z_solid(self):
		return self.z_solid[self.currentchemical.name]
	@property
	def z_total(self):
		cdict={}
		try:
			cdict["chem_divalent_mercury"]=self.chemical_z_liquid *self.volumefraction_liquid +self.chemical_z_solid *self.volumefraction_solid + self.chemical_z_algae*self.volumefraction_algae
		except:
			cdict["chem_divalent_mercury"]=nan
		
		try:
			cdict["chem_elemental_mercury"]=self.chemical_z_liquid *self.volumefraction_liquid +self.chemical_z_solid *self.volumefraction_solid + self.chemical_z_algae*self.volumefraction_algae
		except:
			cdict["chem_elemental_mercury"]=nan
		
		try:
			cdict["chem_methylmercury"]=self.chemical_z_liquid *self.volumefraction_liquid +self.chemical_z_solid *self.volumefraction_solid + self.chemical_z_algae*self.volumefraction_algae
		except:
			cdict["chem_methylmercury"]=nan
		
		return cdict

	@property
	def chemical_z_total(self):
		return self.z_total[self.currentchemical.name]
	@property
	def kd(self):
		cdict={}
		try:
			cdict["chem_divalent_mercury"]=100000.0
		except:
			cdict["chem_divalent_mercury"]=nan
		
		try:
			cdict["chem_elemental_mercury"]=1000.0
		except:
			cdict["chem_elemental_mercury"]=nan
		
		try:
			cdict["chem_methylmercury"]=100000.0
		except:
			cdict["chem_methylmercury"]=nan
		
		return cdict

	@property
	def chemical_kd(self):
		return self.kd[self.currentchemical.name]
	_chlorideconcentration_mg_l=0.01
	@property
	def chlorideconcentration_mg_l(self):
		return self._chlorideconcentration_mg_l
	@chlorideconcentration_mg_l.setter
	def chlorideconcentration_mg_l(self,value):
		self._chlorideconcentration_mg_l=value

	@property
	def chlorophyllconcentration_mg_m3(self):
		return (self.chlorophyllconcentration_mg_l*self.constants.l_per_m3)
	
	@property
	def volume(self):
		return (self.containingvolumeelement.volume)
	
	@property
	def vapordrydepositionvelocity_m_day(self):
		cdict={}
		try:
			cdict["chem_divalent_mercury"]=2500.0
		except:
			cdict["chem_divalent_mercury"]=nan
		
		return cdict

	@property
	def chemical_vapordrydepositionvelocity_m_day(self):
		return self.vapordrydepositionvelocity_m_day[self.currentchemical.name]
class water_column_carnivore:
	def __init__(self,constants,containingscenario,currentchemical,containingvolumeelement,comp_objects_dict):
		self.containingscenario=containingscenario
		self.currentchemical=currentchemical
		self.constants=constants
		self.containingvolumeelement=containingvolumeelement
		self.comp_objects_dict=comp_objects_dict
	@property
	def generaldegradationrate(self):
		cdict={}
		return cdict

	@property
	def chemical_generaldegradationrate(self):
		return self.generaldegradationrate[self.currentchemical.name]
	@property
	def initialconcentration_g_per_kg_usersupplied(self):
		cdict={}
		try:
			cdict["chem_divalent_mercury"]=0.0
		except:
			cdict["chem_divalent_mercury"]=nan
		
		try:
			cdict["chem_elemental_mercury"]=0.0
		except:
			cdict["chem_elemental_mercury"]=nan
		
		try:
			cdict["chem_methylmercury"]=0.0
		except:
			cdict["chem_methylmercury"]=nan
		
		return cdict

	@property
	def chemical_initialconcentration_g_per_kg_usersupplied(self):
		return self.initialconcentration_g_per_kg_usersupplied[self.currentchemical.name]
	@property
	def assimilationefficiencyfromfood(self):
		cdict={}
		try:
			cdict["chem_divalent_mercury"]=0.06
		except:
			cdict["chem_divalent_mercury"]=nan
		
		try:
			cdict["chem_elemental_mercury"]=0.06
		except:
			cdict["chem_elemental_mercury"]=nan
		
		try:
			cdict["chem_methylmercury"]=0.2
		except:
			cdict["chem_methylmercury"]=nan
		
		return cdict

	@property
	def chemical_assimilationefficiencyfromfood(self):
		return self.assimilationefficiencyfromfood[self.currentchemical.name]
	@property
	def acceptableabiotic(self):
		return ("abiotic | surface water | surface water - default")
	
	@property
	def foodingestionrate(self):
		return (self.feedingrate/self.bw)
	
	@property
	def reductionrate(self):
		cdict={}
		try:
			cdict["chem_divalent_mercury"]=0.0
		except:
			cdict["chem_divalent_mercury"]=nan
		
		return cdict

	@property
	def chemical_reductionrate(self):
		return self.reductionrate[self.currentchemical.name]
	_fishlipidfraction=0.057
	@property
	def fishlipidfraction(self):
		return self._fishlipidfraction
	@fishlipidfraction.setter
	def fishlipidfraction(self,value):
		self._fishlipidfraction=value

	@property
	def image(self):
		return ("c:\models\trim\data\images\largemouth.gif")
	
	_bw=2.0
	@property
	def bw(self):
		return self._bw
	@bw.setter
	def bw(self,value):
		self._bw=value

	@property
	def halflife(self):
		cdict={}
		return cdict

	@property
	def chemical_halflife(self):
		return self.halflife[self.currentchemical.name]
	_fractiondietfishbenthiccarnivore=0.01
	@property
	def fractiondietfishbenthiccarnivore(self):
		return self._fractiondietfishbenthiccarnivore
	@fractiondietfishbenthiccarnivore.setter
	def fractiondietfishbenthiccarnivore(self,value):
		self._fractiondietfishbenthiccarnivore=value

	@property
	def feedingrate(self):
		return (0.022 * self.bw ** (0.85) * exp(0.06 * linkedCompartmentvalue(self.containingvolumeelement,self.comp_objects_dict,"surface_water","watertemperature_c")))
	
	@property
	def initialconcentration_g_per_kg(self):
		cdict={}
		try:
			cdict["chem_divalent_mercury"]=self.containingscenario.fractioninitialconcentrations * self.chemical_initialconcentration_g_per_kg_usersupplied
		except:
			cdict["chem_divalent_mercury"]=nan
		
		try:
			cdict["chem_elemental_mercury"]=self.containingscenario.fractioninitialconcentrations * self.chemical_initialconcentration_g_per_kg_usersupplied
		except:
			cdict["chem_elemental_mercury"]=nan
		
		try:
			cdict["chem_methylmercury"]=self.containingscenario.fractioninitialconcentrations * self.chemical_initialconcentration_g_per_kg_usersupplied
		except:
			cdict["chem_methylmercury"]=nan
		
		return cdict

	@property
	def chemical_initialconcentration_g_per_kg(self):
		return self.initialconcentration_g_per_kg[self.currentchemical.name]
	@property
	def isbiotic(self):
		return (True)
	
	@property
	def methylationrate(self):
		cdict={}
		try:
			cdict["chem_divalent_mercury"]=0.0
		except:
			cdict["chem_divalent_mercury"]=nan
		
		return cdict

	@property
	def chemical_methylationrate(self):
		return self.methylationrate[self.currentchemical.name]
	@property
	def gilleliminationrate(self):
		cdict={}
		return cdict

	@property
	def chemical_gilleliminationrate(self):
		return self.gilleliminationrate[self.currentchemical.name]
	@property
	def eliminationrateconstant(self):
		cdict={}
		try:
			cdict["chem_divalent_mercury"]=self.chemical_howmuchfasterhgeliminationisthanformhg * exp(0.066*linkedCompartmentvalue(self.containingvolumeelement,self.comp_objects_dict,"surface_water","watertemperature_c") - 0.20 * log(1000.0*self.bw) - 5.83)
		except:
			cdict["chem_divalent_mercury"]=nan
		
		try:
			cdict["chem_elemental_mercury"]=self.chemical_howmuchfasterhgeliminationisthanformhg * exp(0.066*linkedCompartmentvalue(self.containingvolumeelement,self.comp_objects_dict,"surface_water","watertemperature_c") - 0.20 * log(1000.0*self.bw) -5.83)
		except:
			cdict["chem_elemental_mercury"]=nan
		
		try:
			cdict["chem_methylmercury"]=self.chemical_howmuchfasterhgeliminationisthanformhg * exp(0.066*linkedCompartmentvalue(self.containingvolumeelement,self.comp_objects_dict,"surface_water","watertemperature_c") - 0.20 * log(1000.0*self.bw) -5.83)
		except:
			cdict["chem_methylmercury"]=nan
		
		return cdict

	@property
	def chemical_eliminationrateconstant(self):
		return self.eliminationrateconstant[self.currentchemical.name]
	@property
	def gamma_fish(self):
		cdict={}
		return cdict

	@property
	def chemical_gamma_fish(self):
		return self.gamma_fish[self.currentchemical.name]
	@property
	def absorptionrateconstant(self):
		cdict={}
		return cdict

	@property
	def chemical_absorptionrateconstant(self):
		return self.absorptionrateconstant[self.currentchemical.name]
	@property
	def category(self):
		return ("fish | water column carnivore")
	
	_fractiondietfishbenthicomnivore=0.01
	@property
	def fractiondietfishbenthicomnivore(self):
		return self._fractiondietfishbenthicomnivore
	@fractiondietfishbenthicomnivore.setter
	def fractiondietfishbenthicomnivore(self,value):
		self._fractiondietfishbenthicomnivore=value

	_fractiondietfishomnivore=0.01
	@property
	def fractiondietfishomnivore(self):
		return self._fractiondietfishomnivore
	@fractiondietfishomnivore.setter
	def fractiondietfishomnivore(self,value):
		self._fractiondietfishomnivore=value

	@property
	def concentrationoutputunits(self):
		return ("mg/kg wet weight")
	
	@property
	def fishchemicaluptakerateviagill(self):
		cdict={}
		return cdict

	@property
	def chemical_fishchemicaluptakerateviagill(self):
		return self.fishchemicaluptakerateviagill[self.currentchemical.name]
	@property
	def numberoffishpersquaremeter(self):
		return (self.biomassperarea_kg_m2/self.bw)
	
	_biomassperarea_kg_m2=0.01
	@property
	def biomassperarea_kg_m2(self):
		return self._biomassperarea_kg_m2
	@biomassperarea_kg_m2.setter
	def biomassperarea_kg_m2(self,value):
		self._biomassperarea_kg_m2=value

	@property
	def howmuchfasterhgeliminationisthanformhg(self):
		cdict={}
		try:
			cdict["chem_divalent_mercury"]=3.0
		except:
			cdict["chem_divalent_mercury"]=nan
		
		try:
			cdict["chem_elemental_mercury"]=3.0
		except:
			cdict["chem_elemental_mercury"]=nan
		
		try:
			cdict["chem_methylmercury"]=1.0
		except:
			cdict["chem_methylmercury"]=nan
		
		return cdict

	@property
	def chemical_howmuchfasterhgeliminationisthanformhg(self):
		return self.howmuchfasterhgeliminationisthanformhg[self.currentchemical.name]
	_concentrationoutputfactor=1000.0
	@property
	def concentrationoutputfactor(self):
		return self._concentrationoutputfactor
	@concentrationoutputfactor.setter
	def concentrationoutputfactor(self,value):
		self._concentrationoutputfactor=value

	_fractiondietzooplankton=0.01
	@property
	def fractiondietzooplankton(self):
		return self._fractiondietzooplankton
	@fractiondietzooplankton.setter
	def fractiondietzooplankton(self,value):
		self._fractiondietzooplankton=value

	@property
	def oxidationrate(self):
		cdict={}
		try:
			cdict["chem_elemental_mercury"]=1000000.0
		except:
			cdict["chem_elemental_mercury"]=nan
		
		return cdict

	@property
	def chemical_oxidationrate(self):
		return self.oxidationrate[self.currentchemical.name]
	@property
	def demethylationrate(self):
		cdict={}
		try:
			cdict["chem_methylmercury"]=0.0
		except:
			cdict["chem_methylmercury"]=nan
		
		return cdict

	@property
	def chemical_demethylationrate(self):
		return self.demethylationrate[self.currentchemical.name]
	@property
	def chemicaltransferefficiencyinfish(self):
		cdict={}
		return cdict

	@property
	def chemical_chemicaltransferefficiencyinfish(self):
		return self.chemicaltransferefficiencyinfish[self.currentchemical.name]
	_fractiondietalgae=0.01
	@property
	def fractiondietalgae(self):
		return self._fractiondietalgae
	@fractiondietalgae.setter
	def fractiondietalgae(self,value):
		self._fractiondietalgae=value

	@property
	def populationsize(self):
		return (self.numberoffishpersquaremeter * self.containingvolumeelement.area)
	
	@property
	def totalmass(self):
		return (self.populationsize  * self.bw)
	
	_fractiondietbenthicinvertebrate=0.01
	@property
	def fractiondietbenthicinvertebrate(self):
		return self._fractiondietbenthicinvertebrate
	@fractiondietbenthicinvertebrate.setter
	def fractiondietbenthicinvertebrate(self,value):
		self._fractiondietbenthicinvertebrate=value

	_fractiondietfishherbivore=0.01
	@property
	def fractiondietfishherbivore(self):
		return self._fractiondietfishherbivore
	@fractiondietfishherbivore.setter
	def fractiondietfishherbivore(self,value):
		self._fractiondietfishherbivore=value

class water_column_herbivore:
	def __init__(self,constants,containingscenario,currentchemical,containingvolumeelement,comp_objects_dict):
		self.containingscenario=containingscenario
		self.currentchemical=currentchemical
		self.constants=constants
		self.containingvolumeelement=containingvolumeelement
		self.comp_objects_dict=comp_objects_dict
	@property
	def generaldegradationrate(self):
		cdict={}
		return cdict

	@property
	def chemical_generaldegradationrate(self):
		return self.generaldegradationrate[self.currentchemical.name]
	@property
	def initialconcentration_g_per_kg_usersupplied(self):
		cdict={}
		try:
			cdict["chem_divalent_mercury"]=0.0
		except:
			cdict["chem_divalent_mercury"]=nan
		
		try:
			cdict["chem_elemental_mercury"]=0.0
		except:
			cdict["chem_elemental_mercury"]=nan
		
		try:
			cdict["chem_methylmercury"]=0.0
		except:
			cdict["chem_methylmercury"]=nan
		
		return cdict

	@property
	def chemical_initialconcentration_g_per_kg_usersupplied(self):
		return self.initialconcentration_g_per_kg_usersupplied[self.currentchemical.name]
	@property
	def assimilationefficiencyfromfood(self):
		cdict={}
		try:
			cdict["chem_divalent_mercury"]=0.06
		except:
			cdict["chem_divalent_mercury"]=nan
		
		try:
			cdict["chem_elemental_mercury"]=0.06
		except:
			cdict["chem_elemental_mercury"]=nan
		
		try:
			cdict["chem_methylmercury"]=0.5
		except:
			cdict["chem_methylmercury"]=nan
		
		return cdict

	@property
	def chemical_assimilationefficiencyfromfood(self):
		return self.assimilationefficiencyfromfood[self.currentchemical.name]
	@property
	def acceptableabiotic(self):
		return ("abiotic | surface water | surface water - default")
	
	@property
	def assimilationefficiencyfromplants(self):
		cdict={}
		try:
			cdict["chem_divalent_mercury"]=1.0
		except:
			cdict["chem_divalent_mercury"]=nan
		
		try:
			cdict["chem_elemental_mercury"]=1.0
		except:
			cdict["chem_elemental_mercury"]=nan
		
		try:
			cdict["chem_methylmercury"]=1.0
		except:
			cdict["chem_methylmercury"]=nan
		
		return cdict

	@property
	def chemical_assimilationefficiencyfromplants(self):
		return self.assimilationefficiencyfromplants[self.currentchemical.name]
	_fractiondietmacrophyte=0.01
	@property
	def fractiondietmacrophyte(self):
		return self._fractiondietmacrophyte
	@fractiondietmacrophyte.setter
	def fractiondietmacrophyte(self,value):
		self._fractiondietmacrophyte=value

	@property
	def foodingestionrate(self):
		return (self.feedingrate/self.bw)
	
	@property
	def reductionrate(self):
		cdict={}
		try:
			cdict["chem_divalent_mercury"]=0.0
		except:
			cdict["chem_divalent_mercury"]=nan
		
		return cdict

	@property
	def chemical_reductionrate(self):
		return self.reductionrate[self.currentchemical.name]
	_fishlipidfraction=0.034
	@property
	def fishlipidfraction(self):
		return self._fishlipidfraction
	@fishlipidfraction.setter
	def fishlipidfraction(self,value):
		self._fishlipidfraction=value

	@property
	def image(self):
		return ("c:\models\trim\data\images\bluegill.gif")
	
	_bw=0.025
	@property
	def bw(self):
		return self._bw
	@bw.setter
	def bw(self,value):
		self._bw=value

	@property
	def halflife(self):
		cdict={}
		return cdict

	@property
	def chemical_halflife(self):
		return self.halflife[self.currentchemical.name]
	@property
	def feedingrate(self):
		return (0.022 * self.bw ** (0.85) * exp(0.06 * linkedCompartmentvalue(self.containingvolumeelement,self.comp_objects_dict,"surface_water","watertemperature_c")))
	
	@property
	def initialconcentration_g_per_kg(self):
		cdict={}
		try:
			cdict["chem_divalent_mercury"]=self.containingscenario.fractioninitialconcentrations * self.chemical_initialconcentration_g_per_kg_usersupplied
		except:
			cdict["chem_divalent_mercury"]=nan
		
		try:
			cdict["chem_elemental_mercury"]=self.containingscenario.fractioninitialconcentrations * self.chemical_initialconcentration_g_per_kg_usersupplied
		except:
			cdict["chem_elemental_mercury"]=nan
		
		try:
			cdict["chem_methylmercury"]=self.containingscenario.fractioninitialconcentrations * self.chemical_initialconcentration_g_per_kg_usersupplied
		except:
			cdict["chem_methylmercury"]=nan
		
		return cdict

	@property
	def chemical_initialconcentration_g_per_kg(self):
		return self.initialconcentration_g_per_kg[self.currentchemical.name]
	@property
	def isbiotic(self):
		return (True)
	
	@property
	def assimilationefficiencyfromplankton(self):
		cdict={}
		try:
			cdict["chem_divalent_mercury"]=0.06
		except:
			cdict["chem_divalent_mercury"]=nan
		
		try:
			cdict["chem_elemental_mercury"]=0.06
		except:
			cdict["chem_elemental_mercury"]=nan
		
		try:
			cdict["chem_methylmercury"]=0.5
		except:
			cdict["chem_methylmercury"]=nan
		
		return cdict

	@property
	def chemical_assimilationefficiencyfromplankton(self):
		return self.assimilationefficiencyfromplankton[self.currentchemical.name]
	@property
	def methylationrate(self):
		cdict={}
		try:
			cdict["chem_divalent_mercury"]=0.0
		except:
			cdict["chem_divalent_mercury"]=nan
		
		return cdict

	@property
	def chemical_methylationrate(self):
		return self.methylationrate[self.currentchemical.name]
	@property
	def gilleliminationrate(self):
		cdict={}
		return cdict

	@property
	def chemical_gilleliminationrate(self):
		return self.gilleliminationrate[self.currentchemical.name]
	@property
	def eliminationrateconstant(self):
		cdict={}
		try:
			cdict["chem_divalent_mercury"]=self.chemical_howmuchfasterhgeliminationisthanformhg * exp(0.066*linkedCompartmentvalue(self.containingvolumeelement,self.comp_objects_dict,"surface_water","watertemperature_c") - 0.20 * log(1000.0*self.bw)/log(exp(1.0)) -5.83)
		except:
			cdict["chem_divalent_mercury"]=nan
		
		try:
			cdict["chem_elemental_mercury"]=self.chemical_howmuchfasterhgeliminationisthanformhg * exp(0.066*linkedCompartmentvalue(self.containingvolumeelement,self.comp_objects_dict,"surface_water","watertemperature_c") - 0.20 * log(1000.0*self.bw)/log(exp(1.0)) -5.83)
		except:
			cdict["chem_elemental_mercury"]=nan
		
		try:
			cdict["chem_methylmercury"]=self.chemical_howmuchfasterhgeliminationisthanformhg * exp(0.066*linkedCompartmentvalue(self.containingvolumeelement,self.comp_objects_dict,"surface_water","watertemperature_c") - 0.20 * log(1000.0*self.bw)/log(exp(1.0)) -5.83)
		except:
			cdict["chem_methylmercury"]=nan
		
		return cdict

	@property
	def chemical_eliminationrateconstant(self):
		return self.eliminationrateconstant[self.currentchemical.name]
	@property
	def gamma_fish(self):
		cdict={}
		return cdict

	@property
	def chemical_gamma_fish(self):
		return self.gamma_fish[self.currentchemical.name]
	@property
	def absorptionrateconstant(self):
		cdict={}
		return cdict

	@property
	def chemical_absorptionrateconstant(self):
		return self.absorptionrateconstant[self.currentchemical.name]
	@property
	def category(self):
		return ("fish | water column herbivore")
	
	@property
	def concentrationoutputunits(self):
		return ("mg/kg wet weight")
	
	@property
	def fishchemicaluptakerateviagill(self):
		cdict={}
		return cdict

	@property
	def chemical_fishchemicaluptakerateviagill(self):
		return self.fishchemicaluptakerateviagill[self.currentchemical.name]
	@property
	def numberoffishpersquaremeter(self):
		return (self.biomassperarea_kg_m2/self.bw)
	
	_biomassperarea_kg_m2=0.01
	@property
	def biomassperarea_kg_m2(self):
		return self._biomassperarea_kg_m2
	@biomassperarea_kg_m2.setter
	def biomassperarea_kg_m2(self,value):
		self._biomassperarea_kg_m2=value

	@property
	def howmuchfasterhgeliminationisthanformhg(self):
		cdict={}
		try:
			cdict["chem_divalent_mercury"]=3.0
		except:
			cdict["chem_divalent_mercury"]=nan
		
		try:
			cdict["chem_elemental_mercury"]=3.0
		except:
			cdict["chem_elemental_mercury"]=nan
		
		try:
			cdict["chem_methylmercury"]=1.0
		except:
			cdict["chem_methylmercury"]=nan
		
		return cdict

	@property
	def chemical_howmuchfasterhgeliminationisthanformhg(self):
		return self.howmuchfasterhgeliminationisthanformhg[self.currentchemical.name]
	_concentrationoutputfactor=1000.0
	@property
	def concentrationoutputfactor(self):
		return self._concentrationoutputfactor
	@concentrationoutputfactor.setter
	def concentrationoutputfactor(self,value):
		self._concentrationoutputfactor=value

	_fractiondietzooplankton=0.01
	@property
	def fractiondietzooplankton(self):
		return self._fractiondietzooplankton
	@fractiondietzooplankton.setter
	def fractiondietzooplankton(self,value):
		self._fractiondietzooplankton=value

	@property
	def oxidationrate(self):
		cdict={}
		try:
			cdict["chem_elemental_mercury"]=1000000.0
		except:
			cdict["chem_elemental_mercury"]=nan
		
		return cdict

	@property
	def chemical_oxidationrate(self):
		return self.oxidationrate[self.currentchemical.name]
	@property
	def demethylationrate(self):
		cdict={}
		try:
			cdict["chem_methylmercury"]=0.0
		except:
			cdict["chem_methylmercury"]=nan
		
		return cdict

	@property
	def chemical_demethylationrate(self):
		return self.demethylationrate[self.currentchemical.name]
	@property
	def chemicaltransferefficiencyinfish(self):
		cdict={}
		return cdict

	@property
	def chemical_chemicaltransferefficiencyinfish(self):
		return self.chemicaltransferefficiencyinfish[self.currentchemical.name]
	_fractiondietalgae=0.01
	@property
	def fractiondietalgae(self):
		return self._fractiondietalgae
	@fractiondietalgae.setter
	def fractiondietalgae(self,value):
		self._fractiondietalgae=value

	@property
	def populationsize(self):
		return (self.numberoffishpersquaremeter * self.containingvolumeelement.area)
	
	@property
	def totalmass(self):
		return (self.populationsize  * self.bw)
	
	_fractiondietbenthicinvertebrate=0.01
	@property
	def fractiondietbenthicinvertebrate(self):
		return self._fractiondietbenthicinvertebrate
	@fractiondietbenthicinvertebrate.setter
	def fractiondietbenthicinvertebrate(self,value):
		self._fractiondietbenthicinvertebrate=value

class water_column_omnivore:
	def __init__(self,constants,containingscenario,currentchemical,containingvolumeelement,comp_objects_dict):
		self.containingscenario=containingscenario
		self.currentchemical=currentchemical
		self.constants=constants
		self.containingvolumeelement=containingvolumeelement
		self.comp_objects_dict=comp_objects_dict
	@property
	def generaldegradationrate(self):
		cdict={}
		return cdict

	@property
	def chemical_generaldegradationrate(self):
		return self.generaldegradationrate[self.currentchemical.name]
	@property
	def initialconcentration_g_per_kg_usersupplied(self):
		cdict={}
		try:
			cdict["chem_divalent_mercury"]=0.0
		except:
			cdict["chem_divalent_mercury"]=nan
		
		try:
			cdict["chem_elemental_mercury"]=0.0
		except:
			cdict["chem_elemental_mercury"]=nan
		
		try:
			cdict["chem_methylmercury"]=0.0
		except:
			cdict["chem_methylmercury"]=nan
		
		return cdict

	@property
	def chemical_initialconcentration_g_per_kg_usersupplied(self):
		return self.initialconcentration_g_per_kg_usersupplied[self.currentchemical.name]
	@property
	def assimilationefficiencyfromfood(self):
		cdict={}
		try:
			cdict["chem_divalent_mercury"]=0.06
		except:
			cdict["chem_divalent_mercury"]=nan
		
		try:
			cdict["chem_elemental_mercury"]=0.06
		except:
			cdict["chem_elemental_mercury"]=nan
		
		try:
			cdict["chem_methylmercury"]=0.5
		except:
			cdict["chem_methylmercury"]=nan
		
		return cdict

	@property
	def chemical_assimilationefficiencyfromfood(self):
		return self.assimilationefficiencyfromfood[self.currentchemical.name]
	@property
	def acceptableabiotic(self):
		return ("abiotic | surface water | surface water - default")
	
	@property
	def assimilationefficiencyfromplants(self):
		cdict={}
		try:
			cdict["chem_divalent_mercury"]=1.0
		except:
			cdict["chem_divalent_mercury"]=nan
		
		try:
			cdict["chem_elemental_mercury"]=1.0
		except:
			cdict["chem_elemental_mercury"]=nan
		
		try:
			cdict["chem_methylmercury"]=1.0
		except:
			cdict["chem_methylmercury"]=nan
		
		return cdict

	@property
	def chemical_assimilationefficiencyfromplants(self):
		return self.assimilationefficiencyfromplants[self.currentchemical.name]
	_fractiondietmacrophyte=0.01
	@property
	def fractiondietmacrophyte(self):
		return self._fractiondietmacrophyte
	@fractiondietmacrophyte.setter
	def fractiondietmacrophyte(self,value):
		self._fractiondietmacrophyte=value

	@property
	def foodingestionrate(self):
		return (self.feedingrate/self.bw)
	
	@property
	def reductionrate(self):
		cdict={}
		try:
			cdict["chem_divalent_mercury"]=0.0
		except:
			cdict["chem_divalent_mercury"]=nan
		
		return cdict

	@property
	def chemical_reductionrate(self):
		return self.reductionrate[self.currentchemical.name]
	_fishlipidfraction=0.07
	@property
	def fishlipidfraction(self):
		return self._fishlipidfraction
	@fishlipidfraction.setter
	def fishlipidfraction(self,value):
		self._fishlipidfraction=value

	@property
	def image(self):
		return ("c:\models\trim\data\images\catfish.gif")
	
	_bw=0.25
	@property
	def bw(self):
		return self._bw
	@bw.setter
	def bw(self,value):
		self._bw=value

	@property
	def halflife(self):
		cdict={}
		return cdict

	@property
	def chemical_halflife(self):
		return self.halflife[self.currentchemical.name]
	_fractiondietfishbenthiccarnivore=0.01
	@property
	def fractiondietfishbenthiccarnivore(self):
		return self._fractiondietfishbenthiccarnivore
	@fractiondietfishbenthiccarnivore.setter
	def fractiondietfishbenthiccarnivore(self,value):
		self._fractiondietfishbenthiccarnivore=value

	@property
	def feedingrate(self):
		return (0.022 * self.bw ** (0.85) * exp(0.06 * linkedCompartmentvalue(self.containingvolumeelement,self.comp_objects_dict,"surface_water","watertemperature_c")))
	
	@property
	def initialconcentration_g_per_kg(self):
		cdict={}
		try:
			cdict["chem_divalent_mercury"]=self.containingscenario.fractioninitialconcentrations * self.chemical_initialconcentration_g_per_kg_usersupplied
		except:
			cdict["chem_divalent_mercury"]=nan
		
		try:
			cdict["chem_elemental_mercury"]=self.containingscenario.fractioninitialconcentrations * self.chemical_initialconcentration_g_per_kg_usersupplied
		except:
			cdict["chem_elemental_mercury"]=nan
		
		try:
			cdict["chem_methylmercury"]=self.containingscenario.fractioninitialconcentrations * self.chemical_initialconcentration_g_per_kg_usersupplied
		except:
			cdict["chem_methylmercury"]=nan
		
		return cdict

	@property
	def chemical_initialconcentration_g_per_kg(self):
		return self.initialconcentration_g_per_kg[self.currentchemical.name]
	@property
	def isbiotic(self):
		return (True)
	
	@property
	def methylationrate(self):
		cdict={}
		try:
			cdict["chem_divalent_mercury"]=0.0
		except:
			cdict["chem_divalent_mercury"]=nan
		
		return cdict

	@property
	def chemical_methylationrate(self):
		return self.methylationrate[self.currentchemical.name]
	@property
	def gilleliminationrate(self):
		cdict={}
		return cdict

	@property
	def chemical_gilleliminationrate(self):
		return self.gilleliminationrate[self.currentchemical.name]
	@property
	def eliminationrateconstant(self):
		cdict={}
		try:
			cdict["chem_divalent_mercury"]=self.chemical_howmuchfasterhgeliminationisthanformhg * exp(0.066*linkedCompartmentvalue(self.containingvolumeelement,self.comp_objects_dict,"surface_water","watertemperature_c") - 0.20 * log(1000.0*self.bw)/log(exp(1.0)) -5.83)
		except:
			cdict["chem_divalent_mercury"]=nan
		
		try:
			cdict["chem_elemental_mercury"]=self.chemical_howmuchfasterhgeliminationisthanformhg * exp(0.066*linkedCompartmentvalue(self.containingvolumeelement,self.comp_objects_dict,"surface_water","watertemperature_c") - 0.20 * log(1000.0*self.bw)/log(exp(1.0)) -5.83)
		except:
			cdict["chem_elemental_mercury"]=nan
		
		try:
			cdict["chem_methylmercury"]=self.chemical_howmuchfasterhgeliminationisthanformhg * exp(0.066*linkedCompartmentvalue(self.containingvolumeelement,self.comp_objects_dict,"surface_water","watertemperature_c") - 0.20 * log(1000.0*self.bw)/log(exp(1.0)) -5.83)
		except:
			cdict["chem_methylmercury"]=nan
		
		return cdict

	@property
	def chemical_eliminationrateconstant(self):
		return self.eliminationrateconstant[self.currentchemical.name]
	@property
	def gamma_fish(self):
		cdict={}
		return cdict

	@property
	def chemical_gamma_fish(self):
		return self.gamma_fish[self.currentchemical.name]
	@property
	def absorptionrateconstant(self):
		cdict={}
		return cdict

	@property
	def chemical_absorptionrateconstant(self):
		return self.absorptionrateconstant[self.currentchemical.name]
	@property
	def category(self):
		return ("fish | water column omnivore")
	
	_fractiondietfishbenthicomnivore=0.01
	@property
	def fractiondietfishbenthicomnivore(self):
		return self._fractiondietfishbenthicomnivore
	@fractiondietfishbenthicomnivore.setter
	def fractiondietfishbenthicomnivore(self,value):
		self._fractiondietfishbenthicomnivore=value

	_fractiondietfishomnivore=0.01
	@property
	def fractiondietfishomnivore(self):
		return self._fractiondietfishomnivore
	@fractiondietfishomnivore.setter
	def fractiondietfishomnivore(self,value):
		self._fractiondietfishomnivore=value

	@property
	def concentrationoutputunits(self):
		return ("mg/kg wet weight")
	
	@property
	def fishchemicaluptakerateviagill(self):
		cdict={}
		return cdict

	@property
	def chemical_fishchemicaluptakerateviagill(self):
		return self.fishchemicaluptakerateviagill[self.currentchemical.name]
	@property
	def numberoffishpersquaremeter(self):
		return (self.biomassperarea_kg_m2/self.bw)
	
	_biomassperarea_kg_m2=0.01
	@property
	def biomassperarea_kg_m2(self):
		return self._biomassperarea_kg_m2
	@biomassperarea_kg_m2.setter
	def biomassperarea_kg_m2(self,value):
		self._biomassperarea_kg_m2=value

	@property
	def howmuchfasterhgeliminationisthanformhg(self):
		cdict={}
		try:
			cdict["chem_divalent_mercury"]=3.0
		except:
			cdict["chem_divalent_mercury"]=nan
		
		try:
			cdict["chem_elemental_mercury"]=3.0
		except:
			cdict["chem_elemental_mercury"]=nan
		
		try:
			cdict["chem_methylmercury"]=1.0
		except:
			cdict["chem_methylmercury"]=nan
		
		return cdict

	@property
	def chemical_howmuchfasterhgeliminationisthanformhg(self):
		return self.howmuchfasterhgeliminationisthanformhg[self.currentchemical.name]
	_concentrationoutputfactor=1000.0
	@property
	def concentrationoutputfactor(self):
		return self._concentrationoutputfactor
	@concentrationoutputfactor.setter
	def concentrationoutputfactor(self,value):
		self._concentrationoutputfactor=value

	_fractiondietzooplankton=0.01
	@property
	def fractiondietzooplankton(self):
		return self._fractiondietzooplankton
	@fractiondietzooplankton.setter
	def fractiondietzooplankton(self,value):
		self._fractiondietzooplankton=value

	@property
	def oxidationrate(self):
		cdict={}
		try:
			cdict["chem_elemental_mercury"]=1000000.0
		except:
			cdict["chem_elemental_mercury"]=nan
		
		return cdict

	@property
	def chemical_oxidationrate(self):
		return self.oxidationrate[self.currentchemical.name]
	@property
	def demethylationrate(self):
		cdict={}
		try:
			cdict["chem_methylmercury"]=0.0
		except:
			cdict["chem_methylmercury"]=nan
		
		return cdict

	@property
	def chemical_demethylationrate(self):
		return self.demethylationrate[self.currentchemical.name]
	_fractiondietfishcarnivore=0.01
	@property
	def fractiondietfishcarnivore(self):
		return self._fractiondietfishcarnivore
	@fractiondietfishcarnivore.setter
	def fractiondietfishcarnivore(self,value):
		self._fractiondietfishcarnivore=value

	@property
	def chemicaltransferefficiencyinfish(self):
		cdict={}
		return cdict

	@property
	def chemical_chemicaltransferefficiencyinfish(self):
		return self.chemicaltransferefficiencyinfish[self.currentchemical.name]
	_fractiondietalgae=0.01
	@property
	def fractiondietalgae(self):
		return self._fractiondietalgae
	@fractiondietalgae.setter
	def fractiondietalgae(self,value):
		self._fractiondietalgae=value

	@property
	def populationsize(self):
		return (self.numberoffishpersquaremeter * self.containingvolumeelement.area)
	
	@property
	def totalmass(self):
		return (self.populationsize  * self.bw)
	
	_fractiondietbenthicinvertebrate=0.01
	@property
	def fractiondietbenthicinvertebrate(self):
		return self._fractiondietbenthicinvertebrate
	@fractiondietbenthicinvertebrate.setter
	def fractiondietbenthicinvertebrate(self,value):
		self._fractiondietbenthicinvertebrate=value

	_fractiondietfishherbivore=0.01
	@property
	def fractiondietfishherbivore(self):
		return self._fractiondietfishherbivore
	@fractiondietfishherbivore.setter
	def fractiondietfishherbivore(self,value):
		self._fractiondietfishherbivore=value

class zooplankton:
	def __init__(self,constants,containingscenario,currentchemical,containingvolumeelement,comp_objects_dict):
		self.containingscenario=containingscenario
		self.currentchemical=currentchemical
		self.constants=constants
		self.containingvolumeelement=containingvolumeelement
		self.comp_objects_dict=comp_objects_dict
	@property
	def generaldegradationrate(self):
		cdict={}
		return cdict

	@property
	def chemical_generaldegradationrate(self):
		return self.generaldegradationrate[self.currentchemical.name]
	@property
	def initialconcentration_g_per_kg_usersupplied(self):
		cdict={}
		try:
			cdict["chem_divalent_mercury"]=0.0
		except:
			cdict["chem_divalent_mercury"]=nan
		
		try:
			cdict["chem_elemental_mercury"]=0.0
		except:
			cdict["chem_elemental_mercury"]=nan
		
		try:
			cdict["chem_methylmercury"]=0.0
		except:
			cdict["chem_methylmercury"]=nan
		
		return cdict

	@property
	def chemical_initialconcentration_g_per_kg_usersupplied(self):
		return self.initialconcentration_g_per_kg_usersupplied[self.currentchemical.name]
	@property
	def acceptableabiotic(self):
		return ("abiotic | surface water | surface water - default")
	
	_fractiondietmacrophyte=0.01
	@property
	def fractiondietmacrophyte(self):
		return self._fractiondietmacrophyte
	@fractiondietmacrophyte.setter
	def fractiondietmacrophyte(self,value):
		self._fractiondietmacrophyte=value

	@property
	def foodingestionrate(self):
		return (self.feedingrate/self.bw)
	
	@property
	def reductionrate(self):
		cdict={}
		try:
			cdict["chem_divalent_mercury"]=0.0
		except:
			cdict["chem_divalent_mercury"]=nan
		
		return cdict

	@property
	def chemical_reductionrate(self):
		return self.reductionrate[self.currentchemical.name]
	_bw=5.7e-8
	@property
	def bw(self):
		return self._bw
	@bw.setter
	def bw(self,value):
		self._bw=value

	@property
	def halflife(self):
		cdict={}
		try:
			cdict["chem_divalent_mercury"]=1.0e9
		except:
			cdict["chem_divalent_mercury"]=nan
		
		try:
			cdict["chem_elemental_mercury"]=1.0e9
		except:
			cdict["chem_elemental_mercury"]=nan
		
		try:
			cdict["chem_methylmercury"]=1.0e9
		except:
			cdict["chem_methylmercury"]=nan
		
		return cdict

	@property
	def chemical_halflife(self):
		return self.halflife[self.currentchemical.name]
	@property
	def feedingrate(self):
		return (0.022 * self.bw ** (0.85) * exp(0.06 * linkedCompartmentvalue(self.containingvolumeelement,self.comp_objects_dict,"surface_water","watertemperature_c")))
	
	@property
	def initialconcentration_g_per_kg(self):
		cdict={}
		try:
			cdict["chem_divalent_mercury"]=self.containingscenario.fractioninitialconcentrations * self.chemical_initialconcentration_g_per_kg_usersupplied
		except:
			cdict["chem_divalent_mercury"]=nan
		
		try:
			cdict["chem_elemental_mercury"]=self.containingscenario.fractioninitialconcentrations * self.chemical_initialconcentration_g_per_kg_usersupplied
		except:
			cdict["chem_elemental_mercury"]=nan
		
		try:
			cdict["chem_methylmercury"]=self.containingscenario.fractioninitialconcentrations * self.chemical_initialconcentration_g_per_kg_usersupplied
		except:
			cdict["chem_methylmercury"]=nan
		
		return cdict

	@property
	def chemical_initialconcentration_g_per_kg(self):
		return self.initialconcentration_g_per_kg[self.currentchemical.name]
	@property
	def isbiotic(self):
		return (True)
	
	@property
	def methylationrate(self):
		cdict={}
		try:
			cdict["chem_divalent_mercury"]=0.0
		except:
			cdict["chem_divalent_mercury"]=nan
		
		return cdict

	@property
	def chemical_methylationrate(self):
		return self.methylationrate[self.currentchemical.name]
	@property
	def numberofzooplanktonpersquaremeter(self):
		return (self.biomassperarea_kg_m2/self.bw)
	
	@property
	def eliminationrateconstant(self):
		cdict={}
		try:
			cdict["chem_divalent_mercury"]=self.chemical_howmuchfasterhgeliminationisthanformhg * exp(0.066*linkedCompartmentvalue(self.containingvolumeelement,self.comp_objects_dict,"surface_water","watertemperature_c") - 0.20 * log(1000.0*self.bw)/log(exp(1.0)) -5.83)
		except:
			cdict["chem_divalent_mercury"]=nan
		
		try:
			cdict["chem_elemental_mercury"]=self.chemical_howmuchfasterhgeliminationisthanformhg * exp(0.066*linkedCompartmentvalue(self.containingvolumeelement,self.comp_objects_dict,"surface_water","watertemperature_c") - 0.20 * log(1000.0*self.bw)/log(exp(1.0)) -5.83)
		except:
			cdict["chem_elemental_mercury"]=nan
		
		try:
			cdict["chem_methylmercury"]=self.chemical_howmuchfasterhgeliminationisthanformhg * exp(0.066*linkedCompartmentvalue(self.containingvolumeelement,self.comp_objects_dict,"surface_water","watertemperature_c") - 0.20 * log(1000.0*self.bw)/log(exp(1.0)) -5.83)
		except:
			cdict["chem_methylmercury"]=nan
		
		return cdict

	@property
	def chemical_eliminationrateconstant(self):
		return self.eliminationrateconstant[self.currentchemical.name]
	@property
	def absorptionrateconstant(self):
		cdict={}
		return cdict

	@property
	def chemical_absorptionrateconstant(self):
		return self.absorptionrateconstant[self.currentchemical.name]
	@property
	def category(self):
		return ("invertebrate | zooplankton")
	
	@property
	def concentrationoutputunits(self):
		return ("mg/kg wet weight")
	
	@property
	def assimilationefficiencyfromalgae(self):
		cdict={}
		try:
			cdict["chem_divalent_mercury"]=0.2
		except:
			cdict["chem_divalent_mercury"]=nan
		
		try:
			cdict["chem_elemental_mercury"]=0.015
		except:
			cdict["chem_elemental_mercury"]=nan
		
		try:
			cdict["chem_methylmercury"]=0.5
		except:
			cdict["chem_methylmercury"]=nan
		
		return cdict

	@property
	def chemical_assimilationefficiencyfromalgae(self):
		return self.assimilationefficiencyfromalgae[self.currentchemical.name]
	_biomassperarea_kg_m2=0.01
	@property
	def biomassperarea_kg_m2(self):
		return self._biomassperarea_kg_m2
	@biomassperarea_kg_m2.setter
	def biomassperarea_kg_m2(self,value):
		self._biomassperarea_kg_m2=value

	@property
	def howmuchfasterhgeliminationisthanformhg(self):
		cdict={}
		try:
			cdict["chem_divalent_mercury"]=3.0
		except:
			cdict["chem_divalent_mercury"]=nan
		
		try:
			cdict["chem_elemental_mercury"]=3.0
		except:
			cdict["chem_elemental_mercury"]=nan
		
		try:
			cdict["chem_methylmercury"]=1.0
		except:
			cdict["chem_methylmercury"]=nan
		
		return cdict

	@property
	def chemical_howmuchfasterhgeliminationisthanformhg(self):
		return self.howmuchfasterhgeliminationisthanformhg[self.currentchemical.name]
	_concentrationoutputfactor=1000.0
	@property
	def concentrationoutputfactor(self):
		return self._concentrationoutputfactor
	@concentrationoutputfactor.setter
	def concentrationoutputfactor(self,value):
		self._concentrationoutputfactor=value

	@property
	def oxidationrate(self):
		cdict={}
		try:
			cdict["chem_elemental_mercury"]=1000000.0
		except:
			cdict["chem_elemental_mercury"]=nan
		
		return cdict

	@property
	def chemical_oxidationrate(self):
		return self.oxidationrate[self.currentchemical.name]
	@property
	def demethylationrate(self):
		cdict={}
		try:
			cdict["chem_methylmercury"]=0.0
		except:
			cdict["chem_methylmercury"]=nan
		
		return cdict

	@property
	def chemical_demethylationrate(self):
		return self.demethylationrate[self.currentchemical.name]
	_zooplanktonlipidfraction=0.012
	@property
	def zooplanktonlipidfraction(self):
		return self._zooplanktonlipidfraction
	@zooplanktonlipidfraction.setter
	def zooplanktonlipidfraction(self,value):
		self._zooplanktonlipidfraction=value

	_fractiondietalgae=0.01
	@property
	def fractiondietalgae(self):
		return self._fractiondietalgae
	@fractiondietalgae.setter
	def fractiondietalgae(self,value):
		self._fractiondietalgae=value

	@property
	def populationsize(self):
		return (self.numberofzooplanktonpersquaremeter * self.containingvolumeelement.area)
	
	@property
	def totalmass(self):
		return (self.populationsize  * self.bw)
	
	_fractiondietbenthicinvertebrate=0.01
	@property
	def fractiondietbenthicinvertebrate(self):
		return self._fractiondietbenthicinvertebrate
	@fractiondietbenthicinvertebrate.setter
	def fractiondietbenthicinvertebrate(self,value):
		self._fractiondietbenthicinvertebrate=value
