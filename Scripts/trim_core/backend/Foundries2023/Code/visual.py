'''
########## 

Example output plots. These are not very clean or well formatted.

#########
'''''

import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import re # import the regular expression module

########### function to plot a list of total mass columns from pyTRIM average mass ts output. 

def plot_time_series_mass(data, comp_dict, log_scale=False): # assumes column 0 contains time in hours
  data_preproc=data[['year']+list(comp_dict.values())] # subset the data to just x and y vars to be plotted  
  pl=sns.lineplot(x='year', y='value', hue='variable',data=pd.melt(data_preproc, ['year']))
  if log_scale:
      pl.set(yscale='log')
  plt.legend(title='Compartment', loc='upper left', labels=list(comp_dict.keys()))
  #show the plot
  plt.xlabel("Year")
  plt.ylabel("Mass in g")
  plt.show()
  plt.savefig(r'C:\Users\13963\OneDrive - ICF\Documents\RTR\PyTRIM\Foundries2023\Compartment_Mass_Time_Series.png')
  #return the processed data dataframe
  return ()

ifpn=r'C:\Users\13963\OneDrive - ICF\Documents\RTR\PyTRIM\Foundries2023\output\time_series_mass.csv'
## dictionary of comps to be plotted -- keys are pretty name, values are real name. Chemical name not shown here but should be.
comp_dict={'Surface_Water_Lake_Cadillac':'chem_elemental_mercury_surface_water_in_sw_lakecadillac','Surface_Water_Lake_Mitchell':'chem_elemental_mercury_surface_water_in_sw_lakemitchell'}
df=pd.read_csv(ifpn)
pl=plot_time_series_mass(df, comp_dict, log_scale=True)

##########################################################

########### function to plot mass distribution for aggregate compartment types in final year from pyTRIM average ts output. 


def plot_mass_distribution(dfn_avg, chem_name,comp_patterns,graph_type,log_scale=False):
    
    #create an empty dataframe to store the grouped values by pattern
    data_grouped = pd.DataFrame()
    #loop through the dictionary items and find the matching columns
    for label, pattern in comp_patterns.items():
      #use regular expression to match the column names
      matched_columns = [col for col in dfn_avg.columns if re.search(pattern, col)]
      matched_columns=[col for col in matched_columns if chem_name in col]
      #sum the values of the matched columns and assign to a new column
      data_grouped[label] = dfn_avg[matched_columns].sum(axis=1)
    #get the final year
    final_year = data_grouped.index[-1]
    #get the values for the final year
    final_values = data_grouped.loc[final_year]
    
    final_year_val= dfn_avg['year'].iloc[-1]
    #plot the pie chart for the final year
     
    if graph_type=='pie': 
       pl=final_values.plot(kind='pie', y=comp_patterns.keys(), autopct='%1.0f%%', title=f'Mass Distribution for {chem_name} in {final_year_val}')
           #show the pie chart
       plt.show()
           #return the processed data dataframe and the grouped data dataframe

    if graph_type=='bar': 
            x = comp_patterns.keys() # the categories
            y = final_values.values # the numerical values
            # assign the plt.bar() function to a variable ax
            plt.bar(x, y, align='center', alpha=0.5,log=log_scale) 
            plt.xlabel('Compartment Type')
            plt.ylabel('Mass in g')
            plt.title(f'Mass Distribution for {chem_name} in {final_year_val}')
            # use the ax object to set the x-axis labels

            plt.show()    
   
    plt.savefig(r'C:\Users\13963\OneDrive - ICF\Documents\RTR\PyTRIM\Foundries2023\MassDistribution.png')
  
    return ()


ifpn=r'C:\Users\13963\OneDrive - ICF\Documents\RTR\PyTRIM\Foundries2023\output\time_series_mass.csv'
## dictionary of comps to be plotted -- keys are pretty name, values are real name. Chemical name not shown here but should be.
comp_patterns={'Surface Water':'surface_water','Surface Soil':'soil_surface','Root Zone Soil':'soil_root_zone','Vadose Zone Soil':'soil_vadose_zone','Sediment':'sediment_in_','Benthic Biota':'benthic','Water Column Biota':'water_column','Non-air Sinks':'sink','Air Sinks':'air_in'}
log_scale=True
graph_type='bar'
chem_name='chem_divalent_mercury'

df=pd.read_csv(ifpn)

plot_mass_distribution(df, chem_name,comp_patterns,graph_type,log_scale)

log_scale=False
graph_type='pie'
plot_mass_distribution(df, chem_name,comp_patterns,graph_type,log_scale)

##########################################################
