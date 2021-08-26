### Note: This is an auto generated script
from find_neighbors import *
class Bulk_Advection_from_Surface_Water_to_Flush_rate_Advection_Sink_General_AlgInstID_4125:
	def __init__(self, Constants,containingScenario,currentChemical,SendingCompartment, ReceivingCompartment,dict_inputs):
		self.Name='Bulk Advection from Surface Water to Flush-rate Advection Sink, General(AlgInstID_4125)'
		self.Constants=Constants
		self.containingScenario=containingScenario
		self.currentChemical=currentChemical
		self.SendingCompartment=SendingCompartment
		self.ReceivingCompartment=ReceivingCompartment
		self.category='Advection'
		self.chemicalCategory='All'
		self.doesTransformChemical='false'
		self.TransportChemical='true'
		self.enabled='true'
		self.isDefaultForCategory='true'
		self.mate='<Unset>'
		self.receivingChemicalName='ReplaceMe'
		self.receivingCompartmentCategory='Sink | Abiotic | Surface water | Surface water - Default'
		self.sendingCompartmentCategory='Abiotic | Surface water | Surface water - Default'
		self.sendingChemicalName='ReplaceMe'
		self.dict_inputs=dict_inputs
		
		self.compartmentRelationship='IN_SAME_VOLUME_ELEMENT'


		try: 
			self.transferFactor=self.SendingCompartment.Flushes_per_year/365.0
		except: 
			self.transferFactor="TF Computation Error"

class Degradation_Reaction_Sink_in_Sediment_AlgInstID_4565:
	def __init__(self, Constants,containingScenario,currentChemical,SendingCompartment, ReceivingCompartment,dict_inputs):
		self.Name='Degradation/Reaction Sink in Sediment(AlgInstID_4565)'
		self.Constants=Constants
		self.containingScenario=containingScenario
		self.currentChemical=currentChemical
		self.SendingCompartment=SendingCompartment
		self.ReceivingCompartment=ReceivingCompartment
		self.category='Degradation/Transformation'
		self.chemicalCategory='Organic'
		self.doesTransformChemical='false'
		self.TransportChemical='true'
		self.enabled='true'
		self.isDefaultForCategory='true'
		self.mate='<Unset>'
		self.receivingChemicalName='ReplaceMe'
		self.receivingCompartmentCategory='Sink | Degradation/Reaction Sink'
		self.sendingCompartmentCategory='Abiotic | Sediment | Sediment - Default'
		self.sendingChemicalName='ReplaceMe'
		self.dict_inputs=dict_inputs
		
		self.compartmentRelationship='IN_SAME_VOLUME_ELEMENT'


		try: 
			self.transferFactor=self.SendingCompartment.Chemical_GeneralDegradationRate
		except: 
			self.transferFactor="TF Computation Error"

class Degradation_Reaction_Sink_in_Surface_Water_AlgInstID_4585:
	def __init__(self, Constants,containingScenario,currentChemical,SendingCompartment, ReceivingCompartment,dict_inputs):
		self.Name='Degradation/Reaction Sink in Surface Water(AlgInstID_4585)'
		self.Constants=Constants
		self.containingScenario=containingScenario
		self.currentChemical=currentChemical
		self.SendingCompartment=SendingCompartment
		self.ReceivingCompartment=ReceivingCompartment
		self.category='Degradation/Transformation'
		self.chemicalCategory='Organic'
		self.doesTransformChemical='false'
		self.TransportChemical='true'
		self.enabled='true'
		self.isDefaultForCategory='true'
		self.mate='<Unset>'
		self.receivingChemicalName='ReplaceMe'
		self.receivingCompartmentCategory='Sink | Degradation/Reaction Sink'
		self.sendingCompartmentCategory='Abiotic | Surface water | Surface water - Default'
		self.sendingChemicalName='ReplaceMe'
		self.dict_inputs=dict_inputs
		
		self.compartmentRelationship='IN_SAME_VOLUME_ELEMENT'


		try: 
			self.transferFactor=self.SendingCompartment.Chemical_GeneralDegradationRate
		except: 
			self.transferFactor="TF Computation Error"

class Demethylation_MHg_Hg2_in_Abiotic_Media_Rate_is_input_AlgInstID_1892:
	def __init__(self, Constants,containingScenario,currentChemical,SendingCompartment, ReceivingCompartment,dict_inputs):
		self.Name='Demethylation(MHg -> Hg2) in Abiotic Media, Rate is input(AlgInstID_1892)'
		self.Constants=Constants
		self.containingScenario=containingScenario
		self.currentChemical=currentChemical
		self.SendingCompartment=SendingCompartment
		self.ReceivingCompartment=ReceivingCompartment
		self.category='Transformation'
		self.chemicalCategory='<Unset>'
		self.doesTransformChemical='true'
		self.TransportChemical='false'
		self.enabled='true'
		self.isDefaultForCategory='true'
		self.mate='<Unset>'
		self.receivingChemicalName='Divalent Mercury'
		self.receivingCompartmentCategory='Abiotic'
		self.sendingCompartmentCategory='Abiotic'
		self.sendingChemicalName='MethylMercury'
		self.dict_inputs=dict_inputs
		
		self.compartmentRelationship='SAME'


		try: 
			self.transferFactor=self.SendingCompartment.Chemical_DemethylationRate
		except: 
			self.transferFactor="TF Computation Error"

class Diffusion_from_Sediment_to_Surface_Water_Fugacity_based_AlgInstID_2195:
	def __init__(self, Constants,containingScenario,currentChemical,SendingCompartment, ReceivingCompartment,dict_inputs):
		self.Name='Diffusion from Sediment to Surface Water, Fugacity-based(AlgInstID_2195)'
		self.Constants=Constants
		self.containingScenario=containingScenario
		self.currentChemical=currentChemical
		self.SendingCompartment=SendingCompartment
		self.ReceivingCompartment=ReceivingCompartment
		self.category='Diffusion'
		self.chemicalCategory='All'
		self.doesTransformChemical='false'
		self.TransportChemical='true'
		self.enabled='true'
		self.isDefaultForCategory='true'
		self.mate='<Unset>'
		self.receivingChemicalName='ReplaceMe'
		self.receivingCompartmentCategory='Abiotic | Surface water | Surface water - Default'
		self.sendingCompartmentCategory='Abiotic | Sediment | Sediment - Default'
		self.sendingChemicalName='ReplaceMe'
		self.dict_inputs=dict_inputs
		
		self.MassTransferCoefficient_Receiving_to_Sending=self.SendingCompartment.Chemical_D_effective / self.SendingCompartment.Chemical_BoundaryLayerThicknessbelowWater
		self.compartmentRelationship='SENDER_BELOW'
		self.MassTransferCoefficient_Sending_to_Receiving=self.ReceivingCompartment.Chemical_D_effective / self.ReceivingCompartment.BoundaryLayerThicknessAboveSediment

		self.Diffusiveterm_2=self.MassTransferCoefficient_Sending_to_Receiving
		self.Diffusiveterm_1=self.MassTransferCoefficient_Receiving_to_Sending * self.ReceivingCompartment.Chemical_Z_Total / self.SendingCompartment.Chemical_Z_Total

		self.DiffusiveTerm=(1 / self.Diffusiveterm_1 + 1 / self.Diffusiveterm_2) ** (-1)
		try: 
			self.transferFactor=self.Diffusiveterm * (check_neighbor(self.SendingCompartment,self.ReceivingCompartment,self.dict_inputs).is_neighbor()[1] / self.SendingCompartment.Volume)
		except: 
			self.transferFactor="TF Computation Error"

class Diffusion_from_Surface_Water_to_Sediment_Fugacity_based_AlgInstID_2149:
	def __init__(self, Constants,containingScenario,currentChemical,SendingCompartment, ReceivingCompartment,dict_inputs):
		self.Name='Diffusion from Surface Water to Sediment, Fugacity-based(AlgInstID_2149)'
		self.Constants=Constants
		self.containingScenario=containingScenario
		self.currentChemical=currentChemical
		self.SendingCompartment=SendingCompartment
		self.ReceivingCompartment=ReceivingCompartment
		self.category='Diffusion'
		self.chemicalCategory='All'
		self.doesTransformChemical='false'
		self.TransportChemical='true'
		self.enabled='true'
		self.isDefaultForCategory='true'
		self.mate='<Unset>'
		self.receivingChemicalName='ReplaceMe'
		self.receivingCompartmentCategory='Abiotic | Sediment | Sediment - Default'
		self.sendingCompartmentCategory='Abiotic | Surface water | Surface water - Default'
		self.sendingChemicalName='ReplaceMe'
		self.dict_inputs=dict_inputs
		
		self.MassTransferCoefficient_Receiving_to_Sending=self.ReceivingCompartment.Chemical_D_effective / self.ReceivingCompartment.Chemical_BoundaryLayerThicknessbelowWater
		self.compartmentRelationship='SENDER_ABOVE'
		self.MassTransferCoefficient_Sending_to_Receiving=self.SendingCompartment.Chemical_D_effective / self.SendingCompartment.BoundaryLayerThicknessAboveSediment

		self.Diffusiveterm_2=self.MassTransferCoefficient_Sending_to_Receiving
		self.Diffusiveterm_1=self.MassTransferCoefficient_Receiving_to_Sending * self.ReceivingCompartment.Chemical_Z_Total / self.SendingCompartment.Chemical_Z_Total

		self.DiffusiveTerm=(1 / self.Diffusiveterm_1 + 1 / self.Diffusiveterm_2) ** (-1)
		try: 
			self.transferFactor=self.Diffusiveterm * (check_neighbor(self.SendingCompartment,self.ReceivingCompartment,self.dict_inputs).is_neighbor()[1] / self.SendingCompartment.Volume)
		except: 
			self.transferFactor="TF Computation Error"

class Methylation_Hg2_MHg_in_Abiotic_Media_Rate_is_input_AlgInstID_1891:
	def __init__(self, Constants,containingScenario,currentChemical,SendingCompartment, ReceivingCompartment,dict_inputs):
		self.Name='Methylation(Hg2 -> MHg) in Abiotic Media, Rate is input(AlgInstID_1891)'
		self.Constants=Constants
		self.containingScenario=containingScenario
		self.currentChemical=currentChemical
		self.SendingCompartment=SendingCompartment
		self.ReceivingCompartment=ReceivingCompartment
		self.category='Transformation'
		self.chemicalCategory='<Unset>'
		self.doesTransformChemical='true'
		self.TransportChemical='false'
		self.enabled='true'
		self.isDefaultForCategory='true'
		self.mate='<Unset>'
		self.receivingChemicalName='MethylMercury'
		self.receivingCompartmentCategory='Abiotic'
		self.sendingCompartmentCategory='Abiotic'
		self.sendingChemicalName='Divalent Mercury'
		self.dict_inputs=dict_inputs
		
		self.compartmentRelationship='SAME'


		try: 
			self.transferFactor=self.SendingCompartment.Chemical_MethylationRate
		except: 
			self.transferFactor="TF Computation Error"

class Oxidation_Hg0_Hg2_in_Abiotic_Media_Rate_is_input_AlgInstID_1894:
	def __init__(self, Constants,containingScenario,currentChemical,SendingCompartment, ReceivingCompartment,dict_inputs):
		self.Name='Oxidation(Hg0 -> Hg2) in Abiotic Media, Rate is input(AlgInstID_1894)'
		self.Constants=Constants
		self.containingScenario=containingScenario
		self.currentChemical=currentChemical
		self.SendingCompartment=SendingCompartment
		self.ReceivingCompartment=ReceivingCompartment
		self.category='Transformation'
		self.chemicalCategory='<Unset>'
		self.doesTransformChemical='true'
		self.TransportChemical='false'
		self.enabled='true'
		self.isDefaultForCategory='true'
		self.mate='<Unset>'
		self.receivingChemicalName='Divalent Mercury'
		self.receivingCompartmentCategory='Abiotic'
		self.sendingCompartmentCategory='Abiotic'
		self.sendingChemicalName='Elemental Mercury'
		self.dict_inputs=dict_inputs
		
		self.compartmentRelationship='SAME'


		try: 
			self.transferFactor=self.SendingCompartment.Chemical_OxidationRate
		except: 
			self.transferFactor="TF Computation Error"

class Reduction_Hg2_Hg0_in_Abiotic_Media_Rate_is_input_AlgInstID_1893:
	def __init__(self, Constants,containingScenario,currentChemical,SendingCompartment, ReceivingCompartment,dict_inputs):
		self.Name='Reduction(Hg2 -> Hg0) in Abiotic Media, Rate is input(AlgInstID_1893)'
		self.Constants=Constants
		self.containingScenario=containingScenario
		self.currentChemical=currentChemical
		self.SendingCompartment=SendingCompartment
		self.ReceivingCompartment=ReceivingCompartment
		self.category='Transformation'
		self.chemicalCategory='<Unset>'
		self.doesTransformChemical='true'
		self.TransportChemical='false'
		self.enabled='true'
		self.isDefaultForCategory='true'
		self.mate='<Unset>'
		self.receivingChemicalName='Elemental Mercury'
		self.receivingCompartmentCategory='Abiotic'
		self.sendingCompartmentCategory='Abiotic'
		self.sendingChemicalName='Divalent Mercury'
		self.dict_inputs=dict_inputs
		
		self.compartmentRelationship='SAME'


		try: 
			self.transferFactor=self.SendingCompartment.Chemical_ReductionRate
		except: 
			self.transferFactor="TF Computation Error"

class Resuspension_from_Sediment_to_Surface_Water_General_AlgInstID_2190:
	def __init__(self, Constants,containingScenario,currentChemical,SendingCompartment, ReceivingCompartment,dict_inputs):
		self.Name='Resuspension from Sediment to Surface Water, General(AlgInstID_2190)'
		self.Constants=Constants
		self.containingScenario=containingScenario
		self.currentChemical=currentChemical
		self.SendingCompartment=SendingCompartment
		self.ReceivingCompartment=ReceivingCompartment
		self.category='Advection'
		self.chemicalCategory='All'
		self.doesTransformChemical='false'
		self.TransportChemical='true'
		self.enabled='true'
		self.isDefaultForCategory='true'
		self.mate='<Unset>'
		self.receivingChemicalName='ReplaceMe'
		self.receivingCompartmentCategory='Abiotic | Surface water | Surface water - Default'
		self.sendingCompartmentCategory='Abiotic | Sediment | Sediment - Default'
		self.sendingChemicalName='ReplaceMe'
		self.dict_inputs=dict_inputs
		
		self.SolidArealPhaseVelocity=self.SendingCompartment.SedimentResuspensionRate_m3_m2_day
		self.compartmentRelationship='SENDER_BELOW'


		try: 
			self.transferFactor=self.SolidArealPhaseVelocity * (self.SendingCompartment.Chemical_FractionMass_Sorbed/self.SendingCompartment.VolumeFraction_Solid) * (check_neighbor(self.SendingCompartment,self.ReceivingCompartment,self.dict_inputs).is_neighbor()[1]) / self.SendingCompartment.Volume
		except: 
			self.transferFactor="TF Computation Error"

class Sediment_Burial_from_Sediment_to_Sediment_Burial_Sink_Zero_net_deposition_General_AlgInstID_4135:
	def __init__(self, Constants,containingScenario,currentChemical,SendingCompartment, ReceivingCompartment,dict_inputs):
		self.Name='Sediment Burial from Sediment to Sediment Burial Sink, Zero net deposition, General(AlgInstID_4135)'
		self.Constants=Constants
		self.containingScenario=containingScenario
		self.currentChemical=currentChemical
		self.SendingCompartment=SendingCompartment
		self.ReceivingCompartment=ReceivingCompartment
		self.category='Advection'
		self.chemicalCategory='All'
		self.doesTransformChemical='false'
		self.TransportChemical='true'
		self.enabled='true'
		self.isDefaultForCategory='true'
		self.mate='<Unset>'
		self.receivingChemicalName='ReplaceMe'
		self.receivingCompartmentCategory='Sink | Abiotic | Sediment | Sediment - Default'
		self.sendingCompartmentCategory='Abiotic | Sediment | Sediment - Default'
		self.sendingChemicalName='ReplaceMe'
		self.dict_inputs=dict_inputs
		
		self.SolidArealPhaseVelocity=self.SendingCompartment.SedimentBurialRateToHaveZeroNetDeposition_m3_m2_day
		self.compartmentRelationship='SENDER_ABOVE'


		try: 
			self.transferFactor=self.SolidArealPhaseVelocity * (self.SendingCompartment.Chemical_FractionMass_Sorbed/self.SendingCompartment.VolumeFraction_Solid) * (check_neighbor(self.SendingCompartment,self.ReceivingCompartment,self.dict_inputs).is_neighbor()[1]) / self.SendingCompartment.Volume
		except: 
			self.transferFactor="TF Computation Error"

class Sediment_Deposition_from_Surface_Water_to_Sediment_General_AlgInstID_2139:
	def __init__(self, Constants,containingScenario,currentChemical,SendingCompartment, ReceivingCompartment,dict_inputs):
		self.Name='Sediment Deposition from Surface Water to Sediment, General(AlgInstID_2139)'
		self.Constants=Constants
		self.containingScenario=containingScenario
		self.currentChemical=currentChemical
		self.SendingCompartment=SendingCompartment
		self.ReceivingCompartment=ReceivingCompartment
		self.category='Advection'
		self.chemicalCategory='All'
		self.doesTransformChemical='false'
		self.TransportChemical='true'
		self.enabled='true'
		self.isDefaultForCategory='true'
		self.mate='<Unset>'
		self.receivingChemicalName='ReplaceMe'
		self.receivingCompartmentCategory='Abiotic | Sediment | Sediment - Default'
		self.sendingCompartmentCategory='Abiotic | Surface water | Surface water - Default'
		self.sendingChemicalName='ReplaceMe'
		self.dict_inputs=dict_inputs
		
		self.SolidArealPhaseVelocity=self.SendingCompartment.SedimentDepositionRate_m3_m2_day
		self.compartmentRelationship='SENDER_ABOVE'


		try: 
			self.transferFactor=self.SolidArealPhaseVelocity * (self.SendingCompartment.Chemical_FractionMass_Sorbed/self.SendingCompartment.VolumeFraction_Solid) * (check_neighbor(self.SendingCompartment,self.ReceivingCompartment,self.dict_inputs).is_neighbor()[1]) / self.SendingCompartment.Volume
		except: 
			self.transferFactor="TF Computation Error"

