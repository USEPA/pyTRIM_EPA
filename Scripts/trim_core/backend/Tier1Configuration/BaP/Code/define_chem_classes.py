### note: this is an auto generated script

from math import log
from constants import *
from define_scenario import *
from define_attributes_props import *



class chem_benzo_a_pyrene:
	def __init__(self,constants,containingscenario):
		self.containingscenario=containingscenario
		self.constants=constants
		self.name='chem_benzo_a_pyrene'

	@property
	def airwaterpartitioncoefficient(self):
		return (self.h_over_r_t)
	
	@property
	def cas(self):
		return ("50-32-8")
	
	@property
	def category(self):
		return ("organic | pah | benzo(a)pyrene")
	
	_d_pureair=0.372
	@property
	def d_pureair(self):
		return self._d_pureair

	@d_pureair.setter
	def d_pureair(self,value):
		self._d_pureair=value

	@property
	def d_pureair_m2_s(self):
		return (self.d_pureair/86400)
	
	_d_purewater=7.78e-5
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
		return ("False")
	
	@property
	def enabled(self):
		return ("True")
	
	@property
	def h_over_r_t(self):
		return (self.henrylawconstant/(self.constants.idealgasconstant * self.containingscenario.airtemperature_k))
	
	_henrylawconstant=0.074
	@property
	def henrylawconstant(self):
		return self._henrylawconstant

	@henrylawconstant.setter
	def henrylawconstant(self,value):
		self._henrylawconstant=value

	@property
	def k_oa(self):
		return (self.k_ow*(self.constants.idealgasconstant * self.containingscenario.airtemperature_k/ self.henrylawconstant))
	
	_k_oc=968774.0
	@property
	def k_oc(self):
		return self._k_oc

	@k_oc.setter
	def k_oc(self,value):
		self._k_oc=value

	_k_ow=933000.0
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
	
	_meltingpoint=454.1
	@property
	def meltingpoint(self):
		return self._meltingpoint

	@meltingpoint.setter
	def meltingpoint(self,value):
		self._meltingpoint=value

	_molecularweight=252.31
	@property
	def molecularweight(self):
		return self._molecularweight

	@molecularweight.setter
	def molecularweight(self,value):
		self._molecularweight=value

	_referencebird_bodyweight=0.25
	@property
	def referencebird_bodyweight(self):
		return self._referencebird_bodyweight

	@referencebird_bodyweight.setter
	def referencebird_bodyweight(self,value):
		self._referencebird_bodyweight=value

	_referencebird_eliminationrate=0.6
	@property
	def referencebird_eliminationrate(self):
		return self._referencebird_eliminationrate

	@referencebird_eliminationrate.setter
	def referencebird_eliminationrate(self,value):
		self._referencebird_eliminationrate=value

	_referencebird_generaldegradationrate=2.04
	@property
	def referencebird_generaldegradationrate(self):
		return self._referencebird_generaldegradationrate

	@referencebird_generaldegradationrate.setter
	def referencebird_generaldegradationrate(self,value):
		self._referencebird_generaldegradationrate=value

	_referencemammal_bodyweight=0.25
	@property
	def referencemammal_bodyweight(self):
		return self._referencemammal_bodyweight

	@referencemammal_bodyweight.setter
	def referencemammal_bodyweight(self,value):
		self._referencemammal_bodyweight=value

	_referencemammal_eliminationrate=0.6
	@property
	def referencemammal_eliminationrate(self):
		return self._referencemammal_eliminationrate

	@referencemammal_eliminationrate.setter
	def referencemammal_eliminationrate(self,value):
		self._referencemammal_eliminationrate=value

	_referencemammal_generaldegradationrate=2.04
	@property
	def referencemammal_generaldegradationrate(self):
		return self._referencemammal_generaldegradationrate

	@referencemammal_generaldegradationrate.setter
	def referencemammal_generaldegradationrate(self,value):
		self._referencemammal_generaldegradationrate=value

	@property
	def z_pureair(self):
		return (1 / (self.constants.idealgasconstant * self.containingscenario.airtemperature_k))
	
	@property
	def z_purewater(self):
		return (1 / self.henrylawconstant)
	

chem_objects_dict={}
chem_benzo_a_pyrene=chem_benzo_a_pyrene(constants,containingscenario)
chem_objects_dict["chem_benzo_a_pyrene"]=chem_benzo_a_pyrene
