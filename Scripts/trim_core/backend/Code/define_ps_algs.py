### note: this is an auto generated script
from numpy import nan

class direct_transfer_from_pseudosource_to_surface_water:
	def __init__(self, constants,containingscenario,currentchemical,sendingcompartment, receivingcompartment,dict_inputs):
		self.name='direct transfer from pseudosource to surface water'
		self.constants=constants
		self.containingscenario=containingscenario
		self.currentchemical=currentchemical
		self.sendingcompartment=sendingcompartment
		self.receivingcompartment=receivingcompartment
		self.doestransformchemical= "False"
		try: 
			self.transferfactor=1.0
		except: 
			self.transferfactor="tf computation error"

