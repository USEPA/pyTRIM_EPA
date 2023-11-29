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
  comp_names=[list(chem_name.values())[0]+'_'+x for x in list(comp_dict.values())]    
  data_preproc=data[['year']+comp_names] # subset the data to just x and y vars to be plotted  
  pl=sns.lineplot(x='year', y='value', hue='variable',data=pd.melt(data_preproc, ['year']))
  if log_scale:
      pl.set(yscale='log')
  plt.legend(title='Compartment', loc='upper right', labels=list(comp_dict.keys()))
  #show the plot
  plt.xlabel("Year")
  plt.ylabel("Mass in g")
  plt.title(f'Mass of {list(chem_name.keys())[0]}')   
  plt.savefig(r'C:\Users\13963\OneDrive - ICF\Documents\RTR\PyTRIM\Foundries2023\Mass_Time_Series.png')
  plt.show()
  #return the processed data dataframe
  return ()

ifpn=r'C:\Users\13963\OneDrive - ICF\Documents\RTR\PyTRIM\Foundries2023\output\time_series_mass.csv'
## dictionary of comps to be plotted -- keys are pretty name, values are real name. Chemical name not shown here but should be.
comp_dict={'Surface_Water_Lake_Cadillac':'surface_water_in_sw_lakecadillac','Surface_Soil_E1':'soil_surface_in_surfsoil_e1'}
chem_name={'Hg2+':'chem_divalent_mercury'}
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
      matched_columns=[col for col in matched_columns if list(chem_name.values())[0] in col]
      #sum the values of the matched columns and assign to a new column
      data_grouped[label] = dfn_avg[matched_columns].sum(axis=1)
    #get the final year
    final_year = data_grouped.index[-1]
    #get the values for the final year
    final_values = data_grouped.loc[final_year]
    
    final_year_val= dfn_avg['year'].iloc[-1]
    #plot the pie chart for the final year

    if graph_type=='pie': 

        # Define the data and labels for the pie chart
        data = final_values.values # the numerical values
        labels = comp_patterns.keys() # the categories
        
        # Define a seaborn color palette to use for the pie chart
        colors = sns.color_palette('pastel') # you can choose any palette you like
        
        # Use the plt.pie() function to create the pie chart with the data, labels, colors, and other parameters
        # plt.pie(data, labels=labels, colors=colors, autopct='%1.0f%%',textprops={'fontsize': 8})
        plt.pie(data, colors=colors, autopct='%1.0f%%', textprops={'fontsize': 7})
        plt.legend(title='Compartments', loc='upper right', labels=labels,fontsize=7)
        plt.title(f'Mass Distribution of {list(chem_name.keys())[0]} in {final_year_val}')        
        plt.savefig(r'C:\Users\13963\OneDrive - ICF\Documents\RTR\PyTRIM\Foundries2023\MassDistribution_Bar.png')

    if graph_type=='bar': 
        x = list(comp_patterns.keys()) # the categories
        y = final_values.values # the numerical values
        # Use sns.barplot() instead of plt.bar()
        sns.barplot(x, y, log=log_scale) 
        plt.xlabel('Compartment Type')
        plt.ylabel('Mass in g')
        plt.title(f'Mass Distribution of {list(chem_name.keys())[0]} in {final_year_val}')
        # Rotate and lower the font size of the x-axis labels
        plt.setp(plt.gca().get_xticklabels(), rotation=90, fontsize=10)

        plt.savefig(r'C:\Users\13963\OneDrive - ICF\Documents\RTR\PyTRIM\Foundries2023\MassDistribution_Pie.png')
    plt.show()
  
    return ()


ifpn=r'C:\Users\13963\OneDrive - ICF\Documents\RTR\PyTRIM\Foundries2023\output\time_series_mass.csv'
## dictionary of comps to be plotted -- keys are pretty name, values are real name. Chemical name not shown here but should be.
comp_patterns={'Surface Water':'surface_water','Surface Soil':'soil_surface','Root Zone Soil':'soil_root_zone','Vadose Zone Soil':'soil_vadose_zone','Sediment':'sediment_in_','Benthic Biota':'benthic','Water Column Biota':'water_column','Non-air Sinks':'sink','Air Sinks':'air_in'}
log_scale=True
graph_type='bar'
chem_name={'Hg2+':'chem_divalent_mercury'}

df=pd.read_csv(ifpn)

plot_mass_distribution(df, chem_name,comp_patterns,graph_type,log_scale)

log_scale=False
graph_type='pie'
plot_mass_distribution(df, chem_name,comp_patterns,graph_type,log_scale)

##########################################################
