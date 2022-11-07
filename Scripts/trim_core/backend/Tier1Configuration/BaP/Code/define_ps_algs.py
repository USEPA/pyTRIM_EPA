### note: this is an auto generated script
from numpy import nan

class diffusion_from_dryvaporsource_to_plant_leaf_hg0:
	def __init__(self, constants,containingscenario,currentchemical,sendingcompartment, receivingcompartment,dict_inputs):
		self.name='diffusion from dryvaporsource to plant leaf, hg0'
		self.constants=constants
		self.containingscenario=containingscenario
		self.currentchemical=currentchemical
		self.sendingcompartment=sendingcompartment
		self.receivingcompartment=receivingcompartment
		self.dict_inputs=dict_inputs
		
	@property
	def masstransfercoefficient(self):
		return ( self.receivingcompartment.associated_soil_comp.chemical_masstransfercoefficientonairsideofairsoilboundary )
	
	@property
	def doestransportchemical(self):
		return ("True")
	
	@property
	def receivingchemicalname(self):
		return ("elemental mercury")
	
	@property
	def isdefaultforcategory(self):
		return ("True")
	
	@property
	def enabled(self):
		return ("True")
	
	@property
	def receivingcompartmentcategory(self):
		return ("terrestrial plant | leaf")
	
	@property
	def sendingcompartmentcategory(self):
		return ("pseudosource | dry | vapor")
	
	@property
	def sendingchemicalname(self):
		return ("elemental mercury")
	
	@property
	def category(self):
		return ("abstract transfer")
	
	@property
	def doestransformchemical(self):
		return ("False")
	

	@property
	def transferfractionleaf(self):
		if 'coniferous' not in self.receivingcompartment.name:
			mdict={}
			mdict['ae_notday']=self.receivingcompartment.associated_soil_comp.area * 2*self.receivingcompartment.leafareaindex * self.receivingcompartment.chemical_totalcuticularconductance
			mdict['ae_day']=(self.receivingcompartment.associated_soil_comp.area * 2*self.receivingcompartment.leafareaindex * self.receivingcompartment.chemical_totalcuticularconductance) +(self.receivingcompartment.leafareaindex * self.receivingcompartment.associated_soil_comp.area * self.receivingcompartment.chemical_totalstomatalconductance) 
			mdict['no_ae']=0
			return (mdict)
		else:
			return ((self.receivingcompartment.allowexchange_forair *self.receivingcompartment.associated_soil_comp.area * 2*self.receivingcompartment.leafareaindex * self.receivingcompartment.chemical_totalcuticularconductance)+(self.receivingcompartment.leafareaindex * self.receivingcompartment.associated_soil_comp.area * self.dict_inputs["met_dict"]["frac_time_exchange_day"]* self.receivingcompartment.chemical_totalstomatalconductance))


	@property
	def transferfractionsoil(self):
		return (((self.receivingcompartment.associated_soil_comp.fractionofareaavailableforverticaldiffusion * self.receivingcompartment.associated_soil_comp.area)/self.currentchemical.z_pureair) * ((1/(self.currentchemical.z_pureair * self.masstransfercoefficient))+(1/(self.receivingcompartment.associated_soil_comp.chemical_z_total * (self.receivingcompartment.associated_soil_comp.chemical_d_effective / self.receivingcompartment.associated_soil_comp.depth))))**(-1))

	@property
	def transferfractiontotal(self):
		if 'coniferous' not in self.receivingcompartment.name:
			mdict={}
			mdict['ae_notday']=(self.transferfractionleaf['ae_notday'] + self.transferfractionsoil) 
			mdict['ae_day']=(self.transferfractionleaf['ae_day'] + self.transferfractionsoil )
			mdict['no_ae']=(self.transferfractionleaf['no_ae'] + self.transferfractionsoil)
			return (mdict)
		else:
			return ( self.transferfractionleaf + self.transferfractionsoil )

	@property
	def transferfactor(self):
#		if (not hasattr(self.receivingcompartment,'associated_soil_comp')):
#			return(0)
#		else:
			if 'coniferous' not in self.receivingcompartment.name:
				try:
					rleaf=self.dict_inputs["met_dict"]["frac_time_exchange_not_day"]*(self.transferfractionleaf['ae_notday']/self.transferfractiontotal['ae_notday'])+self.dict_inputs["met_dict"]["frac_time_exchange_day"]*(self.transferfractionleaf['ae_day']/self.transferfractiontotal['ae_day'])+(1-self.dict_inputs["met_dict"]["wt_av_allowexchange"])*(self.transferfractionleaf['no_ae']/self.transferfractiontotal['no_ae'])
					rsoil=self.dict_inputs["met_dict"]["frac_time_exchange_not_day"]*(self.transferfractionsoil/self.transferfractiontotal['ae_notday'])+self.dict_inputs["met_dict"]["frac_time_exchange_day"]*(self.transferfractionsoil/self.transferfractiontotal['ae_day'])+(1-self.dict_inputs["met_dict"]["wt_av_allowexchange"])*(self.transferfractionsoil/self.transferfractiontotal['no_ae'])
					r=rleaf/(rleaf+rsoil)
				except:
					r=nan    
				return(r)
			else:
				try:
					r=self.transferfractionleaf / self.transferfractiontotal if self.transferfractiontotal > 0 else 0
				except:
					r=nan
				return (r)
class diffusion_from_dryvaporsource_to_plant_leaf_mhg:
	def __init__(self, constants,containingscenario,currentchemical,sendingcompartment, receivingcompartment,dict_inputs):
		self.name='diffusion from dryvaporsource to plant leaf, mhg'
		self.constants=constants
		self.containingscenario=containingscenario
		self.currentchemical=currentchemical
		self.sendingcompartment=sendingcompartment
		self.receivingcompartment=receivingcompartment
		self.dict_inputs=dict_inputs
		
	@property
	def masstransfercoefficient(self):
		return ( self.receivingcompartment.associated_soil_comp.chemical_masstransfercoefficientonairsideofairsoilboundary )
	
	@property
	def doestransportchemical(self):
		return ("True")
	
	@property
	def receivingchemicalname(self):
		return ("methylmercury")
	
	@property
	def isdefaultforcategory(self):
		return ("True")
	
	@property
	def enabled(self):
		return ("True")
	
	@property
	def receivingcompartmentcategory(self):
		return ("terrestrial plant | leaf")
	
	@property
	def sendingcompartmentcategory(self):
		return ("pseudosource | dry | vapor")
	
	@property
	def sendingchemicalname(self):
		return ("methylmercury")
	
	@property
	def category(self):
		return ("abstract transfer")
	
	@property
	def doestransformchemical(self):
		return ("False")
	

	@property
	def transferfractionleaf(self):
		if 'coniferous' not in self.receivingcompartment.name:
			mdict={}
			mdict['ae_notday']=self.receivingcompartment.associated_soil_comp.area * 2*self.receivingcompartment.leafareaindex * self.receivingcompartment.chemical_totalcuticularconductance
			mdict['ae_day']=(self.receivingcompartment.associated_soil_comp.area * 2*self.receivingcompartment.leafareaindex * self.receivingcompartment.chemical_totalcuticularconductance) +(self.receivingcompartment.leafareaindex * self.receivingcompartment.associated_soil_comp.area * self.receivingcompartment.chemical_totalstomatalconductance) 
			mdict['no_ae']=0
			return (mdict)
		else:
			return ((self.receivingcompartment.allowexchange_forair *self.receivingcompartment.associated_soil_comp.area * 2*self.receivingcompartment.leafareaindex * self.receivingcompartment.chemical_totalcuticularconductance)+(self.receivingcompartment.leafareaindex * self.receivingcompartment.associated_soil_comp.area * self.dict_inputs["met_dict"]["frac_time_exchange_day"]* self.receivingcompartment.chemical_totalstomatalconductance))


	@property
	def transferfractionsoil(self):
		return (((self.receivingcompartment.associated_soil_comp.fractionofareaavailableforverticaldiffusion * self.receivingcompartment.associated_soil_comp.area)/self.currentchemical.z_pureair) * ((1/(self.currentchemical.z_pureair * self.masstransfercoefficient))+(1/(self.receivingcompartment.associated_soil_comp.chemical_z_total * (self.receivingcompartment.associated_soil_comp.chemical_d_effective / self.receivingcompartment.associated_soil_comp.depth))))**(-1))

	@property
	def transferfractiontotal(self):
		if 'coniferous' not in self.receivingcompartment.name:
			mdict={}
			mdict['ae_notday']=(self.transferfractionleaf['ae_notday'] + self.transferfractionsoil) 
			mdict['ae_day']=(self.transferfractionleaf['ae_day'] + self.transferfractionsoil )
			mdict['no_ae']=(self.transferfractionleaf['no_ae'] + self.transferfractionsoil)
			return (mdict)
		else:
			return ( self.transferfractionleaf + self.transferfractionsoil )

	@property
	def transferfactor(self):
#		if (not hasattr(self.receivingcompartment,'associated_soil_comp')):
#			return(0)
#		else:
			if 'coniferous' not in self.receivingcompartment.name:
				try:
					rleaf=self.dict_inputs["met_dict"]["frac_time_exchange_not_day"]*(self.transferfractionleaf['ae_notday']/self.transferfractiontotal['ae_notday'])+self.dict_inputs["met_dict"]["frac_time_exchange_day"]*(self.transferfractionleaf['ae_day']/self.transferfractiontotal['ae_day'])+(1-self.dict_inputs["met_dict"]["wt_av_allowexchange"])*(self.transferfractionleaf['no_ae']/self.transferfractiontotal['no_ae'])
					rsoil=self.dict_inputs["met_dict"]["frac_time_exchange_not_day"]*(self.transferfractionsoil/self.transferfractiontotal['ae_notday'])+self.dict_inputs["met_dict"]["frac_time_exchange_day"]*(self.transferfractionsoil/self.transferfractiontotal['ae_day'])+(1-self.dict_inputs["met_dict"]["wt_av_allowexchange"])*(self.transferfractionsoil/self.transferfractiontotal['no_ae'])
					r=rleaf/(rleaf+rsoil)
				except:
					r=nan    
				return(r)
			else:
				try:
					r=self.transferfractionleaf / self.transferfractiontotal if self.transferfractiontotal > 0 else 0
				except:
					r=nan
				return (r)
class diffusion_from_dryvaporsource_to_plant_leaf_organics:
	def __init__(self, constants,containingscenario,currentchemical,sendingcompartment, receivingcompartment,dict_inputs):
		self.name='diffusion from dryvaporsource to plant leaf, organics'
		self.constants=constants
		self.containingscenario=containingscenario
		self.currentchemical=currentchemical
		self.sendingcompartment=sendingcompartment
		self.receivingcompartment=receivingcompartment
		self.dict_inputs=dict_inputs
		
	@property
	def masstransfercoefficient(self):
		return ( self.receivingcompartment.associated_soil_comp.chemical_masstransfercoefficientonairsideofairsoilboundary )
	
	@property
	def doestransportchemical(self):
		return ("True")
	
	@property
	def isdefaultforcategory(self):
		return ("True")
	
	@property
	def enabled(self):
		return ("True")
	
	@property
	def receivingcompartmentcategory(self):
		return ("terrestrial plant | leaf")
	
	@property
	def sendingcompartmentcategory(self):
		return ("pseudosource | dry | vapor")
	
	@property
	def chemicalcategory(self):
		return ("organic")
	
	@property
	def category(self):
		return ("abstract transfer")
	
	@property
	def doestransformchemical(self):
		return ("False")
	

	@property
	def transferfractionleaf(self):
		if 'coniferous' not in self.receivingcompartment.name:
			mdict={}
			mdict['ae_notday']=self.receivingcompartment.associated_soil_comp.area * 2*self.receivingcompartment.leafareaindex * self.receivingcompartment.chemical_totalcuticularconductance
			mdict['ae_day']=(self.receivingcompartment.associated_soil_comp.area * 2*self.receivingcompartment.leafareaindex * self.receivingcompartment.chemical_totalcuticularconductance) +(self.receivingcompartment.leafareaindex * self.receivingcompartment.associated_soil_comp.area * self.receivingcompartment.chemical_totalstomatalconductance) 
			mdict['no_ae']=0
			return (mdict)
		else:
			return ((self.receivingcompartment.allowexchange_forair *self.receivingcompartment.associated_soil_comp.area * 2*self.receivingcompartment.leafareaindex * self.receivingcompartment.chemical_totalcuticularconductance)+(self.receivingcompartment.leafareaindex * self.receivingcompartment.associated_soil_comp.area * self.dict_inputs["met_dict"]["frac_time_exchange_day"]* self.receivingcompartment.chemical_totalstomatalconductance))


	@property
	def transferfractionsoil(self):
		return (((self.receivingcompartment.associated_soil_comp.fractionofareaavailableforverticaldiffusion * self.receivingcompartment.associated_soil_comp.area)/self.currentchemical.z_pureair) * ((1/(self.currentchemical.z_pureair * self.masstransfercoefficient))+(1/(self.receivingcompartment.associated_soil_comp.chemical_z_total * (self.receivingcompartment.associated_soil_comp.chemical_d_effective / self.receivingcompartment.associated_soil_comp.depth))))**(-1))

	@property
	def transferfractiontotal(self):
		if 'coniferous' not in self.receivingcompartment.name:
			mdict={}
			mdict['ae_notday']=(self.transferfractionleaf['ae_notday'] + self.transferfractionsoil) 
			mdict['ae_day']=(self.transferfractionleaf['ae_day'] + self.transferfractionsoil )
			mdict['no_ae']=(self.transferfractionleaf['no_ae'] + self.transferfractionsoil)
			return (mdict)
		else:
			return ( self.transferfractionleaf + self.transferfractionsoil )

	@property
	def transferfactor(self):
#		if (not hasattr(self.receivingcompartment,'associated_soil_comp')):
#			return(0)
#		else:
			if 'coniferous' not in self.receivingcompartment.name:
				try:
					rleaf=self.dict_inputs["met_dict"]["frac_time_exchange_not_day"]*(self.transferfractionleaf['ae_notday']/self.transferfractiontotal['ae_notday'])+self.dict_inputs["met_dict"]["frac_time_exchange_day"]*(self.transferfractionleaf['ae_day']/self.transferfractiontotal['ae_day'])+(1-self.dict_inputs["met_dict"]["wt_av_allowexchange"])*(self.transferfractionleaf['no_ae']/self.transferfractiontotal['no_ae'])
					rsoil=self.dict_inputs["met_dict"]["frac_time_exchange_not_day"]*(self.transferfractionsoil/self.transferfractiontotal['ae_notday'])+self.dict_inputs["met_dict"]["frac_time_exchange_day"]*(self.transferfractionsoil/self.transferfractiontotal['ae_day'])+(1-self.dict_inputs["met_dict"]["wt_av_allowexchange"])*(self.transferfractionsoil/self.transferfractiontotal['no_ae'])
					r=rleaf/(rleaf+rsoil)
				except:
					r=nan    
				return(r)
			else:
				try:
					r=self.transferfractionleaf / self.transferfractiontotal if self.transferfractiontotal > 0 else 0
				except:
					r=nan
				return (r)
class diffusion_from_dryvaporsource_to_surface_soil_hg0:
	def __init__(self, constants,containingscenario,currentchemical,sendingcompartment, receivingcompartment,dict_inputs):
		self.name='diffusion from dryvaporsource to surface soil, hg0'
		self.constants=constants
		self.containingscenario=containingscenario
		self.currentchemical=currentchemical
		self.sendingcompartment=sendingcompartment
		self.receivingcompartment=receivingcompartment
		self.dict_inputs=dict_inputs
		
	@property
	def masstransfercoefficient(self):
		return ( self.receivingcompartment.chemical_masstransfercoefficientonairsideofairsoilboundary )
	
	@property
	def doestransportchemical(self):
		return ("True")
	
	@property
	def receivingchemicalname(self):
		return ("elemental mercury")
	
	@property
	def isdefaultforcategory(self):
		return ("True")
	
	@property
	def enabled(self):
		return ("True")
	
	@property
	def receivingcompartmentcategory(self):
		return ("abiotic | soil | surface soil | surface soil - default")
	
	@property
	def sendingcompartmentcategory(self):
		return ("pseudosource | dry | vapor")
	
	@property
	def sendingchemicalname(self):
		return ("elemental mercury")
	
	@property
	def category(self):
		return ("abstract transfer")
	
	@property
	def doestransformchemical(self):
		return ("False")
	                     

	@property
	def transferfractionleaf(self):
		if 'coniferous' not in self.receivingcompartment.associated_leaf_comp.name:
			mdict={}
			mdict['ae_notday']=self.receivingcompartment.area * 2*self.receivingcompartment.associated_leaf_comp.leafareaindex * self.receivingcompartment.associated_leaf_comp.chemical_totalcuticularconductance
			mdict['ae_day']=(self.receivingcompartment.area * 2*self.receivingcompartment.associated_leaf_comp.leafareaindex * self.receivingcompartment.associated_leaf_comp.chemical_totalcuticularconductance) +(self.receivingcompartment.associated_leaf_comp.leafareaindex * self.receivingcompartment.area * self.receivingcompartment.associated_leaf_comp.chemical_totalstomatalconductance) 
			mdict['no_ae']=0
			return (mdict)
		else:
			return ((self.receivingcompartment.associated_leaf_comp.allowexchange_forair *self.receivingcompartment.area * 2*self.receivingcompartment.associated_leaf_comp.leafareaindex * self.receivingcompartment.associated_leaf_comp.chemical_totalcuticularconductance)+(self.receivingcompartment.associated_leaf_comp.leafareaindex * self.receivingcompartment.area * self.dict_inputs["met_dict"]["frac_time_exchange_day"]* self.receivingcompartment.associated_leaf_comp.chemical_totalstomatalconductance))


	@property
	def transferfractionsoil(self):
		return (((self.receivingcompartment.fractionofareaavailableforverticaldiffusion * self.receivingcompartment.area)/self.currentchemical.z_pureair) * ((1/(self.currentchemical.z_pureair * self.masstransfercoefficient))+(1/(self.receivingcompartment.chemical_z_total * (self.receivingcompartment.chemical_d_effective / self.receivingcompartment.depth))))**(-1))

	@property
	def transferfractiontotal(self):
		if 'coniferous' not in self.receivingcompartment.associated_leaf_comp.name:
			mdict={}
			mdict['ae_notday']=(self.transferfractionleaf['ae_notday'] + self.transferfractionsoil) 
			mdict['ae_day']=(self.transferfractionleaf['ae_day'] + self.transferfractionsoil )
			mdict['no_ae']=(self.transferfractionleaf['no_ae'] + self.transferfractionsoil)
			return (mdict)
		else:
			return ( self.transferfractionleaf + self.transferfractionsoil )

	@property
	def transferfactor(self):
		if (not hasattr(self.receivingcompartment,'associated_leaf_comp')):
			return(1)
		else:
			if 'coniferous' not in self.receivingcompartment.associated_leaf_comp.name:
				try:
					rleaf=self.dict_inputs["met_dict"]["frac_time_exchange_not_day"]*(self.transferfractionleaf['ae_notday']/self.transferfractiontotal['ae_notday'])+self.dict_inputs["met_dict"]["frac_time_exchange_day"]*(self.transferfractionleaf['ae_day']/self.transferfractiontotal['ae_day'])+(1-self.dict_inputs["met_dict"]["wt_av_allowexchange"])*(self.transferfractionleaf['no_ae']/self.transferfractiontotal['no_ae'])
					rsoil=self.dict_inputs["met_dict"]["frac_time_exchange_not_day"]*(self.transferfractionsoil/self.transferfractiontotal['ae_notday'])+self.dict_inputs["met_dict"]["frac_time_exchange_day"]*(self.transferfractionsoil/self.transferfractiontotal['ae_day'])+(1-self.dict_inputs["met_dict"]["wt_av_allowexchange"])*(self.transferfractionsoil/self.transferfractiontotal['no_ae'])
					r=rsoil/(rleaf+rsoil)
				except:
					r=nan    
				return(r)
			else:
				try:
					r=self.transferfractionsoil / self.transferfractiontotal if self.transferfractiontotal > 0 else 0
				except:
					r=nan
				return (r)

class diffusion_from_dryvaporsource_to_surface_soil_mhg:
	def __init__(self, constants,containingscenario,currentchemical,sendingcompartment, receivingcompartment,dict_inputs):
		self.name='diffusion from dryvaporsource to surface soil, mhg'
		self.constants=constants
		self.containingscenario=containingscenario
		self.currentchemical=currentchemical
		self.sendingcompartment=sendingcompartment
		self.receivingcompartment=receivingcompartment
		self.dict_inputs=dict_inputs
		
	@property
	def masstransfercoefficient(self):
		return ( self.receivingcompartment.chemical_masstransfercoefficientonairsideofairsoilboundary )
	
	@property
	def doestransportchemical(self):
		return ("True")
	
	@property
	def receivingchemicalname(self):
		return ("methylmercury")
	
	@property
	def isdefaultforcategory(self):
		return ("True")
	
	@property
	def enabled(self):
		return ("True")
	
	@property
	def receivingcompartmentcategory(self):
		return ("abiotic | soil | surface soil | surface soil - default")
	
	@property
	def sendingcompartmentcategory(self):
		return ("pseudosource | dry | vapor")
	
	@property
	def sendingchemicalname(self):
		return ("methylmercury")
	
	@property
	def category(self):
		return ("abstract transfer")
	
	@property
	def doestransformchemical(self):
		return ("False")
	                     

	@property
	def transferfractionleaf(self):
		if 'coniferous' not in self.receivingcompartment.associated_leaf_comp.name:
			mdict={}
			mdict['ae_notday']=self.receivingcompartment.area * 2*self.receivingcompartment.associated_leaf_comp.leafareaindex * self.receivingcompartment.associated_leaf_comp.chemical_totalcuticularconductance
			mdict['ae_day']=(self.receivingcompartment.area * 2*self.receivingcompartment.associated_leaf_comp.leafareaindex * self.receivingcompartment.associated_leaf_comp.chemical_totalcuticularconductance) +(self.receivingcompartment.associated_leaf_comp.leafareaindex * self.receivingcompartment.area * self.receivingcompartment.associated_leaf_comp.chemical_totalstomatalconductance) 
			mdict['no_ae']=0
			return (mdict)
		else:
			return ((self.receivingcompartment.associated_leaf_comp.allowexchange_forair *self.receivingcompartment.area * 2*self.receivingcompartment.associated_leaf_comp.leafareaindex * self.receivingcompartment.associated_leaf_comp.chemical_totalcuticularconductance)+(self.receivingcompartment.associated_leaf_comp.leafareaindex * self.receivingcompartment.area * self.dict_inputs["met_dict"]["frac_time_exchange_day"]* self.receivingcompartment.associated_leaf_comp.chemical_totalstomatalconductance))


	@property
	def transferfractionsoil(self):
		return (((self.receivingcompartment.fractionofareaavailableforverticaldiffusion * self.receivingcompartment.area)/self.currentchemical.z_pureair) * ((1/(self.currentchemical.z_pureair * self.masstransfercoefficient))+(1/(self.receivingcompartment.chemical_z_total * (self.receivingcompartment.chemical_d_effective / self.receivingcompartment.depth))))**(-1))

	@property
	def transferfractiontotal(self):
		if 'coniferous' not in self.receivingcompartment.associated_leaf_comp.name:
			mdict={}
			mdict['ae_notday']=(self.transferfractionleaf['ae_notday'] + self.transferfractionsoil) 
			mdict['ae_day']=(self.transferfractionleaf['ae_day'] + self.transferfractionsoil )
			mdict['no_ae']=(self.transferfractionleaf['no_ae'] + self.transferfractionsoil)
			return (mdict)
		else:
			return ( self.transferfractionleaf + self.transferfractionsoil )

	@property
	def transferfactor(self):
		if (not hasattr(self.receivingcompartment,'associated_leaf_comp')):
			return(1)
		else:
			if 'coniferous' not in self.receivingcompartment.associated_leaf_comp.name:
				try:
					rleaf=self.dict_inputs["met_dict"]["frac_time_exchange_not_day"]*(self.transferfractionleaf['ae_notday']/self.transferfractiontotal['ae_notday'])+self.dict_inputs["met_dict"]["frac_time_exchange_day"]*(self.transferfractionleaf['ae_day']/self.transferfractiontotal['ae_day'])+(1-self.dict_inputs["met_dict"]["wt_av_allowexchange"])*(self.transferfractionleaf['no_ae']/self.transferfractiontotal['no_ae'])
					rsoil=self.dict_inputs["met_dict"]["frac_time_exchange_not_day"]*(self.transferfractionsoil/self.transferfractiontotal['ae_notday'])+self.dict_inputs["met_dict"]["frac_time_exchange_day"]*(self.transferfractionsoil/self.transferfractiontotal['ae_day'])+(1-self.dict_inputs["met_dict"]["wt_av_allowexchange"])*(self.transferfractionsoil/self.transferfractiontotal['no_ae'])
					r=rsoil/(rleaf+rsoil)
				except:
					r=nan    
				return(r)
			else:
				try:
					r=self.transferfractionsoil / self.transferfractiontotal if self.transferfractiontotal > 0 else 0
				except:
					r=nan
				return (r)

class diffusion_from_dryvaporsource_to_surface_soil_organics:
	def __init__(self, constants,containingscenario,currentchemical,sendingcompartment, receivingcompartment,dict_inputs):
		self.name='diffusion from dryvaporsource to surface soil, organics'
		self.constants=constants
		self.containingscenario=containingscenario
		self.currentchemical=currentchemical
		self.sendingcompartment=sendingcompartment
		self.receivingcompartment=receivingcompartment
		self.dict_inputs=dict_inputs
		
	@property
	def masstransfercoefficient(self):
		return ( self.receivingcompartment.chemical_masstransfercoefficientonairsideofairsoilboundary )
	
	@property
	def doestransportchemical(self):
		return ("True")
	
	@property
	def isdefaultforcategory(self):
		return ("True")
	
	@property
	def enabled(self):
		return ("True")
	
	@property
	def receivingcompartmentcategory(self):
		return ("abiotic | soil | surface soil | surface soil - default")
	
	@property
	def sendingcompartmentcategory(self):
		return ("pseudosource | dry | vapor")
	
	@property
	def chemicalcategory(self):
		return ("organic")
	
	@property
	def category(self):
		return ("abstract transfer")
	
	@property
	def doestransformchemical(self):
		return ("False")
	                     

	@property
	def transferfractionleaf(self):
		if 'coniferous' not in self.receivingcompartment.associated_leaf_comp.name:
			mdict={}
			mdict['ae_notday']=self.receivingcompartment.area * 2*self.receivingcompartment.associated_leaf_comp.leafareaindex * self.receivingcompartment.associated_leaf_comp.chemical_totalcuticularconductance
			mdict['ae_day']=(self.receivingcompartment.area * 2*self.receivingcompartment.associated_leaf_comp.leafareaindex * self.receivingcompartment.associated_leaf_comp.chemical_totalcuticularconductance) +(self.receivingcompartment.associated_leaf_comp.leafareaindex * self.receivingcompartment.area * self.receivingcompartment.associated_leaf_comp.chemical_totalstomatalconductance) 
			mdict['no_ae']=0
			return (mdict)
		else:
			return ((self.receivingcompartment.associated_leaf_comp.allowexchange_forair *self.receivingcompartment.area * 2*self.receivingcompartment.associated_leaf_comp.leafareaindex * self.receivingcompartment.associated_leaf_comp.chemical_totalcuticularconductance)+(self.receivingcompartment.associated_leaf_comp.leafareaindex * self.receivingcompartment.area * self.dict_inputs["met_dict"]["frac_time_exchange_day"]* self.receivingcompartment.associated_leaf_comp.chemical_totalstomatalconductance))


	@property
	def transferfractionsoil(self):
		return (((self.receivingcompartment.fractionofareaavailableforverticaldiffusion * self.receivingcompartment.area)/self.currentchemical.z_pureair) * ((1/(self.currentchemical.z_pureair * self.masstransfercoefficient))+(1/(self.receivingcompartment.chemical_z_total * (self.receivingcompartment.chemical_d_effective / self.receivingcompartment.depth))))**(-1))

	@property
	def transferfractiontotal(self):
		if 'coniferous' not in self.receivingcompartment.associated_leaf_comp.name:
			mdict={}
			mdict['ae_notday']=(self.transferfractionleaf['ae_notday'] + self.transferfractionsoil) 
			mdict['ae_day']=(self.transferfractionleaf['ae_day'] + self.transferfractionsoil )
			mdict['no_ae']=(self.transferfractionleaf['no_ae'] + self.transferfractionsoil)
			return (mdict)
		else:
			return ( self.transferfractionleaf + self.transferfractionsoil )

	@property
	def transferfactor(self):
		if (not hasattr(self.receivingcompartment,'associated_leaf_comp')):
			return(1)
		else:
			if 'coniferous' not in self.receivingcompartment.associated_leaf_comp.name:
				try:
					rleaf=self.dict_inputs["met_dict"]["frac_time_exchange_not_day"]*(self.transferfractionleaf['ae_notday']/self.transferfractiontotal['ae_notday'])+self.dict_inputs["met_dict"]["frac_time_exchange_day"]*(self.transferfractionleaf['ae_day']/self.transferfractiontotal['ae_day'])+(1-self.dict_inputs["met_dict"]["wt_av_allowexchange"])*(self.transferfractionleaf['no_ae']/self.transferfractiontotal['no_ae'])
					rsoil=self.dict_inputs["met_dict"]["frac_time_exchange_not_day"]*(self.transferfractionsoil/self.transferfractiontotal['ae_notday'])+self.dict_inputs["met_dict"]["frac_time_exchange_day"]*(self.transferfractionsoil/self.transferfractiontotal['ae_day'])+(1-self.dict_inputs["met_dict"]["wt_av_allowexchange"])*(self.transferfractionsoil/self.transferfractiontotal['no_ae'])
					r=rsoil/(rleaf+rsoil)
				except:
					r=nan    
				return(r)
			else:
				try:
					r=self.transferfractionsoil / self.transferfractiontotal if self.transferfractiontotal > 0 else 0
				except:
					r=nan
				return (r)

class direct_transfer_from_pseudosource_to_surface_water:
	def __init__(self, constants,containingscenario,currentchemical,sendingcompartment, receivingcompartment,dict_inputs):
		self.name='direct transfer from pseudosource to surface water'
		self.constants=constants
		self.containingscenario=containingscenario
		self.currentchemical=currentchemical
		self.sendingcompartment=sendingcompartment
		self.receivingcompartment=receivingcompartment
		self.dict_inputs=dict_inputs
		
	@property
	def doestransportchemical(self):
		return ("True")
	
	@property
	def isdefaultforcategory(self):
		return ("True")
	
	@property
	def enabled(self):
		return ("True")
	
	@property
	def receivingcompartmentcategory(self):
		return ("abiotic | surface water | surface water - default")
	
	@property
	def sendingcompartmentcategory(self):
		return ("pseudosource")
	
	@property
	def chemicalcategory(self):
		return ("all")
	
	@property
	def category(self):
		return ("abstract transfer")
	
	@property
	def doestransformchemical(self):
		return ("False")
	
	@property
	def transferfactor(self):
		try:
			r=1.0
		except:
			r=nan
		return (r)



class dry_deposition_of_particles_from_dryparticlesource_to_plants:
	def __init__(self, constants,containingscenario,currentchemical,sendingcompartment, receivingcompartment,dict_inputs):
		self.name='dry deposition of particles from dryparticlesource to plants'
		self.constants=constants
		self.containingscenario=containingscenario
		self.currentchemical=currentchemical
		self.sendingcompartment=sendingcompartment
		self.receivingcompartment=receivingcompartment
		self.dict_inputs=dict_inputs
		
	@property
	def doestransportchemical(self):
		return ("True")
	
	@property
	def isdefaultforcategory(self):
		return ("True")
	
	@property
	def enabled(self):
		return ("True")
	
	@property
	def receivingcompartmentcategory(self):
		return ("terrestrial plant | leaf particle")
	
	@property
	def sendingcompartmentcategory(self):
		return ("pseudosource | dry | particle")
	
	@property
	def chemicalcategory(self):
		return ("all")
	
	@property
	def category(self):
		return ("abstract transfer")
	
	@property
	def doestransformchemical(self):
		return ("False")
	
	@property
	def transferfactor(self):
		try:
			r=self.receivingcompartment.associated_leaf_comp.allowexchange_forair*self.receivingcompartment.associated_leaf_comp.drydepinterceptionfraction
		except:
			r=nan
		return (r)



class dry_deposition_of_particles_from_dryparticlesource_to_soil:
	def __init__(self, constants,containingscenario,currentchemical,sendingcompartment, receivingcompartment,dict_inputs):
		self.name='dry deposition of particles from dryparticlesource to soil'
		self.constants=constants
		self.containingscenario=containingscenario
		self.currentchemical=currentchemical
		self.sendingcompartment=sendingcompartment
		self.receivingcompartment=receivingcompartment
		self.dict_inputs=dict_inputs
		
	@property
	def doestransportchemical(self):
		return ("True")
	
	@property
	def isdefaultforcategory(self):
		return ("True")
	
	@property
	def enabled(self):
		return ("True")
	
	@property
	def receivingcompartmentcategory(self):
		return ("abiotic | soil | surface soil | surface soil - default")
	
	@property
	def sendingcompartmentcategory(self):
		return ("pseudosource | dry | particle")
	
	@property
	def chemicalcategory(self):
		return ("all")
	
	@property
	def category(self):
		return ("abstract transfer")
	
	@property
	def doestransformchemical(self):
		return ("False")
	
	@property
	def transferfactor(self):
		try:
			r= 1 - (self.receivingcompartment.associated_leaf_comp.allowexchange_forair*self.receivingcompartment.associated_leaf_comp.drydepinterceptionfraction) 
		except:
			r=nan
		return (r)



class dry_deposition_of_vapor_from_dryvaporsource_to_plants_hg2:
	def __init__(self, constants,containingscenario,currentchemical,sendingcompartment, receivingcompartment,dict_inputs):
		self.name='dry deposition of vapor from dryvaporsource to plants,  hg2'
		self.constants=constants
		self.containingscenario=containingscenario
		self.currentchemical=currentchemical
		self.sendingcompartment=sendingcompartment
		self.receivingcompartment=receivingcompartment
		self.dict_inputs=dict_inputs
		
	@property
	def receivingchemicalname(self):
		return ("divalent mercury")
	
	@property
	def doestransportchemical(self):
		return ("True")
	
	@property
	def isdefaultforcategory(self):
		return ("True")
	
	@property
	def enabled(self):
		return ("True")
	
	@property
	def receivingcompartmentcategory(self):
		return ("terrestrial plant | leaf")
	
	@property
	def sendingcompartmentcategory(self):
		return ("pseudosource | dry | vapor")
	
	@property
	def sendingchemicalname(self):
		return ("divalent mercury")
	
	@property
	def category(self):
		return ("abstract transfer")
	
	@property
	def doestransformchemical(self):
		return ("False")
	
	@property
	def transferfactor(self):
		try:
			r=self.receivingcompartment.allowexchange_forair*self.receivingcompartment.drydepinterceptionfraction
		except:
			r=nan
		return (r)



class dry_deposition_of_vapor_from_dryvaporsource_to_soil_hg2:
	def __init__(self, constants,containingscenario,currentchemical,sendingcompartment, receivingcompartment,dict_inputs):
		self.name='dry deposition of vapor from dryvaporsource to soil, hg2'
		self.constants=constants
		self.containingscenario=containingscenario
		self.currentchemical=currentchemical
		self.sendingcompartment=sendingcompartment
		self.receivingcompartment=receivingcompartment
		self.dict_inputs=dict_inputs
		
	@property
	def receivingchemicalname(self):
		return ("divalent mercury")
	
	@property
	def doestransportchemical(self):
		return ("True")
	
	@property
	def isdefaultforcategory(self):
		return ("True")
	
	@property
	def enabled(self):
		return ("True")
	
	@property
	def receivingcompartmentcategory(self):
		return ("abiotic | soil | surface soil | surface soil - default")
	
	@property
	def sendingcompartmentcategory(self):
		return ("pseudosource | dry | vapor")
	
	@property
	def sendingchemicalname(self):
		return ("divalent mercury")
	
	@property
	def category(self):
		return ("abstract transfer")
	
	@property
	def doestransformchemical(self):
		return ("False")
	
	@property
	def transferfactor(self):
		try:
			r=1 - (self.receivingcompartment.associated_leaf_comp.allowexchange_forair*self.receivingcompartment.associated_leaf_comp.drydepinterceptionfraction)
		except:
			r=nan
		return (r)



class wet_deposition_of_particles_from_wetparticlesource_to_plants:
	def __init__(self, constants,containingscenario,currentchemical,sendingcompartment, receivingcompartment,dict_inputs):
		self.name='wet deposition of particles from wetparticlesource to plants'
		self.constants=constants
		self.containingscenario=containingscenario
		self.currentchemical=currentchemical
		self.sendingcompartment=sendingcompartment
		self.receivingcompartment=receivingcompartment
		self.dict_inputs=dict_inputs
		
	@property
	def doestransportchemical(self):
		return ("True")
	
	@property
	def isdefaultforcategory(self):
		return ("True")
	
	@property
	def enabled(self):
		return ("True")
	
	@property
	def receivingcompartmentcategory(self):
		return ("terrestrial plant | leaf particle")
	
	@property
	def sendingcompartmentcategory(self):
		return ("pseudosource | wet | particle")
	
	@property
	def chemicalcategory(self):
		return ("all")
	
	@property
	def category(self):
		return ("abstract transfer")
	
	@property
	def doestransformchemical(self):
		return ("False")
	
	@property
	def transferfactor(self):
		try:
			r= self.receivingcompartment.associated_leaf_comp.allowexchange_forair*self.receivingcompartment.associated_leaf_comp.wetdepinterceptionfraction
		except:
			r=nan
		return (r)



class wet_deposition_of_particles_from_wetparticlesource_to_surface_soil:
	def __init__(self, constants,containingscenario,currentchemical,sendingcompartment, receivingcompartment,dict_inputs):
		self.name='wet deposition of particles from wetparticlesource to surface soil'
		self.constants=constants
		self.containingscenario=containingscenario
		self.currentchemical=currentchemical
		self.sendingcompartment=sendingcompartment
		self.receivingcompartment=receivingcompartment
		self.dict_inputs=dict_inputs
		
	@property
	def doestransportchemical(self):
		return ("True")
	
	@property
	def isdefaultforcategory(self):
		return ("True")
	
	@property
	def enabled(self):
		return ("True")
	
	@property
	def receivingcompartmentcategory(self):
		return ("abiotic | soil | surface soil | surface soil - default")
	
	@property
	def sendingcompartmentcategory(self):
		return ("pseudosource | wet | particle")
	
	@property
	def chemicalcategory(self):
		return ("all")
	
	@property
	def category(self):
		return ("abstract transfer")
	
	@property
	def doestransformchemical(self):
		return ("False")
	
	@property
	def transferfactor(self):
		try:
			r= 1 - (self.receivingcompartment.associated_leaf_comp.allowexchange_forair*self.receivingcompartment.associated_leaf_comp.wetdepinterceptionfraction) 
		except:
			r=nan
		return (r)



class wet_deposition_of_vapor_phase_from_wetvaporsource_to_plants_hg0:
	def __init__(self, constants,containingscenario,currentchemical,sendingcompartment, receivingcompartment,dict_inputs):
		self.name='wet deposition of vapor phase from wetvaporsource to plants,  hg0'
		self.constants=constants
		self.containingscenario=containingscenario
		self.currentchemical=currentchemical
		self.sendingcompartment=sendingcompartment
		self.receivingcompartment=receivingcompartment
		self.dict_inputs=dict_inputs
		
	@property
	def receivingchemicalname(self):
		return ("elemental mercury")
	
	@property
	def doestransportchemical(self):
		return ("True")
	
	@property
	def isdefaultforcategory(self):
		return ("True")
	
	@property
	def enabled(self):
		return ("True")
	
	@property
	def receivingcompartmentcategory(self):
		return ("terrestrial plant | leaf")
	
	@property
	def sendingcompartmentcategory(self):
		return ("pseudosource | wet | vapor")
	
	@property
	def sendingchemicalname(self):
		return ("elemental mercury")
	
	@property
	def category(self):
		return ("abstract transfer")
	
	@property
	def doestransformchemical(self):
		return ("False")
	
	@property
	def transferfactor(self):
		try:
			r=self.receivingcompartment.allowexchange_forair*self.receivingcompartment.wetdepinterceptionfraction
		except:
			r=nan
		return (r)



class wet_deposition_of_vapor_phase_from_wetvaporsource_to_plants_hg2:
	def __init__(self, constants,containingscenario,currentchemical,sendingcompartment, receivingcompartment,dict_inputs):
		self.name='wet deposition of vapor phase from wetvaporsource to plants,  hg2'
		self.constants=constants
		self.containingscenario=containingscenario
		self.currentchemical=currentchemical
		self.sendingcompartment=sendingcompartment
		self.receivingcompartment=receivingcompartment
		self.dict_inputs=dict_inputs
		
	@property
	def receivingchemicalname(self):
		return ("divalent mercury")
	
	@property
	def doestransportchemical(self):
		return ("True")
	
	@property
	def isdefaultforcategory(self):
		return ("True")
	
	@property
	def enabled(self):
		return ("True")
	
	@property
	def receivingcompartmentcategory(self):
		return ("terrestrial plant | leaf")
	
	@property
	def sendingcompartmentcategory(self):
		return ("pseudosource | wet | vapor")
	
	@property
	def sendingchemicalname(self):
		return ("divalent mercury")
	
	@property
	def category(self):
		return ("abstract transfer")
	
	@property
	def doestransformchemical(self):
		return ("False")
	
	@property
	def transferfactor(self):
		try:
			r=self.receivingcompartment.allowexchange_forair*self.receivingcompartment.wetdepinterceptionfraction
		except:
			r=nan
		return (r)



class wet_deposition_of_vapor_phase_from_wetvaporsource_to_plants_organics:
	def __init__(self, constants,containingscenario,currentchemical,sendingcompartment, receivingcompartment,dict_inputs):
		self.name='wet deposition of vapor phase from wetvaporsource to plants,  organics'
		self.constants=constants
		self.containingscenario=containingscenario
		self.currentchemical=currentchemical
		self.sendingcompartment=sendingcompartment
		self.receivingcompartment=receivingcompartment
		self.dict_inputs=dict_inputs
		
	@property
	def doestransportchemical(self):
		return ("True")
	
	@property
	def isdefaultforcategory(self):
		return ("True")
	
	@property
	def enabled(self):
		return ("True")
	
	@property
	def receivingcompartmentcategory(self):
		return ("terrestrial plant | leaf")
	
	@property
	def sendingcompartmentcategory(self):
		return ("pseudosource | wet | vapor")
	
	@property
	def chemicalcategory(self):
		return ("organic")
	
	@property
	def category(self):
		return ("abstract transfer")
	
	@property
	def doestransformchemical(self):
		return ("False")
	
	@property
	def transferfactor(self):
		try:
			r=self.receivingcompartment.allowexchange_forair*self.receivingcompartment.wetdepinterceptionfraction
		except:
			r=nan
		return (r)



class wet_deposition_of_vapor_phase_from_wetvaporsource_to_soil_hg0:
	def __init__(self, constants,containingscenario,currentchemical,sendingcompartment, receivingcompartment,dict_inputs):
		self.name='wet deposition of vapor phase from wetvaporsource to soil, hg0'
		self.constants=constants
		self.containingscenario=containingscenario
		self.currentchemical=currentchemical
		self.sendingcompartment=sendingcompartment
		self.receivingcompartment=receivingcompartment
		self.dict_inputs=dict_inputs
		
	@property
	def receivingchemicalname(self):
		return ("elemental mercury")
	
	@property
	def doestransportchemical(self):
		return ("True")
	
	@property
	def isdefaultforcategory(self):
		return ("True")
	
	@property
	def enabled(self):
		return ("True")
	
	@property
	def receivingcompartmentcategory(self):
		return ("abiotic | soil | surface soil | surface soil - default")
	
	@property
	def sendingcompartmentcategory(self):
		return ("pseudosource | wet | vapor")
	
	@property
	def sendingchemicalname(self):
		return ("elemental mercury")
	
	@property
	def category(self):
		return ("abstract transfer")
	
	@property
	def doestransformchemical(self):
		return ("False")
	
	@property
	def transferfactor(self):
		try:
			r=1 - (self.receivingcompartment.associated_leaf_comp.allowexchange_forair*self.receivingcompartment.associated_leaf_comp.wetdepinterceptionfraction)
		except:
			r=nan
		return (r)



class wet_deposition_of_vapor_phase_from_wetvaporsource_to_soil_hg2:
	def __init__(self, constants,containingscenario,currentchemical,sendingcompartment, receivingcompartment,dict_inputs):
		self.name='wet deposition of vapor phase from wetvaporsource to soil, hg2'
		self.constants=constants
		self.containingscenario=containingscenario
		self.currentchemical=currentchemical
		self.sendingcompartment=sendingcompartment
		self.receivingcompartment=receivingcompartment
		self.dict_inputs=dict_inputs
		
	@property
	def receivingchemicalname(self):
		return ("divalent mercury")
	
	@property
	def doestransportchemical(self):
		return ("True")
	
	@property
	def isdefaultforcategory(self):
		return ("True")
	
	@property
	def enabled(self):
		return ("True")
	
	@property
	def receivingcompartmentcategory(self):
		return ("abiotic | soil | surface soil | surface soil - default")
	
	@property
	def sendingcompartmentcategory(self):
		return ("pseudosource | wet | vapor")
	
	@property
	def sendingchemicalname(self):
		return ("divalent mercury")
	
	@property
	def category(self):
		return ("abstract transfer")
	
	@property
	def doestransformchemical(self):
		return ("False")
	
	@property
	def transferfactor(self):
		try:
			r=1 - (self.receivingcompartment.associated_leaf_comp.allowexchange_forair*self.receivingcompartment.associated_leaf_comp.wetdepinterceptionfraction)
		except:
			r=nan
		return (r)



class wet_deposition_of_vapor_phase_from_wetvaporsource_to_soil_organics:
	def __init__(self, constants,containingscenario,currentchemical,sendingcompartment, receivingcompartment,dict_inputs):
		self.name='wet deposition of vapor phase from wetvaporsource to soil, organics'
		self.constants=constants
		self.containingscenario=containingscenario
		self.currentchemical=currentchemical
		self.sendingcompartment=sendingcompartment
		self.receivingcompartment=receivingcompartment
		self.dict_inputs=dict_inputs
		
	@property
	def doestransportchemical(self):
		return ("True")
	
	@property
	def isdefaultforcategory(self):
		return ("True")
	
	@property
	def enabled(self):
		return ("True")
	
	@property
	def receivingcompartmentcategory(self):
		return ("abiotic | soil | surface soil | surface soil - default")
	
	@property
	def sendingcompartmentcategory(self):
		return ("pseudosource | wet | vapor")
	
	@property
	def chemicalcategory(self):
		return ("organic")
	
	@property
	def category(self):
		return ("abstract transfer")
	
	@property
	def doestransformchemical(self):
		return ("False")
	
	@property
	def transferfactor(self):
		try:
			r=1 - (self.receivingcompartment.associated_leaf_comp.allowexchange_forair*self.receivingcompartment.associated_leaf_comp.wetdepinterceptionfraction)
		except:
			r=nan
		return (r)



