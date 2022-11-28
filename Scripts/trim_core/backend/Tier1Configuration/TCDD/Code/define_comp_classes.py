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
    
wt_av_rain=0.004106108729329538
wt_av_airtemperature=298.0
wt_av_horizontalwindspeed=2.8
wt_av_winddirection=167.15026840076376
wt_av_mixingheight=865.0
wt_av_isday=1.0
wt_av_cumulativerain=0.0
frac_time_rain=0.4286126022264654
wt_av_allowexchange=0.6653047470620446
frac_time_exchange_no_rain=0.310192023633678
frac_time_exchange_rain=0.23258997730302267
frac_time_exchange_day=0.5427820009367007
frac_time_exchange_not_day=0.0
wt_av_litterfallrate=0.01192360404969274


class advection_sink:
	def __init__(self,constants,containingscenario,currentchemical,containingvolumeelement,comp_objects_dict):
		self.containingscenario=containingscenario
		self.currentchemical=currentchemical
		self.constants=constants
		self.containingvolumeelement=containingvolumeelement
		self.comp_objects_dict=comp_objects_dict
	@property
	def concentrationoutputunits(self):
		return ("0.01")
	
	_concentrationoutputfactor=1.0
	@property
	def concentrationoutputfactor(self):
		return self._concentrationoutputfactor
	@concentrationoutputfactor.setter
	def concentrationoutputfactor(self,value):
		self._concentrationoutputfactor=value

	@property
	def acceptableabiotic(self):
		return ("nan")
	
	_isbiotic=False
	@property
	def isbiotic(self):
		return self._isbiotic
	@isbiotic.setter
	def isbiotic(self,value):
		self._isbiotic=value

class air:
	def __init__(self,constants,containingscenario,currentchemical,containingvolumeelement,comp_objects_dict):
		self.containingscenario=containingscenario
		self.currentchemical=currentchemical
		self.constants=constants
		self.containingvolumeelement=containingvolumeelement
		self.comp_objects_dict=comp_objects_dict
	@property
	def dynamicairviscosity_m2_per_sec(self):
		return (self.dynamicairviscosity_cm2_per_sec/1e4)
	
	@property
	def acceptableabiotic(self):
		return ("nan")
	

	@property
	def demethylationrate(self):
		cdict={}
		return cdict

	@property
	def chemical_demethylationrate(self):
		return self.demethylationrate[self.currentchemical.name]

	@property
	def chemical_demethylationrate(self):
		return self.demethylationrate[self.currentchemical.name]

	_fractionorganicmatteronparticulates=0.2
	@property
	def fractionorganicmatteronparticulates(self):
		return self._fractionorganicmatteronparticulates
	@fractionorganicmatteronparticulates.setter
	def fractionorganicmatteronparticulates(self,value):
		self._fractionorganicmatteronparticulates=value

	_airdensity_g_cm3=0.0012
	@property
	def airdensity_g_cm3(self):
		return self._airdensity_g_cm3
	@airdensity_g_cm3.setter
	def airdensity_g_cm3(self,value):
		self._airdensity_g_cm3=value


	@property
	def fractionmass_vapor(self):
		cdict={}
		try:
			cdict["chem_2_3_7_8_tcdd"]=1 -self.chemical_fractionmass_sorbed
		except:
			cdict["chem_2_3_7_8_tcdd"]=nan
		
		return cdict

	@property
	def chemical_fractionmass_vapor(self):
		return self.fractionmass_vapor[self.currentchemical.name]

	@property
	def chemical_fractionmass_vapor(self):
		return self.fractionmass_vapor[self.currentchemical.name]

	@property
	def volumetricairparticlecontent(self):
		return (self.dustload / self.dustdensity)
	

	@property
	def particlevolumetricdrydepositionrate(self):
		cdict={}
		try:
			cdict["chem_2_3_7_8_tcdd"]=self.chemical_vdep * (self.dustload / self.dustdensity)
		except:
			cdict["chem_2_3_7_8_tcdd"]=nan
		
		return cdict

	@property
	def chemical_particlevolumetricdrydepositionrate(self):
		return self.particlevolumetricdrydepositionrate[self.currentchemical.name]

	@property
	def chemical_particlevolumetricdrydepositionrate(self):
		return self.particlevolumetricdrydepositionrate[self.currentchemical.name]

	@property
	def volumefraction_vapor(self):
		return (self.volumetricairaircontent)
	

	@property
	def reductionrate(self):
		cdict={}
		return cdict

	@property
	def chemical_reductionrate(self):
		return self.reductionrate[self.currentchemical.name]

	@property
	def chemical_reductionrate(self):
		return self.reductionrate[self.currentchemical.name]


	@property
	def z_solid(self):
		cdict={}
		try:
			cdict["chem_2_3_7_8_tcdd"]=self.chemical_z_vapor * (self.chemical_fractionmass_sorbed/self.volumetricairparticlecontent)/(self.chemical_fractionmass_vapor/self.volumetricairaircontent)
		except:
			cdict["chem_2_3_7_8_tcdd"]=nan
		
		return cdict

	@property
	def chemical_z_solid(self):
		return self.z_solid[self.currentchemical.name]

	@property
	def chemical_z_solid(self):
		return self.z_solid[self.currentchemical.name]

	@property
	def dynamicairviscosity_cm2_per_sec(self):
		return ((1.32 + 0.009 * self.airtemperature_c)/10.0)
	

	@property
	def initialconcentration_g_per_m3(self):
		cdict={}
		try:
			cdict["chem_2_3_7_8_tcdd"]=self.containingscenario.fractioninitialconcentrations * self.chemical_initialconcentration_g_per_m3_usersupplied
		except:
			cdict["chem_2_3_7_8_tcdd"]=nan
		
		return cdict

	@property
	def chemical_initialconcentration_g_per_m3(self):
		return self.initialconcentration_g_per_m3[self.currentchemical.name]

	@property
	def chemical_initialconcentration_g_per_m3(self):
		return self.initialconcentration_g_per_m3[self.currentchemical.name]


	@property
	def z_liquid(self):
		cdict={}
		try:
			cdict["chem_2_3_7_8_tcdd"]=self.currentchemical.z_purewater
		except:
			cdict["chem_2_3_7_8_tcdd"]=nan
		
		return cdict

	@property
	def chemical_z_liquid(self):
		return self.z_liquid[self.currentchemical.name]

	@property
	def chemical_z_liquid(self):
		return self.z_liquid[self.currentchemical.name]


	@property
	def halflife(self):
		cdict={}
		try:
			cdict["chem_2_3_7_8_tcdd"]=12.0
		except:
			cdict["chem_2_3_7_8_tcdd"]=nan
		
		return cdict

	@property
	def chemical_halflife(self):
		return self.halflife[self.currentchemical.name]

	@property
	def chemical_halflife(self):
		return self.halflife[self.currentchemical.name]

	@property
	def category(self):
		return ("abiotic | air | air - default")
	

	@property
	def fractionmass_sorbed(self):
		cdict={}
		try:
			cdict["chem_2_3_7_8_tcdd"]=1 - 1/(1+self.chemical_particlegaspartitioncoefficient * self.dustload* self.constants.ug_per_kg)
		except:
			cdict["chem_2_3_7_8_tcdd"]=nan
		
		return cdict

	@property
	def chemical_fractionmass_sorbed(self):
		return self.fractionmass_sorbed[self.currentchemical.name]

	@property
	def chemical_fractionmass_sorbed(self):
		return self.fractionmass_sorbed[self.currentchemical.name]

	_concentrationoutputfactor=1000000.0
	@property
	def concentrationoutputfactor(self):
		return self._concentrationoutputfactor
	@concentrationoutputfactor.setter
	def concentrationoutputfactor(self,value):
		self._concentrationoutputfactor=value


	@property
	def initialconcentration_g_per_m3_usersupplied(self):
		cdict={}
		try:
			cdict["chem_2_3_7_8_tcdd"]=0.0
		except:
			cdict["chem_2_3_7_8_tcdd"]=nan
		
		return cdict

	@property
	def chemical_initialconcentration_g_per_m3_usersupplied(self):
		return self.initialconcentration_g_per_m3_usersupplied[self.currentchemical.name]

	@property
	def chemical_initialconcentration_g_per_m3_usersupplied(self):
		return self.initialconcentration_g_per_m3_usersupplied[self.currentchemical.name]


	@property
	def vaporwashoutratio(self):
		cdict={}
		return cdict

	@property
	def chemical_vaporwashoutratio(self):
		return self.vaporwashoutratio[self.currentchemical.name]

	@property
	def chemical_vaporwashoutratio(self):
		return self.vaporwashoutratio[self.currentchemical.name]

	@property
	def concentrationoutputunits(self):
		return ("ug/m3")
	

	@property
	def airschmidtnumber(self):
		cdict={}
		try:
			cdict["chem_2_3_7_8_tcdd"]=self.dynamicairviscosity_m2_per_sec/self.currentchemical.d_pureair_m2_s
		except:
			cdict["chem_2_3_7_8_tcdd"]=nan
		
		return cdict

	@property
	def chemical_airschmidtnumber(self):
		return self.airschmidtnumber[self.currentchemical.name]

	@property
	def chemical_airschmidtnumber(self):
		return self.airschmidtnumber[self.currentchemical.name]


	@property
	def z_total(self):
		cdict={}
		try:
			cdict["chem_2_3_7_8_tcdd"]=self.chemical_z_solid * (self.dustload /self.dustdensity) +self.chemical_z_vapor * (1 - (self.dustload /self.dustdensity))
		except:
			cdict["chem_2_3_7_8_tcdd"]=nan
		
		return cdict

	@property
	def chemical_z_total(self):
		return self.z_total[self.currentchemical.name]

	@property
	def chemical_z_total(self):
		return self.z_total[self.currentchemical.name]


	@property
	def dustresuspensionrate(self):
		cdict={}
		try:
			cdict["chem_2_3_7_8_tcdd"]=self.chemical_particlevolumetricdrydepositionrate
		except:
			cdict["chem_2_3_7_8_tcdd"]=nan
		
		return cdict

	@property
	def chemical_dustresuspensionrate(self):
		return self.dustresuspensionrate[self.currentchemical.name]

	@property
	def chemical_dustresuspensionrate(self):
		return self.dustresuspensionrate[self.currentchemical.name]


	@property
	def oxidationrate(self):
		cdict={}
		return cdict

	@property
	def chemical_oxidationrate(self):
		return self.oxidationrate[self.currentchemical.name]

	@property
	def chemical_oxidationrate(self):
		return self.oxidationrate[self.currentchemical.name]


	@property
	def z_vapor(self):
		cdict={}
		try:
			cdict["chem_2_3_7_8_tcdd"]=self.currentchemical.z_pureair
		except:
			cdict["chem_2_3_7_8_tcdd"]=nan
		
		return cdict

	@property
	def chemical_z_vapor(self):
		return self.z_vapor[self.currentchemical.name]

	@property
	def chemical_z_vapor(self):
		return self.z_vapor[self.currentchemical.name]


	@property
	def particlevolumetricwetdepositionrate(self):
		cdict={}
		try:
			cdict["chem_2_3_7_8_tcdd"]=self.chemical_washoutratio * self.containingscenario.rain * (self.dustload / self.dustdensity)
		except:
			cdict["chem_2_3_7_8_tcdd"]=nan
		
		return cdict

	@property
	def chemical_particlevolumetricwetdepositionrate(self):
		return self.particlevolumetricwetdepositionrate[self.currentchemical.name]

	@property
	def chemical_particlevolumetricwetdepositionrate(self):
		return self.particlevolumetricwetdepositionrate[self.currentchemical.name]


	@property
	def genericdenominatorforcalculatingfractioninphases(self):
		cdict={}
		return cdict

	@property
	def chemical_genericdenominatorforcalculatingfractioninphases(self):
		return self.genericdenominatorforcalculatingfractioninphases[self.currentchemical.name]

	@property
	def chemical_genericdenominatorforcalculatingfractioninphases(self):
		return self.genericdenominatorforcalculatingfractioninphases[self.currentchemical.name]

	@property
	def area(self):
		return (self.containingvolumeelement.area)
	

	@property
	def washoutratio(self):
		cdict={}
		try:
			cdict["chem_2_3_7_8_tcdd"]=18000.0
		except:
			cdict["chem_2_3_7_8_tcdd"]=nan
		
		return cdict

	@property
	def chemical_washoutratio(self):
		return self.washoutratio[self.currentchemical.name]

	@property
	def chemical_washoutratio(self):
		return self.washoutratio[self.currentchemical.name]

	@property
	def height(self):
		return (self.containingvolumeelement.height)
	
	@property
	def volumefraction_solid(self):
		return (self.volumetricairparticlecontent)
	

	@property
	def generaldegradationrate(self):
		cdict={}
		try:
			cdict["chem_2_3_7_8_tcdd"]=log(2)/ self.chemical_halflife
		except:
			cdict["chem_2_3_7_8_tcdd"]=nan
		
		return cdict

	@property
	def chemical_generaldegradationrate(self):
		return self.generaldegradationrate[self.currentchemical.name]

	@property
	def chemical_generaldegradationrate(self):
		return self.generaldegradationrate[self.currentchemical.name]


	@property
	def vdep(self):
		cdict={}
		try:
			cdict["chem_2_3_7_8_tcdd"]=500.0
		except:
			cdict["chem_2_3_7_8_tcdd"]=nan
		
		return cdict

	@property
	def chemical_vdep(self):
		return self.vdep[self.currentchemical.name]

	@property
	def chemical_vdep(self):
		return self.vdep[self.currentchemical.name]

	@property
	def airdensity_kg_m3(self):
		return (self.airdensity_g_cm3 * 1000.0)
	
	@property
	def airtemperature_c(self):
		return (self.containingscenario.airtemperature_k - 273)
	
	@property
	def volumetricairaircontent(self):
		return (1 - self.dustload / self.dustdensity)
	

	@property
	def particlegaspartitioncoefficient(self):
		cdict={}
		try:
			cdict["chem_2_3_7_8_tcdd"]=10** ( self.currentchemical.log10_k_oa  + log(self.fractionorganicmatteronparticulates+1.0e-10)/log(10) - 11.91)
		except:
			cdict["chem_2_3_7_8_tcdd"]=nan
		
		return cdict

	@property
	def chemical_particlegaspartitioncoefficient(self):
		return self.particlegaspartitioncoefficient[self.currentchemical.name]

	@property
	def chemical_particlegaspartitioncoefficient(self):
		return self.particlegaspartitioncoefficient[self.currentchemical.name]

	_isbiotic=False
	@property
	def isbiotic(self):
		return self._isbiotic
	@isbiotic.setter
	def isbiotic(self,value):
		self._isbiotic=value

	_dustload=6.15e-8
	@property
	def dustload(self):
		return self._dustload
	@dustload.setter
	def dustload(self,value):
		self._dustload=value


	@property
	def methylationrate(self):
		cdict={}
		return cdict

	@property
	def chemical_methylationrate(self):
		return self.methylationrate[self.currentchemical.name]

	@property
	def chemical_methylationrate(self):
		return self.methylationrate[self.currentchemical.name]

	_dustdensity=1400.0
	@property
	def dustdensity(self):
		return self._dustdensity
	@dustdensity.setter
	def dustdensity(self,value):
		self._dustdensity=value

	@property
	def volume(self):
		return (self.containingvolumeelement.volume)
	
class benthic_carnivore:
	def __init__(self,constants,containingscenario,currentchemical,containingvolumeelement,comp_objects_dict):
		self.containingscenario=containingscenario
		self.currentchemical=currentchemical
		self.constants=constants
		self.containingvolumeelement=containingvolumeelement
		self.comp_objects_dict=comp_objects_dict
	_biomassperarea_kg_m2=0.01
	@property
	def biomassperarea_kg_m2(self):
		return self._biomassperarea_kg_m2
	@biomassperarea_kg_m2.setter
	def biomassperarea_kg_m2(self,value):
		self._biomassperarea_kg_m2=value

	@property
	def acceptableabiotic(self):
		return ("abiotic | sediment | sediment - default")
	

	@property
	def gilleliminationrate(self):
		cdict={}
		try:
			cdict["chem_2_3_7_8_tcdd"]=self.chemical_fishchemicaluptakerateviagill / self.currentchemical.k_ow
		except:
			cdict["chem_2_3_7_8_tcdd"]=nan
		
		return cdict

	@property
	def chemical_gilleliminationrate(self):
		return self.gilleliminationrate[self.currentchemical.name]

	@property
	def chemical_gilleliminationrate(self):
		return self.gilleliminationrate[self.currentchemical.name]


	@property
	def demethylationrate(self):
		cdict={}
		return cdict

	@property
	def chemical_demethylationrate(self):
		return self.demethylationrate[self.currentchemical.name]

	@property
	def chemical_demethylationrate(self):
		return self.demethylationrate[self.currentchemical.name]


	@property
	def chemicaltransferefficiencyinfish(self):
		cdict={}
		try:
			cdict["chem_2_3_7_8_tcdd"]=(10 ** (-1.5 + 0.4 * self.currentchemical.log10_k_ow) if ( self.currentchemical.log10_k_ow < 3) else (0.5 if (self.currentchemical.log10_k_ow >= 3) and (self.currentchemical.log10_k_ow < 6) else (10 ** (1.2 - 0.25 * self.currentchemical.log10_k_ow)) ) ) if self.bw > 0.1 else (10 ** (-2.6 + 0.5 * self.currentchemical.log10_k_ow) if (self.currentchemical.log10_k_ow < 5) else (0.8 if (self.currentchemical.log10_k_ow >= 5) and (self.currentchemical.log10_k_ow < 6) else (10 ** (2.9 - 0.5 * self.currentchemical.log10_k_ow) )))
		except:
			cdict["chem_2_3_7_8_tcdd"]=nan
		
		return cdict

	@property
	def chemical_chemicaltransferefficiencyinfish(self):
		return self.chemicaltransferefficiencyinfish[self.currentchemical.name]

	@property
	def chemical_chemicaltransferefficiencyinfish(self):
		return self.chemicaltransferefficiencyinfish[self.currentchemical.name]

	_fractiondietbenthicinvertebrate=0.01
	@property
	def fractiondietbenthicinvertebrate(self):
		return self._fractiondietbenthicinvertebrate
	@fractiondietbenthicinvertebrate.setter
	def fractiondietbenthicinvertebrate(self,value):
		self._fractiondietbenthicinvertebrate=value

	_fractiondietfishbenthicomnivore=0.01
	@property
	def fractiondietfishbenthicomnivore(self):
		return self._fractiondietfishbenthicomnivore
	@fractiondietfishbenthicomnivore.setter
	def fractiondietfishbenthicomnivore(self,value):
		self._fractiondietfishbenthicomnivore=value


	@property
	def howmuchfasterhgeliminationisthanformhg(self):
		cdict={}
		return cdict

	@property
	def chemical_howmuchfasterhgeliminationisthanformhg(self):
		return self.howmuchfasterhgeliminationisthanformhg[self.currentchemical.name]

	@property
	def chemical_howmuchfasterhgeliminationisthanformhg(self):
		return self.howmuchfasterhgeliminationisthanformhg[self.currentchemical.name]

	@property
	def numberoffishpersquaremeter(self):
		return (self.biomassperarea_kg_m2/self.bw)
	

	@property
	def reductionrate(self):
		cdict={}
		return cdict

	@property
	def chemical_reductionrate(self):
		return self.reductionrate[self.currentchemical.name]

	@property
	def chemical_reductionrate(self):
		return self.reductionrate[self.currentchemical.name]


	@property
	def gamma_fish(self):
		cdict={}
		return cdict

	@property
	def chemical_gamma_fish(self):
		return self.gamma_fish[self.currentchemical.name]

	@property
	def chemical_gamma_fish(self):
		return self.gamma_fish[self.currentchemical.name]


	@property
	def fishchemicaluptakerateviagill(self):
		cdict={}
		try:
			cdict["chem_2_3_7_8_tcdd"]=600.0
		except:
			cdict["chem_2_3_7_8_tcdd"]=nan
		
		return cdict

	@property
	def chemical_fishchemicaluptakerateviagill(self):
		return self.fishchemicaluptakerateviagill[self.currentchemical.name]

	@property
	def chemical_fishchemicaluptakerateviagill(self):
		return self.fishchemicaluptakerateviagill[self.currentchemical.name]


	@property
	def halflife(self):
		cdict={}
		try:
			cdict["chem_2_3_7_8_tcdd"]=70.0
		except:
			cdict["chem_2_3_7_8_tcdd"]=nan
		
		return cdict

	@property
	def chemical_halflife(self):
		return self.halflife[self.currentchemical.name]

	@property
	def chemical_halflife(self):
		return self.halflife[self.currentchemical.name]

	@property
	def category(self):
		return ("fish | benthic carnivore")
	
	_concentrationoutputfactor=1000.0
	@property
	def concentrationoutputfactor(self):
		return self._concentrationoutputfactor
	@concentrationoutputfactor.setter
	def concentrationoutputfactor(self,value):
		self._concentrationoutputfactor=value

	@property
	def feedingrate(self):
		return (0.022 * self.bw ** (0.85) * exp(0.06 * linkedCompartmentvalue(self.containingvolumeelement,self.comp_objects_dict,"surface_water","watertemperature_c")))
	
	@property
	def concentrationoutputunits(self):
		return ("mg/kg wet weight")
	

	@property
	def initialconcentration_g_per_kg_usersupplied(self):
		cdict={}
		try:
			cdict["chem_2_3_7_8_tcdd"]=0.0
		except:
			cdict["chem_2_3_7_8_tcdd"]=nan
		
		return cdict

	@property
	def chemical_initialconcentration_g_per_kg_usersupplied(self):
		return self.initialconcentration_g_per_kg_usersupplied[self.currentchemical.name]

	@property
	def chemical_initialconcentration_g_per_kg_usersupplied(self):
		return self.initialconcentration_g_per_kg_usersupplied[self.currentchemical.name]


	@property
	def eliminationrateconstant(self):
		cdict={}
		return cdict

	@property
	def chemical_eliminationrateconstant(self):
		return self.eliminationrateconstant[self.currentchemical.name]

	@property
	def chemical_eliminationrateconstant(self):
		return self.eliminationrateconstant[self.currentchemical.name]

	_fractiondietfishomnivore=0.01
	@property
	def fractiondietfishomnivore(self):
		return self._fractiondietfishomnivore
	@fractiondietfishomnivore.setter
	def fractiondietfishomnivore(self,value):
		self._fractiondietfishomnivore=value

	_fractiondietfishcarnivore=0.01
	@property
	def fractiondietfishcarnivore(self):
		return self._fractiondietfishcarnivore
	@fractiondietfishcarnivore.setter
	def fractiondietfishcarnivore(self,value):
		self._fractiondietfishcarnivore=value


	@property
	def oxidationrate(self):
		cdict={}
		return cdict

	@property
	def chemical_oxidationrate(self):
		return self.oxidationrate[self.currentchemical.name]

	@property
	def chemical_oxidationrate(self):
		return self.oxidationrate[self.currentchemical.name]


	@property
	def absorptionrateconstant(self):
		cdict={}
		return cdict

	@property
	def chemical_absorptionrateconstant(self):
		return self.absorptionrateconstant[self.currentchemical.name]

	@property
	def chemical_absorptionrateconstant(self):
		return self.absorptionrateconstant[self.currentchemical.name]


	@property
	def generaldegradationrate(self):
		cdict={}
		try:
			cdict["chem_2_3_7_8_tcdd"]=log(2)/ self.chemical_halflife
		except:
			cdict["chem_2_3_7_8_tcdd"]=nan
		
		return cdict

	@property
	def chemical_generaldegradationrate(self):
		return self.generaldegradationrate[self.currentchemical.name]

	@property
	def chemical_generaldegradationrate(self):
		return self.generaldegradationrate[self.currentchemical.name]

	_fishlipidfraction=0.057
	@property
	def fishlipidfraction(self):
		return self._fishlipidfraction
	@fishlipidfraction.setter
	def fishlipidfraction(self,value):
		self._fishlipidfraction=value


	@property
	def assimilationefficiencyfromfood(self):
		cdict={}
		try:
			cdict["chem_2_3_7_8_tcdd"]=0.41
		except:
			cdict["chem_2_3_7_8_tcdd"]=nan
		
		return cdict

	@property
	def chemical_assimilationefficiencyfromfood(self):
		return self.assimilationefficiencyfromfood[self.currentchemical.name]

	@property
	def chemical_assimilationefficiencyfromfood(self):
		return self.assimilationefficiencyfromfood[self.currentchemical.name]

	@property
	def populationsize(self):
		return (self.numberoffishpersquaremeter * self.containingvolumeelement.area)
	
	@property
	def totalmass(self):
		return (self.populationsize  * self.bw)
	

	@property
	def initialconcentration_g_per_kg(self):
		cdict={}
		try:
			cdict["chem_2_3_7_8_tcdd"]=self.containingscenario.fractioninitialconcentrations * self.chemical_initialconcentration_g_per_kg_usersupplied
		except:
			cdict["chem_2_3_7_8_tcdd"]=nan
		
		return cdict

	@property
	def chemical_initialconcentration_g_per_kg(self):
		return self.initialconcentration_g_per_kg[self.currentchemical.name]

	@property
	def chemical_initialconcentration_g_per_kg(self):
		return self.initialconcentration_g_per_kg[self.currentchemical.name]

	_fractiondietfishherbivore=0.01
	@property
	def fractiondietfishherbivore(self):
		return self._fractiondietfishherbivore
	@fractiondietfishherbivore.setter
	def fractiondietfishherbivore(self,value):
		self._fractiondietfishherbivore=value

	_isbiotic=True
	@property
	def isbiotic(self):
		return self._isbiotic
	@isbiotic.setter
	def isbiotic(self,value):
		self._isbiotic=value

	_fractiondietalgae=0.01
	@property
	def fractiondietalgae(self):
		return self._fractiondietalgae
	@fractiondietalgae.setter
	def fractiondietalgae(self,value):
		self._fractiondietalgae=value

	@property
	def image(self):
		return ("c:\models\trim\data\images\creekchub.gif")
	

	@property
	def methylationrate(self):
		cdict={}
		return cdict

	@property
	def chemical_methylationrate(self):
		return self.methylationrate[self.currentchemical.name]

	@property
	def chemical_methylationrate(self):
		return self.methylationrate[self.currentchemical.name]

	@property
	def foodingestionrate(self):
		return (self.feedingrate/self.bw)
	
	_bw=2.0
	@property
	def bw(self):
		return self._bw
	@bw.setter
	def bw(self,value):
		self._bw=value

class benthic_invertebrate:
	def __init__(self,constants,containingscenario,currentchemical,containingvolumeelement,comp_objects_dict):
		self.containingscenario=containingscenario
		self.currentchemical=currentchemical
		self.constants=constants
		self.containingvolumeelement=containingvolumeelement
		self.comp_objects_dict=comp_objects_dict

	@property
	def sedimentpartitioning_alphaofequilibrium(self):
		cdict={}
		try:
			cdict["chem_2_3_7_8_tcdd"]=0.95
		except:
			cdict["chem_2_3_7_8_tcdd"]=nan
		
		return cdict

	@property
	def chemical_sedimentpartitioning_alphaofequilibrium(self):
		return self.sedimentpartitioning_alphaofequilibrium[self.currentchemical.name]

	@property
	def chemical_sedimentpartitioning_alphaofequilibrium(self):
		return self.sedimentpartitioning_alphaofequilibrium[self.currentchemical.name]


	@property
	def clearanceconstant(self):
		cdict={}
		try:
			cdict["chem_2_3_7_8_tcdd"]=0.0
		except:
			cdict["chem_2_3_7_8_tcdd"]=nan
		
		return cdict

	@property
	def chemical_clearanceconstant(self):
		return self.clearanceconstant[self.currentchemical.name]

	@property
	def chemical_clearanceconstant(self):
		return self.clearanceconstant[self.currentchemical.name]

	_biomassperarea_kg_m2=0.02
	@property
	def biomassperarea_kg_m2(self):
		return self._biomassperarea_kg_m2
	@biomassperarea_kg_m2.setter
	def biomassperarea_kg_m2(self,value):
		self._biomassperarea_kg_m2=value

	@property
	def acceptableabiotic(self):
		return ("abiotic | sediment | sediment - default")
	

	@property
	def uptakeconstant(self):
		cdict={}
		try:
			cdict["chem_2_3_7_8_tcdd"]=self.chemical_clearanceconstant
		except:
			cdict["chem_2_3_7_8_tcdd"]=nan
		
		return cdict

	@property
	def chemical_uptakeconstant(self):
		return self.uptakeconstant[self.currentchemical.name]

	@property
	def chemical_uptakeconstant(self):
		return self.uptakeconstant[self.currentchemical.name]


	@property
	def sedimentpartitioning_partitioncoefficient(self):
		cdict={}
		try:
			cdict["chem_2_3_7_8_tcdd"]=0.205
		except:
			cdict["chem_2_3_7_8_tcdd"]=nan
		
		return cdict

	@property
	def chemical_sedimentpartitioning_partitioncoefficient(self):
		return self.sedimentpartitioning_partitioncoefficient[self.currentchemical.name]

	@property
	def chemical_sedimentpartitioning_partitioncoefficient(self):
		return self.sedimentpartitioning_partitioncoefficient[self.currentchemical.name]


	@property
	def abbreviation(self):
		cdict={}
		return cdict

	@property
	def chemical_abbreviation(self):
		return self.abbreviation[self.currentchemical.name]

	@property
	def chemical_abbreviation(self):
		return self.abbreviation[self.currentchemical.name]


	@property
	def halflife(self):
		cdict={}
		try:
			cdict["chem_2_3_7_8_tcdd"]=5776.226505
		except:
			cdict["chem_2_3_7_8_tcdd"]=nan
		
		return cdict

	@property
	def chemical_halflife(self):
		return self.halflife[self.currentchemical.name]

	@property
	def chemical_halflife(self):
		return self.halflife[self.currentchemical.name]

	@property
	def category(self):
		return ("insect | benthic invertebrate")
	
	_concentrationoutputfactor=1000.0
	@property
	def concentrationoutputfactor(self):
		return self._concentrationoutputfactor
	@concentrationoutputfactor.setter
	def concentrationoutputfactor(self,value):
		self._concentrationoutputfactor=value


	@property
	def initialconcentration_g_per_kg_usersupplied(self):
		cdict={}
		try:
			cdict["chem_2_3_7_8_tcdd"]=0.0
		except:
			cdict["chem_2_3_7_8_tcdd"]=nan
		
		return cdict

	@property
	def chemical_initialconcentration_g_per_kg_usersupplied(self):
		return self.initialconcentration_g_per_kg_usersupplied[self.currentchemical.name]

	@property
	def chemical_initialconcentration_g_per_kg_usersupplied(self):
		return self.initialconcentration_g_per_kg_usersupplied[self.currentchemical.name]

	@property
	def concentrationoutputunits(self):
		return ("mg/kg wet weight")
	

	@property
	def sedimentpartitioning_timetoreachalphaofequilibrium(self):
		cdict={}
		try:
			cdict["chem_2_3_7_8_tcdd"]=120.0
		except:
			cdict["chem_2_3_7_8_tcdd"]=nan
		
		return cdict

	@property
	def chemical_sedimentpartitioning_timetoreachalphaofequilibrium(self):
		return self.sedimentpartitioning_timetoreachalphaofequilibrium[self.currentchemical.name]

	@property
	def chemical_sedimentpartitioning_timetoreachalphaofequilibrium(self):
		return self.sedimentpartitioning_timetoreachalphaofequilibrium[self.currentchemical.name]


	@property
	def generaldegradationrate(self):
		cdict={}
		try:
			cdict["chem_2_3_7_8_tcdd"]=log(2)/ self.chemical_halflife
		except:
			cdict["chem_2_3_7_8_tcdd"]=nan
		
		return cdict

	@property
	def chemical_generaldegradationrate(self):
		return self.generaldegradationrate[self.currentchemical.name]

	@property
	def chemical_generaldegradationrate(self):
		return self.generaldegradationrate[self.currentchemical.name]

	@property
	def populationsize(self):
		return (self.totalmass/self.bw)
	
	@property
	def totalmass(self):
		return (self.biomassperarea_kg_m2 * self.containingvolumeelement.area)
	

	@property
	def initialconcentration_g_per_kg(self):
		cdict={}
		try:
			cdict["chem_2_3_7_8_tcdd"]=self.containingscenario.fractioninitialconcentrations * self.chemical_initialconcentration_g_per_kg_usersupplied
		except:
			cdict["chem_2_3_7_8_tcdd"]=nan
		
		return cdict

	@property
	def chemical_initialconcentration_g_per_kg(self):
		return self.initialconcentration_g_per_kg[self.currentchemical.name]

	@property
	def chemical_initialconcentration_g_per_kg(self):
		return self.initialconcentration_g_per_kg[self.currentchemical.name]

	_isbiotic=True
	@property
	def isbiotic(self):
		return self._isbiotic
	@isbiotic.setter
	def isbiotic(self,value):
		self._isbiotic=value


	@property
	def v_d(self):
		cdict={}
		try:
			cdict["chem_2_3_7_8_tcdd"]=0.0
		except:
			cdict["chem_2_3_7_8_tcdd"]=nan
		
		return cdict

	@property
	def chemical_v_d(self):
		return self.v_d[self.currentchemical.name]

	@property
	def chemical_v_d(self):
		return self.v_d[self.currentchemical.name]

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

class benthic_omnivore:
	def __init__(self,constants,containingscenario,currentchemical,containingvolumeelement,comp_objects_dict):
		self.containingscenario=containingscenario
		self.currentchemical=currentchemical
		self.constants=constants
		self.containingvolumeelement=containingvolumeelement
		self.comp_objects_dict=comp_objects_dict
	_biomassperarea_kg_m2=0.01
	@property
	def biomassperarea_kg_m2(self):
		return self._biomassperarea_kg_m2
	@biomassperarea_kg_m2.setter
	def biomassperarea_kg_m2(self,value):
		self._biomassperarea_kg_m2=value

	@property
	def acceptableabiotic(self):
		return ("abiotic | sediment | sediment - default")
	

	@property
	def gilleliminationrate(self):
		cdict={}
		try:
			cdict["chem_2_3_7_8_tcdd"]=self.chemical_fishchemicaluptakerateviagill / self.currentchemical.k_ow
		except:
			cdict["chem_2_3_7_8_tcdd"]=nan
		
		return cdict

	@property
	def chemical_gilleliminationrate(self):
		return self.gilleliminationrate[self.currentchemical.name]

	@property
	def chemical_gilleliminationrate(self):
		return self.gilleliminationrate[self.currentchemical.name]


	@property
	def demethylationrate(self):
		cdict={}
		return cdict

	@property
	def chemical_demethylationrate(self):
		return self.demethylationrate[self.currentchemical.name]

	@property
	def chemical_demethylationrate(self):
		return self.demethylationrate[self.currentchemical.name]


	@property
	def chemicaltransferefficiencyinfish(self):
		cdict={}
		try:
			cdict["chem_2_3_7_8_tcdd"]=(10 ** (-1.5 + 0.4 * self.currentchemical.log10_k_ow) if ( self.currentchemical.log10_k_ow < 3) else (0.5 if (self.currentchemical.log10_k_ow >= 3) and (self.currentchemical.log10_k_ow < 6) else (10 ** (1.2 - 0.25 * self.currentchemical.log10_k_ow)) ) ) if self.bw > 0.1 else (10 ** (-2.6 + 0.5 * self.currentchemical.log10_k_ow) if (self.currentchemical.log10_k_ow < 5) else (0.8 if (self.currentchemical.log10_k_ow >= 5) and (self.currentchemical.log10_k_ow < 6) else (10 ** (2.9 - 0.5 * self.currentchemical.log10_k_ow) )))
		except:
			cdict["chem_2_3_7_8_tcdd"]=nan
		
		return cdict

	@property
	def chemical_chemicaltransferefficiencyinfish(self):
		return self.chemicaltransferefficiencyinfish[self.currentchemical.name]

	@property
	def chemical_chemicaltransferefficiencyinfish(self):
		return self.chemicaltransferefficiencyinfish[self.currentchemical.name]

	_fractiondietbenthicinvertebrate=0.01
	@property
	def fractiondietbenthicinvertebrate(self):
		return self._fractiondietbenthicinvertebrate
	@fractiondietbenthicinvertebrate.setter
	def fractiondietbenthicinvertebrate(self,value):
		self._fractiondietbenthicinvertebrate=value


	@property
	def howmuchfasterhgeliminationisthanformhg(self):
		cdict={}
		return cdict

	@property
	def chemical_howmuchfasterhgeliminationisthanformhg(self):
		return self.howmuchfasterhgeliminationisthanformhg[self.currentchemical.name]

	@property
	def chemical_howmuchfasterhgeliminationisthanformhg(self):
		return self.howmuchfasterhgeliminationisthanformhg[self.currentchemical.name]

	@property
	def numberoffishpersquaremeter(self):
		return (self.biomassperarea_kg_m2/self.bw)
	

	@property
	def reductionrate(self):
		cdict={}
		return cdict

	@property
	def chemical_reductionrate(self):
		return self.reductionrate[self.currentchemical.name]

	@property
	def chemical_reductionrate(self):
		return self.reductionrate[self.currentchemical.name]


	@property
	def gamma_fish(self):
		cdict={}
		return cdict

	@property
	def chemical_gamma_fish(self):
		return self.gamma_fish[self.currentchemical.name]

	@property
	def chemical_gamma_fish(self):
		return self.gamma_fish[self.currentchemical.name]

	_fractiondietfishbenthiccarnivore=0.01
	@property
	def fractiondietfishbenthiccarnivore(self):
		return self._fractiondietfishbenthiccarnivore
	@fractiondietfishbenthiccarnivore.setter
	def fractiondietfishbenthiccarnivore(self,value):
		self._fractiondietfishbenthiccarnivore=value


	@property
	def fishchemicaluptakerateviagill(self):
		cdict={}
		try:
			cdict["chem_2_3_7_8_tcdd"]=600.0
		except:
			cdict["chem_2_3_7_8_tcdd"]=nan
		
		return cdict

	@property
	def chemical_fishchemicaluptakerateviagill(self):
		return self.fishchemicaluptakerateviagill[self.currentchemical.name]

	@property
	def chemical_fishchemicaluptakerateviagill(self):
		return self.fishchemicaluptakerateviagill[self.currentchemical.name]


	@property
	def halflife(self):
		cdict={}
		try:
			cdict["chem_2_3_7_8_tcdd"]=70.0
		except:
			cdict["chem_2_3_7_8_tcdd"]=nan
		
		return cdict

	@property
	def chemical_halflife(self):
		return self.halflife[self.currentchemical.name]

	@property
	def chemical_halflife(self):
		return self.halflife[self.currentchemical.name]

	@property
	def category(self):
		return ("fish | benthic omnivore")
	
	_concentrationoutputfactor=1000.0
	@property
	def concentrationoutputfactor(self):
		return self._concentrationoutputfactor
	@concentrationoutputfactor.setter
	def concentrationoutputfactor(self,value):
		self._concentrationoutputfactor=value

	@property
	def feedingrate(self):
		return (0.022 * self.bw ** (0.85) * exp(0.06 * linkedCompartmentvalue(self.containingvolumeelement,self.comp_objects_dict,"surface_water","watertemperature_c")))
	
	@property
	def concentrationoutputunits(self):
		return ("mg/kg wet weight")
	

	@property
	def initialconcentration_g_per_kg_usersupplied(self):
		cdict={}
		try:
			cdict["chem_2_3_7_8_tcdd"]=0.0
		except:
			cdict["chem_2_3_7_8_tcdd"]=nan
		
		return cdict

	@property
	def chemical_initialconcentration_g_per_kg_usersupplied(self):
		return self.initialconcentration_g_per_kg_usersupplied[self.currentchemical.name]

	@property
	def chemical_initialconcentration_g_per_kg_usersupplied(self):
		return self.initialconcentration_g_per_kg_usersupplied[self.currentchemical.name]


	@property
	def eliminationrateconstant(self):
		cdict={}
		return cdict

	@property
	def chemical_eliminationrateconstant(self):
		return self.eliminationrateconstant[self.currentchemical.name]

	@property
	def chemical_eliminationrateconstant(self):
		return self.eliminationrateconstant[self.currentchemical.name]

	_fractiondietfishomnivore=0.01
	@property
	def fractiondietfishomnivore(self):
		return self._fractiondietfishomnivore
	@fractiondietfishomnivore.setter
	def fractiondietfishomnivore(self,value):
		self._fractiondietfishomnivore=value

	_fractiondietfishcarnivore=0.01
	@property
	def fractiondietfishcarnivore(self):
		return self._fractiondietfishcarnivore
	@fractiondietfishcarnivore.setter
	def fractiondietfishcarnivore(self,value):
		self._fractiondietfishcarnivore=value


	@property
	def oxidationrate(self):
		cdict={}
		return cdict

	@property
	def chemical_oxidationrate(self):
		return self.oxidationrate[self.currentchemical.name]

	@property
	def chemical_oxidationrate(self):
		return self.oxidationrate[self.currentchemical.name]


	@property
	def absorptionrateconstant(self):
		cdict={}
		return cdict

	@property
	def chemical_absorptionrateconstant(self):
		return self.absorptionrateconstant[self.currentchemical.name]

	@property
	def chemical_absorptionrateconstant(self):
		return self.absorptionrateconstant[self.currentchemical.name]


	@property
	def generaldegradationrate(self):
		cdict={}
		try:
			cdict["chem_2_3_7_8_tcdd"]=log(2)/ self.chemical_halflife
		except:
			cdict["chem_2_3_7_8_tcdd"]=nan
		
		return cdict

	@property
	def chemical_generaldegradationrate(self):
		return self.generaldegradationrate[self.currentchemical.name]

	@property
	def chemical_generaldegradationrate(self):
		return self.generaldegradationrate[self.currentchemical.name]

	_fishlipidfraction=0.07
	@property
	def fishlipidfraction(self):
		return self._fishlipidfraction
	@fishlipidfraction.setter
	def fishlipidfraction(self,value):
		self._fishlipidfraction=value


	@property
	def assimilationefficiencyfromfood(self):
		cdict={}
		try:
			cdict["chem_2_3_7_8_tcdd"]=0.41
		except:
			cdict["chem_2_3_7_8_tcdd"]=nan
		
		return cdict

	@property
	def chemical_assimilationefficiencyfromfood(self):
		return self.assimilationefficiencyfromfood[self.currentchemical.name]

	@property
	def chemical_assimilationefficiencyfromfood(self):
		return self.assimilationefficiencyfromfood[self.currentchemical.name]

	@property
	def populationsize(self):
		return (self.numberoffishpersquaremeter * self.containingvolumeelement.area)
	
	@property
	def totalmass(self):
		return (self.populationsize  * self.bw)
	

	@property
	def initialconcentration_g_per_kg(self):
		cdict={}
		try:
			cdict["chem_2_3_7_8_tcdd"]=self.containingscenario.fractioninitialconcentrations * self.chemical_initialconcentration_g_per_kg_usersupplied
		except:
			cdict["chem_2_3_7_8_tcdd"]=nan
		
		return cdict

	@property
	def chemical_initialconcentration_g_per_kg(self):
		return self.initialconcentration_g_per_kg[self.currentchemical.name]

	@property
	def chemical_initialconcentration_g_per_kg(self):
		return self.initialconcentration_g_per_kg[self.currentchemical.name]

	_fractiondietfishherbivore=0.01
	@property
	def fractiondietfishherbivore(self):
		return self._fractiondietfishherbivore
	@fractiondietfishherbivore.setter
	def fractiondietfishherbivore(self,value):
		self._fractiondietfishherbivore=value

	_isbiotic=True
	@property
	def isbiotic(self):
		return self._isbiotic
	@isbiotic.setter
	def isbiotic(self,value):
		self._isbiotic=value

	_fractiondietalgae=0.01
	@property
	def fractiondietalgae(self):
		return self._fractiondietalgae
	@fractiondietalgae.setter
	def fractiondietalgae(self,value):
		self._fractiondietalgae=value

	@property
	def image(self):
		return ("c:\models\trim\data\images\catfish.gif")
	

	@property
	def methylationrate(self):
		cdict={}
		return cdict

	@property
	def chemical_methylationrate(self):
		return self.methylationrate[self.currentchemical.name]

	@property
	def chemical_methylationrate(self):
		return self.methylationrate[self.currentchemical.name]

	@property
	def foodingestionrate(self):
		return (self.feedingrate/self.bw)
	
	_bw=2.0
	@property
	def bw(self):
		return self._bw
	@bw.setter
	def bw(self,value):
		self._bw=value

class degradation_reaction_sink:
	def __init__(self,constants,containingscenario,currentchemical,containingvolumeelement,comp_objects_dict):
		self.containingscenario=containingscenario
		self.currentchemical=currentchemical
		self.constants=constants
		self.containingvolumeelement=containingvolumeelement
		self.comp_objects_dict=comp_objects_dict
	@property
	def acceptableabiotic(self):
		return ("nan")
	
	_isbiotic=False
	@property
	def isbiotic(self):
		return self._isbiotic
	@isbiotic.setter
	def isbiotic(self,value):
		self._isbiotic=value

	@property
	def category(self):
		return ("sink | degradation/reaction sink")
	
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
	def acceptableabiotic(self):
		return ("abiotic | surface water | surface water - default")
	
	_isbiotic=False
	@property
	def isbiotic(self):
		return self._isbiotic
	@isbiotic.setter
	def isbiotic(self,value):
		self._isbiotic=value

	@property
	def category(self):
		return ("sink | abiotic | surface water | surface water - default")
	
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
	
class groundwater:
	def __init__(self,constants,containingscenario,currentchemical,containingvolumeelement,comp_objects_dict):
		self.containingscenario=containingscenario
		self.currentchemical=currentchemical
		self.constants=constants
		self.containingvolumeelement=containingvolumeelement
		self.comp_objects_dict=comp_objects_dict
	@property
	def acceptableabiotic(self):
		return ("nan")
	

	@property
	def demethylationrate(self):
		cdict={}
		return cdict

	@property
	def chemical_demethylationrate(self):
		return self.demethylationrate[self.currentchemical.name]

	@property
	def chemical_demethylationrate(self):
		return self.demethylationrate[self.currentchemical.name]


	@property
	def fractionmass_vapor(self):
		cdict={}
		try:
			cdict["chem_2_3_7_8_tcdd"]=self.volume * self.volumefraction_vapor * 1000 * (self.chemical_z_vapor /self.chemical_z_liquid) / self.chemical_genericdenominatorforcalculatingfractioninphases
		except:
			cdict["chem_2_3_7_8_tcdd"]=nan
		
		return cdict

	@property
	def chemical_fractionmass_vapor(self):
		return self.fractionmass_vapor[self.currentchemical.name]

	@property
	def chemical_fractionmass_vapor(self):
		return self.fractionmass_vapor[self.currentchemical.name]

	@property
	def volumefraction_vapor(self):
		return (0)
	

	@property
	def fractionmass_dissolved(self):
		cdict={}
		try:
			cdict["chem_2_3_7_8_tcdd"]=self.volume * self.volumefraction_liquid * 1000 /self.chemical_genericdenominatorforcalculatingfractioninphases
		except:
			cdict["chem_2_3_7_8_tcdd"]=nan
		
		return cdict

	@property
	def chemical_fractionmass_dissolved(self):
		return self.fractionmass_dissolved[self.currentchemical.name]

	@property
	def chemical_fractionmass_dissolved(self):
		return self.fractionmass_dissolved[self.currentchemical.name]

	_porosity=0.2
	@property
	def porosity(self):
		return self._porosity
	@porosity.setter
	def porosity(self,value):
		self._porosity=value


	@property
	def initialconcentration_g_per_l_usersupplied(self):
		cdict={}
		try:
			cdict["chem_2_3_7_8_tcdd"]=0.0
		except:
			cdict["chem_2_3_7_8_tcdd"]=nan
		
		return cdict

	@property
	def chemical_initialconcentration_g_per_l_usersupplied(self):
		return self.initialconcentration_g_per_l_usersupplied[self.currentchemical.name]

	@property
	def chemical_initialconcentration_g_per_l_usersupplied(self):
		return self.initialconcentration_g_per_l_usersupplied[self.currentchemical.name]


	@property
	def reductionrate(self):
		cdict={}
		return cdict

	@property
	def chemical_reductionrate(self):
		return self.reductionrate[self.currentchemical.name]

	@property
	def chemical_reductionrate(self):
		return self.reductionrate[self.currentchemical.name]


	@property
	def z_solid(self):
		cdict={}
		try:
			cdict["chem_2_3_7_8_tcdd"]=(self.rho * self.chemical_kd / 1000) * self.currentchemical.z_purewater
		except:
			cdict["chem_2_3_7_8_tcdd"]=nan
		
		return cdict

	@property
	def chemical_z_solid(self):
		return self.z_solid[self.currentchemical.name]

	@property
	def chemical_z_solid(self):
		return self.z_solid[self.currentchemical.name]


	@property
	def d_effective(self):
		cdict={}
		try:
			cdict["chem_2_3_7_8_tcdd"]=self.currentchemical.z_purewater /self.chemical_z_total * self.currentchemical.d_purewater * self.volumefraction_liquid ** (10 / 3) / self.porosity ** 2 + self.currentchemical.z_pureair /self.chemical_z_total * self.currentchemical.d_pureair * self.volumefraction_vapor ** (10 / 3) / self.porosity ** 2
		except:
			cdict["chem_2_3_7_8_tcdd"]=nan
		
		return cdict

	@property
	def chemical_d_effective(self):
		return self.d_effective[self.currentchemical.name]

	@property
	def chemical_d_effective(self):
		return self.d_effective[self.currentchemical.name]


	@property
	def z_liquid(self):
		cdict={}
		try:
			cdict["chem_2_3_7_8_tcdd"]=self.currentchemical.z_purewater
		except:
			cdict["chem_2_3_7_8_tcdd"]=nan
		
		return cdict

	@property
	def chemical_z_liquid(self):
		return self.z_liquid[self.currentchemical.name]

	@property
	def chemical_z_liquid(self):
		return self.z_liquid[self.currentchemical.name]


	@property
	def halflife(self):
		cdict={}
		try:
			cdict["chem_2_3_7_8_tcdd"]=1008.0
		except:
			cdict["chem_2_3_7_8_tcdd"]=nan
		
		return cdict

	@property
	def chemical_halflife(self):
		return self.halflife[self.currentchemical.name]

	@property
	def chemical_halflife(self):
		return self.halflife[self.currentchemical.name]

	@property
	def category(self):
		return ("abiotic | soil | groundwater | groundwater - default")
	
	_fractionsand=0.4
	@property
	def fractionsand(self):
		return self._fractionsand
	@fractionsand.setter
	def fractionsand(self,value):
		self._fractionsand=value


	@property
	def fractionmass_sorbed(self):
		cdict={}
		try:
			cdict["chem_2_3_7_8_tcdd"]=self.volume * (self.chemical_kd * self.rho) * (1 - self.volumefraction_liquid - self.volumefraction_vapor ) / self.chemical_genericdenominatorforcalculatingfractioninphases
		except:
			cdict["chem_2_3_7_8_tcdd"]=nan
		
		return cdict

	@property
	def chemical_fractionmass_sorbed(self):
		return self.fractionmass_sorbed[self.currentchemical.name]

	@property
	def chemical_fractionmass_sorbed(self):
		return self.fractionmass_sorbed[self.currentchemical.name]

	_concentrationoutputfactor=1.0
	@property
	def concentrationoutputfactor(self):
		return self._concentrationoutputfactor
	@concentrationoutputfactor.setter
	def concentrationoutputfactor(self,value):
		self._concentrationoutputfactor=value

	_rho=2600.0
	@property
	def rho(self):
		return self._rho
	@rho.setter
	def rho(self,value):
		self._rho=value


	@property
	def totaltransformationrate(self):
		cdict={}
		try:
			cdict["chem_2_3_7_8_tcdd"]=self.chemical_generaldegradationrate
		except:
			cdict["chem_2_3_7_8_tcdd"]=nan
		
		return cdict

	@property
	def chemical_totaltransformationrate(self):
		return self.totaltransformationrate[self.currentchemical.name]

	@property
	def chemical_totaltransformationrate(self):
		return self.totaltransformationrate[self.currentchemical.name]

	@property
	def concentrationoutputunits(self):
		return ("g/l")
	

	@property
	def initialconcentration_g_per_l(self):
		cdict={}
		try:
			cdict["chem_2_3_7_8_tcdd"]=self.containingscenario.fractioninitialconcentrations * self.chemical_initialconcentration_g_per_l_usersupplied
		except:
			cdict["chem_2_3_7_8_tcdd"]=nan
		
		return cdict

	@property
	def chemical_initialconcentration_g_per_l(self):
		return self.initialconcentration_g_per_l[self.currentchemical.name]

	@property
	def chemical_initialconcentration_g_per_l(self):
		return self.initialconcentration_g_per_l[self.currentchemical.name]

	_ph=0.01
	@property
	def ph(self):
		return self._ph
	@ph.setter
	def ph(self,value):
		self._ph=value


	@property
	def z_total(self):
		cdict={}
		try:
			cdict["chem_2_3_7_8_tcdd"]=self.chemical_z_solid * (1 - self.porosity) + self.chemical_z_liquid* self.volumefraction_liquid + self.chemical_z_vapor * self.volumefraction_vapor
		except:
			cdict["chem_2_3_7_8_tcdd"]=nan
		
		return cdict

	@property
	def chemical_z_total(self):
		return self.z_total[self.currentchemical.name]

	@property
	def chemical_z_total(self):
		return self.z_total[self.currentchemical.name]


	@property
	def oxidationrate(self):
		cdict={}
		return cdict

	@property
	def chemical_oxidationrate(self):
		return self.oxidationrate[self.currentchemical.name]

	@property
	def chemical_oxidationrate(self):
		return self.oxidationrate[self.currentchemical.name]


	@property
	def z_vapor(self):
		cdict={}
		try:
			cdict["chem_2_3_7_8_tcdd"]=self.currentchemical.z_pureair
		except:
			cdict["chem_2_3_7_8_tcdd"]=nan
		
		return cdict

	@property
	def chemical_z_vapor(self):
		return self.z_vapor[self.currentchemical.name]

	@property
	def chemical_z_vapor(self):
		return self.z_vapor[self.currentchemical.name]


	@property
	def genericdenominatorforcalculatingfractioninphases(self):
		cdict={}
		try:
			cdict["chem_2_3_7_8_tcdd"]=self.volume * ( (self.chemical_kd * self.rho) * (1 - self.volumefraction_liquid - self.volumefraction_vapor) + self.volumefraction_liquid * 1000 + self.volumefraction_vapor * (self.chemical_z_vapor /self.chemical_z_liquid) * 1000 )
		except:
			cdict["chem_2_3_7_8_tcdd"]=nan
		
		return cdict

	@property
	def chemical_genericdenominatorforcalculatingfractioninphases(self):
		return self.genericdenominatorforcalculatingfractioninphases[self.currentchemical.name]

	@property
	def chemical_genericdenominatorforcalculatingfractioninphases(self):
		return self.genericdenominatorforcalculatingfractioninphases[self.currentchemical.name]

	@property
	def area(self):
		return (self.containingvolumeelement.area)
	
	@property
	def height(self):
		return (self.containingvolumeelement.height)
	
	@property
	def depth(self):
		return (self.height)
	
	@property
	def volumefraction_solid(self):
		return (1.0 - self.porosity)
	
	_organiccarboncontent=0.01
	@property
	def organiccarboncontent(self):
		return self._organiccarboncontent
	@organiccarboncontent.setter
	def organiccarboncontent(self,value):
		self._organiccarboncontent=value


	@property
	def generaldegradationrate(self):
		cdict={}
		try:
			cdict["chem_2_3_7_8_tcdd"]=log(2)/ self.chemical_halflife
		except:
			cdict["chem_2_3_7_8_tcdd"]=nan
		
		return cdict

	@property
	def chemical_generaldegradationrate(self):
		return self.generaldegradationrate[self.currentchemical.name]

	@property
	def chemical_generaldegradationrate(self):
		return self.generaldegradationrate[self.currentchemical.name]

	@property
	def totalmass(self):
		return (self.volume * self.rho)
	
	@property
	def volumefraction_liquid(self):
		return (self.porosity - self.volumefraction_vapor)
	
	_isbiotic=False
	@property
	def isbiotic(self):
		return self._isbiotic
	@isbiotic.setter
	def isbiotic(self,value):
		self._isbiotic=value


	@property
	def methylationrate(self):
		cdict={}
		return cdict

	@property
	def chemical_methylationrate(self):
		return self.methylationrate[self.currentchemical.name]

	@property
	def chemical_methylationrate(self):
		return self.methylationrate[self.currentchemical.name]


	@property
	def kd(self):
		cdict={}
		try:
			cdict["chem_2_3_7_8_tcdd"]=self.currentchemical.k_oc * self.organiccarboncontent
		except:
			cdict["chem_2_3_7_8_tcdd"]=nan
		
		return cdict

	@property
	def chemical_kd(self):
		return self.kd[self.currentchemical.name]

	@property
	def chemical_kd(self):
		return self.kd[self.currentchemical.name]

	@property
	def volume(self):
		return (self.containingvolumeelement.volume)
	
class leaf_coniferous_forest_in_coniferous_forest:
	def __init__(self,constants,containingscenario,currentchemical,containingvolumeelement,comp_objects_dict):
		self.containingscenario=containingscenario
		self.currentchemical=currentchemical
		self.constants=constants
		self.containingvolumeelement=containingvolumeelement
		self.comp_objects_dict=comp_objects_dict
	@property
	def acceptableabiotic(self):
		return ("abiotic | soil | surface soil")
	
	@property
	def wetdepinterceptionfraction(self):
		return (self.wetdepinterceptionfraction_calculated if self.calculatewetdepinterceptionfraction==1 else self.wetdepinterceptionfraction_usersupplied)
	
	@property
	def dryvolumeperarea(self):
		return (self.wetvolumeperarea*(1 - self.watercontent))
	

	@property
	def demethylationrate(self):
		cdict={}
		return cdict

	@property
	def chemical_demethylationrate(self):
		return self.demethylationrate[self.currentchemical.name]

	@property
	def chemical_demethylationrate(self):
		return self.demethylationrate[self.currentchemical.name]

	_fractionorganicmatteronparticulates=0.2
	@property
	def fractionorganicmatteronparticulates(self):
		return self._fractionorganicmatteronparticulates
	@fractionorganicmatteronparticulates.setter
	def fractionorganicmatteronparticulates(self,value):
		self._fractionorganicmatteronparticulates=value


	@property
	def transferfactortoleafparticle(self):
		cdict={}
		try:
			cdict["chem_2_3_7_8_tcdd"]=0.003
		except:
			cdict["chem_2_3_7_8_tcdd"]=nan
		
		return cdict

	@property
	def chemical_transferfactortoleafparticle(self):
		return self.transferfactortoleafparticle[self.currentchemical.name]

	@property
	def chemical_transferfactortoleafparticle(self):
		return self.transferfactortoleafparticle[self.currentchemical.name]

	_litterfallrate=0.0021
	@property
	def litterfallrate(self):
		return self._litterfallrate
	@litterfallrate.setter
	def litterfallrate(self,value):
		self._litterfallrate=value


	@property
	def reductionrate(self):
		cdict={}
		return cdict

	@property
	def chemical_reductionrate(self):
		return self.reductionrate[self.currentchemical.name]

	@property
	def chemical_reductionrate(self):
		return self.reductionrate[self.currentchemical.name]

	@property
	def drydepinterceptionfraction(self):
		return (1 - exp(-self.attenuationfactor * self.drymassperarea))
	
	_leafwettingfactor=3.0e-4
	@property
	def leafwettingfactor(self):
		return self._leafwettingfactor
	@leafwettingfactor.setter
	def leafwettingfactor(self,value):
		self._leafwettingfactor=value

	@property
	def isday_forother(self):
		return (self.containingscenario.isday_steadystate_forother if self.containingscenario.simulatesteadystate == 1 else self.containingscenario.isday_dynamic)
	
	@property
	def leafarea(self):
		return (self.leafareaindex*self.containingvolumeelement.area)
	

	@property
	def totalcuticularconductance(self):
		cdict={}
		try:
			cdict["chem_2_3_7_8_tcdd"]=1/(1.0/self.chemical_cuticularconductance  + 1.0/self.chemical_boundarylayerconductance)
		except:
			cdict["chem_2_3_7_8_tcdd"]=nan
		
		return cdict

	@property
	def chemical_totalcuticularconductance(self):
		return self.totalcuticularconductance[self.currentchemical.name]

	@property
	def chemical_totalcuticularconductance(self):
		return self.totalcuticularconductance[self.currentchemical.name]

	@property
	def wetvolumeperarea(self):
		return (self.wetmassperarea/self.wetdensity)
	
	@property
	def leafareaindex(self):
		return (self.averageleafareaindex_no_time_dependence)
	
	_lipidcontent=0.00224
	@property
	def lipidcontent(self):
		return self._lipidcontent
	@lipidcontent.setter
	def lipidcontent(self,value):
		self._lipidcontent=value


	@property
	def halflife(self):
		cdict={}
		try:
			cdict["chem_2_3_7_8_tcdd"]=70.0
		except:
			cdict["chem_2_3_7_8_tcdd"]=nan
		
		return cdict

	@property
	def chemical_halflife(self):
		return self.halflife[self.currentchemical.name]

	@property
	def chemical_halflife(self):
		return self.halflife[self.currentchemical.name]

	@property
	def category(self):
		return ("terrestrial plant | leaf | leaf - coniferous forest")
	
	_stomatalareanormalizedeffectivediffusionpathlength=200.0
	@property
	def stomatalareanormalizedeffectivediffusionpathlength(self):
		return self._stomatalareanormalizedeffectivediffusionpathlength
	@stomatalareanormalizedeffectivediffusionpathlength.setter
	def stomatalareanormalizedeffectivediffusionpathlength(self,value):
		self._stomatalareanormalizedeffectivediffusionpathlength=value

	@property
	def wetdepinterceptionfraction_calculated(self):
		return (0 if self.containingscenario.cumulativerain==0 else (self.leafwettingfactor * self.leafareaindex / self.containingscenario.cumulativerain) * (1-exp(-log(2) * self.containingscenario.cumulativerain / (3 * self.leafwettingfactor))))
	
	@property
	def concentrationoutputfactor(self):
		return (1000.0 / self.wetdensity)
	
	_wetmassperarea=2.0
	@property
	def wetmassperarea(self):
		return self._wetmassperarea
	@wetmassperarea.setter
	def wetmassperarea(self,value):
		self._wetmassperarea=value

	@property
	def concentrationoutputunits(self):
		return ("mg/kg wet weight")
	

	@property
	def air_z_total(self):
		cdict={}
		try:
			cdict["chem_2_3_7_8_tcdd"]=self.currentchemical.z_pureair * (1 - self.dustload / self.dustdensity) * (1+self.chemical_particlegaspartitioncoefficient * self.dustload * self.constants.ug_per_kg)
		except:
			cdict["chem_2_3_7_8_tcdd"]=nan
		
		return cdict

	@property
	def chemical_air_z_total(self):
		return self.air_z_total[self.currentchemical.name]

	@property
	def chemical_air_z_total(self):
		return self.air_z_total[self.currentchemical.name]


	@property
	def initialconcentration_g_per_kg_usersupplied(self):
		cdict={}
		try:
			cdict["chem_2_3_7_8_tcdd"]=0.0
		except:
			cdict["chem_2_3_7_8_tcdd"]=nan
		
		return cdict

	@property
	def chemical_initialconcentration_g_per_kg_usersupplied(self):
		return self.initialconcentration_g_per_kg_usersupplied[self.currentchemical.name]

	@property
	def chemical_initialconcentration_g_per_kg_usersupplied(self):
		return self.initialconcentration_g_per_kg_usersupplied[self.currentchemical.name]

	@property
	def isday_forair(self):
		return (self.containingscenario.isday_steadystate_forair if self.containingscenario.simulatesteadystate == 1 else self.containingscenario.isday_dynamic)
	

	@property
	def z_total(self):
		cdict={}
		try:
			cdict["chem_2_3_7_8_tcdd"]=0.18* self.currentchemical.z_pureair + 0.8*self.currentchemical.z_purewater + 0.02*self.currentchemical.k_ow*self.currentchemical.z_purewater
		except:
			cdict["chem_2_3_7_8_tcdd"]=nan
		
		return cdict

	@property
	def chemical_z_total(self):
		return self.z_total[self.currentchemical.name]

	@property
	def chemical_z_total(self):
		return self.z_total[self.currentchemical.name]

	_averageleafareaindex_no_time_dependence=5.0
	@property
	def averageleafareaindex_no_time_dependence(self):
		return self._averageleafareaindex_no_time_dependence
	@averageleafareaindex_no_time_dependence.setter
	def averageleafareaindex_no_time_dependence(self,value):
		self._averageleafareaindex_no_time_dependence=value


	@property
	def mesophyllconductance(self):
		cdict={}
		return cdict

	@property
	def chemical_mesophyllconductance(self):
		return self.mesophyllconductance[self.currentchemical.name]

	@property
	def chemical_mesophyllconductance(self):
		return self.mesophyllconductance[self.currentchemical.name]


	@property
	def oxidationrate(self):
		cdict={}
		return cdict

	@property
	def chemical_oxidationrate(self):
		return self.oxidationrate[self.currentchemical.name]

	@property
	def chemical_oxidationrate(self):
		return self.oxidationrate[self.currentchemical.name]


	@property
	def cuticularconductance(self):
		cdict={}
		try:
			cdict["chem_2_3_7_8_tcdd"]=86400 * 10 ** (0.704 * self.currentchemical.log10_k_ow - 11.2) / (self.chemical_air_z_total / self.currentchemical.z_purewater)
		except:
			cdict["chem_2_3_7_8_tcdd"]=nan
		
		return cdict

	@property
	def chemical_cuticularconductance(self):
		return self.cuticularconductance[self.currentchemical.name]

	@property
	def chemical_cuticularconductance(self):
		return self.cuticularconductance[self.currentchemical.name]

	_wetdensity=820.0
	@property
	def wetdensity(self):
		return self._wetdensity
	@wetdensity.setter
	def wetdensity(self,value):
		self._wetdensity=value

	@property
	def allowexchange_forother(self):
		return (self.allowexchange_steadystate_forother if self.containingscenario.simulatesteadystate == 1 else 1)
	
	@property
	def drymassperarea(self):
		return (self.wetmassperarea*(1-self.watercontent))
	
	_attenuationfactor=2.9
	@property
	def attenuationfactor(self):
		return self._attenuationfactor
	@attenuationfactor.setter
	def attenuationfactor(self,value):
		self._attenuationfactor=value

	_lengthofleaf=0.01
	@property
	def lengthofleaf(self):
		return self._lengthofleaf
	@lengthofleaf.setter
	def lengthofleaf(self,value):
		self._lengthofleaf=value


	@property
	def generaldegradationrate(self):
		cdict={}
		try:
			cdict["chem_2_3_7_8_tcdd"]=log(2)/ self.chemical_halflife
		except:
			cdict["chem_2_3_7_8_tcdd"]=nan
		
		return cdict

	@property
	def chemical_generaldegradationrate(self):
		return self.generaldegradationrate[self.currentchemical.name]

	@property
	def chemical_generaldegradationrate(self):
		return self.generaldegradationrate[self.currentchemical.name]

	@property
	def thicknessofboundarylayerthicknessthroughstillair(self):
		return (0.00389*sqrt(self.lengthofleaf/self.containingscenario.horizontalwindspeed))
	
	_correctionexponent=0.76
	@property
	def correctionexponent(self):
		return self._correctionexponent
	@correctionexponent.setter
	def correctionexponent(self,value):
		self._correctionexponent=value


	@property
	def stomataconductance(self):
		cdict={}
		try:
			cdict["chem_2_3_7_8_tcdd"]=self.currentchemical.d_pureair * self.stomatalareanormalizedeffectivediffusionpathlength * self.degreestomatalopening
		except:
			cdict["chem_2_3_7_8_tcdd"]=nan
		
		return cdict

	@property
	def chemical_stomataconductance(self):
		return self.stomataconductance[self.currentchemical.name]

	@property
	def chemical_stomataconductance(self):
		return self.stomataconductance[self.currentchemical.name]

	@property
	def allowexchange_forair(self):
		return (self.allowexchange_steadystate_forair if self.containingscenario.simulatesteadystate == 1 else 1)
	
	@property
	def totalmass(self):
		return (self.volume*self.wetdensity)
	

	@property
	def particlegaspartitioncoefficient(self):
		cdict={}
		try:
			cdict["chem_2_3_7_8_tcdd"]=10** ( self.currentchemical.log10_k_oa  + log(self.fractionorganicmatteronparticulates+1.0e-10)/log(10) - 11.91)
		except:
			cdict["chem_2_3_7_8_tcdd"]=nan
		
		return cdict

	@property
	def chemical_particlegaspartitioncoefficient(self):
		return self.particlegaspartitioncoefficient[self.currentchemical.name]

	@property
	def chemical_particlegaspartitioncoefficient(self):
		return self.particlegaspartitioncoefficient[self.currentchemical.name]


	@property
	def totalstomatalconductance(self):
		cdict={}
		try:
			cdict["chem_2_3_7_8_tcdd"]=1.0 / ((1.0 / self.chemical_stomataconductance) + (1.0 / self.chemical_boundarylayerconductance))
		except:
			cdict["chem_2_3_7_8_tcdd"]=nan
		
		return cdict

	@property
	def chemical_totalstomatalconductance(self):
		return self.totalstomatalconductance[self.currentchemical.name]

	@property
	def chemical_totalstomatalconductance(self):
		return self.totalstomatalconductance[self.currentchemical.name]


	@property
	def initialconcentration_g_per_kg(self):
		cdict={}
		try:
			cdict["chem_2_3_7_8_tcdd"]=self.containingscenario.fractioninitialconcentrations * self.chemical_initialconcentration_g_per_kg_usersupplied
		except:
			cdict["chem_2_3_7_8_tcdd"]=nan
		
		return cdict

	@property
	def chemical_initialconcentration_g_per_kg(self):
		return self.initialconcentration_g_per_kg[self.currentchemical.name]

	@property
	def chemical_initialconcentration_g_per_kg(self):
		return self.initialconcentration_g_per_kg[self.currentchemical.name]

	_dustload=6.15e-8
	@property
	def dustload(self):
		return self._dustload
	@dustload.setter
	def dustload(self,value):
		self._dustload=value

	_isbiotic=False
	@property
	def isbiotic(self):
		return self._isbiotic
	@isbiotic.setter
	def isbiotic(self,value):
		self._isbiotic=value

	@property
	def image(self):
		return ("c:\models\trim\data\images\leaf.gif")
	

	@property
	def methylationrate(self):
		cdict={}
		return cdict

	@property
	def chemical_methylationrate(self):
		return self.methylationrate[self.currentchemical.name]

	@property
	def chemical_methylationrate(self):
		return self.methylationrate[self.currentchemical.name]

	_watercontent=0.8
	@property
	def watercontent(self):
		return self._watercontent
	@watercontent.setter
	def watercontent(self,value):
		self._watercontent=value

	_wetdepinterceptionfraction_usersupplied=0.2
	@property
	def wetdepinterceptionfraction_usersupplied(self):
		return self._wetdepinterceptionfraction_usersupplied
	@wetdepinterceptionfraction_usersupplied.setter
	def wetdepinterceptionfraction_usersupplied(self,value):
		self._wetdepinterceptionfraction_usersupplied=value

	_dustdensity=1400.0
	@property
	def dustdensity(self):
		return self._dustdensity
	@dustdensity.setter
	def dustdensity(self,value):
		self._dustdensity=value

	_calculatewetdepinterceptionfraction=False
	@property
	def calculatewetdepinterceptionfraction(self):
		return self._calculatewetdepinterceptionfraction
	@calculatewetdepinterceptionfraction.setter
	def calculatewetdepinterceptionfraction(self,value):
		self._calculatewetdepinterceptionfraction=value

	@property
	def density(self):
		return (self.wetdensity)
	
	@property
	def volume(self):
		return (self.wetvolumeperarea * self.containingvolumeelement.area if self.allowexchange_forother > 0 else 0)
	
	_degreestomatalopening=1.0
	@property
	def degreestomatalopening(self):
		return self._degreestomatalopening
	@degreestomatalopening.setter
	def degreestomatalopening(self,value):
		self._degreestomatalopening=value


	@property
	def boundarylayerconductance(self):
		cdict={}
		try:
			cdict["chem_2_3_7_8_tcdd"]=self.currentchemical.d_pureair/self.thicknessofboundarylayerthicknessthroughstillair
		except:
			cdict["chem_2_3_7_8_tcdd"]=nan
		
		return cdict

	@property
	def chemical_boundarylayerconductance(self):
		return self.boundarylayerconductance[self.currentchemical.name]

	@property
	def chemical_boundarylayerconductance(self):
		return self.boundarylayerconductance[self.currentchemical.name]

class leaf_deciduous_forest_in_deciduous_forest:
	def __init__(self,constants,containingscenario,currentchemical,containingvolumeelement,comp_objects_dict):
		self.containingscenario=containingscenario
		self.currentchemical=currentchemical
		self.constants=constants
		self.containingvolumeelement=containingvolumeelement
		self.comp_objects_dict=comp_objects_dict
	@property
	def acceptableabiotic(self):
		return ("abiotic | soil | surface soil")
	
	@property
	def wetdepinterceptionfraction(self):
		return (self.wetdepinterceptionfraction_calculated if self.calculatewetdepinterceptionfraction==1 else self.wetdepinterceptionfraction_usersupplied)
	
	@property
	def dryvolumeperarea(self):
		return (self.wetvolumeperarea*(1 - self.watercontent))
	

	@property
	def demethylationrate(self):
		cdict={}
		return cdict

	@property
	def chemical_demethylationrate(self):
		return self.demethylationrate[self.currentchemical.name]

	@property
	def chemical_demethylationrate(self):
		return self.demethylationrate[self.currentchemical.name]

	_fractionorganicmatteronparticulates=0.2
	@property
	def fractionorganicmatteronparticulates(self):
		return self._fractionorganicmatteronparticulates
	@fractionorganicmatteronparticulates.setter
	def fractionorganicmatteronparticulates(self,value):
		self._fractionorganicmatteronparticulates=value


	@property
	def transferfactortoleafparticle(self):
		cdict={}
		try:
			cdict["chem_2_3_7_8_tcdd"]=0.003
		except:
			cdict["chem_2_3_7_8_tcdd"]=nan
		
		return cdict

	@property
	def chemical_transferfactortoleafparticle(self):
		return self.transferfactortoleafparticle[self.currentchemical.name]

	@property
	def chemical_transferfactortoleafparticle(self):
		return self.transferfactortoleafparticle[self.currentchemical.name]

	_litterfallrate=0.01
	@property
	def litterfallrate(self):
		return self._litterfallrate
	@litterfallrate.setter
	def litterfallrate(self,value):
		self._litterfallrate=value


	@property
	def reductionrate(self):
		cdict={}
		return cdict

	@property
	def chemical_reductionrate(self):
		return self.reductionrate[self.currentchemical.name]

	@property
	def chemical_reductionrate(self):
		return self.reductionrate[self.currentchemical.name]

	@property
	def drydepinterceptionfraction(self):
		return ((1 - exp(-self.attenuationfactor * self.drymassperarea)))
	
	_leafwettingfactor=3.0e-4
	@property
	def leafwettingfactor(self):
		return self._leafwettingfactor
	@leafwettingfactor.setter
	def leafwettingfactor(self,value):
		self._leafwettingfactor=value

	@property
	def isday_forother(self):
		return (self.containingscenario.isday_steadystate_forother if self.containingscenario.simulatesteadystate == 1 else self.containingscenario.isday_dynamic)
	
	@property
	def leafarea(self):
		return (self.leafareaindex*self.containingvolumeelement.area)
	

	@property
	def totalcuticularconductance(self):
		cdict={}
		try:
			cdict["chem_2_3_7_8_tcdd"]=1/(1.0/self.chemical_cuticularconductance  + 1.0/self.chemical_boundarylayerconductance)
		except:
			cdict["chem_2_3_7_8_tcdd"]=nan
		
		return cdict

	@property
	def chemical_totalcuticularconductance(self):
		return self.totalcuticularconductance[self.currentchemical.name]

	@property
	def chemical_totalcuticularconductance(self):
		return self.totalcuticularconductance[self.currentchemical.name]

	@property
	def wetvolumeperarea(self):
		return (self.wetmassperarea/self.wetdensity)
	
	@property
	def leafareaindex(self):
		return (self.averageleafareaindex_no_time_dependence)
	
	_lipidcontent=0.00224
	@property
	def lipidcontent(self):
		return self._lipidcontent
	@lipidcontent.setter
	def lipidcontent(self,value):
		self._lipidcontent=value


	@property
	def halflife(self):
		cdict={}
		try:
			cdict["chem_2_3_7_8_tcdd"]=70.0
		except:
			cdict["chem_2_3_7_8_tcdd"]=nan
		
		return cdict

	@property
	def chemical_halflife(self):
		return self.halflife[self.currentchemical.name]

	@property
	def chemical_halflife(self):
		return self.halflife[self.currentchemical.name]

	@property
	def category(self):
		return ("terrestrial plant | leaf | leaf - deciduous forest")
	
	_stomatalareanormalizedeffectivediffusionpathlength=200.0
	@property
	def stomatalareanormalizedeffectivediffusionpathlength(self):
		return self._stomatalareanormalizedeffectivediffusionpathlength
	@stomatalareanormalizedeffectivediffusionpathlength.setter
	def stomatalareanormalizedeffectivediffusionpathlength(self,value):
		self._stomatalareanormalizedeffectivediffusionpathlength=value

	@property
	def wetdepinterceptionfraction_calculated(self):
		return (0 if self.containingscenario.cumulativerain==0 else (self.leafwettingfactor * self.leafareaindex / self.containingscenario.cumulativerain) * (1-exp(-log(2) * self.containingscenario.cumulativerain / (3 * self.leafwettingfactor))))
	
	@property
	def concentrationoutputfactor(self):
		return (1000.0 / self.wetdensity)
	
	_wetmassperarea=0.6
	@property
	def wetmassperarea(self):
		return self._wetmassperarea
	@wetmassperarea.setter
	def wetmassperarea(self,value):
		self._wetmassperarea=value

	@property
	def concentrationoutputunits(self):
		return ("mg/kg wet weight")
	

	@property
	def air_z_total(self):
		cdict={}
		try:
			cdict["chem_2_3_7_8_tcdd"]=self.currentchemical.z_pureair * (1 - self.dustload / self.dustdensity) * (1+self.chemical_particlegaspartitioncoefficient * self.dustload * self.constants.ug_per_kg)
		except:
			cdict["chem_2_3_7_8_tcdd"]=nan
		
		return cdict

	@property
	def chemical_air_z_total(self):
		return self.air_z_total[self.currentchemical.name]

	@property
	def chemical_air_z_total(self):
		return self.air_z_total[self.currentchemical.name]


	@property
	def initialconcentration_g_per_kg_usersupplied(self):
		cdict={}
		try:
			cdict["chem_2_3_7_8_tcdd"]=0.0
		except:
			cdict["chem_2_3_7_8_tcdd"]=nan
		
		return cdict

	@property
	def chemical_initialconcentration_g_per_kg_usersupplied(self):
		return self.initialconcentration_g_per_kg_usersupplied[self.currentchemical.name]

	@property
	def chemical_initialconcentration_g_per_kg_usersupplied(self):
		return self.initialconcentration_g_per_kg_usersupplied[self.currentchemical.name]

	@property
	def isday_forair(self):
		return (self.containingscenario.isday_steadystate_forair if self.containingscenario.simulatesteadystate == 1 else self.containingscenario.isday_dynamic)
	

	@property
	def z_total(self):
		cdict={}
		try:
			cdict["chem_2_3_7_8_tcdd"]=0.18* self.currentchemical.z_pureair + 0.8*self.currentchemical.z_purewater + 0.02*self.currentchemical.k_ow*self.currentchemical.z_purewater
		except:
			cdict["chem_2_3_7_8_tcdd"]=nan
		
		return cdict

	@property
	def chemical_z_total(self):
		return self.z_total[self.currentchemical.name]

	@property
	def chemical_z_total(self):
		return self.z_total[self.currentchemical.name]

	_averageleafareaindex_no_time_dependence=3.4
	@property
	def averageleafareaindex_no_time_dependence(self):
		return self._averageleafareaindex_no_time_dependence
	@averageleafareaindex_no_time_dependence.setter
	def averageleafareaindex_no_time_dependence(self,value):
		self._averageleafareaindex_no_time_dependence=value


	@property
	def mesophyllconductance(self):
		cdict={}
		return cdict

	@property
	def chemical_mesophyllconductance(self):
		return self.mesophyllconductance[self.currentchemical.name]

	@property
	def chemical_mesophyllconductance(self):
		return self.mesophyllconductance[self.currentchemical.name]


	@property
	def oxidationrate(self):
		cdict={}
		return cdict

	@property
	def chemical_oxidationrate(self):
		return self.oxidationrate[self.currentchemical.name]

	@property
	def chemical_oxidationrate(self):
		return self.oxidationrate[self.currentchemical.name]


	@property
	def cuticularconductance(self):
		cdict={}
		try:
			cdict["chem_2_3_7_8_tcdd"]=86400 * 10 ** (0.704 * self.currentchemical.log10_k_ow - 11.2) / (self.chemical_air_z_total / self.currentchemical.z_purewater)
		except:
			cdict["chem_2_3_7_8_tcdd"]=nan
		
		return cdict

	@property
	def chemical_cuticularconductance(self):
		return self.cuticularconductance[self.currentchemical.name]

	@property
	def chemical_cuticularconductance(self):
		return self.cuticularconductance[self.currentchemical.name]

	_wetdensity=820.0
	@property
	def wetdensity(self):
		return self._wetdensity
	@wetdensity.setter
	def wetdensity(self,value):
		self._wetdensity=value

	@property
	def allowexchange_forother(self):
		return (self.allowexchange_steadystate_forother if self.containingscenario.simulatesteadystate == 1 else wt_av_allowexchange)
	
	@property
	def drymassperarea(self):
		return (self.wetmassperarea*(1-self.watercontent))
	
	_attenuationfactor=2.9
	@property
	def attenuationfactor(self):
		return self._attenuationfactor
	@attenuationfactor.setter
	def attenuationfactor(self,value):
		self._attenuationfactor=value

	_lengthofleaf=0.1
	@property
	def lengthofleaf(self):
		return self._lengthofleaf
	@lengthofleaf.setter
	def lengthofleaf(self,value):
		self._lengthofleaf=value


	@property
	def generaldegradationrate(self):
		cdict={}
		try:
			cdict["chem_2_3_7_8_tcdd"]=log(2)/ self.chemical_halflife
		except:
			cdict["chem_2_3_7_8_tcdd"]=nan
		
		return cdict

	@property
	def chemical_generaldegradationrate(self):
		return self.generaldegradationrate[self.currentchemical.name]

	@property
	def chemical_generaldegradationrate(self):
		return self.generaldegradationrate[self.currentchemical.name]

	@property
	def thicknessofboundarylayerthicknessthroughstillair(self):
		return (0.00389*sqrt(self.lengthofleaf/self.containingscenario.horizontalwindspeed))
	
	_correctionexponent=0.76
	@property
	def correctionexponent(self):
		return self._correctionexponent
	@correctionexponent.setter
	def correctionexponent(self,value):
		self._correctionexponent=value


	@property
	def stomataconductance(self):
		cdict={}
		try:
			cdict["chem_2_3_7_8_tcdd"]=self.currentchemical.d_pureair * self.stomatalareanormalizedeffectivediffusionpathlength * self.degreestomatalopening
		except:
			cdict["chem_2_3_7_8_tcdd"]=nan
		
		return cdict

	@property
	def chemical_stomataconductance(self):
		return self.stomataconductance[self.currentchemical.name]

	@property
	def chemical_stomataconductance(self):
		return self.stomataconductance[self.currentchemical.name]

	@property
	def allowexchange_forair(self):
		return (self.allowexchange_steadystate_forair if self.containingscenario.simulatesteadystate == 1 else wt_av_allowexchange)
	
	@property
	def totalmass(self):
		return (self.volume*self.wetdensity)
	

	@property
	def particlegaspartitioncoefficient(self):
		cdict={}
		try:
			cdict["chem_2_3_7_8_tcdd"]=10** ( self.currentchemical.log10_k_oa  + log(self.fractionorganicmatteronparticulates+1.0e-10)/log(10) - 11.91)
		except:
			cdict["chem_2_3_7_8_tcdd"]=nan
		
		return cdict

	@property
	def chemical_particlegaspartitioncoefficient(self):
		return self.particlegaspartitioncoefficient[self.currentchemical.name]

	@property
	def chemical_particlegaspartitioncoefficient(self):
		return self.particlegaspartitioncoefficient[self.currentchemical.name]


	@property
	def totalstomatalconductance(self):
		cdict={}
		try:
			cdict["chem_2_3_7_8_tcdd"]=1.0 / ((1.0 / self.chemical_stomataconductance) + (1.0 / self.chemical_boundarylayerconductance))
		except:
			cdict["chem_2_3_7_8_tcdd"]=nan
		
		return cdict

	@property
	def chemical_totalstomatalconductance(self):
		return self.totalstomatalconductance[self.currentchemical.name]

	@property
	def chemical_totalstomatalconductance(self):
		return self.totalstomatalconductance[self.currentchemical.name]


	@property
	def initialconcentration_g_per_kg(self):
		cdict={}
		try:
			cdict["chem_2_3_7_8_tcdd"]=self.containingscenario.fractioninitialconcentrations * self.chemical_initialconcentration_g_per_kg_usersupplied
		except:
			cdict["chem_2_3_7_8_tcdd"]=nan
		
		return cdict

	@property
	def chemical_initialconcentration_g_per_kg(self):
		return self.initialconcentration_g_per_kg[self.currentchemical.name]

	@property
	def chemical_initialconcentration_g_per_kg(self):
		return self.initialconcentration_g_per_kg[self.currentchemical.name]

	_dustload=6.15e-8
	@property
	def dustload(self):
		return self._dustload
	@dustload.setter
	def dustload(self,value):
		self._dustload=value

	_isbiotic=False
	@property
	def isbiotic(self):
		return self._isbiotic
	@isbiotic.setter
	def isbiotic(self,value):
		self._isbiotic=value

	@property
	def image(self):
		return ("c:\models\trim\data\images\leaf.gif")
	

	@property
	def methylationrate(self):
		cdict={}
		return cdict

	@property
	def chemical_methylationrate(self):
		return self.methylationrate[self.currentchemical.name]

	@property
	def chemical_methylationrate(self):
		return self.methylationrate[self.currentchemical.name]

	_watercontent=0.8
	@property
	def watercontent(self):
		return self._watercontent
	@watercontent.setter
	def watercontent(self,value):
		self._watercontent=value

	_wetdepinterceptionfraction_usersupplied=0.2
	@property
	def wetdepinterceptionfraction_usersupplied(self):
		return self._wetdepinterceptionfraction_usersupplied
	@wetdepinterceptionfraction_usersupplied.setter
	def wetdepinterceptionfraction_usersupplied(self,value):
		self._wetdepinterceptionfraction_usersupplied=value

	_dustdensity=1400.0
	@property
	def dustdensity(self):
		return self._dustdensity
	@dustdensity.setter
	def dustdensity(self,value):
		self._dustdensity=value

	_calculatewetdepinterceptionfraction=False
	@property
	def calculatewetdepinterceptionfraction(self):
		return self._calculatewetdepinterceptionfraction
	@calculatewetdepinterceptionfraction.setter
	def calculatewetdepinterceptionfraction(self,value):
		self._calculatewetdepinterceptionfraction=value

	@property
	def density(self):
		return (self.wetdensity)
	
	@property
	def volume(self):
		return (self.wetvolumeperarea * self.containingvolumeelement.area if self.allowexchange_forother > 0 else 0)
	
	_degreestomatalopening=1.0
	@property
	def degreestomatalopening(self):
		return self._degreestomatalopening
	@degreestomatalopening.setter
	def degreestomatalopening(self,value):
		self._degreestomatalopening=value


	@property
	def boundarylayerconductance(self):
		cdict={}
		try:
			cdict["chem_2_3_7_8_tcdd"]=self.currentchemical.d_pureair/self.thicknessofboundarylayerthicknessthroughstillair
		except:
			cdict["chem_2_3_7_8_tcdd"]=nan
		
		return cdict

	@property
	def chemical_boundarylayerconductance(self):
		return self.boundarylayerconductance[self.currentchemical.name]

	@property
	def chemical_boundarylayerconductance(self):
		return self.boundarylayerconductance[self.currentchemical.name]

class leaf_grasses_herbs_in_grasses_herbs:
	def __init__(self,constants,containingscenario,currentchemical,containingvolumeelement,comp_objects_dict):
		self.containingscenario=containingscenario
		self.currentchemical=currentchemical
		self.constants=constants
		self.containingvolumeelement=containingvolumeelement
		self.comp_objects_dict=comp_objects_dict
	@property
	def acceptableabiotic(self):
		return ("abiotic | soil | surface soil")
	
	@property
	def wetdepinterceptionfraction(self):
		return (self.wetdepinterceptionfraction_calculated if self.calculatewetdepinterceptionfraction==1 else self.wetdepinterceptionfraction_usersupplied)
	
	@property
	def dryvolumeperarea(self):
		return (self.wetvolumeperarea*(1 - self.watercontent))
	

	@property
	def demethylationrate(self):
		cdict={}
		return cdict

	@property
	def chemical_demethylationrate(self):
		return self.demethylationrate[self.currentchemical.name]

	@property
	def chemical_demethylationrate(self):
		return self.demethylationrate[self.currentchemical.name]

	_fractionorganicmatteronparticulates=0.2
	@property
	def fractionorganicmatteronparticulates(self):
		return self._fractionorganicmatteronparticulates
	@fractionorganicmatteronparticulates.setter
	def fractionorganicmatteronparticulates(self,value):
		self._fractionorganicmatteronparticulates=value


	@property
	def transferfactortoleafparticle(self):
		cdict={}
		try:
			cdict["chem_2_3_7_8_tcdd"]=0.003
		except:
			cdict["chem_2_3_7_8_tcdd"]=nan
		
		return cdict

	@property
	def chemical_transferfactortoleafparticle(self):
		return self.transferfactortoleafparticle[self.currentchemical.name]

	@property
	def chemical_transferfactortoleafparticle(self):
		return self.transferfactortoleafparticle[self.currentchemical.name]

	_litterfallrate=0.01
	@property
	def litterfallrate(self):
		return self._litterfallrate
	@litterfallrate.setter
	def litterfallrate(self,value):
		self._litterfallrate=value


	@property
	def reductionrate(self):
		cdict={}
		return cdict

	@property
	def chemical_reductionrate(self):
		return self.reductionrate[self.currentchemical.name]

	@property
	def chemical_reductionrate(self):
		return self.reductionrate[self.currentchemical.name]

	@property
	def drydepinterceptionfraction(self):
		return ((1 - exp(-self.attenuationfactor * self.drymassperarea)))
	
	_leafwettingfactor=3.0e-4
	@property
	def leafwettingfactor(self):
		return self._leafwettingfactor
	@leafwettingfactor.setter
	def leafwettingfactor(self,value):
		self._leafwettingfactor=value

	@property
	def isday_forother(self):
		return (self.containingscenario.isday_steadystate_forother if self.containingscenario.simulatesteadystate == 1 else self.containingscenario.isday_dynamic)
	
	@property
	def leafarea(self):
		return (self.leafareaindex*self.containingvolumeelement.area)
	

	@property
	def totalcuticularconductance(self):
		cdict={}
		try:
			cdict["chem_2_3_7_8_tcdd"]=1/(1.0/self.chemical_cuticularconductance  + 1.0/self.chemical_boundarylayerconductance)
		except:
			cdict["chem_2_3_7_8_tcdd"]=nan
		
		return cdict

	@property
	def chemical_totalcuticularconductance(self):
		return self.totalcuticularconductance[self.currentchemical.name]

	@property
	def chemical_totalcuticularconductance(self):
		return self.totalcuticularconductance[self.currentchemical.name]

	@property
	def wetvolumeperarea(self):
		return (self.wetmassperarea/self.wetdensity)
	
	@property
	def leafareaindex(self):
		return (self.averageleafareaindex_no_time_dependence)
	
	_lipidcontent=0.00224
	@property
	def lipidcontent(self):
		return self._lipidcontent
	@lipidcontent.setter
	def lipidcontent(self,value):
		self._lipidcontent=value


	@property
	def halflife(self):
		cdict={}
		try:
			cdict["chem_2_3_7_8_tcdd"]=70.0
		except:
			cdict["chem_2_3_7_8_tcdd"]=nan
		
		return cdict

	@property
	def chemical_halflife(self):
		return self.halflife[self.currentchemical.name]

	@property
	def chemical_halflife(self):
		return self.halflife[self.currentchemical.name]

	@property
	def category(self):
		return ("terrestrial plant | leaf | leaf - grasses/herbs")
	
	_stomatalareanormalizedeffectivediffusionpathlength=200.0
	@property
	def stomatalareanormalizedeffectivediffusionpathlength(self):
		return self._stomatalareanormalizedeffectivediffusionpathlength
	@stomatalareanormalizedeffectivediffusionpathlength.setter
	def stomatalareanormalizedeffectivediffusionpathlength(self,value):
		self._stomatalareanormalizedeffectivediffusionpathlength=value

	@property
	def wetdepinterceptionfraction_calculated(self):
		return (0 if self.containingscenario.cumulativerain==0 else (self.leafwettingfactor * self.leafareaindex / self.containingscenario.cumulativerain) * (1-exp(-log(2) * self.containingscenario.cumulativerain / (3 * self.leafwettingfactor))))
	
	@property
	def concentrationoutputfactor(self):
		return (1000.0 / self.wetdensity)
	
	_wetmassperarea=0.6
	@property
	def wetmassperarea(self):
		return self._wetmassperarea
	@wetmassperarea.setter
	def wetmassperarea(self,value):
		self._wetmassperarea=value

	@property
	def concentrationoutputunits(self):
		return ("mg/kg wet weight")
	

	@property
	def air_z_total(self):
		cdict={}
		try:
			cdict["chem_2_3_7_8_tcdd"]=self.currentchemical.z_pureair * (1 - self.dustload / self.dustdensity) * (1+self.chemical_particlegaspartitioncoefficient * self.dustload * self.constants.ug_per_kg)
		except:
			cdict["chem_2_3_7_8_tcdd"]=nan
		
		return cdict

	@property
	def chemical_air_z_total(self):
		return self.air_z_total[self.currentchemical.name]

	@property
	def chemical_air_z_total(self):
		return self.air_z_total[self.currentchemical.name]


	@property
	def initialconcentration_g_per_kg_usersupplied(self):
		cdict={}
		try:
			cdict["chem_2_3_7_8_tcdd"]=0.0
		except:
			cdict["chem_2_3_7_8_tcdd"]=nan
		
		return cdict

	@property
	def chemical_initialconcentration_g_per_kg_usersupplied(self):
		return self.initialconcentration_g_per_kg_usersupplied[self.currentchemical.name]

	@property
	def chemical_initialconcentration_g_per_kg_usersupplied(self):
		return self.initialconcentration_g_per_kg_usersupplied[self.currentchemical.name]

	@property
	def isday_forair(self):
		return (self.containingscenario.isday_steadystate_forair if self.containingscenario.simulatesteadystate == 1 else self.containingscenario.isday_dynamic)
	

	@property
	def z_total(self):
		cdict={}
		try:
			cdict["chem_2_3_7_8_tcdd"]=0.18* self.currentchemical.z_pureair + 0.8*self.currentchemical.z_purewater + 0.02*self.currentchemical.k_ow*self.currentchemical.z_purewater
		except:
			cdict["chem_2_3_7_8_tcdd"]=nan
		
		return cdict

	@property
	def chemical_z_total(self):
		return self.z_total[self.currentchemical.name]

	@property
	def chemical_z_total(self):
		return self.z_total[self.currentchemical.name]

	_averageleafareaindex_no_time_dependence=5.0
	@property
	def averageleafareaindex_no_time_dependence(self):
		return self._averageleafareaindex_no_time_dependence
	@averageleafareaindex_no_time_dependence.setter
	def averageleafareaindex_no_time_dependence(self,value):
		self._averageleafareaindex_no_time_dependence=value


	@property
	def mesophyllconductance(self):
		cdict={}
		return cdict

	@property
	def chemical_mesophyllconductance(self):
		return self.mesophyllconductance[self.currentchemical.name]

	@property
	def chemical_mesophyllconductance(self):
		return self.mesophyllconductance[self.currentchemical.name]


	@property
	def oxidationrate(self):
		cdict={}
		return cdict

	@property
	def chemical_oxidationrate(self):
		return self.oxidationrate[self.currentchemical.name]

	@property
	def chemical_oxidationrate(self):
		return self.oxidationrate[self.currentchemical.name]


	@property
	def cuticularconductance(self):
		cdict={}
		try:
			cdict["chem_2_3_7_8_tcdd"]=86400 * 10 ** (0.704 * self.currentchemical.log10_k_ow - 11.2) / (self.chemical_air_z_total / self.currentchemical.z_purewater)
		except:
			cdict["chem_2_3_7_8_tcdd"]=nan
		
		return cdict

	@property
	def chemical_cuticularconductance(self):
		return self.cuticularconductance[self.currentchemical.name]

	@property
	def chemical_cuticularconductance(self):
		return self.cuticularconductance[self.currentchemical.name]

	_wetdensity=820.0
	@property
	def wetdensity(self):
		return self._wetdensity
	@wetdensity.setter
	def wetdensity(self,value):
		self._wetdensity=value

	@property
	def allowexchange_forother(self):
		return (self.allowexchange_steadystate_forother if self.containingscenario.simulatesteadystate == 1 else wt_av_allowexchange)
	
	@property
	def drymassperarea(self):
		return (self.wetmassperarea*(1-self.watercontent))
	
	_attenuationfactor=2.9
	@property
	def attenuationfactor(self):
		return self._attenuationfactor
	@attenuationfactor.setter
	def attenuationfactor(self,value):
		self._attenuationfactor=value

	_lengthofleaf=0.05
	@property
	def lengthofleaf(self):
		return self._lengthofleaf
	@lengthofleaf.setter
	def lengthofleaf(self,value):
		self._lengthofleaf=value


	@property
	def generaldegradationrate(self):
		cdict={}
		try:
			cdict["chem_2_3_7_8_tcdd"]=log(2)/ self.chemical_halflife
		except:
			cdict["chem_2_3_7_8_tcdd"]=nan
		
		return cdict

	@property
	def chemical_generaldegradationrate(self):
		return self.generaldegradationrate[self.currentchemical.name]

	@property
	def chemical_generaldegradationrate(self):
		return self.generaldegradationrate[self.currentchemical.name]

	@property
	def thicknessofboundarylayerthicknessthroughstillair(self):
		return (0.00389*sqrt(self.lengthofleaf/self.containingscenario.horizontalwindspeed))
	
	_correctionexponent=0.76
	@property
	def correctionexponent(self):
		return self._correctionexponent
	@correctionexponent.setter
	def correctionexponent(self,value):
		self._correctionexponent=value


	@property
	def stomataconductance(self):
		cdict={}
		try:
			cdict["chem_2_3_7_8_tcdd"]=self.currentchemical.d_pureair * self.stomatalareanormalizedeffectivediffusionpathlength * self.degreestomatalopening
		except:
			cdict["chem_2_3_7_8_tcdd"]=nan
		
		return cdict

	@property
	def chemical_stomataconductance(self):
		return self.stomataconductance[self.currentchemical.name]

	@property
	def chemical_stomataconductance(self):
		return self.stomataconductance[self.currentchemical.name]

	@property
	def allowexchange_forair(self):
		return (self.allowexchange_steadystate_forair if self.containingscenario.simulatesteadystate == 1 else wt_av_allowexchange)
	
	@property
	def totalmass(self):
		return (self.volume*self.wetdensity)
	

	@property
	def particlegaspartitioncoefficient(self):
		cdict={}
		try:
			cdict["chem_2_3_7_8_tcdd"]=10** ( self.currentchemical.log10_k_oa  + log(self.fractionorganicmatteronparticulates+1.0e-10)/log(10) - 11.91)
		except:
			cdict["chem_2_3_7_8_tcdd"]=nan
		
		return cdict

	@property
	def chemical_particlegaspartitioncoefficient(self):
		return self.particlegaspartitioncoefficient[self.currentchemical.name]

	@property
	def chemical_particlegaspartitioncoefficient(self):
		return self.particlegaspartitioncoefficient[self.currentchemical.name]


	@property
	def totalstomatalconductance(self):
		cdict={}
		try:
			cdict["chem_2_3_7_8_tcdd"]=1.0 / ((1.0 / self.chemical_stomataconductance) + (1.0 / self.chemical_boundarylayerconductance))
		except:
			cdict["chem_2_3_7_8_tcdd"]=nan
		
		return cdict

	@property
	def chemical_totalstomatalconductance(self):
		return self.totalstomatalconductance[self.currentchemical.name]

	@property
	def chemical_totalstomatalconductance(self):
		return self.totalstomatalconductance[self.currentchemical.name]


	@property
	def initialconcentration_g_per_kg(self):
		cdict={}
		try:
			cdict["chem_2_3_7_8_tcdd"]=self.containingscenario.fractioninitialconcentrations * self.chemical_initialconcentration_g_per_kg_usersupplied
		except:
			cdict["chem_2_3_7_8_tcdd"]=nan
		
		return cdict

	@property
	def chemical_initialconcentration_g_per_kg(self):
		return self.initialconcentration_g_per_kg[self.currentchemical.name]

	@property
	def chemical_initialconcentration_g_per_kg(self):
		return self.initialconcentration_g_per_kg[self.currentchemical.name]

	_dustload=6.15e-8
	@property
	def dustload(self):
		return self._dustload
	@dustload.setter
	def dustload(self,value):
		self._dustload=value

	_isbiotic=False
	@property
	def isbiotic(self):
		return self._isbiotic
	@isbiotic.setter
	def isbiotic(self,value):
		self._isbiotic=value

	@property
	def image(self):
		return ("c:\models\trim\data\images\leaf.gif")
	

	@property
	def methylationrate(self):
		cdict={}
		return cdict

	@property
	def chemical_methylationrate(self):
		return self.methylationrate[self.currentchemical.name]

	@property
	def chemical_methylationrate(self):
		return self.methylationrate[self.currentchemical.name]

	_watercontent=0.8
	@property
	def watercontent(self):
		return self._watercontent
	@watercontent.setter
	def watercontent(self,value):
		self._watercontent=value

	_wetdepinterceptionfraction_usersupplied=0.2
	@property
	def wetdepinterceptionfraction_usersupplied(self):
		return self._wetdepinterceptionfraction_usersupplied
	@wetdepinterceptionfraction_usersupplied.setter
	def wetdepinterceptionfraction_usersupplied(self,value):
		self._wetdepinterceptionfraction_usersupplied=value

	_dustdensity=1400.0
	@property
	def dustdensity(self):
		return self._dustdensity
	@dustdensity.setter
	def dustdensity(self,value):
		self._dustdensity=value

	_calculatewetdepinterceptionfraction=False
	@property
	def calculatewetdepinterceptionfraction(self):
		return self._calculatewetdepinterceptionfraction
	@calculatewetdepinterceptionfraction.setter
	def calculatewetdepinterceptionfraction(self,value):
		self._calculatewetdepinterceptionfraction=value

	@property
	def density(self):
		return (self.wetdensity)
	
	@property
	def volume(self):
		return (self.wetvolumeperarea * self.containingvolumeelement.area if self.allowexchange_forother > 0 else 0)
	
	_degreestomatalopening=1.0
	@property
	def degreestomatalopening(self):
		return self._degreestomatalopening
	@degreestomatalopening.setter
	def degreestomatalopening(self,value):
		self._degreestomatalopening=value


	@property
	def boundarylayerconductance(self):
		cdict={}
		try:
			cdict["chem_2_3_7_8_tcdd"]=self.currentchemical.d_pureair/self.thicknessofboundarylayerthicknessthroughstillair
		except:
			cdict["chem_2_3_7_8_tcdd"]=nan
		
		return cdict

	@property
	def chemical_boundarylayerconductance(self):
		return self.boundarylayerconductance[self.currentchemical.name]

	@property
	def chemical_boundarylayerconductance(self):
		return self.boundarylayerconductance[self.currentchemical.name]

class leaf_particle_coniferous_forest_in_coniferous_forest:
	def __init__(self,constants,containingscenario,currentchemical,containingvolumeelement,comp_objects_dict):
		self.containingscenario=containingscenario
		self.currentchemical=currentchemical
		self.constants=constants
		self.containingvolumeelement=containingvolumeelement
		self.comp_objects_dict=comp_objects_dict
	@property
	def acceptableabiotic(self):
		return ("abiotic | soil | surface soil")
	

	@property
	def demethylationrate(self):
		cdict={}
		return cdict

	@property
	def chemical_demethylationrate(self):
		return self.demethylationrate[self.currentchemical.name]

	@property
	def chemical_demethylationrate(self):
		return self.demethylationrate[self.currentchemical.name]

	@property
	def litterfallrate(self):
		return (self.associated_leaf_comp.litterfallrate)
	

	@property
	def reductionrate(self):
		cdict={}
		return cdict

	@property
	def chemical_reductionrate(self):
		return self.reductionrate[self.currentchemical.name]

	@property
	def chemical_reductionrate(self):
		return self.reductionrate[self.currentchemical.name]


	@property
	def transferfactortoleaf(self):
		cdict={}
		try:
			cdict["chem_2_3_7_8_tcdd"]=0.3
		except:
			cdict["chem_2_3_7_8_tcdd"]=nan
		
		return cdict

	@property
	def chemical_transferfactortoleaf(self):
		return self.transferfactortoleaf[self.currentchemical.name]

	@property
	def chemical_transferfactortoleaf(self):
		return self.transferfactortoleaf[self.currentchemical.name]


	@property
	def halflife(self):
		cdict={}
		try:
			cdict["chem_2_3_7_8_tcdd"]=4.4
		except:
			cdict["chem_2_3_7_8_tcdd"]=nan
		
		return cdict

	@property
	def chemical_halflife(self):
		return self.halflife[self.currentchemical.name]

	@property
	def chemical_halflife(self):
		return self.halflife[self.currentchemical.name]

	@property
	def category(self):
		return ("terrestrial plant | leaf particle | leaf particle - coniferous forest")
	
	@property
	def concentrationoutputfactor(self):
		return (1000.0 / self.dustdensity)
	

	@property
	def initialconcentration_g_per_kg_usersupplied(self):
		cdict={}
		try:
			cdict["chem_2_3_7_8_tcdd"]=0.0
		except:
			cdict["chem_2_3_7_8_tcdd"]=nan
		
		return cdict

	@property
	def chemical_initialconcentration_g_per_kg_usersupplied(self):
		return self.initialconcentration_g_per_kg_usersupplied[self.currentchemical.name]

	@property
	def chemical_initialconcentration_g_per_kg_usersupplied(self):
		return self.initialconcentration_g_per_kg_usersupplied[self.currentchemical.name]

	@property
	def concentrationoutputunits(self):
		return ("mg/kg wet weight")
	

	@property
	def oxidationrate(self):
		cdict={}
		return cdict

	@property
	def chemical_oxidationrate(self):
		return self.oxidationrate[self.currentchemical.name]

	@property
	def chemical_oxidationrate(self):
		return self.oxidationrate[self.currentchemical.name]

	@property
	def allowexchange_forother(self):
		return (self.allowexchange_steadystate_forother if self.containingscenario.simulatesteadystate == 1 else 1)
	

	@property
	def particlevolumetricwetdepositionrate(self):
		cdict={}
		try:
			cdict["chem_2_3_7_8_tcdd"]=self.chemical_washoutratio * self.containingscenario.rain * (self.dustload / self.dustdensity)
		except:
			cdict["chem_2_3_7_8_tcdd"]=nan
		
		return cdict

	@property
	def chemical_particlevolumetricwetdepositionrate(self):
		return self.particlevolumetricwetdepositionrate[self.currentchemical.name]

	@property
	def chemical_particlevolumetricwetdepositionrate(self):
		return self.particlevolumetricwetdepositionrate[self.currentchemical.name]


	@property
	def washoutratio(self):
		cdict={}
		try:
			cdict["chem_2_3_7_8_tcdd"]=18000.0
		except:
			cdict["chem_2_3_7_8_tcdd"]=nan
		
		return cdict

	@property
	def chemical_washoutratio(self):
		return self.washoutratio[self.currentchemical.name]

	@property
	def chemical_washoutratio(self):
		return self.washoutratio[self.currentchemical.name]


	@property
	def generaldegradationrate(self):
		cdict={}
		try:
			cdict["chem_2_3_7_8_tcdd"]=log(2)/ self.chemical_halflife
		except:
			cdict["chem_2_3_7_8_tcdd"]=nan
		
		return cdict

	@property
	def chemical_generaldegradationrate(self):
		return self.generaldegradationrate[self.currentchemical.name]

	@property
	def chemical_generaldegradationrate(self):
		return self.generaldegradationrate[self.currentchemical.name]

	@property
	def totalmass(self):
		return (self.volume * self.dustdensity)
	

	@property
	def initialconcentration_g_per_kg(self):
		cdict={}
		try:
			cdict["chem_2_3_7_8_tcdd"]=self.containingscenario.fractioninitialconcentrations * self.chemical_initialconcentration_g_per_kg_usersupplied
		except:
			cdict["chem_2_3_7_8_tcdd"]=nan
		
		return cdict

	@property
	def chemical_initialconcentration_g_per_kg(self):
		return self.initialconcentration_g_per_kg[self.currentchemical.name]

	@property
	def chemical_initialconcentration_g_per_kg(self):
		return self.initialconcentration_g_per_kg[self.currentchemical.name]

	_dustload=6.15e-8
	@property
	def dustload(self):
		return self._dustload
	@dustload.setter
	def dustload(self,value):
		self._dustload=value

	_isbiotic=False
	@property
	def isbiotic(self):
		return self._isbiotic
	@isbiotic.setter
	def isbiotic(self,value):
		self._isbiotic=value

	_volumeparticleperarealeaf=1.0e-9
	@property
	def volumeparticleperarealeaf(self):
		return self._volumeparticleperarealeaf
	@volumeparticleperarealeaf.setter
	def volumeparticleperarealeaf(self,value):
		self._volumeparticleperarealeaf=value


	@property
	def methylationrate(self):
		cdict={}
		return cdict

	@property
	def chemical_methylationrate(self):
		return self.methylationrate[self.currentchemical.name]

	@property
	def chemical_methylationrate(self):
		return self.methylationrate[self.currentchemical.name]

	_dustdensity=1400.0
	@property
	def dustdensity(self):
		return self._dustdensity
	@dustdensity.setter
	def dustdensity(self,value):
		self._dustdensity=value

	@property
	def volume(self):
		return (self.volumeparticleperarealeaf * self.associated_leaf_comp.leafareaindex * self.containingvolumeelement.area)
	
class leaf_particle_deciduous_forest_in_deciduous_forest:
	def __init__(self,constants,containingscenario,currentchemical,containingvolumeelement,comp_objects_dict):
		self.containingscenario=containingscenario
		self.currentchemical=currentchemical
		self.constants=constants
		self.containingvolumeelement=containingvolumeelement
		self.comp_objects_dict=comp_objects_dict
	@property
	def acceptableabiotic(self):
		return ("abiotic | soil | surface soil")
	

	@property
	def demethylationrate(self):
		cdict={}
		return cdict

	@property
	def chemical_demethylationrate(self):
		return self.demethylationrate[self.currentchemical.name]

	@property
	def chemical_demethylationrate(self):
		return self.demethylationrate[self.currentchemical.name]

	@property
	def litterfallrate(self):
		return (self.associated_leaf_comp.litterfallrate)
	

	@property
	def reductionrate(self):
		cdict={}
		return cdict

	@property
	def chemical_reductionrate(self):
		return self.reductionrate[self.currentchemical.name]

	@property
	def chemical_reductionrate(self):
		return self.reductionrate[self.currentchemical.name]


	@property
	def transferfactortoleaf(self):
		cdict={}
		try:
			cdict["chem_2_3_7_8_tcdd"]=0.3
		except:
			cdict["chem_2_3_7_8_tcdd"]=nan
		
		return cdict

	@property
	def chemical_transferfactortoleaf(self):
		return self.transferfactortoleaf[self.currentchemical.name]

	@property
	def chemical_transferfactortoleaf(self):
		return self.transferfactortoleaf[self.currentchemical.name]


	@property
	def halflife(self):
		cdict={}
		try:
			cdict["chem_2_3_7_8_tcdd"]=4.4
		except:
			cdict["chem_2_3_7_8_tcdd"]=nan
		
		return cdict

	@property
	def chemical_halflife(self):
		return self.halflife[self.currentchemical.name]

	@property
	def chemical_halflife(self):
		return self.halflife[self.currentchemical.name]

	@property
	def category(self):
		return ("terrestrial plant | leaf particle | leaf particle - deciduous forest")
	
	@property
	def concentrationoutputfactor(self):
		return (1000.0 / self.dustdensity)
	

	@property
	def initialconcentration_g_per_kg_usersupplied(self):
		cdict={}
		try:
			cdict["chem_2_3_7_8_tcdd"]=0.0
		except:
			cdict["chem_2_3_7_8_tcdd"]=nan
		
		return cdict

	@property
	def chemical_initialconcentration_g_per_kg_usersupplied(self):
		return self.initialconcentration_g_per_kg_usersupplied[self.currentchemical.name]

	@property
	def chemical_initialconcentration_g_per_kg_usersupplied(self):
		return self.initialconcentration_g_per_kg_usersupplied[self.currentchemical.name]

	@property
	def concentrationoutputunits(self):
		return ("mg/kg wet weight")
	

	@property
	def oxidationrate(self):
		cdict={}
		return cdict

	@property
	def chemical_oxidationrate(self):
		return self.oxidationrate[self.currentchemical.name]

	@property
	def chemical_oxidationrate(self):
		return self.oxidationrate[self.currentchemical.name]

	@property
	def allowexchange_forother(self):
		return (self.allowexchange_steadystate_forother if self.containingscenario.simulatesteadystate == 1 else wt_av_allowexchange)
	

	@property
	def particlevolumetricwetdepositionrate(self):
		cdict={}
		try:
			cdict["chem_2_3_7_8_tcdd"]=self.chemical_washoutratio * self.containingscenario.rain * (self.dustload / self.dustdensity)
		except:
			cdict["chem_2_3_7_8_tcdd"]=nan
		
		return cdict

	@property
	def chemical_particlevolumetricwetdepositionrate(self):
		return self.particlevolumetricwetdepositionrate[self.currentchemical.name]

	@property
	def chemical_particlevolumetricwetdepositionrate(self):
		return self.particlevolumetricwetdepositionrate[self.currentchemical.name]


	@property
	def washoutratio(self):
		cdict={}
		try:
			cdict["chem_2_3_7_8_tcdd"]=18000.0
		except:
			cdict["chem_2_3_7_8_tcdd"]=nan
		
		return cdict

	@property
	def chemical_washoutratio(self):
		return self.washoutratio[self.currentchemical.name]

	@property
	def chemical_washoutratio(self):
		return self.washoutratio[self.currentchemical.name]


	@property
	def generaldegradationrate(self):
		cdict={}
		try:
			cdict["chem_2_3_7_8_tcdd"]=log(2)/ self.chemical_halflife
		except:
			cdict["chem_2_3_7_8_tcdd"]=nan
		
		return cdict

	@property
	def chemical_generaldegradationrate(self):
		return self.generaldegradationrate[self.currentchemical.name]

	@property
	def chemical_generaldegradationrate(self):
		return self.generaldegradationrate[self.currentchemical.name]

	@property
	def totalmass(self):
		return (self.volume * self.dustdensity)
	

	@property
	def initialconcentration_g_per_kg(self):
		cdict={}
		try:
			cdict["chem_2_3_7_8_tcdd"]=self.containingscenario.fractioninitialconcentrations * self.chemical_initialconcentration_g_per_kg_usersupplied
		except:
			cdict["chem_2_3_7_8_tcdd"]=nan
		
		return cdict

	@property
	def chemical_initialconcentration_g_per_kg(self):
		return self.initialconcentration_g_per_kg[self.currentchemical.name]

	@property
	def chemical_initialconcentration_g_per_kg(self):
		return self.initialconcentration_g_per_kg[self.currentchemical.name]

	_dustload=6.15e-8
	@property
	def dustload(self):
		return self._dustload
	@dustload.setter
	def dustload(self,value):
		self._dustload=value

	_isbiotic=False
	@property
	def isbiotic(self):
		return self._isbiotic
	@isbiotic.setter
	def isbiotic(self,value):
		self._isbiotic=value

	_volumeparticleperarealeaf=1.0e-9
	@property
	def volumeparticleperarealeaf(self):
		return self._volumeparticleperarealeaf
	@volumeparticleperarealeaf.setter
	def volumeparticleperarealeaf(self,value):
		self._volumeparticleperarealeaf=value


	@property
	def methylationrate(self):
		cdict={}
		return cdict

	@property
	def chemical_methylationrate(self):
		return self.methylationrate[self.currentchemical.name]

	@property
	def chemical_methylationrate(self):
		return self.methylationrate[self.currentchemical.name]

	_dustdensity=1400.0
	@property
	def dustdensity(self):
		return self._dustdensity
	@dustdensity.setter
	def dustdensity(self,value):
		self._dustdensity=value

	@property
	def volume(self):
		return (self.volumeparticleperarealeaf * self.associated_leaf_comp.leafareaindex * self.containingvolumeelement.area)
	
class leaf_particle_grasses_herbs_in_grasses_herbs:
	def __init__(self,constants,containingscenario,currentchemical,containingvolumeelement,comp_objects_dict):
		self.containingscenario=containingscenario
		self.currentchemical=currentchemical
		self.constants=constants
		self.containingvolumeelement=containingvolumeelement
		self.comp_objects_dict=comp_objects_dict
	@property
	def acceptableabiotic(self):
		return ("abiotic | soil | surface soil")
	

	@property
	def demethylationrate(self):
		cdict={}
		return cdict

	@property
	def chemical_demethylationrate(self):
		return self.demethylationrate[self.currentchemical.name]

	@property
	def chemical_demethylationrate(self):
		return self.demethylationrate[self.currentchemical.name]

	@property
	def litterfallrate(self):
		return (self.associated_leaf_comp.litterfallrate)
	

	@property
	def reductionrate(self):
		cdict={}
		return cdict

	@property
	def chemical_reductionrate(self):
		return self.reductionrate[self.currentchemical.name]

	@property
	def chemical_reductionrate(self):
		return self.reductionrate[self.currentchemical.name]


	@property
	def transferfactortoleaf(self):
		cdict={}
		try:
			cdict["chem_2_3_7_8_tcdd"]=0.3
		except:
			cdict["chem_2_3_7_8_tcdd"]=nan
		
		return cdict

	@property
	def chemical_transferfactortoleaf(self):
		return self.transferfactortoleaf[self.currentchemical.name]

	@property
	def chemical_transferfactortoleaf(self):
		return self.transferfactortoleaf[self.currentchemical.name]


	@property
	def halflife(self):
		cdict={}
		try:
			cdict["chem_2_3_7_8_tcdd"]=4.4
		except:
			cdict["chem_2_3_7_8_tcdd"]=nan
		
		return cdict

	@property
	def chemical_halflife(self):
		return self.halflife[self.currentchemical.name]

	@property
	def chemical_halflife(self):
		return self.halflife[self.currentchemical.name]

	@property
	def category(self):
		return ("terrestrial plant | leaf particle | leaf particle - grasses/herbs")
	
	@property
	def concentrationoutputfactor(self):
		return (1000.0 / self.dustdensity)
	

	@property
	def initialconcentration_g_per_kg_usersupplied(self):
		cdict={}
		try:
			cdict["chem_2_3_7_8_tcdd"]=0.0
		except:
			cdict["chem_2_3_7_8_tcdd"]=nan
		
		return cdict

	@property
	def chemical_initialconcentration_g_per_kg_usersupplied(self):
		return self.initialconcentration_g_per_kg_usersupplied[self.currentchemical.name]

	@property
	def chemical_initialconcentration_g_per_kg_usersupplied(self):
		return self.initialconcentration_g_per_kg_usersupplied[self.currentchemical.name]

	@property
	def concentrationoutputunits(self):
		return ("mg/kg wet weight")
	

	@property
	def oxidationrate(self):
		cdict={}
		return cdict

	@property
	def chemical_oxidationrate(self):
		return self.oxidationrate[self.currentchemical.name]

	@property
	def chemical_oxidationrate(self):
		return self.oxidationrate[self.currentchemical.name]

	@property
	def allowexchange_forother(self):
		return (self.allowexchange_steadystate_forother if self.containingscenario.simulatesteadystate == 1 else wt_av_allowexchange)
	

	@property
	def particlevolumetricwetdepositionrate(self):
		cdict={}
		try:
			cdict["chem_2_3_7_8_tcdd"]=self.chemical_washoutratio * self.containingscenario.rain * (self.dustload / self.dustdensity)
		except:
			cdict["chem_2_3_7_8_tcdd"]=nan
		
		return cdict

	@property
	def chemical_particlevolumetricwetdepositionrate(self):
		return self.particlevolumetricwetdepositionrate[self.currentchemical.name]

	@property
	def chemical_particlevolumetricwetdepositionrate(self):
		return self.particlevolumetricwetdepositionrate[self.currentchemical.name]


	@property
	def washoutratio(self):
		cdict={}
		try:
			cdict["chem_2_3_7_8_tcdd"]=18000.0
		except:
			cdict["chem_2_3_7_8_tcdd"]=nan
		
		return cdict

	@property
	def chemical_washoutratio(self):
		return self.washoutratio[self.currentchemical.name]

	@property
	def chemical_washoutratio(self):
		return self.washoutratio[self.currentchemical.name]


	@property
	def generaldegradationrate(self):
		cdict={}
		try:
			cdict["chem_2_3_7_8_tcdd"]=log(2)/ self.chemical_halflife
		except:
			cdict["chem_2_3_7_8_tcdd"]=nan
		
		return cdict

	@property
	def chemical_generaldegradationrate(self):
		return self.generaldegradationrate[self.currentchemical.name]

	@property
	def chemical_generaldegradationrate(self):
		return self.generaldegradationrate[self.currentchemical.name]

	@property
	def totalmass(self):
		return (self.volume * self.dustdensity)
	

	@property
	def initialconcentration_g_per_kg(self):
		cdict={}
		try:
			cdict["chem_2_3_7_8_tcdd"]=self.containingscenario.fractioninitialconcentrations * self.chemical_initialconcentration_g_per_kg_usersupplied
		except:
			cdict["chem_2_3_7_8_tcdd"]=nan
		
		return cdict

	@property
	def chemical_initialconcentration_g_per_kg(self):
		return self.initialconcentration_g_per_kg[self.currentchemical.name]

	@property
	def chemical_initialconcentration_g_per_kg(self):
		return self.initialconcentration_g_per_kg[self.currentchemical.name]

	_dustload=6.15e-8
	@property
	def dustload(self):
		return self._dustload
	@dustload.setter
	def dustload(self,value):
		self._dustload=value

	_isbiotic=False
	@property
	def isbiotic(self):
		return self._isbiotic
	@isbiotic.setter
	def isbiotic(self,value):
		self._isbiotic=value

	_volumeparticleperarealeaf=1.0e-9
	@property
	def volumeparticleperarealeaf(self):
		return self._volumeparticleperarealeaf
	@volumeparticleperarealeaf.setter
	def volumeparticleperarealeaf(self,value):
		self._volumeparticleperarealeaf=value


	@property
	def methylationrate(self):
		cdict={}
		return cdict

	@property
	def chemical_methylationrate(self):
		return self.methylationrate[self.currentchemical.name]

	@property
	def chemical_methylationrate(self):
		return self.methylationrate[self.currentchemical.name]

	_dustdensity=1400.0
	@property
	def dustdensity(self):
		return self._dustdensity
	@dustdensity.setter
	def dustdensity(self,value):
		self._dustdensity=value

	@property
	def volume(self):
		return (self.volumeparticleperarealeaf * self.associated_leaf_comp.leafareaindex * self.containingvolumeelement.area)
	
class macrophyte:
	def __init__(self,constants,containingscenario,currentchemical,containingvolumeelement,comp_objects_dict):
		self.containingscenario=containingscenario
		self.currentchemical=currentchemical
		self.constants=constants
		self.containingvolumeelement=containingvolumeelement
		self.comp_objects_dict=comp_objects_dict
	_biomassperarea_kg_m2=0.6
	@property
	def biomassperarea_kg_m2(self):
		return self._biomassperarea_kg_m2
	@biomassperarea_kg_m2.setter
	def biomassperarea_kg_m2(self,value):
		self._biomassperarea_kg_m2=value

	@property
	def acceptableabiotic(self):
		return ("abiotic | surface water | surface water - default")
	

	@property
	def depurationrate(self):
		cdict={}
		try:
			cdict["chem_2_3_7_8_tcdd"]=1 / (1.58 + 0.000015 * self.currentchemical.k_ow)
		except:
			cdict["chem_2_3_7_8_tcdd"]=nan
		
		return cdict

	@property
	def chemical_depurationrate(self):
		return self.depurationrate[self.currentchemical.name]

	@property
	def chemical_depurationrate(self):
		return self.depurationrate[self.currentchemical.name]


	@property
	def watercolumndissolvedpartitioning_partitioncoefficient(self):
		cdict={}
		return cdict

	@property
	def chemical_watercolumndissolvedpartitioning_partitioncoefficient(self):
		return self.watercolumndissolvedpartitioning_partitioncoefficient[self.currentchemical.name]

	@property
	def chemical_watercolumndissolvedpartitioning_partitioncoefficient(self):
		return self.watercolumndissolvedpartitioning_partitioncoefficient[self.currentchemical.name]


	@property
	def abbreviation(self):
		cdict={}
		return cdict

	@property
	def chemical_abbreviation(self):
		return self.abbreviation[self.currentchemical.name]

	@property
	def chemical_abbreviation(self):
		return self.abbreviation[self.currentchemical.name]


	@property
	def halflife(self):
		cdict={}
		try:
			cdict["chem_2_3_7_8_tcdd"]=70.0
		except:
			cdict["chem_2_3_7_8_tcdd"]=nan
		
		return cdict

	@property
	def chemical_halflife(self):
		return self.halflife[self.currentchemical.name]

	@property
	def chemical_halflife(self):
		return self.halflife[self.currentchemical.name]

	@property
	def category(self):
		return ("aquatic plant | macrophyte")
	
	_concentrationoutputfactor=1000.0
	@property
	def concentrationoutputfactor(self):
		return self._concentrationoutputfactor
	@concentrationoutputfactor.setter
	def concentrationoutputfactor(self,value):
		self._concentrationoutputfactor=value


	@property
	def watercolumndissolvedpartitioning_timetoreachalphaofequilibrium(self):
		cdict={}
		return cdict

	@property
	def chemical_watercolumndissolvedpartitioning_timetoreachalphaofequilibrium(self):
		return self.watercolumndissolvedpartitioning_timetoreachalphaofequilibrium[self.currentchemical.name]

	@property
	def chemical_watercolumndissolvedpartitioning_timetoreachalphaofequilibrium(self):
		return self.watercolumndissolvedpartitioning_timetoreachalphaofequilibrium[self.currentchemical.name]


	@property
	def initialconcentration_g_per_kg_usersupplied(self):
		cdict={}
		try:
			cdict["chem_2_3_7_8_tcdd"]=0.0
		except:
			cdict["chem_2_3_7_8_tcdd"]=nan
		
		return cdict

	@property
	def chemical_initialconcentration_g_per_kg_usersupplied(self):
		return self.initialconcentration_g_per_kg_usersupplied[self.currentchemical.name]

	@property
	def chemical_initialconcentration_g_per_kg_usersupplied(self):
		return self.initialconcentration_g_per_kg_usersupplied[self.currentchemical.name]

	@property
	def concentrationoutputunits(self):
		return ("mg/kg wet weight")
	

	@property
	def oxidationrate(self):
		cdict={}
		return cdict

	@property
	def chemical_oxidationrate(self):
		return self.oxidationrate[self.currentchemical.name]

	@property
	def chemical_oxidationrate(self):
		return self.oxidationrate[self.currentchemical.name]


	@property
	def generaldegradationrate(self):
		cdict={}
		try:
			cdict["chem_2_3_7_8_tcdd"]=log(2)/ self.chemical_halflife
		except:
			cdict["chem_2_3_7_8_tcdd"]=nan
		
		return cdict

	@property
	def chemical_generaldegradationrate(self):
		return self.generaldegradationrate[self.currentchemical.name]

	@property
	def chemical_generaldegradationrate(self):
		return self.generaldegradationrate[self.currentchemical.name]


	@property
	def bioaccumulationrate(self):
		cdict={}
		try:
			cdict["chem_2_3_7_8_tcdd"]=1 / (0.002 + 500 /self.currentchemical.k_ow)
		except:
			cdict["chem_2_3_7_8_tcdd"]=nan
		
		return cdict

	@property
	def chemical_bioaccumulationrate(self):
		return self.bioaccumulationrate[self.currentchemical.name]

	@property
	def chemical_bioaccumulationrate(self):
		return self.bioaccumulationrate[self.currentchemical.name]

	@property
	def totalmass(self):
		return (self.biomassperarea_kg_m2 * self.containingvolumeelement.area)
	

	@property
	def initialconcentration_g_per_kg(self):
		cdict={}
		try:
			cdict["chem_2_3_7_8_tcdd"]=self.containingscenario.fractioninitialconcentrations * self.chemical_initialconcentration_g_per_kg_usersupplied
		except:
			cdict["chem_2_3_7_8_tcdd"]=nan
		
		return cdict

	@property
	def chemical_initialconcentration_g_per_kg(self):
		return self.initialconcentration_g_per_kg[self.currentchemical.name]

	@property
	def chemical_initialconcentration_g_per_kg(self):
		return self.initialconcentration_g_per_kg[self.currentchemical.name]

	_isbiotic=True
	@property
	def isbiotic(self):
		return self._isbiotic
	@isbiotic.setter
	def isbiotic(self,value):
		self._isbiotic=value

	_density=1.0
	@property
	def density(self):
		return self._density
	@density.setter
	def density(self,value):
		self._density=value

	@property
	def volume(self):
		return (self.totalmass / (self.density*1000))
	

	@property
	def watercolumndissolvedpartitioning_alphaofequilibrium(self):
		cdict={}
		return cdict

	@property
	def chemical_watercolumndissolvedpartitioning_alphaofequilibrium(self):
		return self.watercolumndissolvedpartitioning_alphaofequilibrium[self.currentchemical.name]

	@property
	def chemical_watercolumndissolvedpartitioning_alphaofequilibrium(self):
		return self.watercolumndissolvedpartitioning_alphaofequilibrium[self.currentchemical.name]

class root_grasses_herbs_in_grasses_herbs:
	def __init__(self,constants,containingscenario,currentchemical,containingvolumeelement,comp_objects_dict):
		self.containingscenario=containingscenario
		self.currentchemical=currentchemical
		self.constants=constants
		self.containingvolumeelement=containingvolumeelement
		self.comp_objects_dict=comp_objects_dict
	@property
	def acceptableabiotic(self):
		return ("abiotic | soil | surface soil")
	
	@property
	def dryvolumeperarea(self):
		return (self.wetvolumeperarea*(1 - self.watercontent))
	

	@property
	def demethylationrate(self):
		cdict={}
		return cdict

	@property
	def chemical_demethylationrate(self):
		return self.demethylationrate[self.currentchemical.name]

	@property
	def chemical_demethylationrate(self):
		return self.demethylationrate[self.currentchemical.name]


	@property
	def root_rootzonepartitioningbulksoil_partitioncoefficient(self):
		cdict={}
		return cdict

	@property
	def chemical_root_rootzonepartitioningbulksoil_partitioncoefficient(self):
		return self.root_rootzonepartitioningbulksoil_partitioncoefficient[self.currentchemical.name]

	@property
	def chemical_root_rootzonepartitioningbulksoil_partitioncoefficient(self):
		return self.root_rootzonepartitioningbulksoil_partitioncoefficient[self.currentchemical.name]


	@property
	def reductionrate(self):
		cdict={}
		return cdict

	@property
	def chemical_reductionrate(self):
		return self.reductionrate[self.currentchemical.name]

	@property
	def chemical_reductionrate(self):
		return self.reductionrate[self.currentchemical.name]


	@property
	def root_rootzonepartitioningbulksoil_timetoreachalphaofsteadystate(self):
		cdict={}
		return cdict

	@property
	def chemical_root_rootzonepartitioningbulksoil_timetoreachalphaofsteadystate(self):
		return self.root_rootzonepartitioningbulksoil_timetoreachalphaofsteadystate[self.currentchemical.name]

	@property
	def chemical_root_rootzonepartitioningbulksoil_timetoreachalphaofsteadystate(self):
		return self.root_rootzonepartitioningbulksoil_timetoreachalphaofsteadystate[self.currentchemical.name]

	@property
	def wetvolumeperarea(self):
		return (self.wetmassperarea/self.wetdensity)
	
	_lipidcontent=0.011
	@property
	def lipidcontent(self):
		return self._lipidcontent
	@lipidcontent.setter
	def lipidcontent(self,value):
		self._lipidcontent=value


	@property
	def halflife(self):
		cdict={}
		try:
			cdict["chem_2_3_7_8_tcdd"]=70.0
		except:
			cdict["chem_2_3_7_8_tcdd"]=nan
		
		return cdict

	@property
	def chemical_halflife(self):
		return self.halflife[self.currentchemical.name]

	@property
	def chemical_halflife(self):
		return self.halflife[self.currentchemical.name]

	@property
	def category(self):
		return ("terrestrial plant | root | root - grasses/herbs")
	
	_concentrationoutputfactor=1000.0
	@property
	def concentrationoutputfactor(self):
		return self._concentrationoutputfactor
	@concentrationoutputfactor.setter
	def concentrationoutputfactor(self,value):
		self._concentrationoutputfactor=value

	_wetmassperarea=1.4
	@property
	def wetmassperarea(self):
		return self._wetmassperarea
	@wetmassperarea.setter
	def wetmassperarea(self,value):
		self._wetmassperarea=value


	@property
	def initialconcentration_g_per_kg_usersupplied(self):
		cdict={}
		try:
			cdict["chem_2_3_7_8_tcdd"]=0.0
		except:
			cdict["chem_2_3_7_8_tcdd"]=nan
		
		return cdict

	@property
	def chemical_initialconcentration_g_per_kg_usersupplied(self):
		return self.initialconcentration_g_per_kg_usersupplied[self.currentchemical.name]

	@property
	def chemical_initialconcentration_g_per_kg_usersupplied(self):
		return self.initialconcentration_g_per_kg_usersupplied[self.currentchemical.name]

	@property
	def concentrationoutputunits(self):
		return ("mg/kg wet weight")
	

	@property
	def rootsoilwaterinteraction_t_alpha(self):
		cdict={}
		try:
			cdict["chem_2_3_7_8_tcdd"]=2*(1.62 + exp(self.currentchemical.log10_k_ow - 1.8)) / 24
		except:
			cdict["chem_2_3_7_8_tcdd"]=nan
		
		return cdict

	@property
	def chemical_rootsoilwaterinteraction_t_alpha(self):
		return self.rootsoilwaterinteraction_t_alpha[self.currentchemical.name]

	@property
	def chemical_rootsoilwaterinteraction_t_alpha(self):
		return self.rootsoilwaterinteraction_t_alpha[self.currentchemical.name]


	@property
	def oxidationrate(self):
		cdict={}
		return cdict

	@property
	def chemical_oxidationrate(self):
		return self.oxidationrate[self.currentchemical.name]

	@property
	def chemical_oxidationrate(self):
		return self.oxidationrate[self.currentchemical.name]

	_wetdensity=820.0
	@property
	def wetdensity(self):
		return self._wetdensity
	@wetdensity.setter
	def wetdensity(self,value):
		self._wetdensity=value

	@property
	def allowexchange_forother(self):
		return (self.allowexchange_steadystate_forother if self.containingscenario.simulatesteadystate == 1 else wt_av_allowexchange)
	

	@property
	def generaldegradationrate(self):
		cdict={}
		try:
			cdict["chem_2_3_7_8_tcdd"]=log(2)/ self.chemical_halflife
		except:
			cdict["chem_2_3_7_8_tcdd"]=nan
		
		return cdict

	@property
	def chemical_generaldegradationrate(self):
		return self.generaldegradationrate[self.currentchemical.name]

	@property
	def chemical_generaldegradationrate(self):
		return self.generaldegradationrate[self.currentchemical.name]

	_correctionexponent=0.76
	@property
	def correctionexponent(self):
		return self._correctionexponent
	@correctionexponent.setter
	def correctionexponent(self,value):
		self._correctionexponent=value


	@property
	def rootsoilwaterinteraction_alpha(self):
		cdict={}
		try:
			cdict["chem_2_3_7_8_tcdd"]=0.95
		except:
			cdict["chem_2_3_7_8_tcdd"]=nan
		
		return cdict

	@property
	def chemical_rootsoilwaterinteraction_alpha(self):
		return self.rootsoilwaterinteraction_alpha[self.currentchemical.name]

	@property
	def chemical_rootsoilwaterinteraction_alpha(self):
		return self.rootsoilwaterinteraction_alpha[self.currentchemical.name]

	@property
	def totalmass(self):
		return (self.volume * self.wetdensity)
	

	@property
	def initialconcentration_g_per_kg(self):
		cdict={}
		try:
			cdict["chem_2_3_7_8_tcdd"]=self.containingscenario.fractioninitialconcentrations * self.chemical_initialconcentration_g_per_kg_usersupplied
		except:
			cdict["chem_2_3_7_8_tcdd"]=nan
		
		return cdict

	@property
	def chemical_initialconcentration_g_per_kg(self):
		return self.initialconcentration_g_per_kg[self.currentchemical.name]

	@property
	def chemical_initialconcentration_g_per_kg(self):
		return self.initialconcentration_g_per_kg[self.currentchemical.name]

	_isbiotic=True
	@property
	def isbiotic(self):
		return self._isbiotic
	@isbiotic.setter
	def isbiotic(self,value):
		self._isbiotic=value


	@property
	def methylationrate(self):
		cdict={}
		return cdict

	@property
	def chemical_methylationrate(self):
		return self.methylationrate[self.currentchemical.name]

	@property
	def chemical_methylationrate(self):
		return self.methylationrate[self.currentchemical.name]

	_watercontent=0.8
	@property
	def watercontent(self):
		return self._watercontent
	@watercontent.setter
	def watercontent(self,value):
		self._watercontent=value

	@property
	def density(self):
		return (self.wetdensity)
	
	@property
	def volume(self):
		return (self.wetvolumeperarea*self.containingvolumeelement.area)
	

	@property
	def root_rootzonepartitioningbulksoil_alphaofsteadystate(self):
		cdict={}
		return cdict

	@property
	def chemical_root_rootzonepartitioningbulksoil_alphaofsteadystate(self):
		return self.root_rootzonepartitioningbulksoil_alphaofsteadystate[self.currentchemical.name]

	@property
	def chemical_root_rootzonepartitioningbulksoil_alphaofsteadystate(self):
		return self.root_rootzonepartitioningbulksoil_alphaofsteadystate[self.currentchemical.name]

class sediment:
	def __init__(self,constants,containingscenario,currentchemical,containingvolumeelement,comp_objects_dict):
		self.containingscenario=containingscenario
		self.currentchemical=currentchemical
		self.constants=constants
		self.containingvolumeelement=containingvolumeelement
		self.comp_objects_dict=comp_objects_dict
	_sedimentresuspensionvelocity=6.69E-5
	@property
	def sedimentresuspensionvelocity(self):
		return self._sedimentresuspensionvelocity
	@sedimentresuspensionvelocity.setter
	def sedimentresuspensionvelocity(self,value):
		self._sedimentresuspensionvelocity=value

	@property
	def wetconcoutputunits(self):
		return ("ug/g wet weight")
	
	@property
	def acceptableabiotic(self):
		return ("nan")
	
	@property
	def benthic_solids_concentration(self):
		return (self.rho * (1 - self.porosity))
	

	@property
	def demethylationrate(self):
		cdict={}
		return cdict

	@property
	def chemical_demethylationrate(self):
		return self.demethylationrate[self.currentchemical.name]

	@property
	def chemical_demethylationrate(self):
		return self.demethylationrate[self.currentchemical.name]

	@property
	def sedimentresuspensionrate_m3_m2_day(self):
		return (self.sedimentresuspensionrate_kg_m2_day / self.rho)
	

	@property
	def fractionmass_dissolved(self):
		cdict={}
		try:
			cdict["chem_2_3_7_8_tcdd"]=self.volume * self.volumefraction_liquid /self.chemical_genericdenominatorforcalculatingfractioninphases
		except:
			cdict["chem_2_3_7_8_tcdd"]=nan
		
		return cdict

	@property
	def chemical_fractionmass_dissolved(self):
		return self.fractionmass_dissolved[self.currentchemical.name]

	@property
	def chemical_fractionmass_dissolved(self):
		return self.fractionmass_dissolved[self.currentchemical.name]

	_porosity=0.6
	@property
	def porosity(self):
		return self._porosity
	@porosity.setter
	def porosity(self,value):
		self._porosity=value


	@property
	def reductionrate(self):
		cdict={}
		return cdict

	@property
	def chemical_reductionrate(self):
		return self.reductionrate[self.currentchemical.name]

	@property
	def chemical_reductionrate(self):
		return self.reductionrate[self.currentchemical.name]

	@property
	def sedimentburialratetohavezeronetdeposition_m3_m2_day(self):
		return (1.171E-05)
	

	@property
	def z_solid(self):
		cdict={}
		try:
			cdict["chem_2_3_7_8_tcdd"]=self.chemical_kd * (self.rho / 1000) * self.currentchemical.z_purewater
		except:
			cdict["chem_2_3_7_8_tcdd"]=nan
		
		return cdict

	@property
	def chemical_z_solid(self):
		return self.z_solid[self.currentchemical.name]

	@property
	def chemical_z_solid(self):
		return self.z_solid[self.currentchemical.name]


	@property
	def initialconcentration_g_per_m3(self):
		cdict={}
		try:
			cdict["chem_2_3_7_8_tcdd"]=self.containingscenario.fractioninitialconcentrations * self.chemical_initialconcentration_g_per_m3_usersupplied
		except:
			cdict["chem_2_3_7_8_tcdd"]=nan
		
		return cdict

	@property
	def chemical_initialconcentration_g_per_m3(self):
		return self.initialconcentration_g_per_m3[self.currentchemical.name]

	@property
	def chemical_initialconcentration_g_per_m3(self):
		return self.initialconcentration_g_per_m3[self.currentchemical.name]


	@property
	def d_effective(self):
		cdict={}
		try:
			cdict["chem_2_3_7_8_tcdd"]=self.porosity ** (4 / 3) * self.currentchemical.d_purewater
		except:
			cdict["chem_2_3_7_8_tcdd"]=nan
		
		return cdict

	@property
	def chemical_d_effective(self):
		return self.d_effective[self.currentchemical.name]

	@property
	def chemical_d_effective(self):
		return self.d_effective[self.currentchemical.name]


	@property
	def z_liquid(self):
		cdict={}
		try:
			cdict["chem_2_3_7_8_tcdd"]=self.currentchemical.z_purewater
		except:
			cdict["chem_2_3_7_8_tcdd"]=nan
		
		return cdict

	@property
	def chemical_z_liquid(self):
		return self.z_liquid[self.currentchemical.name]

	@property
	def chemical_z_liquid(self):
		return self.z_liquid[self.currentchemical.name]


	@property
	def boundarylayerthicknessbelowwater(self):
		cdict={}
		try:
			cdict["chem_2_3_7_8_tcdd"]=318 * self.chemical_d_effective ** (0.683)
		except:
			cdict["chem_2_3_7_8_tcdd"]=nan
		
		return cdict

	@property
	def chemical_boundarylayerthicknessbelowwater(self):
		return self.boundarylayerthicknessbelowwater[self.currentchemical.name]

	@property
	def chemical_boundarylayerthicknessbelowwater(self):
		return self.boundarylayerthicknessbelowwater[self.currentchemical.name]


	@property
	def halflife(self):
		cdict={}
		try:
			cdict["chem_2_3_7_8_tcdd"]=1095.0
		except:
			cdict["chem_2_3_7_8_tcdd"]=nan
		
		return cdict

	@property
	def chemical_halflife(self):
		return self.halflife[self.currentchemical.name]

	@property
	def chemical_halflife(self):
		return self.halflife[self.currentchemical.name]

	@property
	def category(self):
		return ("abiotic | sediment | sediment - default")
	
	_fractionsand=0.25
	@property
	def fractionsand(self):
		return self._fractionsand
	@fractionsand.setter
	def fractionsand(self,value):
		self._fractionsand=value


	@property
	def fractionmass_sorbed(self):
		cdict={}
		try:
			cdict["chem_2_3_7_8_tcdd"]=self.volume * self.volumefraction_solid * self.chemical_kd * self.rho * self.constants.m3_per_l  /self.chemical_genericdenominatorforcalculatingfractioninphases
		except:
			cdict["chem_2_3_7_8_tcdd"]=nan
		
		return cdict

	@property
	def chemical_fractionmass_sorbed(self):
		return self.fractionmass_sorbed[self.currentchemical.name]

	@property
	def chemical_fractionmass_sorbed(self):
		return self.fractionmass_sorbed[self.currentchemical.name]

	@property
	def concentrationoutputfactor(self):
		return (1000/(self.volumefraction_solid * self.rho))
	

	@property
	def initialconcentration_g_per_m3_usersupplied(self):
		cdict={}
		try:
			cdict["chem_2_3_7_8_tcdd"]=0.0
		except:
			cdict["chem_2_3_7_8_tcdd"]=nan
		
		return cdict

	@property
	def chemical_initialconcentration_g_per_m3_usersupplied(self):
		return self.initialconcentration_g_per_m3_usersupplied[self.currentchemical.name]

	@property
	def chemical_initialconcentration_g_per_m3_usersupplied(self):
		return self.initialconcentration_g_per_m3_usersupplied[self.currentchemical.name]

	_rho=2600.0
	@property
	def rho(self):
		return self._rho
	@rho.setter
	def rho(self,value):
		self._rho=value

	@property
	def concentrationoutputunits(self):
		return ("ug/g dry weight")
	
	_ph=0.01
	@property
	def ph(self):
		return self._ph
	@ph.setter
	def ph(self,value):
		self._ph=value


	@property
	def z_total(self):
		cdict={}
		try:
			cdict["chem_2_3_7_8_tcdd"]=self.chemical_z_liquid * self.porosity + self.chemical_z_solid * (1 - self.porosity)
		except:
			cdict["chem_2_3_7_8_tcdd"]=nan
		
		return cdict

	@property
	def chemical_z_total(self):
		return self.z_total[self.currentchemical.name]

	@property
	def chemical_z_total(self):
		return self.z_total[self.currentchemical.name]


	@property
	def oxidationrate(self):
		cdict={}
		return cdict

	@property
	def chemical_oxidationrate(self):
		return self.oxidationrate[self.currentchemical.name]

	@property
	def chemical_oxidationrate(self):
		return self.oxidationrate[self.currentchemical.name]

	@property
	def sedimentresuspensionrate_kg_m2_day(self):
		return (self.sedimentresuspensionvelocity*self.benthic_solids_concentration)
	

	@property
	def genericdenominatorforcalculatingfractioninphases(self):
		cdict={}
		try:
			cdict["chem_2_3_7_8_tcdd"]=self.volume * self.volumefraction_solid * self.chemical_kd * self.rho * self.constants.m3_per_l + self.volume * self.volumefraction_liquid
		except:
			cdict["chem_2_3_7_8_tcdd"]=nan
		
		return cdict

	@property
	def chemical_genericdenominatorforcalculatingfractioninphases(self):
		return self.genericdenominatorforcalculatingfractioninphases[self.currentchemical.name]

	@property
	def chemical_genericdenominatorforcalculatingfractioninphases(self):
		return self.genericdenominatorforcalculatingfractioninphases[self.currentchemical.name]

	@property
	def area(self):
		return (self.containingvolumeelement.area)
	
	@property
	def height(self):
		return (self.containingvolumeelement.height)
	
	@property
	def depth(self):
		return (self.height)
	
	@property
	def volumefraction_solid(self):
		return (1 - self.volumefraction_liquid)
	
	_organiccarboncontent=0.01
	@property
	def organiccarboncontent(self):
		return self._organiccarboncontent
	@organiccarboncontent.setter
	def organiccarboncontent(self,value):
		self._organiccarboncontent=value


	@property
	def generaldegradationrate(self):
		cdict={}
		try:
			cdict["chem_2_3_7_8_tcdd"]=log(2)/ self.chemical_halflife
		except:
			cdict["chem_2_3_7_8_tcdd"]=nan
		
		return cdict

	@property
	def chemical_generaldegradationrate(self):
		return self.generaldegradationrate[self.currentchemical.name]

	@property
	def chemical_generaldegradationrate(self):
		return self.generaldegradationrate[self.currentchemical.name]

	@property
	def wetconcoutputfactor(self):
		return ((self.volumefraction_solid * self.rho) / (self.volumefraction_solid * self.rho + self.volumefraction_liquid * self.constants.kg_per_m3_water))
	
	@property
	def totalmass(self):
		return (self.volume*(self.volumefraction_solid*self.rho + self.volumefraction_liquid*self.constants.kg_per_m3_water))
	
	@property
	def volumefraction_liquid(self):
		return (self.porosity)
	
	_isbiotic=False
	@property
	def isbiotic(self):
		return self._isbiotic
	@isbiotic.setter
	def isbiotic(self,value):
		self._isbiotic=value


	@property
	def methylationrate(self):
		cdict={}
		return cdict

	@property
	def chemical_methylationrate(self):
		return self.methylationrate[self.currentchemical.name]

	@property
	def chemical_methylationrate(self):
		return self.methylationrate[self.currentchemical.name]


	@property
	def kd(self):
		cdict={}
		try:
			cdict["chem_2_3_7_8_tcdd"]=self.currentchemical.k_oc * self.organiccarboncontent
		except:
			cdict["chem_2_3_7_8_tcdd"]=nan
		
		return cdict

	@property
	def chemical_kd(self):
		return self.kd[self.currentchemical.name]

	@property
	def chemical_kd(self):
		return self.kd[self.currentchemical.name]

	@property
	def volume(self):
		return (self.containingvolumeelement.volume)
	
class sediment_burial_sink:
	def __init__(self,constants,containingscenario,currentchemical,containingvolumeelement,comp_objects_dict):
		self.containingscenario=containingscenario
		self.currentchemical=currentchemical
		self.constants=constants
		self.containingvolumeelement=containingvolumeelement
		self.comp_objects_dict=comp_objects_dict
	@property
	def acceptableabiotic(self):
		return ("nan")
	
	_isbiotic=False
	@property
	def isbiotic(self):
		return self._isbiotic
	@isbiotic.setter
	def isbiotic(self,value):
		self._isbiotic=value

	@property
	def category(self):
		return ("sink | abiotic | sediment | sediment - default")
	
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
	
class soil_root_zone:
	def __init__(self,constants,containingscenario,currentchemical,containingvolumeelement,comp_objects_dict):
		self.containingscenario=containingscenario
		self.currentchemical=currentchemical
		self.constants=constants
		self.containingvolumeelement=containingvolumeelement
		self.comp_objects_dict=comp_objects_dict
	@property
	def acceptableabiotic(self):
		return ("0.01")
	

	@property
	def z_liquidcolloid(self):
		cdict={}
		return cdict

	@property
	def chemical_z_liquidcolloid(self):
		return self.z_liquidcolloid[self.currentchemical.name]

	@property
	def chemical_z_liquidcolloid(self):
		return self.z_liquidcolloid[self.currentchemical.name]

	@property
	def demethylationrate(self):
		if not hasattr(self,"_demethylationrate"):
			self._demethylationrate={}
			
	@property
	def chemical_demethylationrate(self):
		return self.demethylationrate[self.currentchemical.name]


	@property
	def fractionmass_vapor(self):
		cdict={}
		try:
			cdict["chem_2_3_7_8_tcdd"]=self.volume * self.volumefraction_vapor * 1000 * (self.chemical_z_vapor /self.chemical_z_liquid) / self.chemical_genericdenominatorforcalculatingfractioninphases
		except:
			cdict["chem_2_3_7_8_tcdd"]=nan
		
		return cdict

	@property
	def chemical_fractionmass_vapor(self):
		return self.fractionmass_vapor[self.currentchemical.name]

	@property
	def chemical_fractionmass_vapor(self):
		return self.fractionmass_vapor[self.currentchemical.name]


	@property
	def inputcharacteristicdepth_m(self):
		cdict={}
		try:
			cdict["chem_2_3_7_8_tcdd"]=0.08
		except:
			cdict["chem_2_3_7_8_tcdd"]=nan
		
		return cdict

	@property
	def chemical_inputcharacteristicdepth_m(self):
		return self.inputcharacteristicdepth_m[self.currentchemical.name]

	@property
	def chemical_inputcharacteristicdepth_m(self):
		return self.inputcharacteristicdepth_m[self.currentchemical.name]

	_volumefraction_vapor=0.36
	@property
	def volumefraction_vapor(self):
		return self._volumefraction_vapor
	@volumefraction_vapor.setter
	def volumefraction_vapor(self,value):
		self._volumefraction_vapor=value


	@property
	def depth_times_z_total(self):
		cdict={}
		try:
			cdict["chem_2_3_7_8_tcdd"]=self.height * self.chemical_z_total
		except:
			cdict["chem_2_3_7_8_tcdd"]=nan
		
		return cdict

	@property
	def chemical_depth_times_z_total(self):
		return self.depth_times_z_total[self.currentchemical.name]

	@property
	def chemical_depth_times_z_total(self):
		return self.depth_times_z_total[self.currentchemical.name]


	@property
	def fractionmass_dissolved(self):
		cdict={}
		try:
			cdict["chem_2_3_7_8_tcdd"]=self.volume * self.chemical_volumefraction_liquid * 1000 /self.chemical_genericdenominatorforcalculatingfractioninphases
		except:
			cdict["chem_2_3_7_8_tcdd"]=nan
		
		return cdict

	@property
	def chemical_fractionmass_dissolved(self):
		return self.fractionmass_dissolved[self.currentchemical.name]

	@property
	def chemical_fractionmass_dissolved(self):
		return self.fractionmass_dissolved[self.currentchemical.name]


	@property
	def d_times_gamma(self):
		cdict={}
		try:
			cdict["chem_2_3_7_8_tcdd"]=self.chemical_gradientofsoilconcentrationchange * self.chemical_d_effective
		except:
			cdict["chem_2_3_7_8_tcdd"]=nan
		
		return cdict

	@property
	def chemical_d_times_gamma(self):
		return self.d_times_gamma[self.currentchemical.name]

	@property
	def chemical_d_times_gamma(self):
		return self.d_times_gamma[self.currentchemical.name]


	@property
	def porosity(self):
		cdict={}
		try:
			cdict["chem_2_3_7_8_tcdd"]=self.chemical_volumefraction_liquid + self.volumefraction_vapor
		except:
			cdict["chem_2_3_7_8_tcdd"]=nan
		
		return cdict

	@property
	def chemical_porosity(self):
		return self.porosity[self.currentchemical.name]

	@property
	def chemical_porosity(self):
		return self.porosity[self.currentchemical.name]


	@property
	def kd_colloid(self):
		cdict={}
		return cdict

	@property
	def chemical_kd_colloid(self):
		return self.kd_colloid[self.currentchemical.name]

	@property
	def chemical_kd_colloid(self):
		return self.kd_colloid[self.currentchemical.name]

	@property
	def reductionrate(self):
		if not hasattr(self,"_reductionrate"):
			self._reductionrate={}
			
	@property
	def chemical_reductionrate(self):
		return self.reductionrate[self.currentchemical.name]


	@property
	def dx2(self):
		cdict={}
		try:
			cdict["chem_2_3_7_8_tcdd"]=2*self.depth*sqrt(self.constants.pi) if (self.chemical_effectiveadvectionvelocity==0) else min(4 * self.chemical_d_effective /self.chemical_effectiveadvectionvelocity,2*self.depth*sqrt(self.constants.pi))
		except:
			cdict["chem_2_3_7_8_tcdd"]=nan
		
		return cdict

	@property
	def chemical_dx2(self):
		return self.dx2[self.currentchemical.name]

	@property
	def chemical_dx2(self):
		return self.dx2[self.currentchemical.name]

	_volumefraction_liquidcolloid=0.25
	@property
	def volumefraction_liquidcolloid(self):
		return self._volumefraction_liquidcolloid
	@volumefraction_liquidcolloid.setter
	def volumefraction_liquidcolloid(self,value):
		self._volumefraction_liquidcolloid=value


	@property
	def z_solid(self):
		cdict={}
		try:
			cdict["chem_2_3_7_8_tcdd"]=(self.rho * self.chemical_kd / 1000) * self.currentchemical.z_purewater
		except:
			cdict["chem_2_3_7_8_tcdd"]=nan
		
		return cdict

	@property
	def chemical_z_solid(self):
		return self.z_solid[self.currentchemical.name]

	@property
	def chemical_z_solid(self):
		return self.z_solid[self.currentchemical.name]


	@property
	def z_times_d_times_gamma(self):
		cdict={}
		try:
			cdict["chem_2_3_7_8_tcdd"]=self.chemical_z_total * self.chemical_d_times_gamma
		except:
			cdict["chem_2_3_7_8_tcdd"]=nan
		
		return cdict

	@property
	def chemical_z_times_d_times_gamma(self):
		return self.z_times_d_times_gamma[self.currentchemical.name]

	@property
	def chemical_z_times_d_times_gamma(self):
		return self.z_times_d_times_gamma[self.currentchemical.name]


	@property
	def effectiveadvectionvelocity(self):
		cdict={}
		try:
			cdict["chem_2_3_7_8_tcdd"]=self.averageverticalvelocity * self.currentchemical.z_purewater/self.chemical_z_total
		except:
			cdict["chem_2_3_7_8_tcdd"]=nan
		
		return cdict

	@property
	def chemical_effectiveadvectionvelocity(self):
		return self.effectiveadvectionvelocity[self.currentchemical.name]

	@property
	def chemical_effectiveadvectionvelocity(self):
		return self.effectiveadvectionvelocity[self.currentchemical.name]

	_rho_colloid=2650.0
	@property
	def rho_colloid(self):
		return self._rho_colloid
	@rho_colloid.setter
	def rho_colloid(self,value):
		self._rho_colloid=value


	@property
	def initialconcentration_g_per_m3(self):
		cdict={}
		try:
			cdict["chem_2_3_7_8_tcdd"]=self.containingscenario.fractioninitialconcentrations * self.chemical_initialconcentration_g_per_m3_usersupplied
		except:
			cdict["chem_2_3_7_8_tcdd"]=nan
		
		return cdict

	@property
	def chemical_initialconcentration_g_per_m3(self):
		return self.initialconcentration_g_per_m3[self.currentchemical.name]

	@property
	def chemical_initialconcentration_g_per_m3(self):
		return self.initialconcentration_g_per_m3[self.currentchemical.name]


	@property
	def d_effective(self):
		cdict={}
		try:
			cdict["chem_2_3_7_8_tcdd"]=self.currentchemical.z_purewater /self.chemical_z_total * self.currentchemical.d_purewater * self.chemical_volumefraction_liquid ** (10 / 3) / self.chemical_porosity ** 2 + self.currentchemical.z_pureair /self.chemical_z_total * self.currentchemical.d_pureair * self.volumefraction_vapor ** (10 / 3) / self.chemical_porosity ** 2
		except:
			cdict["chem_2_3_7_8_tcdd"]=nan
		
		return cdict

	@property
	def chemical_d_effective(self):
		return self.d_effective[self.currentchemical.name]

	@property
	def chemical_d_effective(self):
		return self.d_effective[self.currentchemical.name]


	@property
	def z_liquid(self):
		cdict={}
		try:
			cdict["chem_2_3_7_8_tcdd"]=self.currentchemical.z_purewater
		except:
			cdict["chem_2_3_7_8_tcdd"]=nan
		
		return cdict

	@property
	def chemical_z_liquid(self):
		return self.z_liquid[self.currentchemical.name]

	@property
	def chemical_z_liquid(self):
		return self.z_liquid[self.currentchemical.name]


	@property
	def halflife(self):
		cdict={}
		try:
			cdict["chem_2_3_7_8_tcdd"]=3650.0
		except:
			cdict["chem_2_3_7_8_tcdd"]=nan
		
		return cdict

	@property
	def chemical_halflife(self):
		return self.halflife[self.currentchemical.name]

	@property
	def chemical_halflife(self):
		return self.halflife[self.currentchemical.name]

	@property
	def category(self):
		return ("abiotic | soil | root zone | root zone - default")
	
	_fractionsand=0.25
	@property
	def fractionsand(self):
		return self._fractionsand
	@fractionsand.setter
	def fractionsand(self,value):
		self._fractionsand=value


	@property
	def fractionmass_sorbed(self):
		cdict={}
		try:
			cdict["chem_2_3_7_8_tcdd"]=self.volume * (self.chemical_kd * self.rho) * (1 - self.chemical_volumefraction_liquid - self.volumefraction_vapor) / self.chemical_genericdenominatorforcalculatingfractioninphases
		except:
			cdict["chem_2_3_7_8_tcdd"]=nan
		
		return cdict

	@property
	def chemical_fractionmass_sorbed(self):
		return self.fractionmass_sorbed[self.currentchemical.name]

	@property
	def chemical_fractionmass_sorbed(self):
		return self.fractionmass_sorbed[self.currentchemical.name]


	@property
	def concentrationoutputfactor(self):
		cdict={}
		try:
			cdict["chem_2_3_7_8_tcdd"]=1000 / (self.rho * self.chemical_volumefraction_solid)
		except:
			cdict["chem_2_3_7_8_tcdd"]=nan
		
		return cdict

	@property
	def chemical_concentrationoutputfactor(self):
		return self.concentrationoutputfactor[self.currentchemical.name]

	@property
	def chemical_concentrationoutputfactor(self):
		return self.concentrationoutputfactor[self.currentchemical.name]


	@property
	def initialconcentration_g_per_m3_usersupplied(self):
		cdict={}
		try:
			cdict["chem_2_3_7_8_tcdd"]=0.0
		except:
			cdict["chem_2_3_7_8_tcdd"]=nan
		
		return cdict

	@property
	def chemical_initialconcentration_g_per_m3_usersupplied(self):
		return self.initialconcentration_g_per_m3_usersupplied[self.currentchemical.name]

	@property
	def chemical_initialconcentration_g_per_m3_usersupplied(self):
		return self.initialconcentration_g_per_m3_usersupplied[self.currentchemical.name]


	@property
	def dx1(self):
		cdict={}
		try:
			cdict["chem_2_3_7_8_tcdd"]=(self.chemical_effectiveadvectionvelocity/ (2*self.chemical_totaltransformationrate)) +sqrt((self.chemical_effectiveadvectionvelocity / (2*self.chemical_totaltransformationrate))**2 + self.chemical_d_effective / self.chemical_totaltransformationrate) if self.chemical_effectiveadvectionvelocity>0 else sqrt(self.chemical_d_effective / self.chemical_totaltransformationrate)
		except:
			cdict["chem_2_3_7_8_tcdd"]=nan
		
		return cdict

	@property
	def chemical_dx1(self):
		return self.dx1[self.currentchemical.name]

	@property
	def chemical_dx1(self):
		return self.dx1[self.currentchemical.name]

	_rho=2600.0
	@property
	def rho(self):
		return self._rho
	@rho.setter
	def rho(self,value):
		self._rho=value


	@property
	def totaltransformationrate(self):
		cdict={}
		try:
			cdict["chem_2_3_7_8_tcdd"]=self.chemical_generaldegradationrate
		except:
			cdict["chem_2_3_7_8_tcdd"]=nan
		
		return cdict

	@property
	def chemical_totaltransformationrate(self):
		return self.totaltransformationrate[self.currentchemical.name]

	@property
	def chemical_totaltransformationrate(self):
		return self.totaltransformationrate[self.currentchemical.name]

	@property
	def concentrationoutputunits(self):
		return ("ug/g dry weight")
	
	_ph=0.01
	@property
	def ph(self):
		return self._ph
	@ph.setter
	def ph(self,value):
		self._ph=value


	@property
	def z_colloid(self):
		cdict={}
		return cdict

	@property
	def chemical_z_colloid(self):
		return self.z_colloid[self.currentchemical.name]

	@property
	def chemical_z_colloid(self):
		return self.z_colloid[self.currentchemical.name]


	@property
	def z_total(self):
		cdict={}
		try:
			cdict["chem_2_3_7_8_tcdd"]=self.chemical_z_solid * (1 - self.chemical_porosity) + self.chemical_z_liquid* self.chemical_volumefraction_liquid + self.chemical_z_vapor * self.volumefraction_vapor
		except:
			cdict["chem_2_3_7_8_tcdd"]=nan
		
		return cdict

	@property
	def chemical_z_total(self):
		return self.z_total[self.currentchemical.name]

	@property
	def chemical_z_total(self):
		return self.z_total[self.currentchemical.name]

	@property
	def oxidationrate(self):
		if not hasattr(self,"_oxidationrate"):
			self._oxidationrate={}
			
	@property
	def chemical_oxidationrate(self):
		return self.oxidationrate[self.currentchemical.name]


	@property
	def z_vapor(self):
		cdict={}
		try:
			cdict["chem_2_3_7_8_tcdd"]=self.currentchemical.z_pureair
		except:
			cdict["chem_2_3_7_8_tcdd"]=nan
		
		return cdict

	@property
	def chemical_z_vapor(self):
		return self.z_vapor[self.currentchemical.name]

	@property
	def chemical_z_vapor(self):
		return self.z_vapor[self.currentchemical.name]


	@property
	def one_minus_exp_neg_depth_times_gamma(self):
		cdict={}
		try:
			cdict["chem_2_3_7_8_tcdd"]=1 - self.chemical_exp_neg_depth_times_gamma
		except:
			cdict["chem_2_3_7_8_tcdd"]=nan
		
		return cdict

	@property
	def chemical_one_minus_exp_neg_depth_times_gamma(self):
		return self.one_minus_exp_neg_depth_times_gamma[self.currentchemical.name]

	@property
	def chemical_one_minus_exp_neg_depth_times_gamma(self):
		return self.one_minus_exp_neg_depth_times_gamma[self.currentchemical.name]


	@property
	def genericdenominatorforcalculatingfractioninphases(self):
		cdict={}
		try:
			cdict["chem_2_3_7_8_tcdd"]=self.volume * ((self.chemical_kd * self.rho) * (1 - self.chemical_volumefraction_liquid - self.volumefraction_vapor) + self.chemical_volumefraction_liquid * 1000 + self.volumefraction_vapor * (self.chemical_z_vapor /self.chemical_z_liquid) * 1000 )
		except:
			cdict["chem_2_3_7_8_tcdd"]=nan
		
		return cdict

	@property
	def chemical_genericdenominatorforcalculatingfractioninphases(self):
		return self.genericdenominatorforcalculatingfractioninphases[self.currentchemical.name]

	@property
	def chemical_genericdenominatorforcalculatingfractioninphases(self):
		return self.genericdenominatorforcalculatingfractioninphases[self.currentchemical.name]

	@property
	def area(self):
		return (self.containingvolumeelement.area)
	
	_conc_colloid=0.01
	@property
	def conc_colloid(self):
		return self._conc_colloid
	@conc_colloid.setter
	def conc_colloid(self,value):
		self._conc_colloid=value

	@property
	def height(self):
		return (self.containingvolumeelement.height)
	
	@property
	def depth(self):
		return (self.height)
	

	@property
	def volumefraction_solid(self):
		cdict={}
		try:
			cdict["chem_2_3_7_8_tcdd"]=1.0 - self.chemical_porosity
		except:
			cdict["chem_2_3_7_8_tcdd"]=nan
		
		return cdict

	@property
	def chemical_volumefraction_solid(self):
		return self.volumefraction_solid[self.currentchemical.name]

	@property
	def chemical_volumefraction_solid(self):
		return self.volumefraction_solid[self.currentchemical.name]

	_organiccarboncontent=0.01
	@property
	def organiccarboncontent(self):
		return self._organiccarboncontent
	@organiccarboncontent.setter
	def organiccarboncontent(self,value):
		self._organiccarboncontent=value


	@property
	def generaldegradationrate(self):
		cdict={}
		try:
			cdict["chem_2_3_7_8_tcdd"]=log(2)/ self.chemical_halflife
		except:
			cdict["chem_2_3_7_8_tcdd"]=nan
		
		return cdict

	@property
	def chemical_generaldegradationrate(self):
		return self.generaldegradationrate[self.currentchemical.name]

	@property
	def chemical_generaldegradationrate(self):
		return self.generaldegradationrate[self.currentchemical.name]


	@property
	def depth_times_gamma(self):
		cdict={}
		try:
			cdict["chem_2_3_7_8_tcdd"]=self.chemical_gradientofsoilconcentrationchange * self.height
		except:
			cdict["chem_2_3_7_8_tcdd"]=nan
		
		return cdict

	@property
	def chemical_depth_times_gamma(self):
		return self.depth_times_gamma[self.currentchemical.name]

	@property
	def chemical_depth_times_gamma(self):
		return self.depth_times_gamma[self.currentchemical.name]


	@property
	def useinputcharacteristicdepth_0_meansno_elseyes(self):
		cdict={}
		try:
			cdict["chem_2_3_7_8_tcdd"]=0.0
		except:
			cdict["chem_2_3_7_8_tcdd"]=nan
		
		return cdict

	@property
	def chemical_useinputcharacteristicdepth_0_meansno_elseyes(self):
		return self.useinputcharacteristicdepth_0_meansno_elseyes[self.currentchemical.name]

	@property
	def chemical_useinputcharacteristicdepth_0_meansno_elseyes(self):
		return self.useinputcharacteristicdepth_0_meansno_elseyes[self.currentchemical.name]


	@property
	def gradientofsoilconcentrationchange_calculated(self):
		cdict={}
		try:
			cdict["chem_2_3_7_8_tcdd"]=1/self.chemical_dx2 if (self.chemical_totaltransformationrate == 0) else 1/min(self.chemical_dx1, self.chemical_dx2)
		except:
			cdict["chem_2_3_7_8_tcdd"]=nan
		
		return cdict

	@property
	def chemical_gradientofsoilconcentrationchange_calculated(self):
		return self.gradientofsoilconcentrationchange_calculated[self.currentchemical.name]

	@property
	def chemical_gradientofsoilconcentrationchange_calculated(self):
		return self.gradientofsoilconcentrationchange_calculated[self.currentchemical.name]

	@property
	def totalmass(self):
		return (self.volume * self.rho)
	

	@property
	def volumefraction_liquid(self):
		cdict={}
		try:
			cdict["chem_2_3_7_8_tcdd"]=0.15
		except:
			cdict["chem_2_3_7_8_tcdd"]=nan
		
		return cdict

	@property
	def chemical_volumefraction_liquid(self):
		return self.volumefraction_liquid[self.currentchemical.name]

	@property
	def chemical_volumefraction_liquid(self):
		return self.volumefraction_liquid[self.currentchemical.name]

	_isbiotic=False
	@property
	def isbiotic(self):
		return self._isbiotic
	@isbiotic.setter
	def isbiotic(self,value):
		self._isbiotic=value

	@property
	def methylationrate(self):
		if not hasattr(self,"_methylationrate"):
			self._methylationrate={}
			
	@property
	def chemical_methylationrate(self):
		return self.methylationrate[self.currentchemical.name]


	@property
	def gradientofsoilconcentrationchange(self):
		cdict={}
		try:
			cdict["chem_2_3_7_8_tcdd"]=self.chemical_gradientofsoilconcentrationchange_calculated if (self.chemical_useinputcharacteristicdepth_0_meansno_elseyes!=0) else 1/self.chemical_inputcharacteristicdepth_m
		except:
			cdict["chem_2_3_7_8_tcdd"]=nan
		
		return cdict

	@property
	def chemical_gradientofsoilconcentrationchange(self):
		return self.gradientofsoilconcentrationchange[self.currentchemical.name]

	@property
	def chemical_gradientofsoilconcentrationchange(self):
		return self.gradientofsoilconcentrationchange[self.currentchemical.name]

	_averageverticalvelocity=6.0e-4
	@property
	def averageverticalvelocity(self):
		return self._averageverticalvelocity
	@averageverticalvelocity.setter
	def averageverticalvelocity(self,value):
		self._averageverticalvelocity=value


	@property
	def exp_neg_depth_times_gamma(self):
		cdict={}
		try:
			cdict["chem_2_3_7_8_tcdd"]=exp(-self.chemical_depth_times_gamma)
		except:
			cdict["chem_2_3_7_8_tcdd"]=nan
		
		return cdict

	@property
	def chemical_exp_neg_depth_times_gamma(self):
		return self.exp_neg_depth_times_gamma[self.currentchemical.name]

	@property
	def chemical_exp_neg_depth_times_gamma(self):
		return self.exp_neg_depth_times_gamma[self.currentchemical.name]


	@property
	def kd(self):
		cdict={}
		try:
			cdict["chem_2_3_7_8_tcdd"]=self.currentchemical.k_oc * self.organiccarboncontent
		except:
			cdict["chem_2_3_7_8_tcdd"]=nan
		
		return cdict

	@property
	def chemical_kd(self):
		return self.kd[self.currentchemical.name]

	@property
	def chemical_kd(self):
		return self.kd[self.currentchemical.name]

	@property
	def volumefraction_colloid(self):
		return (self.volumefraction_liquidcolloid *( self.conc_colloid/ self.rho_colloid))
	
	@property
	def volume(self):
		return (self.containingvolumeelement.volume)
	
class soil_surface:
	def __init__(self,constants,containingscenario,currentchemical,containingvolumeelement,comp_objects_dict):
		self.containingscenario=containingscenario
		self.currentchemical=currentchemical
		self.constants=constants
		self.containingvolumeelement=containingvolumeelement
		self.comp_objects_dict=comp_objects_dict
	@property
	def wetconcoutputunits(self):
		return ("ug/g wet weight")
	
	@property
	def acceptableabiotic(self):
		return ("nan")
	

	@property
	def z_liquidcolloid(self):
		cdict={}
		return cdict

	@property
	def chemical_z_liquidcolloid(self):
		return self.z_liquidcolloid[self.currentchemical.name]

	@property
	def chemical_z_liquidcolloid(self):
		return self.z_liquidcolloid[self.currentchemical.name]

	_totalrunoffrate_m3_m2_day=0.01
	@property
	def totalrunoffrate_m3_m2_day(self):
		return self._totalrunoffrate_m3_m2_day
	@totalrunoffrate_m3_m2_day.setter
	def totalrunoffrate_m3_m2_day(self,value):
		self._totalrunoffrate_m3_m2_day=value

	@property
	def demethylationrate(self):
		if not hasattr(self,"_demethylationrate"):
			self._demethylationrate={}
			
	@property
	def chemical_demethylationrate(self):
		return self.demethylationrate[self.currentchemical.name]

	_fractionofareaavailableforverticaldiffusion=1.0
	@property
	def fractionofareaavailableforverticaldiffusion(self):
		return self._fractionofareaavailableforverticaldiffusion
	@fractionofareaavailableforverticaldiffusion.setter
	def fractionofareaavailableforverticaldiffusion(self,value):
		self._fractionofareaavailableforverticaldiffusion=value


	@property
	def fractionmass_vapor(self):
		cdict={}
		try:
			cdict["chem_2_3_7_8_tcdd"]=self.volume * self.volumefraction_vapor * 1000 * (self.chemical_z_vapor /self.chemical_z_liquid) / self.chemical_genericdenominatorforcalculatingfractioninphases
		except:
			cdict["chem_2_3_7_8_tcdd"]=nan
		
		return cdict

	@property
	def chemical_fractionmass_vapor(self):
		return self.fractionmass_vapor[self.currentchemical.name]

	@property
	def chemical_fractionmass_vapor(self):
		return self.fractionmass_vapor[self.currentchemical.name]


	@property
	def inputcharacteristicdepth_m(self):
		cdict={}
		try:
			cdict["chem_2_3_7_8_tcdd"]=0.08
		except:
			cdict["chem_2_3_7_8_tcdd"]=nan
		
		return cdict

	@property
	def chemical_inputcharacteristicdepth_m(self):
		return self.inputcharacteristicdepth_m[self.currentchemical.name]

	@property
	def chemical_inputcharacteristicdepth_m(self):
		return self.inputcharacteristicdepth_m[self.currentchemical.name]


	@property
	def masstransfercoefficientonairsideofairsoilboundary(self):
		cdict={}
		try:
			cdict["chem_2_3_7_8_tcdd"]=self.chemical_vapordrydepositionvelocity_m_day
		except:
			cdict["chem_2_3_7_8_tcdd"]=nan
		
		return cdict

	@property
	def chemical_masstransfercoefficientonairsideofairsoilboundary(self):
		return self.masstransfercoefficientonairsideofairsoilboundary[self.currentchemical.name]

	@property
	def chemical_masstransfercoefficientonairsideofairsoilboundary(self):
		return self.masstransfercoefficientonairsideofairsoilboundary[self.currentchemical.name]


	@property
	def depth_times_z_total(self):
		cdict={}
		try:
			cdict["chem_2_3_7_8_tcdd"]=self.height * self.chemical_z_total
		except:
			cdict["chem_2_3_7_8_tcdd"]=nan
		
		return cdict

	@property
	def chemical_depth_times_z_total(self):
		return self.depth_times_z_total[self.currentchemical.name]

	@property
	def chemical_depth_times_z_total(self):
		return self.depth_times_z_total[self.currentchemical.name]


	@property
	def fractionmass_dissolved(self):
		cdict={}
		try:
			cdict["chem_2_3_7_8_tcdd"]=self.volume * self.chemical_volumefraction_liquid * 1000 /self.chemical_genericdenominatorforcalculatingfractioninphases
		except:
			cdict["chem_2_3_7_8_tcdd"]=nan
		
		return cdict

	@property
	def chemical_fractionmass_dissolved(self):
		return self.fractionmass_dissolved[self.currentchemical.name]

	@property
	def chemical_fractionmass_dissolved(self):
		return self.fractionmass_dissolved[self.currentchemical.name]


	@property
	def d_times_gamma(self):
		cdict={}
		try:
			cdict["chem_2_3_7_8_tcdd"]=self.chemical_gradientofsoilconcentrationchange * self.chemical_d_effective
		except:
			cdict["chem_2_3_7_8_tcdd"]=nan
		
		return cdict

	@property
	def chemical_d_times_gamma(self):
		return self.d_times_gamma[self.currentchemical.name]

	@property
	def chemical_d_times_gamma(self):
		return self.d_times_gamma[self.currentchemical.name]

	_volumefraction_vapor=0.43
	@property
	def volumefraction_vapor(self):
		return self._volumefraction_vapor
	@volumefraction_vapor.setter
	def volumefraction_vapor(self,value):
		self._volumefraction_vapor=value


	@property
	def porosity(self):
		cdict={}
		try:
			cdict["chem_2_3_7_8_tcdd"]=self.chemical_volumefraction_liquid + self.volumefraction_vapor
		except:
			cdict["chem_2_3_7_8_tcdd"]=nan
		
		return cdict

	@property
	def chemical_porosity(self):
		return self.porosity[self.currentchemical.name]

	@property
	def chemical_porosity(self):
		return self.porosity[self.currentchemical.name]


	@property
	def kd_colloid(self):
		cdict={}
		return cdict

	@property
	def chemical_kd_colloid(self):
		return self.kd_colloid[self.currentchemical.name]

	@property
	def chemical_kd_colloid(self):
		return self.kd_colloid[self.currentchemical.name]

	@property
	def reductionrate(self):
		if not hasattr(self,"_reductionrate"):
			self._reductionrate={}
			
	@property
	def chemical_reductionrate(self):
		return self.reductionrate[self.currentchemical.name]


	@property
	def dx2(self):
		cdict={}
		try:
			cdict["chem_2_3_7_8_tcdd"]=2*self.depth*sqrt(self.constants.pi) if (self.chemical_effectiveadvectionvelocity==0) else min(4 * self.chemical_d_effective /self.chemical_effectiveadvectionvelocity,2*self.depth*sqrt(self.constants.pi))
		except:
			cdict["chem_2_3_7_8_tcdd"]=nan
		
		return cdict

	@property
	def chemical_dx2(self):
		return self.dx2[self.currentchemical.name]

	@property
	def chemical_dx2(self):
		return self.dx2[self.currentchemical.name]

	_volumefraction_liquidcolloid=0.22
	@property
	def volumefraction_liquidcolloid(self):
		return self._volumefraction_liquidcolloid
	@volumefraction_liquidcolloid.setter
	def volumefraction_liquidcolloid(self,value):
		self._volumefraction_liquidcolloid=value


	@property
	def z_solid(self):
		cdict={}
		try:
			cdict["chem_2_3_7_8_tcdd"]=(self.rho * self.chemical_kd / 1000) * self.currentchemical.z_purewater
		except:
			cdict["chem_2_3_7_8_tcdd"]=nan
		
		return cdict

	@property
	def chemical_z_solid(self):
		return self.z_solid[self.currentchemical.name]

	@property
	def chemical_z_solid(self):
		return self.z_solid[self.currentchemical.name]


	@property
	def z_times_d_times_gamma(self):
		cdict={}
		try:
			cdict["chem_2_3_7_8_tcdd"]=self.chemical_z_total * self.chemical_d_times_gamma
		except:
			cdict["chem_2_3_7_8_tcdd"]=nan
		
		return cdict

	@property
	def chemical_z_times_d_times_gamma(self):
		return self.z_times_d_times_gamma[self.currentchemical.name]

	@property
	def chemical_z_times_d_times_gamma(self):
		return self.z_times_d_times_gamma[self.currentchemical.name]


	@property
	def abbreviation(self):
		cdict={}
		return cdict

	@property
	def chemical_abbreviation(self):
		return self.abbreviation[self.currentchemical.name]

	@property
	def chemical_abbreviation(self):
		return self.abbreviation[self.currentchemical.name]


	@property
	def effectiveadvectionvelocity(self):
		cdict={}
		try:
			cdict["chem_2_3_7_8_tcdd"]=self.averageverticalvelocity * self.currentchemical.z_purewater/self.chemical_z_total
		except:
			cdict["chem_2_3_7_8_tcdd"]=nan
		
		return cdict

	@property
	def chemical_effectiveadvectionvelocity(self):
		return self.effectiveadvectionvelocity[self.currentchemical.name]

	@property
	def chemical_effectiveadvectionvelocity(self):
		return self.effectiveadvectionvelocity[self.currentchemical.name]

	_rho_colloid=2650.0
	@property
	def rho_colloid(self):
		return self._rho_colloid
	@rho_colloid.setter
	def rho_colloid(self,value):
		self._rho_colloid=value


	@property
	def initialconcentration_g_per_m3(self):
		cdict={}
		try:
			cdict["chem_2_3_7_8_tcdd"]=self.containingscenario.fractioninitialconcentrations * self.chemical_initialconcentration_g_per_m3_usersupplied
		except:
			cdict["chem_2_3_7_8_tcdd"]=nan
		
		return cdict

	@property
	def chemical_initialconcentration_g_per_m3(self):
		return self.initialconcentration_g_per_m3[self.currentchemical.name]

	@property
	def chemical_initialconcentration_g_per_m3(self):
		return self.initialconcentration_g_per_m3[self.currentchemical.name]


	@property
	def d_effective(self):
		cdict={}
		try:
			cdict["chem_2_3_7_8_tcdd"]=self.currentchemical.z_purewater /self.chemical_z_total * self.currentchemical.d_purewater * self.chemical_volumefraction_liquid ** (10 / 3) / self.chemical_porosity ** 2 + self.currentchemical.z_pureair /self.chemical_z_total * self.currentchemical.d_pureair * self.volumefraction_vapor ** (10 / 3) / self.chemical_porosity ** 2
		except:
			cdict["chem_2_3_7_8_tcdd"]=nan
		
		return cdict

	@property
	def chemical_d_effective(self):
		return self.d_effective[self.currentchemical.name]

	@property
	def chemical_d_effective(self):
		return self.d_effective[self.currentchemical.name]


	@property
	def z_liquid(self):
		cdict={}
		try:
			cdict["chem_2_3_7_8_tcdd"]=self.currentchemical.z_purewater
		except:
			cdict["chem_2_3_7_8_tcdd"]=nan
		
		return cdict

	@property
	def chemical_z_liquid(self):
		return self.z_liquid[self.currentchemical.name]

	@property
	def chemical_z_liquid(self):
		return self.z_liquid[self.currentchemical.name]


	@property
	def halflife(self):
		cdict={}
		try:
			cdict["chem_2_3_7_8_tcdd"]=3650.0
		except:
			cdict["chem_2_3_7_8_tcdd"]=nan
		
		return cdict

	@property
	def chemical_halflife(self):
		return self.halflife[self.currentchemical.name]

	@property
	def chemical_halflife(self):
		return self.halflife[self.currentchemical.name]

	@property
	def category(self):
		return ("abiotic | soil | surface soil | surface soil - default")
	
	_fractionsand=0.25
	@property
	def fractionsand(self):
		return self._fractionsand
	@fractionsand.setter
	def fractionsand(self,value):
		self._fractionsand=value


	@property
	def fractionmass_sorbed(self):
		cdict={}
		try:
			cdict["chem_2_3_7_8_tcdd"]=self.volume * (self.chemical_kd * self.rho) * (1 - self.chemical_volumefraction_liquid - self.volumefraction_vapor) / self.chemical_genericdenominatorforcalculatingfractioninphases
		except:
			cdict["chem_2_3_7_8_tcdd"]=nan
		
		return cdict

	@property
	def chemical_fractionmass_sorbed(self):
		return self.fractionmass_sorbed[self.currentchemical.name]

	@property
	def chemical_fractionmass_sorbed(self):
		return self.fractionmass_sorbed[self.currentchemical.name]


	@property
	def concentrationoutputfactor(self):
		cdict={}
		try:
			cdict["chem_2_3_7_8_tcdd"]=(1000 / (self.rho * self.chemical_volumefraction_solid))
		except:
			cdict["chem_2_3_7_8_tcdd"]=nan
		
		return cdict

	@property
	def chemical_concentrationoutputfactor(self):
		return self.concentrationoutputfactor[self.currentchemical.name]

	@property
	def chemical_concentrationoutputfactor(self):
		return self.concentrationoutputfactor[self.currentchemical.name]


	@property
	def initialconcentration_g_per_m3_usersupplied(self):
		cdict={}
		try:
			cdict["chem_2_3_7_8_tcdd"]=0.0
		except:
			cdict["chem_2_3_7_8_tcdd"]=nan
		
		return cdict

	@property
	def chemical_initialconcentration_g_per_m3_usersupplied(self):
		return self.initialconcentration_g_per_m3_usersupplied[self.currentchemical.name]

	@property
	def chemical_initialconcentration_g_per_m3_usersupplied(self):
		return self.initialconcentration_g_per_m3_usersupplied[self.currentchemical.name]


	@property
	def dx1(self):
		cdict={}
		try:
			cdict["chem_2_3_7_8_tcdd"]=(self.chemical_effectiveadvectionvelocity/ (2*self.chemical_totaltransformationrate)) +sqrt((self.chemical_effectiveadvectionvelocity / (2*self.chemical_totaltransformationrate))**2 + self.chemical_d_effective / self.chemical_totaltransformationrate) if self.chemical_effectiveadvectionvelocity>0 else sqrt(self.chemical_d_effective / self.chemical_totaltransformationrate)
		except:
			cdict["chem_2_3_7_8_tcdd"]=nan
		
		return cdict

	@property
	def chemical_dx1(self):
		return self.dx1[self.currentchemical.name]

	@property
	def chemical_dx1(self):
		return self.dx1[self.currentchemical.name]

	_rho=2600.0
	@property
	def rho(self):
		return self._rho
	@rho.setter
	def rho(self,value):
		self._rho=value


	@property
	def totaltransformationrate(self):
		cdict={}
		try:
			cdict["chem_2_3_7_8_tcdd"]=self.chemical_generaldegradationrate
		except:
			cdict["chem_2_3_7_8_tcdd"]=nan
		
		return cdict

	@property
	def chemical_totaltransformationrate(self):
		return self.totaltransformationrate[self.currentchemical.name]

	@property
	def chemical_totaltransformationrate(self):
		return self.totaltransformationrate[self.currentchemical.name]

	@property
	def concentrationoutputunits(self):
		return ("ug/g dry weight")
	
	_ph=0.01
	@property
	def ph(self):
		return self._ph
	@ph.setter
	def ph(self,value):
		self._ph=value


	@property
	def z_colloid(self):
		cdict={}
		return cdict

	@property
	def chemical_z_colloid(self):
		return self.z_colloid[self.currentchemical.name]

	@property
	def chemical_z_colloid(self):
		return self.z_colloid[self.currentchemical.name]


	@property
	def z_total(self):
		cdict={}
		try:
			cdict["chem_2_3_7_8_tcdd"]=self.chemical_z_solid * (1 - self.chemical_porosity) + self.chemical_z_liquid* self.chemical_volumefraction_liquid + self.chemical_z_vapor * self.volumefraction_vapor
		except:
			cdict["chem_2_3_7_8_tcdd"]=nan
		
		return cdict

	@property
	def chemical_z_total(self):
		return self.z_total[self.currentchemical.name]

	@property
	def chemical_z_total(self):
		return self.z_total[self.currentchemical.name]

	_fractionofareaavailableforrunoff=1.0
	@property
	def fractionofareaavailableforrunoff(self):
		return self._fractionofareaavailableforrunoff
	@fractionofareaavailableforrunoff.setter
	def fractionofareaavailableforrunoff(self,value):
		self._fractionofareaavailableforrunoff=value

	@property
	def oxidationrate(self):
		if not hasattr(self,"_oxidationrate"):
			self._oxidationrate={}
			
	@property
	def chemical_oxidationrate(self):
		return self.oxidationrate[self.currentchemical.name]


	@property
	def z_vapor(self):
		cdict={}
		try:
			cdict["chem_2_3_7_8_tcdd"]=self.currentchemical.z_pureair
		except:
			cdict["chem_2_3_7_8_tcdd"]=nan
		
		return cdict

	@property
	def chemical_z_vapor(self):
		return self.z_vapor[self.currentchemical.name]

	@property
	def chemical_z_vapor(self):
		return self.z_vapor[self.currentchemical.name]


	@property
	def one_minus_exp_neg_depth_times_gamma(self):
		cdict={}
		try:
			cdict["chem_2_3_7_8_tcdd"]=1 - self.chemical_exp_neg_depth_times_gamma
		except:
			cdict["chem_2_3_7_8_tcdd"]=nan
		
		return cdict

	@property
	def chemical_one_minus_exp_neg_depth_times_gamma(self):
		return self.one_minus_exp_neg_depth_times_gamma[self.currentchemical.name]

	@property
	def chemical_one_minus_exp_neg_depth_times_gamma(self):
		return self.one_minus_exp_neg_depth_times_gamma[self.currentchemical.name]


	@property
	def genericdenominatorforcalculatingfractioninphases(self):
		cdict={}
		try:
			cdict["chem_2_3_7_8_tcdd"]=self.volume * ((self.chemical_kd * self.rho) * (1 - self.chemical_volumefraction_liquid - self.volumefraction_vapor) + self.chemical_volumefraction_liquid * 1000 + self.volumefraction_vapor * (self.chemical_z_vapor /self.chemical_z_liquid) * 1000 )
		except:
			cdict["chem_2_3_7_8_tcdd"]=nan
		
		return cdict

	@property
	def chemical_genericdenominatorforcalculatingfractioninphases(self):
		return self.genericdenominatorforcalculatingfractioninphases[self.currentchemical.name]

	@property
	def chemical_genericdenominatorforcalculatingfractioninphases(self):
		return self.genericdenominatorforcalculatingfractioninphases[self.currentchemical.name]

	@property
	def area(self):
		return (self.containingvolumeelement.area)
	
	_conc_colloid=0.01
	@property
	def conc_colloid(self):
		return self._conc_colloid
	@conc_colloid.setter
	def conc_colloid(self,value):
		self._conc_colloid=value

	@property
	def height(self):
		return (self.containingvolumeelement.height)
	
	@property
	def depth(self):
		return (self.height)
	

	@property
	def volumefraction_solid(self):
		cdict={}
		try:
			cdict["chem_2_3_7_8_tcdd"]=1.0 - self.chemical_porosity
		except:
			cdict["chem_2_3_7_8_tcdd"]=nan
		
		return cdict

	@property
	def chemical_volumefraction_solid(self):
		return self.volumefraction_solid[self.currentchemical.name]

	@property
	def chemical_volumefraction_solid(self):
		return self.volumefraction_solid[self.currentchemical.name]

	_organiccarboncontent=0.01
	@property
	def organiccarboncontent(self):
		return self._organiccarboncontent
	@organiccarboncontent.setter
	def organiccarboncontent(self,value):
		self._organiccarboncontent=value

	_airsoilboundarythickness=0.005
	@property
	def airsoilboundarythickness(self):
		return self._airsoilboundarythickness
	@airsoilboundarythickness.setter
	def airsoilboundarythickness(self,value):
		self._airsoilboundarythickness=value


	@property
	def generaldegradationrate(self):
		cdict={}
		try:
			cdict["chem_2_3_7_8_tcdd"]=log(2)/ self.chemical_halflife
		except:
			cdict["chem_2_3_7_8_tcdd"]=nan
		
		return cdict

	@property
	def chemical_generaldegradationrate(self):
		return self.generaldegradationrate[self.currentchemical.name]

	@property
	def chemical_generaldegradationrate(self):
		return self.generaldegradationrate[self.currentchemical.name]


	@property
	def depth_times_gamma(self):
		cdict={}
		try:
			cdict["chem_2_3_7_8_tcdd"]=self.chemical_gradientofsoilconcentrationchange * self.height
		except:
			cdict["chem_2_3_7_8_tcdd"]=nan
		
		return cdict

	@property
	def chemical_depth_times_gamma(self):
		return self.depth_times_gamma[self.currentchemical.name]

	@property
	def chemical_depth_times_gamma(self):
		return self.depth_times_gamma[self.currentchemical.name]


	@property
	def useinputcharacteristicdepth_0_meansno_elseyes(self):
		cdict={}
		try:
			cdict["chem_2_3_7_8_tcdd"]=0.0
		except:
			cdict["chem_2_3_7_8_tcdd"]=nan
		
		return cdict

	@property
	def chemical_useinputcharacteristicdepth_0_meansno_elseyes(self):
		return self.useinputcharacteristicdepth_0_meansno_elseyes[self.currentchemical.name]

	@property
	def chemical_useinputcharacteristicdepth_0_meansno_elseyes(self):
		return self.useinputcharacteristicdepth_0_meansno_elseyes[self.currentchemical.name]


	@property
	def wetconcoutputfactor(self):
		cdict={}
		try:
			cdict["chem_2_3_7_8_tcdd"]=(self.chemical_volumefraction_solid * self.rho) / ((self.chemical_volumefraction_solid * self.rho) + (self.chemical_volumefraction_liquid * self.constants.kg_per_m3_water))
		except:
			cdict["chem_2_3_7_8_tcdd"]=nan
		
		return cdict

	@property
	def chemical_wetconcoutputfactor(self):
		return self.wetconcoutputfactor[self.currentchemical.name]

	@property
	def chemical_wetconcoutputfactor(self):
		return self.wetconcoutputfactor[self.currentchemical.name]

	_totalerosionrate_kg_m2_day=0.01
	@property
	def totalerosionrate_kg_m2_day(self):
		return self._totalerosionrate_kg_m2_day
	@totalerosionrate_kg_m2_day.setter
	def totalerosionrate_kg_m2_day(self,value):
		self._totalerosionrate_kg_m2_day=value

	_fractionofareaavailableforerosion=1.0
	@property
	def fractionofareaavailableforerosion(self):
		return self._fractionofareaavailableforerosion
	@fractionofareaavailableforerosion.setter
	def fractionofareaavailableforerosion(self,value):
		self._fractionofareaavailableforerosion=value


	@property
	def gradientofsoilconcentrationchange_calculated(self):
		cdict={}
		try:
			cdict["chem_2_3_7_8_tcdd"]=1/self.chemical_dx2 if (self.chemical_totaltransformationrate == 0) else 1/min(self.chemical_dx1, self.chemical_dx2)
		except:
			cdict["chem_2_3_7_8_tcdd"]=nan
		
		return cdict

	@property
	def chemical_gradientofsoilconcentrationchange_calculated(self):
		return self.gradientofsoilconcentrationchange_calculated[self.currentchemical.name]

	@property
	def chemical_gradientofsoilconcentrationchange_calculated(self):
		return self.gradientofsoilconcentrationchange_calculated[self.currentchemical.name]

	@property
	def totalmass(self):
		return (self.volume * self.rho)
	

	@property
	def volumefraction_liquid(self):
		cdict={}
		try:
			cdict["chem_2_3_7_8_tcdd"]=0.15
		except:
			cdict["chem_2_3_7_8_tcdd"]=nan
		
		return cdict

	@property
	def chemical_volumefraction_liquid(self):
		return self.volumefraction_liquid[self.currentchemical.name]

	@property
	def chemical_volumefraction_liquid(self):
		return self.volumefraction_liquid[self.currentchemical.name]

	_isbiotic=False
	@property
	def isbiotic(self):
		return self._isbiotic
	@isbiotic.setter
	def isbiotic(self,value):
		self._isbiotic=value

	@property
	def methylationrate(self):
		if not hasattr(self,"_methylationrate"):
			self._methylationrate={}
			
	@property
	def chemical_methylationrate(self):
		return self.methylationrate[self.currentchemical.name]


	@property
	def gradientofsoilconcentrationchange(self):
		cdict={}
		try:
			cdict["chem_2_3_7_8_tcdd"]=self.chemical_gradientofsoilconcentrationchange_calculated if (self.chemical_useinputcharacteristicdepth_0_meansno_elseyes!=0) else 1/self.chemical_inputcharacteristicdepth_m
		except:
			cdict["chem_2_3_7_8_tcdd"]=nan
		
		return cdict

	@property
	def chemical_gradientofsoilconcentrationchange(self):
		return self.gradientofsoilconcentrationchange[self.currentchemical.name]

	@property
	def chemical_gradientofsoilconcentrationchange(self):
		return self.gradientofsoilconcentrationchange[self.currentchemical.name]

	_averageverticalvelocity=6.0e-4
	@property
	def averageverticalvelocity(self):
		return self._averageverticalvelocity
	@averageverticalvelocity.setter
	def averageverticalvelocity(self,value):
		self._averageverticalvelocity=value


	@property
	def exp_neg_depth_times_gamma(self):
		cdict={}
		try:
			cdict["chem_2_3_7_8_tcdd"]=exp(-self.chemical_depth_times_gamma)
		except:
			cdict["chem_2_3_7_8_tcdd"]=nan
		
		return cdict

	@property
	def chemical_exp_neg_depth_times_gamma(self):
		return self.exp_neg_depth_times_gamma[self.currentchemical.name]

	@property
	def chemical_exp_neg_depth_times_gamma(self):
		return self.exp_neg_depth_times_gamma[self.currentchemical.name]


	@property
	def vapordrydepositionvelocity_m_day(self):
		cdict={}
		try:
			cdict["chem_2_3_7_8_tcdd"]=self.currentchemical.d_pureair / self.airsoilboundarythickness
		except:
			cdict["chem_2_3_7_8_tcdd"]=nan
		
		return cdict

	@property
	def chemical_vapordrydepositionvelocity_m_day(self):
		return self.vapordrydepositionvelocity_m_day[self.currentchemical.name]

	@property
	def chemical_vapordrydepositionvelocity_m_day(self):
		return self.vapordrydepositionvelocity_m_day[self.currentchemical.name]


	@property
	def kd(self):
		cdict={}
		try:
			cdict["chem_2_3_7_8_tcdd"]=self.currentchemical.k_oc * self.organiccarboncontent
		except:
			cdict["chem_2_3_7_8_tcdd"]=nan
		
		return cdict

	@property
	def chemical_kd(self):
		return self.kd[self.currentchemical.name]

	@property
	def chemical_kd(self):
		return self.kd[self.currentchemical.name]

	@property
	def volumefraction_colloid(self):
		return (self.volumefraction_liquidcolloid *( self.conc_colloid/ self.rho_colloid))
	
	@property
	def volume(self):
		return (self.containingvolumeelement.volume)
	
class soil_vadose_zone:
	def __init__(self,constants,containingscenario,currentchemical,containingvolumeelement,comp_objects_dict):
		self.containingscenario=containingscenario
		self.currentchemical=currentchemical
		self.constants=constants
		self.containingvolumeelement=containingvolumeelement
		self.comp_objects_dict=comp_objects_dict
	@property
	def acceptableabiotic(self):
		return ("nan")
	
	@property
	def demethylationrate(self):
		if not hasattr(self,"_demethylationrate"):
			self._demethylationrate={}
			
	@property
	def chemical_demethylationrate(self):
		return self.demethylationrate[self.currentchemical.name]


	@property
	def fractionmass_vapor(self):
		cdict={}
		try:
			cdict["chem_2_3_7_8_tcdd"]=self.volume * self.volumefraction_vapor * 1000 * (self.chemical_z_vapor /self.chemical_z_liquid) / self.chemical_genericdenominatorforcalculatingfractioninphases
		except:
			cdict["chem_2_3_7_8_tcdd"]=nan
		
		return cdict

	@property
	def chemical_fractionmass_vapor(self):
		return self.fractionmass_vapor[self.currentchemical.name]

	@property
	def chemical_fractionmass_vapor(self):
		return self.fractionmass_vapor[self.currentchemical.name]


	@property
	def inputcharacteristicdepth_m(self):
		cdict={}
		try:
			cdict["chem_2_3_7_8_tcdd"]=0.08
		except:
			cdict["chem_2_3_7_8_tcdd"]=nan
		
		return cdict

	@property
	def chemical_inputcharacteristicdepth_m(self):
		return self.inputcharacteristicdepth_m[self.currentchemical.name]

	@property
	def chemical_inputcharacteristicdepth_m(self):
		return self.inputcharacteristicdepth_m[self.currentchemical.name]

	_volumefraction_vapor=0.25
	@property
	def volumefraction_vapor(self):
		return self._volumefraction_vapor
	@volumefraction_vapor.setter
	def volumefraction_vapor(self,value):
		self._volumefraction_vapor=value


	@property
	def depth_times_z_total(self):
		cdict={}
		try:
			cdict["chem_2_3_7_8_tcdd"]=self.height * self.chemical_z_total
		except:
			cdict["chem_2_3_7_8_tcdd"]=nan
		
		return cdict

	@property
	def chemical_depth_times_z_total(self):
		return self.depth_times_z_total[self.currentchemical.name]

	@property
	def chemical_depth_times_z_total(self):
		return self.depth_times_z_total[self.currentchemical.name]


	@property
	def fractionmass_dissolved(self):
		cdict={}
		try:
			cdict["chem_2_3_7_8_tcdd"]=self.volume * self.volumefraction_liquid * 1000 /self.chemical_genericdenominatorforcalculatingfractioninphases
		except:
			cdict["chem_2_3_7_8_tcdd"]=nan
		
		return cdict

	@property
	def chemical_fractionmass_dissolved(self):
		return self.fractionmass_dissolved[self.currentchemical.name]

	@property
	def chemical_fractionmass_dissolved(self):
		return self.fractionmass_dissolved[self.currentchemical.name]


	@property
	def d_times_gamma(self):
		cdict={}
		try:
			cdict["chem_2_3_7_8_tcdd"]=self.chemical_gradientofsoilconcentrationchange * self.chemical_d_effective
		except:
			cdict["chem_2_3_7_8_tcdd"]=nan
		
		return cdict

	@property
	def chemical_d_times_gamma(self):
		return self.d_times_gamma[self.currentchemical.name]

	@property
	def chemical_d_times_gamma(self):
		return self.d_times_gamma[self.currentchemical.name]

	@property
	def porosity(self):
		return (self.volumefraction_liquid + self.volumefraction_vapor)
	
	@property
	def reductionrate(self):
		if not hasattr(self,"_reductionrate"):
			self._reductionrate={}
			
	@property
	def chemical_reductionrate(self):
		return self.reductionrate[self.currentchemical.name]


	@property
	def dx2(self):
		cdict={}
		try:
			cdict["chem_2_3_7_8_tcdd"]=2*self.depth*sqrt(self.constants.pi) if (self.chemical_effectiveadvectionvelocity==0) else min(4 * self.chemical_d_effective /self.chemical_effectiveadvectionvelocity,2*self.depth*sqrt(self.constants.pi))
		except:
			cdict["chem_2_3_7_8_tcdd"]=nan
		
		return cdict

	@property
	def chemical_dx2(self):
		return self.dx2[self.currentchemical.name]

	@property
	def chemical_dx2(self):
		return self.dx2[self.currentchemical.name]


	@property
	def z_solid(self):
		cdict={}
		try:
			cdict["chem_2_3_7_8_tcdd"]=(self.rho * self.chemical_kd / 1000) * self.currentchemical.z_purewater
		except:
			cdict["chem_2_3_7_8_tcdd"]=nan
		
		return cdict

	@property
	def chemical_z_solid(self):
		return self.z_solid[self.currentchemical.name]

	@property
	def chemical_z_solid(self):
		return self.z_solid[self.currentchemical.name]


	@property
	def z_times_d_times_gamma(self):
		cdict={}
		try:
			cdict["chem_2_3_7_8_tcdd"]=self.chemical_z_total * self.chemical_d_times_gamma
		except:
			cdict["chem_2_3_7_8_tcdd"]=nan
		
		return cdict

	@property
	def chemical_z_times_d_times_gamma(self):
		return self.z_times_d_times_gamma[self.currentchemical.name]

	@property
	def chemical_z_times_d_times_gamma(self):
		return self.z_times_d_times_gamma[self.currentchemical.name]


	@property
	def effectiveadvectionvelocity(self):
		cdict={}
		try:
			cdict["chem_2_3_7_8_tcdd"]=self.averageverticalvelocity * self.currentchemical.z_purewater/self.chemical_z_total
		except:
			cdict["chem_2_3_7_8_tcdd"]=nan
		
		return cdict

	@property
	def chemical_effectiveadvectionvelocity(self):
		return self.effectiveadvectionvelocity[self.currentchemical.name]

	@property
	def chemical_effectiveadvectionvelocity(self):
		return self.effectiveadvectionvelocity[self.currentchemical.name]


	@property
	def initialconcentration_g_per_m3(self):
		cdict={}
		try:
			cdict["chem_2_3_7_8_tcdd"]=self.containingscenario.fractioninitialconcentrations * self.chemical_initialconcentration_g_per_m3_usersupplied
		except:
			cdict["chem_2_3_7_8_tcdd"]=nan
		
		return cdict

	@property
	def chemical_initialconcentration_g_per_m3(self):
		return self.initialconcentration_g_per_m3[self.currentchemical.name]

	@property
	def chemical_initialconcentration_g_per_m3(self):
		return self.initialconcentration_g_per_m3[self.currentchemical.name]


	@property
	def d_effective(self):
		cdict={}
		try:
			cdict["chem_2_3_7_8_tcdd"]=self.currentchemical.z_purewater /self.chemical_z_total * self.currentchemical.d_purewater * self.volumefraction_liquid ** (10 / 3) / self.porosity ** 2 + self.currentchemical.z_pureair /self.chemical_z_total * self.currentchemical.d_pureair * self.volumefraction_vapor ** (10 / 3) / self.porosity ** 2
		except:
			cdict["chem_2_3_7_8_tcdd"]=nan
		
		return cdict

	@property
	def chemical_d_effective(self):
		return self.d_effective[self.currentchemical.name]

	@property
	def chemical_d_effective(self):
		return self.d_effective[self.currentchemical.name]


	@property
	def z_liquid(self):
		cdict={}
		try:
			cdict["chem_2_3_7_8_tcdd"]=self.currentchemical.z_purewater
		except:
			cdict["chem_2_3_7_8_tcdd"]=nan
		
		return cdict

	@property
	def chemical_z_liquid(self):
		return self.z_liquid[self.currentchemical.name]

	@property
	def chemical_z_liquid(self):
		return self.z_liquid[self.currentchemical.name]


	@property
	def halflife(self):
		cdict={}
		try:
			cdict["chem_2_3_7_8_tcdd"]=1008.0
		except:
			cdict["chem_2_3_7_8_tcdd"]=nan
		
		return cdict

	@property
	def chemical_halflife(self):
		return self.halflife[self.currentchemical.name]

	@property
	def chemical_halflife(self):
		return self.halflife[self.currentchemical.name]

	@property
	def category(self):
		return ("abiotic | soil | vadose zone | vadose zone - default")
	
	_fractionsand=0.35
	@property
	def fractionsand(self):
		return self._fractionsand
	@fractionsand.setter
	def fractionsand(self,value):
		self._fractionsand=value


	@property
	def fractionmass_sorbed(self):
		cdict={}
		try:
			cdict["chem_2_3_7_8_tcdd"]=self.volume * (self.chemical_kd * self.rho) * (1 - self.volumefraction_liquid - self.volumefraction_vapor) / self.chemical_genericdenominatorforcalculatingfractioninphases
		except:
			cdict["chem_2_3_7_8_tcdd"]=nan
		
		return cdict

	@property
	def chemical_fractionmass_sorbed(self):
		return self.fractionmass_sorbed[self.currentchemical.name]

	@property
	def chemical_fractionmass_sorbed(self):
		return self.fractionmass_sorbed[self.currentchemical.name]

	@property
	def concentrationoutputfactor(self):
		return (1.0 / (self.rho * self.volumefraction_solid * 1000.0 ))
	

	@property
	def initialconcentration_g_per_m3_usersupplied(self):
		cdict={}
		try:
			cdict["chem_2_3_7_8_tcdd"]=0.0
		except:
			cdict["chem_2_3_7_8_tcdd"]=nan
		
		return cdict

	@property
	def chemical_initialconcentration_g_per_m3_usersupplied(self):
		return self.initialconcentration_g_per_m3_usersupplied[self.currentchemical.name]

	@property
	def chemical_initialconcentration_g_per_m3_usersupplied(self):
		return self.initialconcentration_g_per_m3_usersupplied[self.currentchemical.name]


	@property
	def dx1(self):
		cdict={}
		try:
			cdict["chem_2_3_7_8_tcdd"]=(self.chemical_effectiveadvectionvelocity/ (2*self.chemical_totaltransformationrate)) +sqrt((self.chemical_effectiveadvectionvelocity / (2*self.chemical_totaltransformationrate))**2 + self.chemical_d_effective / self.chemical_totaltransformationrate) if self.chemical_effectiveadvectionvelocity>0 else sqrt(self.chemical_d_effective / self.chemical_totaltransformationrate)
		except:
			cdict["chem_2_3_7_8_tcdd"]=nan
		
		return cdict

	@property
	def chemical_dx1(self):
		return self.dx1[self.currentchemical.name]

	@property
	def chemical_dx1(self):
		return self.dx1[self.currentchemical.name]

	_rho=2600.0
	@property
	def rho(self):
		return self._rho
	@rho.setter
	def rho(self,value):
		self._rho=value


	@property
	def totaltransformationrate(self):
		cdict={}
		try:
			cdict["chem_2_3_7_8_tcdd"]=self.chemical_generaldegradationrate
		except:
			cdict["chem_2_3_7_8_tcdd"]=nan
		
		return cdict

	@property
	def chemical_totaltransformationrate(self):
		return self.totaltransformationrate[self.currentchemical.name]

	@property
	def chemical_totaltransformationrate(self):
		return self.totaltransformationrate[self.currentchemical.name]

	@property
	def concentrationoutputunits(self):
		return ("g/g dry weight")
	
	_ph=0.01
	@property
	def ph(self):
		return self._ph
	@ph.setter
	def ph(self,value):
		self._ph=value


	@property
	def z_total(self):
		cdict={}
		try:
			cdict["chem_2_3_7_8_tcdd"]=self.chemical_z_solid * (1 - self.porosity) + self.chemical_z_liquid* self.volumefraction_liquid + self.chemical_z_vapor * self.volumefraction_vapor
		except:
			cdict["chem_2_3_7_8_tcdd"]=nan
		
		return cdict

	@property
	def chemical_z_total(self):
		return self.z_total[self.currentchemical.name]

	@property
	def chemical_z_total(self):
		return self.z_total[self.currentchemical.name]

	@property
	def oxidationrate(self):
		if not hasattr(self,"_oxidationrate"):
			self._oxidationrate={}
			
	@property
	def chemical_oxidationrate(self):
		return self.oxidationrate[self.currentchemical.name]


	@property
	def z_vapor(self):
		cdict={}
		try:
			cdict["chem_2_3_7_8_tcdd"]=self.currentchemical.z_pureair
		except:
			cdict["chem_2_3_7_8_tcdd"]=nan
		
		return cdict

	@property
	def chemical_z_vapor(self):
		return self.z_vapor[self.currentchemical.name]

	@property
	def chemical_z_vapor(self):
		return self.z_vapor[self.currentchemical.name]


	@property
	def one_minus_exp_neg_depth_times_gamma(self):
		cdict={}
		try:
			cdict["chem_2_3_7_8_tcdd"]=1 - self.chemical_exp_neg_depth_times_gamma
		except:
			cdict["chem_2_3_7_8_tcdd"]=nan
		
		return cdict

	@property
	def chemical_one_minus_exp_neg_depth_times_gamma(self):
		return self.one_minus_exp_neg_depth_times_gamma[self.currentchemical.name]

	@property
	def chemical_one_minus_exp_neg_depth_times_gamma(self):
		return self.one_minus_exp_neg_depth_times_gamma[self.currentchemical.name]


	@property
	def genericdenominatorforcalculatingfractioninphases(self):
		cdict={}
		try:
			cdict["chem_2_3_7_8_tcdd"]=self.volume * ((self.chemical_kd * self.rho) * (1 - self.volumefraction_liquid - self.volumefraction_vapor) + self.volumefraction_liquid * 1000 + self.volumefraction_vapor * (self.chemical_z_vapor /self.chemical_z_liquid) * 1000 )
		except:
			cdict["chem_2_3_7_8_tcdd"]=nan
		
		return cdict

	@property
	def chemical_genericdenominatorforcalculatingfractioninphases(self):
		return self.genericdenominatorforcalculatingfractioninphases[self.currentchemical.name]

	@property
	def chemical_genericdenominatorforcalculatingfractioninphases(self):
		return self.genericdenominatorforcalculatingfractioninphases[self.currentchemical.name]

	@property
	def area(self):
		return (self.containingvolumeelement.area)
	
	@property
	def height(self):
		return (self.containingvolumeelement.height)
	
	@property
	def depth(self):
		return (self.height)
	
	@property
	def volumefraction_solid(self):
		return (1.0 - self.porosity)
	
	_organiccarboncontent=0.01
	@property
	def organiccarboncontent(self):
		return self._organiccarboncontent
	@organiccarboncontent.setter
	def organiccarboncontent(self,value):
		self._organiccarboncontent=value


	@property
	def generaldegradationrate(self):
		cdict={}
		try:
			cdict["chem_2_3_7_8_tcdd"]=log(2)/ self.chemical_halflife
		except:
			cdict["chem_2_3_7_8_tcdd"]=nan
		
		return cdict

	@property
	def chemical_generaldegradationrate(self):
		return self.generaldegradationrate[self.currentchemical.name]

	@property
	def chemical_generaldegradationrate(self):
		return self.generaldegradationrate[self.currentchemical.name]


	@property
	def depth_times_gamma(self):
		cdict={}
		try:
			cdict["chem_2_3_7_8_tcdd"]=self.chemical_gradientofsoilconcentrationchange * self.height
		except:
			cdict["chem_2_3_7_8_tcdd"]=nan
		
		return cdict

	@property
	def chemical_depth_times_gamma(self):
		return self.depth_times_gamma[self.currentchemical.name]

	@property
	def chemical_depth_times_gamma(self):
		return self.depth_times_gamma[self.currentchemical.name]


	@property
	def useinputcharacteristicdepth_0_meansno_elseyes(self):
		cdict={}
		try:
			cdict["chem_2_3_7_8_tcdd"]=0.0
		except:
			cdict["chem_2_3_7_8_tcdd"]=nan
		
		return cdict

	@property
	def chemical_useinputcharacteristicdepth_0_meansno_elseyes(self):
		return self.useinputcharacteristicdepth_0_meansno_elseyes[self.currentchemical.name]

	@property
	def chemical_useinputcharacteristicdepth_0_meansno_elseyes(self):
		return self.useinputcharacteristicdepth_0_meansno_elseyes[self.currentchemical.name]


	@property
	def gradientofsoilconcentrationchange_calculated(self):
		cdict={}
		try:
			cdict["chem_2_3_7_8_tcdd"]=1/self.chemical_dx2 if (self.chemical_totaltransformationrate == 0) else 1/min(self.chemical_dx1, self.chemical_dx2)
		except:
			cdict["chem_2_3_7_8_tcdd"]=nan
		
		return cdict

	@property
	def chemical_gradientofsoilconcentrationchange_calculated(self):
		return self.gradientofsoilconcentrationchange_calculated[self.currentchemical.name]

	@property
	def chemical_gradientofsoilconcentrationchange_calculated(self):
		return self.gradientofsoilconcentrationchange_calculated[self.currentchemical.name]

	@property
	def totalmass(self):
		return (self.volume * self.rho)
	
	_volumefraction_liquid=0.14
	@property
	def volumefraction_liquid(self):
		return self._volumefraction_liquid
	@volumefraction_liquid.setter
	def volumefraction_liquid(self,value):
		self._volumefraction_liquid=value

	_isbiotic=False
	@property
	def isbiotic(self):
		return self._isbiotic
	@isbiotic.setter
	def isbiotic(self,value):
		self._isbiotic=value

	@property
	def methylationrate(self):
		if not hasattr(self,"_methylationrate"):
			self._methylationrate={}
			
	@property
	def chemical_methylationrate(self):
		return self.methylationrate[self.currentchemical.name]


	@property
	def gradientofsoilconcentrationchange(self):
		cdict={}
		try:
			cdict["chem_2_3_7_8_tcdd"]=self.chemical_gradientofsoilconcentrationchange_calculated if (self.chemical_useinputcharacteristicdepth_0_meansno_elseyes!=0) else 1/self.chemical_inputcharacteristicdepth_m
		except:
			cdict["chem_2_3_7_8_tcdd"]=nan
		
		return cdict

	@property
	def chemical_gradientofsoilconcentrationchange(self):
		return self.gradientofsoilconcentrationchange[self.currentchemical.name]

	@property
	def chemical_gradientofsoilconcentrationchange(self):
		return self.gradientofsoilconcentrationchange[self.currentchemical.name]

	_averageverticalvelocity=6.0e-4
	@property
	def averageverticalvelocity(self):
		return self._averageverticalvelocity
	@averageverticalvelocity.setter
	def averageverticalvelocity(self,value):
		self._averageverticalvelocity=value


	@property
	def exp_neg_depth_times_gamma(self):
		cdict={}
		try:
			cdict["chem_2_3_7_8_tcdd"]=exp(-self.chemical_depth_times_gamma)
		except:
			cdict["chem_2_3_7_8_tcdd"]=nan
		
		return cdict

	@property
	def chemical_exp_neg_depth_times_gamma(self):
		return self.exp_neg_depth_times_gamma[self.currentchemical.name]

	@property
	def chemical_exp_neg_depth_times_gamma(self):
		return self.exp_neg_depth_times_gamma[self.currentchemical.name]


	@property
	def kd(self):
		cdict={}
		try:
			cdict["chem_2_3_7_8_tcdd"]=self.currentchemical.k_oc * self.organiccarboncontent
		except:
			cdict["chem_2_3_7_8_tcdd"]=nan
		
		return cdict

	@property
	def chemical_kd(self):
		return self.kd[self.currentchemical.name]

	@property
	def chemical_kd(self):
		return self.kd[self.currentchemical.name]

	@property
	def volume(self):
		return (self.containingvolumeelement.volume)
	
class stem_grasses_herbs_in_grasses_herbs:
	def __init__(self,constants,containingscenario,currentchemical,containingvolumeelement,comp_objects_dict):
		self.containingscenario=containingscenario
		self.currentchemical=currentchemical
		self.constants=constants
		self.containingvolumeelement=containingvolumeelement
		self.comp_objects_dict=comp_objects_dict
	@property
	def acceptableabiotic(self):
		return ("abiotic | soil | surface soil")
	
	@property
	def dryvolumeperarea(self):
		return (self.wetvolumeperarea*(1 - self.watercontent))
	

	@property
	def demethylationrate(self):
		cdict={}
		return cdict

	@property
	def chemical_demethylationrate(self):
		return self.demethylationrate[self.currentchemical.name]

	@property
	def chemical_demethylationrate(self):
		return self.demethylationrate[self.currentchemical.name]


	@property
	def reductionrate(self):
		cdict={}
		return cdict

	@property
	def chemical_reductionrate(self):
		return self.reductionrate[self.currentchemical.name]

	@property
	def chemical_reductionrate(self):
		return self.reductionrate[self.currentchemical.name]

	@property
	def wetvolumeperarea(self):
		return (self.wetmassperarea/self.wetdensity)
	
	_lipidcontent=0.00224
	@property
	def lipidcontent(self):
		return self._lipidcontent
	@lipidcontent.setter
	def lipidcontent(self,value):
		self._lipidcontent=value


	@property
	def halflife(self):
		cdict={}
		try:
			cdict["chem_2_3_7_8_tcdd"]=70.0
		except:
			cdict["chem_2_3_7_8_tcdd"]=nan
		
		return cdict

	@property
	def chemical_halflife(self):
		return self.halflife[self.currentchemical.name]

	@property
	def chemical_halflife(self):
		return self.halflife[self.currentchemical.name]

	@property
	def category(self):
		return ("terrestrial plant | stem | stem - grasses/herbs")
	
	_concentrationoutputfactor=1000.0
	@property
	def concentrationoutputfactor(self):
		return self._concentrationoutputfactor
	@concentrationoutputfactor.setter
	def concentrationoutputfactor(self,value):
		self._concentrationoutputfactor=value

	_wetmassperarea=0.24
	@property
	def wetmassperarea(self):
		return self._wetmassperarea
	@wetmassperarea.setter
	def wetmassperarea(self,value):
		self._wetmassperarea=value


	@property
	def initialconcentration_g_per_kg_usersupplied(self):
		cdict={}
		try:
			cdict["chem_2_3_7_8_tcdd"]=0.0
		except:
			cdict["chem_2_3_7_8_tcdd"]=nan
		
		return cdict

	@property
	def chemical_initialconcentration_g_per_kg_usersupplied(self):
		return self.initialconcentration_g_per_kg_usersupplied[self.currentchemical.name]

	@property
	def chemical_initialconcentration_g_per_kg_usersupplied(self):
		return self.initialconcentration_g_per_kg_usersupplied[self.currentchemical.name]

	@property
	def concentrationoutputunits(self):
		return ("mg/kg wet weight")
	

	@property
	def oxidationrate(self):
		cdict={}
		return cdict

	@property
	def chemical_oxidationrate(self):
		return self.oxidationrate[self.currentchemical.name]

	@property
	def chemical_oxidationrate(self):
		return self.oxidationrate[self.currentchemical.name]

	_wetdensity=830.0
	@property
	def wetdensity(self):
		return self._wetdensity
	@wetdensity.setter
	def wetdensity(self,value):
		self._wetdensity=value

	@property
	def allowexchange_forother(self):
		return (self.allowexchange_steadystate_forother if self.containingscenario.simulatesteadystate == 1 else wt_av_allowexchange)
	
	_phloemdensity=1000.0
	@property
	def phloemdensity(self):
		return self._phloemdensity
	@phloemdensity.setter
	def phloemdensity(self,value):
		self._phloemdensity=value

	@property
	def phloemflowrate(self):
		return (self.fractionphloemratewithtranspirationflowrate*self.flowrateoftranspiredwater)
	

	@property
	def tscf(self):
		cdict={}
		try:
			cdict["chem_2_3_7_8_tcdd"]=0.7 * exp(-((self.currentchemical.log10_k_ow - 3.07) ** 2) / 2.78)
		except:
			cdict["chem_2_3_7_8_tcdd"]=nan
		
		return cdict

	@property
	def chemical_tscf(self):
		return self.tscf[self.currentchemical.name]

	@property
	def chemical_tscf(self):
		return self.tscf[self.currentchemical.name]


	@property
	def generaldegradationrate(self):
		cdict={}
		try:
			cdict["chem_2_3_7_8_tcdd"]=log(2)/ self.chemical_halflife
		except:
			cdict["chem_2_3_7_8_tcdd"]=nan
		
		return cdict

	@property
	def chemical_generaldegradationrate(self):
		return self.generaldegradationrate[self.currentchemical.name]

	@property
	def chemical_generaldegradationrate(self):
		return self.generaldegradationrate[self.currentchemical.name]

	_correctionexponent=0.76
	@property
	def correctionexponent(self):
		return self._correctionexponent
	@correctionexponent.setter
	def correctionexponent(self,value):
		self._correctionexponent=value

	_xylemdensity=900.0
	@property
	def xylemdensity(self):
		return self._xylemdensity
	@xylemdensity.setter
	def xylemdensity(self,value):
		self._xylemdensity=value

	_flowrateoftranspiredwaterperareaofleafsurface=0.0048
	@property
	def flowrateoftranspiredwaterperareaofleafsurface(self):
		return self._flowrateoftranspiredwaterperareaofleafsurface
	@flowrateoftranspiredwaterperareaofleafsurface.setter
	def flowrateoftranspiredwaterperareaofleafsurface(self,value):
		self._flowrateoftranspiredwaterperareaofleafsurface=value

	@property
	def totalmass(self):
		return (self.volume * self.wetdensity)
	

	@property
	def initialconcentration_g_per_kg(self):
		cdict={}
		try:
			cdict["chem_2_3_7_8_tcdd"]=self.containingscenario.fractioninitialconcentrations * self.chemical_initialconcentration_g_per_kg_usersupplied
		except:
			cdict["chem_2_3_7_8_tcdd"]=nan
		
		return cdict

	@property
	def chemical_initialconcentration_g_per_kg(self):
		return self.initialconcentration_g_per_kg[self.currentchemical.name]

	@property
	def chemical_initialconcentration_g_per_kg(self):
		return self.initialconcentration_g_per_kg[self.currentchemical.name]

	_isbiotic=True
	@property
	def isbiotic(self):
		return self._isbiotic
	@isbiotic.setter
	def isbiotic(self,value):
		self._isbiotic=value


	@property
	def methylationrate(self):
		cdict={}
		return cdict

	@property
	def chemical_methylationrate(self):
		return self.methylationrate[self.currentchemical.name]

	@property
	def chemical_methylationrate(self):
		return self.methylationrate[self.currentchemical.name]

	_watercontent=0.8
	@property
	def watercontent(self):
		return self._watercontent
	@watercontent.setter
	def watercontent(self,value):
		self._watercontent=value

	_fractionphloemratewithtranspirationflowrate=0.05
	@property
	def fractionphloemratewithtranspirationflowrate(self):
		return self._fractionphloemratewithtranspirationflowrate
	@fractionphloemratewithtranspirationflowrate.setter
	def fractionphloemratewithtranspirationflowrate(self,value):
		self._fractionphloemratewithtranspirationflowrate=value

	@property
	def density(self):
		return (self.wetdensity)
	
	@property
	def volume(self):
		return (self.wetvolumeperarea*self.containingvolumeelement.area)
	
	@property
	def flowrateoftranspiredwater(self):
		return (self.flowrateoftranspiredwaterperareaofleafsurface*self.associated_leaf_comp.leafareaindex * self.associated_soil_comp.area)
	
class surface_water:
	def __init__(self,constants,containingscenario,currentchemical,containingvolumeelement,comp_objects_dict):
		self.containingscenario=containingscenario
		self.currentchemical=currentchemical
		self.constants=constants
		self.containingvolumeelement=containingvolumeelement
		self.comp_objects_dict=comp_objects_dict
	_watertemperature_k=0.01
	@property
	def watertemperature_k(self):
		return self._watertemperature_k
	@watertemperature_k.setter
	def watertemperature_k(self,value):
		self._watertemperature_k=value


	@property
	def fractionmass_dissolved(self):
		cdict={}
		try:
			cdict["chem_2_3_7_8_tcdd"]=self.volume * (self.volumefraction_liquid) / self.chemical_genericdenominatorforcalculatingfractioninphases
		except:
			cdict["chem_2_3_7_8_tcdd"]=nan
		
		return cdict

	@property
	def chemical_fractionmass_dissolved(self):
		return self.fractionmass_dissolved[self.currentchemical.name]

	@property
	def chemical_fractionmass_dissolved(self):
		return self.fractionmass_dissolved[self.currentchemical.name]


	@property
	def initialconcentration_g_per_l_usersupplied(self):
		cdict={}
		try:
			cdict["chem_2_3_7_8_tcdd"]=0.0
		except:
			cdict["chem_2_3_7_8_tcdd"]=nan
		
		return cdict

	@property
	def chemical_initialconcentration_g_per_l_usersupplied(self):
		return self.initialconcentration_g_per_l_usersupplied[self.currentchemical.name]

	@property
	def chemical_initialconcentration_g_per_l_usersupplied(self):
		return self.initialconcentration_g_per_l_usersupplied[self.currentchemical.name]


	@property
	def d_owformhg_ph8(self):
		cdict={}
		return cdict

	@property
	def chemical_d_owformhg_ph8(self):
		return self.d_owformhg_ph8[self.currentchemical.name]

	@property
	def chemical_d_owformhg_ph8(self):
		return self.d_owformhg_ph8[self.currentchemical.name]

	@property
	def chlorideconcentration_mg_m3(self):
		return (self.chlorideconcentration_mg_l*1000)
	
	@property
	def shearvelocity(self):
		return (sqrt(self.dragcoefficient) * self.containingscenario.horizontalwindspeed)
	
	@property
	def category(self):
		return ("abiotic | surface water | surface water - default")
	
	_fractionsand=0.25
	@property
	def fractionsand(self):
		return self._fractionsand
	@fractionsand.setter
	def fractionsand(self,value):
		self._fractionsand=value

	@property
	def concentrationoutputunits(self):
		return ("mg/l")
	

	@property
	def initialconcentration_g_per_l(self):
		cdict={}
		try:
			cdict["chem_2_3_7_8_tcdd"]=self.containingscenario.fractioninitialconcentrations * self.chemical_initialconcentration_g_per_l_usersupplied
		except:
			cdict["chem_2_3_7_8_tcdd"]=nan
		
		return cdict

	@property
	def chemical_initialconcentration_g_per_l(self):
		return self.initialconcentration_g_per_l[self.currentchemical.name]

	@property
	def chemical_initialconcentration_g_per_l(self):
		return self.initialconcentration_g_per_l[self.currentchemical.name]

	@property
	def shearvelocity_m_per_day(self):
		return (self.shearvelocity*86400)
	
	_flushes_per_year=0.01
	@property
	def flushes_per_year(self):
		return self._flushes_per_year
	@flushes_per_year.setter
	def flushes_per_year(self,value):
		self._flushes_per_year=value

	@property
	def sedimentdepositionrate_kg_m2_day(self):
		return (self.sedimentdepositionvelocity*self.suspendedsedimentconcentration)
	
	_algaedensityinwatercolumn_g_l=0.01
	@property
	def algaedensityinwatercolumn_g_l(self):
		return self._algaedensityinwatercolumn_g_l
	@algaedensityinwatercolumn_g_l.setter
	def algaedensityinwatercolumn_g_l(self,value):
		self._algaedensityinwatercolumn_g_l=value

	@property
	def depth(self):
		return (self.height)
	

	@property
	def generaldegradationrate(self):
		cdict={}
		try:
			cdict["chem_2_3_7_8_tcdd"]=log(2)/ self.chemical_halflife
		except:
			cdict["chem_2_3_7_8_tcdd"]=nan
		
		return cdict

	@property
	def chemical_generaldegradationrate(self):
		return self.generaldegradationrate[self.currentchemical.name]

	@property
	def chemical_generaldegradationrate(self):
		return self.generaldegradationrate[self.currentchemical.name]

	@property
	def algaesedimentationrate_m3_m2_day(self):
		return (self.algaesedimentationrate_g_m2_day/self.algaedensity_g_m3)
	
	_sedimentdepositionvelocity=2.0
	@property
	def sedimentdepositionvelocity(self):
		return self._sedimentdepositionvelocity
	@sedimentdepositionvelocity.setter
	def sedimentdepositionvelocity(self,value):
		self._sedimentdepositionvelocity=value


	@property
	def d_owforhg2_ph4(self):
		cdict={}
		return cdict

	@property
	def chemical_d_owforhg2_ph4(self):
		return self.d_owforhg2_ph4[self.currentchemical.name]

	@property
	def chemical_d_owforhg2_ph4(self):
		return self.d_owforhg2_ph4[self.currentchemical.name]


	@property
	def methylationrate(self):
		cdict={}
		return cdict

	@property
	def chemical_methylationrate(self):
		return self.methylationrate[self.currentchemical.name]

	@property
	def chemical_methylationrate(self):
		return self.methylationrate[self.currentchemical.name]


	@property
	def vapordrydepositionvelocity_m_day(self):
		cdict={}
		return cdict

	@property
	def chemical_vapordrydepositionvelocity_m_day(self):
		return self.vapordrydepositionvelocity_m_day[self.currentchemical.name]

	@property
	def chemical_vapordrydepositionvelocity_m_day(self):
		return self.vapordrydepositionvelocity_m_day[self.currentchemical.name]


	@property
	def d_owformhg_ph4(self):
		cdict={}
		return cdict

	@property
	def chemical_d_owformhg_ph4(self):
		return self.d_owformhg_ph4[self.currentchemical.name]

	@property
	def chemical_d_owformhg_ph4(self):
		return self.d_owformhg_ph4[self.currentchemical.name]

	@property
	def algaesedimentationrate_g_m2_day(self):
		return (self.carbonsedimentationrate_g_m2_day/ (self.algaecarboncontentdrywt *(1-self.algaewatercontent)))
	
	_suspendedsedimentconcentration=0.01
	@property
	def suspendedsedimentconcentration(self):
		return self._suspendedsedimentconcentration
	@suspendedsedimentconcentration.setter
	def suspendedsedimentconcentration(self,value):
		self._suspendedsedimentconcentration=value


	@property
	def demethylationrate(self):
		cdict={}
		return cdict

	@property
	def chemical_demethylationrate(self):
		return self.demethylationrate[self.currentchemical.name]

	@property
	def chemical_demethylationrate(self):
		return self.demethylationrate[self.currentchemical.name]

	@property
	def chlorophyllconcentration_mg_m3(self):
		return (self.chlorophyllconcentration_mg_l*self.constants.l_per_m3)
	

	@property
	def d_owformhg_ph5(self):
		cdict={}
		return cdict

	@property
	def chemical_d_owformhg_ph5(self):
		return self.d_owformhg_ph5[self.currentchemical.name]

	@property
	def chemical_d_owformhg_ph5(self):
		return self.d_owformhg_ph5[self.currentchemical.name]

	_chlorideconcentration_mg_l=0.01
	@property
	def chlorideconcentration_mg_l(self):
		return self._chlorideconcentration_mg_l
	@chlorideconcentration_mg_l.setter
	def chlorideconcentration_mg_l(self,value):
		self._chlorideconcentration_mg_l=value


	@property
	def z_solid(self):
		cdict={}
		try:
			cdict["chem_2_3_7_8_tcdd"]=(self.rho * self.chemical_kd / 1000) * self.currentchemical.z_purewater
		except:
			cdict["chem_2_3_7_8_tcdd"]=nan
		
		return cdict

	@property
	def chemical_z_solid(self):
		return self.z_solid[self.currentchemical.name]

	@property
	def chemical_z_solid(self):
		return self.z_solid[self.currentchemical.name]

	_algaedensity_g_m3=1000000.0
	@property
	def algaedensity_g_m3(self):
		return self._algaedensity_g_m3
	@algaedensity_g_m3.setter
	def algaedensity_g_m3(self,value):
		self._algaedensity_g_m3=value

	_ph=0.01
	@property
	def ph(self):
		return self._ph
	@ph.setter
	def ph(self,value):
		self._ph=value

	_algaeradius=2.5
	@property
	def algaeradius(self):
		return self._algaeradius
	@algaeradius.setter
	def algaeradius(self,value):
		self._algaeradius=value


	@property
	def oxidationrate(self):
		cdict={}
		return cdict

	@property
	def chemical_oxidationrate(self):
		return self.oxidationrate[self.currentchemical.name]

	@property
	def chemical_oxidationrate(self):
		return self.oxidationrate[self.currentchemical.name]

	@property
	def volumefraction_solid(self):
		return (self.suspendedsedimentconcentration / self.rho)
	
	_dimensionlessviscoussublayerthickness=4.0
	@property
	def dimensionlessviscoussublayerthickness(self):
		return self._dimensionlessviscoussublayerthickness
	@dimensionlessviscoussublayerthickness.setter
	def dimensionlessviscoussublayerthickness(self,value):
		self._dimensionlessviscoussublayerthickness=value


	@property
	def ratioofconcinalgaetoconcdissolvedinwater(self):
		cdict={}
		try:
			cdict["chem_2_3_7_8_tcdd"]=1.76
		except:
			cdict["chem_2_3_7_8_tcdd"]=nan
		
		return cdict

	@property
	def chemical_ratioofconcinalgaetoconcdissolvedinwater(self):
		return self.ratioofconcinalgaetoconcdissolvedinwater[self.currentchemical.name]

	@property
	def chemical_ratioofconcinalgaetoconcdissolvedinwater(self):
		return self.ratioofconcinalgaetoconcdissolvedinwater[self.currentchemical.name]


	@property
	def d_owforhg2_ph7(self):
		cdict={}
		return cdict

	@property
	def chemical_d_owforhg2_ph7(self):
		return self.d_owforhg2_ph7[self.currentchemical.name]

	@property
	def chemical_d_owforhg2_ph7(self):
		return self.d_owforhg2_ph7[self.currentchemical.name]


	@property
	def d_owforhg2_ph5(self):
		cdict={}
		return cdict

	@property
	def chemical_d_owforhg2_ph5(self):
		return self.d_owforhg2_ph5[self.currentchemical.name]

	@property
	def chemical_d_owforhg2_ph5(self):
		return self.d_owforhg2_ph5[self.currentchemical.name]

	_boundarylayerthicknessabovesediment=0.02
	@property
	def boundarylayerthicknessabovesediment(self):
		return self._boundarylayerthicknessabovesediment
	@boundarylayerthicknessabovesediment.setter
	def boundarylayerthicknessabovesediment(self,value):
		self._boundarylayerthicknessabovesediment=value

	@property
	def algaedensity_g_um3(self):
		return (self.algaedensity_g_m3 / self.constants.um3_per_m3)
	
	@property
	def watertemperature_c(self):
		return (self.containingvolumeelement.watertemperature_k - 273)
	
	_isflowing=False
	@property
	def isflowing(self):
		return self._isflowing
	@isflowing.setter
	def isflowing(self,value):
		self._isflowing=value


	@property
	def reductionrate(self):
		cdict={}
		return cdict

	@property
	def chemical_reductionrate(self):
		return self.reductionrate[self.currentchemical.name]

	@property
	def chemical_reductionrate(self):
		return self.reductionrate[self.currentchemical.name]

	@property
	def sedimentdepositionrate_m3_m2_day(self):
		return (self.sedimentdepositionrate_kg_m2_day / self.rho)
	
	@property
	def waterdensity(self):
		return (1000)
	

	@property
	def d_effective(self):
		cdict={}
		try:
			cdict["chem_2_3_7_8_tcdd"]=self.currentchemical.d_purewater
		except:
			cdict["chem_2_3_7_8_tcdd"]=nan
		
		return cdict

	@property
	def chemical_d_effective(self):
		return self.d_effective[self.currentchemical.name]

	@property
	def chemical_d_effective(self):
		return self.d_effective[self.currentchemical.name]

	@property
	def meandepth_m(self):
		return ((self.containingvolumeelement.top + self.containingvolumeelement.bottom)/2.0)
	

	@property
	def fractionmass_sorbed(self):
		cdict={}
		try:
			cdict["chem_2_3_7_8_tcdd"]=self.volume * (self.volumefraction_solid) * self.chemical_kd * self.constants.m3_per_l * self.rho / self.chemical_genericdenominatorforcalculatingfractioninphases
		except:
			cdict["chem_2_3_7_8_tcdd"]=nan
		
		return cdict

	@property
	def chemical_fractionmass_sorbed(self):
		return self.fractionmass_sorbed[self.currentchemical.name]

	@property
	def chemical_fractionmass_sorbed(self):
		return self.fractionmass_sorbed[self.currentchemical.name]

	_concentrationoutputfactor=1000.0
	@property
	def concentrationoutputfactor(self):
		return self._concentrationoutputfactor
	@concentrationoutputfactor.setter
	def concentrationoutputfactor(self,value):
		self._concentrationoutputfactor=value


	@property
	def algaeuptakerate(self):
		cdict={}
		return cdict

	@property
	def chemical_algaeuptakerate(self):
		return self.algaeuptakerate[self.currentchemical.name]

	@property
	def chemical_algaeuptakerate(self):
		return self.algaeuptakerate[self.currentchemical.name]


	@property
	def z_total(self):
		cdict={}
		try:
			cdict["chem_2_3_7_8_tcdd"]=self.chemical_z_liquid *self.volumefraction_liquid +self.chemical_z_solid *self.volumefraction_solid + self.chemical_z_algae*self.volumefraction_algae
		except:
			cdict["chem_2_3_7_8_tcdd"]=nan
		
		return cdict

	@property
	def chemical_z_total(self):
		return self.z_total[self.currentchemical.name]

	@property
	def chemical_z_total(self):
		return self.z_total[self.currentchemical.name]

	@property
	def volumefraction_algae(self):
		return ((self.algaedensityinwatercolumn_g_l * self.constants.l_per_m3)/(self.algaedensity_g_m3))
	
	@property
	def area(self):
		return (self.containingvolumeelement.area)
	
	@property
	def height(self):
		return (self.containingvolumeelement.height)
	

	@property
	def d_owformhg_ph7(self):
		cdict={}
		return cdict

	@property
	def chemical_d_owformhg_ph7(self):
		return self.d_owformhg_ph7[self.currentchemical.name]

	@property
	def chemical_d_owformhg_ph7(self):
		return self.d_owformhg_ph7[self.currentchemical.name]


	@property
	def d_owforhg2_ph8(self):
		cdict={}
		return cdict

	@property
	def chemical_d_owforhg2_ph8(self):
		return self.d_owforhg2_ph8[self.currentchemical.name]

	@property
	def chemical_d_owforhg2_ph8(self):
		return self.d_owforhg2_ph8[self.currentchemical.name]

	_currentvelocity=0.01
	@property
	def currentvelocity(self):
		return self._currentvelocity
	@currentvelocity.setter
	def currentvelocity(self,value):
		self._currentvelocity=value

	@property
	def acceptableabiotic(self):
		return ("nan")
	

	@property
	def fractionmass_algae(self):
		cdict={}
		try:
			cdict["chem_2_3_7_8_tcdd"]=self.volume * (self.volumefraction_algae) * self.chemical_ratioofconcinalgaetoconcdissolvedinwater * self.algaedensity_g_m3 * (self.constants.m3_per_l) / self.chemical_genericdenominatorforcalculatingfractioninphases
		except:
			cdict["chem_2_3_7_8_tcdd"]=nan
		
		return cdict

	@property
	def chemical_fractionmass_algae(self):
		return self.fractionmass_algae[self.currentchemical.name]

	@property
	def chemical_fractionmass_algae(self):
		return self.fractionmass_algae[self.currentchemical.name]


	@property
	def d_owforhg2_ph6(self):
		cdict={}
		return cdict

	@property
	def chemical_d_owforhg2_ph6(self):
		return self.d_owforhg2_ph6[self.currentchemical.name]

	@property
	def chemical_d_owforhg2_ph6(self):
		return self.d_owforhg2_ph6[self.currentchemical.name]

	_algaegrowthrate=0.7
	@property
	def algaegrowthrate(self):
		return self._algaegrowthrate
	@algaegrowthrate.setter
	def algaegrowthrate(self,value):
		self._algaegrowthrate=value

	@property
	def suspendedsedimentconcentration_mg_l(self):
		return (self.suspendedsedimentconcentration*1000000/self.constants.l_per_m3)
	

	@property
	def z_liquid(self):
		cdict={}
		try:
			cdict["chem_2_3_7_8_tcdd"]=self.currentchemical.z_purewater
		except:
			cdict["chem_2_3_7_8_tcdd"]=nan
		
		return cdict

	@property
	def chemical_z_liquid(self):
		return self.z_liquid[self.currentchemical.name]

	@property
	def chemical_z_liquid(self):
		return self.z_liquid[self.currentchemical.name]

	_algaewatercontent=0.9
	@property
	def algaewatercontent(self):
		return self._algaewatercontent
	@algaewatercontent.setter
	def algaewatercontent(self,value):
		self._algaewatercontent=value


	@property
	def boundarylayerthicknessbelowwater(self):
		cdict={}
		try:
			cdict["chem_2_3_7_8_tcdd"]=318 * self.chemical_d_effective ** (0.683)
		except:
			cdict["chem_2_3_7_8_tcdd"]=nan
		
		return cdict

	@property
	def chemical_boundarylayerthicknessbelowwater(self):
		return self.boundarylayerthicknessbelowwater[self.currentchemical.name]

	@property
	def chemical_boundarylayerthicknessbelowwater(self):
		return self.boundarylayerthicknessbelowwater[self.currentchemical.name]


	@property
	def halflife(self):
		cdict={}
		try:
			cdict["chem_2_3_7_8_tcdd"]=2.7
		except:
			cdict["chem_2_3_7_8_tcdd"]=nan
		
		return cdict

	@property
	def chemical_halflife(self):
		return self.halflife[self.currentchemical.name]

	@property
	def chemical_halflife(self):
		return self.halflife[self.currentchemical.name]

	_rho=2600.0
	@property
	def rho(self):
		return self._rho
	@rho.setter
	def rho(self,value):
		self._rho=value

	@property
	def totalalgaemass(self):
		return (self.volume*self.volumefraction_algae*self.algaedensity_g_m3 * self.constants.kg_per_g)
	

	@property
	def d_ow(self):
		cdict={}
		try:
			cdict["chem_2_3_7_8_tcdd"]=0.0
		except:
			cdict["chem_2_3_7_8_tcdd"]=nan
		
		return cdict

	@property
	def chemical_d_ow(self):
		return self.d_ow[self.currentchemical.name]

	@property
	def chemical_d_ow(self):
		return self.d_ow[self.currentchemical.name]

	_chlorophyllconcentration_mg_l=0.01
	@property
	def chlorophyllconcentration_mg_l(self):
		return self._chlorophyllconcentration_mg_l
	@chlorophyllconcentration_mg_l.setter
	def chlorophyllconcentration_mg_l(self,value):
		self._chlorophyllconcentration_mg_l=value


	@property
	def z_algae(self):
		cdict={}
		try:
			cdict["chem_2_3_7_8_tcdd"]=(self.chemical_ratioofconcinalgaetoconcdissolvedinwater*self.algaedensity_g_m3/1000.0)*self.currentchemical.z_purewater
		except:
			cdict["chem_2_3_7_8_tcdd"]=nan
		
		return cdict

	@property
	def chemical_z_algae(self):
		return self.z_algae[self.currentchemical.name]

	@property
	def chemical_z_algae(self):
		return self.z_algae[self.currentchemical.name]


	@property
	def genericdenominatorforcalculatingfractioninphases(self):
		cdict={}
		try:
			cdict["chem_2_3_7_8_tcdd"]=self.volume * (self.volumefraction_algae * self.chemical_ratioofconcinalgaetoconcdissolvedinwater * self.algaedensity_g_m3 * (self.constants.m3_per_l)  + self.volumefraction_solid * self.chemical_kd * self.constants.m3_per_l * self.rho + self.volumefraction_liquid )
		except:
			cdict["chem_2_3_7_8_tcdd"]=nan
		
		return cdict

	@property
	def chemical_genericdenominatorforcalculatingfractioninphases(self):
		return self.genericdenominatorforcalculatingfractioninphases[self.currentchemical.name]

	@property
	def chemical_genericdenominatorforcalculatingfractioninphases(self):
		return self.genericdenominatorforcalculatingfractioninphases[self.currentchemical.name]

	_algaecarboncontentdrywt=0.465
	@property
	def algaecarboncontentdrywt(self):
		return self._algaecarboncontentdrywt
	@algaecarboncontentdrywt.setter
	def algaecarboncontentdrywt(self,value):
		self._algaecarboncontentdrywt=value

	_organiccarboncontent=0.01
	@property
	def organiccarboncontent(self):
		return self._organiccarboncontent
	@organiccarboncontent.setter
	def organiccarboncontent(self,value):
		self._organiccarboncontent=value


	@property
	def d_owformhg_ph6(self):
		cdict={}
		return cdict

	@property
	def chemical_d_owformhg_ph6(self):
		return self.d_owformhg_ph6[self.currentchemical.name]

	@property
	def chemical_d_owformhg_ph6(self):
		return self.d_owformhg_ph6[self.currentchemical.name]


	@property
	def waterschmidtnumber(self):
		cdict={}
		try:
			cdict["chem_2_3_7_8_tcdd"]=self.waterviscosity/(self.waterdensity * self.currentchemical.d_purewater_m2_per_s)
		except:
			cdict["chem_2_3_7_8_tcdd"]=nan
		
		return cdict

	@property
	def chemical_waterschmidtnumber(self):
		return self.waterschmidtnumber[self.currentchemical.name]

	@property
	def chemical_waterschmidtnumber(self):
		return self.waterschmidtnumber[self.currentchemical.name]

	@property
	def volumefraction_liquid(self):
		return (1 - self.volumefraction_solid - self.volumefraction_algae)
	
	_isbiotic=False
	@property
	def isbiotic(self):
		return self._isbiotic
	@isbiotic.setter
	def isbiotic(self,value):
		self._isbiotic=value

	@property
	def waterviscosity(self):
		return (10**(-3.30233 + 1301 / (998.333 + 8.1855 * (self.watertemperature_c -20) + 0.00585 * (self.watertemperature_c - 20)**2.0)))
	
	_dragcoefficient=0.0011
	@property
	def dragcoefficient(self):
		return self._dragcoefficient
	@dragcoefficient.setter
	def dragcoefficient(self,value):
		self._dragcoefficient=value


	@property
	def kd(self):
		cdict={}
		try:
			cdict["chem_2_3_7_8_tcdd"]=self.currentchemical.k_oc * self.organiccarboncontent
		except:
			cdict["chem_2_3_7_8_tcdd"]=nan
		
		return cdict

	@property
	def chemical_kd(self):
		return self.kd[self.currentchemical.name]

	@property
	def chemical_kd(self):
		return self.kd[self.currentchemical.name]

	@property
	def volume(self):
		return (self.containingvolumeelement.volume)
	
	@property
	def carbonsedimentationrate_g_m2_day(self):
		return ((10**(1.82 + (0.62 * log(self.chlorophyllconcentration_mg_m3)/log(10)))/1000))
	
class water_column_carnivore:
	def __init__(self,constants,containingscenario,currentchemical,containingvolumeelement,comp_objects_dict):
		self.containingscenario=containingscenario
		self.currentchemical=currentchemical
		self.constants=constants
		self.containingvolumeelement=containingvolumeelement
		self.comp_objects_dict=comp_objects_dict
	_biomassperarea_kg_m2=0.01
	@property
	def biomassperarea_kg_m2(self):
		return self._biomassperarea_kg_m2
	@biomassperarea_kg_m2.setter
	def biomassperarea_kg_m2(self,value):
		self._biomassperarea_kg_m2=value

	@property
	def acceptableabiotic(self):
		return ("abiotic | surface water | surface water - default")
	

	@property
	def gilleliminationrate(self):
		cdict={}
		try:
			cdict["chem_2_3_7_8_tcdd"]=self.chemical_fishchemicaluptakerateviagill / self.currentchemical.k_ow
		except:
			cdict["chem_2_3_7_8_tcdd"]=nan
		
		return cdict

	@property
	def chemical_gilleliminationrate(self):
		return self.gilleliminationrate[self.currentchemical.name]

	@property
	def chemical_gilleliminationrate(self):
		return self.gilleliminationrate[self.currentchemical.name]


	@property
	def demethylationrate(self):
		cdict={}
		return cdict

	@property
	def chemical_demethylationrate(self):
		return self.demethylationrate[self.currentchemical.name]

	@property
	def chemical_demethylationrate(self):
		return self.demethylationrate[self.currentchemical.name]


	@property
	def chemicaltransferefficiencyinfish(self):
		cdict={}
		try:
			cdict["chem_2_3_7_8_tcdd"]=(10 ** (-1.5 + 0.4 * self.currentchemical.log10_k_ow) if ( self.currentchemical.log10_k_ow < 3) else (0.5 if (self.currentchemical.log10_k_ow >= 3) and (self.currentchemical.log10_k_ow < 6) else (10 ** (1.2 - 0.25 * self.currentchemical.log10_k_ow)) ) ) if self.bw > 0.1 else (10 ** (-2.6 + 0.5 * self.currentchemical.log10_k_ow) if (self.currentchemical.log10_k_ow < 5) else (0.8 if (self.currentchemical.log10_k_ow >= 5) and (self.currentchemical.log10_k_ow < 6) else (10 ** (2.9 - 0.5 * self.currentchemical.log10_k_ow) )))
		except:
			cdict["chem_2_3_7_8_tcdd"]=nan
		
		return cdict

	@property
	def chemical_chemicaltransferefficiencyinfish(self):
		return self.chemicaltransferefficiencyinfish[self.currentchemical.name]

	@property
	def chemical_chemicaltransferefficiencyinfish(self):
		return self.chemicaltransferefficiencyinfish[self.currentchemical.name]

	_fractiondietbenthicinvertebrate=0.01
	@property
	def fractiondietbenthicinvertebrate(self):
		return self._fractiondietbenthicinvertebrate
	@fractiondietbenthicinvertebrate.setter
	def fractiondietbenthicinvertebrate(self,value):
		self._fractiondietbenthicinvertebrate=value

	_fractiondietfishbenthicomnivore=0.01
	@property
	def fractiondietfishbenthicomnivore(self):
		return self._fractiondietfishbenthicomnivore
	@fractiondietfishbenthicomnivore.setter
	def fractiondietfishbenthicomnivore(self,value):
		self._fractiondietfishbenthicomnivore=value


	@property
	def howmuchfasterhgeliminationisthanformhg(self):
		cdict={}
		return cdict

	@property
	def chemical_howmuchfasterhgeliminationisthanformhg(self):
		return self.howmuchfasterhgeliminationisthanformhg[self.currentchemical.name]

	@property
	def chemical_howmuchfasterhgeliminationisthanformhg(self):
		return self.howmuchfasterhgeliminationisthanformhg[self.currentchemical.name]

	@property
	def numberoffishpersquaremeter(self):
		return (self.biomassperarea_kg_m2/self.bw)
	

	@property
	def reductionrate(self):
		cdict={}
		return cdict

	@property
	def chemical_reductionrate(self):
		return self.reductionrate[self.currentchemical.name]

	@property
	def chemical_reductionrate(self):
		return self.reductionrate[self.currentchemical.name]


	@property
	def gamma_fish(self):
		cdict={}
		return cdict

	@property
	def chemical_gamma_fish(self):
		return self.gamma_fish[self.currentchemical.name]

	@property
	def chemical_gamma_fish(self):
		return self.gamma_fish[self.currentchemical.name]

	_fractiondietfishbenthiccarnivore=0.01
	@property
	def fractiondietfishbenthiccarnivore(self):
		return self._fractiondietfishbenthiccarnivore
	@fractiondietfishbenthiccarnivore.setter
	def fractiondietfishbenthiccarnivore(self,value):
		self._fractiondietfishbenthiccarnivore=value


	@property
	def fishchemicaluptakerateviagill(self):
		cdict={}
		try:
			cdict["chem_2_3_7_8_tcdd"]=600.0
		except:
			cdict["chem_2_3_7_8_tcdd"]=nan
		
		return cdict

	@property
	def chemical_fishchemicaluptakerateviagill(self):
		return self.fishchemicaluptakerateviagill[self.currentchemical.name]

	@property
	def chemical_fishchemicaluptakerateviagill(self):
		return self.fishchemicaluptakerateviagill[self.currentchemical.name]


	@property
	def halflife(self):
		cdict={}
		try:
			cdict["chem_2_3_7_8_tcdd"]=70.0
		except:
			cdict["chem_2_3_7_8_tcdd"]=nan
		
		return cdict

	@property
	def chemical_halflife(self):
		return self.halflife[self.currentchemical.name]

	@property
	def chemical_halflife(self):
		return self.halflife[self.currentchemical.name]

	@property
	def category(self):
		return ("fish | water column carnivore")
	
	_concentrationoutputfactor=1000.0
	@property
	def concentrationoutputfactor(self):
		return self._concentrationoutputfactor
	@concentrationoutputfactor.setter
	def concentrationoutputfactor(self,value):
		self._concentrationoutputfactor=value

	@property
	def feedingrate(self):
		return (0.022 * self.bw ** (0.85) * exp(0.06 * linkedCompartmentvalue(self.containingvolumeelement,self.comp_objects_dict,"surface_water","watertemperature_c")))
	
	@property
	def concentrationoutputunits(self):
		return ("mg/kg wet weight")
	

	@property
	def initialconcentration_g_per_kg_usersupplied(self):
		cdict={}
		try:
			cdict["chem_2_3_7_8_tcdd"]=0.0
		except:
			cdict["chem_2_3_7_8_tcdd"]=nan
		
		return cdict

	@property
	def chemical_initialconcentration_g_per_kg_usersupplied(self):
		return self.initialconcentration_g_per_kg_usersupplied[self.currentchemical.name]

	@property
	def chemical_initialconcentration_g_per_kg_usersupplied(self):
		return self.initialconcentration_g_per_kg_usersupplied[self.currentchemical.name]


	@property
	def eliminationrateconstant(self):
		cdict={}
		return cdict

	@property
	def chemical_eliminationrateconstant(self):
		return self.eliminationrateconstant[self.currentchemical.name]

	@property
	def chemical_eliminationrateconstant(self):
		return self.eliminationrateconstant[self.currentchemical.name]

	_fractiondietfishomnivore=0.01
	@property
	def fractiondietfishomnivore(self):
		return self._fractiondietfishomnivore
	@fractiondietfishomnivore.setter
	def fractiondietfishomnivore(self,value):
		self._fractiondietfishomnivore=value


	@property
	def oxidationrate(self):
		cdict={}
		return cdict

	@property
	def chemical_oxidationrate(self):
		return self.oxidationrate[self.currentchemical.name]

	@property
	def chemical_oxidationrate(self):
		return self.oxidationrate[self.currentchemical.name]


	@property
	def absorptionrateconstant(self):
		cdict={}
		return cdict

	@property
	def chemical_absorptionrateconstant(self):
		return self.absorptionrateconstant[self.currentchemical.name]

	@property
	def chemical_absorptionrateconstant(self):
		return self.absorptionrateconstant[self.currentchemical.name]


	@property
	def generaldegradationrate(self):
		cdict={}
		try:
			cdict["chem_2_3_7_8_tcdd"]=log(2)/ self.chemical_halflife
		except:
			cdict["chem_2_3_7_8_tcdd"]=nan
		
		return cdict

	@property
	def chemical_generaldegradationrate(self):
		return self.generaldegradationrate[self.currentchemical.name]

	@property
	def chemical_generaldegradationrate(self):
		return self.generaldegradationrate[self.currentchemical.name]

	_fishlipidfraction=0.057
	@property
	def fishlipidfraction(self):
		return self._fishlipidfraction
	@fishlipidfraction.setter
	def fishlipidfraction(self,value):
		self._fishlipidfraction=value

	_fractiondietzooplankton=0.01
	@property
	def fractiondietzooplankton(self):
		return self._fractiondietzooplankton
	@fractiondietzooplankton.setter
	def fractiondietzooplankton(self,value):
		self._fractiondietzooplankton=value


	@property
	def assimilationefficiencyfromfood(self):
		cdict={}
		try:
			cdict["chem_2_3_7_8_tcdd"]=0.41
		except:
			cdict["chem_2_3_7_8_tcdd"]=nan
		
		return cdict

	@property
	def chemical_assimilationefficiencyfromfood(self):
		return self.assimilationefficiencyfromfood[self.currentchemical.name]

	@property
	def chemical_assimilationefficiencyfromfood(self):
		return self.assimilationefficiencyfromfood[self.currentchemical.name]

	@property
	def populationsize(self):
		return (self.numberoffishpersquaremeter * self.containingvolumeelement.area)
	
	@property
	def totalmass(self):
		return (self.populationsize  * self.bw)
	

	@property
	def initialconcentration_g_per_kg(self):
		cdict={}
		try:
			cdict["chem_2_3_7_8_tcdd"]=self.containingscenario.fractioninitialconcentrations * self.chemical_initialconcentration_g_per_kg_usersupplied
		except:
			cdict["chem_2_3_7_8_tcdd"]=nan
		
		return cdict

	@property
	def chemical_initialconcentration_g_per_kg(self):
		return self.initialconcentration_g_per_kg[self.currentchemical.name]

	@property
	def chemical_initialconcentration_g_per_kg(self):
		return self.initialconcentration_g_per_kg[self.currentchemical.name]

	_fractiondietfishherbivore=0.01
	@property
	def fractiondietfishherbivore(self):
		return self._fractiondietfishherbivore
	@fractiondietfishherbivore.setter
	def fractiondietfishherbivore(self,value):
		self._fractiondietfishherbivore=value

	_isbiotic=True
	@property
	def isbiotic(self):
		return self._isbiotic
	@isbiotic.setter
	def isbiotic(self,value):
		self._isbiotic=value

	_fractiondietalgae=0.01
	@property
	def fractiondietalgae(self):
		return self._fractiondietalgae
	@fractiondietalgae.setter
	def fractiondietalgae(self,value):
		self._fractiondietalgae=value

	@property
	def image(self):
		return ("c:\models\trim\data\images\largemouth.gif")
	

	@property
	def methylationrate(self):
		cdict={}
		return cdict

	@property
	def chemical_methylationrate(self):
		return self.methylationrate[self.currentchemical.name]

	@property
	def chemical_methylationrate(self):
		return self.methylationrate[self.currentchemical.name]

	@property
	def foodingestionrate(self):
		return (self.feedingrate/self.bw)
	
	_bw=2.0
	@property
	def bw(self):
		return self._bw
	@bw.setter
	def bw(self,value):
		self._bw=value

class water_column_herbivore:
	def __init__(self,constants,containingscenario,currentchemical,containingvolumeelement,comp_objects_dict):
		self.containingscenario=containingscenario
		self.currentchemical=currentchemical
		self.constants=constants
		self.containingvolumeelement=containingvolumeelement
		self.comp_objects_dict=comp_objects_dict
	_biomassperarea_kg_m2=0.01
	@property
	def biomassperarea_kg_m2(self):
		return self._biomassperarea_kg_m2
	@biomassperarea_kg_m2.setter
	def biomassperarea_kg_m2(self,value):
		self._biomassperarea_kg_m2=value

	@property
	def acceptableabiotic(self):
		return ("abiotic | surface water | surface water - default")
	

	@property
	def gilleliminationrate(self):
		cdict={}
		try:
			cdict["chem_2_3_7_8_tcdd"]=self.chemical_fishchemicaluptakerateviagill / self.currentchemical.k_ow
		except:
			cdict["chem_2_3_7_8_tcdd"]=nan
		
		return cdict

	@property
	def chemical_gilleliminationrate(self):
		return self.gilleliminationrate[self.currentchemical.name]

	@property
	def chemical_gilleliminationrate(self):
		return self.gilleliminationrate[self.currentchemical.name]


	@property
	def demethylationrate(self):
		cdict={}
		return cdict

	@property
	def chemical_demethylationrate(self):
		return self.demethylationrate[self.currentchemical.name]

	@property
	def chemical_demethylationrate(self):
		return self.demethylationrate[self.currentchemical.name]


	@property
	def chemicaltransferefficiencyinfish(self):
		cdict={}
		try:
			cdict["chem_2_3_7_8_tcdd"]=(10 ** (-1.5 + 0.4 * self.currentchemical.log10_k_ow) if ( self.currentchemical.log10_k_ow < 3) else (0.5 if (self.currentchemical.log10_k_ow >= 3) and (self.currentchemical.log10_k_ow < 6) else (10 ** (1.2 - 0.25 * self.currentchemical.log10_k_ow)) ) ) if self.bw > 0.1 else (10 ** (-2.6 + 0.5 * self.currentchemical.log10_k_ow) if (self.currentchemical.log10_k_ow < 5) else (0.8 if (self.currentchemical.log10_k_ow >= 5) and (self.currentchemical.log10_k_ow < 6) else (10 ** (2.9 - 0.5 * self.currentchemical.log10_k_ow) )))
		except:
			cdict["chem_2_3_7_8_tcdd"]=nan
		
		return cdict

	@property
	def chemical_chemicaltransferefficiencyinfish(self):
		return self.chemicaltransferefficiencyinfish[self.currentchemical.name]

	@property
	def chemical_chemicaltransferefficiencyinfish(self):
		return self.chemicaltransferefficiencyinfish[self.currentchemical.name]

	_fractiondietbenthicinvertebrate=0.01
	@property
	def fractiondietbenthicinvertebrate(self):
		return self._fractiondietbenthicinvertebrate
	@fractiondietbenthicinvertebrate.setter
	def fractiondietbenthicinvertebrate(self,value):
		self._fractiondietbenthicinvertebrate=value


	@property
	def howmuchfasterhgeliminationisthanformhg(self):
		cdict={}
		return cdict

	@property
	def chemical_howmuchfasterhgeliminationisthanformhg(self):
		return self.howmuchfasterhgeliminationisthanformhg[self.currentchemical.name]

	@property
	def chemical_howmuchfasterhgeliminationisthanformhg(self):
		return self.howmuchfasterhgeliminationisthanformhg[self.currentchemical.name]

	@property
	def numberoffishpersquaremeter(self):
		return (self.biomassperarea_kg_m2/self.bw)
	

	@property
	def reductionrate(self):
		cdict={}
		return cdict

	@property
	def chemical_reductionrate(self):
		return self.reductionrate[self.currentchemical.name]

	@property
	def chemical_reductionrate(self):
		return self.reductionrate[self.currentchemical.name]


	@property
	def gamma_fish(self):
		cdict={}
		return cdict

	@property
	def chemical_gamma_fish(self):
		return self.gamma_fish[self.currentchemical.name]

	@property
	def chemical_gamma_fish(self):
		return self.gamma_fish[self.currentchemical.name]


	@property
	def fishchemicaluptakerateviagill(self):
		cdict={}
		try:
			cdict["chem_2_3_7_8_tcdd"]=600.0
		except:
			cdict["chem_2_3_7_8_tcdd"]=nan
		
		return cdict

	@property
	def chemical_fishchemicaluptakerateviagill(self):
		return self.fishchemicaluptakerateviagill[self.currentchemical.name]

	@property
	def chemical_fishchemicaluptakerateviagill(self):
		return self.fishchemicaluptakerateviagill[self.currentchemical.name]

	_fractiondietmacrophyte=0.01
	@property
	def fractiondietmacrophyte(self):
		return self._fractiondietmacrophyte
	@fractiondietmacrophyte.setter
	def fractiondietmacrophyte(self,value):
		self._fractiondietmacrophyte=value


	@property
	def halflife(self):
		cdict={}
		try:
			cdict["chem_2_3_7_8_tcdd"]=70.0
		except:
			cdict["chem_2_3_7_8_tcdd"]=nan
		
		return cdict

	@property
	def chemical_halflife(self):
		return self.halflife[self.currentchemical.name]

	@property
	def chemical_halflife(self):
		return self.halflife[self.currentchemical.name]

	@property
	def category(self):
		return ("fish | water column herbivore")
	
	_concentrationoutputfactor=1000.0
	@property
	def concentrationoutputfactor(self):
		return self._concentrationoutputfactor
	@concentrationoutputfactor.setter
	def concentrationoutputfactor(self,value):
		self._concentrationoutputfactor=value

	@property
	def feedingrate(self):
		return (0.022 * self.bw ** (0.85) * exp(0.06 * linkedCompartmentvalue(self.containingvolumeelement,self.comp_objects_dict,"surface_water","watertemperature_c")))
	
	@property
	def concentrationoutputunits(self):
		return ("mg/kg wet weight")
	

	@property
	def initialconcentration_g_per_kg_usersupplied(self):
		cdict={}
		try:
			cdict["chem_2_3_7_8_tcdd"]=0.0
		except:
			cdict["chem_2_3_7_8_tcdd"]=nan
		
		return cdict

	@property
	def chemical_initialconcentration_g_per_kg_usersupplied(self):
		return self.initialconcentration_g_per_kg_usersupplied[self.currentchemical.name]

	@property
	def chemical_initialconcentration_g_per_kg_usersupplied(self):
		return self.initialconcentration_g_per_kg_usersupplied[self.currentchemical.name]


	@property
	def assimilationefficiencyfromplankton(self):
		cdict={}
		try:
			cdict["chem_2_3_7_8_tcdd"]=0.41
		except:
			cdict["chem_2_3_7_8_tcdd"]=nan
		
		return cdict

	@property
	def chemical_assimilationefficiencyfromplankton(self):
		return self.assimilationefficiencyfromplankton[self.currentchemical.name]

	@property
	def chemical_assimilationefficiencyfromplankton(self):
		return self.assimilationefficiencyfromplankton[self.currentchemical.name]


	@property
	def eliminationrateconstant(self):
		cdict={}
		return cdict

	@property
	def chemical_eliminationrateconstant(self):
		return self.eliminationrateconstant[self.currentchemical.name]

	@property
	def chemical_eliminationrateconstant(self):
		return self.eliminationrateconstant[self.currentchemical.name]


	@property
	def oxidationrate(self):
		cdict={}
		return cdict

	@property
	def chemical_oxidationrate(self):
		return self.oxidationrate[self.currentchemical.name]

	@property
	def chemical_oxidationrate(self):
		return self.oxidationrate[self.currentchemical.name]


	@property
	def absorptionrateconstant(self):
		cdict={}
		return cdict

	@property
	def chemical_absorptionrateconstant(self):
		return self.absorptionrateconstant[self.currentchemical.name]

	@property
	def chemical_absorptionrateconstant(self):
		return self.absorptionrateconstant[self.currentchemical.name]


	@property
	def generaldegradationrate(self):
		cdict={}
		try:
			cdict["chem_2_3_7_8_tcdd"]=log(2)/ self.chemical_halflife
		except:
			cdict["chem_2_3_7_8_tcdd"]=nan
		
		return cdict

	@property
	def chemical_generaldegradationrate(self):
		return self.generaldegradationrate[self.currentchemical.name]

	@property
	def chemical_generaldegradationrate(self):
		return self.generaldegradationrate[self.currentchemical.name]

	_fishlipidfraction=0.034
	@property
	def fishlipidfraction(self):
		return self._fishlipidfraction
	@fishlipidfraction.setter
	def fishlipidfraction(self,value):
		self._fishlipidfraction=value


	@property
	def assimilationefficiencyfromplants(self):
		cdict={}
		try:
			cdict["chem_2_3_7_8_tcdd"]=0.41
		except:
			cdict["chem_2_3_7_8_tcdd"]=nan
		
		return cdict

	@property
	def chemical_assimilationefficiencyfromplants(self):
		return self.assimilationefficiencyfromplants[self.currentchemical.name]

	@property
	def chemical_assimilationefficiencyfromplants(self):
		return self.assimilationefficiencyfromplants[self.currentchemical.name]


	@property
	def assimilationefficiencyfromfood(self):
		cdict={}
		try:
			cdict["chem_2_3_7_8_tcdd"]=0.41
		except:
			cdict["chem_2_3_7_8_tcdd"]=nan
		
		return cdict

	@property
	def chemical_assimilationefficiencyfromfood(self):
		return self.assimilationefficiencyfromfood[self.currentchemical.name]

	@property
	def chemical_assimilationefficiencyfromfood(self):
		return self.assimilationefficiencyfromfood[self.currentchemical.name]

	_fractiondietzooplankton=0.01
	@property
	def fractiondietzooplankton(self):
		return self._fractiondietzooplankton
	@fractiondietzooplankton.setter
	def fractiondietzooplankton(self,value):
		self._fractiondietzooplankton=value

	@property
	def populationsize(self):
		return (self.numberoffishpersquaremeter * self.containingvolumeelement.area)
	
	@property
	def totalmass(self):
		return (self.populationsize  * self.bw)
	

	@property
	def initialconcentration_g_per_kg(self):
		cdict={}
		try:
			cdict["chem_2_3_7_8_tcdd"]=self.containingscenario.fractioninitialconcentrations * self.chemical_initialconcentration_g_per_kg_usersupplied
		except:
			cdict["chem_2_3_7_8_tcdd"]=nan
		
		return cdict

	@property
	def chemical_initialconcentration_g_per_kg(self):
		return self.initialconcentration_g_per_kg[self.currentchemical.name]

	@property
	def chemical_initialconcentration_g_per_kg(self):
		return self.initialconcentration_g_per_kg[self.currentchemical.name]

	_isbiotic=True
	@property
	def isbiotic(self):
		return self._isbiotic
	@isbiotic.setter
	def isbiotic(self,value):
		self._isbiotic=value

	_fractiondietalgae=0.01
	@property
	def fractiondietalgae(self):
		return self._fractiondietalgae
	@fractiondietalgae.setter
	def fractiondietalgae(self,value):
		self._fractiondietalgae=value

	@property
	def image(self):
		return ("c:\models\trim\data\images\bluegill.gif")
	

	@property
	def methylationrate(self):
		cdict={}
		return cdict

	@property
	def chemical_methylationrate(self):
		return self.methylationrate[self.currentchemical.name]

	@property
	def chemical_methylationrate(self):
		return self.methylationrate[self.currentchemical.name]

	@property
	def foodingestionrate(self):
		return (self.feedingrate/self.bw)
	
	_bw=0.025
	@property
	def bw(self):
		return self._bw
	@bw.setter
	def bw(self,value):
		self._bw=value

class water_column_omnivore:
	def __init__(self,constants,containingscenario,currentchemical,containingvolumeelement,comp_objects_dict):
		self.containingscenario=containingscenario
		self.currentchemical=currentchemical
		self.constants=constants
		self.containingvolumeelement=containingvolumeelement
		self.comp_objects_dict=comp_objects_dict
	_biomassperarea_kg_m2=0.01
	@property
	def biomassperarea_kg_m2(self):
		return self._biomassperarea_kg_m2
	@biomassperarea_kg_m2.setter
	def biomassperarea_kg_m2(self,value):
		self._biomassperarea_kg_m2=value

	@property
	def acceptableabiotic(self):
		return ("abiotic | surface water | surface water - default")
	

	@property
	def gilleliminationrate(self):
		cdict={}
		try:
			cdict["chem_2_3_7_8_tcdd"]=self.chemical_fishchemicaluptakerateviagill / self.currentchemical.k_ow
		except:
			cdict["chem_2_3_7_8_tcdd"]=nan
		
		return cdict

	@property
	def chemical_gilleliminationrate(self):
		return self.gilleliminationrate[self.currentchemical.name]

	@property
	def chemical_gilleliminationrate(self):
		return self.gilleliminationrate[self.currentchemical.name]


	@property
	def demethylationrate(self):
		cdict={}
		return cdict

	@property
	def chemical_demethylationrate(self):
		return self.demethylationrate[self.currentchemical.name]

	@property
	def chemical_demethylationrate(self):
		return self.demethylationrate[self.currentchemical.name]


	@property
	def chemicaltransferefficiencyinfish(self):
		cdict={}
		try:
			cdict["chem_2_3_7_8_tcdd"]=(10 ** (-1.5 + 0.4 * self.currentchemical.log10_k_ow) if ( self.currentchemical.log10_k_ow < 3) else (0.5 if (self.currentchemical.log10_k_ow >= 3) and (self.currentchemical.log10_k_ow < 6) else (10 ** (1.2 - 0.25 * self.currentchemical.log10_k_ow)) ) ) if self.bw > 0.1 else (10 ** (-2.6 + 0.5 * self.currentchemical.log10_k_ow) if (self.currentchemical.log10_k_ow < 5) else (0.8 if (self.currentchemical.log10_k_ow >= 5) and (self.currentchemical.log10_k_ow < 6) else (10 ** (2.9 - 0.5 * self.currentchemical.log10_k_ow) )))
		except:
			cdict["chem_2_3_7_8_tcdd"]=nan
		
		return cdict

	@property
	def chemical_chemicaltransferefficiencyinfish(self):
		return self.chemicaltransferefficiencyinfish[self.currentchemical.name]

	@property
	def chemical_chemicaltransferefficiencyinfish(self):
		return self.chemicaltransferefficiencyinfish[self.currentchemical.name]

	_fractiondietbenthicinvertebrate=0.01
	@property
	def fractiondietbenthicinvertebrate(self):
		return self._fractiondietbenthicinvertebrate
	@fractiondietbenthicinvertebrate.setter
	def fractiondietbenthicinvertebrate(self,value):
		self._fractiondietbenthicinvertebrate=value

	_fractiondietfishbenthicomnivore=0.01
	@property
	def fractiondietfishbenthicomnivore(self):
		return self._fractiondietfishbenthicomnivore
	@fractiondietfishbenthicomnivore.setter
	def fractiondietfishbenthicomnivore(self,value):
		self._fractiondietfishbenthicomnivore=value


	@property
	def howmuchfasterhgeliminationisthanformhg(self):
		cdict={}
		return cdict

	@property
	def chemical_howmuchfasterhgeliminationisthanformhg(self):
		return self.howmuchfasterhgeliminationisthanformhg[self.currentchemical.name]

	@property
	def chemical_howmuchfasterhgeliminationisthanformhg(self):
		return self.howmuchfasterhgeliminationisthanformhg[self.currentchemical.name]

	@property
	def numberoffishpersquaremeter(self):
		return (self.biomassperarea_kg_m2/self.bw)
	

	@property
	def reductionrate(self):
		cdict={}
		return cdict

	@property
	def chemical_reductionrate(self):
		return self.reductionrate[self.currentchemical.name]

	@property
	def chemical_reductionrate(self):
		return self.reductionrate[self.currentchemical.name]


	@property
	def gamma_fish(self):
		cdict={}
		return cdict

	@property
	def chemical_gamma_fish(self):
		return self.gamma_fish[self.currentchemical.name]

	@property
	def chemical_gamma_fish(self):
		return self.gamma_fish[self.currentchemical.name]

	_fractiondietfishbenthiccarnivore=0.01
	@property
	def fractiondietfishbenthiccarnivore(self):
		return self._fractiondietfishbenthiccarnivore
	@fractiondietfishbenthiccarnivore.setter
	def fractiondietfishbenthiccarnivore(self,value):
		self._fractiondietfishbenthiccarnivore=value


	@property
	def fishchemicaluptakerateviagill(self):
		cdict={}
		try:
			cdict["chem_2_3_7_8_tcdd"]=600.0
		except:
			cdict["chem_2_3_7_8_tcdd"]=nan
		
		return cdict

	@property
	def chemical_fishchemicaluptakerateviagill(self):
		return self.fishchemicaluptakerateviagill[self.currentchemical.name]

	@property
	def chemical_fishchemicaluptakerateviagill(self):
		return self.fishchemicaluptakerateviagill[self.currentchemical.name]

	_fractiondietmacrophyte=0.01
	@property
	def fractiondietmacrophyte(self):
		return self._fractiondietmacrophyte
	@fractiondietmacrophyte.setter
	def fractiondietmacrophyte(self,value):
		self._fractiondietmacrophyte=value


	@property
	def halflife(self):
		cdict={}
		try:
			cdict["chem_2_3_7_8_tcdd"]=70.0
		except:
			cdict["chem_2_3_7_8_tcdd"]=nan
		
		return cdict

	@property
	def chemical_halflife(self):
		return self.halflife[self.currentchemical.name]

	@property
	def chemical_halflife(self):
		return self.halflife[self.currentchemical.name]

	@property
	def category(self):
		return ("fish | water column omnivore")
	
	_concentrationoutputfactor=1000.0
	@property
	def concentrationoutputfactor(self):
		return self._concentrationoutputfactor
	@concentrationoutputfactor.setter
	def concentrationoutputfactor(self,value):
		self._concentrationoutputfactor=value

	@property
	def feedingrate(self):
		return (0.022 * self.bw ** (0.85) * exp(0.06 * linkedCompartmentvalue(self.containingvolumeelement,self.comp_objects_dict,"surface_water","watertemperature_c")))
	
	@property
	def concentrationoutputunits(self):
		return ("mg/kg wet weight")
	

	@property
	def initialconcentration_g_per_kg_usersupplied(self):
		cdict={}
		try:
			cdict["chem_2_3_7_8_tcdd"]=0.0
		except:
			cdict["chem_2_3_7_8_tcdd"]=nan
		
		return cdict

	@property
	def chemical_initialconcentration_g_per_kg_usersupplied(self):
		return self.initialconcentration_g_per_kg_usersupplied[self.currentchemical.name]

	@property
	def chemical_initialconcentration_g_per_kg_usersupplied(self):
		return self.initialconcentration_g_per_kg_usersupplied[self.currentchemical.name]


	@property
	def eliminationrateconstant(self):
		cdict={}
		return cdict

	@property
	def chemical_eliminationrateconstant(self):
		return self.eliminationrateconstant[self.currentchemical.name]

	@property
	def chemical_eliminationrateconstant(self):
		return self.eliminationrateconstant[self.currentchemical.name]

	_fractiondietfishomnivore=0.01
	@property
	def fractiondietfishomnivore(self):
		return self._fractiondietfishomnivore
	@fractiondietfishomnivore.setter
	def fractiondietfishomnivore(self,value):
		self._fractiondietfishomnivore=value

	_fractiondietfishcarnivore=0.01
	@property
	def fractiondietfishcarnivore(self):
		return self._fractiondietfishcarnivore
	@fractiondietfishcarnivore.setter
	def fractiondietfishcarnivore(self,value):
		self._fractiondietfishcarnivore=value


	@property
	def oxidationrate(self):
		cdict={}
		return cdict

	@property
	def chemical_oxidationrate(self):
		return self.oxidationrate[self.currentchemical.name]

	@property
	def chemical_oxidationrate(self):
		return self.oxidationrate[self.currentchemical.name]


	@property
	def absorptionrateconstant(self):
		cdict={}
		return cdict

	@property
	def chemical_absorptionrateconstant(self):
		return self.absorptionrateconstant[self.currentchemical.name]

	@property
	def chemical_absorptionrateconstant(self):
		return self.absorptionrateconstant[self.currentchemical.name]


	@property
	def generaldegradationrate(self):
		cdict={}
		try:
			cdict["chem_2_3_7_8_tcdd"]=log(2)/ self.chemical_halflife
		except:
			cdict["chem_2_3_7_8_tcdd"]=nan
		
		return cdict

	@property
	def chemical_generaldegradationrate(self):
		return self.generaldegradationrate[self.currentchemical.name]

	@property
	def chemical_generaldegradationrate(self):
		return self.generaldegradationrate[self.currentchemical.name]

	_fishlipidfraction=0.07
	@property
	def fishlipidfraction(self):
		return self._fishlipidfraction
	@fishlipidfraction.setter
	def fishlipidfraction(self,value):
		self._fishlipidfraction=value


	@property
	def assimilationefficiencyfromplants(self):
		cdict={}
		try:
			cdict["chem_2_3_7_8_tcdd"]=0.41
		except:
			cdict["chem_2_3_7_8_tcdd"]=nan
		
		return cdict

	@property
	def chemical_assimilationefficiencyfromplants(self):
		return self.assimilationefficiencyfromplants[self.currentchemical.name]

	@property
	def chemical_assimilationefficiencyfromplants(self):
		return self.assimilationefficiencyfromplants[self.currentchemical.name]


	@property
	def assimilationefficiencyfromfood(self):
		cdict={}
		try:
			cdict["chem_2_3_7_8_tcdd"]=0.41
		except:
			cdict["chem_2_3_7_8_tcdd"]=nan
		
		return cdict

	@property
	def chemical_assimilationefficiencyfromfood(self):
		return self.assimilationefficiencyfromfood[self.currentchemical.name]

	@property
	def chemical_assimilationefficiencyfromfood(self):
		return self.assimilationefficiencyfromfood[self.currentchemical.name]

	_fractiondietzooplankton=0.01
	@property
	def fractiondietzooplankton(self):
		return self._fractiondietzooplankton
	@fractiondietzooplankton.setter
	def fractiondietzooplankton(self,value):
		self._fractiondietzooplankton=value

	@property
	def populationsize(self):
		return (self.numberoffishpersquaremeter * self.containingvolumeelement.area)
	
	@property
	def totalmass(self):
		return (self.populationsize  * self.bw)
	

	@property
	def initialconcentration_g_per_kg(self):
		cdict={}
		try:
			cdict["chem_2_3_7_8_tcdd"]=self.containingscenario.fractioninitialconcentrations * self.chemical_initialconcentration_g_per_kg_usersupplied
		except:
			cdict["chem_2_3_7_8_tcdd"]=nan
		
		return cdict

	@property
	def chemical_initialconcentration_g_per_kg(self):
		return self.initialconcentration_g_per_kg[self.currentchemical.name]

	@property
	def chemical_initialconcentration_g_per_kg(self):
		return self.initialconcentration_g_per_kg[self.currentchemical.name]

	_fractiondietfishherbivore=0.01
	@property
	def fractiondietfishherbivore(self):
		return self._fractiondietfishherbivore
	@fractiondietfishherbivore.setter
	def fractiondietfishherbivore(self,value):
		self._fractiondietfishherbivore=value

	_isbiotic=True
	@property
	def isbiotic(self):
		return self._isbiotic
	@isbiotic.setter
	def isbiotic(self,value):
		self._isbiotic=value

	_fractiondietalgae=0.01
	@property
	def fractiondietalgae(self):
		return self._fractiondietalgae
	@fractiondietalgae.setter
	def fractiondietalgae(self,value):
		self._fractiondietalgae=value

	@property
	def image(self):
		return ("c:\models\trim\data\images\catfish.gif")
	

	@property
	def methylationrate(self):
		cdict={}
		return cdict

	@property
	def chemical_methylationrate(self):
		return self.methylationrate[self.currentchemical.name]

	@property
	def chemical_methylationrate(self):
		return self.methylationrate[self.currentchemical.name]

	@property
	def foodingestionrate(self):
		return (self.feedingrate/self.bw)
	
	_bw=0.25
	@property
	def bw(self):
		return self._bw
	@bw.setter
	def bw(self,value):
		self._bw=value

class zooplankton:
	def __init__(self,constants,containingscenario,currentchemical,containingvolumeelement,comp_objects_dict):
		self.containingscenario=containingscenario
		self.currentchemical=currentchemical
		self.constants=constants
		self.containingvolumeelement=containingvolumeelement
		self.comp_objects_dict=comp_objects_dict
	_biomassperarea_kg_m2=0.01
	@property
	def biomassperarea_kg_m2(self):
		return self._biomassperarea_kg_m2
	@biomassperarea_kg_m2.setter
	def biomassperarea_kg_m2(self,value):
		self._biomassperarea_kg_m2=value

	@property
	def acceptableabiotic(self):
		return ("abiotic | surface water | surface water - default")
	
	_zooplanktonlipidfraction=0.012
	@property
	def zooplanktonlipidfraction(self):
		return self._zooplanktonlipidfraction
	@zooplanktonlipidfraction.setter
	def zooplanktonlipidfraction(self,value):
		self._zooplanktonlipidfraction=value


	@property
	def demethylationrate(self):
		cdict={}
		return cdict

	@property
	def chemical_demethylationrate(self):
		return self.demethylationrate[self.currentchemical.name]

	@property
	def chemical_demethylationrate(self):
		return self.demethylationrate[self.currentchemical.name]

	_fractiondietbenthicinvertebrate=0.01
	@property
	def fractiondietbenthicinvertebrate(self):
		return self._fractiondietbenthicinvertebrate
	@fractiondietbenthicinvertebrate.setter
	def fractiondietbenthicinvertebrate(self,value):
		self._fractiondietbenthicinvertebrate=value


	@property
	def howmuchfasterhgeliminationisthanformhg(self):
		cdict={}
		return cdict

	@property
	def chemical_howmuchfasterhgeliminationisthanformhg(self):
		return self.howmuchfasterhgeliminationisthanformhg[self.currentchemical.name]

	@property
	def chemical_howmuchfasterhgeliminationisthanformhg(self):
		return self.howmuchfasterhgeliminationisthanformhg[self.currentchemical.name]


	@property
	def assimilationefficiencyfromalgae(self):
		cdict={}
		try:
			cdict["chem_2_3_7_8_tcdd"]=0.41
		except:
			cdict["chem_2_3_7_8_tcdd"]=nan
		
		return cdict

	@property
	def chemical_assimilationefficiencyfromalgae(self):
		return self.assimilationefficiencyfromalgae[self.currentchemical.name]

	@property
	def chemical_assimilationefficiencyfromalgae(self):
		return self.assimilationefficiencyfromalgae[self.currentchemical.name]


	@property
	def reductionrate(self):
		cdict={}
		return cdict

	@property
	def chemical_reductionrate(self):
		return self.reductionrate[self.currentchemical.name]

	@property
	def chemical_reductionrate(self):
		return self.reductionrate[self.currentchemical.name]

	_fractiondietmacrophyte=0.01
	@property
	def fractiondietmacrophyte(self):
		return self._fractiondietmacrophyte
	@fractiondietmacrophyte.setter
	def fractiondietmacrophyte(self,value):
		self._fractiondietmacrophyte=value


	@property
	def halflife(self):
		cdict={}
		try:
			cdict["chem_2_3_7_8_tcdd"]=6931472.0
		except:
			cdict["chem_2_3_7_8_tcdd"]=nan
		
		return cdict

	@property
	def chemical_halflife(self):
		return self.halflife[self.currentchemical.name]

	@property
	def chemical_halflife(self):
		return self.halflife[self.currentchemical.name]

	@property
	def category(self):
		return ("invertebrate | zooplankton")
	
	_concentrationoutputfactor=1000.0
	@property
	def concentrationoutputfactor(self):
		return self._concentrationoutputfactor
	@concentrationoutputfactor.setter
	def concentrationoutputfactor(self,value):
		self._concentrationoutputfactor=value

	@property
	def feedingrate(self):
		return (0.022 * self.bw ** (0.85) * exp(0.06 * linkedCompartmentvalue(self.containingvolumeelement,self.comp_objects_dict,"surface_water","watertemperature_c")))
	
	@property
	def concentrationoutputunits(self):
		return ("mg/kg wet weight")
	

	@property
	def initialconcentration_g_per_kg_usersupplied(self):
		cdict={}
		try:
			cdict["chem_2_3_7_8_tcdd"]=0.0
		except:
			cdict["chem_2_3_7_8_tcdd"]=nan
		
		return cdict

	@property
	def chemical_initialconcentration_g_per_kg_usersupplied(self):
		return self.initialconcentration_g_per_kg_usersupplied[self.currentchemical.name]

	@property
	def chemical_initialconcentration_g_per_kg_usersupplied(self):
		return self.initialconcentration_g_per_kg_usersupplied[self.currentchemical.name]


	@property
	def eliminationrateconstant(self):
		cdict={}
		try:
			cdict["chem_2_3_7_8_tcdd"]=0.2268
		except:
			cdict["chem_2_3_7_8_tcdd"]=nan
		
		return cdict

	@property
	def chemical_eliminationrateconstant(self):
		return self.eliminationrateconstant[self.currentchemical.name]

	@property
	def chemical_eliminationrateconstant(self):
		return self.eliminationrateconstant[self.currentchemical.name]


	@property
	def oxidationrate(self):
		cdict={}
		return cdict

	@property
	def chemical_oxidationrate(self):
		return self.oxidationrate[self.currentchemical.name]

	@property
	def chemical_oxidationrate(self):
		return self.oxidationrate[self.currentchemical.name]


	@property
	def absorptionrateconstant(self):
		cdict={}
		try:
			cdict["chem_2_3_7_8_tcdd"]=8640.0
		except:
			cdict["chem_2_3_7_8_tcdd"]=nan
		
		return cdict

	@property
	def chemical_absorptionrateconstant(self):
		return self.absorptionrateconstant[self.currentchemical.name]

	@property
	def chemical_absorptionrateconstant(self):
		return self.absorptionrateconstant[self.currentchemical.name]


	@property
	def generaldegradationrate(self):
		cdict={}
		try:
			cdict["chem_2_3_7_8_tcdd"]=log(2)/ self.chemical_halflife
		except:
			cdict["chem_2_3_7_8_tcdd"]=nan
		
		return cdict

	@property
	def chemical_generaldegradationrate(self):
		return self.generaldegradationrate[self.currentchemical.name]

	@property
	def chemical_generaldegradationrate(self):
		return self.generaldegradationrate[self.currentchemical.name]

	@property
	def populationsize(self):
		return (self.numberofzooplanktonpersquaremeter * self.containingvolumeelement.area)
	
	@property
	def totalmass(self):
		return (self.populationsize  * self.bw)
	

	@property
	def initialconcentration_g_per_kg(self):
		cdict={}
		try:
			cdict["chem_2_3_7_8_tcdd"]=self.containingscenario.fractioninitialconcentrations * self.chemical_initialconcentration_g_per_kg_usersupplied
		except:
			cdict["chem_2_3_7_8_tcdd"]=nan
		
		return cdict

	@property
	def chemical_initialconcentration_g_per_kg(self):
		return self.initialconcentration_g_per_kg[self.currentchemical.name]

	@property
	def chemical_initialconcentration_g_per_kg(self):
		return self.initialconcentration_g_per_kg[self.currentchemical.name]

	_isbiotic=True
	@property
	def isbiotic(self):
		return self._isbiotic
	@isbiotic.setter
	def isbiotic(self,value):
		self._isbiotic=value

	_fractiondietalgae=0.01
	@property
	def fractiondietalgae(self):
		return self._fractiondietalgae
	@fractiondietalgae.setter
	def fractiondietalgae(self,value):
		self._fractiondietalgae=value


	@property
	def methylationrate(self):
		cdict={}
		return cdict

	@property
	def chemical_methylationrate(self):
		return self.methylationrate[self.currentchemical.name]

	@property
	def chemical_methylationrate(self):
		return self.methylationrate[self.currentchemical.name]

	@property
	def foodingestionrate(self):
		return (self.feedingrate/self.bw)
	
	@property
	def numberofzooplanktonpersquaremeter(self):
		return (self.biomassperarea_kg_m2/self.bw)
	
	_bw=5.7e-8
	@property
	def bw(self):
		return self._bw
	@bw.setter
	def bw(self,value):
		self._bw=value
