### Note: This is an auto generated script
from numpy import nan

class Direct_Transfer_from_PseudoSource_to_Surface_water:
	def __init__(self, Constants,containingScenario,currentChemical,SendingCompartment, ReceivingCompartment):
		self.Name='Direct Transfer from PseudoSource to Surface water'
		self.Constants=Constants
		self.containingScenario=containingScenario
		self.currentChemical=currentChemical
		self.SendingCompartment=SendingCompartment
		self.ReceivingCompartment=ReceivingCompartment
		try: 
			self.transferFactor=1.0
		except: 
			self.transferFactor="TF Computation Error"

