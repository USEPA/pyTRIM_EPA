### note: this is an auto generated script

from math import log
from constants import *
from define_scenario import *
from define_attributes_props import *



class chem_divalent_mercury:
	def __init__(self,constants,containingscenario):
		self.containingscenario=containingscenario
		self.constants=constants
		self.name='chem_divalent_mercury'

	@property
	def airwaterpartitioncoefficient(self):
		return (self.h_over_r_t)
	
	@property
	def cas(self):
		return ("14302-87-5")
	
	@property
	def category(self):
		return ("metals | mercury | divalent mercury")
	
	_d_pureair=0.478413366664244
	@property
	def d_pureair(self):
		return self._d_pureair

	@d_pureair.setter
	def d_pureair(self,value):
		self._d_pureair=value

	@property
	def d_pureair_m2_s(self):
		return (self.d_pureair/86400)
	
	_d_purewater=5.53952319295441e-5
	@property
	def d_purewater(self):
		return self._d_purewater

	@d_purewater.setter
	def d_purewater(self,value):
		self._d_purewater=value

	@property
	def d_purewater_m2_per_s(self):
		return (self.d_purewater/86400)
	
	@property
	def doestransform(self):
		return ("True")
	
	@property
	def enabled(self):
		return ("True")
	
	@property
	def h_over_r_t(self):
		return (self.henrylawconstant/(self.constants.idealgasconstant * self.containingscenario.airtemperature_k))
	
	_henrylawconstant=7.193515704154e-5
	@property
	def henrylawconstant(self):
		return self._henrylawconstant

	@henrylawconstant.setter
	def henrylawconstant(self,value):
		self._henrylawconstant=value

	@property
	def k_oa(self):
		return (self.k_ow*(self.constants.idealgasconstant * self.containingscenario.airtemperature_k/ self.henrylawconstant))
	
	@property
	def k_oc(self):
		return (self.k_ow*0.48)
	
	_k_ow=3.33
	@property
	def k_ow(self):
		return self._k_ow

	@k_ow.setter
	def k_ow(self,value):
		self._k_ow=value

	@property
	def log10_k_oa(self):
		return (log(self.k_oa)/log(10.0))
	
	@property
	def log10_k_ow(self):
		return (log(self.k_ow)/log(10.0))
	
	_meltingpoint=550.1
	@property
	def meltingpoint(self):
		return self._meltingpoint

	@meltingpoint.setter
	def meltingpoint(self,value):
		self._meltingpoint=value

	_molecularweight=201.0
	@property
	def molecularweight(self):
		return self._molecularweight

	@molecularweight.setter
	def molecularweight(self,value):
		self._molecularweight=value

	_vaporwashoutratio=1600000.0
	@property
	def vaporwashoutratio(self):
		return self._vaporwashoutratio

	@vaporwashoutratio.setter
	def vaporwashoutratio(self,value):
		self._vaporwashoutratio=value

	@property
	def z_pureair(self):
		return (1 / (self.constants.idealgasconstant * self.containingscenario.airtemperature_k))
	
	@property
	def z_purewater(self):
		return (1 / self.henrylawconstant)
	

class chem_elemental_mercury:
	def __init__(self,constants,containingscenario):
		self.containingscenario=containingscenario
		self.constants=constants
		self.name='chem_elemental_mercury'

	@property
	def airwaterpartitioncoefficient(self):
		return (self.h_over_r_t)
	
	@property
	def cas(self):
		return ("7439-97-6")
	
	@property
	def category(self):
		return ("metals | mercury | elemental mercury")
	
	_d_pureair=0.478413366664244
	@property
	def d_pureair(self):
		return self._d_pureair

	@d_pureair.setter
	def d_pureair(self,value):
		self._d_pureair=value

	@property
	def d_pureair_m2_s(self):
		return (self.d_pureair/86400)
	
	_d_purewater=5.53952319295441e-5
	@property
	def d_purewater(self):
		return self._d_purewater

	@d_purewater.setter
	def d_purewater(self,value):
		self._d_purewater=value

	@property
	def d_purewater_m2_per_s(self):
		return (self.d_purewater/86400)
	
	@property
	def doestransform(self):
		return ("True")
	
	@property
	def enabled(self):
		return ("True")
	
	@property
	def h_over_r_t(self):
		return (self.henrylawconstant/(self.constants.idealgasconstant * self.containingscenario.airtemperature_k))
	
	_henrylawconstant=719.3515704154
	@property
	def henrylawconstant(self):
		return self._henrylawconstant

	@henrylawconstant.setter
	def henrylawconstant(self,value):
		self._henrylawconstant=value

	@property
	def k_oa(self):
		return (self.k_ow*(self.constants.idealgasconstant * self.containingscenario.airtemperature_k/ self.henrylawconstant))
	
	@property
	def k_oc(self):
		return (self.k_ow*0.48)
	
	_k_ow=4.15
	@property
	def k_ow(self):
		return self._k_ow

	@k_ow.setter
	def k_ow(self,value):
		self._k_ow=value

	@property
	def log10_k_oa(self):
		return (log(self.k_oa)/log(10.0))
	
	@property
	def log10_k_ow(self):
		return (log(self.k_ow)/log(10.0))
	
	_meltingpoint=234.23
	@property
	def meltingpoint(self):
		return self._meltingpoint

	@meltingpoint.setter
	def meltingpoint(self,value):
		self._meltingpoint=value

	_molecularweight=201.0
	@property
	def molecularweight(self):
		return self._molecularweight

	@molecularweight.setter
	def molecularweight(self,value):
		self._molecularweight=value

	_vaporwashoutratio=1200.0
	@property
	def vaporwashoutratio(self):
		return self._vaporwashoutratio

	@vaporwashoutratio.setter
	def vaporwashoutratio(self,value):
		self._vaporwashoutratio=value

	@property
	def z_pureair(self):
		return (1 / (self.constants.idealgasconstant * self.containingscenario.airtemperature_k))
	
	@property
	def z_purewater(self):
		return (1 / self.henrylawconstant)
	

class chem_methylmercury:
	def __init__(self,constants,containingscenario):
		self.containingscenario=containingscenario
		self.constants=constants
		self.name='chem_methylmercury'

	@property
	def airwaterpartitioncoefficient(self):
		return (self.h_over_r_t)
	
	@property
	def cas(self):
		return ("22967-92-6")
	
	@property
	def category(self):
		return ("metals | mercury | methylmercury")
	
	_d_pureair=0.456
	@property
	def d_pureair(self):
		return self._d_pureair

	@d_pureair.setter
	def d_pureair(self,value):
		self._d_pureair=value

	@property
	def d_pureair_m2_s(self):
		return (self.d_pureair/86400)
	
	_d_purewater=5.28e-5
	@property
	def d_purewater(self):
		return self._d_purewater

	@d_purewater.setter
	def d_purewater(self,value):
		self._d_purewater=value

	@property
	def d_purewater_m2_per_s(self):
		return (self.d_purewater/86400)
	
	@property
	def doestransform(self):
		return ("True")
	
	@property
	def enabled(self):
		return ("True")
	
	@property
	def h_over_r_t(self):
		return (self.henrylawconstant/(self.constants.idealgasconstant * self.containingscenario.airtemperature_k))
	
	_henrylawconstant=0.0476190476190476
	@property
	def henrylawconstant(self):
		return self._henrylawconstant

	@henrylawconstant.setter
	def henrylawconstant(self,value):
		self._henrylawconstant=value

	@property
	def k_oa(self):
		return (self.k_ow*(self.constants.idealgasconstant * self.containingscenario.airtemperature_k/ self.henrylawconstant))
	
	@property
	def k_oc(self):
		return (self.k_ow*0.48)
	
	_k_ow=1.7
	@property
	def k_ow(self):
		return self._k_ow

	@k_ow.setter
	def k_ow(self,value):
		self._k_ow=value

	@property
	def log10_k_oa(self):
		return (log(self.k_oa)/log(10.0))
	
	@property
	def log10_k_ow(self):
		return (log(self.k_ow)/log(10.0))
	
	_meltingpoint=443.0
	@property
	def meltingpoint(self):
		return self._meltingpoint

	@meltingpoint.setter
	def meltingpoint(self,value):
		self._meltingpoint=value

	_molecularweight=216.0
	@property
	def molecularweight(self):
		return self._molecularweight

	@molecularweight.setter
	def molecularweight(self,value):
		self._molecularweight=value

	_molesofreportingchemicalpermolesofthischemical=1
	@property
	def molesofreportingchemicalpermolesofthischemical(self):
		return self._molesofreportingchemicalpermolesofthischemical

	@molesofreportingchemicalpermolesofthischemical.setter
	def molesofreportingchemicalpermolesofthischemical(self,value):
		self._molesofreportingchemicalpermolesofthischemical=value

	@property
	def reportasotherchemical(self):
		return ("hg")
	
	_reportingchemicalmw=201.0
	@property
	def reportingchemicalmw(self):
		return self._reportingchemicalmw

	@reportingchemicalmw.setter
	def reportingchemicalmw(self,value):
		self._reportingchemicalmw=value

	_vaporwashoutratio=0.0
	@property
	def vaporwashoutratio(self):
		return self._vaporwashoutratio

	@vaporwashoutratio.setter
	def vaporwashoutratio(self,value):
		self._vaporwashoutratio=value

	@property
	def z_pureair(self):
		return (1 / (self.constants.idealgasconstant * self.containingscenario.airtemperature_k))
	
	@property
	def z_purewater(self):
		return (1 / self.henrylawconstant)
	

chem_objects_dict={}
chem_divalent_mercury=chem_divalent_mercury(constants,containingscenario)
chem_objects_dict["chem_divalent_mercury"]=chem_divalent_mercury
chem_elemental_mercury=chem_elemental_mercury(constants,containingscenario)
chem_objects_dict["chem_elemental_mercury"]=chem_elemental_mercury
chem_methylmercury=chem_methylmercury(constants,containingscenario)
chem_objects_dict["chem_methylmercury"]=chem_methylmercury
