# -*- coding: utf-8 -*-
"""
created on mon jul 19 15:47:12 2021
@author: 13963

utility functions for all modules

"""
import re

def clean_chem_names(name): # function to replace certain special characters with underscore; leaves float values alone
    try:
        name=float(name) 
    except:
        pass
    if type(name)==str:
        cname = 'chem_'+re.sub('[^0-9a-za-z]+', '_', name)
        return(cname)
    return(name)  
    
def ternary2python(xpr):
    question_mark = xpr.find("?")
    colon = xpr.find(":", question_mark)

    # if no (or no more) if conditions return the expression
    if (question_mark == -1) or (colon == -1):
        return xpr

    # extract outer if condition and expressions (True & False)
    condition = xpr[0:question_mark].replace("&&", "and").replace("||", "or").strip()
    expressions = xpr[(question_mark + 1):xpr.__len__()].strip()

    True_expression = ""
    False_expression = ""

    # while looking in pairs, find the location where the colon occurs before the question mark
    question_mark = expressions.find("?")
    colon = expressions.find(":")
    while ((question_mark != -1) and (colon != -1)) and (question_mark < colon):
        question_mark = expressions.find("?", question_mark + 1)
        colon = expressions.find(":", colon + 1)

    # extract True and False expressions
    True_expression = f'{expressions[0:colon].strip()}'
    False_expression = f'{expressions[(colon + 1):expressions.__len__()].strip()}'

    return f'{ternary2python(True_expression)} if {condition} else {ternary2python(False_expression)}'


def is_number(s): # checks if string is number
    try:
        float(s)
        return True
    except ValueError:
        try:
            int(s)
            return True
        except ValueError:
            return False