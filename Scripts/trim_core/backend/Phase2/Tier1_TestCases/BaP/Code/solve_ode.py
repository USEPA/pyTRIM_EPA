# -*- coding: utf-8 -*-
"""
solves the trim.fate ode system  assuming constant transition matrix, source matrix, and zero initial conditions
@author: 13963

"""

# import the required modules
import numpy as np
from scipy.integrate import odeint
import pandas as pd

# def ode_sim(tm,df_tm,sm,df_sm): # need to add start time and end time of simulation as arguments. currently assuming 50 years

#     tm=np.nan_to_num(tm, copy=True, nan=0.0, posinf=None, neginf=None) # replace nans with zero
#     steps_per_day=24    # steps per day for integration and output -- will need to be input / argument eventually
    
#     def m(t): # transition matrix   
#         m=tm #  
#         return(m)
    
#     def s(t): # source term
#         s=sm 
# #        s=sm/steps_per_day # adjusts emission rate to g/integration time step --not required odeint understands from the linspace statement that the  
#         return(s)    
        
#     def dn_dt(n, t): # derivative function
#         n_prime=np.matmul(m(t),n) + s(t)
#         return (n_prime)    
    
#     ndim=sm.shape[0] # number of compartments

#     ts = np.linspace(0,365*50,365*50*steps_per_day) # time line in hours for 50 years, tstart and tend should be inputs

#     n0 = np.zeros(ndim)  # zero mass initial condition
#     nt = odeint(dn_dt, n0, ts,hmax=24) # mass at time t


#     df_nt=pd.DataFrame(nt)
#     cols=list(df_sm.index)
#     df_nt.columns=cols
#     df_nt['time_in_hours']=ts
#     cols_ordered=['time_in_hours']+cols
# #    
#     df_nt=df_nt[cols_ordered]
    
#     return(nt,df_nt)
    
    

def ode_sim(tm_c,tm_v,df_tm,sm,df_sm): # need to add start time and end time of simulation as arguments. currently assuming 50 years

    steps_per_day=24    # steps per day for integration and output -- will need to be input / argument eventually
    
    # tm=np.nan_to_num(tm, copy=True, nan=0.0, posinf=None, neginf=None) # replace nans with zero
    # tm_constant=np.where((type(tm)==np.float)or(type(tm)==np.float64)or(type(tm)==np.float32)or(type(tm)==int),tm,0) # replace array elements of mixed tm array with zero
    # tm_constant=np.where(type(tm)!=np.ndarray,tm,0) # replace non-array elements of mixed tm array with zero
    # tm_variable=np.where(type(tm)==np.ndarray,tm,0) # replace non-array elements of mixed tm array with zero
    

    def m(t): # transition matrix   
        # tm_t=np.zeros((tm_c.shape[0],tm_c.shape[1]))
        # tm_t=tm_c +tm_t
        tm_t=tm_c.copy()
        for k,v in tm_v.items():
            tm_t[k[0]][k[1]]=tm_t[k[0]][k[1]]+float(v[int(t)])


                    
        # m_t=tm_constant +tm_variable_t            
        # m=tm_constant + np.where(type(tm)==np.ndarray,tm_variable[[int(t)]],0) #  matrix at time t is the sum of the constant matrix plus the variable matrix looked up at time t
        tm_t=np.nan_to_num(tm_t, copy=True, nan=0.0, posinf=None, neginf=None) # replace nans with zero
        tm_t=np.array(tm_t, dtype=np.float)
        return(tm_t)
    
    def s(t): # source term
        s=sm 
#        s=sm/steps_per_day # adjusts emission rate to g/integration time step --not required odeint understands from the linspace statement that the  
        return(s)    
        
    def dn_dt(n, t): # derivative function
        n_prime=np.matmul(m(t),n) + s(t)
        return (n_prime)    
    
    ndim=sm.shape[0] # number of compartments

    ts = np.linspace(0,365*50,365*50*steps_per_day) # time line in hours for 50 years, tstart and tend should be inputs
    # ts = np.linspace(0,365*1,365*1*steps_per_day) # time line in hours for 1 years, tstart and tend should be inputs


    n0 = np.zeros(ndim)  # zero mass initial condition
#    nt = odeint(dn_dt, n0, ts,hmax=24) # mass at time t
#    nt = odeint(dn_dt, n0, ts,hmax=24,rtol=1e-5,atol=1e-5) # mass at time t
    nt = odeint(dn_dt, n0, ts,hmax=24,rtol=1e-3,atol=1e-3) # mass at time t



    df_nt=pd.DataFrame(nt)
    cols=list(df_sm.index)
    df_nt.columns=cols
    df_nt['time_in_hours']=ts
    cols_ordered=['time_in_hours']+cols
#    
    df_nt=df_nt[cols_ordered]
    
    return(nt,df_nt)
  
# for x in range(0,tm_t.shape[0]):
#     for y in range(0,tm_t.shape[0]):
#         # if type(tm_t[x][y])==object:
#         if type(tm_t[x][y])!=float and type(tm_t[x][y])!=np.float64:
#             print (x,y)
