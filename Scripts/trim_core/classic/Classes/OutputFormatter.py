# -*- coding: utf-8 -*-

#Builder Class Module - Output Formatter
#This class contains code relevant to output file formatting


#with open("Output.txt", "w") as text_file:
#    text_file.write("Purchase Amount: %s" % 1000)
    
from .Parcel import Parcel
from enum import Enum
import ipdb #for debugging

class CellType(Enum): #most likely will not need this
    cText = 0
    cFormula = 1
    cReference = 2
    
class OutputFormatter:
    
    def __init__(self, FileName):
        self.FileName = FileName        
        with open(FileName, "w") as text_file:
            text_file.write("")
            
    def PrintCell(self, Text:str, IsComment:bool=False) -> str:
        #writes out basic text
        Text += "\n"
        if IsComment:
            Text = "// " + Text
        with open(self.FileName, "a") as text_file:
            text_file.write(Text)
        
    def PrintLine(self, Text:str, IsComment:bool=False) -> str:
        self.PrintCell(Text,IsComment)
        
    def PropertyValue(self, Prop:str, Form, Val, Celltype):
        #shortcut for printing pairs like
        # property: Prop
        # value: Val
        self.PrintLine(str("Property: " + Prop))
        self.PrintCell(str("Form: " + Form))
        self.PrintCell(str("Value: " + Val))
        #some GUI interactions will need to happen here
    
#    def LineFeed(self):
#        self.PrintLine("\n")
    
    def LinePrint(self, left, right, IsComment:bool=False):
        self.PrintLine(str(str(left) + " " + str(right)), IsComment)
        
    def Divider(self, Text:str="", WithSpacing:bool=False):
        if WithSpacing:
            self.PrintLine("----------------------------------------------------------------------------", True)
        if len(Text)>0:
            self.PrintLine(Text, True)
            self.PrintLine("----------------------------------------------------------------------------", True)
    
    @staticmethod
    def _Quoted(Text:str) -> str:
        Quoted = str("\"" + Text + "\"")
        return(Quoted)
        
