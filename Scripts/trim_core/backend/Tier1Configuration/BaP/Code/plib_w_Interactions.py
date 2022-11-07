# -*- coding: utf-8 -*-
"""
created on mon apr 12 21:46:07 2021
@author: 13963

parses pseudo source library objects text file and auto writes code to define pseudo source algorithm classes, specifically define_ps_algs.py

"""

import pandas as pd
import os
import re
import required_elements_temp as req
from util_functions import * 

def process_next_line(next_line):
    next_line_nc=next_line.strip()     # strip space and new line    
    next_line_nc=next_line_nc.split("//")[0] # line stripped of comment
    return(next_line_nc)

def process_pseudo_library(inputs):

    def clean_names(name): # function to replace certain special characters with underscore; leaves float values alone
        try:
            name=float(name) 
        except:
            pass
        if type(name)==str:
            cname = re.sub('[^0-9a-za-z]+', '_', name)
            cname=cname.strip('_')
            return(cname)            
        return(name)  

    ifp=inputs['path_inputs']
    ifn=inputs['pseudo_library_file']    
    ifpn=os.path.join(ifp,ifn)
    
    plib_file=open(ifpn,'r') 
    plib_lines=plib_file.readlines()
    
    
    #### read algorithhms
    
    alg_tuples=[] # initialize list for storing point lines
    alg_flag=False # initialize copy condition
    prop_flag=False # initialize copy condition
    val_flag=False # initialize copy condition
    
    
    for numlin,line in enumerate(plib_lines): # loop over lines
        line_nc=line.strip()     # strip space and new line    
        line_nc=line_nc.split("//")[0] # line stripped of comment
        ptype=line_nc.split(":")[0].strip() # if line has a :, get text to left
        # if ptype=="algorithm": # get algorithm name (assumed to be on single line)
        if ptype=="algorithm" and line[:9]=='algorithm': # get algorithm name (assumed to be on single line) -- new and condition makes sure that only true algorithms are flagged (some mentions are in indented comments) 
            alg_flag=True
            alg_name=line_nc.split(":")[1].strip()
#            print ('*******************************************')
#            print (alg_name)
            continue
        if alg_flag==True and ptype=="property": # get property name (assumed to be on single line) 
            prop_flag=True
            prop_name=line_nc.split(":")[1].strip()        
            # print (prop_name)
            continue
        if alg_flag==True and prop_flag==True and ptype=="value": # get value name (not assumed to be on single line)
            val_flag=True
            val_name=line_nc.split(":")[1:]
            val_name=[x.strip() for x in val_name]
            val_name=':'.join(val_name)   
            val_overflow_flag=True
            count=1
            while val_overflow_flag:                 
                next_line=plib_lines[numlin+count]
                next_line_nc=process_next_line(next_line)
                if not (':' in next_line_nc):
                    val_name=val_name+next_line_nc
                    count=count=count+1
                else:
                    val_overflow_flag=False
            r=(alg_name,prop_name,val_name)
            alg_tuples.append(r)
            prop_flag=False # reinitialize copy condition
            val_flag=False # reinitialize copy condition
            prop_name=""; val_name=""; 
            continue        

            # print (val_name) 
#        if alg_flag==True and prop_flag==True and val_flag==True and (':' not in line_nc): # get remainder of value ( not assumed to be on single line)
#            val_name=val_name+line_nc  # join multiline values
            # print (val_name) 
#            continue
#        if alg_flag==True and prop_flag==True and val_flag==True and (ptype=='property'or ptype=='description' or line[:10]=="algorithm:"): # condition to determine when value reading is over
#            r=(alg_name,prop_name,val_name)
##            print (r)
#            alg_tuples.append(r)
#            prop_flag=False # reinitialize copy condition
#            val_flag=False # reinitialize copy condition
#            prop_name=""; val_name=""; 
#            continue
        if alg_flag==True and (ptype=='pointsource'or ptype=='ptype'or ptype=='compartment'):
            alg_flag=False
    df_psalgs=pd.DataFrame(alg_tuples,columns=['algorithm','property','value']) # convert to DataFrame
    
    ofpn=os.path.join(ifp,"pseudoalgs.csv")
    df_psalgs.to_csv(ofpn,index=False)



   
        
    ########### create matrix of algorithm applicability i.e. which algorithms apply given a receiving compartment and a sending compartment

    required_algs=req.required_algorithms # look up list of required algorithms
    alg_mat=[]
    grouped_alg = df_psalgs.groupby("algorithm")            
    for index,group in enumerate(grouped_alg.groups):    
#        if group not in required_algs:
#            continue    
        
        alg_name=clean_names(group)    
        try:
            category=grouped_alg.get_group(group).loc[grouped_alg.get_group(group)['property']=='category']['value'].values[0]
        except:
            category=""
        try:
            chemical_category=grouped_alg.get_group(group).loc[grouped_alg.get_group(group)['property']=='chemicalcategory']['value'].values[0]
        except:
            chemical_category=""
        try:
            enabled=grouped_alg.get_group(group).loc[grouped_alg.get_group(group)['property']=='enabled']['value'].values[0]
        except:
            enabled=""
        try:
            isdefaultforcategory=grouped_alg.get_group(group).loc[grouped_alg.get_group(group)['property']=='isdefaultforcategory']['value'].values[0]
        except:
            isdefaultforcategory=""
        try:
            receivingchemicalname=grouped_alg.get_group(group).loc[grouped_alg.get_group(group)['property']=='receivingchemicalname']['value'].values[0]
        except:
            receivingchemicalname=""
        try:
            receivingcompartmentcategory=grouped_alg.get_group(group).loc[grouped_alg.get_group(group)['property']=='receivingcompartmentcategory']['value'].values[0]
        except:
            receivingcompartmentcategory=""
        try:
            sendingcompartmentcategory=grouped_alg.get_group(group).loc[grouped_alg.get_group(group)['property']=='sendingcompartmentcategory']['value'].values[0]
        except:
            sendingcompartmentcategory=""
        try:
            sendingchemicalname=grouped_alg.get_group(group).loc[grouped_alg.get_group(group)['property']=='sendingchemicalname']['value'].values[0]
        except:
            sendingchemicalname=""
        alg_mat.append((index,group,alg_name,category,chemical_category,enabled,isdefaultforcategory,receivingchemicalname,receivingcompartmentcategory,sendingcompartmentcategory,sendingchemicalname))
    
    cols=['index','group','alg_name_new','category','chemical_category','enabled','isdefaultforcategory','receivingchemicalname','receivingcompartmentcategory','sendingcompartmentcategory','sendingchemicalname']   
    df_psalg_mat=pd.DataFrame(alg_mat,columns=cols)
    df_psalg_mat=df_psalg_mat.loc[df_psalg_mat['category']=='abstract transfer'] # limit to pseudo source abstract transfer algorithms
    df_psalg_mat['index']=df_psalg_mat['index']+1 # avoid zero index to prevent later problems distinguishing pseudo from non-pseudo
   
    
    #### read point sources
    
    ps_tuples=[] # initialize list for storing point lines
    ps_flag=False # initialize copy condition
    prop_flag=False # initialize copy condition
    val_flag=False # initialize copy condition
    
    
    for line in plib_lines: # loop over lines
        line_nc=line.strip()     # strip space and new line    
        line_nc=line_nc.split("//")[0] # line stripped of comment
        ptype=line_nc.split(":")[0].strip() # if line has a :, get text to left
        if ptype=="pointsource": # get algorithm name (assumed to be on single line)
            ps_flag=True
            ps_name=line_nc.split(":")[1].strip()
#            print ('*******************************************')
#            print (ps_name)
            continue
        if ps_flag==True and ptype=="property": # get property name (assumed to be on single line) 
            prop_flag=True
            prop_name=line_nc.split(":")[1].strip()        
            # print (prop_name)
            continue
        if ps_flag==True and prop_flag==True and ptype=="value": # get value name (assumed to be on single line)
            val_flag=True
            val_name=line_nc.split(":")[1].strip()
            r=(ps_name,prop_name,val_name)
#            print (r)
            ps_tuples.append(r)        
            continue        
    df_ps=pd.DataFrame(ps_tuples,columns=['pointsource','property','value'])
    
    
    #### read ptypes -- not perfect -- order is different across 6 ptypes so script below doesnt grab all descriptions. may not be necessary because this is basically variable declaration.
    
    pt_tuples=[] # initialize list for storing point lines
    
    pt_flag=False # initialize copy condition
    desc_flag=False # initialize copy condition
    dt_flag=False
    units_flag=False # initialize copy condition
    pt_name='';desc_name='';dt_name='';unit_name=''; dv_name="";
    
    for line in plib_lines: # loop over lines
        line_nc=line.strip()     # strip space and new line    
        line_nc=line_nc.split("//")[0] # line stripped of comment
        ptype=line_nc.split(":")[0].strip() # if line has a :, get text to left
        if ptype=="ptype" or ptype=="ptype": # get algorithm name (assumed to be on single line)
            pt_flag=True
            pt_name=line_nc.split(":")[1].strip()
#            print ('*******************************************')
#            print (pt_name)
            continue
        if pt_flag==True and ptype=="description": # get property name (assumed not to be on single line) 
            desc_flag=True
            desc_name=line_nc.split(":")[1].strip()        
            # print (prop_name)
            continue
        if pt_flag==True and desc_flag==True and (':' not in line_nc): # get remainder of value ( not assumed to be on single line)
            desc_name=desc_name+line_nc  # join multiline values
            continue
        if pt_flag==True and ptype=='datatype':
            desc_flag=False
            dt_name=line_nc.split(":")[1].strip()
            continue
        if pt_flag==True and ptype=='defaultvalue':
            dv_name=line_nc.split(":")[1].strip()
            continue
        if pt_flag==True and ptype=='units':
            dt_flag=False
            unit_name=line_nc.split(":")[1].strip()
            r=(pt_name,desc_name,dt_name,dv_name,unit_name)
            pt_tuples.append(r)
            units_flag=False
            pt_flag=False
            pt_name='';desc_name='';dt_name='';unit_name=''; dv_name="";
            continue
            
    df_pt=pd.DataFrame(pt_tuples)
    
    
    
    ############ write python script to define pseudo algorithm classes 
    
    
    ofp=inputs['path_code']
    ofn=r'define_ps_algs.py'
    ofpn=os.path.join(ofp,ofn)
    
    algs=df_psalgs["algorithm"].tolist()
    
    
    
    def clean_names(name): # function to replace certain special characters with underscore; leaves float values alone
        try:
            name=float(name) 
        except:
            pass
        if type(name)==str:
            cname = re.sub('[^0-9a-za-z]+', '_', name)
            return(cname)
        return(name)  
    
    def clean_props(prop): # function to convert properties to pythonic syntax, 
        prop=prop.replace('[','')
        prop=prop.replace(']','')
    
        if '?' in prop: # change java if then else syntax to pythonic syntax
            cond=prop.split('?')[0].strip()
            v1=prop.split('?')[1].strip().split(':')[0].strip()
            v2=prop.split('?')[1].strip().split(':')[1].strip()
            prop= v1+' if ' +cond.replace('&&',' and ')+' else ' +v2
        prop=prop.replace('constants','self.constants')
        prop=prop.replace('containingscenario','self.containingscenario')
        prop=prop.replace('receivingcompartment','self.receivingcompartment')
        prop=prop.replace('sendingcompartment','self.sendingcompartment')
        prop=prop.replace('algorithm.','self.')
        prop=prop.replace('sendingchemical.','self.currentchemical.')
        prop=prop.replace('receivingvolumeelementsumofabiotic | soil | surface soil | surface soil - default.','self.receivingcompartment.associated_soil_comp.')
        prop=prop.replace('receivingvolumeelementsumofterrestrial plant | leaf.','self.receivingcompartment.associated_leaf_comp.')
        if 'thelink.interfacialarea' in prop: # replace thelink interfacial area custom function with python function
            prop=prop.replace('thelink.interfacialarea','check_neighbor(self.sendingcompartment,self.receivingcompartment).is_neighbor()[1]')           
        if 'thelink.fractionspecificcompartmentdiet' in prop: # replace thelink.fractionspecificcompartmentdiet with 1. i believe this okay but check ug.
            prop=prop.replace('thelink.fractionspecificcompartmentdiet','1')          
        if 'currentchemical' not in prop and 'chemical.' in prop:
            prop=prop.replace('chemical.','chemical_')
        prop=prop.replace('.chemical.','.chemical_') # to cover cases where both current chemical and chemical are in the same property

        if 'self.receivingcompartment.allowexchange_forair' in prop and 'self.receivingcompartment.isday_forair * self.receivingcompartment.chemical_totalstomatalconductance' in prop: # to address interaction between exchange and isday
            prop=prop.replace('self.receivingcompartment.allowexchange_forair *((','(self.receivingcompartment.allowexchange_forair *')
            prop=prop.replace('(self.receivingcompartment.isday_forair * self.receivingcompartment.chemical_totalstomatalconductance))','self.dict_inputs["met_dict"]["frac_time_exchange_day"]* self.receivingcompartment.chemical_totalstomatalconductance')
            
        if 'self.receivingcompartment.associated_leaf_comp.allowexchange_forair' in prop and 'self.receivingcompartment.associated_leaf_comp.isday_forair * self.receivingcompartment.associated_leaf_comp.chemical_totalstomatalconductance' in prop:
            prop=prop.replace('self.receivingcompartment.associated_leaf_comp.allowexchange_forair *((','(self.receivingcompartment.associated_leaf_comp.allowexchange_forair *')
            prop=prop.replace('(self.receivingcompartment.associated_leaf_comp.isday_forair * self.receivingcompartment.associated_leaf_comp.chemical_totalstomatalconductance))','self.dict_inputs["met_dict"]["frac_time_exchange_day"]* self.receivingcompartment.associated_leaf_comp.chemical_totalstomatalconductance')


        return (prop)
    
    
    grouped_alg = df_psalgs.groupby("algorithm")
    
    
    
    with open(ofpn, 'w') as f:  
        f.write('### note: this is an auto generated script' +'\n')                
        f.write('from numpy import nan' + '\n\n')
        for index,group in enumerate(grouped_alg.groups):
            # if "surface water" not in group: # temp
            #     continue

            if "source" not in group: # limit to pseudo source algorithms
                continue

    
            alg_name=clean_names(group)
            alg_props=list(grouped_alg.get_group(group)['property'].unique())
            try:
                tf=grouped_alg.get_group(group).loc[grouped_alg.get_group(group)['property']=='transferfactor']['value'].values[0]#.replace('sendingcompartment','self.sendingcompartment').replace('receivingcompartment','self.receivingcompartment')
            except:
                tf="nan"
            tf=clean_props(tf)
    
                
            f.write('class '+str(alg_name)+':'+'\n' +\
                    '\t'+\
                    'def __init__(self, constants,containingscenario,currentchemical,sendingcompartment, receivingcompartment,dict_inputs):\n\t\t'+\
                    'self.name='+"'"+group+"'"+'\n\t\t'+\
                    'self.constants=constants\n\t\t'+\
                    'self.containingscenario=containingscenario\n\t\t'+\
                    'self.currentchemical=currentchemical\n\t\t'+\
                    'self.sendingcompartment=sendingcompartment\n\t\t'+\
                    'self.receivingcompartment=receivingcompartment\n\t\t'+\
                    'self.dict_inputs=dict_inputs'+'\n\t\t')
                #     'self.category='+"'"+grouped_alg.get_group(group).loc[grouped_alg.get_group(group)['property']=='category']['value'].values[0]+"'"+'\n\t\t'
                #     'self.chemicalcategory='+"'"+grouped_alg.get_group(group).loc[grouped_alg.get_group(group)['property']=='chemicalcategory']['value'].values[0]+"'"+'\n\t\t'
                #     'self.doestransformchemical='+"'"+grouped_alg.get_group(group).loc[grouped_alg.get_group(group)['property']=='doestransformchemical']['value'].values[0]+"'"+'\n\t\t'
                #     'self.transportchemical='+"'"+grouped_alg.get_group(group).loc[grouped_alg.get_group(group)['property']=='doestransportchemical']['value'].values[0]+"'"+'\n\t\t'
                #     'self.enabled='+"'"+grouped_alg.get_group(group).loc[grouped_alg.get_group(group)['property']=='enabled']['value'].values[0]+"'"+'\n\t\t'
                #     'self.isdefaultforcategory='+"'"+grouped_alg.get_group(group).loc[grouped_alg.get_group(group)['property']=='isdefaultforcategory']['value'].values[0]+"'"+'\n\t\t'
                #     'self.receivingcompartmentcategory='+"'"+grouped_alg.get_group(group).loc[grouped_alg.get_group(group)['property']=='receivingcompartmentcategory']['value'].values[0]+"'"+'\n\t\t'
                #     'self.sendingcompartmentcategory='+"'"+grouped_alg.get_group(group).loc[grouped_alg.get_group(group)['property']=='sendingcompartmentcategory']['value'].values[0]+"'"+'\n\t\t')
            
            # residual_props=set(alg_props)-set(['category','chemicalcategory','doestransformchemical','doestransportchemical','enabled','isdefaultforcategory','mate','receivingcompartmentcategory','sendingcompartmentcategory','transferfactor'])

            diff_algs_leaf=['diffusion_from_dryvaporsource_to_plant_leaf_hg0',\
            'diffusion_from_dryvaporsource_to_plant_leaf_mhg',\
            'diffusion_from_dryvaporsource_to_plant_leaf_organics'\
            ]

            diff_algs_soil=['diffusion_from_dryvaporsource_to_surface_soil_hg0',\
            'diffusion_from_dryvaporsource_to_surface_soil_mhg',\
            'diffusion_from_dryvaporsource_to_surface_soil_organics'\
            ]

            if alg_name in diff_algs_leaf: # special case of leaf diffusion algorithms to accommodate met interaction terms
                special_props=['transferfactor','transferfractiontotal','transferfractionleaf','transferfractionsoil']
                residual_props=set(alg_props)-set(special_props)

                for prop in residual_props:
                    prop_val=grouped_alg.get_group(group).loc[grouped_alg.get_group(group)['property']==prop]['value'].values[0] #property value
                    prop_val=clean_props(prop_val)
                    if type(prop_val)==float or is_number(prop_val):
                        f.write('\n\t'+\
                                '_'+prop+'='+prop_val +'\n\t' +\
                                '@property'+'\n\t' +\
                                'def '+prop+'(self):'+'\n\t\t' +\
                                'return self._'+prop+'\n\n\t' +\
                                '@'+prop+'.setter''\n\t' +\
                                'def '+prop+'(self,value):'+'\n\t\t' +\
                                'self._'+prop+'=value\n')             
                    else:
                        if prop in ['category','receivingcompartmentcategory','sendingchemicalname','sendingcompartmentcategory','receivingchemicalname','compartmentrelationship','chemicalcategory','doestransformchemical','doestransportchemical','enabled','isdefaultforcategory','receivingchemicalname','receivingcompartmentcategory','sendingcompartmentcategory','sendingchemicalname','transferfactor']: # write as string
                            f.write('\n\t'+\
                                    '@property'+'\n\t' +\
                                    'def '+prop+'(self):'+'\n\t\t' +\
                                    'return ("'+prop_val+'")\n\t') 
                        else:
                            f.write('\n\t'+\
                                    '@property'+'\n\t' +\
                                    'def '+prop+'(self):'+'\n\t\t' +\
                                    'return ('+prop_val+')\n\t')                 

                f.write('''

	@property
	def transferfractionleaf(self):
		mdict={}
		mdict['ae_notday']=self.receivingcompartment.associated_soil_comp.area * 2*self.receivingcompartment.leafareaindex * self.receivingcompartment.chemical_totalcuticularconductance
		mdict['ae_day']=(self.receivingcompartment.associated_soil_comp.area * 2*self.receivingcompartment.leafareaindex * self.receivingcompartment.chemical_totalcuticularconductance) +(self.receivingcompartment.leafareaindex * self.receivingcompartment.associated_soil_comp.area * self.receivingcompartment.chemical_totalstomatalconductance) 
		mdict['no_ae']=0
		return (mdict)

	@property
	def transferfractionsoil(self):
		return (((self.receivingcompartment.associated_soil_comp.fractionofareaavailableforverticaldiffusion * self.receivingcompartment.associated_soil_comp.area)/self.currentchemical.z_pureair) * ((1/(self.currentchemical.z_pureair * self.masstransfercoefficient))+(1/(self.receivingcompartment.associated_soil_comp.chemical_z_total * (self.receivingcompartment.associated_soil_comp.chemical_d_effective / self.receivingcompartment.associated_soil_comp.depth))))**(-1))

	@property
	def transferfractiontotal(self):
		mdict={}
		mdict['ae_notday']=(self.transferfractionleaf['ae_notday'] + self.transferfractionsoil) 
		mdict['ae_day']=(self.transferfractionleaf['ae_day'] + self.transferfractionsoil )
		mdict['no_ae']=(self.transferfractionleaf['no_ae'] + self.transferfractionsoil)
		return (mdict)

	@property
	def transferfactor(self):
		try:
			rleaf=self.dict_inputs["met_dict"]["frac_time_exchange_not_day"]*(self.transferfractionleaf['ae_notday']/self.transferfractiontotal['ae_notday'])+self.dict_inputs["met_dict"]["frac_time_exchange_day"]*(self.transferfractionleaf['ae_day']/self.transferfractiontotal['ae_day'])+(1-self.dict_inputs["met_dict"]["wt_av_allowexchange"])*(self.transferfractionleaf['no_ae']/self.transferfractiontotal['no_ae'])
			rsoil=self.dict_inputs["met_dict"]["frac_time_exchange_not_day"]*(self.transferfractionsoil/self.transferfractiontotal['ae_notday'])+self.dict_inputs["met_dict"]["frac_time_exchange_day"]*(self.transferfractionsoil/self.transferfractiontotal['ae_day'])+(1-self.dict_inputs["met_dict"]["wt_av_allowexchange"])*(self.transferfractionsoil/self.transferfractiontotal['no_ae'])
			r=rleaf/(rleaf+rsoil)
		except:
			r=nan    
		return(r)

''')


            if alg_name in diff_algs_soil:# special case of soil diffusion algorithms to accommodate met interaction terms
                special_props=['transferfactor','transferfractiontotal','transferfractionleaf','transferfractionsoil']
                residual_props=set(alg_props)-set(special_props)

                for prop in residual_props:
                    prop_val=grouped_alg.get_group(group).loc[grouped_alg.get_group(group)['property']==prop]['value'].values[0] #property value
                    prop_val=clean_props(prop_val)
                    if type(prop_val)==float or is_number(prop_val):
                        f.write('\n\t'+\
                                '_'+prop+'='+prop_val +'\n\t' +\
                                '@property'+'\n\t' +\
                                'def '+prop+'(self):'+'\n\t\t' +\
                                'return self._'+prop+'\n\n\t' +\
                                '@'+prop+'.setter''\n\t' +\
                                'def '+prop+'(self,value):'+'\n\t\t' +\
                                'self._'+prop+'=value\n')             
                    else:
                        if prop in ['category','receivingcompartmentcategory','sendingchemicalname','sendingcompartmentcategory','receivingchemicalname','compartmentrelationship','chemicalcategory','doestransformchemical','doestransportchemical','enabled','isdefaultforcategory','receivingchemicalname','receivingcompartmentcategory','sendingcompartmentcategory','sendingchemicalname','transferfactor']: # write as string
                            f.write('\n\t'+\
                                    '@property'+'\n\t' +\
                                    'def '+prop+'(self):'+'\n\t\t' +\
                                    'return ("'+prop_val+'")\n\t') 
                        else:
                            f.write('\n\t'+\
                                    '@property'+'\n\t' +\
                                    'def '+prop+'(self):'+'\n\t\t' +\
                                    'return ('+prop_val+')\n\t')                 
                f.write('''                     

 
	@property
	def transferfractionleaf(self):
		mdict={}
		mdict['ae_notday']=self.receivingcompartment.area * 2*self.receivingcompartment.associated_leaf_comp.leafareaindex * self.receivingcompartment.associated_leaf_comp.chemical_totalcuticularconductance
		mdict['ae_day']=(self.receivingcompartment.area * 2*self.receivingcompartment.associated_leaf_comp.leafareaindex * self.receivingcompartment.associated_leaf_comp.chemical_totalcuticularconductance) +(self.receivingcompartment.associated_leaf_comp.leafareaindex * self.receivingcompartment.area * self.receivingcompartment.associated_leaf_comp.chemical_totalstomatalconductance) 
		mdict['no_ae']=0
		return (mdict)

	@property
	def transferfractionsoil(self):
		return (((self.receivingcompartment.fractionofareaavailableforverticaldiffusion * self.receivingcompartment.area)/self.currentchemical.z_pureair) * ((1/(self.currentchemical.z_pureair * self.masstransfercoefficient))+(1/(self.receivingcompartment.chemical_z_total * (self.receivingcompartment.chemical_d_effective / self.receivingcompartment.depth))))**(-1))

	@property
	def transferfractiontotal(self):
		mdict={}
		mdict['ae_notday']=(self.transferfractionleaf['ae_notday'] + self.transferfractionsoil) 
		mdict['ae_day']=(self.transferfractionleaf['ae_day'] + self.transferfractionsoil )
		mdict['no_ae']=(self.transferfractionleaf['no_ae'] + self.transferfractionsoil)
		return (mdict)

	@property
	def transferfactor(self):
		try:
			rleaf=self.dict_inputs["met_dict"]["frac_time_exchange_not_day"]*(self.transferfractionleaf['ae_notday']/self.transferfractiontotal['ae_notday'])+self.dict_inputs["met_dict"]["frac_time_exchange_day"]*(self.transferfractionleaf['ae_day']/self.transferfractiontotal['ae_day'])+(1-self.dict_inputs["met_dict"]["wt_av_allowexchange"])*(self.transferfractionleaf['no_ae']/self.transferfractiontotal['no_ae'])
			rsoil=self.dict_inputs["met_dict"]["frac_time_exchange_not_day"]*(self.transferfractionsoil/self.transferfractiontotal['ae_notday'])+self.dict_inputs["met_dict"]["frac_time_exchange_day"]*(self.transferfractionsoil/self.transferfractiontotal['ae_day'])+(1-self.dict_inputs["met_dict"]["wt_av_allowexchange"])*(self.transferfractionsoil/self.transferfractiontotal['no_ae'])
			r=rsoil/(rleaf+rsoil)
		except:
			r=nan    
		return(r)

''')
            
            
            if alg_name not in diff_algs_soil and alg_name not in diff_algs_leaf: # for regular algorithms
            

                residual_props=set(alg_props)-set(['transferfactor'])

    ### testing method decorator approach

                for prop in residual_props:
                    prop_val=grouped_alg.get_group(group).loc[grouped_alg.get_group(group)['property']==prop]['value'].values[0] #property value
                    prop_val=clean_props(prop_val)
                    if type(prop_val)==float or is_number(prop_val):
                        f.write('\n\t'+\
                                '_'+prop+'='+prop_val +'\n\t' +\
                                '@property'+'\n\t' +\
                                'def '+prop+'(self):'+'\n\t\t' +\
                                'return self._'+prop+'\n\n\t' +\
                                '@'+prop+'.setter''\n\t' +\
                                'def '+prop+'(self,value):'+'\n\t\t' +\
                                'self._'+prop+'=value\n')             
                    else:
                        if prop in ['category','receivingcompartmentcategory','sendingchemicalname','sendingcompartmentcategory','receivingchemicalname','compartmentrelationship','chemicalcategory','doestransformchemical','doestransportchemical','enabled','isdefaultforcategory','receivingchemicalname','receivingcompartmentcategory','sendingcompartmentcategory','sendingchemicalname','transferfactor']: # write as string
                            f.write('\n\t'+\
                                    '@property'+'\n\t' +\
                                    'def '+prop+'(self):'+'\n\t\t' +\
                                    'return ("'+prop_val+'")\n\t') 
                        else:
                            f.write('\n\t'+\
                                    '@property'+'\n\t' +\
                                    'def '+prop+'(self):'+'\n\t\t' +\
                                    'return ('+prop_val+')\n\t') 


                f.write('\n\t'+\
                        '@property'+'\n\t' +\
                        'def transferfactor(self):'+'\n\t\t' +\
                        'try:'+'\n\t\t\t' +\
                        'r='+tf+'\n\t\t' +\
                        'except:'+'\n\t\t\t' +\
                        'r=nan'+'\n\t\t'+\
                        'return (r)') 

                f.write('\n\n')    

                f.write('\n\n')    
            
    return(df_psalgs,df_psalg_mat,df_ps,df_pt)
    
    
if __name__ == '__main__':
    df_psalgs,df_psalg_mat,df_ps,df_pt=process_pseudo_library(inputs)
