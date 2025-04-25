# -*- coding: utf-8 -*-
"""

To generate initial mass values for each compartment using initial concentrations and previously compiled dataframe of comparment volume/mass/units/conversion factors

Created on Thu Aug 25 08:56:43 2022

@author: 13963

"""

import pandas as pd

def compute_initial_mass(df_c0,df_vmu): # arguments are the chemical mass array (nt), mass dataframe

    df=df_c0.merge(df_vmu,left_index=True,right_index=True)
    df['n0_g']=0
    df.loc[df['initial_concentration_units']=='g_per_m3','n0_g'] = df['initial_concentration']*df['volume_m3']
    df.loc[df['initial_concentration_units']=='g_per_l','n0_g'] = df['initial_concentration']*df['volume_m3']*1000
    df.loc[df['initial_concentration_units']=='g_per_kg','n0_g'] = df['initial_concentration']*df['mass_kg']
    df_n0=df[['initial_concentration_units','n0_g']]
                 
    return(df_n0)
    
    