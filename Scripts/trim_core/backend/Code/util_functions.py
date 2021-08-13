# -*- coding: utf-8 -*-
"""
Created on Mon Jul 19 15:47:12 2021
@author: 13963

Utility functions for all modules

"""
import re

def clean_chem_names(name): # function to replace certain special characters with underscore; leaves float values alone
    try:
        name=float(name) 
    except:
        pass
    if type(name)==str:
        cname = 'Chem_'+re.sub('[^0-9a-zA-Z]+', '_', name)
        return(cname)
    return(name)  