# -*- coding: utf-8 -*-
"""

Function to convert legacy input files to lower case input files. Works for all txt and csv files.
Created on Wed Sep  8 10:10:26 2021

@author: 13963
"""
import os

code_words = ['true', 'false', 'valueerror','dataframe','polygon', 'linestring','none'] # words in Python code with special significance and uppercase letters
dic={'true':'True','false':'False','valueerror':'ValueError','dataframe':'DataFrame','polygon':'Polygon', 'linestring':'LineString','none':'None'}


def convert_lc(inputs):

    path_old_files=inputs['legacy_path_inputs']
    path_new_files=inputs['path_inputs']
        
    inputfiles = [f for f in os.listdir(path_old_files) if os.path.isfile(os.path.join(path_old_files, f))] # list of legacy input files

    for f in inputfiles: # loop over input files and convert to lower case. write to new location.
        fpn=os.path.abspath(os.path.join(path_old_files,f))
    
        oldFileContent = open(fpn, 'r').read()
        newFileContent = oldFileContent.lower()

        for word in code_words: # replace special context words as required
            newFileContent =newFileContent.replace(word,dic[word])     

        ofpn=os.path.abspath(os.path.join(path_new_files,f.lower())) # new file path and name
        
        with open(ofpn, 'w') as f:
            f.write(newFileContent) 
        
    return()
