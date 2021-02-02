import pandas as pd
import os 
from functools import reduce

THIS_FOLDER = os.path.dirname(os.path.abspath(__file__))

# File 1/3: Population by community
df_pop = pd.read_csv(THIS_FOLDER + "/csv/" + "population_by_community.csv", sep =";")
df_pop[['index','Region']] = df_pop['Comunidades y Ciudades Autónomas'].str.split(' ', 1, expand=True) # Get rid of index in region name
df_pop.drop(['Comunidades y Ciudades Autónomas', 'index', 'Tamaño de los municipios', 'Periodo'], axis=1, inplace=True) # Remove redundant columns
df_pop = df_pop.iloc[1:] # Remove total row
df_pop.rename(columns = {'Total': 'Population'}, inplace = True)
#print(df_pop.head(10))

# File 2/3: Age 65 by community
df_age = pd.read_csv(THIS_FOLDER + "/csv/" + "age_65_by_community.csv", sep =";")
df_age[['index','Region']] = df_age['Comunidades y Ciudades Autónomas'].str.split(' ', 1, expand=True) # Get rid of index in region name
df_age.drop(['Comunidades y Ciudades Autónomas', 'index', 'Edad', 'Periodo'], axis=1, inplace=True) # Remove redundant columns
df_age = df_age.iloc[1:] # Remove total row
df_age.rename(columns = {'Total': 'Age65'}, inplace = True)
#print(df_age.head(10))

# File 3/3: Income by community // Cleaned manually
df_inc = pd.read_csv(THIS_FOLDER + "/csv/" + "income.csv", sep =";")
df_inc.rename(columns = {'Total': 'Income'}, inplace = True)
#print(df_inc.head(10))

data_frames = [df_pop, df_age, df_inc]
df_merged = reduce(lambda  left,right: pd.merge(left,right,on=['Region']), data_frames)

# tail -40 covid_data.csv | cut -f2 -d ',' | sort -u # Bash command to get region 'id's in covid_data.csv 
region_ids = ["andalucia", "aragon","asturias","baleares","canarias","cantabria","castilla-la_mancha","castilla_y_leon","cataluna","c_valenciana","extremadura","galicia","madrid","murcia","navarra","pais_vasco","la_rioja","ceuta","melilla"]
df_merged['id'] = region_ids 
#print(df_merged)

df_merged.to_csv('metadata.csv', mode='w', header=True, index=False, sep = ";")


