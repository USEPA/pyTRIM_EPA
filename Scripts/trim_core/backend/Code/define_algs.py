### note: this is an auto generated script
from find_neighbors import *
from numpy import sqrt,nan,log
class algae_deposition_from_surface_water_to_sediment_general_alginstid_2144:
	def __init__(self, constants,containingscenario,currentchemical,sendingcompartment, receivingcompartment,dict_inputs):
		self.name='algae deposition from surface water to sediment, general(alginstid_2144)'
		self.constants=constants
		self.containingscenario=containingscenario
		self.currentchemical=currentchemical
		self.sendingcompartment=sendingcompartment
		self.receivingcompartment=receivingcompartment
		self.category='advection'
		self.chemicalcategory='all'
		self.doestransformchemical='False'
		self.transportchemical='True'
		self.enabled='True'
		self.isdefaultforcategory='True'
		self.mate='<unset>'
		self.receivingchemicalname='replaceme'
		self.receivingcompartmentcategory='abiotic | sediment | sediment - default'
		self.sendingcompartmentcategory='abiotic | surface water | surface water - default'
		self.sendingchemicalname='replaceme'
		self.dict_inputs=dict_inputs
		
	@property
	def compartmentrelationship(self):
		return ("sender_above")
	
	@property
	def transferfactor(self):
		try:
			r=self.sendingcompartment.algaesedimentationrate_m3_m2_day * (self.sendingcompartment.chemical_fractionmass_algae/self.sendingcompartment.volumefraction_algae) * (check_neighbor(self.sendingcompartment,self.receivingcompartment,self.dict_inputs).is_neighbor()[1]) / self.sendingcompartment.volume
		except:
			r=nan
		return (r)

class bulk_advection_from_surface_water_to_flush_rate_advection_sink_general_alginstid_4125:
	def __init__(self, constants,containingscenario,currentchemical,sendingcompartment, receivingcompartment,dict_inputs):
		self.name='bulk advection from surface water to flush-rate advection sink, general(alginstid_4125)'
		self.constants=constants
		self.containingscenario=containingscenario
		self.currentchemical=currentchemical
		self.sendingcompartment=sendingcompartment
		self.receivingcompartment=receivingcompartment
		self.category='advection'
		self.chemicalcategory='all'
		self.doestransformchemical='False'
		self.transportchemical='True'
		self.enabled='True'
		self.isdefaultforcategory='True'
		self.mate='<unset>'
		self.receivingchemicalname='replaceme'
		self.receivingcompartmentcategory='sink | abiotic | surface water | surface water - default'
		self.sendingcompartmentcategory='abiotic | surface water | surface water - default'
		self.sendingchemicalname='replaceme'
		self.dict_inputs=dict_inputs
		
	@property
	def compartmentrelationship(self):
		return ("in_same_volume_element")
	
	@property
	def transferfactor(self):
		try:
			r=self.sendingcompartment.flushes_per_year/365.0
		except:
			r=nan
		return (r)

class degradation_reaction_sink_in_macrophyte:
	def __init__(self, constants,containingscenario,currentchemical,sendingcompartment, receivingcompartment,dict_inputs):
		self.name='degradation/reaction sink in macrophyte'
		self.constants=constants
		self.containingscenario=containingscenario
		self.currentchemical=currentchemical
		self.sendingcompartment=sendingcompartment
		self.receivingcompartment=receivingcompartment
		self.category='degradation/transformation'
		self.chemicalcategory='organic'
		self.doestransformchemical='False'
		self.transportchemical='True'
		self.enabled='True'
		self.isdefaultforcategory='True'
		self.mate='<unset>'
		self.receivingchemicalname='replaceme'
		self.receivingcompartmentcategory='sink | degradation/reaction sink'
		self.sendingcompartmentcategory='aquatic plant | macrophyte'
		self.sendingchemicalname='replaceme'
		self.dict_inputs=dict_inputs
		
	@property
	def compartmentrelationship(self):
		return ("in_same_volume_element")
	
	@property
	def transferfactor(self):
		try:
			r=self.sendingcompartment.chemical_generaldegradationrate
		except:
			r=nan
		return (r)

class degradation_reaction_sink_in_sediment_alginstid_4565:
	def __init__(self, constants,containingscenario,currentchemical,sendingcompartment, receivingcompartment,dict_inputs):
		self.name='degradation/reaction sink in sediment(alginstid_4565)'
		self.constants=constants
		self.containingscenario=containingscenario
		self.currentchemical=currentchemical
		self.sendingcompartment=sendingcompartment
		self.receivingcompartment=receivingcompartment
		self.category='degradation/transformation'
		self.chemicalcategory='organic'
		self.doestransformchemical='False'
		self.transportchemical='True'
		self.enabled='True'
		self.isdefaultforcategory='True'
		self.mate='<unset>'
		self.receivingchemicalname='replaceme'
		self.receivingcompartmentcategory='sink | degradation/reaction sink'
		self.sendingcompartmentcategory='abiotic | sediment | sediment - default'
		self.sendingchemicalname='replaceme'
		self.dict_inputs=dict_inputs
		
	@property
	def compartmentrelationship(self):
		return ("in_same_volume_element")
	
	@property
	def transferfactor(self):
		try:
			r=self.sendingcompartment.chemical_generaldegradationrate
		except:
			r=nan
		return (r)

class degradation_reaction_sink_in_surface_water_alginstid_4585:
	def __init__(self, constants,containingscenario,currentchemical,sendingcompartment, receivingcompartment,dict_inputs):
		self.name='degradation/reaction sink in surface water(alginstid_4585)'
		self.constants=constants
		self.containingscenario=containingscenario
		self.currentchemical=currentchemical
		self.sendingcompartment=sendingcompartment
		self.receivingcompartment=receivingcompartment
		self.category='degradation/transformation'
		self.chemicalcategory='organic'
		self.doestransformchemical='False'
		self.transportchemical='True'
		self.enabled='True'
		self.isdefaultforcategory='True'
		self.mate='<unset>'
		self.receivingchemicalname='replaceme'
		self.receivingcompartmentcategory='sink | degradation/reaction sink'
		self.sendingcompartmentcategory='abiotic | surface water | surface water - default'
		self.sendingchemicalname='replaceme'
		self.dict_inputs=dict_inputs
		
	@property
	def compartmentrelationship(self):
		return ("in_same_volume_element")
	
	@property
	def transferfactor(self):
		try:
			r=self.sendingcompartment.chemical_generaldegradationrate
		except:
			r=nan
		return (r)

class degradation_reaction_sink_in_zooplankton_alginstid_4570_z:
	def __init__(self, constants,containingscenario,currentchemical,sendingcompartment, receivingcompartment,dict_inputs):
		self.name='degradation/reaction sink in zooplankton(alginstid_4570_z)'
		self.constants=constants
		self.containingscenario=containingscenario
		self.currentchemical=currentchemical
		self.sendingcompartment=sendingcompartment
		self.receivingcompartment=receivingcompartment
		self.category='degradation/transformation'
		self.chemicalcategory='organic'
		self.doestransformchemical='False'
		self.transportchemical='True'
		self.enabled='True'
		self.isdefaultforcategory='True'
		self.mate='<unset>'
		self.receivingchemicalname='replaceme'
		self.receivingcompartmentcategory='sink | degradation/reaction sink'
		self.sendingcompartmentcategory='invertebrate | zooplankton'
		self.sendingchemicalname='replaceme'
		self.dict_inputs=dict_inputs
		
	@property
	def compartmentrelationship(self):
		return ("in_same_volume_element")
	
	@property
	def transferfactor(self):
		try:
			r=self.sendingcompartment.chemical_generaldegradationrate
		except:
			r=nan
		return (r)

class demethylation_mhg_hg2_in_fish_alginstid_1446:
	def __init__(self, constants,containingscenario,currentchemical,sendingcompartment, receivingcompartment,dict_inputs):
		self.name='demethylation (mhg->hg2) in fish(alginstid_1446)'
		self.constants=constants
		self.containingscenario=containingscenario
		self.currentchemical=currentchemical
		self.sendingcompartment=sendingcompartment
		self.receivingcompartment=receivingcompartment
		self.category='transformation'
		self.chemicalcategory='<unset>'
		self.doestransformchemical='True'
		self.transportchemical='False'
		self.enabled='True'
		self.isdefaultforcategory='True'
		self.mate='<unset>'
		self.receivingchemicalname='divalent mercury'
		self.receivingcompartmentcategory='fish'
		self.sendingcompartmentcategory='fish'
		self.sendingchemicalname='methylmercury'
		self.dict_inputs=dict_inputs
		
	@property
	def compartmentrelationship(self):
		return ("same")
	
	@property
	def transferfactor(self):
		try:
			r=self.sendingcompartment.chemical_demethylationrate
		except:
			r=nan
		return (r)

class demethylation_mhg_hg2_in_abiotic_media_rate_is_input_alginstid_1892:
	def __init__(self, constants,containingscenario,currentchemical,sendingcompartment, receivingcompartment,dict_inputs):
		self.name='demethylation(mhg -> hg2) in abiotic media, rate is input(alginstid_1892)'
		self.constants=constants
		self.containingscenario=containingscenario
		self.currentchemical=currentchemical
		self.sendingcompartment=sendingcompartment
		self.receivingcompartment=receivingcompartment
		self.category='transformation'
		self.chemicalcategory='<unset>'
		self.doestransformchemical='True'
		self.transportchemical='False'
		self.enabled='True'
		self.isdefaultforcategory='True'
		self.mate='<unset>'
		self.receivingchemicalname='divalent mercury'
		self.receivingcompartmentcategory='abiotic'
		self.sendingcompartmentcategory='abiotic'
		self.sendingchemicalname='methylmercury'
		self.dict_inputs=dict_inputs
		
	@property
	def compartmentrelationship(self):
		return ("same")
	
	@property
	def transferfactor(self):
		try:
			r=self.sendingcompartment.chemical_demethylationrate
		except:
			r=nan
		return (r)

class diffusion_from_sediment_to_surface_water_fugacity_based_alginstid_2195:
	def __init__(self, constants,containingscenario,currentchemical,sendingcompartment, receivingcompartment,dict_inputs):
		self.name='diffusion from sediment to surface water, fugacity-based(alginstid_2195)'
		self.constants=constants
		self.containingscenario=containingscenario
		self.currentchemical=currentchemical
		self.sendingcompartment=sendingcompartment
		self.receivingcompartment=receivingcompartment
		self.category='diffusion'
		self.chemicalcategory='all'
		self.doestransformchemical='False'
		self.transportchemical='True'
		self.enabled='True'
		self.isdefaultforcategory='True'
		self.mate='<unset>'
		self.receivingchemicalname='replaceme'
		self.receivingcompartmentcategory='abiotic | surface water | surface water - default'
		self.sendingcompartmentcategory='abiotic | sediment | sediment - default'
		self.sendingchemicalname='replaceme'
		self.dict_inputs=dict_inputs
		
	@property
	def masstransfercoefficient_receiving_to_sending(self):
		return (self.sendingcompartment.chemical_d_effective / self.sendingcompartment.chemical_boundarylayerthicknessbelowwater)
	
	@property
	def diffusiveterm_1(self):
		return (self.masstransfercoefficient_receiving_to_sending * self.receivingcompartment.chemical_z_total / self.sendingcompartment.chemical_z_total)
	
	@property
	def compartmentrelationship(self):
		return ("sender_below")
	
	@property
	def diffusiveterm_2(self):
		return (self.masstransfercoefficient_sending_to_receiving)
	
	@property
	def diffusiveterm(self):
		return ((1 / self.diffusiveterm_1 + 1 / self.diffusiveterm_2) ** (-1))
	
	@property
	def masstransfercoefficient_sending_to_receiving(self):
		return (self.receivingcompartment.chemical_d_effective / self.receivingcompartment.boundarylayerthicknessabovesediment)
	
	@property
	def transferfactor(self):
		try:
			r=self.diffusiveterm * (check_neighbor(self.sendingcompartment,self.receivingcompartment,self.dict_inputs).is_neighbor()[1] / self.sendingcompartment.volume)
		except:
			r=nan
		return (r)

class diffusion_from_surface_water_to_air_two_film_alginstid_4080_hg:
	def __init__(self, constants,containingscenario,currentchemical,sendingcompartment, receivingcompartment,dict_inputs):
		self.name='diffusion from surface water to air, two film(alginstid_4080)-hg'
		self.constants=constants
		self.containingscenario=containingscenario
		self.currentchemical=currentchemical
		self.sendingcompartment=sendingcompartment
		self.receivingcompartment=receivingcompartment
		self.category='diffusion'
		self.chemicalcategory='metals | mercury'
		self.doestransformchemical='False'
		self.transportchemical='True'
		self.enabled='True'
		self.isdefaultforcategory='True'
		self.mate='<unset>'
		self.receivingchemicalname='replaceme'
		self.receivingcompartmentcategory='abiotic | air | air - default'
		self.sendingcompartmentcategory='abiotic | surface water | surface water - default'
		self.sendingchemicalname='replaceme'
		self.dict_inputs=dict_inputs
		
	@property
	def liquidphasetransfercoefficient_lake(self):
		return ((self.sendingcompartment.shearvelocity_m_per_day)*((self.receivingcompartment.airdensity_kg_m3/self.sendingcompartment.waterdensity)**(0.5))*((self.constants.vonkarmensconstant**(0.33))/self.sendingcompartment.dimensionlessviscoussublayerthickness) * self.sendingcompartment.chemical_waterschmidtnumber**(-0.67))
	
	@property
	def liquidphasetransfercoefficient_flowingwaterbody(self):
		return (self.reaerationvelocity_owensformula * self.ratioofvolatilizationratetoreaerationrate if self.sendingcompartment.depth < 0.61 else ((self.currentchemical.d_purewater_m2_per_s * self.sendingcompartment.currentvelocity/self.sendingcompartment.depth)**(0.5))* 86400 if self.sendingcompartment.depth >= 0.61 and (self.sendingcompartment.currentvelocity < 0.518 or self.sendingcompartment.depth> 13.584 * self.sendingcompartment.currentvelocity**(0.29135)) else self.reaerationvelocity_churchillformula * self.ratioofvolatilizationratetoreaerationrate)
	
	@property
	def reaerationvelocity_owensformula(self):
		return (5.349 * (self.sendingcompartment.currentvelocity**0.67)/ (self.sendingcompartment.depth**0.85))
	
	@property
	def gasphasetransfercoefficient(self):
		return ((self.sendingcompartment.shearvelocity_m_per_day)*((self.constants.vonkarmensconstant**(0.33))/self.sendingcompartment.dimensionlessviscoussublayerthickness) * self.receivingcompartment.chemical_airschmidtnumber**(-0.67))
	
	@property
	def liquidphaseresistance(self):
		return (1/self.liquidphasetransfercoefficient_lake if  not (self.sendingcompartment.isflowing) else 1/self.liquidphasetransfercoefficient_flowingwaterbody)
	
	@property
	def reaerationvelocity_churchillformula(self):
		return (5.049 * (self.sendingcompartment.currentvelocity**0.969)/ (self.sendingcompartment.depth**0.673))
	
	@property
	def gasphaseresistance(self):
		return (1/  ( self.gasphasetransfercoefficient * (self.currentchemical.h_over_r_t) ))
	
	@property
	def volatilizationtransferrate(self):
		return (1/(self.liquidphaseresistance + self.gasphaseresistance))
	
	@property
	def ratioofvolatilizationratetoreaerationrate(self):
		return (sqrt(32/self.currentchemical.molecularweight))
	
	@property
	def transferfactor(self):
		try:
			r=self.volatilizationtransferrate * (self.sendingcompartment.chemical_fractionmass_dissolved /self.sendingcompartment.volumefraction_liquid)*(check_neighbor(self.sendingcompartment,self.receivingcompartment,self.dict_inputs).is_neighbor()[1] / self.sendingcompartment.volume)
		except:
			r=nan
		return (r)

class diffusion_from_surface_water_to_sediment_fugacity_based_alginstid_2149:
	def __init__(self, constants,containingscenario,currentchemical,sendingcompartment, receivingcompartment,dict_inputs):
		self.name='diffusion from surface water to sediment, fugacity-based(alginstid_2149)'
		self.constants=constants
		self.containingscenario=containingscenario
		self.currentchemical=currentchemical
		self.sendingcompartment=sendingcompartment
		self.receivingcompartment=receivingcompartment
		self.category='diffusion'
		self.chemicalcategory='all'
		self.doestransformchemical='False'
		self.transportchemical='True'
		self.enabled='True'
		self.isdefaultforcategory='True'
		self.mate='<unset>'
		self.receivingchemicalname='replaceme'
		self.receivingcompartmentcategory='abiotic | sediment | sediment - default'
		self.sendingcompartmentcategory='abiotic | surface water | surface water - default'
		self.sendingchemicalname='replaceme'
		self.dict_inputs=dict_inputs
		
	@property
	def masstransfercoefficient_receiving_to_sending(self):
		return (self.receivingcompartment.chemical_d_effective / self.receivingcompartment.chemical_boundarylayerthicknessbelowwater)
	
	@property
	def diffusiveterm_1(self):
		return (self.masstransfercoefficient_receiving_to_sending * self.receivingcompartment.chemical_z_total / self.sendingcompartment.chemical_z_total)
	
	@property
	def compartmentrelationship(self):
		return ("sender_above")
	
	@property
	def diffusiveterm_2(self):
		return (self.masstransfercoefficient_sending_to_receiving)
	
	@property
	def diffusiveterm(self):
		return ((1 / self.diffusiveterm_1 + 1 / self.diffusiveterm_2) ** (-1))
	
	@property
	def masstransfercoefficient_sending_to_receiving(self):
		return (self.sendingcompartment.chemical_d_effective / self.sendingcompartment.boundarylayerthicknessabovesediment)
	
	@property
	def transferfactor(self):
		try:
			r=self.diffusiveterm * (check_neighbor(self.sendingcompartment,self.receivingcompartment,self.dict_inputs).is_neighbor()[1] / self.sendingcompartment.volume)
		except:
			r=nan
		return (r)

class elimination_from_fish_to_surface_water_alginstid_1512:
	def __init__(self, constants,containingscenario,currentchemical,sendingcompartment, receivingcompartment,dict_inputs):
		self.name='elimination from fish to surface water(alginstid_1512)'
		self.constants=constants
		self.containingscenario=containingscenario
		self.currentchemical=currentchemical
		self.sendingcompartment=sendingcompartment
		self.receivingcompartment=receivingcompartment
		self.category='bioenergetic fish model'
		self.chemicalcategory='metals'
		self.doestransformchemical='False'
		self.transportchemical='True'
		self.enabled='True'
		self.isdefaultforcategory='True'
		self.mate='<unset>'
		self.receivingchemicalname='replaceme'
		self.receivingcompartmentcategory='abiotic | surface water | surface water - default'
		self.sendingcompartmentcategory='fish'
		self.sendingchemicalname='replaceme'
		self.dict_inputs=dict_inputs
		
	@property
	def transferfactor(self):
		try:
			r=self.sendingcompartment.chemical_eliminationrateconstant
		except:
			r=nan
		return (r)

class elimination_from_zooplankton_to_surface_water:
	def __init__(self, constants,containingscenario,currentchemical,sendingcompartment, receivingcompartment,dict_inputs):
		self.name='elimination from zooplankton to surface water'
		self.constants=constants
		self.containingscenario=containingscenario
		self.currentchemical=currentchemical
		self.sendingcompartment=sendingcompartment
		self.receivingcompartment=receivingcompartment
		self.category='bioenergetic fish model'
		self.chemicalcategory='all'
		self.doestransformchemical='False'
		self.transportchemical='True'
		self.enabled='True'
		self.isdefaultforcategory='True'
		self.mate='<unset>'
		self.receivingchemicalname='replaceme'
		self.receivingcompartmentcategory='abiotic | surface water | surface water - default'
		self.sendingcompartmentcategory='invertebrate | zooplankton'
		self.sendingchemicalname='replaceme'
		self.dict_inputs=dict_inputs
		
	@property
	def transferfactor(self):
		try:
			r=self.sendingcompartment.chemical_eliminationrateconstant
		except:
			r=nan
		return (r)

class exchange_from_macrophyte_to_surface_water_alginstid_1547:
	def __init__(self, constants,containingscenario,currentchemical,sendingcompartment, receivingcompartment,dict_inputs):
		self.name='exchange from macrophyte to surface water(alginstid_1547)'
		self.constants=constants
		self.containingscenario=containingscenario
		self.currentchemical=currentchemical
		self.sendingcompartment=sendingcompartment
		self.receivingcompartment=receivingcompartment
		self.category='exchange'
		self.chemicalcategory='organic'
		self.doestransformchemical='False'
		self.transportchemical='True'
		self.enabled='True'
		self.isdefaultforcategory='True'
		self.mate='<unset>'
		self.receivingchemicalname='replaceme'
		self.receivingcompartmentcategory='abiotic | surface water | surface water - default'
		self.sendingcompartmentcategory='aquatic plant | macrophyte'
		self.sendingchemicalname='replaceme'
		self.dict_inputs=dict_inputs
		
	@property
	def transferfactor(self):
		try:
			r=self.sendingcompartment.chemical_depurationrate
		except:
			r=nan
		return (r)

class fish_bioenergetic_model_ingestion_of_algae_by_fish_alginstid_1527:
	def __init__(self, constants,containingscenario,currentchemical,sendingcompartment, receivingcompartment,dict_inputs):
		self.name='fish bioenergetic model - ingestion of algae by fish(alginstid_1527)'
		self.constants=constants
		self.containingscenario=containingscenario
		self.currentchemical=currentchemical
		self.sendingcompartment=sendingcompartment
		self.receivingcompartment=receivingcompartment
		self.category='bioenergetic fish model'
		self.chemicalcategory='all'
		self.doestransformchemical='False'
		self.transportchemical='True'
		self.enabled='True'
		self.isdefaultforcategory='True'
		self.mate='<unset>'
		self.receivingchemicalname='replaceme'
		self.receivingcompartmentcategory='fish'
		self.sendingcompartmentcategory='abiotic | surface water | surface water - default'
		self.sendingchemicalname='replaceme'
		self.dict_inputs=dict_inputs
		
	@property
	def transferfactor(self):
		try:
			r=self.receivingcompartment.populationsize * self.receivingcompartment.bw * 1 * self.receivingcompartment.fractiondietalgae * self.receivingcompartment.foodingestionrate * self.receivingcompartment.chemical_assimilationefficiencyfromfood * (self.sendingcompartment.chemical_fractionmass_algae/ self.sendingcompartment.totalalgaemass)
		except:
			r=nan
		return (r)

class fish_bioenergetic_model_ingestion_of_algae_by_zooplankton:
	def __init__(self, constants,containingscenario,currentchemical,sendingcompartment, receivingcompartment,dict_inputs):
		self.name='fish bioenergetic model - ingestion of algae by zooplankton'
		self.constants=constants
		self.containingscenario=containingscenario
		self.currentchemical=currentchemical
		self.sendingcompartment=sendingcompartment
		self.receivingcompartment=receivingcompartment
		self.category='bioenergetic fish model'
		self.chemicalcategory='all'
		self.doestransformchemical='False'
		self.transportchemical='True'
		self.enabled='True'
		self.isdefaultforcategory='True'
		self.mate='<unset>'
		self.receivingchemicalname='replaceme'
		self.receivingcompartmentcategory='invertebrate | zooplankton'
		self.sendingcompartmentcategory='abiotic | surface water | surface water - default'
		self.sendingchemicalname='replaceme'
		self.dict_inputs=dict_inputs
		
	@property
	def transferfactor(self):
		try:
			r=self.receivingcompartment.populationsize * self.receivingcompartment.bw * 1 * self.receivingcompartment.fractiondietalgae * self.receivingcompartment.foodingestionrate * self.receivingcompartment.chemical_assimilationefficiencyfromalgae * (self.sendingcompartment.chemical_fractionmass_algae/ self.sendingcompartment.totalalgaemass)
		except:
			r=nan
		return (r)

class fish_bioenergetic_model_ingestion_of_benthic_carnivore_by_benthic_omnivore_alginstid_1455:
	def __init__(self, constants,containingscenario,currentchemical,sendingcompartment, receivingcompartment,dict_inputs):
		self.name='fish bioenergetic model - ingestion of benthic carnivore by benthic omnivore(alginstid_1455)'
		self.constants=constants
		self.containingscenario=containingscenario
		self.currentchemical=currentchemical
		self.sendingcompartment=sendingcompartment
		self.receivingcompartment=receivingcompartment
		self.category='bioenergetic fish model'
		self.chemicalcategory='all'
		self.doestransformchemical='False'
		self.transportchemical='True'
		self.enabled='True'
		self.isdefaultforcategory='True'
		self.mate='<unset>'
		self.receivingchemicalname='replaceme'
		self.receivingcompartmentcategory='fish | benthic omnivore'
		self.sendingcompartmentcategory='fish | benthic carnivore'
		self.sendingchemicalname='replaceme'
		self.dict_inputs=dict_inputs
		
	@property
	def transferfactor(self):
		try:
			r=self.receivingcompartment.populationsize * self.receivingcompartment.bw * 1 * self.receivingcompartment.fractiondietfishbenthiccarnivore * self.receivingcompartment.foodingestionrate * self.receivingcompartment.chemical_assimilationefficiencyfromfood   / self.sendingcompartment.totalmass
		except:
			r=nan
		return (r)

class fish_bioenergetic_model_ingestion_of_benthic_carnivore_by_water_column_carnivore_alginstid_2245:
	def __init__(self, constants,containingscenario,currentchemical,sendingcompartment, receivingcompartment,dict_inputs):
		self.name='fish bioenergetic model - ingestion of benthic carnivore by water column carnivore(alginstid_2245)'
		self.constants=constants
		self.containingscenario=containingscenario
		self.currentchemical=currentchemical
		self.sendingcompartment=sendingcompartment
		self.receivingcompartment=receivingcompartment
		self.category='bioenergetic fish model'
		self.chemicalcategory='all'
		self.doestransformchemical='False'
		self.transportchemical='True'
		self.enabled='True'
		self.isdefaultforcategory='True'
		self.mate='<unset>'
		self.receivingchemicalname='replaceme'
		self.receivingcompartmentcategory='fish | water column carnivore'
		self.sendingcompartmentcategory='fish | benthic carnivore'
		self.sendingchemicalname='replaceme'
		self.dict_inputs=dict_inputs
		
	@property
	def transferfactor(self):
		try:
			r=self.receivingcompartment.populationsize * self.receivingcompartment.bw * 1 * self.receivingcompartment.fractiondietfishbenthiccarnivore * self.receivingcompartment.foodingestionrate * self.receivingcompartment.chemical_assimilationefficiencyfromfood   / self.sendingcompartment.totalmass
		except:
			r=nan
		return (r)

class fish_bioenergetic_model_ingestion_of_benthic_carnivore_by_water_column_omnivore_alginstid_2277:
	def __init__(self, constants,containingscenario,currentchemical,sendingcompartment, receivingcompartment,dict_inputs):
		self.name='fish bioenergetic model - ingestion of benthic carnivore by water column omnivore(alginstid_2277)'
		self.constants=constants
		self.containingscenario=containingscenario
		self.currentchemical=currentchemical
		self.sendingcompartment=sendingcompartment
		self.receivingcompartment=receivingcompartment
		self.category='bioenergetic fish model'
		self.chemicalcategory='all'
		self.doestransformchemical='False'
		self.transportchemical='True'
		self.enabled='True'
		self.isdefaultforcategory='True'
		self.mate='<unset>'
		self.receivingchemicalname='replaceme'
		self.receivingcompartmentcategory='fish | water column omnivore'
		self.sendingcompartmentcategory='fish | benthic carnivore'
		self.sendingchemicalname='replaceme'
		self.dict_inputs=dict_inputs
		
	@property
	def transferfactor(self):
		try:
			r=self.receivingcompartment.populationsize * self.receivingcompartment.bw * 1 * self.receivingcompartment.fractiondietfishbenthiccarnivore * self.receivingcompartment.foodingestionrate * self.receivingcompartment.chemical_assimilationefficiencyfromfood   / self.sendingcompartment.totalmass
		except:
			r=nan
		return (r)

class fish_bioenergetic_model_ingestion_of_benthic_invertebrate_by_benthic_carnivore_icfid_08_001:
	def __init__(self, constants,containingscenario,currentchemical,sendingcompartment, receivingcompartment,dict_inputs):
		self.name='fish bioenergetic model - ingestion of benthic invertebrate by benthic carnivore(icfid_08-001)'
		self.constants=constants
		self.containingscenario=containingscenario
		self.currentchemical=currentchemical
		self.sendingcompartment=sendingcompartment
		self.receivingcompartment=receivingcompartment
		self.category='bioenergetic fish model'
		self.chemicalcategory='all'
		self.doestransformchemical='False'
		self.transportchemical='True'
		self.enabled='True'
		self.isdefaultforcategory='True'
		self.mate='<unset>'
		self.receivingchemicalname='replaceme'
		self.receivingcompartmentcategory='fish | benthic carnivore'
		self.sendingcompartmentcategory='insect | benthic invertebrate'
		self.sendingchemicalname='replaceme'
		self.dict_inputs=dict_inputs
		
	@property
	def transferfactor(self):
		try:
			r=self.receivingcompartment.populationsize * self.receivingcompartment.bw * 1 * self.receivingcompartment.fractiondietbenthicinvertebrate * self.receivingcompartment.foodingestionrate * self.receivingcompartment.chemical_assimilationefficiencyfromfood   / self.sendingcompartment.totalmass
		except:
			r=nan
		return (r)

class fish_bioenergetic_model_ingestion_of_benthic_invertebrate_by_benthic_omnivore_alginstid_1467:
	def __init__(self, constants,containingscenario,currentchemical,sendingcompartment, receivingcompartment,dict_inputs):
		self.name='fish bioenergetic model - ingestion of benthic invertebrate by benthic omnivore(alginstid_1467)'
		self.constants=constants
		self.containingscenario=containingscenario
		self.currentchemical=currentchemical
		self.sendingcompartment=sendingcompartment
		self.receivingcompartment=receivingcompartment
		self.category='bioenergetic fish model'
		self.chemicalcategory='all'
		self.doestransformchemical='False'
		self.transportchemical='True'
		self.enabled='True'
		self.isdefaultforcategory='True'
		self.mate='<unset>'
		self.receivingchemicalname='replaceme'
		self.receivingcompartmentcategory='fish | benthic omnivore'
		self.sendingcompartmentcategory='insect | benthic invertebrate'
		self.sendingchemicalname='replaceme'
		self.dict_inputs=dict_inputs
		
	@property
	def transferfactor(self):
		try:
			r=self.receivingcompartment.populationsize * self.receivingcompartment.bw * 1 * self.receivingcompartment.fractiondietbenthicinvertebrate * self.receivingcompartment.foodingestionrate * self.receivingcompartment.chemical_assimilationefficiencyfromfood   / self.sendingcompartment.totalmass
		except:
			r=nan
		return (r)

class fish_bioenergetic_model_ingestion_of_benthic_invertebrate_by_water_column_carnivore_alginstid_2255:
	def __init__(self, constants,containingscenario,currentchemical,sendingcompartment, receivingcompartment,dict_inputs):
		self.name='fish bioenergetic model - ingestion of benthic invertebrate by water column carnivore(alginstid_2255)'
		self.constants=constants
		self.containingscenario=containingscenario
		self.currentchemical=currentchemical
		self.sendingcompartment=sendingcompartment
		self.receivingcompartment=receivingcompartment
		self.category='bioenergetic fish model'
		self.chemicalcategory='all'
		self.doestransformchemical='False'
		self.transportchemical='True'
		self.enabled='True'
		self.isdefaultforcategory='True'
		self.mate='<unset>'
		self.receivingchemicalname='replaceme'
		self.receivingcompartmentcategory='fish | water column carnivore'
		self.sendingcompartmentcategory='insect | benthic invertebrate'
		self.sendingchemicalname='replaceme'
		self.dict_inputs=dict_inputs
		
	@property
	def transferfactor(self):
		try:
			r=self.receivingcompartment.populationsize * self.receivingcompartment.bw * 1 * self.receivingcompartment.fractiondietbenthicinvertebrate * self.receivingcompartment.foodingestionrate * self.receivingcompartment.chemical_assimilationefficiencyfromfood   / self.sendingcompartment.totalmass
		except:
			r=nan
		return (r)

class fish_bioenergetic_model_ingestion_of_benthic_invertebrate_by_water_column_herbivore_alginstid_2270:
	def __init__(self, constants,containingscenario,currentchemical,sendingcompartment, receivingcompartment,dict_inputs):
		self.name='fish bioenergetic model - ingestion of benthic invertebrate by water column herbivore(alginstid_2270)'
		self.constants=constants
		self.containingscenario=containingscenario
		self.currentchemical=currentchemical
		self.sendingcompartment=sendingcompartment
		self.receivingcompartment=receivingcompartment
		self.category='bioenergetic fish model'
		self.chemicalcategory='all'
		self.doestransformchemical='False'
		self.transportchemical='True'
		self.enabled='True'
		self.isdefaultforcategory='True'
		self.mate='<unset>'
		self.receivingchemicalname='replaceme'
		self.receivingcompartmentcategory='fish | water column herbivore'
		self.sendingcompartmentcategory='insect | benthic invertebrate'
		self.sendingchemicalname='replaceme'
		self.dict_inputs=dict_inputs
		
	@property
	def transferfactor(self):
		try:
			r=self.receivingcompartment.populationsize * self.receivingcompartment.bw * 1 * self.receivingcompartment.fractiondietbenthicinvertebrate * self.receivingcompartment.foodingestionrate * self.receivingcompartment.chemical_assimilationefficiencyfromfood   / self.sendingcompartment.totalmass
		except:
			r=nan
		return (r)

class fish_bioenergetic_model_ingestion_of_benthic_invertebrate_by_water_column_omnivore_alginstid_2287:
	def __init__(self, constants,containingscenario,currentchemical,sendingcompartment, receivingcompartment,dict_inputs):
		self.name='fish bioenergetic model - ingestion of benthic invertebrate by water column omnivore(alginstid_2287)'
		self.constants=constants
		self.containingscenario=containingscenario
		self.currentchemical=currentchemical
		self.sendingcompartment=sendingcompartment
		self.receivingcompartment=receivingcompartment
		self.category='bioenergetic fish model'
		self.chemicalcategory='all'
		self.doestransformchemical='False'
		self.transportchemical='True'
		self.enabled='True'
		self.isdefaultforcategory='True'
		self.mate='<unset>'
		self.receivingchemicalname='replaceme'
		self.receivingcompartmentcategory='fish | water column omnivore'
		self.sendingcompartmentcategory='insect | benthic invertebrate'
		self.sendingchemicalname='replaceme'
		self.dict_inputs=dict_inputs
		
	@property
	def transferfactor(self):
		try:
			r=self.receivingcompartment.populationsize * self.receivingcompartment.bw * 1 * self.receivingcompartment.fractiondietbenthicinvertebrate * self.receivingcompartment.foodingestionrate * self.receivingcompartment.chemical_assimilationefficiencyfromfood   / self.sendingcompartment.totalmass
		except:
			r=nan
		return (r)

class fish_bioenergetic_model_ingestion_of_benthic_omnivore_by_benthic_carnivore_alginstid_1447:
	def __init__(self, constants,containingscenario,currentchemical,sendingcompartment, receivingcompartment,dict_inputs):
		self.name='fish bioenergetic model - ingestion of benthic omnivore by benthic carnivore(alginstid_1447)'
		self.constants=constants
		self.containingscenario=containingscenario
		self.currentchemical=currentchemical
		self.sendingcompartment=sendingcompartment
		self.receivingcompartment=receivingcompartment
		self.category='bioenergetic fish model'
		self.chemicalcategory='all'
		self.doestransformchemical='False'
		self.transportchemical='True'
		self.enabled='True'
		self.isdefaultforcategory='True'
		self.mate='<unset>'
		self.receivingchemicalname='replaceme'
		self.receivingcompartmentcategory='fish | benthic carnivore'
		self.sendingcompartmentcategory='fish | benthic omnivore'
		self.sendingchemicalname='replaceme'
		self.dict_inputs=dict_inputs
		
	@property
	def transferfactor(self):
		try:
			r=self.receivingcompartment.populationsize * self.receivingcompartment.bw * 1 * self.receivingcompartment.fractiondietfishbenthicomnivore * self.receivingcompartment.foodingestionrate * self.receivingcompartment.chemical_assimilationefficiencyfromfood/ self.sendingcompartment.totalmass
		except:
			r=nan
		return (r)

class fish_bioenergetic_model_ingestion_of_benthic_omnivore_by_water_column_carnivore_alginstid_2250:
	def __init__(self, constants,containingscenario,currentchemical,sendingcompartment, receivingcompartment,dict_inputs):
		self.name='fish bioenergetic model - ingestion of benthic omnivore by water column carnivore(alginstid_2250)'
		self.constants=constants
		self.containingscenario=containingscenario
		self.currentchemical=currentchemical
		self.sendingcompartment=sendingcompartment
		self.receivingcompartment=receivingcompartment
		self.category='bioenergetic fish model'
		self.chemicalcategory='all'
		self.doestransformchemical='False'
		self.transportchemical='True'
		self.enabled='True'
		self.isdefaultforcategory='True'
		self.mate='<unset>'
		self.receivingchemicalname='replaceme'
		self.receivingcompartmentcategory='fish | water column carnivore'
		self.sendingcompartmentcategory='fish | benthic omnivore'
		self.sendingchemicalname='replaceme'
		self.dict_inputs=dict_inputs
		
	@property
	def transferfactor(self):
		try:
			r=self.receivingcompartment.populationsize * self.receivingcompartment.bw * 1 * self.receivingcompartment.fractiondietfishbenthicomnivore * self.receivingcompartment.foodingestionrate * self.receivingcompartment.chemical_assimilationefficiencyfromfood/ self.sendingcompartment.totalmass
		except:
			r=nan
		return (r)

class fish_bioenergetic_model_ingestion_of_benthic_omnivore_by_water_column_omnivore_alginstid_2282:
	def __init__(self, constants,containingscenario,currentchemical,sendingcompartment, receivingcompartment,dict_inputs):
		self.name='fish bioenergetic model - ingestion of benthic omnivore by water column omnivore(alginstid_2282)'
		self.constants=constants
		self.containingscenario=containingscenario
		self.currentchemical=currentchemical
		self.sendingcompartment=sendingcompartment
		self.receivingcompartment=receivingcompartment
		self.category='bioenergetic fish model'
		self.chemicalcategory='all'
		self.doestransformchemical='False'
		self.transportchemical='True'
		self.enabled='True'
		self.isdefaultforcategory='True'
		self.mate='<unset>'
		self.receivingchemicalname='replaceme'
		self.receivingcompartmentcategory='fish | water column omnivore'
		self.sendingcompartmentcategory='fish | benthic omnivore'
		self.sendingchemicalname='replaceme'
		self.dict_inputs=dict_inputs
		
	@property
	def transferfactor(self):
		try:
			r=self.receivingcompartment.populationsize * self.receivingcompartment.bw * 1 * self.receivingcompartment.fractiondietfishbenthicomnivore * self.receivingcompartment.foodingestionrate * self.receivingcompartment.chemical_assimilationefficiencyfromfood/ self.sendingcompartment.totalmass
		except:
			r=nan
		return (r)

class fish_bioenergetic_model_ingestion_of_macrophyte_by_water_column_herbivore_alginstid_1646:
	def __init__(self, constants,containingscenario,currentchemical,sendingcompartment, receivingcompartment,dict_inputs):
		self.name='fish bioenergetic model - ingestion of macrophyte by water column herbivore(alginstid_1646)'
		self.constants=constants
		self.containingscenario=containingscenario
		self.currentchemical=currentchemical
		self.sendingcompartment=sendingcompartment
		self.receivingcompartment=receivingcompartment
		self.category='bioenergetic fish model'
		self.chemicalcategory='all'
		self.doestransformchemical='False'
		self.transportchemical='True'
		self.enabled='True'
		self.isdefaultforcategory='True'
		self.mate='<unset>'
		self.receivingchemicalname='replaceme'
		self.receivingcompartmentcategory='fish | water column herbivore'
		self.sendingcompartmentcategory='aquatic plant | macrophyte'
		self.sendingchemicalname='replaceme'
		self.dict_inputs=dict_inputs
		
	@property
	def transferfactor(self):
		try:
			r=self.receivingcompartment.populationsize * self.receivingcompartment.bw * 1 * self.receivingcompartment.fractiondietmacrophyte * self.receivingcompartment.foodingestionrate * self.receivingcompartment.chemical_assimilationefficiencyfromfood / self.sendingcompartment.totalmass
		except:
			r=nan
		return (r)

class fish_bioenergetic_model_ingestion_of_macrophyte_by_water_column_omnivore_alginstid_1655:
	def __init__(self, constants,containingscenario,currentchemical,sendingcompartment, receivingcompartment,dict_inputs):
		self.name='fish bioenergetic model - ingestion of macrophyte by water column omnivore(alginstid_1655)'
		self.constants=constants
		self.containingscenario=containingscenario
		self.currentchemical=currentchemical
		self.sendingcompartment=sendingcompartment
		self.receivingcompartment=receivingcompartment
		self.category='bioenergetic fish model'
		self.chemicalcategory='all'
		self.doestransformchemical='False'
		self.transportchemical='True'
		self.enabled='True'
		self.isdefaultforcategory='True'
		self.mate='<unset>'
		self.receivingchemicalname='replaceme'
		self.receivingcompartmentcategory='fish | water column omnivore'
		self.sendingcompartmentcategory='aquatic plant | macrophyte'
		self.sendingchemicalname='replaceme'
		self.dict_inputs=dict_inputs
		
	@property
	def transferfactor(self):
		try:
			r=self.receivingcompartment.populationsize * self.receivingcompartment.bw * 1 * self.receivingcompartment.fractiondietmacrophyte * self.receivingcompartment.foodingestionrate * self.receivingcompartment.chemical_assimilationefficiencyfromfood / self.sendingcompartment.totalmass
		except:
			r=nan
		return (r)

class fish_bioenergetic_model_ingestion_of_water_column_carnivore_by_benthic_carnivore_alginstid_2158:
	def __init__(self, constants,containingscenario,currentchemical,sendingcompartment, receivingcompartment,dict_inputs):
		self.name='fish bioenergetic model - ingestion of water column carnivore by benthic carnivore(alginstid_2158)'
		self.constants=constants
		self.containingscenario=containingscenario
		self.currentchemical=currentchemical
		self.sendingcompartment=sendingcompartment
		self.receivingcompartment=receivingcompartment
		self.category='bioenergetic fish model'
		self.chemicalcategory='all'
		self.doestransformchemical='False'
		self.transportchemical='True'
		self.enabled='True'
		self.isdefaultforcategory='True'
		self.mate='<unset>'
		self.receivingchemicalname='replaceme'
		self.receivingcompartmentcategory='fish | benthic carnivore'
		self.sendingcompartmentcategory='fish | water column carnivore'
		self.sendingchemicalname='replaceme'
		self.dict_inputs=dict_inputs
		
	@property
	def transferfactor(self):
		try:
			r=self.receivingcompartment.populationsize * self.receivingcompartment.bw * 1 * self.receivingcompartment.fractiondietfishcarnivore * self.receivingcompartment.foodingestionrate * self.receivingcompartment.chemical_assimilationefficiencyfromfood  / self.sendingcompartment.totalmass
		except:
			r=nan
		return (r)

class fish_bioenergetic_model_ingestion_of_water_column_carnivore_by_benthic_omnivore_alginstid_2175:
	def __init__(self, constants,containingscenario,currentchemical,sendingcompartment, receivingcompartment,dict_inputs):
		self.name='fish bioenergetic model - ingestion of water column carnivore by benthic omnivore(alginstid_2175)'
		self.constants=constants
		self.containingscenario=containingscenario
		self.currentchemical=currentchemical
		self.sendingcompartment=sendingcompartment
		self.receivingcompartment=receivingcompartment
		self.category='bioenergetic fish model'
		self.chemicalcategory='all'
		self.doestransformchemical='False'
		self.transportchemical='True'
		self.enabled='True'
		self.isdefaultforcategory='True'
		self.mate='<unset>'
		self.receivingchemicalname='replaceme'
		self.receivingcompartmentcategory='fish | benthic omnivore'
		self.sendingcompartmentcategory='fish | water column carnivore'
		self.sendingchemicalname='replaceme'
		self.dict_inputs=dict_inputs
		
	@property
	def transferfactor(self):
		try:
			r=self.receivingcompartment.populationsize * self.receivingcompartment.bw * 1 * self.receivingcompartment.fractiondietfishcarnivore * self.receivingcompartment.foodingestionrate * self.receivingcompartment.chemical_assimilationefficiencyfromfood  / self.sendingcompartment.totalmass
		except:
			r=nan
		return (r)

class fish_bioenergetic_model_ingestion_of_water_column_carnivore_by_water_column_omnivore_alginstid_1618:
	def __init__(self, constants,containingscenario,currentchemical,sendingcompartment, receivingcompartment,dict_inputs):
		self.name='fish bioenergetic model - ingestion of water column carnivore by water column omnivore(alginstid_1618)'
		self.constants=constants
		self.containingscenario=containingscenario
		self.currentchemical=currentchemical
		self.sendingcompartment=sendingcompartment
		self.receivingcompartment=receivingcompartment
		self.category='bioenergetic fish model'
		self.chemicalcategory='all'
		self.doestransformchemical='False'
		self.transportchemical='True'
		self.enabled='True'
		self.isdefaultforcategory='True'
		self.mate='<unset>'
		self.receivingchemicalname='replaceme'
		self.receivingcompartmentcategory='fish | water column omnivore'
		self.sendingcompartmentcategory='fish | water column carnivore'
		self.sendingchemicalname='replaceme'
		self.dict_inputs=dict_inputs
		
	@property
	def transferfactor(self):
		try:
			r=self.receivingcompartment.populationsize * self.receivingcompartment.bw * 1 * self.receivingcompartment.fractiondietfishcarnivore * self.receivingcompartment.foodingestionrate * self.receivingcompartment.chemical_assimilationefficiencyfromfood  / self.sendingcompartment.totalmass
		except:
			r=nan
		return (r)

class fish_bioenergetic_model_ingestion_of_water_column_herbivore_by_benthic_carnivore_alginstid_2163:
	def __init__(self, constants,containingscenario,currentchemical,sendingcompartment, receivingcompartment,dict_inputs):
		self.name='fish bioenergetic model - ingestion of water column herbivore by benthic carnivore(alginstid_2163)'
		self.constants=constants
		self.containingscenario=containingscenario
		self.currentchemical=currentchemical
		self.sendingcompartment=sendingcompartment
		self.receivingcompartment=receivingcompartment
		self.category='bioenergetic fish model'
		self.chemicalcategory='all'
		self.doestransformchemical='False'
		self.transportchemical='True'
		self.enabled='True'
		self.isdefaultforcategory='True'
		self.mate='<unset>'
		self.receivingchemicalname='replaceme'
		self.receivingcompartmentcategory='fish | benthic carnivore'
		self.sendingcompartmentcategory='fish | water column herbivore'
		self.sendingchemicalname='replaceme'
		self.dict_inputs=dict_inputs
		
	@property
	def transferfactor(self):
		try:
			r=self.receivingcompartment.populationsize * self.receivingcompartment.bw * 1 * self.receivingcompartment.fractiondietfishherbivore * self.receivingcompartment.foodingestionrate * self.receivingcompartment.chemical_assimilationefficiencyfromfood / self.sendingcompartment.totalmass
		except:
			r=nan
		return (r)

class fish_bioenergetic_model_ingestion_of_water_column_herbivore_by_benthic_omnivore_alginstid_2180:
	def __init__(self, constants,containingscenario,currentchemical,sendingcompartment, receivingcompartment,dict_inputs):
		self.name='fish bioenergetic model - ingestion of water column herbivore by benthic omnivore(alginstid_2180)'
		self.constants=constants
		self.containingscenario=containingscenario
		self.currentchemical=currentchemical
		self.sendingcompartment=sendingcompartment
		self.receivingcompartment=receivingcompartment
		self.category='bioenergetic fish model'
		self.chemicalcategory='all'
		self.doestransformchemical='False'
		self.transportchemical='True'
		self.enabled='True'
		self.isdefaultforcategory='True'
		self.mate='<unset>'
		self.receivingchemicalname='replaceme'
		self.receivingcompartmentcategory='fish | benthic omnivore'
		self.sendingcompartmentcategory='fish | water column herbivore'
		self.sendingchemicalname='replaceme'
		self.dict_inputs=dict_inputs
		
	@property
	def transferfactor(self):
		try:
			r=self.receivingcompartment.populationsize * self.receivingcompartment.bw * 1 * self.receivingcompartment.fractiondietfishherbivore * self.receivingcompartment.foodingestionrate * self.receivingcompartment.chemical_assimilationefficiencyfromfood / self.sendingcompartment.totalmass
		except:
			r=nan
		return (r)

class fish_bioenergetic_model_ingestion_of_water_column_herbivore_by_water_column_carnivore_alginstid_1600:
	def __init__(self, constants,containingscenario,currentchemical,sendingcompartment, receivingcompartment,dict_inputs):
		self.name='fish bioenergetic model - ingestion of water column herbivore by water column carnivore(alginstid_1600)'
		self.constants=constants
		self.containingscenario=containingscenario
		self.currentchemical=currentchemical
		self.sendingcompartment=sendingcompartment
		self.receivingcompartment=receivingcompartment
		self.category='bioenergetic fish model'
		self.chemicalcategory='all'
		self.doestransformchemical='False'
		self.transportchemical='True'
		self.enabled='True'
		self.isdefaultforcategory='True'
		self.mate='<unset>'
		self.receivingchemicalname='replaceme'
		self.receivingcompartmentcategory='fish | water column carnivore'
		self.sendingcompartmentcategory='fish | water column herbivore'
		self.sendingchemicalname='replaceme'
		self.dict_inputs=dict_inputs
		
	@property
	def transferfactor(self):
		try:
			r=self.receivingcompartment.populationsize * self.receivingcompartment.bw * 1 * self.receivingcompartment.fractiondietfishherbivore * self.receivingcompartment.foodingestionrate * self.receivingcompartment.chemical_assimilationefficiencyfromfood / self.sendingcompartment.totalmass
		except:
			r=nan
		return (r)

class fish_bioenergetic_model_ingestion_of_water_column_herbivore_by_water_column_omnivore_alginstid_1638:
	def __init__(self, constants,containingscenario,currentchemical,sendingcompartment, receivingcompartment,dict_inputs):
		self.name='fish bioenergetic model - ingestion of water column herbivore by water column omnivore(alginstid_1638)'
		self.constants=constants
		self.containingscenario=containingscenario
		self.currentchemical=currentchemical
		self.sendingcompartment=sendingcompartment
		self.receivingcompartment=receivingcompartment
		self.category='bioenergetic fish model'
		self.chemicalcategory='all'
		self.doestransformchemical='False'
		self.transportchemical='True'
		self.enabled='True'
		self.isdefaultforcategory='True'
		self.mate='<unset>'
		self.receivingchemicalname='replaceme'
		self.receivingcompartmentcategory='fish | water column omnivore'
		self.sendingcompartmentcategory='fish | water column herbivore'
		self.sendingchemicalname='replaceme'
		self.dict_inputs=dict_inputs
		
	@property
	def transferfactor(self):
		try:
			r=self.receivingcompartment.populationsize * self.receivingcompartment.bw * 1 * self.receivingcompartment.fractiondietfishherbivore * self.receivingcompartment.foodingestionrate * self.receivingcompartment.chemical_assimilationefficiencyfromfood / self.sendingcompartment.totalmass
		except:
			r=nan
		return (r)

class fish_bioenergetic_model_ingestion_of_water_column_omnivore_by_benthic_carnivore_alginstid_2168:
	def __init__(self, constants,containingscenario,currentchemical,sendingcompartment, receivingcompartment,dict_inputs):
		self.name='fish bioenergetic model - ingestion of water column omnivore by benthic carnivore(alginstid_2168)'
		self.constants=constants
		self.containingscenario=containingscenario
		self.currentchemical=currentchemical
		self.sendingcompartment=sendingcompartment
		self.receivingcompartment=receivingcompartment
		self.category='bioenergetic fish model'
		self.chemicalcategory='all'
		self.doestransformchemical='False'
		self.transportchemical='True'
		self.enabled='True'
		self.isdefaultforcategory='True'
		self.mate='<unset>'
		self.receivingchemicalname='replaceme'
		self.receivingcompartmentcategory='fish | benthic carnivore'
		self.sendingcompartmentcategory='fish | water column omnivore'
		self.sendingchemicalname='replaceme'
		self.dict_inputs=dict_inputs
		
	@property
	def transferfactor(self):
		try:
			r=self.receivingcompartment.populationsize * self.receivingcompartment.bw * 1 * self.receivingcompartment.fractiondietfishomnivore * self.receivingcompartment.foodingestionrate * self.receivingcompartment.chemical_assimilationefficiencyfromfood / self.sendingcompartment.totalmass
		except:
			r=nan
		return (r)

class fish_bioenergetic_model_ingestion_of_water_column_omnivore_by_benthic_omnivore_alginstid_2185:
	def __init__(self, constants,containingscenario,currentchemical,sendingcompartment, receivingcompartment,dict_inputs):
		self.name='fish bioenergetic model - ingestion of water column omnivore by benthic omnivore(alginstid_2185)'
		self.constants=constants
		self.containingscenario=containingscenario
		self.currentchemical=currentchemical
		self.sendingcompartment=sendingcompartment
		self.receivingcompartment=receivingcompartment
		self.category='bioenergetic fish model'
		self.chemicalcategory='all'
		self.doestransformchemical='False'
		self.transportchemical='True'
		self.enabled='True'
		self.isdefaultforcategory='True'
		self.mate='<unset>'
		self.receivingchemicalname='replaceme'
		self.receivingcompartmentcategory='fish | benthic omnivore'
		self.sendingcompartmentcategory='fish | water column omnivore'
		self.sendingchemicalname='replaceme'
		self.dict_inputs=dict_inputs
		
	@property
	def transferfactor(self):
		try:
			r=self.receivingcompartment.populationsize * self.receivingcompartment.bw * 1 * self.receivingcompartment.fractiondietfishomnivore * self.receivingcompartment.foodingestionrate * self.receivingcompartment.chemical_assimilationefficiencyfromfood / self.sendingcompartment.totalmass
		except:
			r=nan
		return (r)

class fish_bioenergetic_model_ingestion_of_water_column_omnivore_by_water_column_carnivore_alginstid_1610:
	def __init__(self, constants,containingscenario,currentchemical,sendingcompartment, receivingcompartment,dict_inputs):
		self.name='fish bioenergetic model - ingestion of water column omnivore by water column carnivore(alginstid_1610)'
		self.constants=constants
		self.containingscenario=containingscenario
		self.currentchemical=currentchemical
		self.sendingcompartment=sendingcompartment
		self.receivingcompartment=receivingcompartment
		self.category='bioenergetic fish model'
		self.chemicalcategory='all'
		self.doestransformchemical='False'
		self.transportchemical='True'
		self.enabled='True'
		self.isdefaultforcategory='True'
		self.mate='<unset>'
		self.receivingchemicalname='replaceme'
		self.receivingcompartmentcategory='fish | water column carnivore'
		self.sendingcompartmentcategory='fish | water column omnivore'
		self.sendingchemicalname='replaceme'
		self.dict_inputs=dict_inputs
		
	@property
	def transferfactor(self):
		try:
			r=self.receivingcompartment.populationsize * self.receivingcompartment.bw * 1 * self.receivingcompartment.fractiondietfishomnivore * self.receivingcompartment.foodingestionrate * self.receivingcompartment.chemical_assimilationefficiencyfromfood / self.sendingcompartment.totalmass
		except:
			r=nan
		return (r)

class fish_bioenergetic_model_ingestion_of_zooplankton_by_water_column_herbivore:
	def __init__(self, constants,containingscenario,currentchemical,sendingcompartment, receivingcompartment,dict_inputs):
		self.name='fish bioenergetic model - ingestion of zooplankton by water column herbivore'
		self.constants=constants
		self.containingscenario=containingscenario
		self.currentchemical=currentchemical
		self.sendingcompartment=sendingcompartment
		self.receivingcompartment=receivingcompartment
		self.category='bioenergetic fish model'
		self.chemicalcategory='all'
		self.doestransformchemical='False'
		self.transportchemical='True'
		self.enabled='True'
		self.isdefaultforcategory='True'
		self.mate='<unset>'
		self.receivingchemicalname='replaceme'
		self.receivingcompartmentcategory='fish | water column herbivore'
		self.sendingcompartmentcategory='invertebrate | zooplankton'
		self.sendingchemicalname='replaceme'
		self.dict_inputs=dict_inputs
		
	@property
	def transferfactor(self):
		try:
			r=self.receivingcompartment.populationsize * self.receivingcompartment.bw * 1 * self.receivingcompartment.fractiondietzooplankton * self.receivingcompartment.foodingestionrate * self.receivingcompartment.chemical_assimilationefficiencyfromplankton / (self.sendingcompartment.totalmass)
		except:
			r=nan
		return (r)

class methylation_hg2_mhg_in_abiotic_media_rate_is_input_alginstid_1891:
	def __init__(self, constants,containingscenario,currentchemical,sendingcompartment, receivingcompartment,dict_inputs):
		self.name='methylation(hg2 -> mhg) in abiotic media, rate is input(alginstid_1891)'
		self.constants=constants
		self.containingscenario=containingscenario
		self.currentchemical=currentchemical
		self.sendingcompartment=sendingcompartment
		self.receivingcompartment=receivingcompartment
		self.category='transformation'
		self.chemicalcategory='<unset>'
		self.doestransformchemical='True'
		self.transportchemical='False'
		self.enabled='True'
		self.isdefaultforcategory='True'
		self.mate='<unset>'
		self.receivingchemicalname='methylmercury'
		self.receivingcompartmentcategory='abiotic'
		self.sendingcompartmentcategory='abiotic'
		self.sendingchemicalname='divalent mercury'
		self.dict_inputs=dict_inputs
		
	@property
	def compartmentrelationship(self):
		return ("same")
	
	@property
	def transferfactor(self):
		try:
			r=self.sendingcompartment.chemical_methylationrate
		except:
			r=nan
		return (r)

class oxidation_hg0_hg2_in_abiotic_media_rate_is_input_alginstid_1894:
	def __init__(self, constants,containingscenario,currentchemical,sendingcompartment, receivingcompartment,dict_inputs):
		self.name='oxidation(hg0 -> hg2) in abiotic media, rate is input(alginstid_1894)'
		self.constants=constants
		self.containingscenario=containingscenario
		self.currentchemical=currentchemical
		self.sendingcompartment=sendingcompartment
		self.receivingcompartment=receivingcompartment
		self.category='transformation'
		self.chemicalcategory='<unset>'
		self.doestransformchemical='True'
		self.transportchemical='False'
		self.enabled='True'
		self.isdefaultforcategory='True'
		self.mate='<unset>'
		self.receivingchemicalname='divalent mercury'
		self.receivingcompartmentcategory='abiotic'
		self.sendingcompartmentcategory='abiotic'
		self.sendingchemicalname='elemental mercury'
		self.dict_inputs=dict_inputs
		
	@property
	def compartmentrelationship(self):
		return ("same")
	
	@property
	def transferfactor(self):
		try:
			r=self.sendingcompartment.chemical_oxidationrate
		except:
			r=nan
		return (r)

class oxidation_hg0_hg2_in_fish_alginstid_1443:
	def __init__(self, constants,containingscenario,currentchemical,sendingcompartment, receivingcompartment,dict_inputs):
		self.name='oxidation(hg0 -> hg2) in fish(alginstid_1443)'
		self.constants=constants
		self.containingscenario=containingscenario
		self.currentchemical=currentchemical
		self.sendingcompartment=sendingcompartment
		self.receivingcompartment=receivingcompartment
		self.category='transformation'
		self.chemicalcategory='<unset>'
		self.doestransformchemical='True'
		self.transportchemical='False'
		self.enabled='True'
		self.isdefaultforcategory='True'
		self.mate='<unset>'
		self.receivingchemicalname='divalent mercury'
		self.receivingcompartmentcategory='fish'
		self.sendingcompartmentcategory='fish'
		self.sendingchemicalname='elemental mercury'
		self.dict_inputs=dict_inputs
		
	@property
	def compartmentrelationship(self):
		return ("same")
	
	@property
	def transferfactor(self):
		try:
			r=self.sendingcompartment.chemical_oxidationrate
		except:
			r=nan
		return (r)

class oxidation_hg0_hg2_in_macrophytes:
	def __init__(self, constants,containingscenario,currentchemical,sendingcompartment, receivingcompartment,dict_inputs):
		self.name='oxidation(hg0 -> hg2) in macrophytes'
		self.constants=constants
		self.containingscenario=containingscenario
		self.currentchemical=currentchemical
		self.sendingcompartment=sendingcompartment
		self.receivingcompartment=receivingcompartment
		self.category='transformation'
		self.chemicalcategory='<unset>'
		self.doestransformchemical='True'
		self.transportchemical='False'
		self.enabled='True'
		self.isdefaultforcategory='True'
		self.mate='<unset>'
		self.receivingchemicalname='divalent mercury'
		self.receivingcompartmentcategory='aquatic plant | macrophyte'
		self.sendingcompartmentcategory='aquatic plant | macrophyte'
		self.sendingchemicalname='elemental mercury'
		self.dict_inputs=dict_inputs
		
	@property
	def compartmentrelationship(self):
		return ("same")
	
	@property
	def transferfactor(self):
		try:
			r=self.sendingcompartment.chemical_oxidationrate
		except:
			r=nan
		return (r)

class reduction_hg2_hg0_in_abiotic_media_rate_is_input_alginstid_1893:
	def __init__(self, constants,containingscenario,currentchemical,sendingcompartment, receivingcompartment,dict_inputs):
		self.name='reduction(hg2 -> hg0) in abiotic media, rate is input(alginstid_1893)'
		self.constants=constants
		self.containingscenario=containingscenario
		self.currentchemical=currentchemical
		self.sendingcompartment=sendingcompartment
		self.receivingcompartment=receivingcompartment
		self.category='transformation'
		self.chemicalcategory='<unset>'
		self.doestransformchemical='True'
		self.transportchemical='False'
		self.enabled='True'
		self.isdefaultforcategory='True'
		self.mate='<unset>'
		self.receivingchemicalname='elemental mercury'
		self.receivingcompartmentcategory='abiotic'
		self.sendingcompartmentcategory='abiotic'
		self.sendingchemicalname='divalent mercury'
		self.dict_inputs=dict_inputs
		
	@property
	def compartmentrelationship(self):
		return ("same")
	
	@property
	def transferfactor(self):
		try:
			r=self.sendingcompartment.chemical_reductionrate
		except:
			r=nan
		return (r)

class reduction_hg2_hg0_in_fish_alginstid_1444:
	def __init__(self, constants,containingscenario,currentchemical,sendingcompartment, receivingcompartment,dict_inputs):
		self.name='reduction(hg2 -> hg0) in fish(alginstid_1444)'
		self.constants=constants
		self.containingscenario=containingscenario
		self.currentchemical=currentchemical
		self.sendingcompartment=sendingcompartment
		self.receivingcompartment=receivingcompartment
		self.category='transformation'
		self.chemicalcategory='<unset>'
		self.doestransformchemical='True'
		self.transportchemical='False'
		self.enabled='True'
		self.isdefaultforcategory='True'
		self.mate='<unset>'
		self.receivingchemicalname='elemental mercury'
		self.receivingcompartmentcategory='fish'
		self.sendingcompartmentcategory='fish'
		self.sendingchemicalname='divalent mercury'
		self.dict_inputs=dict_inputs
		
	@property
	def compartmentrelationship(self):
		return ("same")
	
	@property
	def transferfactor(self):
		try:
			r=self.sendingcompartment.chemical_reductionrate
		except:
			r=nan
		return (r)

class resuspension_from_sediment_to_surface_water_general_alginstid_2190:
	def __init__(self, constants,containingscenario,currentchemical,sendingcompartment, receivingcompartment,dict_inputs):
		self.name='resuspension from sediment to surface water, general(alginstid_2190)'
		self.constants=constants
		self.containingscenario=containingscenario
		self.currentchemical=currentchemical
		self.sendingcompartment=sendingcompartment
		self.receivingcompartment=receivingcompartment
		self.category='advection'
		self.chemicalcategory='all'
		self.doestransformchemical='False'
		self.transportchemical='True'
		self.enabled='True'
		self.isdefaultforcategory='True'
		self.mate='<unset>'
		self.receivingchemicalname='replaceme'
		self.receivingcompartmentcategory='abiotic | surface water | surface water - default'
		self.sendingcompartmentcategory='abiotic | sediment | sediment - default'
		self.sendingchemicalname='replaceme'
		self.dict_inputs=dict_inputs
		
	@property
	def compartmentrelationship(self):
		return ("sender_below")
	
	@property
	def solidarealphasevelocity(self):
		return (self.sendingcompartment.sedimentresuspensionrate_m3_m2_day)
	
	@property
	def transferfactor(self):
		try:
			r=self.solidarealphasevelocity * (self.sendingcompartment.chemical_fractionmass_sorbed/self.sendingcompartment.volumefraction_solid) * (check_neighbor(self.sendingcompartment,self.receivingcompartment,self.dict_inputs).is_neighbor()[1]) / self.sendingcompartment.volume
		except:
			r=nan
		return (r)

class sediment_burial_from_sediment_to_sediment_burial_sink_zero_net_deposition_general_alginstid_4135:
	def __init__(self, constants,containingscenario,currentchemical,sendingcompartment, receivingcompartment,dict_inputs):
		self.name='sediment burial from sediment to sediment burial sink, zero net deposition, general(alginstid_4135)'
		self.constants=constants
		self.containingscenario=containingscenario
		self.currentchemical=currentchemical
		self.sendingcompartment=sendingcompartment
		self.receivingcompartment=receivingcompartment
		self.category='advection'
		self.chemicalcategory='all'
		self.doestransformchemical='False'
		self.transportchemical='True'
		self.enabled='True'
		self.isdefaultforcategory='True'
		self.mate='<unset>'
		self.receivingchemicalname='replaceme'
		self.receivingcompartmentcategory='sink | abiotic | sediment | sediment - default'
		self.sendingcompartmentcategory='abiotic | sediment | sediment - default'
		self.sendingchemicalname='replaceme'
		self.dict_inputs=dict_inputs
		
	@property
	def compartmentrelationship(self):
		return ("sender_above")
	
	@property
	def solidarealphasevelocity(self):
		return (self.sendingcompartment.sedimentburialratetohavezeronetdeposition_m3_m2_day)
	
	@property
	def transferfactor(self):
		try:
			r=self.solidarealphasevelocity * (self.sendingcompartment.chemical_fractionmass_sorbed/self.sendingcompartment.volumefraction_solid) * (check_neighbor(self.sendingcompartment,self.receivingcompartment,self.dict_inputs).is_neighbor()[1]) / self.sendingcompartment.volume
		except:
			r=nan
		return (r)

class sediment_deposition_from_surface_water_to_sediment_general_alginstid_2139:
	def __init__(self, constants,containingscenario,currentchemical,sendingcompartment, receivingcompartment,dict_inputs):
		self.name='sediment deposition from surface water to sediment, general(alginstid_2139)'
		self.constants=constants
		self.containingscenario=containingscenario
		self.currentchemical=currentchemical
		self.sendingcompartment=sendingcompartment
		self.receivingcompartment=receivingcompartment
		self.category='advection'
		self.chemicalcategory='all'
		self.doestransformchemical='False'
		self.transportchemical='True'
		self.enabled='True'
		self.isdefaultforcategory='True'
		self.mate='<unset>'
		self.receivingchemicalname='replaceme'
		self.receivingcompartmentcategory='abiotic | sediment | sediment - default'
		self.sendingcompartmentcategory='abiotic | surface water | surface water - default'
		self.sendingchemicalname='replaceme'
		self.dict_inputs=dict_inputs
		
	@property
	def compartmentrelationship(self):
		return ("sender_above")
	
	@property
	def solidarealphasevelocity(self):
		return (self.sendingcompartment.sedimentdepositionrate_m3_m2_day)
	
	@property
	def transferfactor(self):
		try:
			r=self.solidarealphasevelocity * (self.sendingcompartment.chemical_fractionmass_sorbed/self.sendingcompartment.volumefraction_solid) * (check_neighbor(self.sendingcompartment,self.receivingcompartment,self.dict_inputs).is_neighbor()[1]) / self.sendingcompartment.volume
		except:
			r=nan
		return (r)

class time_dependent_partition_from_benthic_invertebrate_to_sediment_alginstid_1433:
	def __init__(self, constants,containingscenario,currentchemical,sendingcompartment, receivingcompartment,dict_inputs):
		self.name='time-dependent partition from benthic invertebrate to sediment(alginstid_1433)'
		self.constants=constants
		self.containingscenario=containingscenario
		self.currentchemical=currentchemical
		self.sendingcompartment=sendingcompartment
		self.receivingcompartment=receivingcompartment
		self.category='time-dependent partition'
		self.chemicalcategory='metals'
		self.doestransformchemical='False'
		self.transportchemical='True'
		self.enabled='True'
		self.isdefaultforcategory='True'
		self.mate='<unset>'
		self.receivingchemicalname='replaceme'
		self.receivingcompartmentcategory='abiotic | sediment | sediment - default'
		self.sendingcompartmentcategory='insect | benthic invertebrate'
		self.sendingchemicalname='replaceme'
		self.dict_inputs=dict_inputs
		
	@property
	def k1(self):
		return (-log(1 - self.sendingcompartment.chemical_sedimentpartitioning_alphaofequilibrium) / self.sendingcompartment.chemical_sedimentpartitioning_timetoreachalphaofequilibrium)
	
	@property
	def k2(self):
		return (self.k1 * self.sendingcompartment.chemical_sedimentpartitioning_partitioncoefficient)
	
	@property
	def transferfactor(self):
		try:
			r=self.k1
		except:
			r=nan
		return (r)

class time_dependent_partition_from_macrophyte_to_surface_water_alginstid_1544_hg:
	def __init__(self, constants,containingscenario,currentchemical,sendingcompartment, receivingcompartment,dict_inputs):
		self.name='time-dependent partition from macrophyte to surface water(alginstid_1544),hg'
		self.constants=constants
		self.containingscenario=containingscenario
		self.currentchemical=currentchemical
		self.sendingcompartment=sendingcompartment
		self.receivingcompartment=receivingcompartment
		self.category='time-dependent partition'
		self.chemicalcategory='metals | mercury'
		self.doestransformchemical='False'
		self.transportchemical='True'
		self.enabled='True'
		self.isdefaultforcategory='True'
		self.mate='<unset>'
		self.receivingchemicalname='replaceme'
		self.receivingcompartmentcategory='abiotic | surface water | surface water - default'
		self.sendingcompartmentcategory='aquatic plant | macrophyte'
		self.sendingchemicalname='replaceme'
		self.dict_inputs=dict_inputs
		
	@property
	def k1(self):
		return (-log(1 - self.sendingcompartment.chemical_watercolumndissolvedpartitioning_alphaofequilibrium) / self.sendingcompartment.chemical_watercolumndissolvedpartitioning_timetoreachalphaofequilibrium)
	
	@property
	def k2(self):
		return (self.k1 * self.sendingcompartment.chemical_watercolumndissolvedpartitioning_partitioncoefficient)
	
	@property
	def transferfactor(self):
		try:
			r=self.k1
		except:
			r=nan
		return (r)

class time_dependent_partition_from_sediment_to_benthic_invertebrate_alginstid_1438:
	def __init__(self, constants,containingscenario,currentchemical,sendingcompartment, receivingcompartment,dict_inputs):
		self.name='time-dependent partition from sediment to benthic invertebrate(alginstid_1438)'
		self.constants=constants
		self.containingscenario=containingscenario
		self.currentchemical=currentchemical
		self.sendingcompartment=sendingcompartment
		self.receivingcompartment=receivingcompartment
		self.category='time-dependent partition'
		self.chemicalcategory='metals'
		self.doestransformchemical='False'
		self.transportchemical='True'
		self.enabled='True'
		self.isdefaultforcategory='True'
		self.mate='<unset>'
		self.receivingchemicalname='replaceme'
		self.receivingcompartmentcategory='insect | benthic invertebrate'
		self.sendingcompartmentcategory='abiotic | sediment | sediment - default'
		self.sendingchemicalname='replaceme'
		self.dict_inputs=dict_inputs
		
	@property
	def k1(self):
		return (-log(1 - self.receivingcompartment.chemical_sedimentpartitioning_alphaofequilibrium) / self.receivingcompartment.chemical_sedimentpartitioning_timetoreachalphaofequilibrium)
	
	@property
	def k2(self):
		return (self.k1 * self.receivingcompartment.chemical_sedimentpartitioning_partitioncoefficient)
	
	@property
	def transferfactor(self):
		try:
			r=self.k2 * self.receivingcompartment.totalmass / self.sendingcompartment.totalmass
		except:
			r=nan
		return (r)

class time_dependent_partition_from_surface_water_to_macrophyte_hg_alginstid_1549:
	def __init__(self, constants,containingscenario,currentchemical,sendingcompartment, receivingcompartment,dict_inputs):
		self.name='time-dependent partition from surface water to macrophyte, hg(alginstid_1549)'
		self.constants=constants
		self.containingscenario=containingscenario
		self.currentchemical=currentchemical
		self.sendingcompartment=sendingcompartment
		self.receivingcompartment=receivingcompartment
		self.category='time-dependent partition'
		self.chemicalcategory='metals | mercury'
		self.doestransformchemical='False'
		self.transportchemical='True'
		self.enabled='True'
		self.isdefaultforcategory='True'
		self.mate='<unset>'
		self.receivingchemicalname='replaceme'
		self.receivingcompartmentcategory='aquatic plant | macrophyte'
		self.sendingcompartmentcategory='abiotic | surface water | surface water - default'
		self.sendingchemicalname='replaceme'
		self.dict_inputs=dict_inputs
		
	@property
	def k1(self):
		return (-log(1 - self.receivingcompartment.chemical_watercolumndissolvedpartitioning_alphaofequilibrium) / self.receivingcompartment.chemical_watercolumndissolvedpartitioning_timetoreachalphaofequilibrium)
	
	@property
	def k2(self):
		return (self.k1 * self.receivingcompartment.chemical_watercolumndissolvedpartitioning_partitioncoefficient)
	
	@property
	def transferfactor(self):
		try:
			r=(self.k2 * self.receivingcompartment.totalmass * (self.sendingcompartment.chemical_fractionmass_dissolved/ self.sendingcompartment.volume))*(1/1000)
		except:
			r=nan
		return (r)

class waterflow_from_surface_water_to_surface_water_general_alginstid_3685:
	def __init__(self, constants,containingscenario,currentchemical,sendingcompartment, receivingcompartment,dict_inputs):
		self.name='waterflow from surface water to surface water, general(alginstid_3685)'
		self.constants=constants
		self.containingscenario=containingscenario
		self.currentchemical=currentchemical
		self.sendingcompartment=sendingcompartment
		self.receivingcompartment=receivingcompartment
		self.category='advection'
		self.chemicalcategory='all'
		self.doestransformchemical='False'
		self.transportchemical='True'
		self.enabled='True'
		self.isdefaultforcategory='True'
		self.mate='<unset>'
		self.receivingchemicalname='replaceme'
		self.receivingcompartmentcategory='abiotic | surface water | surface water - default'
		self.sendingcompartmentcategory='abiotic | surface water | surface water - default'
		self.sendingchemicalname='replaceme'
		self.dict_inputs=dict_inputs
		
	@property
	def transferfactor(self):
		try:
			r=float(self.dict_inputs['df_links'].loc[(self.dict_inputs['df_links']['receiving_compartment_new']==self.receivingcompartment.name)&(self.dict_inputs['df_links']['sending_compartment_new']==self.sendingcompartment.name)&(self.dict_inputs['df_links']['property']=='bulkwaterflowrate_volumetric'),'value'].values[0])/ self.sendingcompartment.volume
		except:
			r=nan
		return (r)

