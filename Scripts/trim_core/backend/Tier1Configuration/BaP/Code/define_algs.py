### note: this is an auto generated script
from find_neighbors import *
from numpy import sqrt,nan,log,exp
from util_functions import *
mfp=r"C:\Users\13963\OneDrive - ICF\Documents\RTR\PyTRIM\BaP\input_files"   # path to met file
mfn=r"MetData_streamlined.csv"   # met file name
default_rechargerate=1.42e-04


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

class degradation_reaction_sink_in_air_alginstid_4675:
	def __init__(self, constants,containingscenario,currentchemical,sendingcompartment, receivingcompartment,dict_inputs):
		self.name='degradation/reaction sink in air(alginstid_4675)'
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
		self.sendingcompartmentcategory='abiotic | air | air - default'
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

class degradation_reaction_sink_in_benthic_invertebrate_alginstid_4580:
	def __init__(self, constants,containingscenario,currentchemical,sendingcompartment, receivingcompartment,dict_inputs):
		self.name='degradation/reaction sink in benthic invertebrate(alginstid_4580)'
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
		self.sendingcompartmentcategory='insect | benthic invertebrate'
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

class degradation_reaction_sink_in_fish_alginstid_4570:
	def __init__(self, constants,containingscenario,currentchemical,sendingcompartment, receivingcompartment,dict_inputs):
		self.name='degradation/reaction sink in fish(alginstid_4570)'
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
		self.sendingcompartmentcategory='fish'
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

class degradation_reaction_sink_in_groundwater_alginstid_4145:
	def __init__(self, constants,containingscenario,currentchemical,sendingcompartment, receivingcompartment,dict_inputs):
		self.name='degradation/reaction sink in groundwater(alginstid_4145)'
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
		self.sendingcompartmentcategory='abiotic | soil | groundwater | groundwater - default'
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

class degradation_reaction_sink_in_leaf_alginstid_4165:
	def __init__(self, constants,containingscenario,currentchemical,sendingcompartment, receivingcompartment,dict_inputs):
		self.name='degradation/reaction sink in leaf(alginstid_4165)'
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
		self.sendingcompartmentcategory='terrestrial plant | leaf'
		self.sendingchemicalname='replaceme'
		self.dict_inputs=dict_inputs
		
	@property
	def compartmentrelationship(self):
		return ("in_same_volume_element")
	
	@property
	def transferfactor(self):
		try:
			r=self.sendingcompartment.allowexchange_forother * self.sendingcompartment.chemical_generaldegradationrate
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

class degradation_reaction_sink_in_root_zone_alginstid_4155:
	def __init__(self, constants,containingscenario,currentchemical,sendingcompartment, receivingcompartment,dict_inputs):
		self.name='degradation/reaction sink in root zone(alginstid_4155)'
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
		self.sendingcompartmentcategory='abiotic | soil | root zone | root zone - default'
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

class degradation_reaction_sink_in_root_alginstid_4175:
	def __init__(self, constants,containingscenario,currentchemical,sendingcompartment, receivingcompartment,dict_inputs):
		self.name='degradation/reaction sink in root(alginstid_4175)'
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
		self.sendingcompartmentcategory='terrestrial plant | root'
		self.sendingchemicalname='replaceme'
		self.dict_inputs=dict_inputs
		
	@property
	def compartmentrelationship(self):
		return ("in_same_volume_element")
	
	@property
	def transferfactor(self):
		try:
			r=self.sendingcompartment.allowexchange_forother * self.sendingcompartment.chemical_generaldegradationrate
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

class degradation_reaction_sink_in_stem_alginstid_4170:
	def __init__(self, constants,containingscenario,currentchemical,sendingcompartment, receivingcompartment,dict_inputs):
		self.name='degradation/reaction sink in stem(alginstid_4170)'
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
		self.sendingcompartmentcategory='terrestrial plant | stem'
		self.sendingchemicalname='replaceme'
		self.dict_inputs=dict_inputs
		
	@property
	def compartmentrelationship(self):
		return ("in_same_volume_element")
	
	@property
	def transferfactor(self):
		try:
			r=self.sendingcompartment.allowexchange_forother * self.sendingcompartment.chemical_generaldegradationrate
		except:
			r=nan
		return (r)

class degradation_reaction_sink_in_surface_soil_alginstid_4160:
	def __init__(self, constants,containingscenario,currentchemical,sendingcompartment, receivingcompartment,dict_inputs):
		self.name='degradation/reaction sink in surface soil(alginstid_4160)'
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
		self.sendingcompartmentcategory='abiotic | soil | surface soil | surface soil - default'
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

class degradation_reaction_sink_in_vadose_zone_alginstid_4150:
	def __init__(self, constants,containingscenario,currentchemical,sendingcompartment, receivingcompartment,dict_inputs):
		self.name='degradation/reaction sink in vadose zone(alginstid_4150)'
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
		self.sendingcompartmentcategory='abiotic | soil | vadose zone | vadose zone - default'
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

class demethylation_mhg_hg2_in_plant_leaves_rate_is_input_alginstid_1249:
	def __init__(self, constants,containingscenario,currentchemical,sendingcompartment, receivingcompartment,dict_inputs):
		self.name='demethylation(mhg -> hg2) in plant leaves, rate is input(alginstid_1249)'
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
		self.receivingcompartmentcategory='terrestrial plant | leaf'
		self.sendingcompartmentcategory='terrestrial plant | leaf'
		self.sendingchemicalname='methylmercury'
		self.dict_inputs=dict_inputs
		
	@property
	def compartmentrelationship(self):
		return ("same")
	
	@property
	def transferfactor(self):
		try:
			r=self.sendingcompartment.allowexchange_forother * self.sendingcompartment.chemical_demethylationrate
		except:
			r=nan
		return (r)

class demethylation_mhg_hg2_in_plant_stem_rate_is_input_alginstid_1271:
	def __init__(self, constants,containingscenario,currentchemical,sendingcompartment, receivingcompartment,dict_inputs):
		self.name='demethylation(mhg -> hg2) in plant stem, rate is input(alginstid_1271)'
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
		self.receivingcompartmentcategory='terrestrial plant | stem'
		self.sendingcompartmentcategory='terrestrial plant | stem'
		self.sendingchemicalname='methylmercury'
		self.dict_inputs=dict_inputs
		
	@property
	def compartmentrelationship(self):
		return ("same")
	
	@property
	def transferfactor(self):
		try:
			r=self.sendingcompartment.allowexchange_forother * self.sendingcompartment.chemical_demethylationrate
		except:
			r=nan
		return (r)

class diffusion_from_plant_leaf_to_air_hg0_default_bennett_1998_alginstid_4005:
	def __init__(self, constants,containingscenario,currentchemical,sendingcompartment, receivingcompartment,dict_inputs):
		self.name='diffusion from plant leaf to air, hg0, default (bennett 1998)(alginstid_4005)'
		self.constants=constants
		self.containingscenario=containingscenario
		self.currentchemical=currentchemical
		self.sendingcompartment=sendingcompartment
		self.receivingcompartment=receivingcompartment
		self.category='diffusion'
		self.chemicalcategory='<unset>'
		self.doestransformchemical='False'
		self.transportchemical='True'
		self.enabled='True'
		self.isdefaultforcategory='True'
		self.mate='<unset>'
		self.receivingchemicalname='elemental mercury'
		self.receivingcompartmentcategory='abiotic | air | air - default'
		self.sendingcompartmentcategory='terrestrial plant | leaf'
		self.sendingchemicalname='elemental mercury'
		self.dict_inputs=dict_inputs
		
	@property
	def compartmentrelationship(self):
		return ("above_or_below")
	
	@property
	def transferfactor(self):
		try:
			r=(self.sendingcompartment.allowexchange_forother * (check_neighbor(self.sendingcompartment,self.receivingcompartment,self.dict_inputs).is_neighbor()[1] )* (2*self.sendingcompartment.leafareaindex * self.sendingcompartment.chemical_totalcuticularconductance  + (self.sendingcompartment.isday_forother * self.sendingcompartment.chemical_totalstomatalconductance)) * (self.currentchemical.z_pureair/self.sendingcompartment.chemical_z_total)/self.sendingcompartment.volume ) if self.sendingcompartment.volume > 0 else 0
		except:
			r=nan
		return (r)

class diffusion_from_plant_leaf_to_air_mhg_default_bennett_1998_alginstid_4005:
	def __init__(self, constants,containingscenario,currentchemical,sendingcompartment, receivingcompartment,dict_inputs):
		self.name='diffusion from plant leaf to air, mhg, default (bennett 1998)(alginstid_4005)'
		self.constants=constants
		self.containingscenario=containingscenario
		self.currentchemical=currentchemical
		self.sendingcompartment=sendingcompartment
		self.receivingcompartment=receivingcompartment
		self.category='diffusion'
		self.chemicalcategory='<unset>'
		self.doestransformchemical='False'
		self.transportchemical='True'
		self.enabled='True'
		self.isdefaultforcategory='True'
		self.mate='<unset>'
		self.receivingchemicalname='methylmercury'
		self.receivingcompartmentcategory='abiotic | air | air - default'
		self.sendingcompartmentcategory='terrestrial plant | leaf'
		self.sendingchemicalname='methylmercury'
		self.dict_inputs=dict_inputs
		
	@property
	def compartmentrelationship(self):
		return ("above_or_below")
	
	@property
	def transferfactor(self):
		try:
			r=(self.sendingcompartment.allowexchange_forother * (check_neighbor(self.sendingcompartment,self.receivingcompartment,self.dict_inputs).is_neighbor()[1] )* (2*self.sendingcompartment.leafareaindex * self.sendingcompartment.chemical_totalcuticularconductance  + (self.sendingcompartment.isday_forother * self.sendingcompartment.chemical_totalstomatalconductance)) * (self.currentchemical.z_pureair/self.sendingcompartment.chemical_z_total)/self.sendingcompartment.volume ) if self.sendingcompartment.volume > 0 else 0
		except:
			r=nan
		return (r)

class diffusion_from_plant_leaf_to_air_organics_default_bennett_1998_alginstid_4005:
	def __init__(self, constants,containingscenario,currentchemical,sendingcompartment, receivingcompartment,dict_inputs):
		self.name='diffusion from plant leaf to air, organics, default (bennett 1998)(alginstid_4005)'
		self.constants=constants
		self.containingscenario=containingscenario
		self.currentchemical=currentchemical
		self.sendingcompartment=sendingcompartment
		self.receivingcompartment=receivingcompartment
		self.category='diffusion'
		self.chemicalcategory='organic'
		self.doestransformchemical='False'
		self.transportchemical='True'
		self.enabled='True'
		self.isdefaultforcategory='True'
		self.mate='<unset>'
		self.receivingchemicalname='replaceme'
		self.receivingcompartmentcategory='abiotic | air | air - default'
		self.sendingcompartmentcategory='terrestrial plant | leaf'
		self.sendingchemicalname='replaceme'
		self.dict_inputs=dict_inputs
		
	@property
	def compartmentrelationship(self):
		return ("above_or_below")
	
	@property
	def transferfactor(self):
		try:
			r=(self.sendingcompartment.allowexchange_forother * (check_neighbor(self.sendingcompartment,self.receivingcompartment,self.dict_inputs).is_neighbor()[1] )* (2*self.sendingcompartment.leafareaindex * self.sendingcompartment.chemical_totalcuticularconductance  + (self.sendingcompartment.isday_forother * self.sendingcompartment.chemical_totalstomatalconductance)) * (self.currentchemical.z_pureair/self.sendingcompartment.chemical_z_total)/self.sendingcompartment.volume ) if self.sendingcompartment.volume > 0 else 0
		except:
			r=nan
		return (r)

class diffusion_from_root_zone_to_surface_soil_alginstid_1939:
	def __init__(self, constants,containingscenario,currentchemical,sendingcompartment, receivingcompartment,dict_inputs):
		self.name='diffusion from root zone to surface soil(alginstid_1939)'
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
		self.receivingcompartmentcategory='abiotic | soil | surface soil | surface soil - default'
		self.sendingcompartmentcategory='abiotic | soil | root zone | root zone - default'
		self.sendingchemicalname='replaceme'
		self.dict_inputs=dict_inputs
		
	@property
	def masstransfercoefficient(self):
		return ((0.5*(self.receivingcompartment.chemical_z_times_d_times_gamma + self.sendingcompartment.chemical_z_times_d_times_gamma) * (self.receivingcompartment.chemical_exp_neg_depth_times_gamma  / self.receivingcompartment.chemical_one_minus_exp_neg_depth_times_gamma)) / ( (1 / self.receivingcompartment.chemical_depth_times_gamma)  -  (1 /self.sendingcompartment.chemical_depth_times_gamma)* (self.receivingcompartment.chemical_exp_neg_depth_times_gamma) * (self.sendingcompartment.chemical_one_minus_exp_neg_depth_times_gamma/ self.receivingcompartment.chemical_one_minus_exp_neg_depth_times_gamma)))
	
	@property
	def compartmentrelationship(self):
		return ("above_or_below")
	
	@property
	def transferfactor(self):
		try:
			r=-1 if self.receivingcompartment.chemical_depth_times_gamma > self.sendingcompartment.chemical_depth_times_gamma else self.masstransfercoefficient / self.sendingcompartment.chemical_depth_times_z_total
		except:
			r=nan
		return (r)

class diffusion_from_root_zone_to_vadose_zone_alginstid_1904:
	def __init__(self, constants,containingscenario,currentchemical,sendingcompartment, receivingcompartment,dict_inputs):
		self.name='diffusion from root zone to vadose zone(alginstid_1904)'
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
		self.receivingcompartmentcategory='abiotic | soil | vadose zone | vadose zone - default'
		self.sendingcompartmentcategory='abiotic | soil | root zone | root zone - default'
		self.sendingchemicalname='replaceme'
		self.dict_inputs=dict_inputs
		
	@property
	def masstransfercoefficient(self):
		return ((0.5*(self.sendingcompartment.chemical_z_times_d_times_gamma + self.receivingcompartment.chemical_z_times_d_times_gamma) * (self.sendingcompartment.chemical_exp_neg_depth_times_gamma  / self.sendingcompartment.chemical_one_minus_exp_neg_depth_times_gamma)) / ( (1 / self.sendingcompartment.chemical_depth_times_gamma)  -  (1 /self.receivingcompartment.chemical_depth_times_gamma)* (self.sendingcompartment.chemical_exp_neg_depth_times_gamma) * (self.receivingcompartment.chemical_one_minus_exp_neg_depth_times_gamma/ self.sendingcompartment.chemical_one_minus_exp_neg_depth_times_gamma)))
	
	@property
	def compartmentrelationship(self):
		return ("above_or_below")
	
	@property
	def transferfactor(self):
		try:
			r=-1 if self.sendingcompartment.chemical_depth_times_gamma > self.receivingcompartment.chemical_depth_times_gamma else self.masstransfercoefficient / self.sendingcompartment.chemical_depth_times_z_total
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
	def diffusiveterm(self):
		return ((1 / self.diffusiveterm_1 + 1 / self.diffusiveterm_2) ** (-1))
	
	@property
	def diffusiveterm_1(self):
		return (self.masstransfercoefficient_receiving_to_sending * self.receivingcompartment.chemical_z_total / self.sendingcompartment.chemical_z_total)
	
	@property
	def compartmentrelationship(self):
		return ("sender_below")
	
	@property
	def masstransfercoefficient_sending_to_receiving(self):
		return (self.receivingcompartment.chemical_d_effective / self.receivingcompartment.boundarylayerthicknessabovesediment)
	
	@property
	def masstransfercoefficient_receiving_to_sending(self):
		return (self.sendingcompartment.chemical_d_effective / self.sendingcompartment.chemical_boundarylayerthicknessbelowwater)
	
	@property
	def diffusiveterm_2(self):
		return (self.masstransfercoefficient_sending_to_receiving)
	
	@property
	def transferfactor(self):
		try:
			r=self.diffusiveterm * (check_neighbor(self.sendingcompartment,self.receivingcompartment,self.dict_inputs).is_neighbor()[1] / self.sendingcompartment.volume)
		except:
			r=nan
		return (r)

class diffusion_from_surface_soil_to_air_hg0_alginstid_3997:
	def __init__(self, constants,containingscenario,currentchemical,sendingcompartment, receivingcompartment,dict_inputs):
		self.name='diffusion from surface soil to air, hg0(alginstid_3997)'
		self.constants=constants
		self.containingscenario=containingscenario
		self.currentchemical=currentchemical
		self.sendingcompartment=sendingcompartment
		self.receivingcompartment=receivingcompartment
		self.category='diffusion'
		self.chemicalcategory='<unset>'
		self.doestransformchemical='False'
		self.transportchemical='True'
		self.enabled='True'
		self.isdefaultforcategory='True'
		self.mate='<unset>'
		self.receivingchemicalname='elemental mercury'
		self.receivingcompartmentcategory='abiotic | air | air - default'
		self.sendingcompartmentcategory='abiotic | soil | surface soil | surface soil - default'
		self.sendingchemicalname='elemental mercury'
		self.dict_inputs=dict_inputs
		
	@property
	def masstransfercoefficient(self):
		return (self.sendingcompartment.chemical_masstransfercoefficientonairsideofairsoilboundary)
	
	@property
	def compartmentrelationship(self):
		return ("above_or_below")
	
	@property
	def transferfactor(self):
		try:
			r=((self.sendingcompartment.fractionofareaavailableforverticaldiffusion * check_neighbor(self.sendingcompartment,self.receivingcompartment,self.dict_inputs).is_neighbor()[1])/(self.sendingcompartment.chemical_z_total * self.sendingcompartment.volume)) * ((1/(self.currentchemical.z_pureair * self.masstransfercoefficient)) + (1/(self.sendingcompartment.chemical_z_total * (self.sendingcompartment.chemical_d_effective/self.sendingcompartment.depth))))**(-1)
		except:
			r=nan
		return (r)

class diffusion_from_surface_soil_to_air_mhg_alginstid_3999:
	def __init__(self, constants,containingscenario,currentchemical,sendingcompartment, receivingcompartment,dict_inputs):
		self.name='diffusion from surface soil to air, mhg(alginstid_3999)'
		self.constants=constants
		self.containingscenario=containingscenario
		self.currentchemical=currentchemical
		self.sendingcompartment=sendingcompartment
		self.receivingcompartment=receivingcompartment
		self.category='diffusion'
		self.chemicalcategory='<unset>'
		self.doestransformchemical='False'
		self.transportchemical='True'
		self.enabled='True'
		self.isdefaultforcategory='True'
		self.mate='<unset>'
		self.receivingchemicalname='methylmercury'
		self.receivingcompartmentcategory='abiotic | air | air - default'
		self.sendingcompartmentcategory='abiotic | soil | surface soil | surface soil - default'
		self.sendingchemicalname='methylmercury'
		self.dict_inputs=dict_inputs
		
	@property
	def masstransfercoefficient(self):
		return (self.sendingcompartment.chemical_masstransfercoefficientonairsideofairsoilboundary)
	
	@property
	def compartmentrelationship(self):
		return ("above_or_below")
	
	@property
	def transferfactor(self):
		try:
			r=((self.sendingcompartment.fractionofareaavailableforverticaldiffusion * check_neighbor(self.sendingcompartment,self.receivingcompartment,self.dict_inputs).is_neighbor()[1])/(self.sendingcompartment.chemical_z_total * self.sendingcompartment.volume)) * ((1/(self.currentchemical.z_pureair * self.masstransfercoefficient)) + (1/(self.sendingcompartment.chemical_z_total * (self.sendingcompartment.chemical_d_effective/self.sendingcompartment.depth))))**(-1)
		except:
			r=nan
		return (r)

class diffusion_from_surface_soil_to_root_zone_alginstid_1919:
	def __init__(self, constants,containingscenario,currentchemical,sendingcompartment, receivingcompartment,dict_inputs):
		self.name='diffusion from surface soil to root zone(alginstid_1919)'
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
		self.receivingcompartmentcategory='abiotic | soil | root zone | root zone - default'
		self.sendingcompartmentcategory='abiotic | soil | surface soil | surface soil - default'
		self.sendingchemicalname='replaceme'
		self.dict_inputs=dict_inputs
		
	@property
	def masstransfercoefficient(self):
		return ((0.5*(self.sendingcompartment.chemical_z_times_d_times_gamma + self.receivingcompartment.chemical_z_times_d_times_gamma) * (self.sendingcompartment.chemical_exp_neg_depth_times_gamma  / self.sendingcompartment.chemical_one_minus_exp_neg_depth_times_gamma)) / ( (1 / self.sendingcompartment.chemical_depth_times_gamma)  -  (1 /self.receivingcompartment.chemical_depth_times_gamma)* (self.sendingcompartment.chemical_exp_neg_depth_times_gamma) * (self.receivingcompartment.chemical_one_minus_exp_neg_depth_times_gamma/ self.sendingcompartment.chemical_one_minus_exp_neg_depth_times_gamma)))
	
	@property
	def compartmentrelationship(self):
		return ("above_or_below")
	
	@property
	def transferfactor(self):
		try:
			r=-1 if self.sendingcompartment.chemical_depth_times_gamma > self.receivingcompartment.chemical_depth_times_gamma else self.masstransfercoefficient / self.sendingcompartment.chemical_depth_times_z_total
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
	def reaerationvelocity_owensformula(self):
		return (5.349 * (self.sendingcompartment.currentvelocity**0.67)/ (self.sendingcompartment.depth**0.85))
	
	@property
	def gasphasetransfercoefficient(self):
		return ((self.sendingcompartment.shearvelocity_m_per_day)*((self.constants.vonkarmensconstant**(0.33))/self.sendingcompartment.dimensionlessviscoussublayerthickness) * self.receivingcompartment.chemical_airschmidtnumber**(-0.67))
	
	@property
	def volatilizationtransferrate(self):
		return (1/(self.liquidphaseresistance + self.gasphaseresistance))
	
	@property
	def liquidphaseresistance(self):
		return (1/self.liquidphasetransfercoefficient_lake if  not (self.sendingcompartment.isflowing) else 1/self.liquidphasetransfercoefficient_flowingwaterbody)
	
	@property
	def ratioofvolatilizationratetoreaerationrate(self):
		return (sqrt(32/self.currentchemical.molecularweight))
	
	@property
	def gasphaseresistance(self):
		return (1/  ( self.gasphasetransfercoefficient * (self.currentchemical.h_over_r_t) ))
	
	@property
	def reaerationvelocity_churchillformula(self):
		return (5.049 * (self.sendingcompartment.currentvelocity**0.969)/ (self.sendingcompartment.depth**0.673))
	
	@property
	def liquidphasetransfercoefficient_lake(self):
		return ((self.sendingcompartment.shearvelocity_m_per_day)*((self.receivingcompartment.airdensity_kg_m3/self.sendingcompartment.waterdensity)**(0.5))*((self.constants.vonkarmensconstant**(0.33))/self.sendingcompartment.dimensionlessviscoussublayerthickness) * self.sendingcompartment.chemical_waterschmidtnumber**(-0.67))
	
	@property
	def liquidphasetransfercoefficient_flowingwaterbody(self):
		return (self.reaerationvelocity_owensformula * self.ratioofvolatilizationratetoreaerationrate if self.sendingcompartment.depth < 0.61 else ((self.currentchemical.d_purewater_m2_per_s * self.sendingcompartment.currentvelocity/self.sendingcompartment.depth)**(0.5))* 86400 if self.sendingcompartment.depth >= 0.61 and (self.sendingcompartment.currentvelocity < 0.518 or self.sendingcompartment.depth> 13.584 * self.sendingcompartment.currentvelocity**(0.29135)) else self.reaerationvelocity_churchillformula * self.ratioofvolatilizationratetoreaerationrate)
	
	@property
	def transferfactor(self):
		try:
			r=self.volatilizationtransferrate * (self.sendingcompartment.chemical_fractionmass_dissolved /self.sendingcompartment.volumefraction_liquid)*(check_neighbor(self.sendingcompartment,self.receivingcompartment,self.dict_inputs).is_neighbor()[1] / self.sendingcompartment.volume)
		except:
			r=nan
		return (r)

class diffusion_from_surface_water_to_air_two_film_alginstid_4080_organic:
	def __init__(self, constants,containingscenario,currentchemical,sendingcompartment, receivingcompartment,dict_inputs):
		self.name='diffusion from surface water to air, two film(alginstid_4080)-organic'
		self.constants=constants
		self.containingscenario=containingscenario
		self.currentchemical=currentchemical
		self.sendingcompartment=sendingcompartment
		self.receivingcompartment=receivingcompartment
		self.category='diffusion'
		self.chemicalcategory='organic'
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
	def reaerationvelocity_owensformula(self):
		return (5.349 * (self.sendingcompartment.currentvelocity**0.67)/ (self.sendingcompartment.depth**0.85))
	
	@property
	def gasphasetransfercoefficient(self):
		return ((self.sendingcompartment.shearvelocity_m_per_day)*((self.constants.vonkarmensconstant**(0.33))/self.sendingcompartment.dimensionlessviscoussublayerthickness) * self.receivingcompartment.chemical_airschmidtnumber**(-0.67))
	
	@property
	def volatilizationtransferrate(self):
		return (1/(self.liquidphaseresistance + self.gasphaseresistance))
	
	@property
	def liquidphaseresistance(self):
		return (1/self.liquidphasetransfercoefficient_lake if  not (self.sendingcompartment.isflowing) else 1/self.liquidphasetransfercoefficient_flowingwaterbody)
	
	@property
	def ratioofvolatilizationratetoreaerationrate(self):
		return (sqrt(32/self.currentchemical.molecularweight))
	
	@property
	def gasphaseresistance(self):
		return (1/  ( self.gasphasetransfercoefficient * (self.currentchemical.h_over_r_t) ))
	
	@property
	def reaerationvelocity_churchillformula(self):
		return (5.049 * (self.sendingcompartment.currentvelocity**0.969)/ (self.sendingcompartment.depth**0.673))
	
	@property
	def liquidphasetransfercoefficient_lake(self):
		return ((self.sendingcompartment.shearvelocity_m_per_day)*((self.receivingcompartment.airdensity_kg_m3/self.sendingcompartment.waterdensity)**(0.5))*((self.constants.vonkarmensconstant**(0.33))/self.sendingcompartment.dimensionlessviscoussublayerthickness) * self.sendingcompartment.chemical_waterschmidtnumber**(-0.67))
	
	@property
	def liquidphasetransfercoefficient_flowingwaterbody(self):
		return (self.reaerationvelocity_owensformula * self.ratioofvolatilizationratetoreaerationrate if self.sendingcompartment.depth < 0.61 else ((self.currentchemical.d_purewater_m2_per_s * self.sendingcompartment.currentvelocity/self.sendingcompartment.depth)**(0.5))* 86400 if self.sendingcompartment.depth >= 0.61 and (self.sendingcompartment.currentvelocity < 0.518 or self.sendingcompartment.depth> 13.584 * self.sendingcompartment.currentvelocity**(0.29135)) else self.reaerationvelocity_churchillformula * self.ratioofvolatilizationratetoreaerationrate)
	
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
	def diffusiveterm(self):
		return ((1 / self.diffusiveterm_1 + 1 / self.diffusiveterm_2) ** (-1))
	
	@property
	def diffusiveterm_1(self):
		return (self.masstransfercoefficient_receiving_to_sending * self.receivingcompartment.chemical_z_total / self.sendingcompartment.chemical_z_total)
	
	@property
	def compartmentrelationship(self):
		return ("sender_above")
	
	@property
	def masstransfercoefficient_sending_to_receiving(self):
		return (self.sendingcompartment.chemical_d_effective / self.sendingcompartment.boundarylayerthicknessabovesediment)
	
	@property
	def masstransfercoefficient_receiving_to_sending(self):
		return (self.receivingcompartment.chemical_d_effective / self.receivingcompartment.chemical_boundarylayerthicknessbelowwater)
	
	@property
	def diffusiveterm_2(self):
		return (self.masstransfercoefficient_sending_to_receiving)
	
	@property
	def transferfactor(self):
		try:
			r=self.diffusiveterm * (check_neighbor(self.sendingcompartment,self.receivingcompartment,self.dict_inputs).is_neighbor()[1] / self.sendingcompartment.volume)
		except:
			r=nan
		return (r)

class diffusion_from_vadose_zone_to_root_zone_alginstid_1914:
	def __init__(self, constants,containingscenario,currentchemical,sendingcompartment, receivingcompartment,dict_inputs):
		self.name='diffusion from vadose zone to root zone(alginstid_1914)'
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
		self.receivingcompartmentcategory='abiotic | soil | root zone | root zone - default'
		self.sendingcompartmentcategory='abiotic | soil | vadose zone | vadose zone - default'
		self.sendingchemicalname='replaceme'
		self.dict_inputs=dict_inputs
		
	@property
	def masstransfercoefficient(self):
		return ((0.5*(self.receivingcompartment.chemical_z_times_d_times_gamma + self.sendingcompartment.chemical_z_times_d_times_gamma) * (self.receivingcompartment.chemical_exp_neg_depth_times_gamma  / self.receivingcompartment.chemical_one_minus_exp_neg_depth_times_gamma)) / ( (1 / self.receivingcompartment.chemical_depth_times_gamma)  -  (1 /self.sendingcompartment.chemical_depth_times_gamma)* (self.receivingcompartment.chemical_exp_neg_depth_times_gamma) * (self.sendingcompartment.chemical_one_minus_exp_neg_depth_times_gamma/ self.receivingcompartment.chemical_one_minus_exp_neg_depth_times_gamma)))
	
	@property
	def compartmentrelationship(self):
		return ("above_or_below")
	
	@property
	def transferfactor(self):
		try:
			r=-1 if self.receivingcompartment.chemical_depth_times_gamma > self.sendingcompartment.chemical_depth_times_gamma else self.masstransfercoefficient / self.sendingcompartment.chemical_depth_times_z_total
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

class erosion_from_surface_soil_to_soil_advection_sink:
	def __init__(self, constants,containingscenario,currentchemical,sendingcompartment, receivingcompartment,dict_inputs):
		self.name='erosion from surface soil to soil advection sink'
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
		self.receivingcompartmentcategory='sink | abiotic | soil | surface soil | soil advection sink'
		self.sendingcompartmentcategory='abiotic | soil | surface soil | surface soil - default'
		self.sendingchemicalname='replaceme'
		self.dict_inputs=dict_inputs
		
	@property
	def arealerosionrate(self):
		return (self.sendingcompartment.totalerosionrate_kg_m2_day * float(self.dict_inputs['df_links'].loc[(self.dict_inputs['df_links']['receiving_compartment_new']==self.receivingcompartment.name)&(self.dict_inputs['df_links']['sending_compartment_new']==self.sendingcompartment.name)&(self.dict_inputs['df_links']['property']=='fractionoftotalerosion'),'value'].values[0]))
	
	@property
	def solidarealphasevelocity(self):
		return (self.arealerosionrate / self.sendingcompartment.rho)
	
	@property
	def compartmentrelationship(self):
		return ("in_same_volume_element")
	
	@property
	def transferfactor(self):
		try:
			r=self.solidarealphasevelocity * (self.sendingcompartment.chemical_fractionmass_sorbed/self.sendingcompartment.chemical_volumefraction_solid) * (self.sendingcompartment.fractionofareaavailableforerosion*self.sendingcompartment.area) / self.sendingcompartment.volume
		except:
			r=nan
		return (r)

class erosion_from_surface_soil_to_surface_soil_general_alginstid_2460:
	def __init__(self, constants,containingscenario,currentchemical,sendingcompartment, receivingcompartment,dict_inputs):
		self.name='erosion from surface soil to surface soil, general(alginstid_2460)'
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
		self.receivingcompartmentcategory='abiotic | soil | surface soil | surface soil - default'
		self.sendingcompartmentcategory='abiotic | soil | surface soil | surface soil - default'
		self.sendingchemicalname='replaceme'
		self.dict_inputs=dict_inputs
		
	@property
	def arealerosionrate(self):
		return (self.sendingcompartment.totalerosionrate_kg_m2_day * float(self.dict_inputs['df_links'].loc[(self.dict_inputs['df_links']['receiving_compartment_new']==self.receivingcompartment.name)&(self.dict_inputs['df_links']['sending_compartment_new']==self.sendingcompartment.name)&(self.dict_inputs['df_links']['property']=='fractionoftotalerosion'),'value'].values[0]))
	
	@property
	def solidarealphasevelocity(self):
		return (self.arealerosionrate / self.sendingcompartment.rho)
	
	@property
	def compartmentrelationship(self):
		return ("next_to")
	
	@property
	def transferfactor(self):
		try:
			r=self.solidarealphasevelocity * (self.sendingcompartment.chemical_fractionmass_sorbed/self.sendingcompartment.chemical_volumefraction_solid) * (self.sendingcompartment.fractionofareaavailableforerosion*self.sendingcompartment.area) / self.sendingcompartment.volume
		except:
			r=nan
		return (r)

class erosion_from_surface_soil_to_surface_water_general_alginstid_3515:
	def __init__(self, constants,containingscenario,currentchemical,sendingcompartment, receivingcompartment,dict_inputs):
		self.name='erosion from surface soil to surface water, general(alginstid_3515)'
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
		self.sendingcompartmentcategory='abiotic | soil | surface soil | surface soil - default'
		self.sendingchemicalname='replaceme'
		self.dict_inputs=dict_inputs
		
	@property
	def arealerosionrate(self):
		return (self.sendingcompartment.totalerosionrate_kg_m2_day * float(self.dict_inputs['df_links'].loc[(self.dict_inputs['df_links']['receiving_compartment_new']==self.receivingcompartment.name)&(self.dict_inputs['df_links']['sending_compartment_new']==self.sendingcompartment.name)&(self.dict_inputs['df_links']['property']=='fractionoftotalerosion'),'value'].values[0]))
	
	@property
	def solidarealphasevelocity(self):
		return (self.arealerosionrate / self.sendingcompartment.rho)
	
	@property
	def compartmentrelationship(self):
		return ("next_to")
	
	@property
	def transferfactor(self):
		try:
			r=self.solidarealphasevelocity * (self.sendingcompartment.chemical_fractionmass_sorbed/self.sendingcompartment.chemical_volumefraction_solid) * (self.sendingcompartment.fractionofareaavailableforerosion*self.sendingcompartment.area) / self.sendingcompartment.volume
		except:
			r=nan
		return (r)

class exchange_from_benthic_invertebrate_to_sediment_dioxins:
	def __init__(self, constants,containingscenario,currentchemical,sendingcompartment, receivingcompartment,dict_inputs):
		self.name='exchange from benthic invertebrate to sediment, dioxins'
		self.constants=constants
		self.containingscenario=containingscenario
		self.currentchemical=currentchemical
		self.sendingcompartment=sendingcompartment
		self.receivingcompartment=receivingcompartment
		self.category='exchange'
		self.chemicalcategory='organic | dioxin-furan'
		self.doestransformchemical='False'
		self.transportchemical='True'
		self.enabled='False'
		self.isdefaultforcategory='True'
		self.mate='<unset>'
		self.receivingchemicalname='replaceme'
		self.receivingcompartmentcategory='abiotic | sediment | sediment - default'
		self.sendingcompartmentcategory='insect | benthic invertebrate'
		self.sendingchemicalname='replaceme'
		self.dict_inputs=dict_inputs
		
	@property
	def transferfactor(self):
		try:
			r=(-log(1 - self.sendingcompartment.chemical_sedimentpartitioning_alphaofequilibrium) / self.sendingcompartment.chemical_sedimentpartitioning_timetoreachalphaofequilibrium) * self.receivingcompartment.volumefraction_liquid
		except:
			r=nan
		return (r)

class exchange_from_benthic_invertebrate_to_sediment_pahs:
	def __init__(self, constants,containingscenario,currentchemical,sendingcompartment, receivingcompartment,dict_inputs):
		self.name='exchange from benthic invertebrate to sediment, pahs'
		self.constants=constants
		self.containingscenario=containingscenario
		self.currentchemical=currentchemical
		self.sendingcompartment=sendingcompartment
		self.receivingcompartment=receivingcompartment
		self.category='exchange'
		self.chemicalcategory='organic | pah'
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
	def transferfactor(self):
		try:
			r=(self.sendingcompartment.chemical_clearanceconstant * 24) / self.sendingcompartment.chemical_v_d
		except:
			r=nan
		return (r)

class exchange_from_fish_to_surface_water_organics_alginstid_1515:
	def __init__(self, constants,containingscenario,currentchemical,sendingcompartment, receivingcompartment,dict_inputs):
		self.name='exchange from fish to surface water, organics(alginstid_1515)'
		self.constants=constants
		self.containingscenario=containingscenario
		self.currentchemical=currentchemical
		self.sendingcompartment=sendingcompartment
		self.receivingcompartment=receivingcompartment
		self.category='bioenergetic fish model'
		self.chemicalcategory='organic'
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
			r=self.sendingcompartment.chemical_gilleliminationrate
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

class exchange_from_sediment_to_benthic_invertebrate_interacts_with_pore_water_dioxins:
	def __init__(self, constants,containingscenario,currentchemical,sendingcompartment, receivingcompartment,dict_inputs):
		self.name='exchange from sediment to benthic invertebrate, interacts with pore water, dioxins'
		self.constants=constants
		self.containingscenario=containingscenario
		self.currentchemical=currentchemical
		self.sendingcompartment=sendingcompartment
		self.receivingcompartment=receivingcompartment
		self.category='exchange'
		self.chemicalcategory='organic | dioxin-furan'
		self.doestransformchemical='False'
		self.transportchemical='True'
		self.enabled='False'
		self.isdefaultforcategory='True'
		self.mate='<unset>'
		self.receivingchemicalname='replaceme'
		self.receivingcompartmentcategory='insect | benthic invertebrate'
		self.sendingcompartmentcategory='abiotic | sediment | sediment - default'
		self.sendingchemicalname='replaceme'
		self.dict_inputs=dict_inputs
		
	@property
	def transferfactor(self):
		try:
			r=self.receivingcompartment.totalmass * ((-log(1 - self.receivingcompartment.chemical_sedimentpartitioning_alphaofequilibrium) / self.receivingcompartment.chemical_sedimentpartitioning_timetoreachalphaofequilibrium) * self.receivingcompartment.chemical_sedimentpartitioning_partitioncoefficient * self.sendingcompartment.chemical_fractionmass_dissolved) / (self.sendingcompartment.volume * 1000 * self.sendingcompartment.volumefraction_liquid)
		except:
			r=nan
		return (r)

class exchange_from_sediment_to_benthic_invertebrate_interacts_with_pore_water_pahs:
	def __init__(self, constants,containingscenario,currentchemical,sendingcompartment, receivingcompartment,dict_inputs):
		self.name='exchange from sediment to benthic invertebrate, interacts with pore water, pahs'
		self.constants=constants
		self.containingscenario=containingscenario
		self.currentchemical=currentchemical
		self.sendingcompartment=sendingcompartment
		self.receivingcompartment=receivingcompartment
		self.category='exchange'
		self.chemicalcategory='organic | pah'
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
	def transferfactor(self):
		try:
			r=(24) * self.receivingcompartment.totalmass * (self.receivingcompartment.chemical_clearanceconstant * (1/1000)) * self.sendingcompartment.chemical_fractionmass_dissolved / (self.sendingcompartment.volume * self.sendingcompartment.volumefraction_liquid)
		except:
			r=nan
		return (r)

class exchange_from_surface_water_to_fish_organics_alginstid_1517:
	def __init__(self, constants,containingscenario,currentchemical,sendingcompartment, receivingcompartment,dict_inputs):
		self.name='exchange from surface water to fish, organics(alginstid_1517)'
		self.constants=constants
		self.containingscenario=containingscenario
		self.currentchemical=currentchemical
		self.sendingcompartment=sendingcompartment
		self.receivingcompartment=receivingcompartment
		self.category='bioenergetic fish model'
		self.chemicalcategory='organic'
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
			r=self.receivingcompartment.chemical_fishchemicaluptakerateviagill * self.receivingcompartment.populationsize * (self.receivingcompartment.bw) * (self.sendingcompartment.chemical_fractionmass_dissolved) / (self.sendingcompartment.volume * 1000)
		except:
			r=nan
		return (r)

class exchange_from_surface_water_to_macrophyte_alginstid_1552:
	def __init__(self, constants,containingscenario,currentchemical,sendingcompartment, receivingcompartment,dict_inputs):
		self.name='exchange from surface water to macrophyte(alginstid_1552)'
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
		self.receivingcompartmentcategory='aquatic plant | macrophyte'
		self.sendingcompartmentcategory='abiotic | surface water | surface water - default'
		self.sendingchemicalname='replaceme'
		self.dict_inputs=dict_inputs
		
	@property
	def transferfactor(self):
		try:
			r=self.receivingcompartment.chemical_bioaccumulationrate * self.receivingcompartment.volume * (self.sendingcompartment.chemical_fractionmass_dissolved) / (self.sendingcompartment.volume)
		except:
			r=nan
		return (r)

class exchange_from_surface_water_to_zooplankton_organics_alginstid_1517_z:
	def __init__(self, constants,containingscenario,currentchemical,sendingcompartment, receivingcompartment,dict_inputs):
		self.name='exchange from surface water to zooplankton, organics(alginstid_1517_z)'
		self.constants=constants
		self.containingscenario=containingscenario
		self.currentchemical=currentchemical
		self.sendingcompartment=sendingcompartment
		self.receivingcompartment=receivingcompartment
		self.category='bioenergetic fish model'
		self.chemicalcategory='organic'
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
			r=self.receivingcompartment.chemical_absorptionrateconstant * self.receivingcompartment.populationsize * (self.receivingcompartment.bw) * (self.sendingcompartment.chemical_fractionmass_dissolved) / (self.sendingcompartment.volume * 1000)
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

class litterfall_from_leaves_to_soil_alginstid_1088:
	def __init__(self, constants,containingscenario,currentchemical,sendingcompartment, receivingcompartment,dict_inputs):
		self.name='litterfall from leaves to soil(alginstid_1088)'
		self.constants=constants
		self.containingscenario=containingscenario
		self.currentchemical=currentchemical
		self.sendingcompartment=sendingcompartment
		self.receivingcompartment=receivingcompartment
		self.category='litterfall'
		self.chemicalcategory='all'
		self.doestransformchemical='False'
		self.transportchemical='True'
		self.enabled='True'
		self.isdefaultforcategory='True'
		self.mate='<unset>'
		self.receivingchemicalname='benzo(a)pyrene'
		self.receivingcompartmentcategory='abiotic | soil | surface soil | surface soil - default'
		self.sendingcompartmentcategory='terrestrial plant | leaf'
		self.sendingchemicalname='benzo(a)pyrene'
		self.dict_inputs=dict_inputs
		
	@property
	def compartmentrelationship(self):
		return ("in_same_volume_element")
	
	@property
	def transferfactor(self):
		try:
			r=self.sendingcompartment.litterfallrate
		except:
			r=nan
		return (r)

class litterfall_of_leaf_particle_to_soil_alginstid_1098:
	def __init__(self, constants,containingscenario,currentchemical,sendingcompartment, receivingcompartment,dict_inputs):
		self.name='litterfall of leaf particle to soil(alginstid_1098)'
		self.constants=constants
		self.containingscenario=containingscenario
		self.currentchemical=currentchemical
		self.sendingcompartment=sendingcompartment
		self.receivingcompartment=receivingcompartment
		self.category='litterfall'
		self.chemicalcategory='all'
		self.doestransformchemical='False'
		self.transportchemical='True'
		self.enabled='True'
		self.isdefaultforcategory='True'
		self.mate='<unset>'
		self.receivingchemicalname='benzo(a)pyrene'
		self.receivingcompartmentcategory='abiotic | soil | surface soil | surface soil - default'
		self.sendingcompartmentcategory='terrestrial plant | leaf particle'
		self.sendingchemicalname='benzo(a)pyrene'
		self.dict_inputs=dict_inputs
		
	@property
	def compartmentrelationship(self):
		return ("in_same_volume_element")
	
	@property
	def transferfactor(self):
		try:
			r=self.sendingcompartment.litterfallrate
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

class methylation_hg2_mhg_in_plant_leaves_rate_is_input_alginstid_1248:
	def __init__(self, constants,containingscenario,currentchemical,sendingcompartment, receivingcompartment,dict_inputs):
		self.name='methylation(hg2 -> mhg) in plant leaves, rate is input(alginstid_1248)'
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
		self.receivingcompartmentcategory='terrestrial plant | leaf'
		self.sendingcompartmentcategory='terrestrial plant | leaf'
		self.sendingchemicalname='divalent mercury'
		self.dict_inputs=dict_inputs
		
	@property
	def compartmentrelationship(self):
		return ("same")
	
	@property
	def transferfactor(self):
		try:
			r=self.sendingcompartment.allowexchange_forother * self.sendingcompartment.chemical_methylationrate
		except:
			r=nan
		return (r)

class methylation_hg2_mhg_in_plant_stem_rate_is_input_alginstid_1270:
	def __init__(self, constants,containingscenario,currentchemical,sendingcompartment, receivingcompartment,dict_inputs):
		self.name='methylation(hg2 -> mhg) in plant stem, rate is input(alginstid_1270)'
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
		self.receivingcompartmentcategory='terrestrial plant | stem'
		self.sendingcompartmentcategory='terrestrial plant | stem'
		self.sendingchemicalname='divalent mercury'
		self.dict_inputs=dict_inputs
		
	@property
	def compartmentrelationship(self):
		return ("same")
	
	@property
	def transferfactor(self):
		try:
			r=self.sendingcompartment.allowexchange_forother * self.sendingcompartment.chemical_methylationrate
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

class particles_blown_off_from_plant_leaf_to_air_dry_alginstid_4010:
	def __init__(self, constants,containingscenario,currentchemical,sendingcompartment, receivingcompartment,dict_inputs):
		self.name='particles blown off from plant leaf to air (dry)(alginstid_4010)'
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
		self.receivingcompartmentcategory='abiotic | air | air - default'
		self.sendingcompartmentcategory='terrestrial plant | leaf particle'
		self.sendingchemicalname='replaceme'
		self.dict_inputs=dict_inputs
		
	@property
	def compartmentrelationship(self):
		return ("above_or_below")
	
	@property
	def transferfactor(self):
		try:
			r=1 * self.receivingcompartment.chemical_particlevolumetricdrydepositionrate * self.sendingcompartment.associated_leaf_comp.drydepinterceptionfraction * check_neighbor(self.sendingcompartment,self.receivingcompartment,self.dict_inputs).is_neighbor()[1]/ self.sendingcompartment.volume  * (self.dict_inputs["met_dict"]["frac_time_exchange_no_rain"]) if self.sendingcompartment.volume>0 else 0
		except:
			r=nan
		return (r)

class particles_washed_off_leaf_onto_ground_alginstid_1103:
	def __init__(self, constants,containingscenario,currentchemical,sendingcompartment, receivingcompartment,dict_inputs):
		self.name='particles washed off leaf onto ground(alginstid_1103)'
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
		self.receivingcompartmentcategory='abiotic | soil | surface soil | surface soil - default'
		self.sendingcompartmentcategory='terrestrial plant | leaf particle'
		self.sendingchemicalname='replaceme'
		self.dict_inputs=dict_inputs
		
	@property
	def compartmentrelationship(self):
		return ("in_same_volume_element")
	
	@property
	def transferfactor(self):
		try:
			r=1 * self.sendingcompartment.chemical_particlevolumetricwetdepositionrate * self.sendingcompartment.associated_leaf_comp.wetdepinterceptionfraction * self.receivingcompartment.area/self.sendingcompartment.volume *self.dict_inputs["met_dict"]["frac_time_exchange_rain"]
		except:
			r=nan
		return (r)

class percolation_from_root_zone_to_vadose_zone_alginstid_1909:
	def __init__(self, constants,containingscenario,currentchemical,sendingcompartment, receivingcompartment,dict_inputs):
		self.name='percolation from root zone to vadose zone(alginstid_1909)'
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
		self.receivingcompartmentcategory='abiotic | soil | vadose zone | vadose zone - default'
		self.sendingcompartmentcategory='abiotic | soil | root zone | root zone - default'
		self.sendingchemicalname='replaceme'
		self.dict_inputs=dict_inputs
		
	@property
	def transferfactor(self):
		try:
			r=(self.sendingcompartment.chemical_effectiveadvectionvelocity * self.sendingcompartment.chemical_gradientofsoilconcentrationchange) / (exp(self.sendingcompartment.chemical_gradientofsoilconcentrationchange * self.sendingcompartment.depth) - 1)
		except:
			r=nan
		return (r)

class percolation_from_surface_soil_to_root_zone_alginstid_1924:
	def __init__(self, constants,containingscenario,currentchemical,sendingcompartment, receivingcompartment,dict_inputs):
		self.name='percolation from surface soil to root zone(alginstid_1924)'
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
		self.receivingcompartmentcategory='abiotic | soil | root zone | root zone - default'
		self.sendingcompartmentcategory='abiotic | soil | surface soil | surface soil - default'
		self.sendingchemicalname='replaceme'
		self.dict_inputs=dict_inputs
		
	@property
	def transferfactor(self):
		try:
			r=(self.sendingcompartment.chemical_effectiveadvectionvelocity * self.sendingcompartment.chemical_gradientofsoilconcentrationchange) / (exp(self.sendingcompartment.chemical_gradientofsoilconcentrationchange * self.sendingcompartment.depth) - 1)
		except:
			r=nan
		return (r)

class percolation_from_vadose_zone_to_groundwater_alginstid_1899:
	def __init__(self, constants,containingscenario,currentchemical,sendingcompartment, receivingcompartment,dict_inputs):
		self.name='percolation from vadose zone to groundwater(alginstid_1899)'
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
		self.receivingcompartmentcategory='abiotic | soil | groundwater | groundwater - default'
		self.sendingcompartmentcategory='abiotic | soil | vadose zone | vadose zone - default'
		self.sendingchemicalname='replaceme'
		self.dict_inputs=dict_inputs
		
	@property
	def transferfactor(self):
		try:
			r=(self.sendingcompartment.chemical_effectiveadvectionvelocity * self.sendingcompartment.chemical_gradientofsoilconcentrationchange) / (exp(self.sendingcompartment.chemical_gradientofsoilconcentrationchange * self.sendingcompartment.depth) - 1)
		except:
			r=nan
		return (r)

class recharge_from_groundwater_to_surface_water_general_alginstid_3510:
	def __init__(self, constants,containingscenario,currentchemical,sendingcompartment, receivingcompartment,dict_inputs):
		self.name='recharge from groundwater to surface water, general(alginstid_3510)'
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
		self.sendingcompartmentcategory='abiotic | soil | groundwater | groundwater - default'
		self.sendingchemicalname='replaceme'
		self.dict_inputs=dict_inputs
		
	@property
	def liquidarealphasevelocity(self):
		return (default_rechargerate)
	
	@property
	def transferfactor(self):
		try:
			r=self.liquidarealphasevelocity* (self.sendingcompartment.chemical_fractionmass_dissolved/self.sendingcompartment.volumefraction_liquid) * (check_neighbor(self.sendingcompartment,self.receivingcompartment,self.dict_inputs).is_neighbor()[1]) / self.sendingcompartment.volume
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
	def solidarealphasevelocity(self):
		return (self.sendingcompartment.sedimentresuspensionrate_m3_m2_day)
	
	@property
	def compartmentrelationship(self):
		return ("sender_below")
	
	@property
	def transferfactor(self):
		try:
			r=self.solidarealphasevelocity * (self.sendingcompartment.chemical_fractionmass_sorbed/self.sendingcompartment.volumefraction_solid) * (check_neighbor(self.sendingcompartment,self.receivingcompartment,self.dict_inputs).is_neighbor()[1]) / self.sendingcompartment.volume
		except:
			r=nan
		return (r)

class resuspension_from_surface_soil_to_air_set_to_deposition_rate_of_particles_alginstid_4000:
	def __init__(self, constants,containingscenario,currentchemical,sendingcompartment, receivingcompartment,dict_inputs):
		self.name='resuspension from surface soil to air, set to deposition rate of particles(alginstid_4000)'
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
		self.receivingcompartmentcategory='abiotic | air | air - default'
		self.sendingcompartmentcategory='abiotic | soil | surface soil | surface soil - default'
		self.sendingchemicalname='replaceme'
		self.dict_inputs=dict_inputs
		
	@property
	def transferfactor(self):
		try:
			r=((self.receivingcompartment.chemical_dustresuspensionrate * (1 -  (  self.sendingcompartment.associated_leaf_comp.allowexchange_forair * self.sendingcompartment.associated_leaf_comp.drydepinterceptionfraction ))) / self.receivingcompartment.dustdensity) * (self.sendingcompartment.chemical_z_solid / self.sendingcompartment.chemical_z_total) * (check_neighbor(self.sendingcompartment,self.receivingcompartment,self.dict_inputs).is_neighbor()[1] / self.sendingcompartment.volume)
		except:
			r=nan
		return (r)

class runoff_from_surface_soil_to_soil_advection_sink:
	def __init__(self, constants,containingscenario,currentchemical,sendingcompartment, receivingcompartment,dict_inputs):
		self.name='runoff from surface soil to soil advection sink'
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
		self.receivingcompartmentcategory='sink | abiotic | soil | surface soil | soil advection sink'
		self.sendingcompartmentcategory='abiotic | soil | surface soil | surface soil - default'
		self.sendingchemicalname='replaceme'
		self.dict_inputs=dict_inputs
		
	@property
	def compartmentrelationship(self):
		return ("in_same_volume_element")
	
	@property
	def liquidarealphasevelocity(self):
		return (self.sendingcompartment.totalrunoffrate_m3_m2_day * float(self.dict_inputs['df_links'].loc[(self.dict_inputs['df_links']['receiving_compartment_new']==self.receivingcompartment.name)&(self.dict_inputs['df_links']['sending_compartment_new']==self.sendingcompartment.name)&(self.dict_inputs['df_links']['property']=='fractionoftotalrunoff'),'value'].values[0]))
	
	@property
	def transferfactor(self):
		try:
			r=self.liquidarealphasevelocity* (self.sendingcompartment.chemical_fractionmass_dissolved/self.sendingcompartment.chemical_volumefraction_liquid) * (self.sendingcompartment.fractionofareaavailableforrunoff*self.sendingcompartment.area) / self.sendingcompartment.volume
		except:
			r=nan
		return (r)

class runoff_from_surface_soil_to_surface_soil_general_alginstid_2465:
	def __init__(self, constants,containingscenario,currentchemical,sendingcompartment, receivingcompartment,dict_inputs):
		self.name='runoff from surface soil to surface soil, general(alginstid_2465)'
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
		self.receivingcompartmentcategory='abiotic | soil | surface soil | surface soil - default'
		self.sendingcompartmentcategory='abiotic | soil | surface soil | surface soil - default'
		self.sendingchemicalname='replaceme'
		self.dict_inputs=dict_inputs
		
	@property
	def compartmentrelationship(self):
		return ("next_to")
	
	@property
	def liquidarealphasevelocity(self):
		return (self.sendingcompartment.totalrunoffrate_m3_m2_day * float(self.dict_inputs['df_links'].loc[(self.dict_inputs['df_links']['receiving_compartment_new']==self.receivingcompartment.name)&(self.dict_inputs['df_links']['sending_compartment_new']==self.sendingcompartment.name)&(self.dict_inputs['df_links']['property']=='fractionoftotalrunoff'),'value'].values[0]))
	
	@property
	def transferfactor(self):
		try:
			r=self.liquidarealphasevelocity* (self.sendingcompartment.chemical_fractionmass_dissolved/self.sendingcompartment.chemical_volumefraction_liquid) * (self.sendingcompartment.fractionofareaavailableforrunoff*self.sendingcompartment.area) / self.sendingcompartment.volume
		except:
			r=nan
		return (r)

class runoff_from_surface_soil_to_surface_water_general_alginstid_3520:
	def __init__(self, constants,containingscenario,currentchemical,sendingcompartment, receivingcompartment,dict_inputs):
		self.name='runoff from surface soil to surface water, general(alginstid_3520)'
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
		self.sendingcompartmentcategory='abiotic | soil | surface soil | surface soil - default'
		self.sendingchemicalname='replaceme'
		self.dict_inputs=dict_inputs
		
	@property
	def compartmentrelationship(self):
		return ("next_to")
	
	@property
	def liquidarealphasevelocity(self):
		return (self.sendingcompartment.totalrunoffrate_m3_m2_day * float(self.dict_inputs['df_links'].loc[(self.dict_inputs['df_links']['receiving_compartment_new']==self.receivingcompartment.name)&(self.dict_inputs['df_links']['sending_compartment_new']==self.sendingcompartment.name)&(self.dict_inputs['df_links']['property']=='fractionoftotalrunoff'),'value'].values[0]))
	
	@property
	def transferfactor(self):
		try:
			r=self.liquidarealphasevelocity* (self.sendingcompartment.chemical_fractionmass_dissolved/self.sendingcompartment.chemical_volumefraction_liquid) * (self.sendingcompartment.fractionofareaavailableforrunoff*self.sendingcompartment.area) / self.sendingcompartment.volume
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
	def solidarealphasevelocity(self):
		return (self.sendingcompartment.sedimentburialratetohavezeronetdeposition_m3_m2_day)
	
	@property
	def compartmentrelationship(self):
		return ("sender_above")
	
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
	def solidarealphasevelocity(self):
		return (self.sendingcompartment.sedimentdepositionrate_m3_m2_day)
	
	@property
	def compartmentrelationship(self):
		return ("sender_above")
	
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
	def k2(self):
		return (self.k1 * self.sendingcompartment.chemical_sedimentpartitioning_partitioncoefficient)
	
	@property
	def k1(self):
		return (-log(1 - self.sendingcompartment.chemical_sedimentpartitioning_alphaofequilibrium) / self.sendingcompartment.chemical_sedimentpartitioning_timetoreachalphaofequilibrium)
	
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
	def k2(self):
		return (self.k1 * self.sendingcompartment.chemical_watercolumndissolvedpartitioning_partitioncoefficient)
	
	@property
	def k1(self):
		return (-log(1 - self.sendingcompartment.chemical_watercolumndissolvedpartitioning_alphaofequilibrium) / self.sendingcompartment.chemical_watercolumndissolvedpartitioning_timetoreachalphaofequilibrium)
	
	@property
	def transferfactor(self):
		try:
			r=self.k1
		except:
			r=nan
		return (r)

class time_dependent_partition_from_root_to_root_zone_interacts_with_bulk_soil_agriculture_cd_alginstid_1932:
	def __init__(self, constants,containingscenario,currentchemical,sendingcompartment, receivingcompartment,dict_inputs):
		self.name='time-dependent partition from root to root zone, interacts with bulk soil - agriculture, cd(alginstid_1932)'
		self.constants=constants
		self.containingscenario=containingscenario
		self.currentchemical=currentchemical
		self.sendingcompartment=sendingcompartment
		self.receivingcompartment=receivingcompartment
		self.category='time-dependent partition'
		self.chemicalcategory='metals | cadmium'
		self.doestransformchemical='False'
		self.transportchemical='True'
		self.enabled='True'
		self.isdefaultforcategory='True'
		self.mate='<unset>'
		self.receivingchemicalname='replaceme'
		self.receivingcompartmentcategory='abiotic | soil | root zone | root zone - default'
		self.sendingcompartmentcategory='terrestrial plant | root | root - agriculture - general'
		self.sendingchemicalname='replaceme'
		self.dict_inputs=dict_inputs
		
	@property
	def k2(self):
		return (self.k1 * self.sendingcompartment.chemical_root_rootzonepartitioningbulksoil_partitioncoefficient)
	
	@property
	def k1(self):
		return (-log(1 - self.sendingcompartment.chemical_root_rootzonepartitioningbulksoil_alphaofsteadystate) / self.sendingcompartment.chemical_root_rootzonepartitioningbulksoil_timetoreachalphaofsteadystate)
	
	@property
	def transferfactor(self):
		try:
			r=self.sendingcompartment.allowexchange_forother * self.k1
		except:
			r=nan
		return (r)

class time_dependent_partition_from_root_to_root_zone_interacts_with_bulk_soil_agriculture_hg_alginstid_1932:
	def __init__(self, constants,containingscenario,currentchemical,sendingcompartment, receivingcompartment,dict_inputs):
		self.name='time-dependent partition from root to root zone, interacts with bulk soil - agriculture, hg(alginstid_1932)'
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
		self.receivingcompartmentcategory='abiotic | soil | root zone | root zone - default'
		self.sendingcompartmentcategory='terrestrial plant | root | root - agriculture - general'
		self.sendingchemicalname='replaceme'
		self.dict_inputs=dict_inputs
		
	@property
	def k2(self):
		return (self.k1 * self.sendingcompartment.chemical_root_rootzonepartitioningbulksoil_partitioncoefficient)
	
	@property
	def k1(self):
		return (-log(1 - self.sendingcompartment.chemical_root_rootzonepartitioningbulksoil_alphaofsteadystate) / self.sendingcompartment.chemical_root_rootzonepartitioningbulksoil_timetoreachalphaofsteadystate)
	
	@property
	def transferfactor(self):
		try:
			r=self.sendingcompartment.allowexchange_forother * self.k1
		except:
			r=nan
		return (r)

class time_dependent_partition_from_root_to_root_zone_interacts_with_bulk_soil_grasses_herbs_cd_alginstid_1933:
	def __init__(self, constants,containingscenario,currentchemical,sendingcompartment, receivingcompartment,dict_inputs):
		self.name='time-dependent partition from root to root zone, interacts with bulk soil - grasses/herbs, cd(alginstid_1933)'
		self.constants=constants
		self.containingscenario=containingscenario
		self.currentchemical=currentchemical
		self.sendingcompartment=sendingcompartment
		self.receivingcompartment=receivingcompartment
		self.category='time-dependent partition'
		self.chemicalcategory='metals | cadmium'
		self.doestransformchemical='False'
		self.transportchemical='True'
		self.enabled='True'
		self.isdefaultforcategory='True'
		self.mate='<unset>'
		self.receivingchemicalname='replaceme'
		self.receivingcompartmentcategory='abiotic | soil | root zone | root zone - default'
		self.sendingcompartmentcategory='terrestrial plant | root | root - grasses/herbs'
		self.sendingchemicalname='replaceme'
		self.dict_inputs=dict_inputs
		
	@property
	def k2(self):
		return (self.k1 * self.sendingcompartment.chemical_root_rootzonepartitioningbulksoil_partitioncoefficient)
	
	@property
	def k1(self):
		return (-log(1 - self.sendingcompartment.chemical_root_rootzonepartitioningbulksoil_alphaofsteadystate) / self.sendingcompartment.chemical_root_rootzonepartitioningbulksoil_timetoreachalphaofsteadystate)
	
	@property
	def transferfactor(self):
		try:
			r=self.sendingcompartment.allowexchange_forother * self.k1
		except:
			r=nan
		return (r)

class time_dependent_partition_from_root_to_root_zone_interacts_with_bulk_soil_grasses_herbs_hg_alginstid_1933:
	def __init__(self, constants,containingscenario,currentchemical,sendingcompartment, receivingcompartment,dict_inputs):
		self.name='time-dependent partition from root to root zone, interacts with bulk soil - grasses/herbs, hg(alginstid_1933)'
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
		self.receivingcompartmentcategory='abiotic | soil | root zone | root zone - default'
		self.sendingcompartmentcategory='terrestrial plant | root | root - grasses/herbs'
		self.sendingchemicalname='replaceme'
		self.dict_inputs=dict_inputs
		
	@property
	def k2(self):
		return (self.k1 * self.sendingcompartment.chemical_root_rootzonepartitioningbulksoil_partitioncoefficient)
	
	@property
	def k1(self):
		return (-log(1 - self.sendingcompartment.chemical_root_rootzonepartitioningbulksoil_alphaofsteadystate) / self.sendingcompartment.chemical_root_rootzonepartitioningbulksoil_timetoreachalphaofsteadystate)
	
	@property
	def transferfactor(self):
		try:
			r=self.sendingcompartment.allowexchange_forother * self.k1
		except:
			r=nan
		return (r)

class time_dependent_partition_from_root_to_root_zone_interacts_with_soil_pore_water_agriculture_organics:
	def __init__(self, constants,containingscenario,currentchemical,sendingcompartment, receivingcompartment,dict_inputs):
		self.name='time-dependent partition from root to root zone, interacts with soil pore water - agriculture, organics'
		self.constants=constants
		self.containingscenario=containingscenario
		self.currentchemical=currentchemical
		self.sendingcompartment=sendingcompartment
		self.receivingcompartment=receivingcompartment
		self.category='time-dependent partition'
		self.chemicalcategory='organic'
		self.doestransformchemical='False'
		self.transportchemical='True'
		self.enabled='True'
		self.isdefaultforcategory='True'
		self.mate='<unset>'
		self.receivingchemicalname='replaceme'
		self.receivingcompartmentcategory='abiotic | soil | root zone | root zone - default'
		self.sendingcompartmentcategory='terrestrial plant | root | root - agriculture - general'
		self.sendingchemicalname='replaceme'
		self.dict_inputs=dict_inputs
		
	@property
	def k2(self):
		return (self.k1 * (self.sendingcompartment.watercontent + self.sendingcompartment.lipidcontent * self.currentchemical.k_ow ** self.sendingcompartment.correctionexponent) * self.sendingcompartment.density)
	
	@property
	def k1(self):
		return (-log(1 - self.sendingcompartment.chemical_rootsoilwaterinteraction_alpha) / self.sendingcompartment.chemical_rootsoilwaterinteraction_t_alpha)
	
	@property
	def transferfactor(self):
		try:
			r=self.sendingcompartment.allowexchange_forother * self.k1
		except:
			r=nan
		return (r)

class time_dependent_partition_from_root_to_root_zone_interacts_with_soil_pore_water_grasses_herbs_organics_alginstid_1929:
	def __init__(self, constants,containingscenario,currentchemical,sendingcompartment, receivingcompartment,dict_inputs):
		self.name='time-dependent partition from root to root zone, interacts with soil pore water - grasses/herbs, organics(alginstid_1929)'
		self.constants=constants
		self.containingscenario=containingscenario
		self.currentchemical=currentchemical
		self.sendingcompartment=sendingcompartment
		self.receivingcompartment=receivingcompartment
		self.category='time-dependent partition'
		self.chemicalcategory='organic'
		self.doestransformchemical='False'
		self.transportchemical='True'
		self.enabled='True'
		self.isdefaultforcategory='True'
		self.mate='<unset>'
		self.receivingchemicalname='replaceme'
		self.receivingcompartmentcategory='abiotic | soil | root zone | root zone - default'
		self.sendingcompartmentcategory='terrestrial plant | root | root - grasses/herbs'
		self.sendingchemicalname='replaceme'
		self.dict_inputs=dict_inputs
		
	@property
	def k2(self):
		return (self.k1 * (self.sendingcompartment.watercontent + self.sendingcompartment.lipidcontent * self.currentchemical.k_ow ** self.sendingcompartment.correctionexponent) * self.sendingcompartment.density)
	
	@property
	def k1(self):
		return (-log(1 - self.sendingcompartment.chemical_rootsoilwaterinteraction_alpha) / self.sendingcompartment.chemical_rootsoilwaterinteraction_t_alpha)
	
	@property
	def transferfactor(self):
		try:
			r=self.sendingcompartment.allowexchange_forother * self.k1
		except:
			r=nan
		return (r)

class time_dependent_partition_from_root_zone_to_root_interacts_with_bulk_soil_agriculture_cd_alginstid_1953:
	def __init__(self, constants,containingscenario,currentchemical,sendingcompartment, receivingcompartment,dict_inputs):
		self.name='time-dependent partition from root zone to root, interacts with bulk soil - agriculture, cd(alginstid_1953)'
		self.constants=constants
		self.containingscenario=containingscenario
		self.currentchemical=currentchemical
		self.sendingcompartment=sendingcompartment
		self.receivingcompartment=receivingcompartment
		self.category='time-dependent partition'
		self.chemicalcategory='metals | cadmium'
		self.doestransformchemical='False'
		self.transportchemical='True'
		self.enabled='True'
		self.isdefaultforcategory='True'
		self.mate='<unset>'
		self.receivingchemicalname='replaceme'
		self.receivingcompartmentcategory='terrestrial plant | root | root - agriculture - general'
		self.sendingcompartmentcategory='abiotic | soil | root zone | root zone - default'
		self.sendingchemicalname='replaceme'
		self.dict_inputs=dict_inputs
		
	@property
	def k2(self):
		return (self.k1 * self.receivingcompartment.chemical_root_rootzonepartitioningbulksoil_partitioncoefficient)
	
	@property
	def k1(self):
		return (-log(1 - self.receivingcompartment.chemical_root_rootzonepartitioningbulksoil_alphaofsteadystate) / self.receivingcompartment.chemical_root_rootzonepartitioningbulksoil_timetoreachalphaofsteadystate)
	
	@property
	def transferfactor(self):
		try:
			r=self.receivingcompartment.allowexchange_forother * self.k2 * self.receivingcompartment.volume  / self.sendingcompartment.volume
		except:
			r=nan
		return (r)

class time_dependent_partition_from_root_zone_to_root_interacts_with_bulk_soil_agriculture_hg_alginstid_1953:
	def __init__(self, constants,containingscenario,currentchemical,sendingcompartment, receivingcompartment,dict_inputs):
		self.name='time-dependent partition from root zone to root, interacts with bulk soil - agriculture, hg(alginstid_1953)'
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
		self.receivingcompartmentcategory='terrestrial plant | root | root - agriculture - general'
		self.sendingcompartmentcategory='abiotic | soil | root zone | root zone - default'
		self.sendingchemicalname='replaceme'
		self.dict_inputs=dict_inputs
		
	@property
	def k2(self):
		return (self.k1 * self.receivingcompartment.chemical_root_rootzonepartitioningbulksoil_partitioncoefficient)
	
	@property
	def k1(self):
		return (-log(1 - self.receivingcompartment.chemical_root_rootzonepartitioningbulksoil_alphaofsteadystate) / self.receivingcompartment.chemical_root_rootzonepartitioningbulksoil_timetoreachalphaofsteadystate)
	
	@property
	def transferfactor(self):
		try:
			r=self.receivingcompartment.allowexchange_forother * self.k2 * self.receivingcompartment.volume  / self.sendingcompartment.volume
		except:
			r=nan
		return (r)

class time_dependent_partition_from_root_zone_to_root_interacts_with_bulk_soil_grasses_herbs_cd_alginstid_1952:
	def __init__(self, constants,containingscenario,currentchemical,sendingcompartment, receivingcompartment,dict_inputs):
		self.name='time-dependent partition from root zone to root, interacts with bulk soil - grasses/herbs,cd(alginstid_1952)'
		self.constants=constants
		self.containingscenario=containingscenario
		self.currentchemical=currentchemical
		self.sendingcompartment=sendingcompartment
		self.receivingcompartment=receivingcompartment
		self.category='time-dependent partition'
		self.chemicalcategory='metals | cadmium'
		self.doestransformchemical='False'
		self.transportchemical='True'
		self.enabled='True'
		self.isdefaultforcategory='True'
		self.mate='<unset>'
		self.receivingchemicalname='replaceme'
		self.receivingcompartmentcategory='terrestrial plant | root | root - grasses/herbs'
		self.sendingcompartmentcategory='abiotic | soil | root zone | root zone - default'
		self.sendingchemicalname='replaceme'
		self.dict_inputs=dict_inputs
		
	@property
	def k2(self):
		return (self.k1 * self.receivingcompartment.chemical_root_rootzonepartitioningbulksoil_partitioncoefficient)
	
	@property
	def k1(self):
		return (-log(1 - self.receivingcompartment.chemical_root_rootzonepartitioningbulksoil_alphaofsteadystate) / self.receivingcompartment.chemical_root_rootzonepartitioningbulksoil_timetoreachalphaofsteadystate)
	
	@property
	def transferfactor(self):
		try:
			r=self.receivingcompartment.allowexchange_forother * self.k2 * self.receivingcompartment.volume  / self.sendingcompartment.volume
		except:
			r=nan
		return (r)

class time_dependent_partition_from_root_zone_to_root_interacts_with_bulk_soil_grasses_herbs_hg_alginstid_1952:
	def __init__(self, constants,containingscenario,currentchemical,sendingcompartment, receivingcompartment,dict_inputs):
		self.name='time-dependent partition from root zone to root, interacts with bulk soil - grasses/herbs,hg(alginstid_1952)'
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
		self.receivingcompartmentcategory='terrestrial plant | root | root - grasses/herbs'
		self.sendingcompartmentcategory='abiotic | soil | root zone | root zone - default'
		self.sendingchemicalname='replaceme'
		self.dict_inputs=dict_inputs
		
	@property
	def k2(self):
		return (self.k1 * self.receivingcompartment.chemical_root_rootzonepartitioningbulksoil_partitioncoefficient)
	
	@property
	def k1(self):
		return (-log(1 - self.receivingcompartment.chemical_root_rootzonepartitioningbulksoil_alphaofsteadystate) / self.receivingcompartment.chemical_root_rootzonepartitioningbulksoil_timetoreachalphaofsteadystate)
	
	@property
	def transferfactor(self):
		try:
			r=self.receivingcompartment.allowexchange_forother * self.k2 * self.receivingcompartment.volume  / self.sendingcompartment.volume
		except:
			r=nan
		return (r)

class time_dependent_partition_from_root_zone_to_root_interacts_with_soil_pore_water_agriculture_organics:
	def __init__(self, constants,containingscenario,currentchemical,sendingcompartment, receivingcompartment,dict_inputs):
		self.name='time-dependent partition from root zone to root, interacts with soil pore water - agriculture, organics'
		self.constants=constants
		self.containingscenario=containingscenario
		self.currentchemical=currentchemical
		self.sendingcompartment=sendingcompartment
		self.receivingcompartment=receivingcompartment
		self.category='time-dependent partition'
		self.chemicalcategory='organic'
		self.doestransformchemical='False'
		self.transportchemical='True'
		self.enabled='True'
		self.isdefaultforcategory='True'
		self.mate='<unset>'
		self.receivingchemicalname='benzo(a)pyrene'
		self.receivingcompartmentcategory='terrestrial plant | root | root - agriculture - general'
		self.sendingcompartmentcategory='abiotic | soil | root zone | root zone - default'
		self.sendingchemicalname='benzo(a)pyrene'
		self.dict_inputs=dict_inputs
		
	@property
	def k2(self):
		return (self.k1 * (self.receivingcompartment.watercontent + self.receivingcompartment.lipidcontent * self.currentchemical.k_ow ** self.receivingcompartment.correctionexponent) * self.receivingcompartment.density)
	
	@property
	def k1(self):
		return (-log(1 - self.receivingcompartment.chemical_rootsoilwaterinteraction_alpha) / self.receivingcompartment.chemical_rootsoilwaterinteraction_t_alpha)
	
	@property
	def transferfactor(self):
		try:
			r=self.receivingcompartment.allowexchange_forother * self.k2 * self.constants.m3_per_l * self.receivingcompartment.volume * (self.currentchemical.z_purewater / self.sendingcompartment.chemical_z_total) / self.sendingcompartment.volume
		except:
			r=nan
		return (r)

class time_dependent_partition_from_root_zone_to_root_interacts_with_soil_pore_water_grasses_herbs_organics_alginstid_1949:
	def __init__(self, constants,containingscenario,currentchemical,sendingcompartment, receivingcompartment,dict_inputs):
		self.name='time-dependent partition from root zone to root, interacts with soil pore water - grasses/herbs, organics(alginstid_1949)'
		self.constants=constants
		self.containingscenario=containingscenario
		self.currentchemical=currentchemical
		self.sendingcompartment=sendingcompartment
		self.receivingcompartment=receivingcompartment
		self.category='time-dependent partition'
		self.chemicalcategory='organic'
		self.doestransformchemical='False'
		self.transportchemical='True'
		self.enabled='True'
		self.isdefaultforcategory='True'
		self.mate='<unset>'
		self.receivingchemicalname='benzo(a)pyrene'
		self.receivingcompartmentcategory='terrestrial plant | root | root - grasses/herbs'
		self.sendingcompartmentcategory='abiotic | soil | root zone | root zone - default'
		self.sendingchemicalname='benzo(a)pyrene'
		self.dict_inputs=dict_inputs
		
	@property
	def k2(self):
		return (self.k1 * (self.receivingcompartment.watercontent + self.receivingcompartment.lipidcontent * self.currentchemical.k_ow ** self.receivingcompartment.correctionexponent) * self.receivingcompartment.density)
	
	@property
	def k1(self):
		return (-log(1 - self.receivingcompartment.chemical_rootsoilwaterinteraction_alpha) / self.receivingcompartment.chemical_rootsoilwaterinteraction_t_alpha)
	
	@property
	def transferfactor(self):
		try:
			r=self.receivingcompartment.allowexchange_forother * self.k2 * self.constants.m3_per_l * self.receivingcompartment.volume * (self.currentchemical.z_purewater / self.sendingcompartment.chemical_z_total) / self.sendingcompartment.volume
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
	def k2(self):
		return (self.k1 * self.receivingcompartment.chemical_sedimentpartitioning_partitioncoefficient)
	
	@property
	def k1(self):
		return (-log(1 - self.receivingcompartment.chemical_sedimentpartitioning_alphaofequilibrium) / self.receivingcompartment.chemical_sedimentpartitioning_timetoreachalphaofequilibrium)
	
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
	def k2(self):
		return (self.k1 * self.receivingcompartment.chemical_watercolumndissolvedpartitioning_partitioncoefficient)
	
	@property
	def k1(self):
		return (-log(1 - self.receivingcompartment.chemical_watercolumndissolvedpartitioning_alphaofequilibrium) / self.receivingcompartment.chemical_watercolumndissolvedpartitioning_timetoreachalphaofequilibrium)
	
	@property
	def transferfactor(self):
		try:
			r=(self.k2 * self.receivingcompartment.totalmass * (self.sendingcompartment.chemical_fractionmass_dissolved/ self.sendingcompartment.volume))*(1/1000)
		except:
			r=nan
		return (r)

class transfer_from_leaf_particle_on_surface_to_leaf_cd_alginstid_1250:
	def __init__(self, constants,containingscenario,currentchemical,sendingcompartment, receivingcompartment,dict_inputs):
		self.name='transfer from leaf particle on surface to leaf, cd(alginstid_1250)'
		self.constants=constants
		self.containingscenario=containingscenario
		self.currentchemical=currentchemical
		self.sendingcompartment=sendingcompartment
		self.receivingcompartment=receivingcompartment
		self.category='general transfer'
		self.chemicalcategory='metals | cadmium'
		self.doestransformchemical='False'
		self.transportchemical='True'
		self.enabled='True'
		self.isdefaultforcategory='True'
		self.mate='<unset>'
		self.receivingchemicalname='replaceme'
		self.receivingcompartmentcategory='terrestrial plant | leaf'
		self.sendingcompartmentcategory='terrestrial plant | leaf particle'
		self.sendingchemicalname='replaceme'
		self.dict_inputs=dict_inputs
		
	@property
	def compartmentrelationship(self):
		return ("in_same_composite")
	
	@property
	def transferfactor(self):
		try:
			r=self.receivingcompartment.allowexchange_forother *  self.sendingcompartment.chemical_transferfactortoleaf
		except:
			r=nan
		return (r)

class transfer_from_leaf_particle_on_surface_to_leaf_hg_alginstid_1250:
	def __init__(self, constants,containingscenario,currentchemical,sendingcompartment, receivingcompartment,dict_inputs):
		self.name='transfer from leaf particle on surface to leaf, hg(alginstid_1250)'
		self.constants=constants
		self.containingscenario=containingscenario
		self.currentchemical=currentchemical
		self.sendingcompartment=sendingcompartment
		self.receivingcompartment=receivingcompartment
		self.category='general transfer'
		self.chemicalcategory='metals | mercury'
		self.doestransformchemical='False'
		self.transportchemical='True'
		self.enabled='True'
		self.isdefaultforcategory='True'
		self.mate='<unset>'
		self.receivingchemicalname='replaceme'
		self.receivingcompartmentcategory='terrestrial plant | leaf'
		self.sendingcompartmentcategory='terrestrial plant | leaf particle'
		self.sendingchemicalname='replaceme'
		self.dict_inputs=dict_inputs
		
	@property
	def compartmentrelationship(self):
		return ("in_same_composite")
	
	@property
	def transferfactor(self):
		try:
			r=self.receivingcompartment.allowexchange_forother *  self.sendingcompartment.chemical_transferfactortoleaf
		except:
			r=nan
		return (r)

class transfer_from_leaf_particle_on_surface_to_leaf_organic_alginstid_1250:
	def __init__(self, constants,containingscenario,currentchemical,sendingcompartment, receivingcompartment,dict_inputs):
		self.name='transfer from leaf particle on surface to leaf, organic(alginstid_1250)'
		self.constants=constants
		self.containingscenario=containingscenario
		self.currentchemical=currentchemical
		self.sendingcompartment=sendingcompartment
		self.receivingcompartment=receivingcompartment
		self.category='general transfer'
		self.chemicalcategory='organic'
		self.doestransformchemical='False'
		self.transportchemical='True'
		self.enabled='True'
		self.isdefaultforcategory='True'
		self.mate='<unset>'
		self.receivingchemicalname='replaceme'
		self.receivingcompartmentcategory='terrestrial plant | leaf'
		self.sendingcompartmentcategory='terrestrial plant | leaf particle'
		self.sendingchemicalname='replaceme'
		self.dict_inputs=dict_inputs
		
	@property
	def compartmentrelationship(self):
		return ("in_same_composite")
	
	@property
	def transferfactor(self):
		try:
			r=self.receivingcompartment.allowexchange_forother *  self.sendingcompartment.chemical_transferfactortoleaf
		except:
			r=nan
		return (r)

class transfer_from_leaf_to_leaf_particle_on_surface_cd_alginstid_1255:
	def __init__(self, constants,containingscenario,currentchemical,sendingcompartment, receivingcompartment,dict_inputs):
		self.name='transfer from leaf to leaf particle on surface, cd(alginstid_1255)'
		self.constants=constants
		self.containingscenario=containingscenario
		self.currentchemical=currentchemical
		self.sendingcompartment=sendingcompartment
		self.receivingcompartment=receivingcompartment
		self.category='general transfer'
		self.chemicalcategory='metals | cadmium'
		self.doestransformchemical='False'
		self.transportchemical='True'
		self.enabled='True'
		self.isdefaultforcategory='True'
		self.mate='<unset>'
		self.receivingchemicalname='replaceme'
		self.receivingcompartmentcategory='terrestrial plant | leaf particle'
		self.sendingcompartmentcategory='terrestrial plant | leaf'
		self.sendingchemicalname='replaceme'
		self.dict_inputs=dict_inputs
		
	@property
	def compartmentrelationship(self):
		return ("in_same_composite")
	
	@property
	def transferfactor(self):
		try:
			r=self.sendingcompartment.allowexchange_forother * self.sendingcompartment.chemical_transferfactortoleafparticle
		except:
			r=nan
		return (r)

class transfer_from_leaf_to_leaf_particle_on_surface_hg_alginstid_1255:
	def __init__(self, constants,containingscenario,currentchemical,sendingcompartment, receivingcompartment,dict_inputs):
		self.name='transfer from leaf to leaf particle on surface, hg(alginstid_1255)'
		self.constants=constants
		self.containingscenario=containingscenario
		self.currentchemical=currentchemical
		self.sendingcompartment=sendingcompartment
		self.receivingcompartment=receivingcompartment
		self.category='general transfer'
		self.chemicalcategory='metals | mercury'
		self.doestransformchemical='False'
		self.transportchemical='True'
		self.enabled='True'
		self.isdefaultforcategory='True'
		self.mate='<unset>'
		self.receivingchemicalname='replaceme'
		self.receivingcompartmentcategory='terrestrial plant | leaf particle'
		self.sendingcompartmentcategory='terrestrial plant | leaf'
		self.sendingchemicalname='replaceme'
		self.dict_inputs=dict_inputs
		
	@property
	def compartmentrelationship(self):
		return ("in_same_composite")
	
	@property
	def transferfactor(self):
		try:
			r=self.sendingcompartment.allowexchange_forother * self.sendingcompartment.chemical_transferfactortoleafparticle
		except:
			r=nan
		return (r)

class transfer_from_leaf_to_leaf_particle_on_surface_organic_alginstid_1255:
	def __init__(self, constants,containingscenario,currentchemical,sendingcompartment, receivingcompartment,dict_inputs):
		self.name='transfer from leaf to leaf particle on surface, organic(alginstid_1255)'
		self.constants=constants
		self.containingscenario=containingscenario
		self.currentchemical=currentchemical
		self.sendingcompartment=sendingcompartment
		self.receivingcompartment=receivingcompartment
		self.category='general transfer'
		self.chemicalcategory='organic'
		self.doestransformchemical='False'
		self.transportchemical='True'
		self.enabled='True'
		self.isdefaultforcategory='True'
		self.mate='<unset>'
		self.receivingchemicalname='replaceme'
		self.receivingcompartmentcategory='terrestrial plant | leaf particle'
		self.sendingcompartmentcategory='terrestrial plant | leaf'
		self.sendingchemicalname='replaceme'
		self.dict_inputs=dict_inputs
		
	@property
	def compartmentrelationship(self):
		return ("in_same_composite")
	
	@property
	def transferfactor(self):
		try:
			r=self.sendingcompartment.allowexchange_forother * self.sendingcompartment.chemical_transferfactortoleafparticle
		except:
			r=nan
		return (r)

class transfer_from_leaf_to_stem_agriculture_cd_alginstid_1265:
	def __init__(self, constants,containingscenario,currentchemical,sendingcompartment, receivingcompartment,dict_inputs):
		self.name='transfer from leaf to stem - agriculture, cd(alginstid_1265)'
		self.constants=constants
		self.containingscenario=containingscenario
		self.currentchemical=currentchemical
		self.sendingcompartment=sendingcompartment
		self.receivingcompartment=receivingcompartment
		self.category='advection'
		self.chemicalcategory='metals | cadmium'
		self.doestransformchemical='False'
		self.transportchemical='True'
		self.enabled='True'
		self.isdefaultforcategory='True'
		self.mate='<unset>'
		self.receivingchemicalname='replaceme'
		self.receivingcompartmentcategory='terrestrial plant | stem | stem - agriculture - general'
		self.sendingcompartmentcategory='terrestrial plant | leaf | leaf - agriculture - general'
		self.sendingchemicalname='replaceme'
		self.dict_inputs=dict_inputs
		
	@property
	def compartmentrelationship(self):
		return ("in_same_composite")
	
	@property
	def partitioncoefficientbetweenleavesandphloemwater(self):
		return (self.sendingcompartment.watercontent * self.sendingcompartment.density/self.receivingcompartment.phloemdensity)
	
	@property
	def transferfactor(self):
		try:
			r=( self.sendingcompartment.allowexchange_forother *(self.receivingcompartment.phloemflowrate/self.partitioncoefficientbetweenleavesandphloemwater)/self.sendingcompartment.volume ) if self.sendingcompartment.volume > 0 else 0
		except:
			r=nan
		return (r)

class transfer_from_leaf_to_stem_agriculture_hg_alginstid_1265:
	def __init__(self, constants,containingscenario,currentchemical,sendingcompartment, receivingcompartment,dict_inputs):
		self.name='transfer from leaf to stem - agriculture, hg(alginstid_1265)'
		self.constants=constants
		self.containingscenario=containingscenario
		self.currentchemical=currentchemical
		self.sendingcompartment=sendingcompartment
		self.receivingcompartment=receivingcompartment
		self.category='advection'
		self.chemicalcategory='metals | mercury'
		self.doestransformchemical='False'
		self.transportchemical='True'
		self.enabled='True'
		self.isdefaultforcategory='True'
		self.mate='<unset>'
		self.receivingchemicalname='replaceme'
		self.receivingcompartmentcategory='terrestrial plant | stem | stem - agriculture - general'
		self.sendingcompartmentcategory='terrestrial plant | leaf | leaf - agriculture - general'
		self.sendingchemicalname='replaceme'
		self.dict_inputs=dict_inputs
		
	@property
	def compartmentrelationship(self):
		return ("in_same_composite")
	
	@property
	def partitioncoefficientbetweenleavesandphloemwater(self):
		return ((self.sendingcompartment.watercontent + self.sendingcompartment.lipidcontent*self.currentchemical.k_ow ** self.sendingcompartment.correctionexponent)* self.sendingcompartment.density/self.receivingcompartment.phloemdensity)
	
	@property
	def transferfactor(self):
		try:
			r=( self.sendingcompartment.allowexchange_forother *(self.receivingcompartment.phloemflowrate/self.partitioncoefficientbetweenleavesandphloemwater)/self.sendingcompartment.volume ) if self.sendingcompartment.volume > 0 else 0
		except:
			r=nan
		return (r)

class transfer_from_leaf_to_stem_agriculture_organic_alginstid_1265:
	def __init__(self, constants,containingscenario,currentchemical,sendingcompartment, receivingcompartment,dict_inputs):
		self.name='transfer from leaf to stem - agriculture, organic(alginstid_1265)'
		self.constants=constants
		self.containingscenario=containingscenario
		self.currentchemical=currentchemical
		self.sendingcompartment=sendingcompartment
		self.receivingcompartment=receivingcompartment
		self.category='advection'
		self.chemicalcategory='organic'
		self.doestransformchemical='False'
		self.transportchemical='True'
		self.enabled='True'
		self.isdefaultforcategory='True'
		self.mate='<unset>'
		self.receivingchemicalname='replaceme'
		self.receivingcompartmentcategory='terrestrial plant | stem | stem - agriculture - general'
		self.sendingcompartmentcategory='terrestrial plant | leaf | leaf - agriculture - general'
		self.sendingchemicalname='replaceme'
		self.dict_inputs=dict_inputs
		
	@property
	def compartmentrelationship(self):
		return ("in_same_composite")
	
	@property
	def partitioncoefficientbetweenleavesandphloemwater(self):
		return ((self.sendingcompartment.watercontent + self.sendingcompartment.lipidcontent*self.currentchemical.k_ow ** self.sendingcompartment.correctionexponent)* self.sendingcompartment.density/self.receivingcompartment.phloemdensity)
	
	@property
	def transferfactor(self):
		try:
			r=( self.sendingcompartment.allowexchange_forother *(self.receivingcompartment.phloemflowrate/self.partitioncoefficientbetweenleavesandphloemwater)/self.sendingcompartment.volume ) if self.sendingcompartment.volume > 0 else 0
		except:
			r=nan
		return (r)

class transfer_from_leaf_to_stem_grasses_herbs_cd:
	def __init__(self, constants,containingscenario,currentchemical,sendingcompartment, receivingcompartment,dict_inputs):
		self.name='transfer from leaf to stem - grasses/herbs, cd'
		self.constants=constants
		self.containingscenario=containingscenario
		self.currentchemical=currentchemical
		self.sendingcompartment=sendingcompartment
		self.receivingcompartment=receivingcompartment
		self.category='advection'
		self.chemicalcategory='metals | cadmium'
		self.doestransformchemical='False'
		self.transportchemical='True'
		self.enabled='True'
		self.isdefaultforcategory='True'
		self.mate='<unset>'
		self.receivingchemicalname='replaceme'
		self.receivingcompartmentcategory='terrestrial plant | stem | stem - grasses/herbs'
		self.sendingcompartmentcategory='terrestrial plant | leaf | leaf - grasses/herbs'
		self.sendingchemicalname='replaceme'
		self.dict_inputs=dict_inputs
		
	@property
	def compartmentrelationship(self):
		return ("in_same_composite")
	
	@property
	def partitioncoefficientbetweenleavesandphloemwater(self):
		return (self.sendingcompartment.watercontent * self.sendingcompartment.density/self.receivingcompartment.phloemdensity)
	
	@property
	def transferfactor(self):
		try:
			r=( self.sendingcompartment.allowexchange_forother *(self.receivingcompartment.phloemflowrate/self.partitioncoefficientbetweenleavesandphloemwater)/self.sendingcompartment.volume ) if self.sendingcompartment.volume > 0 else 0
		except:
			r=nan
		return (r)

class transfer_from_leaf_to_stem_grasses_herbs_hg:
	def __init__(self, constants,containingscenario,currentchemical,sendingcompartment, receivingcompartment,dict_inputs):
		self.name='transfer from leaf to stem - grasses/herbs, hg'
		self.constants=constants
		self.containingscenario=containingscenario
		self.currentchemical=currentchemical
		self.sendingcompartment=sendingcompartment
		self.receivingcompartment=receivingcompartment
		self.category='advection'
		self.chemicalcategory='metals | mercury'
		self.doestransformchemical='False'
		self.transportchemical='True'
		self.enabled='True'
		self.isdefaultforcategory='True'
		self.mate='<unset>'
		self.receivingchemicalname='replaceme'
		self.receivingcompartmentcategory='terrestrial plant | stem | stem - grasses/herbs'
		self.sendingcompartmentcategory='terrestrial plant | leaf | leaf - grasses/herbs'
		self.sendingchemicalname='replaceme'
		self.dict_inputs=dict_inputs
		
	@property
	def compartmentrelationship(self):
		return ("in_same_composite")
	
	@property
	def partitioncoefficientbetweenleavesandphloemwater(self):
		return ((self.sendingcompartment.watercontent + self.sendingcompartment.lipidcontent*self.currentchemical.k_ow ** self.sendingcompartment.correctionexponent)* self.sendingcompartment.density/self.receivingcompartment.phloemdensity)
	
	@property
	def transferfactor(self):
		try:
			r=( self.sendingcompartment.allowexchange_forother *(self.receivingcompartment.phloemflowrate/self.partitioncoefficientbetweenleavesandphloemwater)/self.sendingcompartment.volume ) if self.sendingcompartment.volume > 0 else 0
		except:
			r=nan
		return (r)

class transfer_from_leaf_to_stem_grasses_herbs_organic:
	def __init__(self, constants,containingscenario,currentchemical,sendingcompartment, receivingcompartment,dict_inputs):
		self.name='transfer from leaf to stem - grasses/herbs, organic'
		self.constants=constants
		self.containingscenario=containingscenario
		self.currentchemical=currentchemical
		self.sendingcompartment=sendingcompartment
		self.receivingcompartment=receivingcompartment
		self.category='advection'
		self.chemicalcategory='organic'
		self.doestransformchemical='False'
		self.transportchemical='True'
		self.enabled='True'
		self.isdefaultforcategory='True'
		self.mate='<unset>'
		self.receivingchemicalname='replaceme'
		self.receivingcompartmentcategory='terrestrial plant | stem | stem - grasses/herbs'
		self.sendingcompartmentcategory='terrestrial plant | leaf | leaf - grasses/herbs'
		self.sendingchemicalname='replaceme'
		self.dict_inputs=dict_inputs
		
	@property
	def compartmentrelationship(self):
		return ("in_same_composite")
	
	@property
	def partitioncoefficientbetweenleavesandphloemwater(self):
		return ((self.sendingcompartment.watercontent + self.sendingcompartment.lipidcontent*self.currentchemical.k_ow ** self.sendingcompartment.correctionexponent)* self.sendingcompartment.density/self.receivingcompartment.phloemdensity)
	
	@property
	def transferfactor(self):
		try:
			r=( self.sendingcompartment.allowexchange_forother *(self.receivingcompartment.phloemflowrate/self.partitioncoefficientbetweenleavesandphloemwater)/self.sendingcompartment.volume ) if self.sendingcompartment.volume > 0 else 0
		except:
			r=nan
		return (r)

class transfer_from_root_zone_to_stem_agriculture_cd:
	def __init__(self, constants,containingscenario,currentchemical,sendingcompartment, receivingcompartment,dict_inputs):
		self.name='transfer from root zone to stem - agriculture, cd'
		self.constants=constants
		self.containingscenario=containingscenario
		self.currentchemical=currentchemical
		self.sendingcompartment=sendingcompartment
		self.receivingcompartment=receivingcompartment
		self.category='advection'
		self.chemicalcategory='metals | cadmium'
		self.doestransformchemical='False'
		self.transportchemical='True'
		self.enabled='True'
		self.isdefaultforcategory='True'
		self.mate='<unset>'
		self.receivingchemicalname='replaceme'
		self.receivingcompartmentcategory='terrestrial plant | stem | stem - agriculture - general'
		self.sendingcompartmentcategory='abiotic | soil | root zone | root zone - default'
		self.sendingchemicalname='replaceme'
		self.dict_inputs=dict_inputs
		
	@property
	def transferfactor(self):
		try:
			r=self.receivingcompartment.allowexchange_forother * self.receivingcompartment.flowrateoftranspiredwater * self.receivingcompartment.chemical_tscf * (self.sendingcompartment.chemical_fractionmass_dissolved/self.sendingcompartment.chemical_volumefraction_liquid)/self.sendingcompartment.volume
		except:
			r=nan
		return (r)

class transfer_from_root_zone_to_stem_agriculture_hg:
	def __init__(self, constants,containingscenario,currentchemical,sendingcompartment, receivingcompartment,dict_inputs):
		self.name='transfer from root zone to stem - agriculture, hg'
		self.constants=constants
		self.containingscenario=containingscenario
		self.currentchemical=currentchemical
		self.sendingcompartment=sendingcompartment
		self.receivingcompartment=receivingcompartment
		self.category='advection'
		self.chemicalcategory='metals | mercury'
		self.doestransformchemical='False'
		self.transportchemical='True'
		self.enabled='True'
		self.isdefaultforcategory='True'
		self.mate='<unset>'
		self.receivingchemicalname='replaceme'
		self.receivingcompartmentcategory='terrestrial plant | stem | stem - agriculture - general'
		self.sendingcompartmentcategory='abiotic | soil | root zone | root zone - default'
		self.sendingchemicalname='replaceme'
		self.dict_inputs=dict_inputs
		
	@property
	def transferfactor(self):
		try:
			r=self.receivingcompartment.allowexchange_forother * self.receivingcompartment.flowrateoftranspiredwater * self.receivingcompartment.chemical_tscf * (self.sendingcompartment.chemical_fractionmass_dissolved/self.sendingcompartment.chemical_volumefraction_liquid)/self.sendingcompartment.volume
		except:
			r=nan
		return (r)

class transfer_from_root_zone_to_stem_agriculture_organic:
	def __init__(self, constants,containingscenario,currentchemical,sendingcompartment, receivingcompartment,dict_inputs):
		self.name='transfer from root zone to stem - agriculture, organic'
		self.constants=constants
		self.containingscenario=containingscenario
		self.currentchemical=currentchemical
		self.sendingcompartment=sendingcompartment
		self.receivingcompartment=receivingcompartment
		self.category='advection'
		self.chemicalcategory='organic'
		self.doestransformchemical='False'
		self.transportchemical='True'
		self.enabled='True'
		self.isdefaultforcategory='True'
		self.mate='<unset>'
		self.receivingchemicalname='replaceme'
		self.receivingcompartmentcategory='terrestrial plant | stem | stem - agriculture - general'
		self.sendingcompartmentcategory='abiotic | soil | root zone | root zone - default'
		self.sendingchemicalname='replaceme'
		self.dict_inputs=dict_inputs
		
	@property
	def transferfactor(self):
		try:
			r=self.receivingcompartment.allowexchange_forother * self.receivingcompartment.flowrateoftranspiredwater * self.receivingcompartment.chemical_tscf * (self.sendingcompartment.chemical_fractionmass_dissolved/self.sendingcompartment.chemical_volumefraction_liquid)/self.sendingcompartment.volume
		except:
			r=nan
		return (r)

class transfer_from_root_zone_to_stem_grasses_herbs_cd_alginstid_1944:
	def __init__(self, constants,containingscenario,currentchemical,sendingcompartment, receivingcompartment,dict_inputs):
		self.name='transfer from root zone to stem - grasses/herbs, cd(alginstid_1944)'
		self.constants=constants
		self.containingscenario=containingscenario
		self.currentchemical=currentchemical
		self.sendingcompartment=sendingcompartment
		self.receivingcompartment=receivingcompartment
		self.category='advection'
		self.chemicalcategory='metals | cadmium'
		self.doestransformchemical='False'
		self.transportchemical='True'
		self.enabled='True'
		self.isdefaultforcategory='True'
		self.mate='<unset>'
		self.receivingchemicalname='replaceme'
		self.receivingcompartmentcategory='terrestrial plant | stem | stem - grasses/herbs'
		self.sendingcompartmentcategory='abiotic | soil | root zone | root zone - default'
		self.sendingchemicalname='replaceme'
		self.dict_inputs=dict_inputs
		
	@property
	def transferfactor(self):
		try:
			r=self.receivingcompartment.allowexchange_forother * self.receivingcompartment.flowrateoftranspiredwater * self.receivingcompartment.chemical_tscf * (self.sendingcompartment.chemical_fractionmass_dissolved/self.sendingcompartment.chemical_volumefraction_liquid)/self.sendingcompartment.volume
		except:
			r=nan
		return (r)

class transfer_from_root_zone_to_stem_grasses_herbs_hg_alginstid_1944:
	def __init__(self, constants,containingscenario,currentchemical,sendingcompartment, receivingcompartment,dict_inputs):
		self.name='transfer from root zone to stem - grasses/herbs, hg(alginstid_1944)'
		self.constants=constants
		self.containingscenario=containingscenario
		self.currentchemical=currentchemical
		self.sendingcompartment=sendingcompartment
		self.receivingcompartment=receivingcompartment
		self.category='advection'
		self.chemicalcategory='metals | mercury'
		self.doestransformchemical='False'
		self.transportchemical='True'
		self.enabled='True'
		self.isdefaultforcategory='True'
		self.mate='<unset>'
		self.receivingchemicalname='replaceme'
		self.receivingcompartmentcategory='terrestrial plant | stem | stem - grasses/herbs'
		self.sendingcompartmentcategory='abiotic | soil | root zone | root zone - default'
		self.sendingchemicalname='replaceme'
		self.dict_inputs=dict_inputs
		
	@property
	def transferfactor(self):
		try:
			r=self.receivingcompartment.allowexchange_forother * self.receivingcompartment.flowrateoftranspiredwater * self.receivingcompartment.chemical_tscf * (self.sendingcompartment.chemical_fractionmass_dissolved/self.sendingcompartment.chemical_volumefraction_liquid)/self.sendingcompartment.volume
		except:
			r=nan
		return (r)

class transfer_from_root_zone_to_stem_grasses_herbs_organics_alginstid_1944:
	def __init__(self, constants,containingscenario,currentchemical,sendingcompartment, receivingcompartment,dict_inputs):
		self.name='transfer from root zone to stem - grasses/herbs, organics(alginstid_1944)'
		self.constants=constants
		self.containingscenario=containingscenario
		self.currentchemical=currentchemical
		self.sendingcompartment=sendingcompartment
		self.receivingcompartment=receivingcompartment
		self.category='advection'
		self.chemicalcategory='organic'
		self.doestransformchemical='False'
		self.transportchemical='True'
		self.enabled='True'
		self.isdefaultforcategory='True'
		self.mate='<unset>'
		self.receivingchemicalname='replaceme'
		self.receivingcompartmentcategory='terrestrial plant | stem | stem - grasses/herbs'
		self.sendingcompartmentcategory='abiotic | soil | root zone | root zone - default'
		self.sendingchemicalname='replaceme'
		self.dict_inputs=dict_inputs
		
	@property
	def transferfactor(self):
		try:
			r=self.receivingcompartment.allowexchange_forother * self.receivingcompartment.flowrateoftranspiredwater * self.receivingcompartment.chemical_tscf * (self.sendingcompartment.chemical_fractionmass_dissolved/self.sendingcompartment.chemical_volumefraction_liquid)/self.sendingcompartment.volume
		except:
			r=nan
		return (r)

class transfer_from_stem_to_leaf_agriculture_cd:
	def __init__(self, constants,containingscenario,currentchemical,sendingcompartment, receivingcompartment,dict_inputs):
		self.name='transfer from stem to leaf - agriculture, cd'
		self.constants=constants
		self.containingscenario=containingscenario
		self.currentchemical=currentchemical
		self.sendingcompartment=sendingcompartment
		self.receivingcompartment=receivingcompartment
		self.category='advection'
		self.chemicalcategory='metals | cadmium'
		self.doestransformchemical='False'
		self.transportchemical='True'
		self.enabled='True'
		self.isdefaultforcategory='True'
		self.mate='<unset>'
		self.receivingchemicalname='replaceme'
		self.receivingcompartmentcategory='terrestrial plant | leaf | leaf - agriculture - general'
		self.sendingcompartmentcategory='terrestrial plant | stem | stem - agriculture - general'
		self.sendingchemicalname='replaceme'
		self.dict_inputs=dict_inputs
		
	@property
	def partitioncoefficientbetweenstemandxylemwater(self):
		return (self.sendingcompartment.watercontent  * self.sendingcompartment.density/self.sendingcompartment.xylemdensity)
	
	@property
	def compartmentrelationship(self):
		return ("in_same_composite")
	
	@property
	def transferfactor(self):
		try:
			r=self.receivingcompartment.allowexchange_forother * (self.sendingcompartment.flowrateoftranspiredwater/self.partitioncoefficientbetweenstemandxylemwater)/self.sendingcompartment.volume
		except:
			r=nan
		return (r)

class transfer_from_stem_to_leaf_agriculture_hg:
	def __init__(self, constants,containingscenario,currentchemical,sendingcompartment, receivingcompartment,dict_inputs):
		self.name='transfer from stem to leaf - agriculture, hg'
		self.constants=constants
		self.containingscenario=containingscenario
		self.currentchemical=currentchemical
		self.sendingcompartment=sendingcompartment
		self.receivingcompartment=receivingcompartment
		self.category='advection'
		self.chemicalcategory='metals | mercury'
		self.doestransformchemical='False'
		self.transportchemical='True'
		self.enabled='True'
		self.isdefaultforcategory='True'
		self.mate='<unset>'
		self.receivingchemicalname='replaceme'
		self.receivingcompartmentcategory='terrestrial plant | leaf | leaf - agriculture - general'
		self.sendingcompartmentcategory='terrestrial plant | stem | stem - agriculture - general'
		self.sendingchemicalname='replaceme'
		self.dict_inputs=dict_inputs
		
	@property
	def partitioncoefficientbetweenstemandxylemwater(self):
		return ((self.sendingcompartment.watercontent  + self.sendingcompartment.lipidcontent*self.currentchemical.k_ow ** self.sendingcompartment.correctionexponent)* self.sendingcompartment.density/self.sendingcompartment.xylemdensity)
	
	@property
	def compartmentrelationship(self):
		return ("in_same_composite")
	
	@property
	def transferfactor(self):
		try:
			r=self.receivingcompartment.allowexchange_forother * (self.sendingcompartment.flowrateoftranspiredwater/self.partitioncoefficientbetweenstemandxylemwater)/self.sendingcompartment.volume
		except:
			r=nan
		return (r)

class transfer_from_stem_to_leaf_agriculture_organic:
	def __init__(self, constants,containingscenario,currentchemical,sendingcompartment, receivingcompartment,dict_inputs):
		self.name='transfer from stem to leaf - agriculture, organic'
		self.constants=constants
		self.containingscenario=containingscenario
		self.currentchemical=currentchemical
		self.sendingcompartment=sendingcompartment
		self.receivingcompartment=receivingcompartment
		self.category='advection'
		self.chemicalcategory='organic'
		self.doestransformchemical='False'
		self.transportchemical='True'
		self.enabled='True'
		self.isdefaultforcategory='True'
		self.mate='<unset>'
		self.receivingchemicalname='replaceme'
		self.receivingcompartmentcategory='terrestrial plant | leaf | leaf - agriculture - general'
		self.sendingcompartmentcategory='terrestrial plant | stem | stem - agriculture - general'
		self.sendingchemicalname='replaceme'
		self.dict_inputs=dict_inputs
		
	@property
	def partitioncoefficientbetweenstemandxylemwater(self):
		return ((self.sendingcompartment.watercontent  + self.sendingcompartment.lipidcontent*self.currentchemical.k_ow ** self.sendingcompartment.correctionexponent)* self.sendingcompartment.density/self.sendingcompartment.xylemdensity)
	
	@property
	def compartmentrelationship(self):
		return ("in_same_composite")
	
	@property
	def transferfactor(self):
		try:
			r=self.receivingcompartment.allowexchange_forother * (self.sendingcompartment.flowrateoftranspiredwater/self.partitioncoefficientbetweenstemandxylemwater)/self.sendingcompartment.volume
		except:
			r=nan
		return (r)

class transfer_from_stem_to_leaf_grasses_herbs_cd_alginstid_1260:
	def __init__(self, constants,containingscenario,currentchemical,sendingcompartment, receivingcompartment,dict_inputs):
		self.name='transfer from stem to leaf - grasses/herbs, cd(alginstid_1260)'
		self.constants=constants
		self.containingscenario=containingscenario
		self.currentchemical=currentchemical
		self.sendingcompartment=sendingcompartment
		self.receivingcompartment=receivingcompartment
		self.category='advection'
		self.chemicalcategory='metals | cadmium'
		self.doestransformchemical='False'
		self.transportchemical='True'
		self.enabled='True'
		self.isdefaultforcategory='True'
		self.mate='<unset>'
		self.receivingchemicalname='replaceme'
		self.receivingcompartmentcategory='terrestrial plant | leaf | leaf - grasses/herbs'
		self.sendingcompartmentcategory='terrestrial plant | stem | stem - grasses/herbs'
		self.sendingchemicalname='replaceme'
		self.dict_inputs=dict_inputs
		
	@property
	def partitioncoefficientbetweenstemandxylemwater(self):
		return (self.sendingcompartment.watercontent  * self.sendingcompartment.density/self.sendingcompartment.xylemdensity)
	
	@property
	def compartmentrelationship(self):
		return ("in_same_composite")
	
	@property
	def transferfactor(self):
		try:
			r=self.receivingcompartment.allowexchange_forother * (self.sendingcompartment.flowrateoftranspiredwater/self.partitioncoefficientbetweenstemandxylemwater)/self.sendingcompartment.volume
		except:
			r=nan
		return (r)

class transfer_from_stem_to_leaf_grasses_herbs_hg_alginstid_1260:
	def __init__(self, constants,containingscenario,currentchemical,sendingcompartment, receivingcompartment,dict_inputs):
		self.name='transfer from stem to leaf - grasses/herbs, hg(alginstid_1260)'
		self.constants=constants
		self.containingscenario=containingscenario
		self.currentchemical=currentchemical
		self.sendingcompartment=sendingcompartment
		self.receivingcompartment=receivingcompartment
		self.category='advection'
		self.chemicalcategory='metals | mercury'
		self.doestransformchemical='False'
		self.transportchemical='True'
		self.enabled='True'
		self.isdefaultforcategory='True'
		self.mate='<unset>'
		self.receivingchemicalname='replaceme'
		self.receivingcompartmentcategory='terrestrial plant | leaf | leaf - grasses/herbs'
		self.sendingcompartmentcategory='terrestrial plant | stem | stem - grasses/herbs'
		self.sendingchemicalname='replaceme'
		self.dict_inputs=dict_inputs
		
	@property
	def partitioncoefficientbetweenstemandxylemwater(self):
		return ((self.sendingcompartment.watercontent  + self.sendingcompartment.lipidcontent*self.currentchemical.k_ow ** self.sendingcompartment.correctionexponent)* self.sendingcompartment.density/self.sendingcompartment.xylemdensity)
	
	@property
	def compartmentrelationship(self):
		return ("in_same_composite")
	
	@property
	def transferfactor(self):
		try:
			r=self.receivingcompartment.allowexchange_forother * (self.sendingcompartment.flowrateoftranspiredwater/self.partitioncoefficientbetweenstemandxylemwater)/self.sendingcompartment.volume
		except:
			r=nan
		return (r)

class transfer_from_stem_to_leaf_grasses_herbs_organic_alginstid_1260:
	def __init__(self, constants,containingscenario,currentchemical,sendingcompartment, receivingcompartment,dict_inputs):
		self.name='transfer from stem to leaf - grasses/herbs, organic(alginstid_1260)'
		self.constants=constants
		self.containingscenario=containingscenario
		self.currentchemical=currentchemical
		self.sendingcompartment=sendingcompartment
		self.receivingcompartment=receivingcompartment
		self.category='advection'
		self.chemicalcategory='organic'
		self.doestransformchemical='False'
		self.transportchemical='True'
		self.enabled='True'
		self.isdefaultforcategory='True'
		self.mate='<unset>'
		self.receivingchemicalname='replaceme'
		self.receivingcompartmentcategory='terrestrial plant | leaf | leaf - grasses/herbs'
		self.sendingcompartmentcategory='terrestrial plant | stem | stem - grasses/herbs'
		self.sendingchemicalname='replaceme'
		self.dict_inputs=dict_inputs
		
	@property
	def partitioncoefficientbetweenstemandxylemwater(self):
		return ((self.sendingcompartment.watercontent  + self.sendingcompartment.lipidcontent*self.currentchemical.k_ow ** self.sendingcompartment.correctionexponent)* self.sendingcompartment.density/self.sendingcompartment.xylemdensity)
	
	@property
	def compartmentrelationship(self):
		return ("in_same_composite")
	
	@property
	def transferfactor(self):
		try:
			r=self.receivingcompartment.allowexchange_forother * (self.sendingcompartment.flowrateoftranspiredwater/self.partitioncoefficientbetweenstemandxylemwater)/self.sendingcompartment.volume
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

