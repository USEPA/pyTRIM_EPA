# -*- coding: utf-8 -*-
"""
Solves the TRIM.FaTE ODE system  assuming constant transition matrix, source matrix, and zero initial conditions
@author: 13963

"""

# Import the required modules
import numpy as np
from scipy.integrate import odeint
import pandas as pd

def ode_sim(tm,df_tm,sm,df_sm): # need to add start time and end time of simulation as arguments. currently assuming 50 years

    tm=np.nan_to_num(tm, copy=True, nan=0.0, posinf=None, neginf=None) # replace nans with zero
    steps_per_day=24    # steps per day for integration and output -- will need to be input / argument eventually
    
    def M(t): # transition matrix   
        m=tm #  
        return(m)
    
    def S(t): # source term
        s=sm 
#        s=sm/steps_per_day # adjusts emission rate to g/integration time step --NOT REQUIRED ODEINT UNDERSTANDS FROM THE LINSPACE STATEMENT THAT THE  
        return(s)    
        
    def dN_dt(N, t): # derivative function
        N_prime=np.matmul(M(t),N) + S(t)
        return (N_prime)    
    
    ndim=sm.shape[0] # number of compartments

    ts = np.linspace(0,365*50,365*50*steps_per_day) # time line in hours for 50 years, tstart and tend should be inputs

    N0 = np.zeros(ndim)  # zero mass initial condition
    Nt = odeint(dN_dt, N0, ts,hmax=24) # Mass at time t


    df_Nt=pd.DataFrame(Nt)
    cols=list(df_sm.index)
    df_Nt.columns=cols
    df_Nt['Time_in_hours']=ts
    cols_ordered=['Time_in_hours']+cols
#    
    df_Nt=df_Nt[cols_ordered]
    
    return(Nt,df_Nt)
    
    
