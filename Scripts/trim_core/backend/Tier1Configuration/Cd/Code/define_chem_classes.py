### note: this is an auto generated script

from math import log
from constants import *
from define_scenario import *
from define_attributes_props import *



class chem_cadmium:
	def __init__(self,constants,containingscenario):
		self.containingscenario=containingscenario
		self.constants=constants
		self.name='chem_cadmium'

	@property
	def cas(self):
		return ("7440-43-9")
	
	@property
	def category(self):
		return ("metals | cadmium")
	
	_d_pureair=0.71
	@property
	def d_pureair(self):
		return self._d_pureair

	@d_pureair.setter
	def d_pureair(self,value):
		self._d_pureair=value

	@property
	def d_pureair_m2_s(self):
		return (self.d_pureair/86400)
	
	_d_purewater=8.16e-5
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
	
	_henrylawconstant=1.0e-37
	@property
	def henrylawconstant(self):
		return self._henrylawconstant

	@henrylawconstant.setter
	def henrylawconstant(self,value):
		self._henrylawconstant=value

	_meltingpoint=593.15
	@property
	def meltingpoint(self):
		return self._meltingpoint

	@meltingpoint.setter
	def meltingpoint(self,value):
		self._meltingpoint=value

	_molecularweight=112.41
	@property
	def molecularweight(self):
		return self._molecularweight

	@molecularweight.setter
	def molecularweight(self,value):
		self._molecularweight=value

	@property
	def z_pureair(self):
		return (1 / (self.constants.idealgasconstant * self.containingscenario.airtemperature_k))
	
	@property
	def z_purewater(self):
		return (1 / self.henrylawconstant)
	

chem_objects_dict={}
chem_cadmium=chem_cadmium(constants,containingscenario)
chem_objects_dict["chem_cadmium"]=chem_cadmium
