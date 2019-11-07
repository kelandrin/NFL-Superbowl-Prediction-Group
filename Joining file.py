import pandas as pd
import os
from functools import reduce


#Returns a list of the names of the excel sheets starting with offense then defense
def get_list_of_filenames(path:str) -> list:
    filenames = []
    for filename in os.listdir(path):
        filenames.append(filename)

    return sorted(filenames, reverse = True)

def get_list_of_dataframes(names:list) -> list:
    Dataframes = []
    for name in names:
        df = pd.read_excel(path + name)
        df.rename(columns={df.columns[-1]: 'Year', df.columns[2]: 'Team'}, inplace = True)
        df.drop(df.columns[0], axis=1,inplace = True)
        Dataframes.append(df)
    return Dataframes

#Puts the columns 'Team' and 'Year' in the first 2 columns of the Dataframe
def Team_n_year_to_front(df_merged:pd.DataFrame) -> pd.DataFrame:
    my_column = df_merged.pop('Team')
    my_column1 = df_merged.pop('Year')
    df_merged.insert(0, my_column.name, my_column)
    df_merged.insert(1, my_column1.name, my_column1)

    return df_merged[:-12]

#Merges all of the Dataframes and sorts them by year
def merge_n_sort(Dataframes: list) -> pd.DataFrame:
    df_merged = reduce(lambda left, right: pd.merge(left, right, on=['Team', 'Year'],
                                                    how='outer'), Dataframes).fillna('--')
    df_merged = Team_n_year_to_front(df_merged)

    return df_merged.sort_values(by=['Year'])


#Executable
path ='/Users/matthew/Google Drive/MSBA Grad Program/MSBA FALL quarter/BANA 212 (Data and Programming Analytics)/NFL Final project/NFL Excel Sheets/'
filenames = get_list_of_filenames(path)
Dataframes = get_list_of_dataframes(filenames)
df_merged = merge_n_sort(Dataframes)
df_merged.to_excel("NFL-merged.xlsx")




