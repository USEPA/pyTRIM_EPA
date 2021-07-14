# -*- coding: utf-8 -*-

#Builder Module - Layout
 
#This module contains functions for updating and getting information about the
#scenario's layout.
import numpy as np
import pandas as pd
import ipdb
from math import isclose
#from Layout import MMultPower
#from Classes.Parcel import Parcel
#from Classes.ParcelCollection import ParcelCollection

def RunoffMatrixIsValid(Matrix:list) -> list:
    """
    checks whether the user-supplied runoff fractions are valid
    
    returns a np.matrix object if the matrix is valid
    """
    if len(Matrix) != len(Matrix[0]):
        raise ValueError(f"""Input matrix is not a square matrix;
            has length {len(Matrix)}x{len(Matrix[0])}""")
    
    for r, row in enumerate(Matrix):
        Sum = round(sum(row),4)
        if Sum < 0 or Sum > 1:
            raise ValueError(f"Sum of row {r}: {row} = {Sum}, and is < 0 or > 1")
     
    return(np.matrix(Matrix, dtype='double'))


def RunoffTerminationMatrix(RunoffInitialMatrix:list):
    """
    Multiplies the runnoff fraction matrix (for a single time step) by itself
    until steady-state is reached.
    If lakes are not self-connected (at 100%), or if there are runoff loops, this will fail.
    
    returns a np.matrix object
    """
    
    Matrix = RunoffMatrixIsValid(RunoffInitialMatrix)
    
    LoopCounter = 0
    
    #ipdb.set_trace()
    while True:
        MatrixProduct = np.matmul(Matrix, Matrix, dtype='double')
        
        if np.array_equal(MatrixProduct, Matrix):
            return(Matrix, LoopCounter)
        
        elif LoopCounter > 300:
            return(Matrix, LoopCounter-1)
        
        else:
            Matrix = MatrixProduct
            LoopCounter += 1

mat = (Watersheds.iloc[:,5:]).fillna(0).values.tolist()
term=(RunoffTerminationMatrix(mat))     
        