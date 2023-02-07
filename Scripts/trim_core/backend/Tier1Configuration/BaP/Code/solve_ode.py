# -*- coding: utf-8 -*-
"""
solves the trim.fate ode system  assuming constant transition matrix, source matrix, and zero initial conditions
@author: 13963

"""

# import the required modules
import numpy as np
from scipy.integrate import odeint
import pandas as pd

def ode_sim(tm,df_tm,sm,df_sm): # need to add start time and end time of simulation as arguments. currently assuming 50 years

    tm=np.nan_to_num(tm, copy=True, nan=0.0, posinf=None, neginf=None) # replace nans with zero
    steps_per_day=24    # steps per day for integration and output -- will need to be input / argument eventually
    
    def m(t): # transition matrix   
        m=tm #  
        return(m)
    
    def s(t): # source term
        s=sm 
#        s=sm/steps_per_day # adjusts emission rate to g/integration time step --not required odeint understands from the linspace statement that the  
        return(s)    
        
    def dn_dt(n, t): # derivative function
        n_prime=np.matmul(m(t),n) + s(t)
        return (n_prime)    
    
    ndim=sm.shape[0] # number of compartments

    ts = np.linspace(0,365*50,365*50*steps_per_day) # time line in hours for 50 years, tstart and tend should be inputs

    n0 = np.zeros(ndim)  # zero mass initial condition
    nt = odeint(dn_dt, n0, ts,hmax=24) # mass at time t


    df_nt=pd.DataFrame(nt)
    cols=list(df_sm.index)
    df_nt.columns=cols
    df_nt['time_in_hours']=ts
    cols_ordered=['time_in_hours']+cols
#    
    df_nt=df_nt[cols_ordered]
    
    return(nt,df_nt)
    
    
