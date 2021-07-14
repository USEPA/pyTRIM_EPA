# -*- coding: utf-8 -*-

#create the sources library import file.

from ..Classes.OutputFormatter import OutputFormatter
import datetime

def GenerateSources(FileName, ScenarioName, ScenarioDescription, Layout_EmissionSources):

    SourcesFormatter = OutputFormatter(FileName)

    EmissionChemicals = list(Layout_EmissionSources)[2:-2]
    
    SourceNames = list(Layout_EmissionSources.loc[:,"Location"])
    ElevationRow = Layout_EmissionSources.loc[:,"Stack elevation (m)"]
    XRow = Layout_EmissionSources.loc[:,"X coordinate"]
    YRow = Layout_EmissionSources.loc[:,"Y coordinate"]

    SourcesFormatter.PrintLine("TRIM.FaTE library file with site-specific emission sources", True)
    SourcesFormatter.PrintCell("")
    SourcesFormatter.PrintLine(ScenarioName, True)
    SourcesFormatter.PrintLine(ScenarioDescription, True)
    SourcesFormatter.PrintCell("")
    SourcesFormatter.LinePrint("Generated:", str(datetime.datetime.now()), True)
    SourcesFormatter.PrintCell("")
    SourcesFormatter.PrintLine("Version:1")
    SourcesFormatter.PrintCell("")
    SourcesFormatter.PrintCell("")
    SourcesFormatter.PrintLine("This file must be imported into the TRIM.FaTE library directly", True)
    SourcesFormatter.PrintLine("(not the scenario). Sources must then be manually added to the", True)
    SourcesFormatter.PrintLine("scenario using the graphical interface.", True)
    SourcesFormatter.PrintCell("")
    SourcesFormatter.PrintCell("")

    for i, Source in enumerate(Layout_EmissionSources.index.to_list()):
        SourcesFormatter.LinePrint("PointSource:", str(Source))
        SourcesFormatter.PropertyValue("Enabled", "Constant", "True", "")
        SourcesFormatter.PropertyValue("X", "Constant", str(XRow[i]), "")
        SourcesFormatter.PropertyValue("Y", "Constant", str(YRow[i]), "")
        SourcesFormatter.PropertyValue("Elevation", "Constant", str(ElevationRow[i]), "")        
        SourcesFormatter.PrintLine("Property: EmissionRate")
        
        for chem in EmissionChemicals:
            SourcesFormatter.PrintLine(str("Value:  {" + str(chem) + "} " + 
                                                     str(Layout_EmissionSources[str(chem)][Layout_EmissionSources.index==Source][0])))
        SourcesFormatter.PrintCell("")
        SourcesFormatter.PrintCell("")
        
if __name__ == "__main__":
    GenerateSources(str(Out+"Sources.txt"), "Foundries", "Testing", Layout_EmissionSources)
#str(Layout_EmissionSources["X coordinate"][Layout_EmissionSources.index==Source][0])