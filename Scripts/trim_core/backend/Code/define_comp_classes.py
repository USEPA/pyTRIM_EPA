### Note: This is an auto generated script
from math import log
from numpy import nan
from numpy import sqrt

    
def Function_ChemicalTransferEfficiencyinFish(BW,log10_K_ow):
    if BW > 0.1:
        if log10_K_ow < 3:
            r=10 ** (-1.5 + 0.4 * log10_K_ow)
        else:
            if (log10_K_ow >= 3) and (log10_K_ow < 6):
               r=0.5 
            else:
                r=10 ** (1.2 - 0.25 * log10_K_ow) 
    else:
        if log10_K_ow < 5:
            r=10 ** (-2.6 + 0.5 * log10_K_ow)
        else:
            if (log10_K_ow >= 5) and (log10_K_ow < 6):
               r=0.8 
            else:
                r=10 ** (2.9 - 0.5 * log10_K_ow) 
    return(r)
        

class Advection_Sink:
	def __init__(self,Constants,containingScenario,currentChemical,containingVolumeElement):
		self.containingScenario=containingScenario
		self.currentChemical=currentChemical
		self.Constants=Constants
		self.containingVolumeElement=containingVolumeElement
		
		self.acceptableAbiotic=()
		self.acceptableAbiotic='nan'

		self.category=()
		self.category='Sink | Abiotic | Air | Air - Default'

		self.concentrationOutputUnits=()
		self.concentrationOutputUnits='0.01'

		self.isBiotic=()
		self.isBiotic=False

		self.concentrationOutputFactor=()
		self.concentrationOutputFactor=1.0

		self.VolumeFraction_Liquid={}
		try:
			self.Chemical_VolumeFraction_Liquid=self.VolumeFraction_Liquid[self.currentChemical.Name]
		except:
			self.Chemical_VolumeFraction_Liquid=nan

		self.VolumeFraction_Solid={}
		try:
			self.Chemical_VolumeFraction_Solid=self.VolumeFraction_Solid[self.currentChemical.Name]
		except:
			self.Chemical_VolumeFraction_Solid=nan

		self.GenericDenominatorforCalculatingFractioninPhases={}
		try:
			self.Chemical_GenericDenominatorforCalculatingFractioninPhases=self.GenericDenominatorforCalculatingFractioninPhases[self.currentChemical.Name]
		except:
			self.Chemical_GenericDenominatorforCalculatingFractioninPhases=nan

class Air:
	def __init__(self,Constants,containingScenario,currentChemical,containingVolumeElement):
		self.containingScenario=containingScenario
		self.currentChemical=currentChemical
		self.Constants=Constants
		self.containingVolumeElement=containingVolumeElement
		
		self.acceptableAbiotic=()
		self.acceptableAbiotic='nan'

		self.category=()
		self.category='Abiotic | Air | Air - Default'

		self.concentrationOutputUnits=()
		self.concentrationOutputUnits='ug/m3'

		self.isBiotic=()
		self.isBiotic=False

		self.AirDensity_g_cm3=()
		self.AirDensity_g_cm3=0.0012

		self.DemethylationRate={}
		self.DemethylationRate["Chem_MethylMercury"]=0.0
		try:
			self.Chemical_DemethylationRate=self.DemethylationRate[self.currentChemical.Name]
		except:
			self.Chemical_DemethylationRate=nan

		self.DustDensity=()
		self.DustDensity=1400.0

		self.DustLoad=()
		self.DustLoad=6.15E-8

		self.FractionOrganicMatteronParticulates=()
		self.FractionOrganicMatteronParticulates=0.2

		self.HalfLife={}
		self.HalfLife["Chem_1_2_3_4_6_7_8_9_OCDD"]=162.0
		self.HalfLife["Chem_1_2_3_4_6_7_8_9_OCDF"]=321.0
		self.HalfLife["Chem_1_2_3_4_6_7_8_HpCDD"]=64.0
		self.HalfLife["Chem_1_2_3_4_6_7_8_HpCDF"]=137.0
		self.HalfLife["Chem_1_2_3_4_7_8_9_HpCDF"]=122.0
		self.HalfLife["Chem_1_2_3_4_7_8_HxCDD"]=42.0
		self.HalfLife["Chem_1_2_3_4_7_8_HxCDF"]=78.0
		self.HalfLife["Chem_1_2_3_6_7_8_HxCDD"]=28.0
		self.HalfLife["Chem_1_2_3_6_7_8_HxCDF"]=55.0
		self.HalfLife["Chem_1_2_3_7_8_9_HxCDD"]=28.0
		self.HalfLife["Chem_1_2_3_7_8_9_HxCDF"]=51.0
		self.HalfLife["Chem_1_2_3_7_8_PeCDD"]=18.0
		self.HalfLife["Chem_1_2_3_7_8_PeCDF"]=31.0
		self.HalfLife["Chem_2_3_4_6_7_8_HxCDF"]=59.0
		self.HalfLife["Chem_2_3_4_7_8_PeCDF"]=33.0
		self.HalfLife["Chem_2_3_7_8_TCDD"]=12.0
		self.HalfLife["Chem_2_3_7_8_TCDF"]=19.0
		self.HalfLife["Chem_2_Methylnaphthalene"]=0.154
		self.HalfLife["Chem_7_12_Dimethylbenz_a_anthracene"]=0.092
		self.HalfLife["Chem_Acenaphthene"]=0.3
		self.HalfLife["Chem_Acenaphthylene"]=0.208
		self.HalfLife["Chem_Benz_a_anthracene"]=0.125
		self.HalfLife["Chem_Benzo_A_Pyrene"]=0.046
		self.HalfLife["Chem_Benzo_b_fluoranthene"]=0.596
		self.HalfLife["Chem_Benzo_g_h_i_perylene"]=0.215
		self.HalfLife["Chem_Benzo_k_fluoranthene"]=0.458
		self.HalfLife["Chem_Chrysene"]=0.334
		self.HalfLife["Chem_Dibenz_a_h_anthracene"]=0.178
		self.HalfLife["Chem_Fluoranthene"]=0.46
		self.HalfLife["Chem_Fluorene"]=0.46
		self.HalfLife["Chem_Indeno_1_2_3_cd_pyrene"]=0.262
		try:
			self.Chemical_HalfLife=self.HalfLife[self.currentChemical.Name]
		except:
			self.Chemical_HalfLife=nan

		self.MethylationRate={}
		self.MethylationRate["Chem_Divalent_Mercury"]=0.0
		try:
			self.Chemical_MethylationRate=self.MethylationRate[self.currentChemical.Name]
		except:
			self.Chemical_MethylationRate=nan

		self.OxidationRate={}
		self.OxidationRate["Chem_Elemental_Mercury"]=0.00385081766977747
		try:
			self.Chemical_OxidationRate=self.OxidationRate[self.currentChemical.Name]
		except:
			self.Chemical_OxidationRate=nan

		self.ReductionRate={}
		self.ReductionRate["Chem_Divalent_Mercury"]=0.0
		try:
			self.Chemical_ReductionRate=self.ReductionRate[self.currentChemical.Name]
		except:
			self.Chemical_ReductionRate=nan

		self.WashoutRatio={}
		self.WashoutRatio["Chem_1_2_3_4_6_7_8_9_OCDD"]=91000.0
		self.WashoutRatio["Chem_1_2_3_4_6_7_8_9_OCDF"]=22000.0
		self.WashoutRatio["Chem_1_2_3_4_6_7_8_HpCDD"]=64000.0
		self.WashoutRatio["Chem_1_2_3_4_6_7_8_HpCDF"]=32000.0
		self.WashoutRatio["Chem_1_2_3_4_7_8_9_HpCDF"]=32000.0
		self.WashoutRatio["Chem_1_2_3_4_7_8_HxCDD"]=9000.0
		self.WashoutRatio["Chem_1_2_3_4_7_8_HxCDF"]=10000.0
		self.WashoutRatio["Chem_1_2_3_6_7_8_HxCDD"]=9000.0
		self.WashoutRatio["Chem_1_2_3_6_7_8_HxCDF"]=10000.0
		self.WashoutRatio["Chem_1_2_3_7_8_9_HxCDD"]=9000.0
		self.WashoutRatio["Chem_1_2_3_7_8_9_HxCDF"]=10000.0
		self.WashoutRatio["Chem_1_2_3_7_8_PeCDD"]=18000.0
		self.WashoutRatio["Chem_1_2_3_7_8_PeCDF"]=13000.0
		self.WashoutRatio["Chem_2_3_4_6_7_8_HxCDF"]=10000.0
		self.WashoutRatio["Chem_2_3_4_7_8_PeCDF"]=14000.0
		self.WashoutRatio["Chem_2_3_7_8_TCDD"]=18000.0
		self.WashoutRatio["Chem_2_3_7_8_TCDF"]=19000.0
		self.WashoutRatio["Chem_2_Methylnaphthalene"]=200000.0
		self.WashoutRatio["Chem_7_12_Dimethylbenz_a_anthracene"]=200000.0
		self.WashoutRatio["Chem_Acenaphthene"]=200000.0
		self.WashoutRatio["Chem_Acenaphthylene"]=200000.0
		self.WashoutRatio["Chem_Arsenic"]=200000.0
		self.WashoutRatio["Chem_Benz_a_anthracene"]=200000.0
		self.WashoutRatio["Chem_Benzo_A_Pyrene"]=200000.0
		self.WashoutRatio["Chem_Benzo_b_fluoranthene"]=200000.0
		self.WashoutRatio["Chem_Benzo_g_h_i_perylene"]=200000.0
		self.WashoutRatio["Chem_Benzo_k_fluoranthene"]=200000.0
		self.WashoutRatio["Chem_Cadmium"]=200000.0
		self.WashoutRatio["Chem_Chrysene"]=200000.0
		self.WashoutRatio["Chem_Dibenz_a_h_anthracene"]=200000.0
		self.WashoutRatio["Chem_Divalent_Mercury"]=200000.0
		self.WashoutRatio["Chem_Elemental_Mercury"]=200000.0
		self.WashoutRatio["Chem_Fluoranthene"]=200000.0
		self.WashoutRatio["Chem_Fluorene"]=200000.0
		self.WashoutRatio["Chem_Indeno_1_2_3_cd_pyrene"]=200000.0
		self.WashoutRatio["Chem_Lead"]=330000.0
		self.WashoutRatio["Chem_MethylMercury"]=200000.0
		try:
			self.Chemical_WashoutRatio=self.WashoutRatio[self.currentChemical.Name]
		except:
			self.Chemical_WashoutRatio=nan

		self.concentrationOutputFactor=()
		self.concentrationOutputFactor=1000000.0

		self.initialConcentration_g_per_m3_UserSupplied={}
		self.initialConcentration_g_per_m3_UserSupplied["Chem_1_2_3_4_6_7_8_9_OCDD"]=0.0
		self.initialConcentration_g_per_m3_UserSupplied["Chem_1_2_3_4_6_7_8_9_OCDF"]=0.0
		self.initialConcentration_g_per_m3_UserSupplied["Chem_1_2_3_4_6_7_8_HpCDD"]=0.0
		self.initialConcentration_g_per_m3_UserSupplied["Chem_1_2_3_4_6_7_8_HpCDF"]=0.0
		self.initialConcentration_g_per_m3_UserSupplied["Chem_1_2_3_4_7_8_9_HpCDF"]=0.0
		self.initialConcentration_g_per_m3_UserSupplied["Chem_1_2_3_4_7_8_HxCDD"]=0.0
		self.initialConcentration_g_per_m3_UserSupplied["Chem_1_2_3_4_7_8_HxCDF"]=0.0
		self.initialConcentration_g_per_m3_UserSupplied["Chem_1_2_3_6_7_8_HxCDD"]=0.0
		self.initialConcentration_g_per_m3_UserSupplied["Chem_1_2_3_6_7_8_HxCDF"]=0.0
		self.initialConcentration_g_per_m3_UserSupplied["Chem_1_2_3_7_8_9_HxCDD"]=0.0
		self.initialConcentration_g_per_m3_UserSupplied["Chem_1_2_3_7_8_9_HxCDF"]=0.0
		self.initialConcentration_g_per_m3_UserSupplied["Chem_1_2_3_7_8_PeCDD"]=0.0
		self.initialConcentration_g_per_m3_UserSupplied["Chem_1_2_3_7_8_PeCDF"]=0.0
		self.initialConcentration_g_per_m3_UserSupplied["Chem_2_3_4_6_7_8_HxCDF"]=0.0
		self.initialConcentration_g_per_m3_UserSupplied["Chem_2_3_4_7_8_PeCDF"]=0.0
		self.initialConcentration_g_per_m3_UserSupplied["Chem_2_3_7_8_TCDD"]=0.0
		self.initialConcentration_g_per_m3_UserSupplied["Chem_2_3_7_8_TCDF"]=0.0
		self.initialConcentration_g_per_m3_UserSupplied["Chem_2_Methylnaphthalene"]=0.0
		self.initialConcentration_g_per_m3_UserSupplied["Chem_7_12_Dimethylbenz_a_anthracene"]=0.0
		self.initialConcentration_g_per_m3_UserSupplied["Chem_Acenaphthene"]=0.0
		self.initialConcentration_g_per_m3_UserSupplied["Chem_Acenaphthylene"]=0.0
		self.initialConcentration_g_per_m3_UserSupplied["Chem_Arsenic"]=0.0
		self.initialConcentration_g_per_m3_UserSupplied["Chem_Benz_a_anthracene"]=0.0
		self.initialConcentration_g_per_m3_UserSupplied["Chem_Benzo_A_Pyrene"]=0.0
		self.initialConcentration_g_per_m3_UserSupplied["Chem_Benzo_b_fluoranthene"]=0.0
		self.initialConcentration_g_per_m3_UserSupplied["Chem_Benzo_g_h_i_perylene"]=0.0
		self.initialConcentration_g_per_m3_UserSupplied["Chem_Benzo_k_fluoranthene"]=0.0
		self.initialConcentration_g_per_m3_UserSupplied["Chem_Cadmium"]=0.0
		self.initialConcentration_g_per_m3_UserSupplied["Chem_Chrysene"]=0.0
		self.initialConcentration_g_per_m3_UserSupplied["Chem_Dibenz_a_h_anthracene"]=0.0
		self.initialConcentration_g_per_m3_UserSupplied["Chem_Divalent_Mercury"]=0.0
		self.initialConcentration_g_per_m3_UserSupplied["Chem_Elemental_Mercury"]=0.0
		self.initialConcentration_g_per_m3_UserSupplied["Chem_Fluoranthene"]=0.0
		self.initialConcentration_g_per_m3_UserSupplied["Chem_Fluorene"]=0.0
		self.initialConcentration_g_per_m3_UserSupplied["Chem_Indeno_1_2_3_cd_pyrene"]=0.0
		self.initialConcentration_g_per_m3_UserSupplied["Chem_MethylMercury"]=0.0
		try:
			self.Chemical_initialConcentration_g_per_m3_UserSupplied=self.initialConcentration_g_per_m3_UserSupplied[self.currentChemical.Name]
		except:
			self.Chemical_initialConcentration_g_per_m3_UserSupplied=nan

		self.vdep={}
		self.vdep["Chem_1_2_3_4_6_7_8_9_OCDD"]=500.0
		self.vdep["Chem_1_2_3_4_6_7_8_9_OCDF"]=500.0
		self.vdep["Chem_1_2_3_4_6_7_8_HpCDD"]=500.0
		self.vdep["Chem_1_2_3_4_6_7_8_HpCDF"]=500.0
		self.vdep["Chem_1_2_3_4_7_8_9_HpCDF"]=500.0
		self.vdep["Chem_1_2_3_4_7_8_HxCDD"]=500.0
		self.vdep["Chem_1_2_3_4_7_8_HxCDF"]=500.0
		self.vdep["Chem_1_2_3_6_7_8_HxCDD"]=500.0
		self.vdep["Chem_1_2_3_6_7_8_HxCDF"]=500.0
		self.vdep["Chem_1_2_3_7_8_9_HxCDD"]=500.0
		self.vdep["Chem_1_2_3_7_8_9_HxCDF"]=500.0
		self.vdep["Chem_1_2_3_7_8_PeCDD"]=500.0
		self.vdep["Chem_1_2_3_7_8_PeCDF"]=500.0
		self.vdep["Chem_2_3_4_6_7_8_HxCDF"]=500.0
		self.vdep["Chem_2_3_4_7_8_PeCDF"]=500.0
		self.vdep["Chem_2_3_7_8_TCDD"]=500.0
		self.vdep["Chem_2_3_7_8_TCDF"]=500.0
		self.vdep["Chem_2_Methylnaphthalene"]=500.0
		self.vdep["Chem_7_12_Dimethylbenz_a_anthracene"]=500.0
		self.vdep["Chem_Acenaphthene"]=500.0
		self.vdep["Chem_Acenaphthylene"]=500.0
		self.vdep["Chem_Arsenic"]=500.0
		self.vdep["Chem_Benz_a_anthracene"]=500.0
		self.vdep["Chem_Benzo_A_Pyrene"]=500.0
		self.vdep["Chem_Benzo_b_fluoranthene"]=500.0
		self.vdep["Chem_Benzo_g_h_i_perylene"]=500.0
		self.vdep["Chem_Benzo_k_fluoranthene"]=500.0
		self.vdep["Chem_Cadmium"]=260.0
		self.vdep["Chem_Chrysene"]=500.0
		self.vdep["Chem_Dibenz_a_h_anthracene"]=500.0
		self.vdep["Chem_Divalent_Mercury"]=500.0
		self.vdep["Chem_Elemental_Mercury"]=500.0
		self.vdep["Chem_Fluoranthene"]=500.0
		self.vdep["Chem_Fluorene"]=500.0
		self.vdep["Chem_Indeno_1_2_3_cd_pyrene"]=500.0
		self.vdep["Chem_Lead"]=500.0
		self.vdep["Chem_MethylMercury"]=500.0
		try:
			self.Chemical_vdep=self.vdep[self.currentChemical.Name]
		except:
			self.Chemical_vdep=nan

		self.AirDensity_kg_m3=()
		self.AirDensity_kg_m3=self.AirDensity_g_cm3 * 1000.0

		self.AirTemperature_C=()
		self.AirTemperature_C=self.containingScenario.AirTemperature_K - 273

		self.GeneralDegradationRate={}
		self.GeneralDegradationRate["Chem_1_2_3_4_6_7_8_9_OCDD"]=log(2)/ self.Chemical_HalfLife
		self.GeneralDegradationRate["Chem_1_2_3_4_6_7_8_9_OCDF"]=log(2)/ self.Chemical_HalfLife
		self.GeneralDegradationRate["Chem_1_2_3_4_6_7_8_HpCDD"]=log(2)/ self.Chemical_HalfLife
		self.GeneralDegradationRate["Chem_1_2_3_4_6_7_8_HpCDF"]=log(2)/ self.Chemical_HalfLife
		self.GeneralDegradationRate["Chem_1_2_3_4_7_8_9_HpCDF"]=log(2)/ self.Chemical_HalfLife
		self.GeneralDegradationRate["Chem_1_2_3_4_7_8_HxCDD"]=log(2)/ self.Chemical_HalfLife
		self.GeneralDegradationRate["Chem_1_2_3_4_7_8_HxCDF"]=log(2)/ self.Chemical_HalfLife
		self.GeneralDegradationRate["Chem_1_2_3_6_7_8_HxCDD"]=log(2)/ self.Chemical_HalfLife
		self.GeneralDegradationRate["Chem_1_2_3_6_7_8_HxCDF"]=log(2)/ self.Chemical_HalfLife
		self.GeneralDegradationRate["Chem_1_2_3_7_8_9_HxCDD"]=log(2)/ self.Chemical_HalfLife
		self.GeneralDegradationRate["Chem_1_2_3_7_8_9_HxCDF"]=log(2)/ self.Chemical_HalfLife
		self.GeneralDegradationRate["Chem_1_2_3_7_8_PeCDD"]=log(2)/ self.Chemical_HalfLife
		self.GeneralDegradationRate["Chem_1_2_3_7_8_PeCDF"]=log(2)/ self.Chemical_HalfLife
		self.GeneralDegradationRate["Chem_2_3_4_6_7_8_HxCDF"]=log(2)/ self.Chemical_HalfLife
		self.GeneralDegradationRate["Chem_2_3_4_7_8_PeCDF"]=log(2)/ self.Chemical_HalfLife
		self.GeneralDegradationRate["Chem_2_3_7_8_TCDD"]=log(2)/ self.Chemical_HalfLife
		self.GeneralDegradationRate["Chem_2_3_7_8_TCDF"]=log(2)/ self.Chemical_HalfLife
		self.GeneralDegradationRate["Chem_2_Methylnaphthalene"]=log(2)/ self.Chemical_HalfLife
		self.GeneralDegradationRate["Chem_7_12_Dimethylbenz_a_anthracene"]=log(2)/ self.Chemical_HalfLife
		self.GeneralDegradationRate["Chem_Acenaphthene"]=log(2)/ self.Chemical_HalfLife
		self.GeneralDegradationRate["Chem_Acenaphthylene"]=log(2)/ self.Chemical_HalfLife
		self.GeneralDegradationRate["Chem_Benz_a_anthracene"]=log(2)/ self.Chemical_HalfLife
		self.GeneralDegradationRate["Chem_Benzo_A_Pyrene"]=log(2)/ self.Chemical_HalfLife
		self.GeneralDegradationRate["Chem_Benzo_b_fluoranthene"]=log(2)/ self.Chemical_HalfLife
		self.GeneralDegradationRate["Chem_Benzo_g_h_i_perylene"]=log(2)/ self.Chemical_HalfLife
		self.GeneralDegradationRate["Chem_Benzo_k_fluoranthene"]=log(2)/ self.Chemical_HalfLife
		self.GeneralDegradationRate["Chem_Chrysene"]=log(2)/ self.Chemical_HalfLife
		self.GeneralDegradationRate["Chem_Dibenz_a_h_anthracene"]=log(2)/ self.Chemical_HalfLife
		self.GeneralDegradationRate["Chem_Fluoranthene"]=log(2)/ self.Chemical_HalfLife
		self.GeneralDegradationRate["Chem_Fluorene"]=log(2)/ self.Chemical_HalfLife
		self.GeneralDegradationRate["Chem_Indeno_1_2_3_cd_pyrene"]=log(2)/ self.Chemical_HalfLife
		try:
			self.Chemical_GeneralDegradationRate=self.GeneralDegradationRate[self.currentChemical.Name]
		except:
			self.Chemical_GeneralDegradationRate=nan

		self.GenericDenominatorforCalculatingFractioninPhases={}
		self.GenericDenominatorforCalculatingFractioninPhases["Chem_Indeno_1_2_3_cd_pyrene"]=log(2)/ self.Chemical_HalfLife
		try:
			self.Chemical_GenericDenominatorforCalculatingFractioninPhases=self.GenericDenominatorforCalculatingFractioninPhases[self.currentChemical.Name]
		except:
			self.Chemical_GenericDenominatorforCalculatingFractioninPhases=nan

		self.ParticleGasPartitionCoefficient={}
		self.ParticleGasPartitionCoefficient["Chem_1_2_3_4_6_7_8_9_OCDD"]=10** ( self.currentChemical.log10_K_OA  + log(self.FractionOrganicMatteronParticulates+1.0e-10)/log(10) - 11.91)
		self.ParticleGasPartitionCoefficient["Chem_1_2_3_4_6_7_8_9_OCDF"]=10** ( self.currentChemical.log10_K_OA  + log(self.FractionOrganicMatteronParticulates+1.0e-10)/log(10) - 11.91)
		self.ParticleGasPartitionCoefficient["Chem_1_2_3_4_6_7_8_HpCDD"]=10** ( self.currentChemical.log10_K_OA  + log(self.FractionOrganicMatteronParticulates+1.0e-10)/log(10) - 11.91)
		self.ParticleGasPartitionCoefficient["Chem_1_2_3_4_6_7_8_HpCDF"]=10** ( self.currentChemical.log10_K_OA  + log(self.FractionOrganicMatteronParticulates+1.0e-10)/log(10) - 11.91)
		self.ParticleGasPartitionCoefficient["Chem_1_2_3_4_7_8_9_HpCDF"]=10** ( self.currentChemical.log10_K_OA  + log(self.FractionOrganicMatteronParticulates+1.0e-10)/log(10) - 11.91)
		self.ParticleGasPartitionCoefficient["Chem_1_2_3_4_7_8_HxCDD"]=10** ( self.currentChemical.log10_K_OA  + log(self.FractionOrganicMatteronParticulates+1.0e-10)/log(10) - 11.91)
		self.ParticleGasPartitionCoefficient["Chem_1_2_3_4_7_8_HxCDF"]=10** ( self.currentChemical.log10_K_OA  + log(self.FractionOrganicMatteronParticulates+1.0e-10)/log(10) - 11.91)
		self.ParticleGasPartitionCoefficient["Chem_1_2_3_6_7_8_HxCDD"]=10** ( self.currentChemical.log10_K_OA  + log(self.FractionOrganicMatteronParticulates+1.0e-10)/log(10) - 11.91)
		self.ParticleGasPartitionCoefficient["Chem_1_2_3_6_7_8_HxCDF"]=10** ( self.currentChemical.log10_K_OA  + log(self.FractionOrganicMatteronParticulates+1.0e-10)/log(10) - 11.91)
		self.ParticleGasPartitionCoefficient["Chem_1_2_3_7_8_9_HxCDD"]=10** ( self.currentChemical.log10_K_OA  + log(self.FractionOrganicMatteronParticulates+1.0e-10)/log(10) - 11.91)
		self.ParticleGasPartitionCoefficient["Chem_1_2_3_7_8_9_HxCDF"]=10** ( self.currentChemical.log10_K_OA  + log(self.FractionOrganicMatteronParticulates+1.0e-10)/log(10) - 11.91)
		self.ParticleGasPartitionCoefficient["Chem_1_2_3_7_8_PeCDD"]=10** ( self.currentChemical.log10_K_OA  + log(self.FractionOrganicMatteronParticulates+1.0e-10)/log(10) - 11.91)
		self.ParticleGasPartitionCoefficient["Chem_1_2_3_7_8_PeCDF"]=10** ( self.currentChemical.log10_K_OA  + log(self.FractionOrganicMatteronParticulates+1.0e-10)/log(10) - 11.91)
		self.ParticleGasPartitionCoefficient["Chem_2_3_4_6_7_8_HxCDF"]=10** ( self.currentChemical.log10_K_OA  + log(self.FractionOrganicMatteronParticulates+1.0e-10)/log(10) - 11.91)
		self.ParticleGasPartitionCoefficient["Chem_2_3_4_7_8_PeCDF"]=10** ( self.currentChemical.log10_K_OA  + log(self.FractionOrganicMatteronParticulates+1.0e-10)/log(10) - 11.91)
		self.ParticleGasPartitionCoefficient["Chem_2_3_7_8_TCDD"]=10** ( self.currentChemical.log10_K_OA  + log(self.FractionOrganicMatteronParticulates+1.0e-10)/log(10) - 11.91)
		self.ParticleGasPartitionCoefficient["Chem_2_3_7_8_TCDF"]=10** ( self.currentChemical.log10_K_OA  + log(self.FractionOrganicMatteronParticulates+1.0e-10)/log(10) - 11.91)
		self.ParticleGasPartitionCoefficient["Chem_2_Methylnaphthalene"]=10** ( self.currentChemical.log10_K_OA  + log(self.FractionOrganicMatteronParticulates+1.0e-10)/log(10) - 11.91)
		self.ParticleGasPartitionCoefficient["Chem_7_12_Dimethylbenz_a_anthracene"]=10** ( self.currentChemical.log10_K_OA  + log(self.FractionOrganicMatteronParticulates+1.0e-10)/log(10) - 11.91)
		self.ParticleGasPartitionCoefficient["Chem_Acenaphthene"]=10** ( self.currentChemical.log10_K_OA  + log(self.FractionOrganicMatteronParticulates+1.0e-10)/log(10) - 11.91)
		self.ParticleGasPartitionCoefficient["Chem_Acenaphthylene"]=10** ( self.currentChemical.log10_K_OA  + log(self.FractionOrganicMatteronParticulates+1.0e-10)/log(10) - 11.91)
		self.ParticleGasPartitionCoefficient["Chem_Benz_a_anthracene"]=10** ( self.currentChemical.log10_K_OA  + log(self.FractionOrganicMatteronParticulates+1.0e-10)/log(10) - 11.91)
		self.ParticleGasPartitionCoefficient["Chem_Benzo_A_Pyrene"]=10** ( self.currentChemical.log10_K_OA  + log(self.FractionOrganicMatteronParticulates+1.0e-10)/log(10) - 11.91)
		self.ParticleGasPartitionCoefficient["Chem_Benzo_b_fluoranthene"]=10** ( self.currentChemical.log10_K_OA  + log(self.FractionOrganicMatteronParticulates+1.0e-10)/log(10) - 11.91)
		self.ParticleGasPartitionCoefficient["Chem_Benzo_g_h_i_perylene"]=10** ( self.currentChemical.log10_K_OA  + log(self.FractionOrganicMatteronParticulates+1.0e-10)/log(10) - 11.91)
		self.ParticleGasPartitionCoefficient["Chem_Benzo_k_fluoranthene"]=10** ( self.currentChemical.log10_K_OA  + log(self.FractionOrganicMatteronParticulates+1.0e-10)/log(10) - 11.91)
		self.ParticleGasPartitionCoefficient["Chem_Chrysene"]=10** ( self.currentChemical.log10_K_OA  + log(self.FractionOrganicMatteronParticulates+1.0e-10)/log(10) - 11.91)
		self.ParticleGasPartitionCoefficient["Chem_Dibenz_a_h_anthracene"]=10** ( self.currentChemical.log10_K_OA  + log(self.FractionOrganicMatteronParticulates+1.0e-10)/log(10) - 11.91)
		self.ParticleGasPartitionCoefficient["Chem_Divalent_Mercury"]=10** ( self.currentChemical.log10_K_OA  + log(self.FractionOrganicMatteronParticulates+1.0e-10)/log(10) - 11.91)
		self.ParticleGasPartitionCoefficient["Chem_Elemental_Mercury"]=10** ( self.currentChemical.log10_K_OA  + log(self.FractionOrganicMatteronParticulates+1.0e-10)/log(10) - 11.91)
		self.ParticleGasPartitionCoefficient["Chem_Fluoranthene"]=10** ( self.currentChemical.log10_K_OA  + log(self.FractionOrganicMatteronParticulates+1.0e-10)/log(10) - 11.91)
		self.ParticleGasPartitionCoefficient["Chem_Fluorene"]=10** ( self.currentChemical.log10_K_OA  + log(self.FractionOrganicMatteronParticulates+1.0e-10)/log(10) - 11.91)
		self.ParticleGasPartitionCoefficient["Chem_Indeno_1_2_3_cd_pyrene"]=10** ( self.currentChemical.log10_K_OA  + log(self.FractionOrganicMatteronParticulates+1.0e-10)/log(10) - 11.91)
		self.ParticleGasPartitionCoefficient["Chem_Lead"]=10** ( self.currentChemical.log10_K_OA  + log(self.FractionOrganicMatteronParticulates+1.0e-10)/log(10) - 11.91)
		self.ParticleGasPartitionCoefficient["Chem_MethylMercury"]=10** ( self.currentChemical.log10_K_OA  + log(self.FractionOrganicMatteronParticulates+1.0e-10)/log(10) - 11.91)
		try:
			self.Chemical_ParticleGasPartitionCoefficient=self.ParticleGasPartitionCoefficient[self.currentChemical.Name]
		except:
			self.Chemical_ParticleGasPartitionCoefficient=nan

		self.ParticleVolumetricDRYDepositionRate={}
		self.ParticleVolumetricDRYDepositionRate["Chem_1_2_3_4_6_7_8_9_OCDD"]=self.Chemical_vdep * (self.DustLoad / self.DustDensity)
		self.ParticleVolumetricDRYDepositionRate["Chem_1_2_3_4_6_7_8_9_OCDF"]=self.Chemical_vdep * (self.DustLoad / self.DustDensity)
		self.ParticleVolumetricDRYDepositionRate["Chem_1_2_3_4_6_7_8_HpCDD"]=self.Chemical_vdep * (self.DustLoad / self.DustDensity)
		self.ParticleVolumetricDRYDepositionRate["Chem_1_2_3_4_6_7_8_HpCDF"]=self.Chemical_vdep * (self.DustLoad / self.DustDensity)
		self.ParticleVolumetricDRYDepositionRate["Chem_1_2_3_4_7_8_9_HpCDF"]=self.Chemical_vdep * (self.DustLoad / self.DustDensity)
		self.ParticleVolumetricDRYDepositionRate["Chem_1_2_3_4_7_8_HxCDD"]=self.Chemical_vdep * (self.DustLoad / self.DustDensity)
		self.ParticleVolumetricDRYDepositionRate["Chem_1_2_3_4_7_8_HxCDF"]=self.Chemical_vdep * (self.DustLoad / self.DustDensity)
		self.ParticleVolumetricDRYDepositionRate["Chem_1_2_3_6_7_8_HxCDD"]=self.Chemical_vdep * (self.DustLoad / self.DustDensity)
		self.ParticleVolumetricDRYDepositionRate["Chem_1_2_3_6_7_8_HxCDF"]=self.Chemical_vdep * (self.DustLoad / self.DustDensity)
		self.ParticleVolumetricDRYDepositionRate["Chem_1_2_3_7_8_9_HxCDD"]=self.Chemical_vdep * (self.DustLoad / self.DustDensity)
		self.ParticleVolumetricDRYDepositionRate["Chem_1_2_3_7_8_9_HxCDF"]=self.Chemical_vdep * (self.DustLoad / self.DustDensity)
		self.ParticleVolumetricDRYDepositionRate["Chem_1_2_3_7_8_PeCDD"]=self.Chemical_vdep * (self.DustLoad / self.DustDensity)
		self.ParticleVolumetricDRYDepositionRate["Chem_1_2_3_7_8_PeCDF"]=self.Chemical_vdep * (self.DustLoad / self.DustDensity)
		self.ParticleVolumetricDRYDepositionRate["Chem_2_3_4_6_7_8_HxCDF"]=self.Chemical_vdep * (self.DustLoad / self.DustDensity)
		self.ParticleVolumetricDRYDepositionRate["Chem_2_3_4_7_8_PeCDF"]=self.Chemical_vdep * (self.DustLoad / self.DustDensity)
		self.ParticleVolumetricDRYDepositionRate["Chem_2_3_7_8_TCDD"]=self.Chemical_vdep * (self.DustLoad / self.DustDensity)
		self.ParticleVolumetricDRYDepositionRate["Chem_2_3_7_8_TCDF"]=self.Chemical_vdep * (self.DustLoad / self.DustDensity)
		self.ParticleVolumetricDRYDepositionRate["Chem_2_Methylnaphthalene"]=self.Chemical_vdep * (self.DustLoad / self.DustDensity)
		self.ParticleVolumetricDRYDepositionRate["Chem_7_12_Dimethylbenz_a_anthracene"]=self.Chemical_vdep * (self.DustLoad / self.DustDensity)
		self.ParticleVolumetricDRYDepositionRate["Chem_Acenaphthene"]=self.Chemical_vdep * (self.DustLoad / self.DustDensity)
		self.ParticleVolumetricDRYDepositionRate["Chem_Acenaphthylene"]=self.Chemical_vdep * (self.DustLoad / self.DustDensity)
		self.ParticleVolumetricDRYDepositionRate["Chem_Arsenic"]=self.Chemical_vdep * (self.DustLoad / self.DustDensity)
		self.ParticleVolumetricDRYDepositionRate["Chem_Benz_a_anthracene"]=self.Chemical_vdep * (self.DustLoad / self.DustDensity)
		self.ParticleVolumetricDRYDepositionRate["Chem_Benzo_A_Pyrene"]=self.Chemical_vdep * (self.DustLoad / self.DustDensity)
		self.ParticleVolumetricDRYDepositionRate["Chem_Benzo_b_fluoranthene"]=self.Chemical_vdep * (self.DustLoad / self.DustDensity)
		self.ParticleVolumetricDRYDepositionRate["Chem_Benzo_g_h_i_perylene"]=self.Chemical_vdep * (self.DustLoad / self.DustDensity)
		self.ParticleVolumetricDRYDepositionRate["Chem_Benzo_k_fluoranthene"]=self.Chemical_vdep * (self.DustLoad / self.DustDensity)
		self.ParticleVolumetricDRYDepositionRate["Chem_Cadmium"]=self.Chemical_vdep * (self.DustLoad / self.DustDensity)
		self.ParticleVolumetricDRYDepositionRate["Chem_Chrysene"]=self.Chemical_vdep * (self.DustLoad / self.DustDensity)
		self.ParticleVolumetricDRYDepositionRate["Chem_Dibenz_a_h_anthracene"]=self.Chemical_vdep * (self.DustLoad / self.DustDensity)
		self.ParticleVolumetricDRYDepositionRate["Chem_Divalent_Mercury"]=self.Chemical_vdep * (self.DustLoad / self.DustDensity)
		self.ParticleVolumetricDRYDepositionRate["Chem_Elemental_Mercury"]=self.Chemical_vdep * (self.DustLoad / self.DustDensity)
		self.ParticleVolumetricDRYDepositionRate["Chem_Fluoranthene"]=self.Chemical_vdep * (self.DustLoad / self.DustDensity)
		self.ParticleVolumetricDRYDepositionRate["Chem_Fluorene"]=self.Chemical_vdep * (self.DustLoad / self.DustDensity)
		self.ParticleVolumetricDRYDepositionRate["Chem_Indeno_1_2_3_cd_pyrene"]=self.Chemical_vdep * (self.DustLoad / self.DustDensity)
		self.ParticleVolumetricDRYDepositionRate["Chem_Lead"]=self.Chemical_vdep * (self.DustLoad / self.DustDensity)
		self.ParticleVolumetricDRYDepositionRate["Chem_MethylMercury"]=self.Chemical_vdep * (self.DustLoad / self.DustDensity)
		try:
			self.Chemical_ParticleVolumetricDRYDepositionRate=self.ParticleVolumetricDRYDepositionRate[self.currentChemical.Name]
		except:
			self.Chemical_ParticleVolumetricDRYDepositionRate=nan

		self.ParticleVolumetricWetDepositionRate={}
		self.ParticleVolumetricWetDepositionRate["Chem_1_2_3_4_6_7_8_9_OCDD"]=self.Chemical_WashoutRatio * self.containingScenario.Rain * (self.DustLoad / self.DustDensity)
		self.ParticleVolumetricWetDepositionRate["Chem_1_2_3_4_6_7_8_9_OCDF"]=self.Chemical_WashoutRatio * self.containingScenario.Rain * (self.DustLoad / self.DustDensity)
		self.ParticleVolumetricWetDepositionRate["Chem_1_2_3_4_6_7_8_HpCDD"]=self.Chemical_WashoutRatio * self.containingScenario.Rain * (self.DustLoad / self.DustDensity)
		self.ParticleVolumetricWetDepositionRate["Chem_1_2_3_4_6_7_8_HpCDF"]=self.Chemical_WashoutRatio * self.containingScenario.Rain * (self.DustLoad / self.DustDensity)
		self.ParticleVolumetricWetDepositionRate["Chem_1_2_3_4_7_8_9_HpCDF"]=self.Chemical_WashoutRatio * self.containingScenario.Rain * (self.DustLoad / self.DustDensity)
		self.ParticleVolumetricWetDepositionRate["Chem_1_2_3_4_7_8_HxCDD"]=self.Chemical_WashoutRatio * self.containingScenario.Rain * (self.DustLoad / self.DustDensity)
		self.ParticleVolumetricWetDepositionRate["Chem_1_2_3_4_7_8_HxCDF"]=self.Chemical_WashoutRatio * self.containingScenario.Rain * (self.DustLoad / self.DustDensity)
		self.ParticleVolumetricWetDepositionRate["Chem_1_2_3_6_7_8_HxCDD"]=self.Chemical_WashoutRatio * self.containingScenario.Rain * (self.DustLoad / self.DustDensity)
		self.ParticleVolumetricWetDepositionRate["Chem_1_2_3_6_7_8_HxCDF"]=self.Chemical_WashoutRatio * self.containingScenario.Rain * (self.DustLoad / self.DustDensity)
		self.ParticleVolumetricWetDepositionRate["Chem_1_2_3_7_8_9_HxCDD"]=self.Chemical_WashoutRatio * self.containingScenario.Rain * (self.DustLoad / self.DustDensity)
		self.ParticleVolumetricWetDepositionRate["Chem_1_2_3_7_8_9_HxCDF"]=self.Chemical_WashoutRatio * self.containingScenario.Rain * (self.DustLoad / self.DustDensity)
		self.ParticleVolumetricWetDepositionRate["Chem_1_2_3_7_8_PeCDD"]=self.Chemical_WashoutRatio * self.containingScenario.Rain * (self.DustLoad / self.DustDensity)
		self.ParticleVolumetricWetDepositionRate["Chem_1_2_3_7_8_PeCDF"]=self.Chemical_WashoutRatio * self.containingScenario.Rain * (self.DustLoad / self.DustDensity)
		self.ParticleVolumetricWetDepositionRate["Chem_2_3_4_6_7_8_HxCDF"]=self.Chemical_WashoutRatio * self.containingScenario.Rain * (self.DustLoad / self.DustDensity)
		self.ParticleVolumetricWetDepositionRate["Chem_2_3_4_7_8_PeCDF"]=self.Chemical_WashoutRatio * self.containingScenario.Rain * (self.DustLoad / self.DustDensity)
		self.ParticleVolumetricWetDepositionRate["Chem_2_3_7_8_TCDD"]=self.Chemical_WashoutRatio * self.containingScenario.Rain * (self.DustLoad / self.DustDensity)
		self.ParticleVolumetricWetDepositionRate["Chem_2_3_7_8_TCDF"]=self.Chemical_WashoutRatio * self.containingScenario.Rain * (self.DustLoad / self.DustDensity)
		self.ParticleVolumetricWetDepositionRate["Chem_2_Methylnaphthalene"]=self.Chemical_WashoutRatio * self.containingScenario.Rain * (self.DustLoad / self.DustDensity)
		self.ParticleVolumetricWetDepositionRate["Chem_7_12_Dimethylbenz_a_anthracene"]=self.Chemical_WashoutRatio * self.containingScenario.Rain * (self.DustLoad / self.DustDensity)
		self.ParticleVolumetricWetDepositionRate["Chem_Acenaphthene"]=self.Chemical_WashoutRatio * self.containingScenario.Rain * (self.DustLoad / self.DustDensity)
		self.ParticleVolumetricWetDepositionRate["Chem_Acenaphthylene"]=self.Chemical_WashoutRatio * self.containingScenario.Rain * (self.DustLoad / self.DustDensity)
		self.ParticleVolumetricWetDepositionRate["Chem_Arsenic"]=self.Chemical_WashoutRatio * self.containingScenario.Rain * (self.DustLoad / self.DustDensity)
		self.ParticleVolumetricWetDepositionRate["Chem_Benz_a_anthracene"]=self.Chemical_WashoutRatio * self.containingScenario.Rain * (self.DustLoad / self.DustDensity)
		self.ParticleVolumetricWetDepositionRate["Chem_Benzo_A_Pyrene"]=self.Chemical_WashoutRatio * self.containingScenario.Rain * (self.DustLoad / self.DustDensity)
		self.ParticleVolumetricWetDepositionRate["Chem_Benzo_b_fluoranthene"]=self.Chemical_WashoutRatio * self.containingScenario.Rain * (self.DustLoad / self.DustDensity)
		self.ParticleVolumetricWetDepositionRate["Chem_Benzo_g_h_i_perylene"]=self.Chemical_WashoutRatio * self.containingScenario.Rain * (self.DustLoad / self.DustDensity)
		self.ParticleVolumetricWetDepositionRate["Chem_Benzo_k_fluoranthene"]=self.Chemical_WashoutRatio * self.containingScenario.Rain * (self.DustLoad / self.DustDensity)
		self.ParticleVolumetricWetDepositionRate["Chem_Cadmium"]=self.Chemical_WashoutRatio * self.containingScenario.Rain * (self.DustLoad / self.DustDensity)
		self.ParticleVolumetricWetDepositionRate["Chem_Chrysene"]=self.Chemical_WashoutRatio * self.containingScenario.Rain * (self.DustLoad / self.DustDensity)
		self.ParticleVolumetricWetDepositionRate["Chem_Dibenz_a_h_anthracene"]=self.Chemical_WashoutRatio * self.containingScenario.Rain * (self.DustLoad / self.DustDensity)
		self.ParticleVolumetricWetDepositionRate["Chem_Divalent_Mercury"]=self.Chemical_WashoutRatio * self.containingScenario.Rain * (self.DustLoad / self.DustDensity)
		self.ParticleVolumetricWetDepositionRate["Chem_Elemental_Mercury"]=self.Chemical_WashoutRatio * self.containingScenario.Rain * (self.DustLoad / self.DustDensity)
		self.ParticleVolumetricWetDepositionRate["Chem_Fluoranthene"]=self.Chemical_WashoutRatio * self.containingScenario.Rain * (self.DustLoad / self.DustDensity)
		self.ParticleVolumetricWetDepositionRate["Chem_Fluorene"]=self.Chemical_WashoutRatio * self.containingScenario.Rain * (self.DustLoad / self.DustDensity)
		self.ParticleVolumetricWetDepositionRate["Chem_Indeno_1_2_3_cd_pyrene"]=self.Chemical_WashoutRatio * self.containingScenario.Rain * (self.DustLoad / self.DustDensity)
		self.ParticleVolumetricWetDepositionRate["Chem_Lead"]=self.Chemical_WashoutRatio * self.containingScenario.Rain * (self.DustLoad / self.DustDensity)
		self.ParticleVolumetricWetDepositionRate["Chem_MethylMercury"]=self.Chemical_WashoutRatio * self.containingScenario.Rain * (self.DustLoad / self.DustDensity)
		try:
			self.Chemical_ParticleVolumetricWetDepositionRate=self.ParticleVolumetricWetDepositionRate[self.currentChemical.Name]
		except:
			self.Chemical_ParticleVolumetricWetDepositionRate=nan

		self.VolumetricAirAirContent=()
		self.VolumetricAirAirContent=1 - self.DustLoad / self.DustDensity

		self.VolumetricAirParticleContent=()
		self.VolumetricAirParticleContent=self.DustLoad / self.DustDensity

		self.Z_Liquid={}
		self.Z_Liquid["Chem_1_2_3_4_6_7_8_9_OCDD"]=self.currentChemical.Z_purewater
		self.Z_Liquid["Chem_1_2_3_4_6_7_8_9_OCDF"]=self.currentChemical.Z_purewater
		self.Z_Liquid["Chem_1_2_3_4_6_7_8_HpCDD"]=self.currentChemical.Z_purewater
		self.Z_Liquid["Chem_1_2_3_4_6_7_8_HpCDF"]=self.currentChemical.Z_purewater
		self.Z_Liquid["Chem_1_2_3_4_7_8_9_HpCDF"]=self.currentChemical.Z_purewater
		self.Z_Liquid["Chem_1_2_3_4_7_8_HxCDD"]=self.currentChemical.Z_purewater
		self.Z_Liquid["Chem_1_2_3_4_7_8_HxCDF"]=self.currentChemical.Z_purewater
		self.Z_Liquid["Chem_1_2_3_6_7_8_HxCDD"]=self.currentChemical.Z_purewater
		self.Z_Liquid["Chem_1_2_3_6_7_8_HxCDF"]=self.currentChemical.Z_purewater
		self.Z_Liquid["Chem_1_2_3_7_8_9_HxCDD"]=self.currentChemical.Z_purewater
		self.Z_Liquid["Chem_1_2_3_7_8_9_HxCDF"]=self.currentChemical.Z_purewater
		self.Z_Liquid["Chem_1_2_3_7_8_PeCDD"]=self.currentChemical.Z_purewater
		self.Z_Liquid["Chem_1_2_3_7_8_PeCDF"]=self.currentChemical.Z_purewater
		self.Z_Liquid["Chem_2_3_4_6_7_8_HxCDF"]=self.currentChemical.Z_purewater
		self.Z_Liquid["Chem_2_3_4_7_8_PeCDF"]=self.currentChemical.Z_purewater
		self.Z_Liquid["Chem_2_3_7_8_TCDD"]=self.currentChemical.Z_purewater
		self.Z_Liquid["Chem_2_3_7_8_TCDF"]=self.currentChemical.Z_purewater
		self.Z_Liquid["Chem_2_Methylnaphthalene"]=self.currentChemical.Z_purewater
		self.Z_Liquid["Chem_7_12_Dimethylbenz_a_anthracene"]=self.currentChemical.Z_purewater
		self.Z_Liquid["Chem_Acenaphthene"]=self.currentChemical.Z_purewater
		self.Z_Liquid["Chem_Acenaphthylene"]=self.currentChemical.Z_purewater
		self.Z_Liquid["Chem_Benz_a_anthracene"]=self.currentChemical.Z_purewater
		self.Z_Liquid["Chem_Benzo_A_Pyrene"]=self.currentChemical.Z_purewater
		self.Z_Liquid["Chem_Benzo_b_fluoranthene"]=self.currentChemical.Z_purewater
		self.Z_Liquid["Chem_Benzo_g_h_i_perylene"]=self.currentChemical.Z_purewater
		self.Z_Liquid["Chem_Benzo_k_fluoranthene"]=self.currentChemical.Z_purewater
		self.Z_Liquid["Chem_Chrysene"]=self.currentChemical.Z_purewater
		self.Z_Liquid["Chem_Dibenz_a_h_anthracene"]=self.currentChemical.Z_purewater
		self.Z_Liquid["Chem_Divalent_Mercury"]=self.currentChemical.Z_purewater
		self.Z_Liquid["Chem_Elemental_Mercury"]=self.currentChemical.Z_purewater
		self.Z_Liquid["Chem_Fluoranthene"]=self.currentChemical.Z_purewater
		self.Z_Liquid["Chem_Fluorene"]=self.currentChemical.Z_purewater
		self.Z_Liquid["Chem_Indeno_1_2_3_cd_pyrene"]=self.currentChemical.Z_purewater
		self.Z_Liquid["Chem_MethylMercury"]=self.currentChemical.Z_purewater
		try:
			self.Chemical_Z_Liquid=self.Z_Liquid[self.currentChemical.Name]
		except:
			self.Chemical_Z_Liquid=nan

		self.Z_Vapor={}
		self.Z_Vapor["Chem_1_2_3_4_6_7_8_9_OCDD"]=self.currentChemical.Z_pureair
		self.Z_Vapor["Chem_1_2_3_4_6_7_8_9_OCDF"]=self.currentChemical.Z_pureair
		self.Z_Vapor["Chem_1_2_3_4_6_7_8_HpCDD"]=self.currentChemical.Z_pureair
		self.Z_Vapor["Chem_1_2_3_4_6_7_8_HpCDF"]=self.currentChemical.Z_pureair
		self.Z_Vapor["Chem_1_2_3_4_7_8_9_HpCDF"]=self.currentChemical.Z_pureair
		self.Z_Vapor["Chem_1_2_3_4_7_8_HxCDD"]=self.currentChemical.Z_pureair
		self.Z_Vapor["Chem_1_2_3_4_7_8_HxCDF"]=self.currentChemical.Z_pureair
		self.Z_Vapor["Chem_1_2_3_6_7_8_HxCDD"]=self.currentChemical.Z_pureair
		self.Z_Vapor["Chem_1_2_3_6_7_8_HxCDF"]=self.currentChemical.Z_pureair
		self.Z_Vapor["Chem_1_2_3_7_8_9_HxCDD"]=self.currentChemical.Z_pureair
		self.Z_Vapor["Chem_1_2_3_7_8_9_HxCDF"]=self.currentChemical.Z_pureair
		self.Z_Vapor["Chem_1_2_3_7_8_PeCDD"]=self.currentChemical.Z_pureair
		self.Z_Vapor["Chem_1_2_3_7_8_PeCDF"]=self.currentChemical.Z_pureair
		self.Z_Vapor["Chem_2_3_4_6_7_8_HxCDF"]=self.currentChemical.Z_pureair
		self.Z_Vapor["Chem_2_3_4_7_8_PeCDF"]=self.currentChemical.Z_pureair
		self.Z_Vapor["Chem_2_3_7_8_TCDD"]=self.currentChemical.Z_pureair
		self.Z_Vapor["Chem_2_3_7_8_TCDF"]=self.currentChemical.Z_pureair
		self.Z_Vapor["Chem_2_Methylnaphthalene"]=self.currentChemical.Z_pureair
		self.Z_Vapor["Chem_7_12_Dimethylbenz_a_anthracene"]=self.currentChemical.Z_pureair
		self.Z_Vapor["Chem_Acenaphthene"]=self.currentChemical.Z_pureair
		self.Z_Vapor["Chem_Acenaphthylene"]=self.currentChemical.Z_pureair
		self.Z_Vapor["Chem_Benz_a_anthracene"]=self.currentChemical.Z_pureair
		self.Z_Vapor["Chem_Benzo_A_Pyrene"]=self.currentChemical.Z_pureair
		self.Z_Vapor["Chem_Benzo_b_fluoranthene"]=self.currentChemical.Z_pureair
		self.Z_Vapor["Chem_Benzo_g_h_i_perylene"]=self.currentChemical.Z_pureair
		self.Z_Vapor["Chem_Benzo_k_fluoranthene"]=self.currentChemical.Z_pureair
		self.Z_Vapor["Chem_Chrysene"]=self.currentChemical.Z_pureair
		self.Z_Vapor["Chem_Dibenz_a_h_anthracene"]=self.currentChemical.Z_pureair
		self.Z_Vapor["Chem_Divalent_Mercury"]=self.currentChemical.Z_pureair
		self.Z_Vapor["Chem_Elemental_Mercury"]=self.currentChemical.Z_pureair
		self.Z_Vapor["Chem_Fluoranthene"]=self.currentChemical.Z_pureair
		self.Z_Vapor["Chem_Fluorene"]=self.currentChemical.Z_pureair
		self.Z_Vapor["Chem_Indeno_1_2_3_cd_pyrene"]=self.currentChemical.Z_pureair
		self.Z_Vapor["Chem_MethylMercury"]=self.currentChemical.Z_pureair
		try:
			self.Chemical_Z_Vapor=self.Z_Vapor[self.currentChemical.Name]
		except:
			self.Chemical_Z_Vapor=nan

		self.DynamicAirViscosity_cm2_per_sec=()
		self.DynamicAirViscosity_cm2_per_sec=(1.32 + 0.009 * self.AirTemperature_C)/10.0

		self.FractionMass_Sorbed={}
		self.FractionMass_Sorbed["Chem_1_2_3_4_6_7_8_9_OCDD"]=1 - 1/(1+self.Chemical_ParticleGasPartitionCoefficient * self.DustLoad* self.Constants.ug_per_kg)
		self.FractionMass_Sorbed["Chem_1_2_3_4_6_7_8_9_OCDF"]=1 - 1/(1+self.Chemical_ParticleGasPartitionCoefficient * self.DustLoad* self.Constants.ug_per_kg)
		self.FractionMass_Sorbed["Chem_1_2_3_4_6_7_8_HpCDD"]=1 - 1/(1+self.Chemical_ParticleGasPartitionCoefficient * self.DustLoad* self.Constants.ug_per_kg)
		self.FractionMass_Sorbed["Chem_1_2_3_4_6_7_8_HpCDF"]=1 - 1/(1+self.Chemical_ParticleGasPartitionCoefficient * self.DustLoad* self.Constants.ug_per_kg)
		self.FractionMass_Sorbed["Chem_1_2_3_4_7_8_9_HpCDF"]=1 - 1/(1+self.Chemical_ParticleGasPartitionCoefficient * self.DustLoad* self.Constants.ug_per_kg)
		self.FractionMass_Sorbed["Chem_1_2_3_4_7_8_HxCDD"]=1 - 1/(1+self.Chemical_ParticleGasPartitionCoefficient * self.DustLoad* self.Constants.ug_per_kg)
		self.FractionMass_Sorbed["Chem_1_2_3_4_7_8_HxCDF"]=1 - 1/(1+self.Chemical_ParticleGasPartitionCoefficient * self.DustLoad* self.Constants.ug_per_kg)
		self.FractionMass_Sorbed["Chem_1_2_3_6_7_8_HxCDD"]=1 - 1/(1+self.Chemical_ParticleGasPartitionCoefficient * self.DustLoad* self.Constants.ug_per_kg)
		self.FractionMass_Sorbed["Chem_1_2_3_6_7_8_HxCDF"]=1 - 1/(1+self.Chemical_ParticleGasPartitionCoefficient * self.DustLoad* self.Constants.ug_per_kg)
		self.FractionMass_Sorbed["Chem_1_2_3_7_8_9_HxCDD"]=1 - 1/(1+self.Chemical_ParticleGasPartitionCoefficient * self.DustLoad* self.Constants.ug_per_kg)
		self.FractionMass_Sorbed["Chem_1_2_3_7_8_9_HxCDF"]=1 - 1/(1+self.Chemical_ParticleGasPartitionCoefficient * self.DustLoad* self.Constants.ug_per_kg)
		self.FractionMass_Sorbed["Chem_1_2_3_7_8_PeCDD"]=1 - 1/(1+self.Chemical_ParticleGasPartitionCoefficient * self.DustLoad* self.Constants.ug_per_kg)
		self.FractionMass_Sorbed["Chem_1_2_3_7_8_PeCDF"]=1 - 1/(1+self.Chemical_ParticleGasPartitionCoefficient * self.DustLoad* self.Constants.ug_per_kg)
		self.FractionMass_Sorbed["Chem_2_3_4_6_7_8_HxCDF"]=1 - 1/(1+self.Chemical_ParticleGasPartitionCoefficient * self.DustLoad* self.Constants.ug_per_kg)
		self.FractionMass_Sorbed["Chem_2_3_4_7_8_PeCDF"]=1 - 1/(1+self.Chemical_ParticleGasPartitionCoefficient * self.DustLoad* self.Constants.ug_per_kg)
		self.FractionMass_Sorbed["Chem_2_3_7_8_TCDD"]=1 - 1/(1+self.Chemical_ParticleGasPartitionCoefficient * self.DustLoad* self.Constants.ug_per_kg)
		self.FractionMass_Sorbed["Chem_2_3_7_8_TCDF"]=1 - 1/(1+self.Chemical_ParticleGasPartitionCoefficient * self.DustLoad* self.Constants.ug_per_kg)
		self.FractionMass_Sorbed["Chem_2_Methylnaphthalene"]=1 - 1/(1+self.Chemical_ParticleGasPartitionCoefficient * self.DustLoad* self.Constants.ug_per_kg)
		self.FractionMass_Sorbed["Chem_7_12_Dimethylbenz_a_anthracene"]=1 - 1/(1+self.Chemical_ParticleGasPartitionCoefficient * self.DustLoad* self.Constants.ug_per_kg)
		self.FractionMass_Sorbed["Chem_Acenaphthene"]=1 - 1/(1+self.Chemical_ParticleGasPartitionCoefficient * self.DustLoad* self.Constants.ug_per_kg)
		self.FractionMass_Sorbed["Chem_Acenaphthylene"]=1 - 1/(1+self.Chemical_ParticleGasPartitionCoefficient * self.DustLoad* self.Constants.ug_per_kg)
		self.FractionMass_Sorbed["Chem_Arsenic"]=0.999999
		self.FractionMass_Sorbed["Chem_Benz_a_anthracene"]=1 - 1/(1+self.Chemical_ParticleGasPartitionCoefficient * self.DustLoad* self.Constants.ug_per_kg)
		self.FractionMass_Sorbed["Chem_Benzo_A_Pyrene"]=1 - 1/(1+self.Chemical_ParticleGasPartitionCoefficient * self.DustLoad* self.Constants.ug_per_kg)
		self.FractionMass_Sorbed["Chem_Benzo_b_fluoranthene"]=1 - 1/(1+self.Chemical_ParticleGasPartitionCoefficient * self.DustLoad* self.Constants.ug_per_kg)
		self.FractionMass_Sorbed["Chem_Benzo_g_h_i_perylene"]=1 - 1/(1+self.Chemical_ParticleGasPartitionCoefficient * self.DustLoad* self.Constants.ug_per_kg)
		self.FractionMass_Sorbed["Chem_Benzo_k_fluoranthene"]=1 - 1/(1+self.Chemical_ParticleGasPartitionCoefficient * self.DustLoad* self.Constants.ug_per_kg)
		self.FractionMass_Sorbed["Chem_Cadmium"]=0.999999
		self.FractionMass_Sorbed["Chem_Chrysene"]=1 - 1/(1+self.Chemical_ParticleGasPartitionCoefficient * self.DustLoad* self.Constants.ug_per_kg)
		self.FractionMass_Sorbed["Chem_Dibenz_a_h_anthracene"]=1 - 1/(1+self.Chemical_ParticleGasPartitionCoefficient * self.DustLoad* self.Constants.ug_per_kg)
		self.FractionMass_Sorbed["Chem_Divalent_Mercury"]=1 - 1/(1+self.Chemical_ParticleGasPartitionCoefficient * self.DustLoad* self.Constants.ug_per_kg)
		self.FractionMass_Sorbed["Chem_Elemental_Mercury"]=1 - 1/(1+self.Chemical_ParticleGasPartitionCoefficient * self.DustLoad* self.Constants.ug_per_kg)
		self.FractionMass_Sorbed["Chem_Fluoranthene"]=1 - 1/(1+self.Chemical_ParticleGasPartitionCoefficient * self.DustLoad* self.Constants.ug_per_kg)
		self.FractionMass_Sorbed["Chem_Fluorene"]=1 - 1/(1+self.Chemical_ParticleGasPartitionCoefficient * self.DustLoad* self.Constants.ug_per_kg)
		self.FractionMass_Sorbed["Chem_Indeno_1_2_3_cd_pyrene"]=1 - 1/(1+self.Chemical_ParticleGasPartitionCoefficient * self.DustLoad* self.Constants.ug_per_kg)
		self.FractionMass_Sorbed["Chem_Lead"]=1 - 1/(1+self.Chemical_ParticleGasPartitionCoefficient * self.DustLoad* self.Constants.ug_per_kg)
		self.FractionMass_Sorbed["Chem_MethylMercury"]=1 - 1/(1+self.Chemical_ParticleGasPartitionCoefficient * self.DustLoad* self.Constants.ug_per_kg)
		try:
			self.Chemical_FractionMass_Sorbed=self.FractionMass_Sorbed[self.currentChemical.Name]
		except:
			self.Chemical_FractionMass_Sorbed=nan

		self.VolumeFraction_Liquid={}
		try:
			self.Chemical_VolumeFraction_Liquid=self.VolumeFraction_Liquid[self.currentChemical.Name]
		except:
			self.Chemical_VolumeFraction_Liquid=nan

		self.VolumeFraction_Solid=()
		self.VolumeFraction_Solid=self.VolumetricAirParticleContent

		self.GenericDenominatorforCalculatingFractioninPhases={}
		self.GenericDenominatorforCalculatingFractioninPhases["Chem_Indeno_1_2_3_cd_pyrene"]=log(2)/ self.Chemical_HalfLife
		try:
			self.Chemical_GenericDenominatorforCalculatingFractioninPhases=self.GenericDenominatorforCalculatingFractioninPhases[self.currentChemical.Name]
		except:
			self.Chemical_GenericDenominatorforCalculatingFractioninPhases=nan

		self.DynamicAirViscosity_m2_per_sec=()
		self.DynamicAirViscosity_m2_per_sec=self.DynamicAirViscosity_cm2_per_sec/1e4

		self.FractionMass_vapor={}
		self.FractionMass_vapor["Chem_1_2_3_4_6_7_8_9_OCDD"]=1 -self.Chemical_FractionMass_Sorbed
		self.FractionMass_vapor["Chem_1_2_3_4_6_7_8_9_OCDF"]=1 -self.Chemical_FractionMass_Sorbed
		self.FractionMass_vapor["Chem_1_2_3_4_6_7_8_HpCDD"]=1 -self.Chemical_FractionMass_Sorbed
		self.FractionMass_vapor["Chem_1_2_3_4_6_7_8_HpCDF"]=1 -self.Chemical_FractionMass_Sorbed
		self.FractionMass_vapor["Chem_1_2_3_4_7_8_9_HpCDF"]=1 -self.Chemical_FractionMass_Sorbed
		self.FractionMass_vapor["Chem_1_2_3_4_7_8_HxCDD"]=1 -self.Chemical_FractionMass_Sorbed
		self.FractionMass_vapor["Chem_1_2_3_4_7_8_HxCDF"]=1 -self.Chemical_FractionMass_Sorbed
		self.FractionMass_vapor["Chem_1_2_3_6_7_8_HxCDD"]=1 -self.Chemical_FractionMass_Sorbed
		self.FractionMass_vapor["Chem_1_2_3_6_7_8_HxCDF"]=1 -self.Chemical_FractionMass_Sorbed
		self.FractionMass_vapor["Chem_1_2_3_7_8_9_HxCDD"]=1 -self.Chemical_FractionMass_Sorbed
		self.FractionMass_vapor["Chem_1_2_3_7_8_9_HxCDF"]=1 -self.Chemical_FractionMass_Sorbed
		self.FractionMass_vapor["Chem_1_2_3_7_8_PeCDD"]=1 -self.Chemical_FractionMass_Sorbed
		self.FractionMass_vapor["Chem_1_2_3_7_8_PeCDF"]=1 -self.Chemical_FractionMass_Sorbed
		self.FractionMass_vapor["Chem_2_3_4_6_7_8_HxCDF"]=1 -self.Chemical_FractionMass_Sorbed
		self.FractionMass_vapor["Chem_2_3_4_7_8_PeCDF"]=1 -self.Chemical_FractionMass_Sorbed
		self.FractionMass_vapor["Chem_2_3_7_8_TCDD"]=1 -self.Chemical_FractionMass_Sorbed
		self.FractionMass_vapor["Chem_2_3_7_8_TCDF"]=1 -self.Chemical_FractionMass_Sorbed
		self.FractionMass_vapor["Chem_2_Methylnaphthalene"]=1 -self.Chemical_FractionMass_Sorbed
		self.FractionMass_vapor["Chem_7_12_Dimethylbenz_a_anthracene"]=1 -self.Chemical_FractionMass_Sorbed
		self.FractionMass_vapor["Chem_Acenaphthene"]=1 -self.Chemical_FractionMass_Sorbed
		self.FractionMass_vapor["Chem_Acenaphthylene"]=1 -self.Chemical_FractionMass_Sorbed
		self.FractionMass_vapor["Chem_Arsenic"]=1 -self.Chemical_FractionMass_Sorbed
		self.FractionMass_vapor["Chem_Benz_a_anthracene"]=1 -self.Chemical_FractionMass_Sorbed
		self.FractionMass_vapor["Chem_Benzo_A_Pyrene"]=1 -self.Chemical_FractionMass_Sorbed
		self.FractionMass_vapor["Chem_Benzo_b_fluoranthene"]=1 -self.Chemical_FractionMass_Sorbed
		self.FractionMass_vapor["Chem_Benzo_g_h_i_perylene"]=1 -self.Chemical_FractionMass_Sorbed
		self.FractionMass_vapor["Chem_Benzo_k_fluoranthene"]=1 -self.Chemical_FractionMass_Sorbed
		self.FractionMass_vapor["Chem_Cadmium"]=1 -self.Chemical_FractionMass_Sorbed
		self.FractionMass_vapor["Chem_Chrysene"]=1 -self.Chemical_FractionMass_Sorbed
		self.FractionMass_vapor["Chem_Dibenz_a_h_anthracene"]=1 -self.Chemical_FractionMass_Sorbed
		self.FractionMass_vapor["Chem_Divalent_Mercury"]=1 -self.Chemical_FractionMass_Sorbed
		self.FractionMass_vapor["Chem_Elemental_Mercury"]=1 -self.Chemical_FractionMass_Sorbed
		self.FractionMass_vapor["Chem_Fluoranthene"]=1 -self.Chemical_FractionMass_Sorbed
		self.FractionMass_vapor["Chem_Fluorene"]=1 -self.Chemical_FractionMass_Sorbed
		self.FractionMass_vapor["Chem_Indeno_1_2_3_cd_pyrene"]=1 -self.Chemical_FractionMass_Sorbed
		self.FractionMass_vapor["Chem_MethylMercury"]=1 -self.Chemical_FractionMass_Sorbed
		try:
			self.Chemical_FractionMass_vapor=self.FractionMass_vapor[self.currentChemical.Name]
		except:
			self.Chemical_FractionMass_vapor=nan

		self.AirSchmidtNumber={}
		self.AirSchmidtNumber["Chem_1_2_3_4_6_7_8_9_OCDD"]=self.DynamicAirViscosity_m2_per_sec/self.currentChemical.D_pureair_m2_s
		self.AirSchmidtNumber["Chem_1_2_3_4_6_7_8_9_OCDF"]=self.DynamicAirViscosity_m2_per_sec/self.currentChemical.D_pureair_m2_s
		self.AirSchmidtNumber["Chem_1_2_3_4_6_7_8_HpCDD"]=self.DynamicAirViscosity_m2_per_sec/self.currentChemical.D_pureair_m2_s
		self.AirSchmidtNumber["Chem_1_2_3_4_6_7_8_HpCDF"]=self.DynamicAirViscosity_m2_per_sec/self.currentChemical.D_pureair_m2_s
		self.AirSchmidtNumber["Chem_1_2_3_4_7_8_9_HpCDF"]=self.DynamicAirViscosity_m2_per_sec/self.currentChemical.D_pureair_m2_s
		self.AirSchmidtNumber["Chem_1_2_3_4_7_8_HxCDD"]=self.DynamicAirViscosity_m2_per_sec/self.currentChemical.D_pureair_m2_s
		self.AirSchmidtNumber["Chem_1_2_3_4_7_8_HxCDF"]=self.DynamicAirViscosity_m2_per_sec/self.currentChemical.D_pureair_m2_s
		self.AirSchmidtNumber["Chem_1_2_3_6_7_8_HxCDD"]=self.DynamicAirViscosity_m2_per_sec/self.currentChemical.D_pureair_m2_s
		self.AirSchmidtNumber["Chem_1_2_3_6_7_8_HxCDF"]=self.DynamicAirViscosity_m2_per_sec/self.currentChemical.D_pureair_m2_s
		self.AirSchmidtNumber["Chem_1_2_3_7_8_9_HxCDD"]=self.DynamicAirViscosity_m2_per_sec/self.currentChemical.D_pureair_m2_s
		self.AirSchmidtNumber["Chem_1_2_3_7_8_9_HxCDF"]=self.DynamicAirViscosity_m2_per_sec/self.currentChemical.D_pureair_m2_s
		self.AirSchmidtNumber["Chem_1_2_3_7_8_PeCDD"]=self.DynamicAirViscosity_m2_per_sec/self.currentChemical.D_pureair_m2_s
		self.AirSchmidtNumber["Chem_1_2_3_7_8_PeCDF"]=self.DynamicAirViscosity_m2_per_sec/self.currentChemical.D_pureair_m2_s
		self.AirSchmidtNumber["Chem_2_3_4_6_7_8_HxCDF"]=self.DynamicAirViscosity_m2_per_sec/self.currentChemical.D_pureair_m2_s
		self.AirSchmidtNumber["Chem_2_3_4_7_8_PeCDF"]=self.DynamicAirViscosity_m2_per_sec/self.currentChemical.D_pureair_m2_s
		self.AirSchmidtNumber["Chem_2_3_7_8_TCDD"]=self.DynamicAirViscosity_m2_per_sec/self.currentChemical.D_pureair_m2_s
		self.AirSchmidtNumber["Chem_2_3_7_8_TCDF"]=self.DynamicAirViscosity_m2_per_sec/self.currentChemical.D_pureair_m2_s
		self.AirSchmidtNumber["Chem_2_Methylnaphthalene"]=self.DynamicAirViscosity_m2_per_sec/self.currentChemical.D_pureair_m2_s
		self.AirSchmidtNumber["Chem_7_12_Dimethylbenz_a_anthracene"]=self.DynamicAirViscosity_m2_per_sec/self.currentChemical.D_pureair_m2_s
		self.AirSchmidtNumber["Chem_Acenaphthene"]=self.DynamicAirViscosity_m2_per_sec/self.currentChemical.D_pureair_m2_s
		self.AirSchmidtNumber["Chem_Acenaphthylene"]=self.DynamicAirViscosity_m2_per_sec/self.currentChemical.D_pureair_m2_s
		self.AirSchmidtNumber["Chem_Arsenic"]=self.DynamicAirViscosity_m2_per_sec/self.currentChemical.D_pureair_m2_s
		self.AirSchmidtNumber["Chem_Benz_a_anthracene"]=self.DynamicAirViscosity_m2_per_sec/self.currentChemical.D_pureair_m2_s
		self.AirSchmidtNumber["Chem_Benzo_A_Pyrene"]=self.DynamicAirViscosity_m2_per_sec/self.currentChemical.D_pureair_m2_s
		self.AirSchmidtNumber["Chem_Benzo_b_fluoranthene"]=self.DynamicAirViscosity_m2_per_sec/self.currentChemical.D_pureair_m2_s
		self.AirSchmidtNumber["Chem_Benzo_g_h_i_perylene"]=self.DynamicAirViscosity_m2_per_sec/self.currentChemical.D_pureair_m2_s
		self.AirSchmidtNumber["Chem_Benzo_k_fluoranthene"]=self.DynamicAirViscosity_m2_per_sec/self.currentChemical.D_pureair_m2_s
		self.AirSchmidtNumber["Chem_Cadmium"]=self.DynamicAirViscosity_m2_per_sec/self.currentChemical.D_pureair_m2_s
		self.AirSchmidtNumber["Chem_Chrysene"]=self.DynamicAirViscosity_m2_per_sec/self.currentChemical.D_pureair_m2_s
		self.AirSchmidtNumber["Chem_Dibenz_a_h_anthracene"]=self.DynamicAirViscosity_m2_per_sec/self.currentChemical.D_pureair_m2_s
		self.AirSchmidtNumber["Chem_Divalent_Mercury"]=self.DynamicAirViscosity_m2_per_sec/self.currentChemical.D_pureair_m2_s
		self.AirSchmidtNumber["Chem_Elemental_Mercury"]=self.DynamicAirViscosity_m2_per_sec/self.currentChemical.D_pureair_m2_s
		self.AirSchmidtNumber["Chem_Fluoranthene"]=self.DynamicAirViscosity_m2_per_sec/self.currentChemical.D_pureair_m2_s
		self.AirSchmidtNumber["Chem_Fluorene"]=self.DynamicAirViscosity_m2_per_sec/self.currentChemical.D_pureair_m2_s
		self.AirSchmidtNumber["Chem_Indeno_1_2_3_cd_pyrene"]=self.DynamicAirViscosity_m2_per_sec/self.currentChemical.D_pureair_m2_s
		self.AirSchmidtNumber["Chem_Lead"]=self.DynamicAirViscosity_m2_per_sec/self.currentChemical.D_pureair_m2_s
		self.AirSchmidtNumber["Chem_MethylMercury"]=self.DynamicAirViscosity_m2_per_sec/self.currentChemical.D_pureair_m2_s
		try:
			self.Chemical_AirSchmidtNumber=self.AirSchmidtNumber[self.currentChemical.Name]
		except:
			self.Chemical_AirSchmidtNumber=nan

		self.Area=()
		self.Area=containingVolumeElement.Area

		self.DustResuspensionRate={}
		self.DustResuspensionRate["Chem_1_2_3_4_6_7_8_9_OCDD"]=self.Chemical_ParticleVolumetricDRYDepositionRate
		self.DustResuspensionRate["Chem_1_2_3_4_6_7_8_9_OCDF"]=self.Chemical_ParticleVolumetricDRYDepositionRate
		self.DustResuspensionRate["Chem_1_2_3_4_6_7_8_HpCDD"]=self.Chemical_ParticleVolumetricDRYDepositionRate
		self.DustResuspensionRate["Chem_1_2_3_4_6_7_8_HpCDF"]=self.Chemical_ParticleVolumetricDRYDepositionRate
		self.DustResuspensionRate["Chem_1_2_3_4_7_8_9_HpCDF"]=self.Chemical_ParticleVolumetricDRYDepositionRate
		self.DustResuspensionRate["Chem_1_2_3_4_7_8_HxCDD"]=self.Chemical_ParticleVolumetricDRYDepositionRate
		self.DustResuspensionRate["Chem_1_2_3_4_7_8_HxCDF"]=self.Chemical_ParticleVolumetricDRYDepositionRate
		self.DustResuspensionRate["Chem_1_2_3_6_7_8_HxCDD"]=self.Chemical_ParticleVolumetricDRYDepositionRate
		self.DustResuspensionRate["Chem_1_2_3_6_7_8_HxCDF"]=self.Chemical_ParticleVolumetricDRYDepositionRate
		self.DustResuspensionRate["Chem_1_2_3_7_8_9_HxCDD"]=self.Chemical_ParticleVolumetricDRYDepositionRate
		self.DustResuspensionRate["Chem_1_2_3_7_8_9_HxCDF"]=self.Chemical_ParticleVolumetricDRYDepositionRate
		self.DustResuspensionRate["Chem_1_2_3_7_8_PeCDD"]=self.Chemical_ParticleVolumetricDRYDepositionRate
		self.DustResuspensionRate["Chem_1_2_3_7_8_PeCDF"]=self.Chemical_ParticleVolumetricDRYDepositionRate
		self.DustResuspensionRate["Chem_2_3_4_6_7_8_HxCDF"]=self.Chemical_ParticleVolumetricDRYDepositionRate
		self.DustResuspensionRate["Chem_2_3_4_7_8_PeCDF"]=self.Chemical_ParticleVolumetricDRYDepositionRate
		self.DustResuspensionRate["Chem_2_3_7_8_TCDD"]=self.Chemical_ParticleVolumetricDRYDepositionRate
		self.DustResuspensionRate["Chem_2_3_7_8_TCDF"]=self.Chemical_ParticleVolumetricDRYDepositionRate
		self.DustResuspensionRate["Chem_2_Methylnaphthalene"]=self.Chemical_ParticleVolumetricDRYDepositionRate
		self.DustResuspensionRate["Chem_7_12_Dimethylbenz_a_anthracene"]=self.Chemical_ParticleVolumetricDRYDepositionRate
		self.DustResuspensionRate["Chem_Acenaphthene"]=self.Chemical_ParticleVolumetricDRYDepositionRate
		self.DustResuspensionRate["Chem_Acenaphthylene"]=self.Chemical_ParticleVolumetricDRYDepositionRate
		self.DustResuspensionRate["Chem_Arsenic"]=self.Chemical_ParticleVolumetricDRYDepositionRate
		self.DustResuspensionRate["Chem_Benz_a_anthracene"]=self.Chemical_ParticleVolumetricDRYDepositionRate
		self.DustResuspensionRate["Chem_Benzo_A_Pyrene"]=self.Chemical_ParticleVolumetricDRYDepositionRate
		self.DustResuspensionRate["Chem_Benzo_b_fluoranthene"]=self.Chemical_ParticleVolumetricDRYDepositionRate
		self.DustResuspensionRate["Chem_Benzo_g_h_i_perylene"]=self.Chemical_ParticleVolumetricDRYDepositionRate
		self.DustResuspensionRate["Chem_Benzo_k_fluoranthene"]=self.Chemical_ParticleVolumetricDRYDepositionRate
		self.DustResuspensionRate["Chem_Cadmium"]=self.Chemical_ParticleVolumetricDRYDepositionRate
		self.DustResuspensionRate["Chem_Chrysene"]=self.Chemical_ParticleVolumetricDRYDepositionRate
		self.DustResuspensionRate["Chem_Dibenz_a_h_anthracene"]=self.Chemical_ParticleVolumetricDRYDepositionRate
		self.DustResuspensionRate["Chem_Divalent_Mercury"]=self.Chemical_ParticleVolumetricDRYDepositionRate
		self.DustResuspensionRate["Chem_Elemental_Mercury"]=self.Chemical_ParticleVolumetricDRYDepositionRate
		self.DustResuspensionRate["Chem_Fluoranthene"]=self.Chemical_ParticleVolumetricDRYDepositionRate
		self.DustResuspensionRate["Chem_Fluorene"]=self.Chemical_ParticleVolumetricDRYDepositionRate
		self.DustResuspensionRate["Chem_Indeno_1_2_3_cd_pyrene"]=self.Chemical_ParticleVolumetricDRYDepositionRate
		self.DustResuspensionRate["Chem_Lead"]=self.Chemical_ParticleVolumetricDRYDepositionRate
		self.DustResuspensionRate["Chem_MethylMercury"]=self.Chemical_ParticleVolumetricDRYDepositionRate
		try:
			self.Chemical_DustResuspensionRate=self.DustResuspensionRate[self.currentChemical.Name]
		except:
			self.Chemical_DustResuspensionRate=nan

		self.Height=()
		self.Height=containingVolumeElement.Height

		self.VaporWashoutRatio={}
		self.VaporWashoutRatio["Chem_Divalent_Mercury"]=self.currentChemical.VaporWashoutRatio
		self.VaporWashoutRatio["Chem_Elemental_Mercury"]=self.currentChemical.VaporWashoutRatio
		self.VaporWashoutRatio["Chem_MethylMercury"]=self.currentChemical.VaporWashoutRatio
		try:
			self.Chemical_VaporWashoutRatio=self.VaporWashoutRatio[self.currentChemical.Name]
		except:
			self.Chemical_VaporWashoutRatio=nan

		self.Volume=()
		self.Volume=containingVolumeElement.Volume

		self.VolumeFraction_Solid=()
		self.VolumeFraction_Solid=self.VolumetricAirParticleContent

		self.VolumeFraction_vapor=()
		self.VolumeFraction_vapor=self.VolumetricAirAirContent

		self.Z_Solid={}
		self.Z_Solid["Chem_1_2_3_4_6_7_8_9_OCDD"]=self.Chemical_Z_Vapor * (self.Chemical_FractionMass_Sorbed/self.VolumetricAirParticleContent)/(self.Chemical_FractionMass_vapor/self.VolumetricAirAirContent)
		self.Z_Solid["Chem_1_2_3_4_6_7_8_9_OCDF"]=self.Chemical_Z_Vapor * (self.Chemical_FractionMass_Sorbed/self.VolumetricAirParticleContent)/(self.Chemical_FractionMass_vapor/self.VolumetricAirAirContent)
		self.Z_Solid["Chem_1_2_3_4_6_7_8_HpCDD"]=self.Chemical_Z_Vapor * (self.Chemical_FractionMass_Sorbed/self.VolumetricAirParticleContent)/(self.Chemical_FractionMass_vapor/self.VolumetricAirAirContent)
		self.Z_Solid["Chem_1_2_3_4_6_7_8_HpCDF"]=self.Chemical_Z_Vapor * (self.Chemical_FractionMass_Sorbed/self.VolumetricAirParticleContent)/(self.Chemical_FractionMass_vapor/self.VolumetricAirAirContent)
		self.Z_Solid["Chem_1_2_3_4_7_8_9_HpCDF"]=self.Chemical_Z_Vapor * (self.Chemical_FractionMass_Sorbed/self.VolumetricAirParticleContent)/(self.Chemical_FractionMass_vapor/self.VolumetricAirAirContent)
		self.Z_Solid["Chem_1_2_3_4_7_8_HxCDD"]=self.Chemical_Z_Vapor * (self.Chemical_FractionMass_Sorbed/self.VolumetricAirParticleContent)/(self.Chemical_FractionMass_vapor/self.VolumetricAirAirContent)
		self.Z_Solid["Chem_1_2_3_4_7_8_HxCDF"]=self.Chemical_Z_Vapor * (self.Chemical_FractionMass_Sorbed/self.VolumetricAirParticleContent)/(self.Chemical_FractionMass_vapor/self.VolumetricAirAirContent)
		self.Z_Solid["Chem_1_2_3_6_7_8_HxCDD"]=self.Chemical_Z_Vapor * (self.Chemical_FractionMass_Sorbed/self.VolumetricAirParticleContent)/(self.Chemical_FractionMass_vapor/self.VolumetricAirAirContent)
		self.Z_Solid["Chem_1_2_3_6_7_8_HxCDF"]=self.Chemical_Z_Vapor * (self.Chemical_FractionMass_Sorbed/self.VolumetricAirParticleContent)/(self.Chemical_FractionMass_vapor/self.VolumetricAirAirContent)
		self.Z_Solid["Chem_1_2_3_7_8_9_HxCDD"]=self.Chemical_Z_Vapor * (self.Chemical_FractionMass_Sorbed/self.VolumetricAirParticleContent)/(self.Chemical_FractionMass_vapor/self.VolumetricAirAirContent)
		self.Z_Solid["Chem_1_2_3_7_8_9_HxCDF"]=self.Chemical_Z_Vapor * (self.Chemical_FractionMass_Sorbed/self.VolumetricAirParticleContent)/(self.Chemical_FractionMass_vapor/self.VolumetricAirAirContent)
		self.Z_Solid["Chem_1_2_3_7_8_PeCDD"]=self.Chemical_Z_Vapor * (self.Chemical_FractionMass_Sorbed/self.VolumetricAirParticleContent)/(self.Chemical_FractionMass_vapor/self.VolumetricAirAirContent)
		self.Z_Solid["Chem_1_2_3_7_8_PeCDF"]=self.Chemical_Z_Vapor * (self.Chemical_FractionMass_Sorbed/self.VolumetricAirParticleContent)/(self.Chemical_FractionMass_vapor/self.VolumetricAirAirContent)
		self.Z_Solid["Chem_2_3_4_6_7_8_HxCDF"]=self.Chemical_Z_Vapor * (self.Chemical_FractionMass_Sorbed/self.VolumetricAirParticleContent)/(self.Chemical_FractionMass_vapor/self.VolumetricAirAirContent)
		self.Z_Solid["Chem_2_3_4_7_8_PeCDF"]=self.Chemical_Z_Vapor * (self.Chemical_FractionMass_Sorbed/self.VolumetricAirParticleContent)/(self.Chemical_FractionMass_vapor/self.VolumetricAirAirContent)
		self.Z_Solid["Chem_2_3_7_8_TCDD"]=self.Chemical_Z_Vapor * (self.Chemical_FractionMass_Sorbed/self.VolumetricAirParticleContent)/(self.Chemical_FractionMass_vapor/self.VolumetricAirAirContent)
		self.Z_Solid["Chem_2_3_7_8_TCDF"]=self.Chemical_Z_Vapor * (self.Chemical_FractionMass_Sorbed/self.VolumetricAirParticleContent)/(self.Chemical_FractionMass_vapor/self.VolumetricAirAirContent)
		self.Z_Solid["Chem_2_Methylnaphthalene"]=self.Chemical_Z_Vapor * (self.Chemical_FractionMass_Sorbed/self.VolumetricAirParticleContent)/(self.Chemical_FractionMass_vapor/self.VolumetricAirAirContent)
		self.Z_Solid["Chem_7_12_Dimethylbenz_a_anthracene"]=self.Chemical_Z_Vapor * (self.Chemical_FractionMass_Sorbed/self.VolumetricAirParticleContent)/(self.Chemical_FractionMass_vapor/self.VolumetricAirAirContent)
		self.Z_Solid["Chem_Acenaphthene"]=self.Chemical_Z_Vapor * (self.Chemical_FractionMass_Sorbed/self.VolumetricAirParticleContent)/(self.Chemical_FractionMass_vapor/self.VolumetricAirAirContent)
		self.Z_Solid["Chem_Acenaphthylene"]=self.Chemical_Z_Vapor * (self.Chemical_FractionMass_Sorbed/self.VolumetricAirParticleContent)/(self.Chemical_FractionMass_vapor/self.VolumetricAirAirContent)
		self.Z_Solid["Chem_Benz_a_anthracene"]=self.Chemical_Z_Vapor * (self.Chemical_FractionMass_Sorbed/self.VolumetricAirParticleContent)/(self.Chemical_FractionMass_vapor/self.VolumetricAirAirContent)
		self.Z_Solid["Chem_Benzo_A_Pyrene"]=self.Chemical_Z_Vapor * (self.Chemical_FractionMass_Sorbed/self.VolumetricAirParticleContent)/(self.Chemical_FractionMass_vapor/self.VolumetricAirAirContent)
		self.Z_Solid["Chem_Benzo_b_fluoranthene"]=self.Chemical_Z_Vapor * (self.Chemical_FractionMass_Sorbed/self.VolumetricAirParticleContent)/(self.Chemical_FractionMass_vapor/self.VolumetricAirAirContent)
		self.Z_Solid["Chem_Benzo_g_h_i_perylene"]=self.Chemical_Z_Vapor * (self.Chemical_FractionMass_Sorbed/self.VolumetricAirParticleContent)/(self.Chemical_FractionMass_vapor/self.VolumetricAirAirContent)
		self.Z_Solid["Chem_Benzo_k_fluoranthene"]=self.Chemical_Z_Vapor * (self.Chemical_FractionMass_Sorbed/self.VolumetricAirParticleContent)/(self.Chemical_FractionMass_vapor/self.VolumetricAirAirContent)
		self.Z_Solid["Chem_Chrysene"]=self.Chemical_Z_Vapor * (self.Chemical_FractionMass_Sorbed/self.VolumetricAirParticleContent)/(self.Chemical_FractionMass_vapor/self.VolumetricAirAirContent)
		self.Z_Solid["Chem_Dibenz_a_h_anthracene"]=self.Chemical_Z_Vapor * (self.Chemical_FractionMass_Sorbed/self.VolumetricAirParticleContent)/(self.Chemical_FractionMass_vapor/self.VolumetricAirAirContent)
		self.Z_Solid["Chem_Divalent_Mercury"]=self.Chemical_Z_Vapor * (self.Chemical_FractionMass_Sorbed/self.VolumetricAirParticleContent)/(self.Chemical_FractionMass_vapor/self.VolumetricAirAirContent)
		self.Z_Solid["Chem_Elemental_Mercury"]=self.Chemical_Z_Vapor * (self.Chemical_FractionMass_Sorbed/self.VolumetricAirParticleContent)/(self.Chemical_FractionMass_vapor/self.VolumetricAirAirContent)
		self.Z_Solid["Chem_Fluoranthene"]=self.Chemical_Z_Vapor * (self.Chemical_FractionMass_Sorbed/self.VolumetricAirParticleContent)/(self.Chemical_FractionMass_vapor/self.VolumetricAirAirContent)
		self.Z_Solid["Chem_Fluorene"]=self.Chemical_Z_Vapor * (self.Chemical_FractionMass_Sorbed/self.VolumetricAirParticleContent)/(self.Chemical_FractionMass_vapor/self.VolumetricAirAirContent)
		self.Z_Solid["Chem_Indeno_1_2_3_cd_pyrene"]=self.Chemical_Z_Vapor * (self.Chemical_FractionMass_Sorbed/self.VolumetricAirParticleContent)/(self.Chemical_FractionMass_vapor/self.VolumetricAirAirContent)
		self.Z_Solid["Chem_MethylMercury"]=self.Chemical_Z_Vapor * (self.Chemical_FractionMass_Sorbed/self.VolumetricAirParticleContent)/(self.Chemical_FractionMass_vapor/self.VolumetricAirAirContent)
		try:
			self.Chemical_Z_Solid=self.Z_Solid[self.currentChemical.Name]
		except:
			self.Chemical_Z_Solid=nan

		self.Z_Total={}
		self.Z_Total["Chem_1_2_3_4_6_7_8_9_OCDD"]=self.Chemical_Z_Solid * (self.DustLoad /self.DustDensity) +self.Chemical_Z_Vapor * (1 - (self.DustLoad /self.DustDensity))
		self.Z_Total["Chem_1_2_3_4_6_7_8_9_OCDF"]=self.Chemical_Z_Solid * (self.DustLoad /self.DustDensity) +self.Chemical_Z_Vapor * (1 - (self.DustLoad /self.DustDensity))
		self.Z_Total["Chem_1_2_3_4_6_7_8_HpCDD"]=self.Chemical_Z_Solid * (self.DustLoad /self.DustDensity) +self.Chemical_Z_Vapor * (1 - (self.DustLoad /self.DustDensity))
		self.Z_Total["Chem_1_2_3_4_6_7_8_HpCDF"]=self.Chemical_Z_Solid * (self.DustLoad /self.DustDensity) +self.Chemical_Z_Vapor * (1 - (self.DustLoad /self.DustDensity))
		self.Z_Total["Chem_1_2_3_4_7_8_9_HpCDF"]=self.Chemical_Z_Solid * (self.DustLoad /self.DustDensity) +self.Chemical_Z_Vapor * (1 - (self.DustLoad /self.DustDensity))
		self.Z_Total["Chem_1_2_3_4_7_8_HxCDD"]=self.Chemical_Z_Solid * (self.DustLoad /self.DustDensity) +self.Chemical_Z_Vapor * (1 - (self.DustLoad /self.DustDensity))
		self.Z_Total["Chem_1_2_3_4_7_8_HxCDF"]=self.Chemical_Z_Solid * (self.DustLoad /self.DustDensity) +self.Chemical_Z_Vapor * (1 - (self.DustLoad /self.DustDensity))
		self.Z_Total["Chem_1_2_3_6_7_8_HxCDD"]=self.Chemical_Z_Solid * (self.DustLoad /self.DustDensity) +self.Chemical_Z_Vapor * (1 - (self.DustLoad /self.DustDensity))
		self.Z_Total["Chem_1_2_3_6_7_8_HxCDF"]=self.Chemical_Z_Solid * (self.DustLoad /self.DustDensity) +self.Chemical_Z_Vapor * (1 - (self.DustLoad /self.DustDensity))
		self.Z_Total["Chem_1_2_3_7_8_9_HxCDD"]=self.Chemical_Z_Solid * (self.DustLoad /self.DustDensity) +self.Chemical_Z_Vapor * (1 - (self.DustLoad /self.DustDensity))
		self.Z_Total["Chem_1_2_3_7_8_9_HxCDF"]=self.Chemical_Z_Solid * (self.DustLoad /self.DustDensity) +self.Chemical_Z_Vapor * (1 - (self.DustLoad /self.DustDensity))
		self.Z_Total["Chem_1_2_3_7_8_PeCDD"]=self.Chemical_Z_Solid * (self.DustLoad /self.DustDensity) +self.Chemical_Z_Vapor * (1 - (self.DustLoad /self.DustDensity))
		self.Z_Total["Chem_1_2_3_7_8_PeCDF"]=self.Chemical_Z_Solid * (self.DustLoad /self.DustDensity) +self.Chemical_Z_Vapor * (1 - (self.DustLoad /self.DustDensity))
		self.Z_Total["Chem_2_3_4_6_7_8_HxCDF"]=self.Chemical_Z_Solid * (self.DustLoad /self.DustDensity) +self.Chemical_Z_Vapor * (1 - (self.DustLoad /self.DustDensity))
		self.Z_Total["Chem_2_3_4_7_8_PeCDF"]=self.Chemical_Z_Solid * (self.DustLoad /self.DustDensity) +self.Chemical_Z_Vapor * (1 - (self.DustLoad /self.DustDensity))
		self.Z_Total["Chem_2_3_7_8_TCDD"]=self.Chemical_Z_Solid * (self.DustLoad /self.DustDensity) +self.Chemical_Z_Vapor * (1 - (self.DustLoad /self.DustDensity))
		self.Z_Total["Chem_2_3_7_8_TCDF"]=self.Chemical_Z_Solid * (self.DustLoad /self.DustDensity) +self.Chemical_Z_Vapor * (1 - (self.DustLoad /self.DustDensity))
		self.Z_Total["Chem_2_Methylnaphthalene"]=self.Chemical_Z_Solid * (self.DustLoad /self.DustDensity) +self.Chemical_Z_Vapor * (1 - (self.DustLoad /self.DustDensity))
		self.Z_Total["Chem_7_12_Dimethylbenz_a_anthracene"]=self.Chemical_Z_Solid * (self.DustLoad /self.DustDensity) +self.Chemical_Z_Vapor * (1 - (self.DustLoad /self.DustDensity))
		self.Z_Total["Chem_Acenaphthene"]=self.Chemical_Z_Solid * (self.DustLoad /self.DustDensity) +self.Chemical_Z_Vapor * (1 - (self.DustLoad /self.DustDensity))
		self.Z_Total["Chem_Acenaphthylene"]=self.Chemical_Z_Solid * (self.DustLoad /self.DustDensity) +self.Chemical_Z_Vapor * (1 - (self.DustLoad /self.DustDensity))
		self.Z_Total["Chem_Benz_a_anthracene"]=self.Chemical_Z_Solid * (self.DustLoad /self.DustDensity) +self.Chemical_Z_Vapor * (1 - (self.DustLoad /self.DustDensity))
		self.Z_Total["Chem_Benzo_A_Pyrene"]=self.Chemical_Z_Solid * (self.DustLoad /self.DustDensity) +self.Chemical_Z_Vapor * (1 - (self.DustLoad /self.DustDensity))
		self.Z_Total["Chem_Benzo_b_fluoranthene"]=self.Chemical_Z_Solid * (self.DustLoad /self.DustDensity) +self.Chemical_Z_Vapor * (1 - (self.DustLoad /self.DustDensity))
		self.Z_Total["Chem_Benzo_g_h_i_perylene"]=self.Chemical_Z_Solid * (self.DustLoad /self.DustDensity) +self.Chemical_Z_Vapor * (1 - (self.DustLoad /self.DustDensity))
		self.Z_Total["Chem_Benzo_k_fluoranthene"]=self.Chemical_Z_Solid * (self.DustLoad /self.DustDensity) +self.Chemical_Z_Vapor * (1 - (self.DustLoad /self.DustDensity))
		self.Z_Total["Chem_Chrysene"]=self.Chemical_Z_Solid * (self.DustLoad /self.DustDensity) +self.Chemical_Z_Vapor * (1 - (self.DustLoad /self.DustDensity))
		self.Z_Total["Chem_Dibenz_a_h_anthracene"]=self.Chemical_Z_Solid * (self.DustLoad /self.DustDensity) +self.Chemical_Z_Vapor * (1 - (self.DustLoad /self.DustDensity))
		self.Z_Total["Chem_Divalent_Mercury"]=self.Chemical_Z_Solid * (self.DustLoad /self.DustDensity) +self.Chemical_Z_Vapor * (1 - (self.DustLoad /self.DustDensity))
		self.Z_Total["Chem_Elemental_Mercury"]=self.Chemical_Z_Solid * (self.DustLoad /self.DustDensity) +self.Chemical_Z_Vapor * (1 - (self.DustLoad /self.DustDensity))
		self.Z_Total["Chem_Fluoranthene"]=self.Chemical_Z_Solid * (self.DustLoad /self.DustDensity) +self.Chemical_Z_Vapor * (1 - (self.DustLoad /self.DustDensity))
		self.Z_Total["Chem_Fluorene"]=self.Chemical_Z_Solid * (self.DustLoad /self.DustDensity) +self.Chemical_Z_Vapor * (1 - (self.DustLoad /self.DustDensity))
		self.Z_Total["Chem_Indeno_1_2_3_cd_pyrene"]=self.Chemical_Z_Solid * (self.DustLoad /self.DustDensity) +self.Chemical_Z_Vapor * (1 - (self.DustLoad /self.DustDensity))
		self.Z_Total["Chem_MethylMercury"]=self.Chemical_Z_Solid * (self.DustLoad /self.DustDensity) +self.Chemical_Z_Vapor * (1 - (self.DustLoad /self.DustDensity))
		try:
			self.Chemical_Z_Total=self.Z_Total[self.currentChemical.Name]
		except:
			self.Chemical_Z_Total=nan

		self.initialConcentration_g_per_m3={}
		self.initialConcentration_g_per_m3["Chem_1_2_3_4_6_7_8_9_OCDD"]=self.containingScenario.FractionInitialConcentrations * self.Chemical_initialConcentration_g_per_m3_UserSupplied
		self.initialConcentration_g_per_m3["Chem_1_2_3_4_6_7_8_9_OCDF"]=self.containingScenario.FractionInitialConcentrations * self.Chemical_initialConcentration_g_per_m3_UserSupplied
		self.initialConcentration_g_per_m3["Chem_1_2_3_4_6_7_8_HpCDD"]=self.containingScenario.FractionInitialConcentrations * self.Chemical_initialConcentration_g_per_m3_UserSupplied
		self.initialConcentration_g_per_m3["Chem_1_2_3_4_6_7_8_HpCDF"]=self.containingScenario.FractionInitialConcentrations * self.Chemical_initialConcentration_g_per_m3_UserSupplied
		self.initialConcentration_g_per_m3["Chem_1_2_3_4_7_8_9_HpCDF"]=self.containingScenario.FractionInitialConcentrations * self.Chemical_initialConcentration_g_per_m3_UserSupplied
		self.initialConcentration_g_per_m3["Chem_1_2_3_4_7_8_HxCDD"]=self.containingScenario.FractionInitialConcentrations * self.Chemical_initialConcentration_g_per_m3_UserSupplied
		self.initialConcentration_g_per_m3["Chem_1_2_3_4_7_8_HxCDF"]=self.containingScenario.FractionInitialConcentrations * self.Chemical_initialConcentration_g_per_m3_UserSupplied
		self.initialConcentration_g_per_m3["Chem_1_2_3_6_7_8_HxCDD"]=self.containingScenario.FractionInitialConcentrations * self.Chemical_initialConcentration_g_per_m3_UserSupplied
		self.initialConcentration_g_per_m3["Chem_1_2_3_6_7_8_HxCDF"]=self.containingScenario.FractionInitialConcentrations * self.Chemical_initialConcentration_g_per_m3_UserSupplied
		self.initialConcentration_g_per_m3["Chem_1_2_3_7_8_9_HxCDD"]=self.containingScenario.FractionInitialConcentrations * self.Chemical_initialConcentration_g_per_m3_UserSupplied
		self.initialConcentration_g_per_m3["Chem_1_2_3_7_8_9_HxCDF"]=self.containingScenario.FractionInitialConcentrations * self.Chemical_initialConcentration_g_per_m3_UserSupplied
		self.initialConcentration_g_per_m3["Chem_1_2_3_7_8_PeCDD"]=self.containingScenario.FractionInitialConcentrations * self.Chemical_initialConcentration_g_per_m3_UserSupplied
		self.initialConcentration_g_per_m3["Chem_1_2_3_7_8_PeCDF"]=self.containingScenario.FractionInitialConcentrations * self.Chemical_initialConcentration_g_per_m3_UserSupplied
		self.initialConcentration_g_per_m3["Chem_2_3_4_6_7_8_HxCDF"]=self.containingScenario.FractionInitialConcentrations * self.Chemical_initialConcentration_g_per_m3_UserSupplied
		self.initialConcentration_g_per_m3["Chem_2_3_4_7_8_PeCDF"]=self.containingScenario.FractionInitialConcentrations * self.Chemical_initialConcentration_g_per_m3_UserSupplied
		self.initialConcentration_g_per_m3["Chem_2_3_7_8_TCDD"]=self.containingScenario.FractionInitialConcentrations * self.Chemical_initialConcentration_g_per_m3_UserSupplied
		self.initialConcentration_g_per_m3["Chem_2_3_7_8_TCDF"]=self.containingScenario.FractionInitialConcentrations * self.Chemical_initialConcentration_g_per_m3_UserSupplied
		self.initialConcentration_g_per_m3["Chem_2_Methylnaphthalene"]=self.containingScenario.FractionInitialConcentrations * self.Chemical_initialConcentration_g_per_m3_UserSupplied
		self.initialConcentration_g_per_m3["Chem_7_12_Dimethylbenz_a_anthracene"]=self.containingScenario.FractionInitialConcentrations * self.Chemical_initialConcentration_g_per_m3_UserSupplied
		self.initialConcentration_g_per_m3["Chem_Acenaphthene"]=self.containingScenario.FractionInitialConcentrations * self.Chemical_initialConcentration_g_per_m3_UserSupplied
		self.initialConcentration_g_per_m3["Chem_Acenaphthylene"]=self.containingScenario.FractionInitialConcentrations * self.Chemical_initialConcentration_g_per_m3_UserSupplied
		self.initialConcentration_g_per_m3["Chem_Benz_a_anthracene"]=self.containingScenario.FractionInitialConcentrations * self.Chemical_initialConcentration_g_per_m3_UserSupplied
		self.initialConcentration_g_per_m3["Chem_Benzo_A_Pyrene"]=self.containingScenario.FractionInitialConcentrations * self.Chemical_initialConcentration_g_per_m3_UserSupplied
		self.initialConcentration_g_per_m3["Chem_Benzo_b_fluoranthene"]=self.containingScenario.FractionInitialConcentrations * self.Chemical_initialConcentration_g_per_m3_UserSupplied
		self.initialConcentration_g_per_m3["Chem_Benzo_g_h_i_perylene"]=self.containingScenario.FractionInitialConcentrations * self.Chemical_initialConcentration_g_per_m3_UserSupplied
		self.initialConcentration_g_per_m3["Chem_Benzo_k_fluoranthene"]=self.containingScenario.FractionInitialConcentrations * self.Chemical_initialConcentration_g_per_m3_UserSupplied
		self.initialConcentration_g_per_m3["Chem_Chrysene"]=self.containingScenario.FractionInitialConcentrations * self.Chemical_initialConcentration_g_per_m3_UserSupplied
		self.initialConcentration_g_per_m3["Chem_Dibenz_a_h_anthracene"]=self.containingScenario.FractionInitialConcentrations * self.Chemical_initialConcentration_g_per_m3_UserSupplied
		self.initialConcentration_g_per_m3["Chem_Divalent_Mercury"]=self.containingScenario.FractionInitialConcentrations * self.Chemical_initialConcentration_g_per_m3_UserSupplied
		self.initialConcentration_g_per_m3["Chem_Elemental_Mercury"]=self.containingScenario.FractionInitialConcentrations * self.Chemical_initialConcentration_g_per_m3_UserSupplied
		self.initialConcentration_g_per_m3["Chem_Fluoranthene"]=self.containingScenario.FractionInitialConcentrations * self.Chemical_initialConcentration_g_per_m3_UserSupplied
		self.initialConcentration_g_per_m3["Chem_Fluorene"]=self.containingScenario.FractionInitialConcentrations * self.Chemical_initialConcentration_g_per_m3_UserSupplied
		self.initialConcentration_g_per_m3["Chem_Indeno_1_2_3_cd_pyrene"]=self.containingScenario.FractionInitialConcentrations * self.Chemical_initialConcentration_g_per_m3_UserSupplied
		self.initialConcentration_g_per_m3["Chem_MethylMercury"]=self.containingScenario.FractionInitialConcentrations * self.Chemical_initialConcentration_g_per_m3_UserSupplied
		try:
			self.Chemical_initialConcentration_g_per_m3=self.initialConcentration_g_per_m3[self.currentChemical.Name]
		except:
			self.Chemical_initialConcentration_g_per_m3=nan

class Degradation_Reaction_Sink:
	def __init__(self,Constants,containingScenario,currentChemical,containingVolumeElement):
		self.containingScenario=containingScenario
		self.currentChemical=currentChemical
		self.Constants=Constants
		self.containingVolumeElement=containingVolumeElement
		
		self.acceptableAbiotic=()
		self.acceptableAbiotic='nan'

		self.category=()
		self.category='Sink | Degradation/Reaction Sink'

		self.concentrationOutputUnits=()
		self.concentrationOutputUnits='0.01'

		self.isBiotic=()
		self.isBiotic=False

		self.concentrationOutputFactor=()
		self.concentrationOutputFactor=1.0

		self.VolumeFraction_Liquid={}
		try:
			self.Chemical_VolumeFraction_Liquid=self.VolumeFraction_Liquid[self.currentChemical.Name]
		except:
			self.Chemical_VolumeFraction_Liquid=nan

		self.VolumeFraction_Solid={}
		try:
			self.Chemical_VolumeFraction_Solid=self.VolumeFraction_Solid[self.currentChemical.Name]
		except:
			self.Chemical_VolumeFraction_Solid=nan

		self.GenericDenominatorforCalculatingFractioninPhases={}
		try:
			self.Chemical_GenericDenominatorforCalculatingFractioninPhases=self.GenericDenominatorforCalculatingFractioninPhases[self.currentChemical.Name]
		except:
			self.Chemical_GenericDenominatorforCalculatingFractioninPhases=nan

class Flush_Rate_Sink:
	def __init__(self,Constants,containingScenario,currentChemical,containingVolumeElement):
		self.containingScenario=containingScenario
		self.currentChemical=currentChemical
		self.Constants=Constants
		self.containingVolumeElement=containingVolumeElement
		
		self.acceptableAbiotic=()
		self.acceptableAbiotic='Abiotic | Surface water | Surface water - Default'

		self.category=()
		self.category='Sink | Abiotic | Surface water | Surface water - Default'

		self.concentrationOutputUnits=()
		self.concentrationOutputUnits='0.01'

		self.isBiotic=()
		self.isBiotic=False

		self.concentrationOutputFactor=()
		self.concentrationOutputFactor=1.0

		self.VolumeFraction_Liquid={}
		try:
			self.Chemical_VolumeFraction_Liquid=self.VolumeFraction_Liquid[self.currentChemical.Name]
		except:
			self.Chemical_VolumeFraction_Liquid=nan

		self.VolumeFraction_Solid={}
		try:
			self.Chemical_VolumeFraction_Solid=self.VolumeFraction_Solid[self.currentChemical.Name]
		except:
			self.Chemical_VolumeFraction_Solid=nan

		self.GenericDenominatorforCalculatingFractioninPhases={}
		try:
			self.Chemical_GenericDenominatorforCalculatingFractioninPhases=self.GenericDenominatorforCalculatingFractioninPhases[self.currentChemical.Name]
		except:
			self.Chemical_GenericDenominatorforCalculatingFractioninPhases=nan

class Sediment:
	def __init__(self,Constants,containingScenario,currentChemical,containingVolumeElement):
		self.containingScenario=containingScenario
		self.currentChemical=currentChemical
		self.Constants=Constants
		self.containingVolumeElement=containingVolumeElement
		
		self.acceptableAbiotic=()
		self.acceptableAbiotic='nan'

		self.category=()
		self.category='Abiotic | Sediment | Sediment - Default'

		self.concentrationOutputUnits=()
		self.concentrationOutputUnits='ug/g dry weight'

		self.wetConcOutputUnits=()
		self.wetConcOutputUnits='ug/g wet weight'

		self.isBiotic=()
		self.isBiotic=False

		self.DemethylationRate={}
		self.DemethylationRate["Chem_MethylMercury"]=0.0501
		try:
			self.Chemical_DemethylationRate=self.DemethylationRate[self.currentChemical.Name]
		except:
			self.Chemical_DemethylationRate=nan

		self.FractionSand=()
		self.FractionSand=0.25

		self.HalfLife={}
		self.HalfLife["Chem_1_2_3_4_6_7_8_9_OCDD"]=1095.0
		self.HalfLife["Chem_1_2_3_4_6_7_8_9_OCDF"]=1095.0
		self.HalfLife["Chem_1_2_3_4_6_7_8_HpCDD"]=1095.0
		self.HalfLife["Chem_1_2_3_4_6_7_8_HpCDF"]=1095.0
		self.HalfLife["Chem_1_2_3_4_7_8_9_HpCDF"]=1095.0
		self.HalfLife["Chem_1_2_3_4_7_8_HxCDD"]=1095.0
		self.HalfLife["Chem_1_2_3_4_7_8_HxCDF"]=1095.0
		self.HalfLife["Chem_1_2_3_6_7_8_HxCDD"]=1095.0
		self.HalfLife["Chem_1_2_3_6_7_8_HxCDF"]=1095.0
		self.HalfLife["Chem_1_2_3_7_8_9_HxCDD"]=1095.0
		self.HalfLife["Chem_1_2_3_7_8_9_HxCDF"]=1095.0
		self.HalfLife["Chem_1_2_3_7_8_PeCDD"]=1095.0
		self.HalfLife["Chem_1_2_3_7_8_PeCDF"]=1095.0
		self.HalfLife["Chem_2_3_4_6_7_8_HxCDF"]=1095.0
		self.HalfLife["Chem_2_3_4_7_8_PeCDF"]=1095.0
		self.HalfLife["Chem_2_3_7_8_TCDD"]=1095.0
		self.HalfLife["Chem_2_3_7_8_TCDF"]=1095.0
		self.HalfLife["Chem_2_Methylnaphthalene"]=2290.0
		self.HalfLife["Chem_7_12_Dimethylbenz_a_anthracene"]=2290.0
		self.HalfLife["Chem_Acenaphthene"]=2290.0
		self.HalfLife["Chem_Acenaphthylene"]=2290.0
		self.HalfLife["Chem_Benz_a_anthracene"]=2290.0
		self.HalfLife["Chem_Benzo_A_Pyrene"]=2290.0
		self.HalfLife["Chem_Benzo_b_fluoranthene"]=2290.0
		self.HalfLife["Chem_Benzo_g_h_i_perylene"]=2290.0
		self.HalfLife["Chem_Benzo_k_fluoranthene"]=2290.0
		self.HalfLife["Chem_Chrysene"]=2290.0
		self.HalfLife["Chem_Dibenz_a_h_anthracene"]=2290.0
		self.HalfLife["Chem_Fluoranthene"]=2290.0
		self.HalfLife["Chem_Fluorene"]=2290.0
		self.HalfLife["Chem_Indeno_1_2_3_cd_pyrene"]=2290.0
		try:
			self.Chemical_HalfLife=self.HalfLife[self.currentChemical.Name]
		except:
			self.Chemical_HalfLife=nan

		self.MethylationRate={}
		self.MethylationRate["Chem_Divalent_Mercury"]=1.0E-4
		try:
			self.Chemical_MethylationRate=self.MethylationRate[self.currentChemical.Name]
		except:
			self.Chemical_MethylationRate=nan

		self.OrganicCarbonContent=()
		self.OrganicCarbonContent=0.01

		self.OxidationRate={}
		self.OxidationRate["Chem_Elemental_Mercury"]=0.0
		try:
			self.Chemical_OxidationRate=self.OxidationRate[self.currentChemical.Name]
		except:
			self.Chemical_OxidationRate=nan

		self.Porosity=()
		self.Porosity=0.6

		self.ReductionRate={}
		self.ReductionRate["Chem_Divalent_Mercury"]=1.0E-6
		try:
			self.Chemical_ReductionRate=self.ReductionRate[self.currentChemical.Name]
		except:
			self.Chemical_ReductionRate=nan

		self.SedimentResuspensionVelocity=()
		self.SedimentResuspensionVelocity=9.64763202734353e-05

		self.initialConcentration_g_per_m3_UserSupplied={}
		self.initialConcentration_g_per_m3_UserSupplied["Chem_1_2_3_4_6_7_8_9_OCDD"]=0.0
		self.initialConcentration_g_per_m3_UserSupplied["Chem_1_2_3_4_6_7_8_9_OCDF"]=0.0
		self.initialConcentration_g_per_m3_UserSupplied["Chem_1_2_3_4_6_7_8_HpCDD"]=0.0
		self.initialConcentration_g_per_m3_UserSupplied["Chem_1_2_3_4_6_7_8_HpCDF"]=0.0
		self.initialConcentration_g_per_m3_UserSupplied["Chem_1_2_3_4_7_8_9_HpCDF"]=0.0
		self.initialConcentration_g_per_m3_UserSupplied["Chem_1_2_3_4_7_8_HxCDD"]=0.0
		self.initialConcentration_g_per_m3_UserSupplied["Chem_1_2_3_4_7_8_HxCDF"]=0.0
		self.initialConcentration_g_per_m3_UserSupplied["Chem_1_2_3_6_7_8_HxCDD"]=0.0
		self.initialConcentration_g_per_m3_UserSupplied["Chem_1_2_3_6_7_8_HxCDF"]=0.0
		self.initialConcentration_g_per_m3_UserSupplied["Chem_1_2_3_7_8_9_HxCDD"]=0.0
		self.initialConcentration_g_per_m3_UserSupplied["Chem_1_2_3_7_8_9_HxCDF"]=0.0
		self.initialConcentration_g_per_m3_UserSupplied["Chem_1_2_3_7_8_PeCDD"]=0.0
		self.initialConcentration_g_per_m3_UserSupplied["Chem_1_2_3_7_8_PeCDF"]=0.0
		self.initialConcentration_g_per_m3_UserSupplied["Chem_2_3_4_6_7_8_HxCDF"]=0.0
		self.initialConcentration_g_per_m3_UserSupplied["Chem_2_3_4_7_8_PeCDF"]=0.0
		self.initialConcentration_g_per_m3_UserSupplied["Chem_2_3_7_8_TCDD"]=0.0
		self.initialConcentration_g_per_m3_UserSupplied["Chem_2_3_7_8_TCDF"]=0.0
		self.initialConcentration_g_per_m3_UserSupplied["Chem_2_Methylnaphthalene"]=0.0
		self.initialConcentration_g_per_m3_UserSupplied["Chem_7_12_Dimethylbenz_a_anthracene"]=0.0
		self.initialConcentration_g_per_m3_UserSupplied["Chem_Acenaphthene"]=0.0
		self.initialConcentration_g_per_m3_UserSupplied["Chem_Acenaphthylene"]=0.0
		self.initialConcentration_g_per_m3_UserSupplied["Chem_Arsenic"]=0.0
		self.initialConcentration_g_per_m3_UserSupplied["Chem_Benz_a_anthracene"]=0.0
		self.initialConcentration_g_per_m3_UserSupplied["Chem_Benzo_A_Pyrene"]=0.0
		self.initialConcentration_g_per_m3_UserSupplied["Chem_Benzo_b_fluoranthene"]=0.0
		self.initialConcentration_g_per_m3_UserSupplied["Chem_Benzo_g_h_i_perylene"]=0.0
		self.initialConcentration_g_per_m3_UserSupplied["Chem_Benzo_k_fluoranthene"]=0.0
		self.initialConcentration_g_per_m3_UserSupplied["Chem_Cadmium"]=0.0
		self.initialConcentration_g_per_m3_UserSupplied["Chem_Chrysene"]=0.0
		self.initialConcentration_g_per_m3_UserSupplied["Chem_Dibenz_a_h_anthracene"]=0.0
		self.initialConcentration_g_per_m3_UserSupplied["Chem_Divalent_Mercury"]=0.0
		self.initialConcentration_g_per_m3_UserSupplied["Chem_Elemental_Mercury"]=0.0
		self.initialConcentration_g_per_m3_UserSupplied["Chem_Fluoranthene"]=0.0
		self.initialConcentration_g_per_m3_UserSupplied["Chem_Fluorene"]=0.0
		self.initialConcentration_g_per_m3_UserSupplied["Chem_Indeno_1_2_3_cd_pyrene"]=0.0
		self.initialConcentration_g_per_m3_UserSupplied["Chem_MethylMercury"]=0.0
		try:
			self.Chemical_initialConcentration_g_per_m3_UserSupplied=self.initialConcentration_g_per_m3_UserSupplied[self.currentChemical.Name]
		except:
			self.Chemical_initialConcentration_g_per_m3_UserSupplied=nan

		self.pH=()
		self.pH=0.01

		self.rho=()
		self.rho=2600.0

		self.Benthic_Solids_Concentration=()
		self.Benthic_Solids_Concentration=self.rho * (1 - self.Porosity)

		self.D_effective={}
		self.D_effective["Chem_1_2_3_4_6_7_8_9_OCDD"]=self.Porosity ** (4 / 3) * self.currentChemical.D_purewater
		self.D_effective["Chem_1_2_3_4_6_7_8_9_OCDF"]=self.Porosity ** (4 / 3) * self.currentChemical.D_purewater
		self.D_effective["Chem_1_2_3_4_6_7_8_HpCDD"]=self.Porosity ** (4 / 3) * self.currentChemical.D_purewater
		self.D_effective["Chem_1_2_3_4_6_7_8_HpCDF"]=self.Porosity ** (4 / 3) * self.currentChemical.D_purewater
		self.D_effective["Chem_1_2_3_4_7_8_9_HpCDF"]=self.Porosity ** (4 / 3) * self.currentChemical.D_purewater
		self.D_effective["Chem_1_2_3_4_7_8_HxCDD"]=self.Porosity ** (4 / 3) * self.currentChemical.D_purewater
		self.D_effective["Chem_1_2_3_4_7_8_HxCDF"]=self.Porosity ** (4 / 3) * self.currentChemical.D_purewater
		self.D_effective["Chem_1_2_3_6_7_8_HxCDD"]=self.Porosity ** (4 / 3) * self.currentChemical.D_purewater
		self.D_effective["Chem_1_2_3_6_7_8_HxCDF"]=self.Porosity ** (4 / 3) * self.currentChemical.D_purewater
		self.D_effective["Chem_1_2_3_7_8_9_HxCDD"]=self.Porosity ** (4 / 3) * self.currentChemical.D_purewater
		self.D_effective["Chem_1_2_3_7_8_9_HxCDF"]=self.Porosity ** (4 / 3) * self.currentChemical.D_purewater
		self.D_effective["Chem_1_2_3_7_8_PeCDD"]=self.Porosity ** (4 / 3) * self.currentChemical.D_purewater
		self.D_effective["Chem_1_2_3_7_8_PeCDF"]=self.Porosity ** (4 / 3) * self.currentChemical.D_purewater
		self.D_effective["Chem_2_3_4_6_7_8_HxCDF"]=self.Porosity ** (4 / 3) * self.currentChemical.D_purewater
		self.D_effective["Chem_2_3_4_7_8_PeCDF"]=self.Porosity ** (4 / 3) * self.currentChemical.D_purewater
		self.D_effective["Chem_2_3_7_8_TCDD"]=self.Porosity ** (4 / 3) * self.currentChemical.D_purewater
		self.D_effective["Chem_2_3_7_8_TCDF"]=self.Porosity ** (4 / 3) * self.currentChemical.D_purewater
		self.D_effective["Chem_2_Methylnaphthalene"]=self.Porosity ** (4 / 3) * self.currentChemical.D_purewater
		self.D_effective["Chem_7_12_Dimethylbenz_a_anthracene"]=self.Porosity ** (4 / 3) * self.currentChemical.D_purewater
		self.D_effective["Chem_Acenaphthene"]=self.Porosity ** (4 / 3) * self.currentChemical.D_purewater
		self.D_effective["Chem_Acenaphthylene"]=self.Porosity ** (4 / 3) * self.currentChemical.D_purewater
		self.D_effective["Chem_Arsenic"]=self.Porosity ** (4 / 3) * self.currentChemical.D_purewater
		self.D_effective["Chem_Benz_a_anthracene"]=self.Porosity ** (4 / 3) * self.currentChemical.D_purewater
		self.D_effective["Chem_Benzo_A_Pyrene"]=self.Porosity ** (4 / 3) * self.currentChemical.D_purewater
		self.D_effective["Chem_Benzo_b_fluoranthene"]=self.Porosity ** (4 / 3) * self.currentChemical.D_purewater
		self.D_effective["Chem_Benzo_g_h_i_perylene"]=self.Porosity ** (4 / 3) * self.currentChemical.D_purewater
		self.D_effective["Chem_Benzo_k_fluoranthene"]=self.Porosity ** (4 / 3) * self.currentChemical.D_purewater
		self.D_effective["Chem_Cadmium"]=self.Porosity ** (4 / 3) * self.currentChemical.D_purewater
		self.D_effective["Chem_Chrysene"]=self.Porosity ** (4 / 3) * self.currentChemical.D_purewater
		self.D_effective["Chem_Dibenz_a_h_anthracene"]=self.Porosity ** (4 / 3) * self.currentChemical.D_purewater
		self.D_effective["Chem_Divalent_Mercury"]=self.Porosity ** (4 / 3) * self.currentChemical.D_purewater
		self.D_effective["Chem_Elemental_Mercury"]=self.Porosity ** (4 / 3) * self.currentChemical.D_purewater
		self.D_effective["Chem_Fluoranthene"]=self.Porosity ** (4 / 3) * self.currentChemical.D_purewater
		self.D_effective["Chem_Fluorene"]=self.Porosity ** (4 / 3) * self.currentChemical.D_purewater
		self.D_effective["Chem_Indeno_1_2_3_cd_pyrene"]=self.Porosity ** (4 / 3) * self.currentChemical.D_purewater
		self.D_effective["Chem_Lead"]=self.Porosity ** (4 / 3) * self.currentChemical.D_purewater
		self.D_effective["Chem_MethylMercury"]=self.Porosity ** (4 / 3) * self.currentChemical.D_purewater
		try:
			self.Chemical_D_effective=self.D_effective[self.currentChemical.Name]
		except:
			self.Chemical_D_effective=nan

		self.GeneralDegradationRate={}
		self.GeneralDegradationRate["Chem_1_2_3_4_6_7_8_9_OCDD"]=log(2)/ self.Chemical_HalfLife
		self.GeneralDegradationRate["Chem_1_2_3_4_6_7_8_9_OCDF"]=log(2)/ self.Chemical_HalfLife
		self.GeneralDegradationRate["Chem_1_2_3_4_6_7_8_HpCDD"]=log(2)/ self.Chemical_HalfLife
		self.GeneralDegradationRate["Chem_1_2_3_4_6_7_8_HpCDF"]=log(2)/ self.Chemical_HalfLife
		self.GeneralDegradationRate["Chem_1_2_3_4_7_8_9_HpCDF"]=log(2)/ self.Chemical_HalfLife
		self.GeneralDegradationRate["Chem_1_2_3_4_7_8_HxCDD"]=log(2)/ self.Chemical_HalfLife
		self.GeneralDegradationRate["Chem_1_2_3_4_7_8_HxCDF"]=log(2)/ self.Chemical_HalfLife
		self.GeneralDegradationRate["Chem_1_2_3_6_7_8_HxCDD"]=log(2)/ self.Chemical_HalfLife
		self.GeneralDegradationRate["Chem_1_2_3_6_7_8_HxCDF"]=log(2)/ self.Chemical_HalfLife
		self.GeneralDegradationRate["Chem_1_2_3_7_8_9_HxCDD"]=log(2)/ self.Chemical_HalfLife
		self.GeneralDegradationRate["Chem_1_2_3_7_8_9_HxCDF"]=log(2)/ self.Chemical_HalfLife
		self.GeneralDegradationRate["Chem_1_2_3_7_8_PeCDD"]=log(2)/ self.Chemical_HalfLife
		self.GeneralDegradationRate["Chem_1_2_3_7_8_PeCDF"]=log(2)/ self.Chemical_HalfLife
		self.GeneralDegradationRate["Chem_2_3_4_6_7_8_HxCDF"]=log(2)/ self.Chemical_HalfLife
		self.GeneralDegradationRate["Chem_2_3_4_7_8_PeCDF"]=log(2)/ self.Chemical_HalfLife
		self.GeneralDegradationRate["Chem_2_3_7_8_TCDD"]=log(2)/ self.Chemical_HalfLife
		self.GeneralDegradationRate["Chem_2_3_7_8_TCDF"]=log(2)/ self.Chemical_HalfLife
		self.GeneralDegradationRate["Chem_2_Methylnaphthalene"]=log(2)/ self.Chemical_HalfLife
		self.GeneralDegradationRate["Chem_7_12_Dimethylbenz_a_anthracene"]=log(2)/ self.Chemical_HalfLife
		self.GeneralDegradationRate["Chem_Acenaphthene"]=log(2)/ self.Chemical_HalfLife
		self.GeneralDegradationRate["Chem_Acenaphthylene"]=log(2)/ self.Chemical_HalfLife
		self.GeneralDegradationRate["Chem_Benz_a_anthracene"]=log(2)/ self.Chemical_HalfLife
		self.GeneralDegradationRate["Chem_Benzo_A_Pyrene"]=log(2)/ self.Chemical_HalfLife
		self.GeneralDegradationRate["Chem_Benzo_b_fluoranthene"]=log(2)/ self.Chemical_HalfLife
		self.GeneralDegradationRate["Chem_Benzo_g_h_i_perylene"]=log(2)/ self.Chemical_HalfLife
		self.GeneralDegradationRate["Chem_Benzo_k_fluoranthene"]=log(2)/ self.Chemical_HalfLife
		self.GeneralDegradationRate["Chem_Chrysene"]=log(2)/ self.Chemical_HalfLife
		self.GeneralDegradationRate["Chem_Dibenz_a_h_anthracene"]=log(2)/ self.Chemical_HalfLife
		self.GeneralDegradationRate["Chem_Fluoranthene"]=log(2)/ self.Chemical_HalfLife
		self.GeneralDegradationRate["Chem_Fluorene"]=log(2)/ self.Chemical_HalfLife
		self.GeneralDegradationRate["Chem_Indeno_1_2_3_cd_pyrene"]=log(2)/ self.Chemical_HalfLife
		try:
			self.Chemical_GeneralDegradationRate=self.GeneralDegradationRate[self.currentChemical.Name]
		except:
			self.Chemical_GeneralDegradationRate=nan

		self.Kd={}
		self.Kd["Chem_1_2_3_4_6_7_8_9_OCDD"]=self.currentChemical.K_oc * self.OrganicCarbonContent
		self.Kd["Chem_1_2_3_4_6_7_8_9_OCDF"]=self.currentChemical.K_oc * self.OrganicCarbonContent
		self.Kd["Chem_1_2_3_4_6_7_8_HpCDD"]=self.currentChemical.K_oc * self.OrganicCarbonContent
		self.Kd["Chem_1_2_3_4_6_7_8_HpCDF"]=self.currentChemical.K_oc * self.OrganicCarbonContent
		self.Kd["Chem_1_2_3_4_7_8_9_HpCDF"]=self.currentChemical.K_oc * self.OrganicCarbonContent
		self.Kd["Chem_1_2_3_4_7_8_HxCDD"]=self.currentChemical.K_oc * self.OrganicCarbonContent
		self.Kd["Chem_1_2_3_4_7_8_HxCDF"]=self.currentChemical.K_oc * self.OrganicCarbonContent
		self.Kd["Chem_1_2_3_6_7_8_HxCDD"]=self.currentChemical.K_oc * self.OrganicCarbonContent
		self.Kd["Chem_1_2_3_6_7_8_HxCDF"]=self.currentChemical.K_oc * self.OrganicCarbonContent
		self.Kd["Chem_1_2_3_7_8_9_HxCDD"]=self.currentChemical.K_oc * self.OrganicCarbonContent
		self.Kd["Chem_1_2_3_7_8_9_HxCDF"]=self.currentChemical.K_oc * self.OrganicCarbonContent
		self.Kd["Chem_1_2_3_7_8_PeCDD"]=self.currentChemical.K_oc * self.OrganicCarbonContent
		self.Kd["Chem_1_2_3_7_8_PeCDF"]=self.currentChemical.K_oc * self.OrganicCarbonContent
		self.Kd["Chem_2_3_4_6_7_8_HxCDF"]=self.currentChemical.K_oc * self.OrganicCarbonContent
		self.Kd["Chem_2_3_4_7_8_PeCDF"]=self.currentChemical.K_oc * self.OrganicCarbonContent
		self.Kd["Chem_2_3_7_8_TCDD"]=self.currentChemical.K_oc * self.OrganicCarbonContent
		self.Kd["Chem_2_3_7_8_TCDF"]=self.currentChemical.K_oc * self.OrganicCarbonContent
		self.Kd["Chem_2_Methylnaphthalene"]=self.currentChemical.K_oc * self.OrganicCarbonContent
		self.Kd["Chem_7_12_Dimethylbenz_a_anthracene"]=self.currentChemical.K_oc * self.OrganicCarbonContent
		self.Kd["Chem_Acenaphthene"]=self.currentChemical.K_oc * self.OrganicCarbonContent
		self.Kd["Chem_Acenaphthylene"]=self.currentChemical.K_oc * self.OrganicCarbonContent
		self.Kd["Chem_Arsenic"]=316.2
		self.Kd["Chem_Benz_a_anthracene"]=self.currentChemical.K_oc * self.OrganicCarbonContent
		self.Kd["Chem_Benzo_A_Pyrene"]=self.currentChemical.K_oc * self.OrganicCarbonContent
		self.Kd["Chem_Benzo_b_fluoranthene"]=self.currentChemical.K_oc * self.OrganicCarbonContent
		self.Kd["Chem_Benzo_g_h_i_perylene"]=self.currentChemical.K_oc * self.OrganicCarbonContent
		self.Kd["Chem_Benzo_k_fluoranthene"]=self.currentChemical.K_oc * self.OrganicCarbonContent
		self.Kd["Chem_Cadmium"]=0.01
		self.Kd["Chem_Chrysene"]=self.currentChemical.K_oc * self.OrganicCarbonContent
		self.Kd["Chem_Dibenz_a_h_anthracene"]=self.currentChemical.K_oc * self.OrganicCarbonContent
		self.Kd["Chem_Divalent_Mercury"]=50000.0
		self.Kd["Chem_Elemental_Mercury"]=3000.0
		self.Kd["Chem_Fluoranthene"]=self.currentChemical.K_oc * self.OrganicCarbonContent
		self.Kd["Chem_Fluorene"]=self.currentChemical.K_oc * self.OrganicCarbonContent
		self.Kd["Chem_Indeno_1_2_3_cd_pyrene"]=self.currentChemical.K_oc * self.OrganicCarbonContent
		self.Kd["Chem_Lead"]=0.01
		self.Kd["Chem_MethylMercury"]=3000.0
		try:
			self.Chemical_Kd=self.Kd[self.currentChemical.Name]
		except:
			self.Chemical_Kd=nan

		self.SedimentBurialRateToHaveZeroNetDeposition_m3_m2_day=()
		self.SedimentBurialRateToHaveZeroNetDeposition_m3_m2_day=0.01

		self.VolumeFraction_Liquid=()
		self.VolumeFraction_Liquid=self.Porosity

		self.Z_Liquid={}
		self.Z_Liquid["Chem_1_2_3_4_6_7_8_9_OCDD"]=self.currentChemical.Z_purewater
		self.Z_Liquid["Chem_1_2_3_4_6_7_8_9_OCDF"]=self.currentChemical.Z_purewater
		self.Z_Liquid["Chem_1_2_3_4_6_7_8_HpCDD"]=self.currentChemical.Z_purewater
		self.Z_Liquid["Chem_1_2_3_4_6_7_8_HpCDF"]=self.currentChemical.Z_purewater
		self.Z_Liquid["Chem_1_2_3_4_7_8_9_HpCDF"]=self.currentChemical.Z_purewater
		self.Z_Liquid["Chem_1_2_3_4_7_8_HxCDD"]=self.currentChemical.Z_purewater
		self.Z_Liquid["Chem_1_2_3_4_7_8_HxCDF"]=self.currentChemical.Z_purewater
		self.Z_Liquid["Chem_1_2_3_6_7_8_HxCDD"]=self.currentChemical.Z_purewater
		self.Z_Liquid["Chem_1_2_3_6_7_8_HxCDF"]=self.currentChemical.Z_purewater
		self.Z_Liquid["Chem_1_2_3_7_8_9_HxCDD"]=self.currentChemical.Z_purewater
		self.Z_Liquid["Chem_1_2_3_7_8_9_HxCDF"]=self.currentChemical.Z_purewater
		self.Z_Liquid["Chem_1_2_3_7_8_PeCDD"]=self.currentChemical.Z_purewater
		self.Z_Liquid["Chem_1_2_3_7_8_PeCDF"]=self.currentChemical.Z_purewater
		self.Z_Liquid["Chem_2_3_4_6_7_8_HxCDF"]=self.currentChemical.Z_purewater
		self.Z_Liquid["Chem_2_3_4_7_8_PeCDF"]=self.currentChemical.Z_purewater
		self.Z_Liquid["Chem_2_3_7_8_TCDD"]=self.currentChemical.Z_purewater
		self.Z_Liquid["Chem_2_3_7_8_TCDF"]=self.currentChemical.Z_purewater
		self.Z_Liquid["Chem_2_Methylnaphthalene"]=self.currentChemical.Z_purewater
		self.Z_Liquid["Chem_7_12_Dimethylbenz_a_anthracene"]=self.currentChemical.Z_purewater
		self.Z_Liquid["Chem_Acenaphthene"]=self.currentChemical.Z_purewater
		self.Z_Liquid["Chem_Acenaphthylene"]=self.currentChemical.Z_purewater
		self.Z_Liquid["Chem_Arsenic"]=self.currentChemical.Z_purewater
		self.Z_Liquid["Chem_Benz_a_anthracene"]=self.currentChemical.Z_purewater
		self.Z_Liquid["Chem_Benzo_A_Pyrene"]=self.currentChemical.Z_purewater
		self.Z_Liquid["Chem_Benzo_b_fluoranthene"]=self.currentChemical.Z_purewater
		self.Z_Liquid["Chem_Benzo_g_h_i_perylene"]=self.currentChemical.Z_purewater
		self.Z_Liquid["Chem_Benzo_k_fluoranthene"]=self.currentChemical.Z_purewater
		self.Z_Liquid["Chem_Cadmium"]=self.currentChemical.Z_purewater
		self.Z_Liquid["Chem_Chrysene"]=self.currentChemical.Z_purewater
		self.Z_Liquid["Chem_Dibenz_a_h_anthracene"]=self.currentChemical.Z_purewater
		self.Z_Liquid["Chem_Divalent_Mercury"]=self.currentChemical.Z_purewater
		self.Z_Liquid["Chem_Elemental_Mercury"]=self.currentChemical.Z_purewater
		self.Z_Liquid["Chem_Fluoranthene"]=self.currentChemical.Z_purewater
		self.Z_Liquid["Chem_Fluorene"]=self.currentChemical.Z_purewater
		self.Z_Liquid["Chem_Indeno_1_2_3_cd_pyrene"]=self.currentChemical.Z_purewater
		self.Z_Liquid["Chem_Lead"]=self.currentChemical.Z_purewater
		self.Z_Liquid["Chem_MethylMercury"]=self.currentChemical.Z_purewater
		try:
			self.Chemical_Z_Liquid=self.Z_Liquid[self.currentChemical.Name]
		except:
			self.Chemical_Z_Liquid=nan

		self.BoundaryLayerThicknessbelowWater={}
		self.BoundaryLayerThicknessbelowWater["Chem_1_2_3_4_6_7_8_9_OCDD"]=318 * self.Chemical_D_effective ** (0.683)
		self.BoundaryLayerThicknessbelowWater["Chem_1_2_3_4_6_7_8_9_OCDF"]=318 * self.Chemical_D_effective ** (0.683)
		self.BoundaryLayerThicknessbelowWater["Chem_1_2_3_4_6_7_8_HpCDD"]=318 * self.Chemical_D_effective ** (0.683)
		self.BoundaryLayerThicknessbelowWater["Chem_1_2_3_4_6_7_8_HpCDF"]=318 * self.Chemical_D_effective ** (0.683)
		self.BoundaryLayerThicknessbelowWater["Chem_1_2_3_4_7_8_9_HpCDF"]=318 * self.Chemical_D_effective ** (0.683)
		self.BoundaryLayerThicknessbelowWater["Chem_1_2_3_4_7_8_HxCDD"]=318 * self.Chemical_D_effective ** (0.683)
		self.BoundaryLayerThicknessbelowWater["Chem_1_2_3_4_7_8_HxCDF"]=318 * self.Chemical_D_effective ** (0.683)
		self.BoundaryLayerThicknessbelowWater["Chem_1_2_3_6_7_8_HxCDD"]=318 * self.Chemical_D_effective ** (0.683)
		self.BoundaryLayerThicknessbelowWater["Chem_1_2_3_6_7_8_HxCDF"]=318 * self.Chemical_D_effective ** (0.683)
		self.BoundaryLayerThicknessbelowWater["Chem_1_2_3_7_8_9_HxCDD"]=318 * self.Chemical_D_effective ** (0.683)
		self.BoundaryLayerThicknessbelowWater["Chem_1_2_3_7_8_9_HxCDF"]=318 * self.Chemical_D_effective ** (0.683)
		self.BoundaryLayerThicknessbelowWater["Chem_1_2_3_7_8_PeCDD"]=318 * self.Chemical_D_effective ** (0.683)
		self.BoundaryLayerThicknessbelowWater["Chem_1_2_3_7_8_PeCDF"]=318 * self.Chemical_D_effective ** (0.683)
		self.BoundaryLayerThicknessbelowWater["Chem_2_3_4_6_7_8_HxCDF"]=318 * self.Chemical_D_effective ** (0.683)
		self.BoundaryLayerThicknessbelowWater["Chem_2_3_4_7_8_PeCDF"]=318 * self.Chemical_D_effective ** (0.683)
		self.BoundaryLayerThicknessbelowWater["Chem_2_3_7_8_TCDD"]=318 * self.Chemical_D_effective ** (0.683)
		self.BoundaryLayerThicknessbelowWater["Chem_2_3_7_8_TCDF"]=318 * self.Chemical_D_effective ** (0.683)
		self.BoundaryLayerThicknessbelowWater["Chem_2_Methylnaphthalene"]=318 * self.Chemical_D_effective ** (0.683)
		self.BoundaryLayerThicknessbelowWater["Chem_7_12_Dimethylbenz_a_anthracene"]=318 * self.Chemical_D_effective ** (0.683)
		self.BoundaryLayerThicknessbelowWater["Chem_Acenaphthene"]=318 * self.Chemical_D_effective ** (0.683)
		self.BoundaryLayerThicknessbelowWater["Chem_Acenaphthylene"]=318 * self.Chemical_D_effective ** (0.683)
		self.BoundaryLayerThicknessbelowWater["Chem_Arsenic"]=318 * self.Chemical_D_effective ** (0.683)
		self.BoundaryLayerThicknessbelowWater["Chem_Benz_a_anthracene"]=318 * self.Chemical_D_effective ** (0.683)
		self.BoundaryLayerThicknessbelowWater["Chem_Benzo_A_Pyrene"]=318 * self.Chemical_D_effective ** (0.683)
		self.BoundaryLayerThicknessbelowWater["Chem_Benzo_b_fluoranthene"]=318 * self.Chemical_D_effective ** (0.683)
		self.BoundaryLayerThicknessbelowWater["Chem_Benzo_g_h_i_perylene"]=318 * self.Chemical_D_effective ** (0.683)
		self.BoundaryLayerThicknessbelowWater["Chem_Benzo_k_fluoranthene"]=318 * self.Chemical_D_effective ** (0.683)
		self.BoundaryLayerThicknessbelowWater["Chem_Cadmium"]=318 * self.Chemical_D_effective ** (0.683)
		self.BoundaryLayerThicknessbelowWater["Chem_Chrysene"]=318 * self.Chemical_D_effective ** (0.683)
		self.BoundaryLayerThicknessbelowWater["Chem_Dibenz_a_h_anthracene"]=318 * self.Chemical_D_effective ** (0.683)
		self.BoundaryLayerThicknessbelowWater["Chem_Divalent_Mercury"]=318 * self.Chemical_D_effective ** (0.683)
		self.BoundaryLayerThicknessbelowWater["Chem_Elemental_Mercury"]=318 * self.Chemical_D_effective ** (0.683)
		self.BoundaryLayerThicknessbelowWater["Chem_Fluoranthene"]=318 * self.Chemical_D_effective ** (0.683)
		self.BoundaryLayerThicknessbelowWater["Chem_Fluorene"]=318 * self.Chemical_D_effective ** (0.683)
		self.BoundaryLayerThicknessbelowWater["Chem_Indeno_1_2_3_cd_pyrene"]=318 * self.Chemical_D_effective ** (0.683)
		self.BoundaryLayerThicknessbelowWater["Chem_Lead"]=318 * self.Chemical_D_effective ** (0.683)
		self.BoundaryLayerThicknessbelowWater["Chem_MethylMercury"]=318 * self.Chemical_D_effective ** (0.683)
		try:
			self.Chemical_BoundaryLayerThicknessbelowWater=self.BoundaryLayerThicknessbelowWater[self.currentChemical.Name]
		except:
			self.Chemical_BoundaryLayerThicknessbelowWater=nan

		self.SedimentResuspensionRate_kg_m2_day=()
		self.SedimentResuspensionRate_kg_m2_day=self.SedimentResuspensionVelocity*self.Benthic_Solids_Concentration

		self.Z_Solid={}
		self.Z_Solid["Chem_1_2_3_4_6_7_8_9_OCDD"]=self.Chemical_Kd * (self.rho / 1000) * self.currentChemical.Z_purewater
		self.Z_Solid["Chem_1_2_3_4_6_7_8_9_OCDF"]=self.Chemical_Kd * (self.rho / 1000) * self.currentChemical.Z_purewater
		self.Z_Solid["Chem_1_2_3_4_6_7_8_HpCDD"]=self.Chemical_Kd * (self.rho / 1000) * self.currentChemical.Z_purewater
		self.Z_Solid["Chem_1_2_3_4_6_7_8_HpCDF"]=self.Chemical_Kd * (self.rho / 1000) * self.currentChemical.Z_purewater
		self.Z_Solid["Chem_1_2_3_4_7_8_9_HpCDF"]=self.Chemical_Kd * (self.rho / 1000) * self.currentChemical.Z_purewater
		self.Z_Solid["Chem_1_2_3_4_7_8_HxCDD"]=self.Chemical_Kd * (self.rho / 1000) * self.currentChemical.Z_purewater
		self.Z_Solid["Chem_1_2_3_4_7_8_HxCDF"]=self.Chemical_Kd * (self.rho / 1000) * self.currentChemical.Z_purewater
		self.Z_Solid["Chem_1_2_3_6_7_8_HxCDD"]=self.Chemical_Kd * (self.rho / 1000) * self.currentChemical.Z_purewater
		self.Z_Solid["Chem_1_2_3_6_7_8_HxCDF"]=self.Chemical_Kd * (self.rho / 1000) * self.currentChemical.Z_purewater
		self.Z_Solid["Chem_1_2_3_7_8_9_HxCDD"]=self.Chemical_Kd * (self.rho / 1000) * self.currentChemical.Z_purewater
		self.Z_Solid["Chem_1_2_3_7_8_9_HxCDF"]=self.Chemical_Kd * (self.rho / 1000) * self.currentChemical.Z_purewater
		self.Z_Solid["Chem_1_2_3_7_8_PeCDD"]=self.Chemical_Kd * (self.rho / 1000) * self.currentChemical.Z_purewater
		self.Z_Solid["Chem_1_2_3_7_8_PeCDF"]=self.Chemical_Kd * (self.rho / 1000) * self.currentChemical.Z_purewater
		self.Z_Solid["Chem_2_3_4_6_7_8_HxCDF"]=self.Chemical_Kd * (self.rho / 1000) * self.currentChemical.Z_purewater
		self.Z_Solid["Chem_2_3_4_7_8_PeCDF"]=self.Chemical_Kd * (self.rho / 1000) * self.currentChemical.Z_purewater
		self.Z_Solid["Chem_2_3_7_8_TCDD"]=self.Chemical_Kd * (self.rho / 1000) * self.currentChemical.Z_purewater
		self.Z_Solid["Chem_2_3_7_8_TCDF"]=self.Chemical_Kd * (self.rho / 1000) * self.currentChemical.Z_purewater
		self.Z_Solid["Chem_2_Methylnaphthalene"]=self.Chemical_Kd * (self.rho / 1000) * self.currentChemical.Z_purewater
		self.Z_Solid["Chem_7_12_Dimethylbenz_a_anthracene"]=self.Chemical_Kd * (self.rho / 1000) * self.currentChemical.Z_purewater
		self.Z_Solid["Chem_Acenaphthene"]=self.Chemical_Kd * (self.rho / 1000) * self.currentChemical.Z_purewater
		self.Z_Solid["Chem_Acenaphthylene"]=self.Chemical_Kd * (self.rho / 1000) * self.currentChemical.Z_purewater
		self.Z_Solid["Chem_Arsenic"]=self.Chemical_Kd * (self.rho / 1000) * self.currentChemical.Z_purewater
		self.Z_Solid["Chem_Benz_a_anthracene"]=self.Chemical_Kd * (self.rho / 1000) * self.currentChemical.Z_purewater
		self.Z_Solid["Chem_Benzo_A_Pyrene"]=self.Chemical_Kd * (self.rho / 1000) * self.currentChemical.Z_purewater
		self.Z_Solid["Chem_Benzo_b_fluoranthene"]=self.Chemical_Kd * (self.rho / 1000) * self.currentChemical.Z_purewater
		self.Z_Solid["Chem_Benzo_g_h_i_perylene"]=self.Chemical_Kd * (self.rho / 1000) * self.currentChemical.Z_purewater
		self.Z_Solid["Chem_Benzo_k_fluoranthene"]=self.Chemical_Kd * (self.rho / 1000) * self.currentChemical.Z_purewater
		self.Z_Solid["Chem_Cadmium"]=self.Chemical_Kd * (self.rho / 1000) * self.currentChemical.Z_purewater
		self.Z_Solid["Chem_Chrysene"]=self.Chemical_Kd * (self.rho / 1000) * self.currentChemical.Z_purewater
		self.Z_Solid["Chem_Dibenz_a_h_anthracene"]=self.Chemical_Kd * (self.rho / 1000) * self.currentChemical.Z_purewater
		self.Z_Solid["Chem_Divalent_Mercury"]=self.Chemical_Kd * (self.rho / 1000) * self.currentChemical.Z_purewater
		self.Z_Solid["Chem_Elemental_Mercury"]=self.Chemical_Kd * (self.rho / 1000) * self.currentChemical.Z_purewater
		self.Z_Solid["Chem_Fluoranthene"]=self.Chemical_Kd * (self.rho / 1000) * self.currentChemical.Z_purewater
		self.Z_Solid["Chem_Fluorene"]=self.Chemical_Kd * (self.rho / 1000) * self.currentChemical.Z_purewater
		self.Z_Solid["Chem_Indeno_1_2_3_cd_pyrene"]=self.Chemical_Kd * (self.rho / 1000) * self.currentChemical.Z_purewater
		self.Z_Solid["Chem_Lead"]=self.Chemical_Kd * (self.rho / 1000) * self.currentChemical.Z_purewater
		self.Z_Solid["Chem_MethylMercury"]=self.Chemical_Kd * (self.rho / 1000) * self.currentChemical.Z_purewater
		try:
			self.Chemical_Z_Solid=self.Z_Solid[self.currentChemical.Name]
		except:
			self.Chemical_Z_Solid=nan

		self.VolumeFraction_Liquid=()
		self.VolumeFraction_Liquid=self.Porosity

		self.VolumeFraction_Solid=()
		self.VolumeFraction_Solid=1 - self.VolumeFraction_Liquid

		self.GenericDenominatorforCalculatingFractioninPhases={}
		self.GenericDenominatorforCalculatingFractioninPhases["Chem_1_2_3_4_6_7_8_9_OCDD"]=self.containingVolumeElement.Volume * self.VolumeFraction_Solid * self.Chemical_Kd * self.rho * self.Constants.m3_per_L + self.containingVolumeElement.Volume * self.VolumeFraction_Liquid
		self.GenericDenominatorforCalculatingFractioninPhases["Chem_1_2_3_4_6_7_8_9_OCDF"]=self.containingVolumeElement.Volume * self.VolumeFraction_Solid * self.Chemical_Kd * self.rho * self.Constants.m3_per_L + self.containingVolumeElement.Volume * self.VolumeFraction_Liquid
		self.GenericDenominatorforCalculatingFractioninPhases["Chem_1_2_3_4_6_7_8_HpCDD"]=self.containingVolumeElement.Volume * self.VolumeFraction_Solid * self.Chemical_Kd * self.rho * self.Constants.m3_per_L + self.containingVolumeElement.Volume * self.VolumeFraction_Liquid
		self.GenericDenominatorforCalculatingFractioninPhases["Chem_1_2_3_4_6_7_8_HpCDF"]=self.containingVolumeElement.Volume * self.VolumeFraction_Solid * self.Chemical_Kd * self.rho * self.Constants.m3_per_L + self.containingVolumeElement.Volume * self.VolumeFraction_Liquid
		self.GenericDenominatorforCalculatingFractioninPhases["Chem_1_2_3_4_7_8_9_HpCDF"]=self.containingVolumeElement.Volume * self.VolumeFraction_Solid * self.Chemical_Kd * self.rho * self.Constants.m3_per_L + self.containingVolumeElement.Volume * self.VolumeFraction_Liquid
		self.GenericDenominatorforCalculatingFractioninPhases["Chem_1_2_3_4_7_8_HxCDD"]=self.containingVolumeElement.Volume * self.VolumeFraction_Solid * self.Chemical_Kd * self.rho * self.Constants.m3_per_L + self.containingVolumeElement.Volume * self.VolumeFraction_Liquid
		self.GenericDenominatorforCalculatingFractioninPhases["Chem_1_2_3_4_7_8_HxCDF"]=self.containingVolumeElement.Volume * self.VolumeFraction_Solid * self.Chemical_Kd * self.rho * self.Constants.m3_per_L + self.containingVolumeElement.Volume * self.VolumeFraction_Liquid
		self.GenericDenominatorforCalculatingFractioninPhases["Chem_1_2_3_6_7_8_HxCDD"]=self.containingVolumeElement.Volume * self.VolumeFraction_Solid * self.Chemical_Kd * self.rho * self.Constants.m3_per_L + self.containingVolumeElement.Volume * self.VolumeFraction_Liquid
		self.GenericDenominatorforCalculatingFractioninPhases["Chem_1_2_3_6_7_8_HxCDF"]=self.containingVolumeElement.Volume * self.VolumeFraction_Solid * self.Chemical_Kd * self.rho * self.Constants.m3_per_L + self.containingVolumeElement.Volume * self.VolumeFraction_Liquid
		self.GenericDenominatorforCalculatingFractioninPhases["Chem_1_2_3_7_8_9_HxCDD"]=self.containingVolumeElement.Volume * self.VolumeFraction_Solid * self.Chemical_Kd * self.rho * self.Constants.m3_per_L + self.containingVolumeElement.Volume * self.VolumeFraction_Liquid
		self.GenericDenominatorforCalculatingFractioninPhases["Chem_1_2_3_7_8_9_HxCDF"]=self.containingVolumeElement.Volume * self.VolumeFraction_Solid * self.Chemical_Kd * self.rho * self.Constants.m3_per_L + self.containingVolumeElement.Volume * self.VolumeFraction_Liquid
		self.GenericDenominatorforCalculatingFractioninPhases["Chem_1_2_3_7_8_PeCDD"]=self.containingVolumeElement.Volume * self.VolumeFraction_Solid * self.Chemical_Kd * self.rho * self.Constants.m3_per_L + self.containingVolumeElement.Volume * self.VolumeFraction_Liquid
		self.GenericDenominatorforCalculatingFractioninPhases["Chem_1_2_3_7_8_PeCDF"]=self.containingVolumeElement.Volume * self.VolumeFraction_Solid * self.Chemical_Kd * self.rho * self.Constants.m3_per_L + self.containingVolumeElement.Volume * self.VolumeFraction_Liquid
		self.GenericDenominatorforCalculatingFractioninPhases["Chem_2_3_4_6_7_8_HxCDF"]=self.containingVolumeElement.Volume * self.VolumeFraction_Solid * self.Chemical_Kd * self.rho * self.Constants.m3_per_L + self.containingVolumeElement.Volume * self.VolumeFraction_Liquid
		self.GenericDenominatorforCalculatingFractioninPhases["Chem_2_3_4_7_8_PeCDF"]=self.containingVolumeElement.Volume * self.VolumeFraction_Solid * self.Chemical_Kd * self.rho * self.Constants.m3_per_L + self.containingVolumeElement.Volume * self.VolumeFraction_Liquid
		self.GenericDenominatorforCalculatingFractioninPhases["Chem_2_3_7_8_TCDD"]=self.containingVolumeElement.Volume * self.VolumeFraction_Solid * self.Chemical_Kd * self.rho * self.Constants.m3_per_L + self.containingVolumeElement.Volume * self.VolumeFraction_Liquid
		self.GenericDenominatorforCalculatingFractioninPhases["Chem_2_3_7_8_TCDF"]=self.containingVolumeElement.Volume * self.VolumeFraction_Solid * self.Chemical_Kd * self.rho * self.Constants.m3_per_L + self.containingVolumeElement.Volume * self.VolumeFraction_Liquid
		self.GenericDenominatorforCalculatingFractioninPhases["Chem_2_Methylnaphthalene"]=self.containingVolumeElement.Volume * self.VolumeFraction_Solid * self.Chemical_Kd * self.rho * self.Constants.m3_per_L + self.containingVolumeElement.Volume * self.VolumeFraction_Liquid
		self.GenericDenominatorforCalculatingFractioninPhases["Chem_7_12_Dimethylbenz_a_anthracene"]=self.containingVolumeElement.Volume * self.VolumeFraction_Solid * self.Chemical_Kd * self.rho * self.Constants.m3_per_L + self.containingVolumeElement.Volume * self.VolumeFraction_Liquid
		self.GenericDenominatorforCalculatingFractioninPhases["Chem_Acenaphthene"]=self.containingVolumeElement.Volume * self.VolumeFraction_Solid * self.Chemical_Kd * self.rho * self.Constants.m3_per_L + self.containingVolumeElement.Volume * self.VolumeFraction_Liquid
		self.GenericDenominatorforCalculatingFractioninPhases["Chem_Acenaphthylene"]=self.containingVolumeElement.Volume * self.VolumeFraction_Solid * self.Chemical_Kd * self.rho * self.Constants.m3_per_L + self.containingVolumeElement.Volume * self.VolumeFraction_Liquid
		self.GenericDenominatorforCalculatingFractioninPhases["Chem_Arsenic"]=self.containingVolumeElement.Volume * self.VolumeFraction_Solid * self.Chemical_Kd * self.rho * self.Constants.m3_per_L + self.containingVolumeElement.Volume * self.VolumeFraction_Liquid
		self.GenericDenominatorforCalculatingFractioninPhases["Chem_Benz_a_anthracene"]=self.containingVolumeElement.Volume * self.VolumeFraction_Solid * self.Chemical_Kd * self.rho * self.Constants.m3_per_L + self.containingVolumeElement.Volume * self.VolumeFraction_Liquid
		self.GenericDenominatorforCalculatingFractioninPhases["Chem_Benzo_A_Pyrene"]=self.containingVolumeElement.Volume * self.VolumeFraction_Solid * self.Chemical_Kd * self.rho * self.Constants.m3_per_L + self.containingVolumeElement.Volume * self.VolumeFraction_Liquid
		self.GenericDenominatorforCalculatingFractioninPhases["Chem_Benzo_b_fluoranthene"]=self.containingVolumeElement.Volume * self.VolumeFraction_Solid * self.Chemical_Kd * self.rho * self.Constants.m3_per_L + self.containingVolumeElement.Volume * self.VolumeFraction_Liquid
		self.GenericDenominatorforCalculatingFractioninPhases["Chem_Benzo_g_h_i_perylene"]=self.containingVolumeElement.Volume * self.VolumeFraction_Solid * self.Chemical_Kd * self.rho * self.Constants.m3_per_L + self.containingVolumeElement.Volume * self.VolumeFraction_Liquid
		self.GenericDenominatorforCalculatingFractioninPhases["Chem_Benzo_k_fluoranthene"]=self.containingVolumeElement.Volume * self.VolumeFraction_Solid * self.Chemical_Kd * self.rho * self.Constants.m3_per_L + self.containingVolumeElement.Volume * self.VolumeFraction_Liquid
		self.GenericDenominatorforCalculatingFractioninPhases["Chem_Cadmium"]=self.containingVolumeElement.Volume * self.VolumeFraction_Solid * self.Chemical_Kd * self.rho * self.Constants.m3_per_L + self.containingVolumeElement.Volume * self.VolumeFraction_Liquid
		self.GenericDenominatorforCalculatingFractioninPhases["Chem_Chrysene"]=self.containingVolumeElement.Volume * self.VolumeFraction_Solid * self.Chemical_Kd * self.rho * self.Constants.m3_per_L + self.containingVolumeElement.Volume * self.VolumeFraction_Liquid
		self.GenericDenominatorforCalculatingFractioninPhases["Chem_Dibenz_a_h_anthracene"]=self.containingVolumeElement.Volume * self.VolumeFraction_Solid * self.Chemical_Kd * self.rho * self.Constants.m3_per_L + self.containingVolumeElement.Volume * self.VolumeFraction_Liquid
		self.GenericDenominatorforCalculatingFractioninPhases["Chem_Divalent_Mercury"]=self.containingVolumeElement.Volume * self.VolumeFraction_Solid * self.Chemical_Kd * self.rho * self.Constants.m3_per_L + self.containingVolumeElement.Volume * self.VolumeFraction_Liquid
		self.GenericDenominatorforCalculatingFractioninPhases["Chem_Elemental_Mercury"]=self.containingVolumeElement.Volume * self.VolumeFraction_Solid * self.Chemical_Kd * self.rho * self.Constants.m3_per_L + self.containingVolumeElement.Volume * self.VolumeFraction_Liquid
		self.GenericDenominatorforCalculatingFractioninPhases["Chem_Fluoranthene"]=self.containingVolumeElement.Volume * self.VolumeFraction_Solid * self.Chemical_Kd * self.rho * self.Constants.m3_per_L + self.containingVolumeElement.Volume * self.VolumeFraction_Liquid
		self.GenericDenominatorforCalculatingFractioninPhases["Chem_Fluorene"]=self.containingVolumeElement.Volume * self.VolumeFraction_Solid * self.Chemical_Kd * self.rho * self.Constants.m3_per_L + self.containingVolumeElement.Volume * self.VolumeFraction_Liquid
		self.GenericDenominatorforCalculatingFractioninPhases["Chem_Indeno_1_2_3_cd_pyrene"]=self.containingVolumeElement.Volume * self.VolumeFraction_Solid * self.Chemical_Kd * self.rho * self.Constants.m3_per_L + self.containingVolumeElement.Volume * self.VolumeFraction_Liquid
		self.GenericDenominatorforCalculatingFractioninPhases["Chem_Lead"]=self.containingVolumeElement.Volume * self.VolumeFraction_Solid * self.Chemical_Kd * self.rho * self.Constants.m3_per_L + self.containingVolumeElement.Volume * self.VolumeFraction_Liquid
		self.GenericDenominatorforCalculatingFractioninPhases["Chem_MethylMercury"]=self.containingVolumeElement.Volume * self.VolumeFraction_Solid * self.Chemical_Kd * self.rho * self.Constants.m3_per_L + self.containingVolumeElement.Volume * self.VolumeFraction_Liquid
		try:
			self.Chemical_GenericDenominatorforCalculatingFractioninPhases=self.GenericDenominatorforCalculatingFractioninPhases[self.currentChemical.Name]
		except:
			self.Chemical_GenericDenominatorforCalculatingFractioninPhases=nan

		self.SedimentResuspensionRate_m3_m2_day=()
		self.SedimentResuspensionRate_m3_m2_day=self.SedimentResuspensionRate_kg_m2_day / self.rho

		self.Z_Total={}
		self.Z_Total["Chem_1_2_3_4_6_7_8_9_OCDD"]=self.Chemical_Z_Liquid * self.Porosity + self.Chemical_Z_Solid * (1 - self.Porosity)
		self.Z_Total["Chem_1_2_3_4_6_7_8_9_OCDF"]=self.Chemical_Z_Liquid * self.Porosity + self.Chemical_Z_Solid * (1 - self.Porosity)
		self.Z_Total["Chem_1_2_3_4_6_7_8_HpCDD"]=self.Chemical_Z_Liquid * self.Porosity + self.Chemical_Z_Solid * (1 - self.Porosity)
		self.Z_Total["Chem_1_2_3_4_6_7_8_HpCDF"]=self.Chemical_Z_Liquid * self.Porosity + self.Chemical_Z_Solid * (1 - self.Porosity)
		self.Z_Total["Chem_1_2_3_4_7_8_9_HpCDF"]=self.Chemical_Z_Liquid * self.Porosity + self.Chemical_Z_Solid * (1 - self.Porosity)
		self.Z_Total["Chem_1_2_3_4_7_8_HxCDD"]=self.Chemical_Z_Liquid * self.Porosity + self.Chemical_Z_Solid * (1 - self.Porosity)
		self.Z_Total["Chem_1_2_3_4_7_8_HxCDF"]=self.Chemical_Z_Liquid * self.Porosity + self.Chemical_Z_Solid * (1 - self.Porosity)
		self.Z_Total["Chem_1_2_3_6_7_8_HxCDD"]=self.Chemical_Z_Liquid * self.Porosity + self.Chemical_Z_Solid * (1 - self.Porosity)
		self.Z_Total["Chem_1_2_3_6_7_8_HxCDF"]=self.Chemical_Z_Liquid * self.Porosity + self.Chemical_Z_Solid * (1 - self.Porosity)
		self.Z_Total["Chem_1_2_3_7_8_9_HxCDD"]=self.Chemical_Z_Liquid * self.Porosity + self.Chemical_Z_Solid * (1 - self.Porosity)
		self.Z_Total["Chem_1_2_3_7_8_9_HxCDF"]=self.Chemical_Z_Liquid * self.Porosity + self.Chemical_Z_Solid * (1 - self.Porosity)
		self.Z_Total["Chem_1_2_3_7_8_PeCDD"]=self.Chemical_Z_Liquid * self.Porosity + self.Chemical_Z_Solid * (1 - self.Porosity)
		self.Z_Total["Chem_1_2_3_7_8_PeCDF"]=self.Chemical_Z_Liquid * self.Porosity + self.Chemical_Z_Solid * (1 - self.Porosity)
		self.Z_Total["Chem_2_3_4_6_7_8_HxCDF"]=self.Chemical_Z_Liquid * self.Porosity + self.Chemical_Z_Solid * (1 - self.Porosity)
		self.Z_Total["Chem_2_3_4_7_8_PeCDF"]=self.Chemical_Z_Liquid * self.Porosity + self.Chemical_Z_Solid * (1 - self.Porosity)
		self.Z_Total["Chem_2_3_7_8_TCDD"]=self.Chemical_Z_Liquid * self.Porosity + self.Chemical_Z_Solid * (1 - self.Porosity)
		self.Z_Total["Chem_2_3_7_8_TCDF"]=self.Chemical_Z_Liquid * self.Porosity + self.Chemical_Z_Solid * (1 - self.Porosity)
		self.Z_Total["Chem_2_Methylnaphthalene"]=self.Chemical_Z_Liquid * self.Porosity + self.Chemical_Z_Solid * (1 - self.Porosity)
		self.Z_Total["Chem_7_12_Dimethylbenz_a_anthracene"]=self.Chemical_Z_Liquid * self.Porosity + self.Chemical_Z_Solid * (1 - self.Porosity)
		self.Z_Total["Chem_Acenaphthene"]=self.Chemical_Z_Liquid * self.Porosity + self.Chemical_Z_Solid * (1 - self.Porosity)
		self.Z_Total["Chem_Acenaphthylene"]=self.Chemical_Z_Liquid * self.Porosity + self.Chemical_Z_Solid * (1 - self.Porosity)
		self.Z_Total["Chem_Arsenic"]=self.Chemical_Z_Liquid * self.Porosity + self.Chemical_Z_Solid * (1 - self.Porosity)
		self.Z_Total["Chem_Benz_a_anthracene"]=self.Chemical_Z_Liquid * self.Porosity + self.Chemical_Z_Solid * (1 - self.Porosity)
		self.Z_Total["Chem_Benzo_A_Pyrene"]=self.Chemical_Z_Liquid * self.Porosity + self.Chemical_Z_Solid * (1 - self.Porosity)
		self.Z_Total["Chem_Benzo_b_fluoranthene"]=self.Chemical_Z_Liquid * self.Porosity + self.Chemical_Z_Solid * (1 - self.Porosity)
		self.Z_Total["Chem_Benzo_g_h_i_perylene"]=self.Chemical_Z_Liquid * self.Porosity + self.Chemical_Z_Solid * (1 - self.Porosity)
		self.Z_Total["Chem_Benzo_k_fluoranthene"]=self.Chemical_Z_Liquid * self.Porosity + self.Chemical_Z_Solid * (1 - self.Porosity)
		self.Z_Total["Chem_Cadmium"]=self.Chemical_Z_Liquid * self.Porosity + self.Chemical_Z_Solid * (1 - self.Porosity)
		self.Z_Total["Chem_Chrysene"]=self.Chemical_Z_Liquid * self.Porosity + self.Chemical_Z_Solid * (1 - self.Porosity)
		self.Z_Total["Chem_Dibenz_a_h_anthracene"]=self.Chemical_Z_Liquid * self.Porosity + self.Chemical_Z_Solid * (1 - self.Porosity)
		self.Z_Total["Chem_Divalent_Mercury"]=self.Chemical_Z_Liquid * self.Porosity + self.Chemical_Z_Solid * (1 - self.Porosity)
		self.Z_Total["Chem_Elemental_Mercury"]=self.Chemical_Z_Liquid * self.Porosity + self.Chemical_Z_Solid * (1 - self.Porosity)
		self.Z_Total["Chem_Fluoranthene"]=self.Chemical_Z_Liquid * self.Porosity + self.Chemical_Z_Solid * (1 - self.Porosity)
		self.Z_Total["Chem_Fluorene"]=self.Chemical_Z_Liquid * self.Porosity + self.Chemical_Z_Solid * (1 - self.Porosity)
		self.Z_Total["Chem_Indeno_1_2_3_cd_pyrene"]=self.Chemical_Z_Liquid * self.Porosity + self.Chemical_Z_Solid * (1 - self.Porosity)
		self.Z_Total["Chem_Lead"]=self.Chemical_Z_Liquid * self.Porosity + self.Chemical_Z_Solid * (1 - self.Porosity)
		self.Z_Total["Chem_MethylMercury"]=self.Chemical_Z_Liquid * self.Porosity + self.Chemical_Z_Solid * (1 - self.Porosity)
		try:
			self.Chemical_Z_Total=self.Z_Total[self.currentChemical.Name]
		except:
			self.Chemical_Z_Total=nan

		self.Area=()
		self.Area=containingVolumeElement.Area

		self.Depth=()
		self.Depth=self.containingVolumeElement.Height

		self.FractionMass_Dissolved={}
		self.FractionMass_Dissolved["Chem_1_2_3_4_6_7_8_9_OCDD"]=self.containingVolumeElement.Volume * self.VolumeFraction_Liquid /self.Chemical_GenericDenominatorforCalculatingFractioninPhases
		self.FractionMass_Dissolved["Chem_1_2_3_4_6_7_8_9_OCDF"]=self.containingVolumeElement.Volume * self.VolumeFraction_Liquid /self.Chemical_GenericDenominatorforCalculatingFractioninPhases
		self.FractionMass_Dissolved["Chem_1_2_3_4_6_7_8_HpCDD"]=self.containingVolumeElement.Volume * self.VolumeFraction_Liquid /self.Chemical_GenericDenominatorforCalculatingFractioninPhases
		self.FractionMass_Dissolved["Chem_1_2_3_4_6_7_8_HpCDF"]=self.containingVolumeElement.Volume * self.VolumeFraction_Liquid /self.Chemical_GenericDenominatorforCalculatingFractioninPhases
		self.FractionMass_Dissolved["Chem_1_2_3_4_7_8_9_HpCDF"]=self.containingVolumeElement.Volume * self.VolumeFraction_Liquid /self.Chemical_GenericDenominatorforCalculatingFractioninPhases
		self.FractionMass_Dissolved["Chem_1_2_3_4_7_8_HxCDD"]=self.containingVolumeElement.Volume * self.VolumeFraction_Liquid /self.Chemical_GenericDenominatorforCalculatingFractioninPhases
		self.FractionMass_Dissolved["Chem_1_2_3_4_7_8_HxCDF"]=self.containingVolumeElement.Volume * self.VolumeFraction_Liquid /self.Chemical_GenericDenominatorforCalculatingFractioninPhases
		self.FractionMass_Dissolved["Chem_1_2_3_6_7_8_HxCDD"]=self.containingVolumeElement.Volume * self.VolumeFraction_Liquid /self.Chemical_GenericDenominatorforCalculatingFractioninPhases
		self.FractionMass_Dissolved["Chem_1_2_3_6_7_8_HxCDF"]=self.containingVolumeElement.Volume * self.VolumeFraction_Liquid /self.Chemical_GenericDenominatorforCalculatingFractioninPhases
		self.FractionMass_Dissolved["Chem_1_2_3_7_8_9_HxCDD"]=self.containingVolumeElement.Volume * self.VolumeFraction_Liquid /self.Chemical_GenericDenominatorforCalculatingFractioninPhases
		self.FractionMass_Dissolved["Chem_1_2_3_7_8_9_HxCDF"]=self.containingVolumeElement.Volume * self.VolumeFraction_Liquid /self.Chemical_GenericDenominatorforCalculatingFractioninPhases
		self.FractionMass_Dissolved["Chem_1_2_3_7_8_PeCDD"]=self.containingVolumeElement.Volume * self.VolumeFraction_Liquid /self.Chemical_GenericDenominatorforCalculatingFractioninPhases
		self.FractionMass_Dissolved["Chem_1_2_3_7_8_PeCDF"]=self.containingVolumeElement.Volume * self.VolumeFraction_Liquid /self.Chemical_GenericDenominatorforCalculatingFractioninPhases
		self.FractionMass_Dissolved["Chem_2_3_4_6_7_8_HxCDF"]=self.containingVolumeElement.Volume * self.VolumeFraction_Liquid /self.Chemical_GenericDenominatorforCalculatingFractioninPhases
		self.FractionMass_Dissolved["Chem_2_3_4_7_8_PeCDF"]=self.containingVolumeElement.Volume * self.VolumeFraction_Liquid /self.Chemical_GenericDenominatorforCalculatingFractioninPhases
		self.FractionMass_Dissolved["Chem_2_3_7_8_TCDD"]=self.containingVolumeElement.Volume * self.VolumeFraction_Liquid /self.Chemical_GenericDenominatorforCalculatingFractioninPhases
		self.FractionMass_Dissolved["Chem_2_3_7_8_TCDF"]=self.containingVolumeElement.Volume * self.VolumeFraction_Liquid /self.Chemical_GenericDenominatorforCalculatingFractioninPhases
		self.FractionMass_Dissolved["Chem_2_Methylnaphthalene"]=self.containingVolumeElement.Volume * self.VolumeFraction_Liquid /self.Chemical_GenericDenominatorforCalculatingFractioninPhases
		self.FractionMass_Dissolved["Chem_7_12_Dimethylbenz_a_anthracene"]=self.containingVolumeElement.Volume * self.VolumeFraction_Liquid /self.Chemical_GenericDenominatorforCalculatingFractioninPhases
		self.FractionMass_Dissolved["Chem_Acenaphthene"]=self.containingVolumeElement.Volume * self.VolumeFraction_Liquid /self.Chemical_GenericDenominatorforCalculatingFractioninPhases
		self.FractionMass_Dissolved["Chem_Acenaphthylene"]=self.containingVolumeElement.Volume * self.VolumeFraction_Liquid /self.Chemical_GenericDenominatorforCalculatingFractioninPhases
		self.FractionMass_Dissolved["Chem_Benz_a_anthracene"]=self.containingVolumeElement.Volume * self.VolumeFraction_Liquid /self.Chemical_GenericDenominatorforCalculatingFractioninPhases
		self.FractionMass_Dissolved["Chem_Benzo_A_Pyrene"]=self.containingVolumeElement.Volume * self.VolumeFraction_Liquid /self.Chemical_GenericDenominatorforCalculatingFractioninPhases
		self.FractionMass_Dissolved["Chem_Benzo_b_fluoranthene"]=self.containingVolumeElement.Volume * self.VolumeFraction_Liquid /self.Chemical_GenericDenominatorforCalculatingFractioninPhases
		self.FractionMass_Dissolved["Chem_Benzo_g_h_i_perylene"]=self.containingVolumeElement.Volume * self.VolumeFraction_Liquid /self.Chemical_GenericDenominatorforCalculatingFractioninPhases
		self.FractionMass_Dissolved["Chem_Benzo_k_fluoranthene"]=self.containingVolumeElement.Volume * self.VolumeFraction_Liquid /self.Chemical_GenericDenominatorforCalculatingFractioninPhases
		self.FractionMass_Dissolved["Chem_Chrysene"]=self.containingVolumeElement.Volume * self.VolumeFraction_Liquid /self.Chemical_GenericDenominatorforCalculatingFractioninPhases
		self.FractionMass_Dissolved["Chem_Dibenz_a_h_anthracene"]=self.containingVolumeElement.Volume * self.VolumeFraction_Liquid /self.Chemical_GenericDenominatorforCalculatingFractioninPhases
		self.FractionMass_Dissolved["Chem_Divalent_Mercury"]=self.containingVolumeElement.Volume * self.VolumeFraction_Liquid /self.Chemical_GenericDenominatorforCalculatingFractioninPhases
		self.FractionMass_Dissolved["Chem_Elemental_Mercury"]=self.containingVolumeElement.Volume * self.VolumeFraction_Liquid /self.Chemical_GenericDenominatorforCalculatingFractioninPhases
		self.FractionMass_Dissolved["Chem_Fluoranthene"]=self.containingVolumeElement.Volume * self.VolumeFraction_Liquid /self.Chemical_GenericDenominatorforCalculatingFractioninPhases
		self.FractionMass_Dissolved["Chem_Fluorene"]=self.containingVolumeElement.Volume * self.VolumeFraction_Liquid /self.Chemical_GenericDenominatorforCalculatingFractioninPhases
		self.FractionMass_Dissolved["Chem_Indeno_1_2_3_cd_pyrene"]=self.containingVolumeElement.Volume * self.VolumeFraction_Liquid /self.Chemical_GenericDenominatorforCalculatingFractioninPhases
		self.FractionMass_Dissolved["Chem_MethylMercury"]=self.containingVolumeElement.Volume * self.VolumeFraction_Liquid /self.Chemical_GenericDenominatorforCalculatingFractioninPhases
		try:
			self.Chemical_FractionMass_Dissolved=self.FractionMass_Dissolved[self.currentChemical.Name]
		except:
			self.Chemical_FractionMass_Dissolved=nan

		self.FractionMass_Sorbed={}
		self.FractionMass_Sorbed["Chem_1_2_3_4_6_7_8_9_OCDD"]=self.containingVolumeElement.Volume * self.VolumeFraction_Solid * self.Chemical_Kd * self.rho * self.Constants.m3_per_L  /self.Chemical_GenericDenominatorforCalculatingFractioninPhases
		self.FractionMass_Sorbed["Chem_1_2_3_4_6_7_8_9_OCDF"]=self.containingVolumeElement.Volume * self.VolumeFraction_Solid * self.Chemical_Kd * self.rho * self.Constants.m3_per_L  /self.Chemical_GenericDenominatorforCalculatingFractioninPhases
		self.FractionMass_Sorbed["Chem_1_2_3_4_6_7_8_HpCDD"]=self.containingVolumeElement.Volume * self.VolumeFraction_Solid * self.Chemical_Kd * self.rho * self.Constants.m3_per_L  /self.Chemical_GenericDenominatorforCalculatingFractioninPhases
		self.FractionMass_Sorbed["Chem_1_2_3_4_6_7_8_HpCDF"]=self.containingVolumeElement.Volume * self.VolumeFraction_Solid * self.Chemical_Kd * self.rho * self.Constants.m3_per_L  /self.Chemical_GenericDenominatorforCalculatingFractioninPhases
		self.FractionMass_Sorbed["Chem_1_2_3_4_7_8_9_HpCDF"]=self.containingVolumeElement.Volume * self.VolumeFraction_Solid * self.Chemical_Kd * self.rho * self.Constants.m3_per_L  /self.Chemical_GenericDenominatorforCalculatingFractioninPhases
		self.FractionMass_Sorbed["Chem_1_2_3_4_7_8_HxCDD"]=self.containingVolumeElement.Volume * self.VolumeFraction_Solid * self.Chemical_Kd * self.rho * self.Constants.m3_per_L  /self.Chemical_GenericDenominatorforCalculatingFractioninPhases
		self.FractionMass_Sorbed["Chem_1_2_3_4_7_8_HxCDF"]=self.containingVolumeElement.Volume * self.VolumeFraction_Solid * self.Chemical_Kd * self.rho * self.Constants.m3_per_L  /self.Chemical_GenericDenominatorforCalculatingFractioninPhases
		self.FractionMass_Sorbed["Chem_1_2_3_6_7_8_HxCDD"]=self.containingVolumeElement.Volume * self.VolumeFraction_Solid * self.Chemical_Kd * self.rho * self.Constants.m3_per_L  /self.Chemical_GenericDenominatorforCalculatingFractioninPhases
		self.FractionMass_Sorbed["Chem_1_2_3_6_7_8_HxCDF"]=self.containingVolumeElement.Volume * self.VolumeFraction_Solid * self.Chemical_Kd * self.rho * self.Constants.m3_per_L  /self.Chemical_GenericDenominatorforCalculatingFractioninPhases
		self.FractionMass_Sorbed["Chem_1_2_3_7_8_9_HxCDD"]=self.containingVolumeElement.Volume * self.VolumeFraction_Solid * self.Chemical_Kd * self.rho * self.Constants.m3_per_L  /self.Chemical_GenericDenominatorforCalculatingFractioninPhases
		self.FractionMass_Sorbed["Chem_1_2_3_7_8_9_HxCDF"]=self.containingVolumeElement.Volume * self.VolumeFraction_Solid * self.Chemical_Kd * self.rho * self.Constants.m3_per_L  /self.Chemical_GenericDenominatorforCalculatingFractioninPhases
		self.FractionMass_Sorbed["Chem_1_2_3_7_8_PeCDD"]=self.containingVolumeElement.Volume * self.VolumeFraction_Solid * self.Chemical_Kd * self.rho * self.Constants.m3_per_L  /self.Chemical_GenericDenominatorforCalculatingFractioninPhases
		self.FractionMass_Sorbed["Chem_1_2_3_7_8_PeCDF"]=self.containingVolumeElement.Volume * self.VolumeFraction_Solid * self.Chemical_Kd * self.rho * self.Constants.m3_per_L  /self.Chemical_GenericDenominatorforCalculatingFractioninPhases
		self.FractionMass_Sorbed["Chem_2_3_4_6_7_8_HxCDF"]=self.containingVolumeElement.Volume * self.VolumeFraction_Solid * self.Chemical_Kd * self.rho * self.Constants.m3_per_L  /self.Chemical_GenericDenominatorforCalculatingFractioninPhases
		self.FractionMass_Sorbed["Chem_2_3_4_7_8_PeCDF"]=self.containingVolumeElement.Volume * self.VolumeFraction_Solid * self.Chemical_Kd * self.rho * self.Constants.m3_per_L  /self.Chemical_GenericDenominatorforCalculatingFractioninPhases
		self.FractionMass_Sorbed["Chem_2_3_7_8_TCDD"]=self.containingVolumeElement.Volume * self.VolumeFraction_Solid * self.Chemical_Kd * self.rho * self.Constants.m3_per_L  /self.Chemical_GenericDenominatorforCalculatingFractioninPhases
		self.FractionMass_Sorbed["Chem_2_3_7_8_TCDF"]=self.containingVolumeElement.Volume * self.VolumeFraction_Solid * self.Chemical_Kd * self.rho * self.Constants.m3_per_L  /self.Chemical_GenericDenominatorforCalculatingFractioninPhases
		self.FractionMass_Sorbed["Chem_2_Methylnaphthalene"]=self.containingVolumeElement.Volume * self.VolumeFraction_Solid * self.Chemical_Kd * self.rho * self.Constants.m3_per_L  /self.Chemical_GenericDenominatorforCalculatingFractioninPhases
		self.FractionMass_Sorbed["Chem_7_12_Dimethylbenz_a_anthracene"]=self.containingVolumeElement.Volume * self.VolumeFraction_Solid * self.Chemical_Kd * self.rho * self.Constants.m3_per_L  /self.Chemical_GenericDenominatorforCalculatingFractioninPhases
		self.FractionMass_Sorbed["Chem_Acenaphthene"]=self.containingVolumeElement.Volume * self.VolumeFraction_Solid * self.Chemical_Kd * self.rho * self.Constants.m3_per_L  /self.Chemical_GenericDenominatorforCalculatingFractioninPhases
		self.FractionMass_Sorbed["Chem_Acenaphthylene"]=self.containingVolumeElement.Volume * self.VolumeFraction_Solid * self.Chemical_Kd * self.rho * self.Constants.m3_per_L  /self.Chemical_GenericDenominatorforCalculatingFractioninPhases
		self.FractionMass_Sorbed["Chem_Arsenic"]=self.containingVolumeElement.Volume * self.VolumeFraction_Solid * self.Chemical_Kd * self.rho * self.Constants.m3_per_L  /self.Chemical_GenericDenominatorforCalculatingFractioninPhases
		self.FractionMass_Sorbed["Chem_Benz_a_anthracene"]=self.containingVolumeElement.Volume * self.VolumeFraction_Solid * self.Chemical_Kd * self.rho * self.Constants.m3_per_L  /self.Chemical_GenericDenominatorforCalculatingFractioninPhases
		self.FractionMass_Sorbed["Chem_Benzo_A_Pyrene"]=self.containingVolumeElement.Volume * self.VolumeFraction_Solid * self.Chemical_Kd * self.rho * self.Constants.m3_per_L  /self.Chemical_GenericDenominatorforCalculatingFractioninPhases
		self.FractionMass_Sorbed["Chem_Benzo_b_fluoranthene"]=self.containingVolumeElement.Volume * self.VolumeFraction_Solid * self.Chemical_Kd * self.rho * self.Constants.m3_per_L  /self.Chemical_GenericDenominatorforCalculatingFractioninPhases
		self.FractionMass_Sorbed["Chem_Benzo_g_h_i_perylene"]=self.containingVolumeElement.Volume * self.VolumeFraction_Solid * self.Chemical_Kd * self.rho * self.Constants.m3_per_L  /self.Chemical_GenericDenominatorforCalculatingFractioninPhases
		self.FractionMass_Sorbed["Chem_Benzo_k_fluoranthene"]=self.containingVolumeElement.Volume * self.VolumeFraction_Solid * self.Chemical_Kd * self.rho * self.Constants.m3_per_L  /self.Chemical_GenericDenominatorforCalculatingFractioninPhases
		self.FractionMass_Sorbed["Chem_Cadmium"]=self.containingVolumeElement.Volume * self.VolumeFraction_Solid * self.Chemical_Kd * self.rho * self.Constants.m3_per_L  /self.Chemical_GenericDenominatorforCalculatingFractioninPhases
		self.FractionMass_Sorbed["Chem_Chrysene"]=self.containingVolumeElement.Volume * self.VolumeFraction_Solid * self.Chemical_Kd * self.rho * self.Constants.m3_per_L  /self.Chemical_GenericDenominatorforCalculatingFractioninPhases
		self.FractionMass_Sorbed["Chem_Dibenz_a_h_anthracene"]=self.containingVolumeElement.Volume * self.VolumeFraction_Solid * self.Chemical_Kd * self.rho * self.Constants.m3_per_L  /self.Chemical_GenericDenominatorforCalculatingFractioninPhases
		self.FractionMass_Sorbed["Chem_Divalent_Mercury"]=self.containingVolumeElement.Volume * self.VolumeFraction_Solid * self.Chemical_Kd * self.rho * self.Constants.m3_per_L  /self.Chemical_GenericDenominatorforCalculatingFractioninPhases
		self.FractionMass_Sorbed["Chem_Elemental_Mercury"]=self.containingVolumeElement.Volume * self.VolumeFraction_Solid * self.Chemical_Kd * self.rho * self.Constants.m3_per_L  /self.Chemical_GenericDenominatorforCalculatingFractioninPhases
		self.FractionMass_Sorbed["Chem_Fluoranthene"]=self.containingVolumeElement.Volume * self.VolumeFraction_Solid * self.Chemical_Kd * self.rho * self.Constants.m3_per_L  /self.Chemical_GenericDenominatorforCalculatingFractioninPhases
		self.FractionMass_Sorbed["Chem_Fluorene"]=self.containingVolumeElement.Volume * self.VolumeFraction_Solid * self.Chemical_Kd * self.rho * self.Constants.m3_per_L  /self.Chemical_GenericDenominatorforCalculatingFractioninPhases
		self.FractionMass_Sorbed["Chem_Indeno_1_2_3_cd_pyrene"]=self.containingVolumeElement.Volume * self.VolumeFraction_Solid * self.Chemical_Kd * self.rho * self.Constants.m3_per_L  /self.Chemical_GenericDenominatorforCalculatingFractioninPhases
		self.FractionMass_Sorbed["Chem_Lead"]=self.containingVolumeElement.Volume * self.VolumeFraction_Solid * self.Chemical_Kd * self.rho * self.Constants.m3_per_L  /self.Chemical_GenericDenominatorforCalculatingFractioninPhases
		self.FractionMass_Sorbed["Chem_MethylMercury"]=self.containingVolumeElement.Volume * self.VolumeFraction_Solid * self.Chemical_Kd * self.rho * self.Constants.m3_per_L  /self.Chemical_GenericDenominatorforCalculatingFractioninPhases
		try:
			self.Chemical_FractionMass_Sorbed=self.FractionMass_Sorbed[self.currentChemical.Name]
		except:
			self.Chemical_FractionMass_Sorbed=nan

		self.GenericDenominatorforCalculatingFractioninPhases={}
		self.GenericDenominatorforCalculatingFractioninPhases["Chem_1_2_3_4_6_7_8_9_OCDD"]=self.containingVolumeElement.Volume * self.VolumeFraction_Solid * self.Chemical_Kd * self.rho * self.Constants.m3_per_L + self.containingVolumeElement.Volume * self.VolumeFraction_Liquid
		self.GenericDenominatorforCalculatingFractioninPhases["Chem_1_2_3_4_6_7_8_9_OCDF"]=self.containingVolumeElement.Volume * self.VolumeFraction_Solid * self.Chemical_Kd * self.rho * self.Constants.m3_per_L + self.containingVolumeElement.Volume * self.VolumeFraction_Liquid
		self.GenericDenominatorforCalculatingFractioninPhases["Chem_1_2_3_4_6_7_8_HpCDD"]=self.containingVolumeElement.Volume * self.VolumeFraction_Solid * self.Chemical_Kd * self.rho * self.Constants.m3_per_L + self.containingVolumeElement.Volume * self.VolumeFraction_Liquid
		self.GenericDenominatorforCalculatingFractioninPhases["Chem_1_2_3_4_6_7_8_HpCDF"]=self.containingVolumeElement.Volume * self.VolumeFraction_Solid * self.Chemical_Kd * self.rho * self.Constants.m3_per_L + self.containingVolumeElement.Volume * self.VolumeFraction_Liquid
		self.GenericDenominatorforCalculatingFractioninPhases["Chem_1_2_3_4_7_8_9_HpCDF"]=self.containingVolumeElement.Volume * self.VolumeFraction_Solid * self.Chemical_Kd * self.rho * self.Constants.m3_per_L + self.containingVolumeElement.Volume * self.VolumeFraction_Liquid
		self.GenericDenominatorforCalculatingFractioninPhases["Chem_1_2_3_4_7_8_HxCDD"]=self.containingVolumeElement.Volume * self.VolumeFraction_Solid * self.Chemical_Kd * self.rho * self.Constants.m3_per_L + self.containingVolumeElement.Volume * self.VolumeFraction_Liquid
		self.GenericDenominatorforCalculatingFractioninPhases["Chem_1_2_3_4_7_8_HxCDF"]=self.containingVolumeElement.Volume * self.VolumeFraction_Solid * self.Chemical_Kd * self.rho * self.Constants.m3_per_L + self.containingVolumeElement.Volume * self.VolumeFraction_Liquid
		self.GenericDenominatorforCalculatingFractioninPhases["Chem_1_2_3_6_7_8_HxCDD"]=self.containingVolumeElement.Volume * self.VolumeFraction_Solid * self.Chemical_Kd * self.rho * self.Constants.m3_per_L + self.containingVolumeElement.Volume * self.VolumeFraction_Liquid
		self.GenericDenominatorforCalculatingFractioninPhases["Chem_1_2_3_6_7_8_HxCDF"]=self.containingVolumeElement.Volume * self.VolumeFraction_Solid * self.Chemical_Kd * self.rho * self.Constants.m3_per_L + self.containingVolumeElement.Volume * self.VolumeFraction_Liquid
		self.GenericDenominatorforCalculatingFractioninPhases["Chem_1_2_3_7_8_9_HxCDD"]=self.containingVolumeElement.Volume * self.VolumeFraction_Solid * self.Chemical_Kd * self.rho * self.Constants.m3_per_L + self.containingVolumeElement.Volume * self.VolumeFraction_Liquid
		self.GenericDenominatorforCalculatingFractioninPhases["Chem_1_2_3_7_8_9_HxCDF"]=self.containingVolumeElement.Volume * self.VolumeFraction_Solid * self.Chemical_Kd * self.rho * self.Constants.m3_per_L + self.containingVolumeElement.Volume * self.VolumeFraction_Liquid
		self.GenericDenominatorforCalculatingFractioninPhases["Chem_1_2_3_7_8_PeCDD"]=self.containingVolumeElement.Volume * self.VolumeFraction_Solid * self.Chemical_Kd * self.rho * self.Constants.m3_per_L + self.containingVolumeElement.Volume * self.VolumeFraction_Liquid
		self.GenericDenominatorforCalculatingFractioninPhases["Chem_1_2_3_7_8_PeCDF"]=self.containingVolumeElement.Volume * self.VolumeFraction_Solid * self.Chemical_Kd * self.rho * self.Constants.m3_per_L + self.containingVolumeElement.Volume * self.VolumeFraction_Liquid
		self.GenericDenominatorforCalculatingFractioninPhases["Chem_2_3_4_6_7_8_HxCDF"]=self.containingVolumeElement.Volume * self.VolumeFraction_Solid * self.Chemical_Kd * self.rho * self.Constants.m3_per_L + self.containingVolumeElement.Volume * self.VolumeFraction_Liquid
		self.GenericDenominatorforCalculatingFractioninPhases["Chem_2_3_4_7_8_PeCDF"]=self.containingVolumeElement.Volume * self.VolumeFraction_Solid * self.Chemical_Kd * self.rho * self.Constants.m3_per_L + self.containingVolumeElement.Volume * self.VolumeFraction_Liquid
		self.GenericDenominatorforCalculatingFractioninPhases["Chem_2_3_7_8_TCDD"]=self.containingVolumeElement.Volume * self.VolumeFraction_Solid * self.Chemical_Kd * self.rho * self.Constants.m3_per_L + self.containingVolumeElement.Volume * self.VolumeFraction_Liquid
		self.GenericDenominatorforCalculatingFractioninPhases["Chem_2_3_7_8_TCDF"]=self.containingVolumeElement.Volume * self.VolumeFraction_Solid * self.Chemical_Kd * self.rho * self.Constants.m3_per_L + self.containingVolumeElement.Volume * self.VolumeFraction_Liquid
		self.GenericDenominatorforCalculatingFractioninPhases["Chem_2_Methylnaphthalene"]=self.containingVolumeElement.Volume * self.VolumeFraction_Solid * self.Chemical_Kd * self.rho * self.Constants.m3_per_L + self.containingVolumeElement.Volume * self.VolumeFraction_Liquid
		self.GenericDenominatorforCalculatingFractioninPhases["Chem_7_12_Dimethylbenz_a_anthracene"]=self.containingVolumeElement.Volume * self.VolumeFraction_Solid * self.Chemical_Kd * self.rho * self.Constants.m3_per_L + self.containingVolumeElement.Volume * self.VolumeFraction_Liquid
		self.GenericDenominatorforCalculatingFractioninPhases["Chem_Acenaphthene"]=self.containingVolumeElement.Volume * self.VolumeFraction_Solid * self.Chemical_Kd * self.rho * self.Constants.m3_per_L + self.containingVolumeElement.Volume * self.VolumeFraction_Liquid
		self.GenericDenominatorforCalculatingFractioninPhases["Chem_Acenaphthylene"]=self.containingVolumeElement.Volume * self.VolumeFraction_Solid * self.Chemical_Kd * self.rho * self.Constants.m3_per_L + self.containingVolumeElement.Volume * self.VolumeFraction_Liquid
		self.GenericDenominatorforCalculatingFractioninPhases["Chem_Arsenic"]=self.containingVolumeElement.Volume * self.VolumeFraction_Solid * self.Chemical_Kd * self.rho * self.Constants.m3_per_L + self.containingVolumeElement.Volume * self.VolumeFraction_Liquid
		self.GenericDenominatorforCalculatingFractioninPhases["Chem_Benz_a_anthracene"]=self.containingVolumeElement.Volume * self.VolumeFraction_Solid * self.Chemical_Kd * self.rho * self.Constants.m3_per_L + self.containingVolumeElement.Volume * self.VolumeFraction_Liquid
		self.GenericDenominatorforCalculatingFractioninPhases["Chem_Benzo_A_Pyrene"]=self.containingVolumeElement.Volume * self.VolumeFraction_Solid * self.Chemical_Kd * self.rho * self.Constants.m3_per_L + self.containingVolumeElement.Volume * self.VolumeFraction_Liquid
		self.GenericDenominatorforCalculatingFractioninPhases["Chem_Benzo_b_fluoranthene"]=self.containingVolumeElement.Volume * self.VolumeFraction_Solid * self.Chemical_Kd * self.rho * self.Constants.m3_per_L + self.containingVolumeElement.Volume * self.VolumeFraction_Liquid
		self.GenericDenominatorforCalculatingFractioninPhases["Chem_Benzo_g_h_i_perylene"]=self.containingVolumeElement.Volume * self.VolumeFraction_Solid * self.Chemical_Kd * self.rho * self.Constants.m3_per_L + self.containingVolumeElement.Volume * self.VolumeFraction_Liquid
		self.GenericDenominatorforCalculatingFractioninPhases["Chem_Benzo_k_fluoranthene"]=self.containingVolumeElement.Volume * self.VolumeFraction_Solid * self.Chemical_Kd * self.rho * self.Constants.m3_per_L + self.containingVolumeElement.Volume * self.VolumeFraction_Liquid
		self.GenericDenominatorforCalculatingFractioninPhases["Chem_Cadmium"]=self.containingVolumeElement.Volume * self.VolumeFraction_Solid * self.Chemical_Kd * self.rho * self.Constants.m3_per_L + self.containingVolumeElement.Volume * self.VolumeFraction_Liquid
		self.GenericDenominatorforCalculatingFractioninPhases["Chem_Chrysene"]=self.containingVolumeElement.Volume * self.VolumeFraction_Solid * self.Chemical_Kd * self.rho * self.Constants.m3_per_L + self.containingVolumeElement.Volume * self.VolumeFraction_Liquid
		self.GenericDenominatorforCalculatingFractioninPhases["Chem_Dibenz_a_h_anthracene"]=self.containingVolumeElement.Volume * self.VolumeFraction_Solid * self.Chemical_Kd * self.rho * self.Constants.m3_per_L + self.containingVolumeElement.Volume * self.VolumeFraction_Liquid
		self.GenericDenominatorforCalculatingFractioninPhases["Chem_Divalent_Mercury"]=self.containingVolumeElement.Volume * self.VolumeFraction_Solid * self.Chemical_Kd * self.rho * self.Constants.m3_per_L + self.containingVolumeElement.Volume * self.VolumeFraction_Liquid
		self.GenericDenominatorforCalculatingFractioninPhases["Chem_Elemental_Mercury"]=self.containingVolumeElement.Volume * self.VolumeFraction_Solid * self.Chemical_Kd * self.rho * self.Constants.m3_per_L + self.containingVolumeElement.Volume * self.VolumeFraction_Liquid
		self.GenericDenominatorforCalculatingFractioninPhases["Chem_Fluoranthene"]=self.containingVolumeElement.Volume * self.VolumeFraction_Solid * self.Chemical_Kd * self.rho * self.Constants.m3_per_L + self.containingVolumeElement.Volume * self.VolumeFraction_Liquid
		self.GenericDenominatorforCalculatingFractioninPhases["Chem_Fluorene"]=self.containingVolumeElement.Volume * self.VolumeFraction_Solid * self.Chemical_Kd * self.rho * self.Constants.m3_per_L + self.containingVolumeElement.Volume * self.VolumeFraction_Liquid
		self.GenericDenominatorforCalculatingFractioninPhases["Chem_Indeno_1_2_3_cd_pyrene"]=self.containingVolumeElement.Volume * self.VolumeFraction_Solid * self.Chemical_Kd * self.rho * self.Constants.m3_per_L + self.containingVolumeElement.Volume * self.VolumeFraction_Liquid
		self.GenericDenominatorforCalculatingFractioninPhases["Chem_Lead"]=self.containingVolumeElement.Volume * self.VolumeFraction_Solid * self.Chemical_Kd * self.rho * self.Constants.m3_per_L + self.containingVolumeElement.Volume * self.VolumeFraction_Liquid
		self.GenericDenominatorforCalculatingFractioninPhases["Chem_MethylMercury"]=self.containingVolumeElement.Volume * self.VolumeFraction_Solid * self.Chemical_Kd * self.rho * self.Constants.m3_per_L + self.containingVolumeElement.Volume * self.VolumeFraction_Liquid
		try:
			self.Chemical_GenericDenominatorforCalculatingFractioninPhases=self.GenericDenominatorforCalculatingFractioninPhases[self.currentChemical.Name]
		except:
			self.Chemical_GenericDenominatorforCalculatingFractioninPhases=nan

		self.Height=()
		self.Height=containingVolumeElement.Height

		self.Volume=()
		self.Volume=containingVolumeElement.Volume

		self.VolumeFraction_Solid=()
		self.VolumeFraction_Solid=1 - self.VolumeFraction_Liquid

		self.concentrationOutputFactor=()
		self.concentrationOutputFactor=1000/(self.VolumeFraction_Solid * self.rho)

		self.initialConcentration_g_per_m3={}
		self.initialConcentration_g_per_m3["Chem_1_2_3_4_6_7_8_9_OCDD"]=self.containingScenario.FractionInitialConcentrations * self.Chemical_initialConcentration_g_per_m3_UserSupplied
		self.initialConcentration_g_per_m3["Chem_1_2_3_4_6_7_8_9_OCDF"]=self.containingScenario.FractionInitialConcentrations * self.Chemical_initialConcentration_g_per_m3_UserSupplied
		self.initialConcentration_g_per_m3["Chem_1_2_3_4_6_7_8_HpCDD"]=self.containingScenario.FractionInitialConcentrations * self.Chemical_initialConcentration_g_per_m3_UserSupplied
		self.initialConcentration_g_per_m3["Chem_1_2_3_4_6_7_8_HpCDF"]=self.containingScenario.FractionInitialConcentrations * self.Chemical_initialConcentration_g_per_m3_UserSupplied
		self.initialConcentration_g_per_m3["Chem_1_2_3_4_7_8_9_HpCDF"]=self.containingScenario.FractionInitialConcentrations * self.Chemical_initialConcentration_g_per_m3_UserSupplied
		self.initialConcentration_g_per_m3["Chem_1_2_3_4_7_8_HxCDD"]=self.containingScenario.FractionInitialConcentrations * self.Chemical_initialConcentration_g_per_m3_UserSupplied
		self.initialConcentration_g_per_m3["Chem_1_2_3_4_7_8_HxCDF"]=self.containingScenario.FractionInitialConcentrations * self.Chemical_initialConcentration_g_per_m3_UserSupplied
		self.initialConcentration_g_per_m3["Chem_1_2_3_6_7_8_HxCDD"]=self.containingScenario.FractionInitialConcentrations * self.Chemical_initialConcentration_g_per_m3_UserSupplied
		self.initialConcentration_g_per_m3["Chem_1_2_3_6_7_8_HxCDF"]=self.containingScenario.FractionInitialConcentrations * self.Chemical_initialConcentration_g_per_m3_UserSupplied
		self.initialConcentration_g_per_m3["Chem_1_2_3_7_8_9_HxCDD"]=self.containingScenario.FractionInitialConcentrations * self.Chemical_initialConcentration_g_per_m3_UserSupplied
		self.initialConcentration_g_per_m3["Chem_1_2_3_7_8_9_HxCDF"]=self.containingScenario.FractionInitialConcentrations * self.Chemical_initialConcentration_g_per_m3_UserSupplied
		self.initialConcentration_g_per_m3["Chem_1_2_3_7_8_PeCDD"]=self.containingScenario.FractionInitialConcentrations * self.Chemical_initialConcentration_g_per_m3_UserSupplied
		self.initialConcentration_g_per_m3["Chem_1_2_3_7_8_PeCDF"]=self.containingScenario.FractionInitialConcentrations * self.Chemical_initialConcentration_g_per_m3_UserSupplied
		self.initialConcentration_g_per_m3["Chem_2_3_4_6_7_8_HxCDF"]=self.containingScenario.FractionInitialConcentrations * self.Chemical_initialConcentration_g_per_m3_UserSupplied
		self.initialConcentration_g_per_m3["Chem_2_3_4_7_8_PeCDF"]=self.containingScenario.FractionInitialConcentrations * self.Chemical_initialConcentration_g_per_m3_UserSupplied
		self.initialConcentration_g_per_m3["Chem_2_3_7_8_TCDD"]=self.containingScenario.FractionInitialConcentrations * self.Chemical_initialConcentration_g_per_m3_UserSupplied
		self.initialConcentration_g_per_m3["Chem_2_3_7_8_TCDF"]=self.containingScenario.FractionInitialConcentrations * self.Chemical_initialConcentration_g_per_m3_UserSupplied
		self.initialConcentration_g_per_m3["Chem_2_Methylnaphthalene"]=self.containingScenario.FractionInitialConcentrations * self.Chemical_initialConcentration_g_per_m3_UserSupplied
		self.initialConcentration_g_per_m3["Chem_7_12_Dimethylbenz_a_anthracene"]=self.containingScenario.FractionInitialConcentrations * self.Chemical_initialConcentration_g_per_m3_UserSupplied
		self.initialConcentration_g_per_m3["Chem_Acenaphthene"]=self.containingScenario.FractionInitialConcentrations * self.Chemical_initialConcentration_g_per_m3_UserSupplied
		self.initialConcentration_g_per_m3["Chem_Acenaphthylene"]=self.containingScenario.FractionInitialConcentrations * self.Chemical_initialConcentration_g_per_m3_UserSupplied
		self.initialConcentration_g_per_m3["Chem_Benz_a_anthracene"]=self.containingScenario.FractionInitialConcentrations * self.Chemical_initialConcentration_g_per_m3_UserSupplied
		self.initialConcentration_g_per_m3["Chem_Benzo_A_Pyrene"]=self.containingScenario.FractionInitialConcentrations * self.Chemical_initialConcentration_g_per_m3_UserSupplied
		self.initialConcentration_g_per_m3["Chem_Benzo_b_fluoranthene"]=self.containingScenario.FractionInitialConcentrations * self.Chemical_initialConcentration_g_per_m3_UserSupplied
		self.initialConcentration_g_per_m3["Chem_Benzo_g_h_i_perylene"]=self.containingScenario.FractionInitialConcentrations * self.Chemical_initialConcentration_g_per_m3_UserSupplied
		self.initialConcentration_g_per_m3["Chem_Benzo_k_fluoranthene"]=self.containingScenario.FractionInitialConcentrations * self.Chemical_initialConcentration_g_per_m3_UserSupplied
		self.initialConcentration_g_per_m3["Chem_Chrysene"]=self.containingScenario.FractionInitialConcentrations * self.Chemical_initialConcentration_g_per_m3_UserSupplied
		self.initialConcentration_g_per_m3["Chem_Dibenz_a_h_anthracene"]=self.containingScenario.FractionInitialConcentrations * self.Chemical_initialConcentration_g_per_m3_UserSupplied
		self.initialConcentration_g_per_m3["Chem_Divalent_Mercury"]=self.containingScenario.FractionInitialConcentrations * self.Chemical_initialConcentration_g_per_m3_UserSupplied
		self.initialConcentration_g_per_m3["Chem_Elemental_Mercury"]=self.containingScenario.FractionInitialConcentrations * self.Chemical_initialConcentration_g_per_m3_UserSupplied
		self.initialConcentration_g_per_m3["Chem_Fluoranthene"]=self.containingScenario.FractionInitialConcentrations * self.Chemical_initialConcentration_g_per_m3_UserSupplied
		self.initialConcentration_g_per_m3["Chem_Fluorene"]=self.containingScenario.FractionInitialConcentrations * self.Chemical_initialConcentration_g_per_m3_UserSupplied
		self.initialConcentration_g_per_m3["Chem_Indeno_1_2_3_cd_pyrene"]=self.containingScenario.FractionInitialConcentrations * self.Chemical_initialConcentration_g_per_m3_UserSupplied
		self.initialConcentration_g_per_m3["Chem_MethylMercury"]=self.containingScenario.FractionInitialConcentrations * self.Chemical_initialConcentration_g_per_m3_UserSupplied
		try:
			self.Chemical_initialConcentration_g_per_m3=self.initialConcentration_g_per_m3[self.currentChemical.Name]
		except:
			self.Chemical_initialConcentration_g_per_m3=nan

		self.totalMass=()
		self.totalMass=self.containingVolumeElement.Volume*(self.VolumeFraction_Solid*self.rho + self.VolumeFraction_Liquid*self.Constants.kg_per_m3_Water)

		self.wetConcOutputFactor=()
		self.wetConcOutputFactor=(self.VolumeFraction_Solid * self.rho) / (self.VolumeFraction_Solid * self.rho + self.VolumeFraction_Liquid * self.Constants.kg_per_m3_Water)

class Sediment_Burial_Sink:
	def __init__(self,Constants,containingScenario,currentChemical,containingVolumeElement):
		self.containingScenario=containingScenario
		self.currentChemical=currentChemical
		self.Constants=Constants
		self.containingVolumeElement=containingVolumeElement
		
		self.acceptableAbiotic=()
		self.acceptableAbiotic='nan'

		self.category=()
		self.category='Sink | Abiotic | Sediment | Sediment - Default'

		self.concentrationOutputUnits=()
		self.concentrationOutputUnits='0.01'

		self.isBiotic=()
		self.isBiotic=False

		self.concentrationOutputFactor=()
		self.concentrationOutputFactor=1.0

		self.VolumeFraction_Liquid={}
		try:
			self.Chemical_VolumeFraction_Liquid=self.VolumeFraction_Liquid[self.currentChemical.Name]
		except:
			self.Chemical_VolumeFraction_Liquid=nan

		self.VolumeFraction_Solid={}
		try:
			self.Chemical_VolumeFraction_Solid=self.VolumeFraction_Solid[self.currentChemical.Name]
		except:
			self.Chemical_VolumeFraction_Solid=nan

		self.GenericDenominatorforCalculatingFractioninPhases={}
		try:
			self.Chemical_GenericDenominatorforCalculatingFractioninPhases=self.GenericDenominatorforCalculatingFractioninPhases[self.currentChemical.Name]
		except:
			self.Chemical_GenericDenominatorforCalculatingFractioninPhases=nan

class Surface_water:
	def __init__(self,Constants,containingScenario,currentChemical,containingVolumeElement):
		self.containingScenario=containingScenario
		self.currentChemical=currentChemical
		self.Constants=Constants
		self.containingVolumeElement=containingVolumeElement
		
		self.acceptableAbiotic=()
		self.acceptableAbiotic='nan'

		self.category=()
		self.category='Abiotic | Surface water | Surface water - Default'

		self.concentrationOutputUnits=()
		self.concentrationOutputUnits='mg/L'

		self.isBiotic=()
		self.isBiotic=False

		self.isFlowing=()
		self.isFlowing=False

		self.AlgaeCarbonContentDryWt=()
		self.AlgaeCarbonContentDryWt=0.465

		self.AlgaeDensity_g_m3=()
		self.AlgaeDensity_g_m3=1000000.0

		self.AlgaeDensityinWaterColumn_g_L=()
		self.AlgaeDensityinWaterColumn_g_L=0.01

		self.AlgaeGrowthRate=()
		self.AlgaeGrowthRate=0.7

		self.AlgaeRadius=()
		self.AlgaeRadius=2.5

		self.AlgaeUptakeRate={}
		self.AlgaeUptakeRate["Chem_Divalent_Mercury"]=2.04E-10
		self.AlgaeUptakeRate["Chem_Elemental_Mercury"]=0.0
		self.AlgaeUptakeRate["Chem_MethylMercury"]=3.6E-10
		try:
			self.Chemical_AlgaeUptakeRate=self.AlgaeUptakeRate[self.currentChemical.Name]
		except:
			self.Chemical_AlgaeUptakeRate=nan

		self.AlgaeWaterContent=()
		self.AlgaeWaterContent=0.9

		self.BoundaryLayerThicknessAboveSediment=()
		self.BoundaryLayerThicknessAboveSediment=0.02

		self.ChlorideConcentration_mg_L=()
		self.ChlorideConcentration_mg_L=0.01

		self.ChlorophyllConcentration_mg_L=()
		self.ChlorophyllConcentration_mg_L=0.01

		self.CurrentVelocity=()
		self.CurrentVelocity=0.01

		self.DemethylationRate={}
		self.DemethylationRate["Chem_MethylMercury"]=0.013
		try:
			self.Chemical_DemethylationRate=self.DemethylationRate[self.currentChemical.Name]
		except:
			self.Chemical_DemethylationRate=nan

		self.DimensionlessViscousSublayerThickness=()
		self.DimensionlessViscousSublayerThickness=4.0

		self.DragCoefficient=()
		self.DragCoefficient=0.0011

		self.Flushes_per_year=()
		self.Flushes_per_year=0.01

		self.FractionSand=()
		self.FractionSand=0.25

		self.HalfLife={}
		self.HalfLife["Chem_1_2_3_4_6_7_8_9_OCDD"]=0.67
		self.HalfLife["Chem_1_2_3_4_6_7_8_9_OCDF"]=0.58
		self.HalfLife["Chem_1_2_3_4_6_7_8_HpCDD"]=47.0
		self.HalfLife["Chem_1_2_3_4_6_7_8_HpCDF"]=0.58
		self.HalfLife["Chem_1_2_3_4_7_8_9_HpCDF"]=0.58
		self.HalfLife["Chem_1_2_3_4_7_8_HxCDD"]=6.3
		self.HalfLife["Chem_1_2_3_4_7_8_HxCDF"]=0.58
		self.HalfLife["Chem_1_2_3_6_7_8_HxCDD"]=6.3
		self.HalfLife["Chem_1_2_3_6_7_8_HxCDF"]=0.58
		self.HalfLife["Chem_1_2_3_7_8_9_HxCDD"]=6.3
		self.HalfLife["Chem_1_2_3_7_8_9_HxCDF"]=0.58
		self.HalfLife["Chem_1_2_3_7_8_PeCDD"]=2.7
		self.HalfLife["Chem_1_2_3_7_8_PeCDF"]=0.19
		self.HalfLife["Chem_2_3_4_6_7_8_HxCDF"]=0.58
		self.HalfLife["Chem_2_3_4_7_8_PeCDF"]=0.19
		self.HalfLife["Chem_2_3_7_8_TCDD"]=2.7
		self.HalfLife["Chem_2_3_7_8_TCDF"]=0.18
		self.HalfLife["Chem_2_Methylnaphthalene"]=78.0
		self.HalfLife["Chem_7_12_Dimethylbenz_a_anthracene"]=216.0
		self.HalfLife["Chem_Acenaphthene"]=25.0
		self.HalfLife["Chem_Acenaphthylene"]=184.0
		self.HalfLife["Chem_Benz_a_anthracene"]=0.375
		self.HalfLife["Chem_Benzo_A_Pyrene"]=0.138
		self.HalfLife["Chem_Benzo_b_fluoranthene"]=90.0
		self.HalfLife["Chem_Benzo_g_h_i_perylene"]=1670.0
		self.HalfLife["Chem_Benzo_k_fluoranthene"]=62.4
		self.HalfLife["Chem_Chrysene"]=1.626
		self.HalfLife["Chem_Dibenz_a_h_anthracene"]=97.8
		self.HalfLife["Chem_Fluoranthene"]=160.0
		self.HalfLife["Chem_Fluorene"]=8.5
		self.HalfLife["Chem_Indeno_1_2_3_cd_pyrene"]=750.0
		try:
			self.Chemical_HalfLife=self.HalfLife[self.currentChemical.Name]
		except:
			self.Chemical_HalfLife=nan

		self.MethylationRate={}
		self.MethylationRate["Chem_Divalent_Mercury"]=0.001
		try:
			self.Chemical_MethylationRate=self.MethylationRate[self.currentChemical.Name]
		except:
			self.Chemical_MethylationRate=nan

		self.OrganicCarbonContent=()
		self.OrganicCarbonContent=0.01

		self.OxidationRate={}
		self.OxidationRate["Chem_Elemental_Mercury"]=0.0
		try:
			self.Chemical_OxidationRate=self.OxidationRate[self.currentChemical.Name]
		except:
			self.Chemical_OxidationRate=nan

		self.ReductionRate={}
		self.ReductionRate["Chem_Divalent_Mercury"]=0.0075
		try:
			self.Chemical_ReductionRate=self.ReductionRate[self.currentChemical.Name]
		except:
			self.Chemical_ReductionRate=nan

		self.SedimentDepositionVelocity=()
		self.SedimentDepositionVelocity=2.0

		self.SuspendedSedimentconcentration=()
		self.SuspendedSedimentconcentration=0.01

		self.VaporDryDepositionVelocity_m_day={}
		self.VaporDryDepositionVelocity_m_day["Chem_Divalent_Mercury"]=2500.0
		try:
			self.Chemical_VaporDryDepositionVelocity_m_day=self.VaporDryDepositionVelocity_m_day[self.currentChemical.Name]
		except:
			self.Chemical_VaporDryDepositionVelocity_m_day=nan

		self.WaterTemperature_K=()
		self.WaterTemperature_K=0.01

		self.concentrationOutputFactor=()
		self.concentrationOutputFactor=1000.0

		self.initialConcentration_g_per_L_UserSupplied={}
		self.initialConcentration_g_per_L_UserSupplied["Chem_1_2_3_4_6_7_8_9_OCDD"]=0.0
		self.initialConcentration_g_per_L_UserSupplied["Chem_1_2_3_4_6_7_8_9_OCDF"]=0.0
		self.initialConcentration_g_per_L_UserSupplied["Chem_1_2_3_4_6_7_8_HpCDD"]=0.0
		self.initialConcentration_g_per_L_UserSupplied["Chem_1_2_3_4_6_7_8_HpCDF"]=0.0
		self.initialConcentration_g_per_L_UserSupplied["Chem_1_2_3_4_7_8_9_HpCDF"]=0.0
		self.initialConcentration_g_per_L_UserSupplied["Chem_1_2_3_4_7_8_HxCDD"]=0.0
		self.initialConcentration_g_per_L_UserSupplied["Chem_1_2_3_4_7_8_HxCDF"]=0.0
		self.initialConcentration_g_per_L_UserSupplied["Chem_1_2_3_6_7_8_HxCDD"]=0.0
		self.initialConcentration_g_per_L_UserSupplied["Chem_1_2_3_6_7_8_HxCDF"]=0.0
		self.initialConcentration_g_per_L_UserSupplied["Chem_1_2_3_7_8_9_HxCDD"]=0.0
		self.initialConcentration_g_per_L_UserSupplied["Chem_1_2_3_7_8_9_HxCDF"]=0.0
		self.initialConcentration_g_per_L_UserSupplied["Chem_1_2_3_7_8_PeCDD"]=0.0
		self.initialConcentration_g_per_L_UserSupplied["Chem_1_2_3_7_8_PeCDF"]=0.0
		self.initialConcentration_g_per_L_UserSupplied["Chem_2_3_4_6_7_8_HxCDF"]=0.0
		self.initialConcentration_g_per_L_UserSupplied["Chem_2_3_4_7_8_PeCDF"]=0.0
		self.initialConcentration_g_per_L_UserSupplied["Chem_2_3_7_8_TCDD"]=0.0
		self.initialConcentration_g_per_L_UserSupplied["Chem_2_3_7_8_TCDF"]=0.0
		self.initialConcentration_g_per_L_UserSupplied["Chem_2_Methylnaphthalene"]=0.0
		self.initialConcentration_g_per_L_UserSupplied["Chem_7_12_Dimethylbenz_a_anthracene"]=0.0
		self.initialConcentration_g_per_L_UserSupplied["Chem_Acenaphthene"]=0.0
		self.initialConcentration_g_per_L_UserSupplied["Chem_Acenaphthylene"]=0.0
		self.initialConcentration_g_per_L_UserSupplied["Chem_Arsenic"]=0.0
		self.initialConcentration_g_per_L_UserSupplied["Chem_Benz_a_anthracene"]=0.0
		self.initialConcentration_g_per_L_UserSupplied["Chem_Benzo_A_Pyrene"]=0.0
		self.initialConcentration_g_per_L_UserSupplied["Chem_Benzo_b_fluoranthene"]=0.0
		self.initialConcentration_g_per_L_UserSupplied["Chem_Benzo_g_h_i_perylene"]=0.0
		self.initialConcentration_g_per_L_UserSupplied["Chem_Benzo_k_fluoranthene"]=0.0
		self.initialConcentration_g_per_L_UserSupplied["Chem_Cadmium"]=0.0
		self.initialConcentration_g_per_L_UserSupplied["Chem_Chrysene"]=0.0
		self.initialConcentration_g_per_L_UserSupplied["Chem_Dibenz_a_h_anthracene"]=0.0
		self.initialConcentration_g_per_L_UserSupplied["Chem_Divalent_Mercury"]=0.0
		self.initialConcentration_g_per_L_UserSupplied["Chem_Elemental_Mercury"]=0.0
		self.initialConcentration_g_per_L_UserSupplied["Chem_Fluoranthene"]=0.0
		self.initialConcentration_g_per_L_UserSupplied["Chem_Fluorene"]=0.0
		self.initialConcentration_g_per_L_UserSupplied["Chem_Indeno_1_2_3_cd_pyrene"]=0.0
		self.initialConcentration_g_per_L_UserSupplied["Chem_MethylMercury"]=0.0
		try:
			self.Chemical_initialConcentration_g_per_L_UserSupplied=self.initialConcentration_g_per_L_UserSupplied[self.currentChemical.Name]
		except:
			self.Chemical_initialConcentration_g_per_L_UserSupplied=nan

		self.pH=()
		self.pH=0.01

		self.rho=()
		self.rho=2600.0

		self.AlgaeDensity_g_um3=()
		self.AlgaeDensity_g_um3=self.AlgaeDensity_g_m3 / self.Constants.um3_per_m3

		self.ChlorideConcentration_mg_m3=()
		self.ChlorideConcentration_mg_m3=0.01

		self.ChlorophyllConcentration_mg_m3=()
		self.ChlorophyllConcentration_mg_m3=self.ChlorophyllConcentration_mg_L*self.Constants.L_per_m3

		self.D_effective={}
		self.D_effective["Chem_1_2_3_4_6_7_8_9_OCDD"]=self.currentChemical.D_purewater
		self.D_effective["Chem_1_2_3_4_6_7_8_9_OCDF"]=self.currentChemical.D_purewater
		self.D_effective["Chem_1_2_3_4_6_7_8_HpCDD"]=self.currentChemical.D_purewater
		self.D_effective["Chem_1_2_3_4_6_7_8_HpCDF"]=self.currentChemical.D_purewater
		self.D_effective["Chem_1_2_3_4_7_8_9_HpCDF"]=self.currentChemical.D_purewater
		self.D_effective["Chem_1_2_3_4_7_8_HxCDD"]=self.currentChemical.D_purewater
		self.D_effective["Chem_1_2_3_4_7_8_HxCDF"]=self.currentChemical.D_purewater
		self.D_effective["Chem_1_2_3_6_7_8_HxCDD"]=self.currentChemical.D_purewater
		self.D_effective["Chem_1_2_3_6_7_8_HxCDF"]=self.currentChemical.D_purewater
		self.D_effective["Chem_1_2_3_7_8_9_HxCDD"]=self.currentChemical.D_purewater
		self.D_effective["Chem_1_2_3_7_8_9_HxCDF"]=self.currentChemical.D_purewater
		self.D_effective["Chem_1_2_3_7_8_PeCDD"]=self.currentChemical.D_purewater
		self.D_effective["Chem_1_2_3_7_8_PeCDF"]=self.currentChemical.D_purewater
		self.D_effective["Chem_2_3_4_6_7_8_HxCDF"]=self.currentChemical.D_purewater
		self.D_effective["Chem_2_3_4_7_8_PeCDF"]=self.currentChemical.D_purewater
		self.D_effective["Chem_2_3_7_8_TCDD"]=self.currentChemical.D_purewater
		self.D_effective["Chem_2_3_7_8_TCDF"]=self.currentChemical.D_purewater
		self.D_effective["Chem_2_Methylnaphthalene"]=self.currentChemical.D_purewater
		self.D_effective["Chem_7_12_Dimethylbenz_a_anthracene"]=self.currentChemical.D_purewater
		self.D_effective["Chem_Acenaphthene"]=self.currentChemical.D_purewater
		self.D_effective["Chem_Acenaphthylene"]=self.currentChemical.D_purewater
		self.D_effective["Chem_Arsenic"]=self.currentChemical.D_purewater
		self.D_effective["Chem_Benz_a_anthracene"]=self.currentChemical.D_purewater
		self.D_effective["Chem_Benzo_A_Pyrene"]=self.currentChemical.D_purewater
		self.D_effective["Chem_Benzo_b_fluoranthene"]=self.currentChemical.D_purewater
		self.D_effective["Chem_Benzo_g_h_i_perylene"]=self.currentChemical.D_purewater
		self.D_effective["Chem_Benzo_k_fluoranthene"]=self.currentChemical.D_purewater
		self.D_effective["Chem_Cadmium"]=self.currentChemical.D_purewater
		self.D_effective["Chem_Chrysene"]=self.currentChemical.D_purewater
		self.D_effective["Chem_Dibenz_a_h_anthracene"]=self.currentChemical.D_purewater
		self.D_effective["Chem_Divalent_Mercury"]=self.currentChemical.D_purewater
		self.D_effective["Chem_Elemental_Mercury"]=self.currentChemical.D_purewater
		self.D_effective["Chem_Fluoranthene"]=self.currentChemical.D_purewater
		self.D_effective["Chem_Fluorene"]=self.currentChemical.D_purewater
		self.D_effective["Chem_Indeno_1_2_3_cd_pyrene"]=self.currentChemical.D_purewater
		self.D_effective["Chem_Lead"]=self.currentChemical.D_purewater
		self.D_effective["Chem_MethylMercury"]=self.currentChemical.D_purewater
		try:
			self.Chemical_D_effective=self.D_effective[self.currentChemical.Name]
		except:
			self.Chemical_D_effective=nan

		self.D_ow={}
		self.D_ow["Chem_1_2_3_4_6_7_8_9_OCDD"]=0.0
		self.D_ow["Chem_1_2_3_4_6_7_8_9_OCDF"]=0.0
		self.D_ow["Chem_1_2_3_4_6_7_8_HpCDD"]=0.0
		self.D_ow["Chem_1_2_3_4_6_7_8_HpCDF"]=0.0
		self.D_ow["Chem_1_2_3_4_7_8_9_HpCDF"]=0.0
		self.D_ow["Chem_1_2_3_4_7_8_HxCDD"]=0.0
		self.D_ow["Chem_1_2_3_4_7_8_HxCDF"]=0.0
		self.D_ow["Chem_1_2_3_6_7_8_HxCDD"]=0.0
		self.D_ow["Chem_1_2_3_6_7_8_HxCDF"]=0.0
		self.D_ow["Chem_1_2_3_7_8_9_HxCDD"]=0.0
		self.D_ow["Chem_1_2_3_7_8_9_HxCDF"]=0.0
		self.D_ow["Chem_1_2_3_7_8_PeCDD"]=0.0
		self.D_ow["Chem_1_2_3_7_8_PeCDF"]=0.0
		self.D_ow["Chem_2_3_4_6_7_8_HxCDF"]=0.0
		self.D_ow["Chem_2_3_4_7_8_PeCDF"]=0.0
		self.D_ow["Chem_2_3_7_8_TCDD"]=0.0
		self.D_ow["Chem_2_3_7_8_TCDF"]=0.0
		self.D_ow["Chem_2_Methylnaphthalene"]=0.0
		self.D_ow["Chem_7_12_Dimethylbenz_a_anthracene"]=0.0
		self.D_ow["Chem_Acenaphthene"]=0.0
		self.D_ow["Chem_Acenaphthylene"]=0.0
		self.D_ow["Chem_Benz_a_anthracene"]=0.0
		self.D_ow["Chem_Benzo_A_Pyrene"]=0.0
		self.D_ow["Chem_Benzo_b_fluoranthene"]=0.0
		self.D_ow["Chem_Benzo_g_h_i_perylene"]=0.0
		self.D_ow["Chem_Benzo_k_fluoranthene"]=0.0
		self.D_ow["Chem_Chrysene"]=0.0
		self.D_ow["Chem_Dibenz_a_h_anthracene"]=0.0
		self.D_ow["Chem_Divalent_Mercury"]=0.01
		self.D_ow["Chem_Elemental_Mercury"]=0.0
		self.D_ow["Chem_Fluoranthene"]=0.0
		self.D_ow["Chem_Fluorene"]=0.0
		self.D_ow["Chem_Indeno_1_2_3_cd_pyrene"]=0.0
		self.D_ow["Chem_Lead"]=self.currentChemical.K_ow
		self.D_ow["Chem_MethylMercury"]=0.01
		try:
			self.Chemical_D_ow=self.D_ow[self.currentChemical.Name]
		except:
			self.Chemical_D_ow=nan

		self.D_owforHg2_ph4={}
		self.D_owforHg2_ph4["Chem_Divalent_Mercury"]=0.01
		try:
			self.Chemical_D_owforHg2_ph4=self.D_owforHg2_ph4[self.currentChemical.Name]
		except:
			self.Chemical_D_owforHg2_ph4=nan

		self.D_owforHg2_ph5={}
		self.D_owforHg2_ph5["Chem_Divalent_Mercury"]=0.01
		try:
			self.Chemical_D_owforHg2_ph5=self.D_owforHg2_ph5[self.currentChemical.Name]
		except:
			self.Chemical_D_owforHg2_ph5=nan

		self.D_owforHg2_ph6={}
		self.D_owforHg2_ph6["Chem_Divalent_Mercury"]=0.01
		try:
			self.Chemical_D_owforHg2_ph6=self.D_owforHg2_ph6[self.currentChemical.Name]
		except:
			self.Chemical_D_owforHg2_ph6=nan

		self.D_owforHg2_ph7={}
		self.D_owforHg2_ph7["Chem_Divalent_Mercury"]=0.01
		try:
			self.Chemical_D_owforHg2_ph7=self.D_owforHg2_ph7[self.currentChemical.Name]
		except:
			self.Chemical_D_owforHg2_ph7=nan

		self.D_owforHg2_ph8={}
		self.D_owforHg2_ph8["Chem_Divalent_Mercury"]=0.01
		try:
			self.Chemical_D_owforHg2_ph8=self.D_owforHg2_ph8[self.currentChemical.Name]
		except:
			self.Chemical_D_owforHg2_ph8=nan

		self.D_owforMHg_ph4={}
		self.D_owforMHg_ph4["Chem_MethylMercury"]=0.01
		try:
			self.Chemical_D_owforMHg_ph4=self.D_owforMHg_ph4[self.currentChemical.Name]
		except:
			self.Chemical_D_owforMHg_ph4=nan

		self.D_owforMHg_ph5={}
		self.D_owforMHg_ph5["Chem_MethylMercury"]=0.01
		try:
			self.Chemical_D_owforMHg_ph5=self.D_owforMHg_ph5[self.currentChemical.Name]
		except:
			self.Chemical_D_owforMHg_ph5=nan

		self.D_owforMHg_ph6={}
		self.D_owforMHg_ph6["Chem_MethylMercury"]=0.01
		try:
			self.Chemical_D_owforMHg_ph6=self.D_owforMHg_ph6[self.currentChemical.Name]
		except:
			self.Chemical_D_owforMHg_ph6=nan

		self.D_owforMHg_ph7={}
		self.D_owforMHg_ph7["Chem_MethylMercury"]=0.01
		try:
			self.Chemical_D_owforMHg_ph7=self.D_owforMHg_ph7[self.currentChemical.Name]
		except:
			self.Chemical_D_owforMHg_ph7=nan

		self.D_owforMHg_ph8={}
		self.D_owforMHg_ph8["Chem_MethylMercury"]=0.01
		try:
			self.Chemical_D_owforMHg_ph8=self.D_owforMHg_ph8[self.currentChemical.Name]
		except:
			self.Chemical_D_owforMHg_ph8=nan

		self.GeneralDegradationRate={}
		self.GeneralDegradationRate["Chem_1_2_3_4_6_7_8_9_OCDD"]=log(2)/ self.Chemical_HalfLife
		self.GeneralDegradationRate["Chem_1_2_3_4_6_7_8_9_OCDF"]=log(2)/ self.Chemical_HalfLife
		self.GeneralDegradationRate["Chem_1_2_3_4_6_7_8_HpCDD"]=log(2)/ self.Chemical_HalfLife
		self.GeneralDegradationRate["Chem_1_2_3_4_6_7_8_HpCDF"]=log(2)/ self.Chemical_HalfLife
		self.GeneralDegradationRate["Chem_1_2_3_4_7_8_9_HpCDF"]=log(2)/ self.Chemical_HalfLife
		self.GeneralDegradationRate["Chem_1_2_3_4_7_8_HxCDD"]=log(2)/ self.Chemical_HalfLife
		self.GeneralDegradationRate["Chem_1_2_3_4_7_8_HxCDF"]=log(2)/ self.Chemical_HalfLife
		self.GeneralDegradationRate["Chem_1_2_3_6_7_8_HxCDD"]=log(2)/ self.Chemical_HalfLife
		self.GeneralDegradationRate["Chem_1_2_3_6_7_8_HxCDF"]=log(2)/ self.Chemical_HalfLife
		self.GeneralDegradationRate["Chem_1_2_3_7_8_9_HxCDD"]=log(2)/ self.Chemical_HalfLife
		self.GeneralDegradationRate["Chem_1_2_3_7_8_9_HxCDF"]=log(2)/ self.Chemical_HalfLife
		self.GeneralDegradationRate["Chem_1_2_3_7_8_PeCDD"]=log(2)/ self.Chemical_HalfLife
		self.GeneralDegradationRate["Chem_1_2_3_7_8_PeCDF"]=log(2)/ self.Chemical_HalfLife
		self.GeneralDegradationRate["Chem_2_3_4_6_7_8_HxCDF"]=log(2)/ self.Chemical_HalfLife
		self.GeneralDegradationRate["Chem_2_3_4_7_8_PeCDF"]=log(2)/ self.Chemical_HalfLife
		self.GeneralDegradationRate["Chem_2_3_7_8_TCDD"]=log(2)/ self.Chemical_HalfLife
		self.GeneralDegradationRate["Chem_2_3_7_8_TCDF"]=log(2)/ self.Chemical_HalfLife
		self.GeneralDegradationRate["Chem_2_Methylnaphthalene"]=log(2)/ self.Chemical_HalfLife
		self.GeneralDegradationRate["Chem_7_12_Dimethylbenz_a_anthracene"]=log(2)/ self.Chemical_HalfLife
		self.GeneralDegradationRate["Chem_Acenaphthene"]=log(2)/ self.Chemical_HalfLife
		self.GeneralDegradationRate["Chem_Acenaphthylene"]=log(2)/ self.Chemical_HalfLife
		self.GeneralDegradationRate["Chem_Benz_a_anthracene"]=log(2)/ self.Chemical_HalfLife
		self.GeneralDegradationRate["Chem_Benzo_A_Pyrene"]=log(2)/ self.Chemical_HalfLife
		self.GeneralDegradationRate["Chem_Benzo_b_fluoranthene"]=log(2)/ self.Chemical_HalfLife
		self.GeneralDegradationRate["Chem_Benzo_g_h_i_perylene"]=log(2)/ self.Chemical_HalfLife
		self.GeneralDegradationRate["Chem_Benzo_k_fluoranthene"]=log(2)/ self.Chemical_HalfLife
		self.GeneralDegradationRate["Chem_Chrysene"]=log(2)/ self.Chemical_HalfLife
		self.GeneralDegradationRate["Chem_Dibenz_a_h_anthracene"]=log(2)/ self.Chemical_HalfLife
		self.GeneralDegradationRate["Chem_Fluoranthene"]=log(2)/ self.Chemical_HalfLife
		self.GeneralDegradationRate["Chem_Fluorene"]=log(2)/ self.Chemical_HalfLife
		self.GeneralDegradationRate["Chem_Indeno_1_2_3_cd_pyrene"]=log(2)/ self.Chemical_HalfLife
		try:
			self.Chemical_GeneralDegradationRate=self.GeneralDegradationRate[self.currentChemical.Name]
		except:
			self.Chemical_GeneralDegradationRate=nan

		self.Kd={}
		self.Kd["Chem_1_2_3_4_6_7_8_9_OCDD"]=self.currentChemical.K_oc * self.OrganicCarbonContent
		self.Kd["Chem_1_2_3_4_6_7_8_9_OCDF"]=self.currentChemical.K_oc * self.OrganicCarbonContent
		self.Kd["Chem_1_2_3_4_6_7_8_HpCDD"]=self.currentChemical.K_oc * self.OrganicCarbonContent
		self.Kd["Chem_1_2_3_4_6_7_8_HpCDF"]=self.currentChemical.K_oc * self.OrganicCarbonContent
		self.Kd["Chem_1_2_3_4_7_8_9_HpCDF"]=self.currentChemical.K_oc * self.OrganicCarbonContent
		self.Kd["Chem_1_2_3_4_7_8_HxCDD"]=self.currentChemical.K_oc * self.OrganicCarbonContent
		self.Kd["Chem_1_2_3_4_7_8_HxCDF"]=self.currentChemical.K_oc * self.OrganicCarbonContent
		self.Kd["Chem_1_2_3_6_7_8_HxCDD"]=self.currentChemical.K_oc * self.OrganicCarbonContent
		self.Kd["Chem_1_2_3_6_7_8_HxCDF"]=self.currentChemical.K_oc * self.OrganicCarbonContent
		self.Kd["Chem_1_2_3_7_8_9_HxCDD"]=self.currentChemical.K_oc * self.OrganicCarbonContent
		self.Kd["Chem_1_2_3_7_8_9_HxCDF"]=self.currentChemical.K_oc * self.OrganicCarbonContent
		self.Kd["Chem_1_2_3_7_8_PeCDD"]=self.currentChemical.K_oc * self.OrganicCarbonContent
		self.Kd["Chem_1_2_3_7_8_PeCDF"]=self.currentChemical.K_oc * self.OrganicCarbonContent
		self.Kd["Chem_2_3_4_6_7_8_HxCDF"]=self.currentChemical.K_oc * self.OrganicCarbonContent
		self.Kd["Chem_2_3_4_7_8_PeCDF"]=self.currentChemical.K_oc * self.OrganicCarbonContent
		self.Kd["Chem_2_3_7_8_TCDD"]=self.currentChemical.K_oc * self.OrganicCarbonContent
		self.Kd["Chem_2_3_7_8_TCDF"]=self.currentChemical.K_oc * self.OrganicCarbonContent
		self.Kd["Chem_2_Methylnaphthalene"]=self.currentChemical.K_oc * self.OrganicCarbonContent
		self.Kd["Chem_7_12_Dimethylbenz_a_anthracene"]=self.currentChemical.K_oc * self.OrganicCarbonContent
		self.Kd["Chem_Acenaphthene"]=self.currentChemical.K_oc * self.OrganicCarbonContent
		self.Kd["Chem_Acenaphthylene"]=self.currentChemical.K_oc * self.OrganicCarbonContent
		self.Kd["Chem_Arsenic"]=10000.0
		self.Kd["Chem_Benz_a_anthracene"]=self.currentChemical.K_oc * self.OrganicCarbonContent
		self.Kd["Chem_Benzo_A_Pyrene"]=self.currentChemical.K_oc * self.OrganicCarbonContent
		self.Kd["Chem_Benzo_b_fluoranthene"]=self.currentChemical.K_oc * self.OrganicCarbonContent
		self.Kd["Chem_Benzo_g_h_i_perylene"]=self.currentChemical.K_oc * self.OrganicCarbonContent
		self.Kd["Chem_Benzo_k_fluoranthene"]=self.currentChemical.K_oc * self.OrganicCarbonContent
		self.Kd["Chem_Cadmium"]=0.01
		self.Kd["Chem_Chrysene"]=self.currentChemical.K_oc * self.OrganicCarbonContent
		self.Kd["Chem_Dibenz_a_h_anthracene"]=self.currentChemical.K_oc * self.OrganicCarbonContent
		self.Kd["Chem_Divalent_Mercury"]=100000.0
		self.Kd["Chem_Elemental_Mercury"]=1000.0
		self.Kd["Chem_Fluoranthene"]=self.currentChemical.K_oc * self.OrganicCarbonContent
		self.Kd["Chem_Fluorene"]=self.currentChemical.K_oc * self.OrganicCarbonContent
		self.Kd["Chem_Indeno_1_2_3_cd_pyrene"]=self.currentChemical.K_oc * self.OrganicCarbonContent
		self.Kd["Chem_Lead"]=0.01
		self.Kd["Chem_MethylMercury"]=100000.0
		try:
			self.Chemical_Kd=self.Kd[self.currentChemical.Name]
		except:
			self.Chemical_Kd=nan

		self.SedimentDepositionRate_kg_m2_day=()
		self.SedimentDepositionRate_kg_m2_day=self.SedimentDepositionVelocity*self.SuspendedSedimentconcentration

		self.ShearVelocity=()
		self.ShearVelocity=sqrt(self.DragCoefficient) * self.containingScenario.horizontalWindSpeed

		self.SuspendedSedimentconcentration_mg_L=()
		self.SuspendedSedimentconcentration_mg_L=self.SuspendedSedimentconcentration*1000000/self.Constants.L_per_m3

		self.VolumeFraction_Algae=()
		self.VolumeFraction_Algae=(self.AlgaeDensityinWaterColumn_g_L * self.Constants.L_per_m3)/(self.AlgaeDensity_g_m3)

		self.VolumeFraction_Solid=()
		self.VolumeFraction_Solid=self.SuspendedSedimentconcentration / self.rho

		self.WaterDensity=()
		self.WaterDensity=1000

		self.WaterViscosity=()
		self.WaterViscosity=1.197E-02

		self.Z_Liquid={}
		self.Z_Liquid["Chem_1_2_3_4_6_7_8_9_OCDD"]=self.currentChemical.Z_purewater
		self.Z_Liquid["Chem_1_2_3_4_6_7_8_9_OCDF"]=self.currentChemical.Z_purewater
		self.Z_Liquid["Chem_1_2_3_4_6_7_8_HpCDD"]=self.currentChemical.Z_purewater
		self.Z_Liquid["Chem_1_2_3_4_6_7_8_HpCDF"]=self.currentChemical.Z_purewater
		self.Z_Liquid["Chem_1_2_3_4_7_8_9_HpCDF"]=self.currentChemical.Z_purewater
		self.Z_Liquid["Chem_1_2_3_4_7_8_HxCDD"]=self.currentChemical.Z_purewater
		self.Z_Liquid["Chem_1_2_3_4_7_8_HxCDF"]=self.currentChemical.Z_purewater
		self.Z_Liquid["Chem_1_2_3_6_7_8_HxCDD"]=self.currentChemical.Z_purewater
		self.Z_Liquid["Chem_1_2_3_6_7_8_HxCDF"]=self.currentChemical.Z_purewater
		self.Z_Liquid["Chem_1_2_3_7_8_9_HxCDD"]=self.currentChemical.Z_purewater
		self.Z_Liquid["Chem_1_2_3_7_8_9_HxCDF"]=self.currentChemical.Z_purewater
		self.Z_Liquid["Chem_1_2_3_7_8_PeCDD"]=self.currentChemical.Z_purewater
		self.Z_Liquid["Chem_1_2_3_7_8_PeCDF"]=self.currentChemical.Z_purewater
		self.Z_Liquid["Chem_2_3_4_6_7_8_HxCDF"]=self.currentChemical.Z_purewater
		self.Z_Liquid["Chem_2_3_4_7_8_PeCDF"]=self.currentChemical.Z_purewater
		self.Z_Liquid["Chem_2_3_7_8_TCDD"]=self.currentChemical.Z_purewater
		self.Z_Liquid["Chem_2_3_7_8_TCDF"]=self.currentChemical.Z_purewater
		self.Z_Liquid["Chem_2_Methylnaphthalene"]=self.currentChemical.Z_purewater
		self.Z_Liquid["Chem_7_12_Dimethylbenz_a_anthracene"]=self.currentChemical.Z_purewater
		self.Z_Liquid["Chem_Acenaphthene"]=self.currentChemical.Z_purewater
		self.Z_Liquid["Chem_Acenaphthylene"]=self.currentChemical.Z_purewater
		self.Z_Liquid["Chem_Arsenic"]=self.currentChemical.Z_purewater
		self.Z_Liquid["Chem_Benz_a_anthracene"]=self.currentChemical.Z_purewater
		self.Z_Liquid["Chem_Benzo_A_Pyrene"]=self.currentChemical.Z_purewater
		self.Z_Liquid["Chem_Benzo_b_fluoranthene"]=self.currentChemical.Z_purewater
		self.Z_Liquid["Chem_Benzo_g_h_i_perylene"]=self.currentChemical.Z_purewater
		self.Z_Liquid["Chem_Benzo_k_fluoranthene"]=self.currentChemical.Z_purewater
		self.Z_Liquid["Chem_Cadmium"]=self.currentChemical.Z_purewater
		self.Z_Liquid["Chem_Chrysene"]=self.currentChemical.Z_purewater
		self.Z_Liquid["Chem_Dibenz_a_h_anthracene"]=self.currentChemical.Z_purewater
		self.Z_Liquid["Chem_Divalent_Mercury"]=self.currentChemical.Z_purewater
		self.Z_Liquid["Chem_Elemental_Mercury"]=self.currentChemical.Z_purewater
		self.Z_Liquid["Chem_Fluoranthene"]=self.currentChemical.Z_purewater
		self.Z_Liquid["Chem_Fluorene"]=self.currentChemical.Z_purewater
		self.Z_Liquid["Chem_Indeno_1_2_3_cd_pyrene"]=self.currentChemical.Z_purewater
		self.Z_Liquid["Chem_Lead"]=self.currentChemical.Z_purewater
		self.Z_Liquid["Chem_MethylMercury"]=self.currentChemical.Z_purewater
		try:
			self.Chemical_Z_Liquid=self.Z_Liquid[self.currentChemical.Name]
		except:
			self.Chemical_Z_Liquid=nan

		self.BoundaryLayerThicknessbelowWater={}
		self.BoundaryLayerThicknessbelowWater["Chem_1_2_3_4_6_7_8_9_OCDD"]=318 * self.Chemical_D_effective ** (0.683)
		self.BoundaryLayerThicknessbelowWater["Chem_1_2_3_4_6_7_8_9_OCDF"]=318 * self.Chemical_D_effective ** (0.683)
		self.BoundaryLayerThicknessbelowWater["Chem_1_2_3_4_6_7_8_HpCDD"]=318 * self.Chemical_D_effective ** (0.683)
		self.BoundaryLayerThicknessbelowWater["Chem_1_2_3_4_6_7_8_HpCDF"]=318 * self.Chemical_D_effective ** (0.683)
		self.BoundaryLayerThicknessbelowWater["Chem_1_2_3_4_7_8_9_HpCDF"]=318 * self.Chemical_D_effective ** (0.683)
		self.BoundaryLayerThicknessbelowWater["Chem_1_2_3_4_7_8_HxCDD"]=318 * self.Chemical_D_effective ** (0.683)
		self.BoundaryLayerThicknessbelowWater["Chem_1_2_3_4_7_8_HxCDF"]=318 * self.Chemical_D_effective ** (0.683)
		self.BoundaryLayerThicknessbelowWater["Chem_1_2_3_6_7_8_HxCDD"]=318 * self.Chemical_D_effective ** (0.683)
		self.BoundaryLayerThicknessbelowWater["Chem_1_2_3_6_7_8_HxCDF"]=318 * self.Chemical_D_effective ** (0.683)
		self.BoundaryLayerThicknessbelowWater["Chem_1_2_3_7_8_9_HxCDD"]=318 * self.Chemical_D_effective ** (0.683)
		self.BoundaryLayerThicknessbelowWater["Chem_1_2_3_7_8_9_HxCDF"]=318 * self.Chemical_D_effective ** (0.683)
		self.BoundaryLayerThicknessbelowWater["Chem_1_2_3_7_8_PeCDD"]=318 * self.Chemical_D_effective ** (0.683)
		self.BoundaryLayerThicknessbelowWater["Chem_1_2_3_7_8_PeCDF"]=318 * self.Chemical_D_effective ** (0.683)
		self.BoundaryLayerThicknessbelowWater["Chem_2_3_4_6_7_8_HxCDF"]=318 * self.Chemical_D_effective ** (0.683)
		self.BoundaryLayerThicknessbelowWater["Chem_2_3_4_7_8_PeCDF"]=318 * self.Chemical_D_effective ** (0.683)
		self.BoundaryLayerThicknessbelowWater["Chem_2_3_7_8_TCDD"]=318 * self.Chemical_D_effective ** (0.683)
		self.BoundaryLayerThicknessbelowWater["Chem_2_3_7_8_TCDF"]=318 * self.Chemical_D_effective ** (0.683)
		self.BoundaryLayerThicknessbelowWater["Chem_2_Methylnaphthalene"]=318 * self.Chemical_D_effective ** (0.683)
		self.BoundaryLayerThicknessbelowWater["Chem_7_12_Dimethylbenz_a_anthracene"]=318 * self.Chemical_D_effective ** (0.683)
		self.BoundaryLayerThicknessbelowWater["Chem_Acenaphthene"]=318 * self.Chemical_D_effective ** (0.683)
		self.BoundaryLayerThicknessbelowWater["Chem_Acenaphthylene"]=318 * self.Chemical_D_effective ** (0.683)
		self.BoundaryLayerThicknessbelowWater["Chem_Benz_a_anthracene"]=318 * self.Chemical_D_effective ** (0.683)
		self.BoundaryLayerThicknessbelowWater["Chem_Benzo_A_Pyrene"]=318 * self.Chemical_D_effective ** (0.683)
		self.BoundaryLayerThicknessbelowWater["Chem_Benzo_b_fluoranthene"]=318 * self.Chemical_D_effective ** (0.683)
		self.BoundaryLayerThicknessbelowWater["Chem_Benzo_g_h_i_perylene"]=318 * self.Chemical_D_effective ** (0.683)
		self.BoundaryLayerThicknessbelowWater["Chem_Benzo_k_fluoranthene"]=318 * self.Chemical_D_effective ** (0.683)
		self.BoundaryLayerThicknessbelowWater["Chem_Chrysene"]=318 * self.Chemical_D_effective ** (0.683)
		self.BoundaryLayerThicknessbelowWater["Chem_Dibenz_a_h_anthracene"]=318 * self.Chemical_D_effective ** (0.683)
		self.BoundaryLayerThicknessbelowWater["Chem_Divalent_Mercury"]=318 * self.Chemical_D_effective ** (0.683)
		self.BoundaryLayerThicknessbelowWater["Chem_Elemental_Mercury"]=318 * self.Chemical_D_effective ** (0.683)
		self.BoundaryLayerThicknessbelowWater["Chem_Fluoranthene"]=318 * self.Chemical_D_effective ** (0.683)
		self.BoundaryLayerThicknessbelowWater["Chem_Fluorene"]=318 * self.Chemical_D_effective ** (0.683)
		self.BoundaryLayerThicknessbelowWater["Chem_Indeno_1_2_3_cd_pyrene"]=318 * self.Chemical_D_effective ** (0.683)
		self.BoundaryLayerThicknessbelowWater["Chem_MethylMercury"]=318 * self.Chemical_D_effective ** (0.683)
		try:
			self.Chemical_BoundaryLayerThicknessbelowWater=self.BoundaryLayerThicknessbelowWater[self.currentChemical.Name]
		except:
			self.Chemical_BoundaryLayerThicknessbelowWater=nan

		self.CarbonSedimentationRate_g_m2_day=()
		self.CarbonSedimentationRate_g_m2_day=(10**(1.82 + (0.62 * log(self.ChlorophyllConcentration_mg_m3)/log(10)))/1000)

		self.RatioOfConcInAlgaeToConcDissolvedInWater={}
		self.RatioOfConcInAlgaeToConcDissolvedInWater["Chem_1_2_3_4_6_7_8_9_OCDD"]=5.31
		self.RatioOfConcInAlgaeToConcDissolvedInWater["Chem_1_2_3_4_6_7_8_9_OCDF"]=4.54
		self.RatioOfConcInAlgaeToConcDissolvedInWater["Chem_1_2_3_4_6_7_8_HpCDD"]=4.54
		self.RatioOfConcInAlgaeToConcDissolvedInWater["Chem_1_2_3_4_6_7_8_HpCDF"]=2.83
		self.RatioOfConcInAlgaeToConcDissolvedInWater["Chem_1_2_3_4_7_8_9_HpCDF"]=1.9
		self.RatioOfConcInAlgaeToConcDissolvedInWater["Chem_1_2_3_4_7_8_HxCDD"]=3.88
		self.RatioOfConcInAlgaeToConcDissolvedInWater["Chem_1_2_3_4_7_8_HxCDF"]=2.06
		self.RatioOfConcInAlgaeToConcDissolvedInWater["Chem_1_2_3_6_7_8_HxCDD"]=5.36
		self.RatioOfConcInAlgaeToConcDissolvedInWater["Chem_1_2_3_6_7_8_HxCDF"]=4.25
		self.RatioOfConcInAlgaeToConcDissolvedInWater["Chem_1_2_3_7_8_9_HxCDD"]=5.36
		self.RatioOfConcInAlgaeToConcDissolvedInWater["Chem_1_2_3_7_8_9_HxCDF"]=3.26
		self.RatioOfConcInAlgaeToConcDissolvedInWater["Chem_1_2_3_7_8_PeCDD"]=1.55
		self.RatioOfConcInAlgaeToConcDissolvedInWater["Chem_1_2_3_7_8_PeCDF"]=1.75
		self.RatioOfConcInAlgaeToConcDissolvedInWater["Chem_2_3_4_6_7_8_HxCDF"]=4.26
		self.RatioOfConcInAlgaeToConcDissolvedInWater["Chem_2_3_4_7_8_PeCDF"]=1.39
		self.RatioOfConcInAlgaeToConcDissolvedInWater["Chem_2_3_7_8_TCDD"]=1.76
		self.RatioOfConcInAlgaeToConcDissolvedInWater["Chem_2_3_7_8_TCDF"]=0.71
		self.RatioOfConcInAlgaeToConcDissolvedInWater["Chem_2_Methylnaphthalene"]=2.6
		self.RatioOfConcInAlgaeToConcDissolvedInWater["Chem_7_12_Dimethylbenz_a_anthracene"]=333.4
		self.RatioOfConcInAlgaeToConcDissolvedInWater["Chem_Acenaphthene"]=3.0
		self.RatioOfConcInAlgaeToConcDissolvedInWater["Chem_Acenaphthylene"]=3.7
		self.RatioOfConcInAlgaeToConcDissolvedInWater["Chem_Arsenic"]=0.155
		self.RatioOfConcInAlgaeToConcDissolvedInWater["Chem_Benz_a_anthracene"]=325.0
		self.RatioOfConcInAlgaeToConcDissolvedInWater["Chem_Benzo_A_Pyrene"]=510.0
		self.RatioOfConcInAlgaeToConcDissolvedInWater["Chem_Benzo_b_fluoranthene"]=317.0
		self.RatioOfConcInAlgaeToConcDissolvedInWater["Chem_Benzo_g_h_i_perylene"]=1539.0
		self.RatioOfConcInAlgaeToConcDissolvedInWater["Chem_Benzo_k_fluoranthene"]=473.0
		self.RatioOfConcInAlgaeToConcDissolvedInWater["Chem_Cadmium"]=1.87
		self.RatioOfConcInAlgaeToConcDissolvedInWater["Chem_Chrysene"]=280.0
		self.RatioOfConcInAlgaeToConcDissolvedInWater["Chem_Dibenz_a_h_anthracene"]=1388.0
		self.RatioOfConcInAlgaeToConcDissolvedInWater["Chem_Divalent_Mercury"]=(self.Chemical_D_ow * self.Chemical_AlgaeUptakeRate * 3 / (self.AlgaeRadius * self.AlgaeDensity_g_um3 * self.AlgaeGrowthRate))
		self.RatioOfConcInAlgaeToConcDissolvedInWater["Chem_Elemental_Mercury"]=(self.Chemical_D_ow * self.Chemical_AlgaeUptakeRate * 3 / (self.AlgaeRadius * self.AlgaeDensity_g_um3 * self.AlgaeGrowthRate))
		self.RatioOfConcInAlgaeToConcDissolvedInWater["Chem_Fluoranthene"]=67.4
		self.RatioOfConcInAlgaeToConcDissolvedInWater["Chem_Fluorene"]=5.8
		self.RatioOfConcInAlgaeToConcDissolvedInWater["Chem_Indeno_1_2_3_cd_pyrene"]=1653.0
		self.RatioOfConcInAlgaeToConcDissolvedInWater["Chem_Lead"]=0.6
		self.RatioOfConcInAlgaeToConcDissolvedInWater["Chem_MethylMercury"]=(self.Chemical_D_ow * self.Chemical_AlgaeUptakeRate * 3 / (self.AlgaeRadius * self.AlgaeDensity_g_um3 * self.AlgaeGrowthRate))
		try:
			self.Chemical_RatioOfConcInAlgaeToConcDissolvedInWater=self.RatioOfConcInAlgaeToConcDissolvedInWater[self.currentChemical.Name]
		except:
			self.Chemical_RatioOfConcInAlgaeToConcDissolvedInWater=nan

		self.SedimentDepositionRate_m3_m2_day=()
		self.SedimentDepositionRate_m3_m2_day=self.SedimentDepositionRate_kg_m2_day / self.rho

		self.ShearVelocity_m_per_day=()
		self.ShearVelocity_m_per_day=self.ShearVelocity*86400

		self.WaterSchmidtNumber={}
		self.WaterSchmidtNumber["Chem_1_2_3_4_6_7_8_9_OCDD"]=self.WaterViscosity/(self.WaterDensity * self.currentChemical.D_purewater_m2_per_s)
		self.WaterSchmidtNumber["Chem_1_2_3_4_6_7_8_9_OCDF"]=self.WaterViscosity/(self.WaterDensity * self.currentChemical.D_purewater_m2_per_s)
		self.WaterSchmidtNumber["Chem_1_2_3_4_6_7_8_HpCDD"]=self.WaterViscosity/(self.WaterDensity * self.currentChemical.D_purewater_m2_per_s)
		self.WaterSchmidtNumber["Chem_1_2_3_4_6_7_8_HpCDF"]=self.WaterViscosity/(self.WaterDensity * self.currentChemical.D_purewater_m2_per_s)
		self.WaterSchmidtNumber["Chem_1_2_3_4_7_8_9_HpCDF"]=self.WaterViscosity/(self.WaterDensity * self.currentChemical.D_purewater_m2_per_s)
		self.WaterSchmidtNumber["Chem_1_2_3_4_7_8_HxCDD"]=self.WaterViscosity/(self.WaterDensity * self.currentChemical.D_purewater_m2_per_s)
		self.WaterSchmidtNumber["Chem_1_2_3_4_7_8_HxCDF"]=self.WaterViscosity/(self.WaterDensity * self.currentChemical.D_purewater_m2_per_s)
		self.WaterSchmidtNumber["Chem_1_2_3_6_7_8_HxCDD"]=self.WaterViscosity/(self.WaterDensity * self.currentChemical.D_purewater_m2_per_s)
		self.WaterSchmidtNumber["Chem_1_2_3_6_7_8_HxCDF"]=self.WaterViscosity/(self.WaterDensity * self.currentChemical.D_purewater_m2_per_s)
		self.WaterSchmidtNumber["Chem_1_2_3_7_8_9_HxCDD"]=self.WaterViscosity/(self.WaterDensity * self.currentChemical.D_purewater_m2_per_s)
		self.WaterSchmidtNumber["Chem_1_2_3_7_8_9_HxCDF"]=self.WaterViscosity/(self.WaterDensity * self.currentChemical.D_purewater_m2_per_s)
		self.WaterSchmidtNumber["Chem_1_2_3_7_8_PeCDD"]=self.WaterViscosity/(self.WaterDensity * self.currentChemical.D_purewater_m2_per_s)
		self.WaterSchmidtNumber["Chem_1_2_3_7_8_PeCDF"]=self.WaterViscosity/(self.WaterDensity * self.currentChemical.D_purewater_m2_per_s)
		self.WaterSchmidtNumber["Chem_2_3_4_6_7_8_HxCDF"]=self.WaterViscosity/(self.WaterDensity * self.currentChemical.D_purewater_m2_per_s)
		self.WaterSchmidtNumber["Chem_2_3_4_7_8_PeCDF"]=self.WaterViscosity/(self.WaterDensity * self.currentChemical.D_purewater_m2_per_s)
		self.WaterSchmidtNumber["Chem_2_3_7_8_TCDD"]=self.WaterViscosity/(self.WaterDensity * self.currentChemical.D_purewater_m2_per_s)
		self.WaterSchmidtNumber["Chem_2_3_7_8_TCDF"]=self.WaterViscosity/(self.WaterDensity * self.currentChemical.D_purewater_m2_per_s)
		self.WaterSchmidtNumber["Chem_2_Methylnaphthalene"]=self.WaterViscosity/(self.WaterDensity * self.currentChemical.D_purewater_m2_per_s)
		self.WaterSchmidtNumber["Chem_7_12_Dimethylbenz_a_anthracene"]=self.WaterViscosity/(self.WaterDensity * self.currentChemical.D_purewater_m2_per_s)
		self.WaterSchmidtNumber["Chem_Acenaphthene"]=self.WaterViscosity/(self.WaterDensity * self.currentChemical.D_purewater_m2_per_s)
		self.WaterSchmidtNumber["Chem_Acenaphthylene"]=self.WaterViscosity/(self.WaterDensity * self.currentChemical.D_purewater_m2_per_s)
		self.WaterSchmidtNumber["Chem_Arsenic"]=self.WaterViscosity/(self.WaterDensity * self.currentChemical.D_purewater_m2_per_s)
		self.WaterSchmidtNumber["Chem_Benz_a_anthracene"]=self.WaterViscosity/(self.WaterDensity * self.currentChemical.D_purewater_m2_per_s)
		self.WaterSchmidtNumber["Chem_Benzo_A_Pyrene"]=self.WaterViscosity/(self.WaterDensity * self.currentChemical.D_purewater_m2_per_s)
		self.WaterSchmidtNumber["Chem_Benzo_b_fluoranthene"]=self.WaterViscosity/(self.WaterDensity * self.currentChemical.D_purewater_m2_per_s)
		self.WaterSchmidtNumber["Chem_Benzo_g_h_i_perylene"]=self.WaterViscosity/(self.WaterDensity * self.currentChemical.D_purewater_m2_per_s)
		self.WaterSchmidtNumber["Chem_Benzo_k_fluoranthene"]=self.WaterViscosity/(self.WaterDensity * self.currentChemical.D_purewater_m2_per_s)
		self.WaterSchmidtNumber["Chem_Cadmium"]=self.WaterViscosity/(self.WaterDensity * self.currentChemical.D_purewater_m2_per_s)
		self.WaterSchmidtNumber["Chem_Chrysene"]=self.WaterViscosity/(self.WaterDensity * self.currentChemical.D_purewater_m2_per_s)
		self.WaterSchmidtNumber["Chem_Dibenz_a_h_anthracene"]=self.WaterViscosity/(self.WaterDensity * self.currentChemical.D_purewater_m2_per_s)
		self.WaterSchmidtNumber["Chem_Divalent_Mercury"]=self.WaterViscosity/(self.WaterDensity * self.currentChemical.D_purewater_m2_per_s)
		self.WaterSchmidtNumber["Chem_Elemental_Mercury"]=self.WaterViscosity/(self.WaterDensity * self.currentChemical.D_purewater_m2_per_s)
		self.WaterSchmidtNumber["Chem_Fluoranthene"]=self.WaterViscosity/(self.WaterDensity * self.currentChemical.D_purewater_m2_per_s)
		self.WaterSchmidtNumber["Chem_Fluorene"]=self.WaterViscosity/(self.WaterDensity * self.currentChemical.D_purewater_m2_per_s)
		self.WaterSchmidtNumber["Chem_Indeno_1_2_3_cd_pyrene"]=self.WaterViscosity/(self.WaterDensity * self.currentChemical.D_purewater_m2_per_s)
		self.WaterSchmidtNumber["Chem_Lead"]=self.WaterViscosity/(self.WaterDensity * self.currentChemical.D_purewater_m2_per_s)
		self.WaterSchmidtNumber["Chem_MethylMercury"]=self.WaterViscosity/(self.WaterDensity * self.currentChemical.D_purewater_m2_per_s)
		try:
			self.Chemical_WaterSchmidtNumber=self.WaterSchmidtNumber[self.currentChemical.Name]
		except:
			self.Chemical_WaterSchmidtNumber=nan

		self.Z_Solid={}
		self.Z_Solid["Chem_1_2_3_4_6_7_8_9_OCDD"]=(self.rho * self.Chemical_Kd / 1000) * self.currentChemical.Z_purewater
		self.Z_Solid["Chem_1_2_3_4_6_7_8_9_OCDF"]=(self.rho * self.Chemical_Kd / 1000) * self.currentChemical.Z_purewater
		self.Z_Solid["Chem_1_2_3_4_6_7_8_HpCDD"]=(self.rho * self.Chemical_Kd / 1000) * self.currentChemical.Z_purewater
		self.Z_Solid["Chem_1_2_3_4_6_7_8_HpCDF"]=(self.rho * self.Chemical_Kd / 1000) * self.currentChemical.Z_purewater
		self.Z_Solid["Chem_1_2_3_4_7_8_9_HpCDF"]=(self.rho * self.Chemical_Kd / 1000) * self.currentChemical.Z_purewater
		self.Z_Solid["Chem_1_2_3_4_7_8_HxCDD"]=(self.rho * self.Chemical_Kd / 1000) * self.currentChemical.Z_purewater
		self.Z_Solid["Chem_1_2_3_4_7_8_HxCDF"]=(self.rho * self.Chemical_Kd / 1000) * self.currentChemical.Z_purewater
		self.Z_Solid["Chem_1_2_3_6_7_8_HxCDD"]=(self.rho * self.Chemical_Kd / 1000) * self.currentChemical.Z_purewater
		self.Z_Solid["Chem_1_2_3_6_7_8_HxCDF"]=(self.rho * self.Chemical_Kd / 1000) * self.currentChemical.Z_purewater
		self.Z_Solid["Chem_1_2_3_7_8_9_HxCDD"]=(self.rho * self.Chemical_Kd / 1000) * self.currentChemical.Z_purewater
		self.Z_Solid["Chem_1_2_3_7_8_9_HxCDF"]=(self.rho * self.Chemical_Kd / 1000) * self.currentChemical.Z_purewater
		self.Z_Solid["Chem_1_2_3_7_8_PeCDD"]=(self.rho * self.Chemical_Kd / 1000) * self.currentChemical.Z_purewater
		self.Z_Solid["Chem_1_2_3_7_8_PeCDF"]=(self.rho * self.Chemical_Kd / 1000) * self.currentChemical.Z_purewater
		self.Z_Solid["Chem_2_3_4_6_7_8_HxCDF"]=(self.rho * self.Chemical_Kd / 1000) * self.currentChemical.Z_purewater
		self.Z_Solid["Chem_2_3_4_7_8_PeCDF"]=(self.rho * self.Chemical_Kd / 1000) * self.currentChemical.Z_purewater
		self.Z_Solid["Chem_2_3_7_8_TCDD"]=(self.rho * self.Chemical_Kd / 1000) * self.currentChemical.Z_purewater
		self.Z_Solid["Chem_2_3_7_8_TCDF"]=(self.rho * self.Chemical_Kd / 1000) * self.currentChemical.Z_purewater
		self.Z_Solid["Chem_2_Methylnaphthalene"]=(self.rho * self.Chemical_Kd / 1000) * self.currentChemical.Z_purewater
		self.Z_Solid["Chem_7_12_Dimethylbenz_a_anthracene"]=(self.rho * self.Chemical_Kd / 1000) * self.currentChemical.Z_purewater
		self.Z_Solid["Chem_Acenaphthene"]=(self.rho * self.Chemical_Kd / 1000) * self.currentChemical.Z_purewater
		self.Z_Solid["Chem_Acenaphthylene"]=(self.rho * self.Chemical_Kd / 1000) * self.currentChemical.Z_purewater
		self.Z_Solid["Chem_Arsenic"]=(self.rho * self.Chemical_Kd / 1000) * self.currentChemical.Z_purewater
		self.Z_Solid["Chem_Benz_a_anthracene"]=(self.rho * self.Chemical_Kd / 1000) * self.currentChemical.Z_purewater
		self.Z_Solid["Chem_Benzo_A_Pyrene"]=self.Chemical_Kd * (self.rho / 1000) * self.currentChemical.Z_purewater
		self.Z_Solid["Chem_Benzo_b_fluoranthene"]=(self.rho * self.Chemical_Kd / 1000) * self.currentChemical.Z_purewater
		self.Z_Solid["Chem_Benzo_g_h_i_perylene"]=(self.rho * self.Chemical_Kd / 1000) * self.currentChemical.Z_purewater
		self.Z_Solid["Chem_Benzo_k_fluoranthene"]=(self.rho * self.Chemical_Kd / 1000) * self.currentChemical.Z_purewater
		self.Z_Solid["Chem_Cadmium"]=(self.rho * self.Chemical_Kd / 1000) * self.currentChemical.Z_purewater
		self.Z_Solid["Chem_Chrysene"]=(self.rho * self.Chemical_Kd / 1000) * self.currentChemical.Z_purewater
		self.Z_Solid["Chem_Dibenz_a_h_anthracene"]=(self.rho * self.Chemical_Kd / 1000) * self.currentChemical.Z_purewater
		self.Z_Solid["Chem_Divalent_Mercury"]=self.Chemical_Kd * (self.rho / 1000) * self.currentChemical.Z_purewater
		self.Z_Solid["Chem_Elemental_Mercury"]=self.Chemical_Kd * (self.rho / 1000) * self.currentChemical.Z_purewater
		self.Z_Solid["Chem_Fluoranthene"]=(self.rho * self.Chemical_Kd / 1000) * self.currentChemical.Z_purewater
		self.Z_Solid["Chem_Fluorene"]=(self.rho * self.Chemical_Kd / 1000) * self.currentChemical.Z_purewater
		self.Z_Solid["Chem_Indeno_1_2_3_cd_pyrene"]=(self.rho * self.Chemical_Kd / 1000) * self.currentChemical.Z_purewater
		self.Z_Solid["Chem_Lead"]=(self.rho * self.Chemical_Kd / 1000) * self.currentChemical.Z_purewater
		self.Z_Solid["Chem_MethylMercury"]=self.Chemical_Kd * (self.rho / 1000) * self.currentChemical.Z_purewater
		try:
			self.Chemical_Z_Solid=self.Z_Solid[self.currentChemical.Name]
		except:
			self.Chemical_Z_Solid=nan

		self.VolumeFraction_Liquid=()
		self.VolumeFraction_Liquid=1 - self.VolumeFraction_Solid - self.VolumeFraction_Algae

		self.VolumeFraction_Solid=()
		self.VolumeFraction_Solid=self.SuspendedSedimentconcentration / self.rho

		self.GenericDenominatorforCalculatingFractioninPhases={}
		self.GenericDenominatorforCalculatingFractioninPhases["Chem_1_2_3_4_6_7_8_9_OCDD"]=self.containingVolumeElement.Volume * (self.VolumeFraction_Algae * self.Chemical_RatioOfConcInAlgaeToConcDissolvedInWater * self.AlgaeDensity_g_m3 * (self.Constants.m3_per_L)  + self.VolumeFraction_Solid * self.Chemical_Kd * self.Constants.m3_per_L * self.rho + self.VolumeFraction_Liquid )
		self.GenericDenominatorforCalculatingFractioninPhases["Chem_1_2_3_4_6_7_8_9_OCDF"]=self.containingVolumeElement.Volume * (self.VolumeFraction_Algae * self.Chemical_RatioOfConcInAlgaeToConcDissolvedInWater * self.AlgaeDensity_g_m3 * (self.Constants.m3_per_L)  + self.VolumeFraction_Solid * self.Chemical_Kd * self.Constants.m3_per_L * self.rho + self.VolumeFraction_Liquid )
		self.GenericDenominatorforCalculatingFractioninPhases["Chem_1_2_3_4_6_7_8_HpCDD"]=self.containingVolumeElement.Volume * (self.VolumeFraction_Algae * self.Chemical_RatioOfConcInAlgaeToConcDissolvedInWater * self.AlgaeDensity_g_m3 * (self.Constants.m3_per_L)  + self.VolumeFraction_Solid * self.Chemical_Kd * self.Constants.m3_per_L * self.rho + self.VolumeFraction_Liquid )
		self.GenericDenominatorforCalculatingFractioninPhases["Chem_1_2_3_4_6_7_8_HpCDF"]=self.containingVolumeElement.Volume * (self.VolumeFraction_Algae * self.Chemical_RatioOfConcInAlgaeToConcDissolvedInWater * self.AlgaeDensity_g_m3 * (self.Constants.m3_per_L)  + self.VolumeFraction_Solid * self.Chemical_Kd * self.Constants.m3_per_L * self.rho + self.VolumeFraction_Liquid )
		self.GenericDenominatorforCalculatingFractioninPhases["Chem_1_2_3_4_7_8_9_HpCDF"]=self.containingVolumeElement.Volume * (self.VolumeFraction_Algae * self.Chemical_RatioOfConcInAlgaeToConcDissolvedInWater * self.AlgaeDensity_g_m3 * (self.Constants.m3_per_L)  + self.VolumeFraction_Solid * self.Chemical_Kd * self.Constants.m3_per_L * self.rho + self.VolumeFraction_Liquid )
		self.GenericDenominatorforCalculatingFractioninPhases["Chem_1_2_3_4_7_8_HxCDD"]=self.containingVolumeElement.Volume * (self.VolumeFraction_Algae * self.Chemical_RatioOfConcInAlgaeToConcDissolvedInWater * self.AlgaeDensity_g_m3 * (self.Constants.m3_per_L)  + self.VolumeFraction_Solid * self.Chemical_Kd * self.Constants.m3_per_L * self.rho + self.VolumeFraction_Liquid )
		self.GenericDenominatorforCalculatingFractioninPhases["Chem_1_2_3_4_7_8_HxCDF"]=self.containingVolumeElement.Volume * (self.VolumeFraction_Algae * self.Chemical_RatioOfConcInAlgaeToConcDissolvedInWater * self.AlgaeDensity_g_m3 * (self.Constants.m3_per_L)  + self.VolumeFraction_Solid * self.Chemical_Kd * self.Constants.m3_per_L * self.rho + self.VolumeFraction_Liquid )
		self.GenericDenominatorforCalculatingFractioninPhases["Chem_1_2_3_6_7_8_HxCDD"]=self.containingVolumeElement.Volume * (self.VolumeFraction_Algae * self.Chemical_RatioOfConcInAlgaeToConcDissolvedInWater * self.AlgaeDensity_g_m3 * (self.Constants.m3_per_L)  + self.VolumeFraction_Solid * self.Chemical_Kd * self.Constants.m3_per_L * self.rho + self.VolumeFraction_Liquid )
		self.GenericDenominatorforCalculatingFractioninPhases["Chem_1_2_3_6_7_8_HxCDF"]=self.containingVolumeElement.Volume * (self.VolumeFraction_Algae * self.Chemical_RatioOfConcInAlgaeToConcDissolvedInWater * self.AlgaeDensity_g_m3 * (self.Constants.m3_per_L)  + self.VolumeFraction_Solid * self.Chemical_Kd * self.Constants.m3_per_L * self.rho + self.VolumeFraction_Liquid )
		self.GenericDenominatorforCalculatingFractioninPhases["Chem_1_2_3_7_8_9_HxCDD"]=self.containingVolumeElement.Volume * (self.VolumeFraction_Algae * self.Chemical_RatioOfConcInAlgaeToConcDissolvedInWater * self.AlgaeDensity_g_m3 * (self.Constants.m3_per_L)  + self.VolumeFraction_Solid * self.Chemical_Kd * self.Constants.m3_per_L * self.rho + self.VolumeFraction_Liquid )
		self.GenericDenominatorforCalculatingFractioninPhases["Chem_1_2_3_7_8_9_HxCDF"]=self.containingVolumeElement.Volume * (self.VolumeFraction_Algae * self.Chemical_RatioOfConcInAlgaeToConcDissolvedInWater * self.AlgaeDensity_g_m3 * (self.Constants.m3_per_L)  + self.VolumeFraction_Solid * self.Chemical_Kd * self.Constants.m3_per_L * self.rho + self.VolumeFraction_Liquid )
		self.GenericDenominatorforCalculatingFractioninPhases["Chem_1_2_3_7_8_PeCDD"]=self.containingVolumeElement.Volume * (self.VolumeFraction_Algae * self.Chemical_RatioOfConcInAlgaeToConcDissolvedInWater * self.AlgaeDensity_g_m3 * (self.Constants.m3_per_L)  + self.VolumeFraction_Solid * self.Chemical_Kd * self.Constants.m3_per_L * self.rho + self.VolumeFraction_Liquid )
		self.GenericDenominatorforCalculatingFractioninPhases["Chem_1_2_3_7_8_PeCDF"]=self.containingVolumeElement.Volume * (self.VolumeFraction_Algae * self.Chemical_RatioOfConcInAlgaeToConcDissolvedInWater * self.AlgaeDensity_g_m3 * (self.Constants.m3_per_L)  + self.VolumeFraction_Solid * self.Chemical_Kd * self.Constants.m3_per_L * self.rho + self.VolumeFraction_Liquid )
		self.GenericDenominatorforCalculatingFractioninPhases["Chem_2_3_4_6_7_8_HxCDF"]=self.containingVolumeElement.Volume * (self.VolumeFraction_Algae * self.Chemical_RatioOfConcInAlgaeToConcDissolvedInWater * self.AlgaeDensity_g_m3 * (self.Constants.m3_per_L)  + self.VolumeFraction_Solid * self.Chemical_Kd * self.Constants.m3_per_L * self.rho + self.VolumeFraction_Liquid )
		self.GenericDenominatorforCalculatingFractioninPhases["Chem_2_3_4_7_8_PeCDF"]=self.containingVolumeElement.Volume * (self.VolumeFraction_Algae * self.Chemical_RatioOfConcInAlgaeToConcDissolvedInWater * self.AlgaeDensity_g_m3 * (self.Constants.m3_per_L)  + self.VolumeFraction_Solid * self.Chemical_Kd * self.Constants.m3_per_L * self.rho + self.VolumeFraction_Liquid )
		self.GenericDenominatorforCalculatingFractioninPhases["Chem_2_3_7_8_TCDD"]=self.containingVolumeElement.Volume * (self.VolumeFraction_Algae * self.Chemical_RatioOfConcInAlgaeToConcDissolvedInWater * self.AlgaeDensity_g_m3 * (self.Constants.m3_per_L)  + self.VolumeFraction_Solid * self.Chemical_Kd * self.Constants.m3_per_L * self.rho + self.VolumeFraction_Liquid )
		self.GenericDenominatorforCalculatingFractioninPhases["Chem_2_3_7_8_TCDF"]=self.containingVolumeElement.Volume * (self.VolumeFraction_Algae * self.Chemical_RatioOfConcInAlgaeToConcDissolvedInWater * self.AlgaeDensity_g_m3 * (self.Constants.m3_per_L)  + self.VolumeFraction_Solid * self.Chemical_Kd * self.Constants.m3_per_L * self.rho + self.VolumeFraction_Liquid )
		self.GenericDenominatorforCalculatingFractioninPhases["Chem_2_Methylnaphthalene"]=self.containingVolumeElement.Volume * (self.VolumeFraction_Algae * self.Chemical_RatioOfConcInAlgaeToConcDissolvedInWater * self.AlgaeDensity_g_m3 * (self.Constants.m3_per_L)  + self.VolumeFraction_Solid * self.Chemical_Kd * self.Constants.m3_per_L * self.rho + self.VolumeFraction_Liquid )
		self.GenericDenominatorforCalculatingFractioninPhases["Chem_7_12_Dimethylbenz_a_anthracene"]=self.containingVolumeElement.Volume * (self.VolumeFraction_Algae * self.Chemical_RatioOfConcInAlgaeToConcDissolvedInWater * self.AlgaeDensity_g_m3 * (self.Constants.m3_per_L)  + self.VolumeFraction_Solid * self.Chemical_Kd * self.Constants.m3_per_L * self.rho + self.VolumeFraction_Liquid )
		self.GenericDenominatorforCalculatingFractioninPhases["Chem_Acenaphthene"]=self.containingVolumeElement.Volume * (self.VolumeFraction_Algae * self.Chemical_RatioOfConcInAlgaeToConcDissolvedInWater * self.AlgaeDensity_g_m3 * (self.Constants.m3_per_L)  + self.VolumeFraction_Solid * self.Chemical_Kd * self.Constants.m3_per_L * self.rho + self.VolumeFraction_Liquid )
		self.GenericDenominatorforCalculatingFractioninPhases["Chem_Acenaphthylene"]=self.containingVolumeElement.Volume * (self.VolumeFraction_Algae * self.Chemical_RatioOfConcInAlgaeToConcDissolvedInWater * self.AlgaeDensity_g_m3 * (self.Constants.m3_per_L)  + self.VolumeFraction_Solid * self.Chemical_Kd * self.Constants.m3_per_L * self.rho + self.VolumeFraction_Liquid )
		self.GenericDenominatorforCalculatingFractioninPhases["Chem_Arsenic"]=self.containingVolumeElement.Volume * (self.VolumeFraction_Algae * self.Chemical_RatioOfConcInAlgaeToConcDissolvedInWater * self.AlgaeDensity_g_m3 * (self.Constants.m3_per_L)  + self.VolumeFraction_Solid * self.Chemical_Kd * self.Constants.m3_per_L * self.rho + self.VolumeFraction_Liquid )
		self.GenericDenominatorforCalculatingFractioninPhases["Chem_Benz_a_anthracene"]=self.containingVolumeElement.Volume * (self.VolumeFraction_Algae * self.Chemical_RatioOfConcInAlgaeToConcDissolvedInWater * self.AlgaeDensity_g_m3 * (self.Constants.m3_per_L)  + self.VolumeFraction_Solid * self.Chemical_Kd * self.Constants.m3_per_L * self.rho + self.VolumeFraction_Liquid )
		self.GenericDenominatorforCalculatingFractioninPhases["Chem_Benzo_A_Pyrene"]=self.containingVolumeElement.Volume * (self.VolumeFraction_Algae * self.Chemical_RatioOfConcInAlgaeToConcDissolvedInWater * self.AlgaeDensity_g_m3 * (self.Constants.m3_per_L)  + self.VolumeFraction_Solid * self.Chemical_Kd * self.Constants.m3_per_L * self.rho + self.VolumeFraction_Liquid )
		self.GenericDenominatorforCalculatingFractioninPhases["Chem_Benzo_b_fluoranthene"]=self.containingVolumeElement.Volume * (self.VolumeFraction_Algae * self.Chemical_RatioOfConcInAlgaeToConcDissolvedInWater * self.AlgaeDensity_g_m3 * (self.Constants.m3_per_L)  + self.VolumeFraction_Solid * self.Chemical_Kd * self.Constants.m3_per_L * self.rho + self.VolumeFraction_Liquid )
		self.GenericDenominatorforCalculatingFractioninPhases["Chem_Benzo_g_h_i_perylene"]=self.containingVolumeElement.Volume * (self.VolumeFraction_Algae * self.Chemical_RatioOfConcInAlgaeToConcDissolvedInWater * self.AlgaeDensity_g_m3 * (self.Constants.m3_per_L)  + self.VolumeFraction_Solid * self.Chemical_Kd * self.Constants.m3_per_L * self.rho + self.VolumeFraction_Liquid )
		self.GenericDenominatorforCalculatingFractioninPhases["Chem_Benzo_k_fluoranthene"]=self.containingVolumeElement.Volume * (self.VolumeFraction_Algae * self.Chemical_RatioOfConcInAlgaeToConcDissolvedInWater * self.AlgaeDensity_g_m3 * (self.Constants.m3_per_L)  + self.VolumeFraction_Solid * self.Chemical_Kd * self.Constants.m3_per_L * self.rho + self.VolumeFraction_Liquid )
		self.GenericDenominatorforCalculatingFractioninPhases["Chem_Cadmium"]=self.containingVolumeElement.Volume * (self.VolumeFraction_Algae * self.Chemical_RatioOfConcInAlgaeToConcDissolvedInWater * self.AlgaeDensity_g_m3 * (self.Constants.m3_per_L)  + self.VolumeFraction_Solid * self.Chemical_Kd * self.Constants.m3_per_L * self.rho + self.VolumeFraction_Liquid )
		self.GenericDenominatorforCalculatingFractioninPhases["Chem_Chrysene"]=self.containingVolumeElement.Volume * (self.VolumeFraction_Algae * self.Chemical_RatioOfConcInAlgaeToConcDissolvedInWater * self.AlgaeDensity_g_m3 * (self.Constants.m3_per_L)  + self.VolumeFraction_Solid * self.Chemical_Kd * self.Constants.m3_per_L * self.rho + self.VolumeFraction_Liquid )
		self.GenericDenominatorforCalculatingFractioninPhases["Chem_Dibenz_a_h_anthracene"]=self.containingVolumeElement.Volume * (self.VolumeFraction_Algae * self.Chemical_RatioOfConcInAlgaeToConcDissolvedInWater * self.AlgaeDensity_g_m3 * (self.Constants.m3_per_L)  + self.VolumeFraction_Solid * self.Chemical_Kd * self.Constants.m3_per_L * self.rho + self.VolumeFraction_Liquid )
		self.GenericDenominatorforCalculatingFractioninPhases["Chem_Divalent_Mercury"]=self.containingVolumeElement.Volume * (self.VolumeFraction_Algae * self.Chemical_RatioOfConcInAlgaeToConcDissolvedInWater * self.AlgaeDensity_g_m3 * (self.Constants.m3_per_L)  + self.VolumeFraction_Solid * self.Chemical_Kd * self.Constants.m3_per_L * self.rho + self.VolumeFraction_Liquid )
		self.GenericDenominatorforCalculatingFractioninPhases["Chem_Elemental_Mercury"]=self.containingVolumeElement.Volume * (self.VolumeFraction_Algae * self.Chemical_RatioOfConcInAlgaeToConcDissolvedInWater * self.AlgaeDensity_g_m3 * (self.Constants.m3_per_L)  + self.VolumeFraction_Solid * self.Chemical_Kd * self.Constants.m3_per_L * self.rho + self.VolumeFraction_Liquid )
		self.GenericDenominatorforCalculatingFractioninPhases["Chem_Fluoranthene"]=self.containingVolumeElement.Volume * (self.VolumeFraction_Algae * self.Chemical_RatioOfConcInAlgaeToConcDissolvedInWater * self.AlgaeDensity_g_m3 * (self.Constants.m3_per_L)  + self.VolumeFraction_Solid * self.Chemical_Kd * self.Constants.m3_per_L * self.rho + self.VolumeFraction_Liquid )
		self.GenericDenominatorforCalculatingFractioninPhases["Chem_Fluorene"]=self.containingVolumeElement.Volume * (self.VolumeFraction_Algae * self.Chemical_RatioOfConcInAlgaeToConcDissolvedInWater * self.AlgaeDensity_g_m3 * (self.Constants.m3_per_L)  + self.VolumeFraction_Solid * self.Chemical_Kd * self.Constants.m3_per_L * self.rho + self.VolumeFraction_Liquid )
		self.GenericDenominatorforCalculatingFractioninPhases["Chem_Indeno_1_2_3_cd_pyrene"]=self.containingVolumeElement.Volume * (self.VolumeFraction_Algae * self.Chemical_RatioOfConcInAlgaeToConcDissolvedInWater * self.AlgaeDensity_g_m3 * (self.Constants.m3_per_L)  + self.VolumeFraction_Solid * self.Chemical_Kd * self.Constants.m3_per_L * self.rho + self.VolumeFraction_Liquid )
		self.GenericDenominatorforCalculatingFractioninPhases["Chem_Lead"]=self.containingVolumeElement.Volume * (self.VolumeFraction_Algae * self.Chemical_RatioOfConcInAlgaeToConcDissolvedInWater * self.AlgaeDensity_g_m3 * (self.Constants.m3_per_L)  + self.VolumeFraction_Solid * self.Chemical_Kd * self.Constants.m3_per_L * self.rho + self.VolumeFraction_Liquid )
		self.GenericDenominatorforCalculatingFractioninPhases["Chem_MethylMercury"]=self.containingVolumeElement.Volume * (self.VolumeFraction_Algae * self.Chemical_RatioOfConcInAlgaeToConcDissolvedInWater * self.AlgaeDensity_g_m3 * (self.Constants.m3_per_L)  + self.VolumeFraction_Solid * self.Chemical_Kd * self.Constants.m3_per_L * self.rho + self.VolumeFraction_Liquid )
		try:
			self.Chemical_GenericDenominatorforCalculatingFractioninPhases=self.GenericDenominatorforCalculatingFractioninPhases[self.currentChemical.Name]
		except:
			self.Chemical_GenericDenominatorforCalculatingFractioninPhases=nan

		self.AlgaeSedimentationRate_g_m2_day=()
		self.AlgaeSedimentationRate_g_m2_day=self.CarbonSedimentationRate_g_m2_day/ (self.AlgaeCarbonContentDryWt *(1-self.AlgaeWaterContent))

		self.Z_Algae={}
		self.Z_Algae["Chem_1_2_3_4_6_7_8_9_OCDD"]=(self.Chemical_RatioOfConcInAlgaeToConcDissolvedInWater*self.AlgaeDensity_g_m3/1000.0)*self.currentChemical.Z_purewater
		self.Z_Algae["Chem_1_2_3_4_6_7_8_9_OCDF"]=(self.Chemical_RatioOfConcInAlgaeToConcDissolvedInWater*self.AlgaeDensity_g_m3/1000.0)*self.currentChemical.Z_purewater
		self.Z_Algae["Chem_1_2_3_4_6_7_8_HpCDD"]=(self.Chemical_RatioOfConcInAlgaeToConcDissolvedInWater*self.AlgaeDensity_g_m3/1000.0)*self.currentChemical.Z_purewater
		self.Z_Algae["Chem_1_2_3_4_6_7_8_HpCDF"]=(self.Chemical_RatioOfConcInAlgaeToConcDissolvedInWater*self.AlgaeDensity_g_m3/1000.0)*self.currentChemical.Z_purewater
		self.Z_Algae["Chem_1_2_3_4_7_8_9_HpCDF"]=(self.Chemical_RatioOfConcInAlgaeToConcDissolvedInWater*self.AlgaeDensity_g_m3/1000.0)*self.currentChemical.Z_purewater
		self.Z_Algae["Chem_1_2_3_4_7_8_HxCDD"]=(self.Chemical_RatioOfConcInAlgaeToConcDissolvedInWater*self.AlgaeDensity_g_m3/1000.0)*self.currentChemical.Z_purewater
		self.Z_Algae["Chem_1_2_3_4_7_8_HxCDF"]=(self.Chemical_RatioOfConcInAlgaeToConcDissolvedInWater*self.AlgaeDensity_g_m3/1000.0)*self.currentChemical.Z_purewater
		self.Z_Algae["Chem_1_2_3_6_7_8_HxCDD"]=(self.Chemical_RatioOfConcInAlgaeToConcDissolvedInWater*self.AlgaeDensity_g_m3/1000.0)*self.currentChemical.Z_purewater
		self.Z_Algae["Chem_1_2_3_6_7_8_HxCDF"]=(self.Chemical_RatioOfConcInAlgaeToConcDissolvedInWater*self.AlgaeDensity_g_m3/1000.0)*self.currentChemical.Z_purewater
		self.Z_Algae["Chem_1_2_3_7_8_9_HxCDD"]=(self.Chemical_RatioOfConcInAlgaeToConcDissolvedInWater*self.AlgaeDensity_g_m3/1000.0)*self.currentChemical.Z_purewater
		self.Z_Algae["Chem_1_2_3_7_8_9_HxCDF"]=(self.Chemical_RatioOfConcInAlgaeToConcDissolvedInWater*self.AlgaeDensity_g_m3/1000.0)*self.currentChemical.Z_purewater
		self.Z_Algae["Chem_1_2_3_7_8_PeCDD"]=(self.Chemical_RatioOfConcInAlgaeToConcDissolvedInWater*self.AlgaeDensity_g_m3/1000.0)*self.currentChemical.Z_purewater
		self.Z_Algae["Chem_1_2_3_7_8_PeCDF"]=(self.Chemical_RatioOfConcInAlgaeToConcDissolvedInWater*self.AlgaeDensity_g_m3/1000.0)*self.currentChemical.Z_purewater
		self.Z_Algae["Chem_2_3_4_6_7_8_HxCDF"]=(self.Chemical_RatioOfConcInAlgaeToConcDissolvedInWater*self.AlgaeDensity_g_m3/1000.0)*self.currentChemical.Z_purewater
		self.Z_Algae["Chem_2_3_4_7_8_PeCDF"]=(self.Chemical_RatioOfConcInAlgaeToConcDissolvedInWater*self.AlgaeDensity_g_m3/1000.0)*self.currentChemical.Z_purewater
		self.Z_Algae["Chem_2_3_7_8_TCDD"]=(self.Chemical_RatioOfConcInAlgaeToConcDissolvedInWater*self.AlgaeDensity_g_m3/1000.0)*self.currentChemical.Z_purewater
		self.Z_Algae["Chem_2_3_7_8_TCDF"]=(self.Chemical_RatioOfConcInAlgaeToConcDissolvedInWater*self.AlgaeDensity_g_m3/1000.0)*self.currentChemical.Z_purewater
		self.Z_Algae["Chem_2_Methylnaphthalene"]=(self.Chemical_RatioOfConcInAlgaeToConcDissolvedInWater*self.AlgaeDensity_g_m3/1000.0)*self.currentChemical.Z_purewater
		self.Z_Algae["Chem_7_12_Dimethylbenz_a_anthracene"]=(self.Chemical_RatioOfConcInAlgaeToConcDissolvedInWater*self.AlgaeDensity_g_m3/1000.0)*self.currentChemical.Z_purewater
		self.Z_Algae["Chem_Acenaphthene"]=(self.Chemical_RatioOfConcInAlgaeToConcDissolvedInWater*self.AlgaeDensity_g_m3/1000.0)*self.currentChemical.Z_purewater
		self.Z_Algae["Chem_Acenaphthylene"]=(self.Chemical_RatioOfConcInAlgaeToConcDissolvedInWater*self.AlgaeDensity_g_m3/1000.0)*self.currentChemical.Z_purewater
		self.Z_Algae["Chem_Arsenic"]=(self.Chemical_RatioOfConcInAlgaeToConcDissolvedInWater*self.AlgaeDensity_g_m3/1000.0)*self.currentChemical.Z_purewater
		self.Z_Algae["Chem_Benz_a_anthracene"]=(self.Chemical_RatioOfConcInAlgaeToConcDissolvedInWater*self.AlgaeDensity_g_m3/1000.0)*self.currentChemical.Z_purewater
		self.Z_Algae["Chem_Benzo_A_Pyrene"]=(self.Chemical_RatioOfConcInAlgaeToConcDissolvedInWater*self.AlgaeDensity_g_m3/1000.0)*self.currentChemical.Z_purewater
		self.Z_Algae["Chem_Benzo_b_fluoranthene"]=(self.Chemical_RatioOfConcInAlgaeToConcDissolvedInWater*self.AlgaeDensity_g_m3/1000.0)*self.currentChemical.Z_purewater
		self.Z_Algae["Chem_Benzo_g_h_i_perylene"]=(self.Chemical_RatioOfConcInAlgaeToConcDissolvedInWater*self.AlgaeDensity_g_m3/1000.0)*self.currentChemical.Z_purewater
		self.Z_Algae["Chem_Benzo_k_fluoranthene"]=(self.Chemical_RatioOfConcInAlgaeToConcDissolvedInWater*self.AlgaeDensity_g_m3/1000.0)*self.currentChemical.Z_purewater
		self.Z_Algae["Chem_Cadmium"]=(self.Chemical_RatioOfConcInAlgaeToConcDissolvedInWater*self.AlgaeDensity_g_m3/1000.0)*self.currentChemical.Z_purewater
		self.Z_Algae["Chem_Chrysene"]=(self.Chemical_RatioOfConcInAlgaeToConcDissolvedInWater*self.AlgaeDensity_g_m3/1000.0)*self.currentChemical.Z_purewater
		self.Z_Algae["Chem_Dibenz_a_h_anthracene"]=(self.Chemical_RatioOfConcInAlgaeToConcDissolvedInWater*self.AlgaeDensity_g_m3/1000.0)*self.currentChemical.Z_purewater
		self.Z_Algae["Chem_Divalent_Mercury"]=(self.Chemical_RatioOfConcInAlgaeToConcDissolvedInWater*self.AlgaeDensity_g_m3/1000.0)*self.currentChemical.Z_purewater
		self.Z_Algae["Chem_Elemental_Mercury"]=(self.Chemical_RatioOfConcInAlgaeToConcDissolvedInWater*self.AlgaeDensity_g_m3/1000.0)*self.currentChemical.Z_purewater
		self.Z_Algae["Chem_Fluoranthene"]=(self.Chemical_RatioOfConcInAlgaeToConcDissolvedInWater*self.AlgaeDensity_g_m3/1000.0)*self.currentChemical.Z_purewater
		self.Z_Algae["Chem_Fluorene"]=(self.Chemical_RatioOfConcInAlgaeToConcDissolvedInWater*self.AlgaeDensity_g_m3/1000.0)*self.currentChemical.Z_purewater
		self.Z_Algae["Chem_Indeno_1_2_3_cd_pyrene"]=(self.Chemical_RatioOfConcInAlgaeToConcDissolvedInWater*self.AlgaeDensity_g_m3/1000.0)*self.currentChemical.Z_purewater
		self.Z_Algae["Chem_Lead"]=(self.Chemical_RatioOfConcInAlgaeToConcDissolvedInWater*self.AlgaeDensity_g_m3/1000.0)*self.currentChemical.Z_purewater
		self.Z_Algae["Chem_MethylMercury"]=(self.Chemical_RatioOfConcInAlgaeToConcDissolvedInWater*self.AlgaeDensity_g_m3/1000.0)*self.currentChemical.Z_purewater
		try:
			self.Chemical_Z_Algae=self.Z_Algae[self.currentChemical.Name]
		except:
			self.Chemical_Z_Algae=nan

		self.AlgaeSedimentationRate_m3_m2_day=()
		self.AlgaeSedimentationRate_m3_m2_day=self.AlgaeSedimentationRate_g_m2_day/self.AlgaeDensity_g_m3

		self.Area=()
		self.Area=containingVolumeElement.Area

		self.Depth=()
		self.Depth=self.containingVolumeElement.Height

		self.FractionMass_Algae={}
		self.FractionMass_Algae["Chem_1_2_3_4_6_7_8_9_OCDD"]=self.containingVolumeElement.Volume * (self.VolumeFraction_Algae) * self.Chemical_RatioOfConcInAlgaeToConcDissolvedInWater * self.AlgaeDensity_g_m3 * (self.Constants.m3_per_L) / self.Chemical_GenericDenominatorforCalculatingFractioninPhases
		self.FractionMass_Algae["Chem_1_2_3_4_6_7_8_9_OCDF"]=self.containingVolumeElement.Volume * (self.VolumeFraction_Algae) * self.Chemical_RatioOfConcInAlgaeToConcDissolvedInWater * self.AlgaeDensity_g_m3 * (self.Constants.m3_per_L) / self.Chemical_GenericDenominatorforCalculatingFractioninPhases
		self.FractionMass_Algae["Chem_1_2_3_4_6_7_8_HpCDD"]=self.containingVolumeElement.Volume * (self.VolumeFraction_Algae) * self.Chemical_RatioOfConcInAlgaeToConcDissolvedInWater * self.AlgaeDensity_g_m3 * (self.Constants.m3_per_L) / self.Chemical_GenericDenominatorforCalculatingFractioninPhases
		self.FractionMass_Algae["Chem_1_2_3_4_6_7_8_HpCDF"]=self.containingVolumeElement.Volume * (self.VolumeFraction_Algae) * self.Chemical_RatioOfConcInAlgaeToConcDissolvedInWater * self.AlgaeDensity_g_m3 * (self.Constants.m3_per_L) / self.Chemical_GenericDenominatorforCalculatingFractioninPhases
		self.FractionMass_Algae["Chem_1_2_3_4_7_8_9_HpCDF"]=self.containingVolumeElement.Volume * (self.VolumeFraction_Algae) * self.Chemical_RatioOfConcInAlgaeToConcDissolvedInWater * self.AlgaeDensity_g_m3 * (self.Constants.m3_per_L) / self.Chemical_GenericDenominatorforCalculatingFractioninPhases
		self.FractionMass_Algae["Chem_1_2_3_4_7_8_HxCDD"]=self.containingVolumeElement.Volume * (self.VolumeFraction_Algae) * self.Chemical_RatioOfConcInAlgaeToConcDissolvedInWater * self.AlgaeDensity_g_m3 * (self.Constants.m3_per_L) / self.Chemical_GenericDenominatorforCalculatingFractioninPhases
		self.FractionMass_Algae["Chem_1_2_3_4_7_8_HxCDF"]=self.containingVolumeElement.Volume * (self.VolumeFraction_Algae) * self.Chemical_RatioOfConcInAlgaeToConcDissolvedInWater * self.AlgaeDensity_g_m3 * (self.Constants.m3_per_L) / self.Chemical_GenericDenominatorforCalculatingFractioninPhases
		self.FractionMass_Algae["Chem_1_2_3_6_7_8_HxCDD"]=self.containingVolumeElement.Volume * (self.VolumeFraction_Algae) * self.Chemical_RatioOfConcInAlgaeToConcDissolvedInWater * self.AlgaeDensity_g_m3 * (self.Constants.m3_per_L) / self.Chemical_GenericDenominatorforCalculatingFractioninPhases
		self.FractionMass_Algae["Chem_1_2_3_6_7_8_HxCDF"]=self.containingVolumeElement.Volume * (self.VolumeFraction_Algae) * self.Chemical_RatioOfConcInAlgaeToConcDissolvedInWater * self.AlgaeDensity_g_m3 * (self.Constants.m3_per_L) / self.Chemical_GenericDenominatorforCalculatingFractioninPhases
		self.FractionMass_Algae["Chem_1_2_3_7_8_9_HxCDD"]=self.containingVolumeElement.Volume * (self.VolumeFraction_Algae) * self.Chemical_RatioOfConcInAlgaeToConcDissolvedInWater * self.AlgaeDensity_g_m3 * (self.Constants.m3_per_L) / self.Chemical_GenericDenominatorforCalculatingFractioninPhases
		self.FractionMass_Algae["Chem_1_2_3_7_8_9_HxCDF"]=self.containingVolumeElement.Volume * (self.VolumeFraction_Algae) * self.Chemical_RatioOfConcInAlgaeToConcDissolvedInWater * self.AlgaeDensity_g_m3 * (self.Constants.m3_per_L) / self.Chemical_GenericDenominatorforCalculatingFractioninPhases
		self.FractionMass_Algae["Chem_1_2_3_7_8_PeCDD"]=self.containingVolumeElement.Volume * (self.VolumeFraction_Algae) * self.Chemical_RatioOfConcInAlgaeToConcDissolvedInWater * self.AlgaeDensity_g_m3 * (self.Constants.m3_per_L) / self.Chemical_GenericDenominatorforCalculatingFractioninPhases
		self.FractionMass_Algae["Chem_1_2_3_7_8_PeCDF"]=self.containingVolumeElement.Volume * (self.VolumeFraction_Algae) * self.Chemical_RatioOfConcInAlgaeToConcDissolvedInWater * self.AlgaeDensity_g_m3 * (self.Constants.m3_per_L) / self.Chemical_GenericDenominatorforCalculatingFractioninPhases
		self.FractionMass_Algae["Chem_2_3_4_6_7_8_HxCDF"]=self.containingVolumeElement.Volume * (self.VolumeFraction_Algae) * self.Chemical_RatioOfConcInAlgaeToConcDissolvedInWater * self.AlgaeDensity_g_m3 * (self.Constants.m3_per_L) / self.Chemical_GenericDenominatorforCalculatingFractioninPhases
		self.FractionMass_Algae["Chem_2_3_4_7_8_PeCDF"]=self.containingVolumeElement.Volume * (self.VolumeFraction_Algae) * self.Chemical_RatioOfConcInAlgaeToConcDissolvedInWater * self.AlgaeDensity_g_m3 * (self.Constants.m3_per_L) / self.Chemical_GenericDenominatorforCalculatingFractioninPhases
		self.FractionMass_Algae["Chem_2_3_7_8_TCDD"]=self.containingVolumeElement.Volume * (self.VolumeFraction_Algae) * self.Chemical_RatioOfConcInAlgaeToConcDissolvedInWater * self.AlgaeDensity_g_m3 * (self.Constants.m3_per_L) / self.Chemical_GenericDenominatorforCalculatingFractioninPhases
		self.FractionMass_Algae["Chem_2_3_7_8_TCDF"]=self.containingVolumeElement.Volume * (self.VolumeFraction_Algae) * self.Chemical_RatioOfConcInAlgaeToConcDissolvedInWater * self.AlgaeDensity_g_m3 * (self.Constants.m3_per_L) / self.Chemical_GenericDenominatorforCalculatingFractioninPhases
		self.FractionMass_Algae["Chem_2_Methylnaphthalene"]=self.containingVolumeElement.Volume * (self.VolumeFraction_Algae) * self.Chemical_RatioOfConcInAlgaeToConcDissolvedInWater * self.AlgaeDensity_g_m3 * (self.Constants.m3_per_L) / self.Chemical_GenericDenominatorforCalculatingFractioninPhases
		self.FractionMass_Algae["Chem_7_12_Dimethylbenz_a_anthracene"]=self.containingVolumeElement.Volume * (self.VolumeFraction_Algae) * self.Chemical_RatioOfConcInAlgaeToConcDissolvedInWater * self.AlgaeDensity_g_m3 * (self.Constants.m3_per_L) / self.Chemical_GenericDenominatorforCalculatingFractioninPhases
		self.FractionMass_Algae["Chem_Acenaphthene"]=self.containingVolumeElement.Volume * (self.VolumeFraction_Algae) * self.Chemical_RatioOfConcInAlgaeToConcDissolvedInWater * self.AlgaeDensity_g_m3 * (self.Constants.m3_per_L) / self.Chemical_GenericDenominatorforCalculatingFractioninPhases
		self.FractionMass_Algae["Chem_Acenaphthylene"]=self.containingVolumeElement.Volume * (self.VolumeFraction_Algae) * self.Chemical_RatioOfConcInAlgaeToConcDissolvedInWater * self.AlgaeDensity_g_m3 * (self.Constants.m3_per_L) / self.Chemical_GenericDenominatorforCalculatingFractioninPhases
		self.FractionMass_Algae["Chem_Arsenic"]=self.containingVolumeElement.Volume * (self.VolumeFraction_Algae) * self.Chemical_RatioOfConcInAlgaeToConcDissolvedInWater * self.AlgaeDensity_g_m3 * (self.Constants.m3_per_L) / self.Chemical_GenericDenominatorforCalculatingFractioninPhases
		self.FractionMass_Algae["Chem_Benz_a_anthracene"]=self.containingVolumeElement.Volume * (self.VolumeFraction_Algae) * self.Chemical_RatioOfConcInAlgaeToConcDissolvedInWater * self.AlgaeDensity_g_m3 * (self.Constants.m3_per_L) / self.Chemical_GenericDenominatorforCalculatingFractioninPhases
		self.FractionMass_Algae["Chem_Benzo_A_Pyrene"]=self.containingVolumeElement.Volume * (self.VolumeFraction_Algae) * self.Chemical_RatioOfConcInAlgaeToConcDissolvedInWater * self.AlgaeDensity_g_m3 * (self.Constants.m3_per_L) / self.Chemical_GenericDenominatorforCalculatingFractioninPhases
		self.FractionMass_Algae["Chem_Benzo_b_fluoranthene"]=self.containingVolumeElement.Volume * (self.VolumeFraction_Algae) * self.Chemical_RatioOfConcInAlgaeToConcDissolvedInWater * self.AlgaeDensity_g_m3 * (self.Constants.m3_per_L) / self.Chemical_GenericDenominatorforCalculatingFractioninPhases
		self.FractionMass_Algae["Chem_Benzo_g_h_i_perylene"]=self.containingVolumeElement.Volume * (self.VolumeFraction_Algae) * self.Chemical_RatioOfConcInAlgaeToConcDissolvedInWater * self.AlgaeDensity_g_m3 * (self.Constants.m3_per_L) / self.Chemical_GenericDenominatorforCalculatingFractioninPhases
		self.FractionMass_Algae["Chem_Benzo_k_fluoranthene"]=self.containingVolumeElement.Volume * (self.VolumeFraction_Algae) * self.Chemical_RatioOfConcInAlgaeToConcDissolvedInWater * self.AlgaeDensity_g_m3 * (self.Constants.m3_per_L) / self.Chemical_GenericDenominatorforCalculatingFractioninPhases
		self.FractionMass_Algae["Chem_Cadmium"]=self.containingVolumeElement.Volume * (self.VolumeFraction_Algae) * self.Chemical_RatioOfConcInAlgaeToConcDissolvedInWater * self.AlgaeDensity_g_m3 * (self.Constants.m3_per_L) / self.Chemical_GenericDenominatorforCalculatingFractioninPhases
		self.FractionMass_Algae["Chem_Chrysene"]=self.containingVolumeElement.Volume * (self.VolumeFraction_Algae) * self.Chemical_RatioOfConcInAlgaeToConcDissolvedInWater * self.AlgaeDensity_g_m3 * (self.Constants.m3_per_L) / self.Chemical_GenericDenominatorforCalculatingFractioninPhases
		self.FractionMass_Algae["Chem_Dibenz_a_h_anthracene"]=self.containingVolumeElement.Volume * (self.VolumeFraction_Algae) * self.Chemical_RatioOfConcInAlgaeToConcDissolvedInWater * self.AlgaeDensity_g_m3 * (self.Constants.m3_per_L) / self.Chemical_GenericDenominatorforCalculatingFractioninPhases
		self.FractionMass_Algae["Chem_Divalent_Mercury"]=self.containingVolumeElement.Volume * (self.VolumeFraction_Algae) * self.Chemical_RatioOfConcInAlgaeToConcDissolvedInWater * self.AlgaeDensity_g_m3 * (self.Constants.m3_per_L) / self.Chemical_GenericDenominatorforCalculatingFractioninPhases
		self.FractionMass_Algae["Chem_Elemental_Mercury"]=self.containingVolumeElement.Volume * (self.VolumeFraction_Algae) * self.Chemical_RatioOfConcInAlgaeToConcDissolvedInWater * self.AlgaeDensity_g_m3 * (self.Constants.m3_per_L) / self.Chemical_GenericDenominatorforCalculatingFractioninPhases
		self.FractionMass_Algae["Chem_Fluoranthene"]=self.containingVolumeElement.Volume * (self.VolumeFraction_Algae) * self.Chemical_RatioOfConcInAlgaeToConcDissolvedInWater * self.AlgaeDensity_g_m3 * (self.Constants.m3_per_L) / self.Chemical_GenericDenominatorforCalculatingFractioninPhases
		self.FractionMass_Algae["Chem_Fluorene"]=self.containingVolumeElement.Volume * (self.VolumeFraction_Algae) * self.Chemical_RatioOfConcInAlgaeToConcDissolvedInWater * self.AlgaeDensity_g_m3 * (self.Constants.m3_per_L) / self.Chemical_GenericDenominatorforCalculatingFractioninPhases
		self.FractionMass_Algae["Chem_Indeno_1_2_3_cd_pyrene"]=self.containingVolumeElement.Volume * (self.VolumeFraction_Algae) * self.Chemical_RatioOfConcInAlgaeToConcDissolvedInWater * self.AlgaeDensity_g_m3 * (self.Constants.m3_per_L) / self.Chemical_GenericDenominatorforCalculatingFractioninPhases
		self.FractionMass_Algae["Chem_Lead"]=self.containingVolumeElement.Volume * (self.VolumeFraction_Algae) * self.Chemical_RatioOfConcInAlgaeToConcDissolvedInWater * self.AlgaeDensity_g_m3 * (self.Constants.m3_per_L) / self.Chemical_GenericDenominatorforCalculatingFractioninPhases
		self.FractionMass_Algae["Chem_MethylMercury"]=self.containingVolumeElement.Volume * (self.VolumeFraction_Algae) * self.Chemical_RatioOfConcInAlgaeToConcDissolvedInWater * self.AlgaeDensity_g_m3 * (self.Constants.m3_per_L) / self.Chemical_GenericDenominatorforCalculatingFractioninPhases
		try:
			self.Chemical_FractionMass_Algae=self.FractionMass_Algae[self.currentChemical.Name]
		except:
			self.Chemical_FractionMass_Algae=nan

		self.FractionMass_Dissolved={}
		self.FractionMass_Dissolved["Chem_1_2_3_4_6_7_8_9_OCDD"]=self.containingVolumeElement.Volume * (self.VolumeFraction_Liquid) / self.Chemical_GenericDenominatorforCalculatingFractioninPhases
		self.FractionMass_Dissolved["Chem_1_2_3_4_6_7_8_9_OCDF"]=self.containingVolumeElement.Volume * (self.VolumeFraction_Liquid) / self.Chemical_GenericDenominatorforCalculatingFractioninPhases
		self.FractionMass_Dissolved["Chem_1_2_3_4_6_7_8_HpCDD"]=self.containingVolumeElement.Volume * (self.VolumeFraction_Liquid) / self.Chemical_GenericDenominatorforCalculatingFractioninPhases
		self.FractionMass_Dissolved["Chem_1_2_3_4_6_7_8_HpCDF"]=self.containingVolumeElement.Volume * (self.VolumeFraction_Liquid) / self.Chemical_GenericDenominatorforCalculatingFractioninPhases
		self.FractionMass_Dissolved["Chem_1_2_3_4_7_8_9_HpCDF"]=self.containingVolumeElement.Volume * (self.VolumeFraction_Liquid) / self.Chemical_GenericDenominatorforCalculatingFractioninPhases
		self.FractionMass_Dissolved["Chem_1_2_3_4_7_8_HxCDD"]=self.containingVolumeElement.Volume * (self.VolumeFraction_Liquid) / self.Chemical_GenericDenominatorforCalculatingFractioninPhases
		self.FractionMass_Dissolved["Chem_1_2_3_4_7_8_HxCDF"]=self.containingVolumeElement.Volume * (self.VolumeFraction_Liquid) / self.Chemical_GenericDenominatorforCalculatingFractioninPhases
		self.FractionMass_Dissolved["Chem_1_2_3_6_7_8_HxCDD"]=self.containingVolumeElement.Volume * (self.VolumeFraction_Liquid) / self.Chemical_GenericDenominatorforCalculatingFractioninPhases
		self.FractionMass_Dissolved["Chem_1_2_3_6_7_8_HxCDF"]=self.containingVolumeElement.Volume * (self.VolumeFraction_Liquid) / self.Chemical_GenericDenominatorforCalculatingFractioninPhases
		self.FractionMass_Dissolved["Chem_1_2_3_7_8_9_HxCDD"]=self.containingVolumeElement.Volume * (self.VolumeFraction_Liquid) / self.Chemical_GenericDenominatorforCalculatingFractioninPhases
		self.FractionMass_Dissolved["Chem_1_2_3_7_8_9_HxCDF"]=self.containingVolumeElement.Volume * (self.VolumeFraction_Liquid) / self.Chemical_GenericDenominatorforCalculatingFractioninPhases
		self.FractionMass_Dissolved["Chem_1_2_3_7_8_PeCDD"]=self.containingVolumeElement.Volume * (self.VolumeFraction_Liquid) / self.Chemical_GenericDenominatorforCalculatingFractioninPhases
		self.FractionMass_Dissolved["Chem_1_2_3_7_8_PeCDF"]=self.containingVolumeElement.Volume * (self.VolumeFraction_Liquid) / self.Chemical_GenericDenominatorforCalculatingFractioninPhases
		self.FractionMass_Dissolved["Chem_2_3_4_6_7_8_HxCDF"]=self.containingVolumeElement.Volume * (self.VolumeFraction_Liquid) / self.Chemical_GenericDenominatorforCalculatingFractioninPhases
		self.FractionMass_Dissolved["Chem_2_3_4_7_8_PeCDF"]=self.containingVolumeElement.Volume * (self.VolumeFraction_Liquid) / self.Chemical_GenericDenominatorforCalculatingFractioninPhases
		self.FractionMass_Dissolved["Chem_2_3_7_8_TCDD"]=self.containingVolumeElement.Volume * (self.VolumeFraction_Liquid) / self.Chemical_GenericDenominatorforCalculatingFractioninPhases
		self.FractionMass_Dissolved["Chem_2_3_7_8_TCDF"]=self.containingVolumeElement.Volume * (self.VolumeFraction_Liquid) / self.Chemical_GenericDenominatorforCalculatingFractioninPhases
		self.FractionMass_Dissolved["Chem_2_Methylnaphthalene"]=self.containingVolumeElement.Volume * (self.VolumeFraction_Liquid) / self.Chemical_GenericDenominatorforCalculatingFractioninPhases
		self.FractionMass_Dissolved["Chem_7_12_Dimethylbenz_a_anthracene"]=self.containingVolumeElement.Volume * (self.VolumeFraction_Liquid) / self.Chemical_GenericDenominatorforCalculatingFractioninPhases
		self.FractionMass_Dissolved["Chem_Acenaphthene"]=self.containingVolumeElement.Volume * (self.VolumeFraction_Liquid) / self.Chemical_GenericDenominatorforCalculatingFractioninPhases
		self.FractionMass_Dissolved["Chem_Acenaphthylene"]=self.containingVolumeElement.Volume * (self.VolumeFraction_Liquid) / self.Chemical_GenericDenominatorforCalculatingFractioninPhases
		self.FractionMass_Dissolved["Chem_Arsenic"]=self.containingVolumeElement.Volume * (self.VolumeFraction_Liquid) / self.Chemical_GenericDenominatorforCalculatingFractioninPhases
		self.FractionMass_Dissolved["Chem_Benz_a_anthracene"]=self.containingVolumeElement.Volume * (self.VolumeFraction_Liquid) / self.Chemical_GenericDenominatorforCalculatingFractioninPhases
		self.FractionMass_Dissolved["Chem_Benzo_A_Pyrene"]=self.containingVolumeElement.Volume * (self.VolumeFraction_Liquid) / self.Chemical_GenericDenominatorforCalculatingFractioninPhases
		self.FractionMass_Dissolved["Chem_Benzo_b_fluoranthene"]=self.containingVolumeElement.Volume * (self.VolumeFraction_Liquid) / self.Chemical_GenericDenominatorforCalculatingFractioninPhases
		self.FractionMass_Dissolved["Chem_Benzo_g_h_i_perylene"]=self.containingVolumeElement.Volume * (self.VolumeFraction_Liquid) / self.Chemical_GenericDenominatorforCalculatingFractioninPhases
		self.FractionMass_Dissolved["Chem_Benzo_k_fluoranthene"]=self.containingVolumeElement.Volume * (self.VolumeFraction_Liquid) / self.Chemical_GenericDenominatorforCalculatingFractioninPhases
		self.FractionMass_Dissolved["Chem_Cadmium"]=self.containingVolumeElement.Volume * (self.VolumeFraction_Liquid) / self.Chemical_GenericDenominatorforCalculatingFractioninPhases
		self.FractionMass_Dissolved["Chem_Chrysene"]=self.containingVolumeElement.Volume * (self.VolumeFraction_Liquid) / self.Chemical_GenericDenominatorforCalculatingFractioninPhases
		self.FractionMass_Dissolved["Chem_Dibenz_a_h_anthracene"]=self.containingVolumeElement.Volume * (self.VolumeFraction_Liquid) / self.Chemical_GenericDenominatorforCalculatingFractioninPhases
		self.FractionMass_Dissolved["Chem_Divalent_Mercury"]=self.containingVolumeElement.Volume * (self.VolumeFraction_Liquid) / self.Chemical_GenericDenominatorforCalculatingFractioninPhases
		self.FractionMass_Dissolved["Chem_Elemental_Mercury"]=self.containingVolumeElement.Volume * (self.VolumeFraction_Liquid) / self.Chemical_GenericDenominatorforCalculatingFractioninPhases
		self.FractionMass_Dissolved["Chem_Fluoranthene"]=self.containingVolumeElement.Volume * (self.VolumeFraction_Liquid) / self.Chemical_GenericDenominatorforCalculatingFractioninPhases
		self.FractionMass_Dissolved["Chem_Fluorene"]=self.containingVolumeElement.Volume * (self.VolumeFraction_Liquid) / self.Chemical_GenericDenominatorforCalculatingFractioninPhases
		self.FractionMass_Dissolved["Chem_Indeno_1_2_3_cd_pyrene"]=self.containingVolumeElement.Volume * (self.VolumeFraction_Liquid) / self.Chemical_GenericDenominatorforCalculatingFractioninPhases
		self.FractionMass_Dissolved["Chem_Lead"]=self.containingVolumeElement.Volume * (self.VolumeFraction_Liquid) / self.Chemical_GenericDenominatorforCalculatingFractioninPhases
		self.FractionMass_Dissolved["Chem_MethylMercury"]=self.containingVolumeElement.Volume * (self.VolumeFraction_Liquid) / self.Chemical_GenericDenominatorforCalculatingFractioninPhases
		try:
			self.Chemical_FractionMass_Dissolved=self.FractionMass_Dissolved[self.currentChemical.Name]
		except:
			self.Chemical_FractionMass_Dissolved=nan

		self.FractionMass_Sorbed={}
		self.FractionMass_Sorbed["Chem_1_2_3_4_6_7_8_9_OCDD"]=self.containingVolumeElement.Volume * (self.VolumeFraction_Solid) * self.Chemical_Kd * self.Constants.m3_per_L * self.rho / self.Chemical_GenericDenominatorforCalculatingFractioninPhases
		self.FractionMass_Sorbed["Chem_1_2_3_4_6_7_8_9_OCDF"]=self.containingVolumeElement.Volume * (self.VolumeFraction_Solid) * self.Chemical_Kd * self.Constants.m3_per_L * self.rho / self.Chemical_GenericDenominatorforCalculatingFractioninPhases
		self.FractionMass_Sorbed["Chem_1_2_3_4_6_7_8_HpCDD"]=self.containingVolumeElement.Volume * (self.VolumeFraction_Solid) * self.Chemical_Kd * self.Constants.m3_per_L * self.rho / self.Chemical_GenericDenominatorforCalculatingFractioninPhases
		self.FractionMass_Sorbed["Chem_1_2_3_4_6_7_8_HpCDF"]=self.containingVolumeElement.Volume * (self.VolumeFraction_Solid) * self.Chemical_Kd * self.Constants.m3_per_L * self.rho / self.Chemical_GenericDenominatorforCalculatingFractioninPhases
		self.FractionMass_Sorbed["Chem_1_2_3_4_7_8_9_HpCDF"]=self.containingVolumeElement.Volume * (self.VolumeFraction_Solid) * self.Chemical_Kd * self.Constants.m3_per_L * self.rho / self.Chemical_GenericDenominatorforCalculatingFractioninPhases
		self.FractionMass_Sorbed["Chem_1_2_3_4_7_8_HxCDD"]=self.containingVolumeElement.Volume * (self.VolumeFraction_Solid) * self.Chemical_Kd * self.Constants.m3_per_L * self.rho / self.Chemical_GenericDenominatorforCalculatingFractioninPhases
		self.FractionMass_Sorbed["Chem_1_2_3_4_7_8_HxCDF"]=self.containingVolumeElement.Volume * (self.VolumeFraction_Solid) * self.Chemical_Kd * self.Constants.m3_per_L * self.rho / self.Chemical_GenericDenominatorforCalculatingFractioninPhases
		self.FractionMass_Sorbed["Chem_1_2_3_6_7_8_HxCDD"]=self.containingVolumeElement.Volume * (self.VolumeFraction_Solid) * self.Chemical_Kd * self.Constants.m3_per_L * self.rho / self.Chemical_GenericDenominatorforCalculatingFractioninPhases
		self.FractionMass_Sorbed["Chem_1_2_3_6_7_8_HxCDF"]=self.containingVolumeElement.Volume * (self.VolumeFraction_Solid) * self.Chemical_Kd * self.Constants.m3_per_L * self.rho / self.Chemical_GenericDenominatorforCalculatingFractioninPhases
		self.FractionMass_Sorbed["Chem_1_2_3_7_8_9_HxCDD"]=self.containingVolumeElement.Volume * (self.VolumeFraction_Solid) * self.Chemical_Kd * self.Constants.m3_per_L * self.rho / self.Chemical_GenericDenominatorforCalculatingFractioninPhases
		self.FractionMass_Sorbed["Chem_1_2_3_7_8_9_HxCDF"]=self.containingVolumeElement.Volume * (self.VolumeFraction_Solid) * self.Chemical_Kd * self.Constants.m3_per_L * self.rho / self.Chemical_GenericDenominatorforCalculatingFractioninPhases
		self.FractionMass_Sorbed["Chem_1_2_3_7_8_PeCDD"]=self.containingVolumeElement.Volume * (self.VolumeFraction_Solid) * self.Chemical_Kd * self.Constants.m3_per_L * self.rho / self.Chemical_GenericDenominatorforCalculatingFractioninPhases
		self.FractionMass_Sorbed["Chem_1_2_3_7_8_PeCDF"]=self.containingVolumeElement.Volume * (self.VolumeFraction_Solid) * self.Chemical_Kd * self.Constants.m3_per_L * self.rho / self.Chemical_GenericDenominatorforCalculatingFractioninPhases
		self.FractionMass_Sorbed["Chem_2_3_4_6_7_8_HxCDF"]=self.containingVolumeElement.Volume * (self.VolumeFraction_Solid) * self.Chemical_Kd * self.Constants.m3_per_L * self.rho / self.Chemical_GenericDenominatorforCalculatingFractioninPhases
		self.FractionMass_Sorbed["Chem_2_3_4_7_8_PeCDF"]=self.containingVolumeElement.Volume * (self.VolumeFraction_Solid) * self.Chemical_Kd * self.Constants.m3_per_L * self.rho / self.Chemical_GenericDenominatorforCalculatingFractioninPhases
		self.FractionMass_Sorbed["Chem_2_3_7_8_TCDD"]=self.containingVolumeElement.Volume * (self.VolumeFraction_Solid) * self.Chemical_Kd * self.Constants.m3_per_L * self.rho / self.Chemical_GenericDenominatorforCalculatingFractioninPhases
		self.FractionMass_Sorbed["Chem_2_3_7_8_TCDF"]=self.containingVolumeElement.Volume * (self.VolumeFraction_Solid) * self.Chemical_Kd * self.Constants.m3_per_L * self.rho / self.Chemical_GenericDenominatorforCalculatingFractioninPhases
		self.FractionMass_Sorbed["Chem_2_Methylnaphthalene"]=self.containingVolumeElement.Volume * (self.VolumeFraction_Solid) * self.Chemical_Kd * self.Constants.m3_per_L * self.rho / self.Chemical_GenericDenominatorforCalculatingFractioninPhases
		self.FractionMass_Sorbed["Chem_7_12_Dimethylbenz_a_anthracene"]=self.containingVolumeElement.Volume * (self.VolumeFraction_Solid) * self.Chemical_Kd * self.Constants.m3_per_L * self.rho / self.Chemical_GenericDenominatorforCalculatingFractioninPhases
		self.FractionMass_Sorbed["Chem_Acenaphthene"]=self.containingVolumeElement.Volume * (self.VolumeFraction_Solid) * self.Chemical_Kd * self.Constants.m3_per_L * self.rho / self.Chemical_GenericDenominatorforCalculatingFractioninPhases
		self.FractionMass_Sorbed["Chem_Acenaphthylene"]=self.containingVolumeElement.Volume * (self.VolumeFraction_Solid) * self.Chemical_Kd * self.Constants.m3_per_L * self.rho / self.Chemical_GenericDenominatorforCalculatingFractioninPhases
		self.FractionMass_Sorbed["Chem_Arsenic"]=self.containingVolumeElement.Volume * (self.VolumeFraction_Solid) * self.Chemical_Kd * self.Constants.m3_per_L * self.rho / self.Chemical_GenericDenominatorforCalculatingFractioninPhases
		self.FractionMass_Sorbed["Chem_Benz_a_anthracene"]=self.containingVolumeElement.Volume * (self.VolumeFraction_Solid) * self.Chemical_Kd * self.Constants.m3_per_L * self.rho / self.Chemical_GenericDenominatorforCalculatingFractioninPhases
		self.FractionMass_Sorbed["Chem_Benzo_A_Pyrene"]=self.containingVolumeElement.Volume * (self.VolumeFraction_Solid) * self.Chemical_Kd * self.Constants.m3_per_L * self.rho / self.Chemical_GenericDenominatorforCalculatingFractioninPhases
		self.FractionMass_Sorbed["Chem_Benzo_b_fluoranthene"]=self.containingVolumeElement.Volume * (self.VolumeFraction_Solid) * self.Chemical_Kd * self.Constants.m3_per_L * self.rho / self.Chemical_GenericDenominatorforCalculatingFractioninPhases
		self.FractionMass_Sorbed["Chem_Benzo_g_h_i_perylene"]=self.containingVolumeElement.Volume * (self.VolumeFraction_Solid) * self.Chemical_Kd * self.Constants.m3_per_L * self.rho / self.Chemical_GenericDenominatorforCalculatingFractioninPhases
		self.FractionMass_Sorbed["Chem_Benzo_k_fluoranthene"]=self.containingVolumeElement.Volume * (self.VolumeFraction_Solid) * self.Chemical_Kd * self.Constants.m3_per_L * self.rho / self.Chemical_GenericDenominatorforCalculatingFractioninPhases
		self.FractionMass_Sorbed["Chem_Cadmium"]=self.containingVolumeElement.Volume * (self.VolumeFraction_Solid) * self.Chemical_Kd * self.Constants.m3_per_L * self.rho / self.Chemical_GenericDenominatorforCalculatingFractioninPhases
		self.FractionMass_Sorbed["Chem_Chrysene"]=self.containingVolumeElement.Volume * (self.VolumeFraction_Solid) * self.Chemical_Kd * self.Constants.m3_per_L * self.rho / self.Chemical_GenericDenominatorforCalculatingFractioninPhases
		self.FractionMass_Sorbed["Chem_Dibenz_a_h_anthracene"]=self.containingVolumeElement.Volume * (self.VolumeFraction_Solid) * self.Chemical_Kd * self.Constants.m3_per_L * self.rho / self.Chemical_GenericDenominatorforCalculatingFractioninPhases
		self.FractionMass_Sorbed["Chem_Divalent_Mercury"]=self.containingVolumeElement.Volume * (self.VolumeFraction_Solid) * self.Chemical_Kd * self.Constants.m3_per_L * self.rho / self.Chemical_GenericDenominatorforCalculatingFractioninPhases
		self.FractionMass_Sorbed["Chem_Elemental_Mercury"]=self.containingVolumeElement.Volume * (self.VolumeFraction_Solid) * self.Chemical_Kd * self.Constants.m3_per_L * self.rho / self.Chemical_GenericDenominatorforCalculatingFractioninPhases
		self.FractionMass_Sorbed["Chem_Fluoranthene"]=self.containingVolumeElement.Volume * (self.VolumeFraction_Solid) * self.Chemical_Kd * self.Constants.m3_per_L * self.rho / self.Chemical_GenericDenominatorforCalculatingFractioninPhases
		self.FractionMass_Sorbed["Chem_Fluorene"]=self.containingVolumeElement.Volume * (self.VolumeFraction_Solid) * self.Chemical_Kd * self.Constants.m3_per_L * self.rho / self.Chemical_GenericDenominatorforCalculatingFractioninPhases
		self.FractionMass_Sorbed["Chem_Indeno_1_2_3_cd_pyrene"]=self.containingVolumeElement.Volume * (self.VolumeFraction_Solid) * self.Chemical_Kd * self.Constants.m3_per_L * self.rho / self.Chemical_GenericDenominatorforCalculatingFractioninPhases
		self.FractionMass_Sorbed["Chem_Lead"]=self.containingVolumeElement.Volume * (self.VolumeFraction_Solid) * self.Chemical_Kd * self.Constants.m3_per_L * self.rho / self.Chemical_GenericDenominatorforCalculatingFractioninPhases
		self.FractionMass_Sorbed["Chem_MethylMercury"]=self.containingVolumeElement.Volume * (self.VolumeFraction_Solid) * self.Chemical_Kd * self.Constants.m3_per_L * self.rho / self.Chemical_GenericDenominatorforCalculatingFractioninPhases
		try:
			self.Chemical_FractionMass_Sorbed=self.FractionMass_Sorbed[self.currentChemical.Name]
		except:
			self.Chemical_FractionMass_Sorbed=nan

		self.GenericDenominatorforCalculatingFractioninPhases={}
		self.GenericDenominatorforCalculatingFractioninPhases["Chem_1_2_3_4_6_7_8_9_OCDD"]=self.containingVolumeElement.Volume * (self.VolumeFraction_Algae * self.Chemical_RatioOfConcInAlgaeToConcDissolvedInWater * self.AlgaeDensity_g_m3 * (self.Constants.m3_per_L)  + self.VolumeFraction_Solid * self.Chemical_Kd * self.Constants.m3_per_L * self.rho + self.VolumeFraction_Liquid )
		self.GenericDenominatorforCalculatingFractioninPhases["Chem_1_2_3_4_6_7_8_9_OCDF"]=self.containingVolumeElement.Volume * (self.VolumeFraction_Algae * self.Chemical_RatioOfConcInAlgaeToConcDissolvedInWater * self.AlgaeDensity_g_m3 * (self.Constants.m3_per_L)  + self.VolumeFraction_Solid * self.Chemical_Kd * self.Constants.m3_per_L * self.rho + self.VolumeFraction_Liquid )
		self.GenericDenominatorforCalculatingFractioninPhases["Chem_1_2_3_4_6_7_8_HpCDD"]=self.containingVolumeElement.Volume * (self.VolumeFraction_Algae * self.Chemical_RatioOfConcInAlgaeToConcDissolvedInWater * self.AlgaeDensity_g_m3 * (self.Constants.m3_per_L)  + self.VolumeFraction_Solid * self.Chemical_Kd * self.Constants.m3_per_L * self.rho + self.VolumeFraction_Liquid )
		self.GenericDenominatorforCalculatingFractioninPhases["Chem_1_2_3_4_6_7_8_HpCDF"]=self.containingVolumeElement.Volume * (self.VolumeFraction_Algae * self.Chemical_RatioOfConcInAlgaeToConcDissolvedInWater * self.AlgaeDensity_g_m3 * (self.Constants.m3_per_L)  + self.VolumeFraction_Solid * self.Chemical_Kd * self.Constants.m3_per_L * self.rho + self.VolumeFraction_Liquid )
		self.GenericDenominatorforCalculatingFractioninPhases["Chem_1_2_3_4_7_8_9_HpCDF"]=self.containingVolumeElement.Volume * (self.VolumeFraction_Algae * self.Chemical_RatioOfConcInAlgaeToConcDissolvedInWater * self.AlgaeDensity_g_m3 * (self.Constants.m3_per_L)  + self.VolumeFraction_Solid * self.Chemical_Kd * self.Constants.m3_per_L * self.rho + self.VolumeFraction_Liquid )
		self.GenericDenominatorforCalculatingFractioninPhases["Chem_1_2_3_4_7_8_HxCDD"]=self.containingVolumeElement.Volume * (self.VolumeFraction_Algae * self.Chemical_RatioOfConcInAlgaeToConcDissolvedInWater * self.AlgaeDensity_g_m3 * (self.Constants.m3_per_L)  + self.VolumeFraction_Solid * self.Chemical_Kd * self.Constants.m3_per_L * self.rho + self.VolumeFraction_Liquid )
		self.GenericDenominatorforCalculatingFractioninPhases["Chem_1_2_3_4_7_8_HxCDF"]=self.containingVolumeElement.Volume * (self.VolumeFraction_Algae * self.Chemical_RatioOfConcInAlgaeToConcDissolvedInWater * self.AlgaeDensity_g_m3 * (self.Constants.m3_per_L)  + self.VolumeFraction_Solid * self.Chemical_Kd * self.Constants.m3_per_L * self.rho + self.VolumeFraction_Liquid )
		self.GenericDenominatorforCalculatingFractioninPhases["Chem_1_2_3_6_7_8_HxCDD"]=self.containingVolumeElement.Volume * (self.VolumeFraction_Algae * self.Chemical_RatioOfConcInAlgaeToConcDissolvedInWater * self.AlgaeDensity_g_m3 * (self.Constants.m3_per_L)  + self.VolumeFraction_Solid * self.Chemical_Kd * self.Constants.m3_per_L * self.rho + self.VolumeFraction_Liquid )
		self.GenericDenominatorforCalculatingFractioninPhases["Chem_1_2_3_6_7_8_HxCDF"]=self.containingVolumeElement.Volume * (self.VolumeFraction_Algae * self.Chemical_RatioOfConcInAlgaeToConcDissolvedInWater * self.AlgaeDensity_g_m3 * (self.Constants.m3_per_L)  + self.VolumeFraction_Solid * self.Chemical_Kd * self.Constants.m3_per_L * self.rho + self.VolumeFraction_Liquid )
		self.GenericDenominatorforCalculatingFractioninPhases["Chem_1_2_3_7_8_9_HxCDD"]=self.containingVolumeElement.Volume * (self.VolumeFraction_Algae * self.Chemical_RatioOfConcInAlgaeToConcDissolvedInWater * self.AlgaeDensity_g_m3 * (self.Constants.m3_per_L)  + self.VolumeFraction_Solid * self.Chemical_Kd * self.Constants.m3_per_L * self.rho + self.VolumeFraction_Liquid )
		self.GenericDenominatorforCalculatingFractioninPhases["Chem_1_2_3_7_8_9_HxCDF"]=self.containingVolumeElement.Volume * (self.VolumeFraction_Algae * self.Chemical_RatioOfConcInAlgaeToConcDissolvedInWater * self.AlgaeDensity_g_m3 * (self.Constants.m3_per_L)  + self.VolumeFraction_Solid * self.Chemical_Kd * self.Constants.m3_per_L * self.rho + self.VolumeFraction_Liquid )
		self.GenericDenominatorforCalculatingFractioninPhases["Chem_1_2_3_7_8_PeCDD"]=self.containingVolumeElement.Volume * (self.VolumeFraction_Algae * self.Chemical_RatioOfConcInAlgaeToConcDissolvedInWater * self.AlgaeDensity_g_m3 * (self.Constants.m3_per_L)  + self.VolumeFraction_Solid * self.Chemical_Kd * self.Constants.m3_per_L * self.rho + self.VolumeFraction_Liquid )
		self.GenericDenominatorforCalculatingFractioninPhases["Chem_1_2_3_7_8_PeCDF"]=self.containingVolumeElement.Volume * (self.VolumeFraction_Algae * self.Chemical_RatioOfConcInAlgaeToConcDissolvedInWater * self.AlgaeDensity_g_m3 * (self.Constants.m3_per_L)  + self.VolumeFraction_Solid * self.Chemical_Kd * self.Constants.m3_per_L * self.rho + self.VolumeFraction_Liquid )
		self.GenericDenominatorforCalculatingFractioninPhases["Chem_2_3_4_6_7_8_HxCDF"]=self.containingVolumeElement.Volume * (self.VolumeFraction_Algae * self.Chemical_RatioOfConcInAlgaeToConcDissolvedInWater * self.AlgaeDensity_g_m3 * (self.Constants.m3_per_L)  + self.VolumeFraction_Solid * self.Chemical_Kd * self.Constants.m3_per_L * self.rho + self.VolumeFraction_Liquid )
		self.GenericDenominatorforCalculatingFractioninPhases["Chem_2_3_4_7_8_PeCDF"]=self.containingVolumeElement.Volume * (self.VolumeFraction_Algae * self.Chemical_RatioOfConcInAlgaeToConcDissolvedInWater * self.AlgaeDensity_g_m3 * (self.Constants.m3_per_L)  + self.VolumeFraction_Solid * self.Chemical_Kd * self.Constants.m3_per_L * self.rho + self.VolumeFraction_Liquid )
		self.GenericDenominatorforCalculatingFractioninPhases["Chem_2_3_7_8_TCDD"]=self.containingVolumeElement.Volume * (self.VolumeFraction_Algae * self.Chemical_RatioOfConcInAlgaeToConcDissolvedInWater * self.AlgaeDensity_g_m3 * (self.Constants.m3_per_L)  + self.VolumeFraction_Solid * self.Chemical_Kd * self.Constants.m3_per_L * self.rho + self.VolumeFraction_Liquid )
		self.GenericDenominatorforCalculatingFractioninPhases["Chem_2_3_7_8_TCDF"]=self.containingVolumeElement.Volume * (self.VolumeFraction_Algae * self.Chemical_RatioOfConcInAlgaeToConcDissolvedInWater * self.AlgaeDensity_g_m3 * (self.Constants.m3_per_L)  + self.VolumeFraction_Solid * self.Chemical_Kd * self.Constants.m3_per_L * self.rho + self.VolumeFraction_Liquid )
		self.GenericDenominatorforCalculatingFractioninPhases["Chem_2_Methylnaphthalene"]=self.containingVolumeElement.Volume * (self.VolumeFraction_Algae * self.Chemical_RatioOfConcInAlgaeToConcDissolvedInWater * self.AlgaeDensity_g_m3 * (self.Constants.m3_per_L)  + self.VolumeFraction_Solid * self.Chemical_Kd * self.Constants.m3_per_L * self.rho + self.VolumeFraction_Liquid )
		self.GenericDenominatorforCalculatingFractioninPhases["Chem_7_12_Dimethylbenz_a_anthracene"]=self.containingVolumeElement.Volume * (self.VolumeFraction_Algae * self.Chemical_RatioOfConcInAlgaeToConcDissolvedInWater * self.AlgaeDensity_g_m3 * (self.Constants.m3_per_L)  + self.VolumeFraction_Solid * self.Chemical_Kd * self.Constants.m3_per_L * self.rho + self.VolumeFraction_Liquid )
		self.GenericDenominatorforCalculatingFractioninPhases["Chem_Acenaphthene"]=self.containingVolumeElement.Volume * (self.VolumeFraction_Algae * self.Chemical_RatioOfConcInAlgaeToConcDissolvedInWater * self.AlgaeDensity_g_m3 * (self.Constants.m3_per_L)  + self.VolumeFraction_Solid * self.Chemical_Kd * self.Constants.m3_per_L * self.rho + self.VolumeFraction_Liquid )
		self.GenericDenominatorforCalculatingFractioninPhases["Chem_Acenaphthylene"]=self.containingVolumeElement.Volume * (self.VolumeFraction_Algae * self.Chemical_RatioOfConcInAlgaeToConcDissolvedInWater * self.AlgaeDensity_g_m3 * (self.Constants.m3_per_L)  + self.VolumeFraction_Solid * self.Chemical_Kd * self.Constants.m3_per_L * self.rho + self.VolumeFraction_Liquid )
		self.GenericDenominatorforCalculatingFractioninPhases["Chem_Arsenic"]=self.containingVolumeElement.Volume * (self.VolumeFraction_Algae * self.Chemical_RatioOfConcInAlgaeToConcDissolvedInWater * self.AlgaeDensity_g_m3 * (self.Constants.m3_per_L)  + self.VolumeFraction_Solid * self.Chemical_Kd * self.Constants.m3_per_L * self.rho + self.VolumeFraction_Liquid )
		self.GenericDenominatorforCalculatingFractioninPhases["Chem_Benz_a_anthracene"]=self.containingVolumeElement.Volume * (self.VolumeFraction_Algae * self.Chemical_RatioOfConcInAlgaeToConcDissolvedInWater * self.AlgaeDensity_g_m3 * (self.Constants.m3_per_L)  + self.VolumeFraction_Solid * self.Chemical_Kd * self.Constants.m3_per_L * self.rho + self.VolumeFraction_Liquid )
		self.GenericDenominatorforCalculatingFractioninPhases["Chem_Benzo_A_Pyrene"]=self.containingVolumeElement.Volume * (self.VolumeFraction_Algae * self.Chemical_RatioOfConcInAlgaeToConcDissolvedInWater * self.AlgaeDensity_g_m3 * (self.Constants.m3_per_L)  + self.VolumeFraction_Solid * self.Chemical_Kd * self.Constants.m3_per_L * self.rho + self.VolumeFraction_Liquid )
		self.GenericDenominatorforCalculatingFractioninPhases["Chem_Benzo_b_fluoranthene"]=self.containingVolumeElement.Volume * (self.VolumeFraction_Algae * self.Chemical_RatioOfConcInAlgaeToConcDissolvedInWater * self.AlgaeDensity_g_m3 * (self.Constants.m3_per_L)  + self.VolumeFraction_Solid * self.Chemical_Kd * self.Constants.m3_per_L * self.rho + self.VolumeFraction_Liquid )
		self.GenericDenominatorforCalculatingFractioninPhases["Chem_Benzo_g_h_i_perylene"]=self.containingVolumeElement.Volume * (self.VolumeFraction_Algae * self.Chemical_RatioOfConcInAlgaeToConcDissolvedInWater * self.AlgaeDensity_g_m3 * (self.Constants.m3_per_L)  + self.VolumeFraction_Solid * self.Chemical_Kd * self.Constants.m3_per_L * self.rho + self.VolumeFraction_Liquid )
		self.GenericDenominatorforCalculatingFractioninPhases["Chem_Benzo_k_fluoranthene"]=self.containingVolumeElement.Volume * (self.VolumeFraction_Algae * self.Chemical_RatioOfConcInAlgaeToConcDissolvedInWater * self.AlgaeDensity_g_m3 * (self.Constants.m3_per_L)  + self.VolumeFraction_Solid * self.Chemical_Kd * self.Constants.m3_per_L * self.rho + self.VolumeFraction_Liquid )
		self.GenericDenominatorforCalculatingFractioninPhases["Chem_Cadmium"]=self.containingVolumeElement.Volume * (self.VolumeFraction_Algae * self.Chemical_RatioOfConcInAlgaeToConcDissolvedInWater * self.AlgaeDensity_g_m3 * (self.Constants.m3_per_L)  + self.VolumeFraction_Solid * self.Chemical_Kd * self.Constants.m3_per_L * self.rho + self.VolumeFraction_Liquid )
		self.GenericDenominatorforCalculatingFractioninPhases["Chem_Chrysene"]=self.containingVolumeElement.Volume * (self.VolumeFraction_Algae * self.Chemical_RatioOfConcInAlgaeToConcDissolvedInWater * self.AlgaeDensity_g_m3 * (self.Constants.m3_per_L)  + self.VolumeFraction_Solid * self.Chemical_Kd * self.Constants.m3_per_L * self.rho + self.VolumeFraction_Liquid )
		self.GenericDenominatorforCalculatingFractioninPhases["Chem_Dibenz_a_h_anthracene"]=self.containingVolumeElement.Volume * (self.VolumeFraction_Algae * self.Chemical_RatioOfConcInAlgaeToConcDissolvedInWater * self.AlgaeDensity_g_m3 * (self.Constants.m3_per_L)  + self.VolumeFraction_Solid * self.Chemical_Kd * self.Constants.m3_per_L * self.rho + self.VolumeFraction_Liquid )
		self.GenericDenominatorforCalculatingFractioninPhases["Chem_Divalent_Mercury"]=self.containingVolumeElement.Volume * (self.VolumeFraction_Algae * self.Chemical_RatioOfConcInAlgaeToConcDissolvedInWater * self.AlgaeDensity_g_m3 * (self.Constants.m3_per_L)  + self.VolumeFraction_Solid * self.Chemical_Kd * self.Constants.m3_per_L * self.rho + self.VolumeFraction_Liquid )
		self.GenericDenominatorforCalculatingFractioninPhases["Chem_Elemental_Mercury"]=self.containingVolumeElement.Volume * (self.VolumeFraction_Algae * self.Chemical_RatioOfConcInAlgaeToConcDissolvedInWater * self.AlgaeDensity_g_m3 * (self.Constants.m3_per_L)  + self.VolumeFraction_Solid * self.Chemical_Kd * self.Constants.m3_per_L * self.rho + self.VolumeFraction_Liquid )
		self.GenericDenominatorforCalculatingFractioninPhases["Chem_Fluoranthene"]=self.containingVolumeElement.Volume * (self.VolumeFraction_Algae * self.Chemical_RatioOfConcInAlgaeToConcDissolvedInWater * self.AlgaeDensity_g_m3 * (self.Constants.m3_per_L)  + self.VolumeFraction_Solid * self.Chemical_Kd * self.Constants.m3_per_L * self.rho + self.VolumeFraction_Liquid )
		self.GenericDenominatorforCalculatingFractioninPhases["Chem_Fluorene"]=self.containingVolumeElement.Volume * (self.VolumeFraction_Algae * self.Chemical_RatioOfConcInAlgaeToConcDissolvedInWater * self.AlgaeDensity_g_m3 * (self.Constants.m3_per_L)  + self.VolumeFraction_Solid * self.Chemical_Kd * self.Constants.m3_per_L * self.rho + self.VolumeFraction_Liquid )
		self.GenericDenominatorforCalculatingFractioninPhases["Chem_Indeno_1_2_3_cd_pyrene"]=self.containingVolumeElement.Volume * (self.VolumeFraction_Algae * self.Chemical_RatioOfConcInAlgaeToConcDissolvedInWater * self.AlgaeDensity_g_m3 * (self.Constants.m3_per_L)  + self.VolumeFraction_Solid * self.Chemical_Kd * self.Constants.m3_per_L * self.rho + self.VolumeFraction_Liquid )
		self.GenericDenominatorforCalculatingFractioninPhases["Chem_Lead"]=self.containingVolumeElement.Volume * (self.VolumeFraction_Algae * self.Chemical_RatioOfConcInAlgaeToConcDissolvedInWater * self.AlgaeDensity_g_m3 * (self.Constants.m3_per_L)  + self.VolumeFraction_Solid * self.Chemical_Kd * self.Constants.m3_per_L * self.rho + self.VolumeFraction_Liquid )
		self.GenericDenominatorforCalculatingFractioninPhases["Chem_MethylMercury"]=self.containingVolumeElement.Volume * (self.VolumeFraction_Algae * self.Chemical_RatioOfConcInAlgaeToConcDissolvedInWater * self.AlgaeDensity_g_m3 * (self.Constants.m3_per_L)  + self.VolumeFraction_Solid * self.Chemical_Kd * self.Constants.m3_per_L * self.rho + self.VolumeFraction_Liquid )
		try:
			self.Chemical_GenericDenominatorforCalculatingFractioninPhases=self.GenericDenominatorforCalculatingFractioninPhases[self.currentChemical.Name]
		except:
			self.Chemical_GenericDenominatorforCalculatingFractioninPhases=nan

		self.Height=()
		self.Height=containingVolumeElement.Height

		self.MeanDepth_m=()
		self.MeanDepth_m=(containingVolumeElement.Top + containingVolumeElement.Bottom)/2.0

		self.TotalAlgaeMass=()
		self.TotalAlgaeMass=self.containingVolumeElement.Volume*self.VolumeFraction_Algae*self.AlgaeDensity_g_m3 * self.Constants.kg_per_g

		self.Volume=()
		self.Volume=containingVolumeElement.Volume

		self.VolumeFraction_Liquid=()
		self.VolumeFraction_Liquid=1 - self.VolumeFraction_Solid - self.VolumeFraction_Algae

		self.WaterTemperature_C=()
		self.WaterTemperature_C=containingVolumeElement.WaterTemperature_K - 273

		self.Z_Total={}
		self.Z_Total["Chem_1_2_3_4_6_7_8_9_OCDD"]=self.Chemical_Z_Liquid *self.VolumeFraction_Liquid +self.Chemical_Z_Solid *self.VolumeFraction_Solid + self.Chemical_Z_Algae*self.VolumeFraction_Algae
		self.Z_Total["Chem_1_2_3_4_6_7_8_9_OCDF"]=self.Chemical_Z_Liquid *self.VolumeFraction_Liquid +self.Chemical_Z_Solid *self.VolumeFraction_Solid + self.Chemical_Z_Algae*self.VolumeFraction_Algae
		self.Z_Total["Chem_1_2_3_4_6_7_8_HpCDD"]=self.Chemical_Z_Liquid *self.VolumeFraction_Liquid +self.Chemical_Z_Solid *self.VolumeFraction_Solid + self.Chemical_Z_Algae*self.VolumeFraction_Algae
		self.Z_Total["Chem_1_2_3_4_6_7_8_HpCDF"]=self.Chemical_Z_Liquid *self.VolumeFraction_Liquid +self.Chemical_Z_Solid *self.VolumeFraction_Solid + self.Chemical_Z_Algae*self.VolumeFraction_Algae
		self.Z_Total["Chem_1_2_3_4_7_8_9_HpCDF"]=self.Chemical_Z_Liquid *self.VolumeFraction_Liquid +self.Chemical_Z_Solid *self.VolumeFraction_Solid + self.Chemical_Z_Algae*self.VolumeFraction_Algae
		self.Z_Total["Chem_1_2_3_4_7_8_HxCDD"]=self.Chemical_Z_Liquid *self.VolumeFraction_Liquid +self.Chemical_Z_Solid *self.VolumeFraction_Solid + self.Chemical_Z_Algae*self.VolumeFraction_Algae
		self.Z_Total["Chem_1_2_3_4_7_8_HxCDF"]=self.Chemical_Z_Liquid *self.VolumeFraction_Liquid +self.Chemical_Z_Solid *self.VolumeFraction_Solid + self.Chemical_Z_Algae*self.VolumeFraction_Algae
		self.Z_Total["Chem_1_2_3_6_7_8_HxCDD"]=self.Chemical_Z_Liquid *self.VolumeFraction_Liquid +self.Chemical_Z_Solid *self.VolumeFraction_Solid + self.Chemical_Z_Algae*self.VolumeFraction_Algae
		self.Z_Total["Chem_1_2_3_6_7_8_HxCDF"]=self.Chemical_Z_Liquid *self.VolumeFraction_Liquid +self.Chemical_Z_Solid *self.VolumeFraction_Solid + self.Chemical_Z_Algae*self.VolumeFraction_Algae
		self.Z_Total["Chem_1_2_3_7_8_9_HxCDD"]=self.Chemical_Z_Liquid *self.VolumeFraction_Liquid +self.Chemical_Z_Solid *self.VolumeFraction_Solid + self.Chemical_Z_Algae*self.VolumeFraction_Algae
		self.Z_Total["Chem_1_2_3_7_8_9_HxCDF"]=self.Chemical_Z_Liquid *self.VolumeFraction_Liquid +self.Chemical_Z_Solid *self.VolumeFraction_Solid + self.Chemical_Z_Algae*self.VolumeFraction_Algae
		self.Z_Total["Chem_1_2_3_7_8_PeCDD"]=self.Chemical_Z_Liquid *self.VolumeFraction_Liquid +self.Chemical_Z_Solid *self.VolumeFraction_Solid + self.Chemical_Z_Algae*self.VolumeFraction_Algae
		self.Z_Total["Chem_1_2_3_7_8_PeCDF"]=self.Chemical_Z_Liquid *self.VolumeFraction_Liquid +self.Chemical_Z_Solid *self.VolumeFraction_Solid + self.Chemical_Z_Algae*self.VolumeFraction_Algae
		self.Z_Total["Chem_2_3_4_6_7_8_HxCDF"]=self.Chemical_Z_Liquid *self.VolumeFraction_Liquid +self.Chemical_Z_Solid *self.VolumeFraction_Solid + self.Chemical_Z_Algae*self.VolumeFraction_Algae
		self.Z_Total["Chem_2_3_4_7_8_PeCDF"]=self.Chemical_Z_Liquid *self.VolumeFraction_Liquid +self.Chemical_Z_Solid *self.VolumeFraction_Solid + self.Chemical_Z_Algae*self.VolumeFraction_Algae
		self.Z_Total["Chem_2_3_7_8_TCDD"]=self.Chemical_Z_Liquid *self.VolumeFraction_Liquid +self.Chemical_Z_Solid *self.VolumeFraction_Solid + self.Chemical_Z_Algae*self.VolumeFraction_Algae
		self.Z_Total["Chem_2_3_7_8_TCDF"]=self.Chemical_Z_Liquid *self.VolumeFraction_Liquid +self.Chemical_Z_Solid *self.VolumeFraction_Solid + self.Chemical_Z_Algae*self.VolumeFraction_Algae
		self.Z_Total["Chem_2_Methylnaphthalene"]=self.Chemical_Z_Liquid *self.VolumeFraction_Liquid +self.Chemical_Z_Solid *self.VolumeFraction_Solid + self.Chemical_Z_Algae*self.VolumeFraction_Algae
		self.Z_Total["Chem_7_12_Dimethylbenz_a_anthracene"]=self.Chemical_Z_Liquid *self.VolumeFraction_Liquid +self.Chemical_Z_Solid *self.VolumeFraction_Solid + self.Chemical_Z_Algae*self.VolumeFraction_Algae
		self.Z_Total["Chem_Acenaphthene"]=self.Chemical_Z_Liquid *self.VolumeFraction_Liquid +self.Chemical_Z_Solid *self.VolumeFraction_Solid + self.Chemical_Z_Algae*self.VolumeFraction_Algae
		self.Z_Total["Chem_Acenaphthylene"]=self.Chemical_Z_Liquid *self.VolumeFraction_Liquid +self.Chemical_Z_Solid *self.VolumeFraction_Solid + self.Chemical_Z_Algae*self.VolumeFraction_Algae
		self.Z_Total["Chem_Arsenic"]=self.Chemical_Z_Liquid *self.VolumeFraction_Liquid +self.Chemical_Z_Solid *self.VolumeFraction_Solid + self.Chemical_Z_Algae*self.VolumeFraction_Algae
		self.Z_Total["Chem_Benz_a_anthracene"]=self.Chemical_Z_Liquid *self.VolumeFraction_Liquid +self.Chemical_Z_Solid *self.VolumeFraction_Solid + self.Chemical_Z_Algae*self.VolumeFraction_Algae
		self.Z_Total["Chem_Benzo_A_Pyrene"]=self.Chemical_Z_Liquid *self.VolumeFraction_Liquid +self.Chemical_Z_Solid *self.VolumeFraction_Solid + self.Chemical_Z_Algae*self.VolumeFraction_Algae
		self.Z_Total["Chem_Benzo_b_fluoranthene"]=self.Chemical_Z_Liquid *self.VolumeFraction_Liquid +self.Chemical_Z_Solid *self.VolumeFraction_Solid + self.Chemical_Z_Algae*self.VolumeFraction_Algae
		self.Z_Total["Chem_Benzo_g_h_i_perylene"]=self.Chemical_Z_Liquid *self.VolumeFraction_Liquid +self.Chemical_Z_Solid *self.VolumeFraction_Solid + self.Chemical_Z_Algae*self.VolumeFraction_Algae
		self.Z_Total["Chem_Benzo_k_fluoranthene"]=self.Chemical_Z_Liquid *self.VolumeFraction_Liquid +self.Chemical_Z_Solid *self.VolumeFraction_Solid + self.Chemical_Z_Algae*self.VolumeFraction_Algae
		self.Z_Total["Chem_Cadmium"]=self.Chemical_Z_Liquid *self.VolumeFraction_Liquid +self.Chemical_Z_Solid *self.VolumeFraction_Solid + self.Chemical_Z_Algae*self.VolumeFraction_Algae
		self.Z_Total["Chem_Chrysene"]=self.Chemical_Z_Liquid *self.VolumeFraction_Liquid +self.Chemical_Z_Solid *self.VolumeFraction_Solid + self.Chemical_Z_Algae*self.VolumeFraction_Algae
		self.Z_Total["Chem_Dibenz_a_h_anthracene"]=self.Chemical_Z_Liquid *self.VolumeFraction_Liquid +self.Chemical_Z_Solid *self.VolumeFraction_Solid + self.Chemical_Z_Algae*self.VolumeFraction_Algae
		self.Z_Total["Chem_Divalent_Mercury"]=self.Chemical_Z_Liquid *self.VolumeFraction_Liquid +self.Chemical_Z_Solid *self.VolumeFraction_Solid + self.Chemical_Z_Algae*self.VolumeFraction_Algae
		self.Z_Total["Chem_Elemental_Mercury"]=self.Chemical_Z_Liquid *self.VolumeFraction_Liquid +self.Chemical_Z_Solid *self.VolumeFraction_Solid + self.Chemical_Z_Algae*self.VolumeFraction_Algae
		self.Z_Total["Chem_Fluoranthene"]=self.Chemical_Z_Liquid *self.VolumeFraction_Liquid +self.Chemical_Z_Solid *self.VolumeFraction_Solid + self.Chemical_Z_Algae*self.VolumeFraction_Algae
		self.Z_Total["Chem_Fluorene"]=self.Chemical_Z_Liquid *self.VolumeFraction_Liquid +self.Chemical_Z_Solid *self.VolumeFraction_Solid + self.Chemical_Z_Algae*self.VolumeFraction_Algae
		self.Z_Total["Chem_Indeno_1_2_3_cd_pyrene"]=self.Chemical_Z_Liquid *self.VolumeFraction_Liquid +self.Chemical_Z_Solid *self.VolumeFraction_Solid + self.Chemical_Z_Algae*self.VolumeFraction_Algae
		self.Z_Total["Chem_Lead"]=self.Chemical_Z_Liquid *self.VolumeFraction_Liquid +self.Chemical_Z_Solid *self.VolumeFraction_Solid + self.Chemical_Z_Algae*self.VolumeFraction_Algae
		self.Z_Total["Chem_MethylMercury"]=self.Chemical_Z_Liquid *self.VolumeFraction_Liquid +self.Chemical_Z_Solid *self.VolumeFraction_Solid + self.Chemical_Z_Algae*self.VolumeFraction_Algae
		try:
			self.Chemical_Z_Total=self.Z_Total[self.currentChemical.Name]
		except:
			self.Chemical_Z_Total=nan

		self.initialConcentration_g_per_L={}
		self.initialConcentration_g_per_L["Chem_1_2_3_4_6_7_8_9_OCDD"]=self.containingScenario.FractionInitialConcentrations * self.Chemical_initialConcentration_g_per_L_UserSupplied
		self.initialConcentration_g_per_L["Chem_1_2_3_4_6_7_8_9_OCDF"]=self.containingScenario.FractionInitialConcentrations * self.Chemical_initialConcentration_g_per_L_UserSupplied
		self.initialConcentration_g_per_L["Chem_1_2_3_4_6_7_8_HpCDD"]=self.containingScenario.FractionInitialConcentrations * self.Chemical_initialConcentration_g_per_L_UserSupplied
		self.initialConcentration_g_per_L["Chem_1_2_3_4_6_7_8_HpCDF"]=self.containingScenario.FractionInitialConcentrations * self.Chemical_initialConcentration_g_per_L_UserSupplied
		self.initialConcentration_g_per_L["Chem_1_2_3_4_7_8_9_HpCDF"]=self.containingScenario.FractionInitialConcentrations * self.Chemical_initialConcentration_g_per_L_UserSupplied
		self.initialConcentration_g_per_L["Chem_1_2_3_4_7_8_HxCDD"]=self.containingScenario.FractionInitialConcentrations * self.Chemical_initialConcentration_g_per_L_UserSupplied
		self.initialConcentration_g_per_L["Chem_1_2_3_4_7_8_HxCDF"]=self.containingScenario.FractionInitialConcentrations * self.Chemical_initialConcentration_g_per_L_UserSupplied
		self.initialConcentration_g_per_L["Chem_1_2_3_6_7_8_HxCDD"]=self.containingScenario.FractionInitialConcentrations * self.Chemical_initialConcentration_g_per_L_UserSupplied
		self.initialConcentration_g_per_L["Chem_1_2_3_6_7_8_HxCDF"]=self.containingScenario.FractionInitialConcentrations * self.Chemical_initialConcentration_g_per_L_UserSupplied
		self.initialConcentration_g_per_L["Chem_1_2_3_7_8_9_HxCDD"]=self.containingScenario.FractionInitialConcentrations * self.Chemical_initialConcentration_g_per_L_UserSupplied
		self.initialConcentration_g_per_L["Chem_1_2_3_7_8_9_HxCDF"]=self.containingScenario.FractionInitialConcentrations * self.Chemical_initialConcentration_g_per_L_UserSupplied
		self.initialConcentration_g_per_L["Chem_1_2_3_7_8_PeCDD"]=self.containingScenario.FractionInitialConcentrations * self.Chemical_initialConcentration_g_per_L_UserSupplied
		self.initialConcentration_g_per_L["Chem_1_2_3_7_8_PeCDF"]=self.containingScenario.FractionInitialConcentrations * self.Chemical_initialConcentration_g_per_L_UserSupplied
		self.initialConcentration_g_per_L["Chem_2_3_4_6_7_8_HxCDF"]=self.containingScenario.FractionInitialConcentrations * self.Chemical_initialConcentration_g_per_L_UserSupplied
		self.initialConcentration_g_per_L["Chem_2_3_4_7_8_PeCDF"]=self.containingScenario.FractionInitialConcentrations * self.Chemical_initialConcentration_g_per_L_UserSupplied
		self.initialConcentration_g_per_L["Chem_2_3_7_8_TCDD"]=self.containingScenario.FractionInitialConcentrations * self.Chemical_initialConcentration_g_per_L_UserSupplied
		self.initialConcentration_g_per_L["Chem_2_3_7_8_TCDF"]=self.containingScenario.FractionInitialConcentrations * self.Chemical_initialConcentration_g_per_L_UserSupplied
		self.initialConcentration_g_per_L["Chem_2_Methylnaphthalene"]=self.containingScenario.FractionInitialConcentrations * self.Chemical_initialConcentration_g_per_L_UserSupplied
		self.initialConcentration_g_per_L["Chem_7_12_Dimethylbenz_a_anthracene"]=self.containingScenario.FractionInitialConcentrations * self.Chemical_initialConcentration_g_per_L_UserSupplied
		self.initialConcentration_g_per_L["Chem_Acenaphthene"]=self.containingScenario.FractionInitialConcentrations * self.Chemical_initialConcentration_g_per_L_UserSupplied
		self.initialConcentration_g_per_L["Chem_Acenaphthylene"]=self.containingScenario.FractionInitialConcentrations * self.Chemical_initialConcentration_g_per_L_UserSupplied
		self.initialConcentration_g_per_L["Chem_Benz_a_anthracene"]=self.containingScenario.FractionInitialConcentrations * self.Chemical_initialConcentration_g_per_L_UserSupplied
		self.initialConcentration_g_per_L["Chem_Benzo_A_Pyrene"]=self.containingScenario.FractionInitialConcentrations * self.Chemical_initialConcentration_g_per_L_UserSupplied
		self.initialConcentration_g_per_L["Chem_Benzo_b_fluoranthene"]=self.containingScenario.FractionInitialConcentrations * self.Chemical_initialConcentration_g_per_L_UserSupplied
		self.initialConcentration_g_per_L["Chem_Benzo_g_h_i_perylene"]=self.containingScenario.FractionInitialConcentrations * self.Chemical_initialConcentration_g_per_L_UserSupplied
		self.initialConcentration_g_per_L["Chem_Benzo_k_fluoranthene"]=self.containingScenario.FractionInitialConcentrations * self.Chemical_initialConcentration_g_per_L_UserSupplied
		self.initialConcentration_g_per_L["Chem_Chrysene"]=self.containingScenario.FractionInitialConcentrations * self.Chemical_initialConcentration_g_per_L_UserSupplied
		self.initialConcentration_g_per_L["Chem_Dibenz_a_h_anthracene"]=self.containingScenario.FractionInitialConcentrations * self.Chemical_initialConcentration_g_per_L_UserSupplied
		self.initialConcentration_g_per_L["Chem_Divalent_Mercury"]=self.containingScenario.FractionInitialConcentrations * self.Chemical_initialConcentration_g_per_L_UserSupplied
		self.initialConcentration_g_per_L["Chem_Elemental_Mercury"]=self.containingScenario.FractionInitialConcentrations * self.Chemical_initialConcentration_g_per_L_UserSupplied
		self.initialConcentration_g_per_L["Chem_Fluoranthene"]=self.containingScenario.FractionInitialConcentrations * self.Chemical_initialConcentration_g_per_L_UserSupplied
		self.initialConcentration_g_per_L["Chem_Fluorene"]=self.containingScenario.FractionInitialConcentrations * self.Chemical_initialConcentration_g_per_L_UserSupplied
		self.initialConcentration_g_per_L["Chem_Indeno_1_2_3_cd_pyrene"]=self.containingScenario.FractionInitialConcentrations * self.Chemical_initialConcentration_g_per_L_UserSupplied
		self.initialConcentration_g_per_L["Chem_MethylMercury"]=self.containingScenario.FractionInitialConcentrations * self.Chemical_initialConcentration_g_per_L_UserSupplied
		try:
			self.Chemical_initialConcentration_g_per_L=self.initialConcentration_g_per_L[self.currentChemical.Name]
		except:
			self.Chemical_initialConcentration_g_per_L=nan
