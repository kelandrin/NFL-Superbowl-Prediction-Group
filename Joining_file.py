import pandas as pd
import os
from functools import reduce

#Returns a list of the names of the excel sheets starting with offense then defense then recrods
def get_list_of_filenames(path:str) -> list:
    records_files = [] # creating this because I need to do an initial merge of the records files to avoid win_x,win_y
    rest_of_filenames = []
    for filename in os.listdir(path):
        print(filename)
        if filename.endswith('records.xlsx'):
            records_files.append(filename)
        elif filename != '.DS_Store': #was not running due to a .ds_store file so I left it out
            rest_of_filenames.append(filename)

    sorted_rest_of_filenames = sorted(rest_of_filenames,reverse = True)
    return (sorted_rest_of_filenames + records_files)

#turns list of filenames into a list of dataframes
def get_list_of_dataframes(names:list) -> list:
    Dataframes = []
    for name in names:
        df = pd.read_excel(path + name)
        if name.startswith('Offense') or name.startswith('Defense'): #edit the dfs that start with offense/defense
            df.rename(columns={df.columns[-1]: 'Year', df.columns[2]: 'Team'}, inplace = True)
        #drop the first unnamed column
        if name != "Superbowl_winners.xlsx":
            df.drop(df.columns[0], axis=1,inplace = True)
        Dataframes.append(df)
    return Dataframes

#Puts the columns 'Team' and 'Year' in the first 2 columns of the Dataframe
def Team_n_year_n_records_to_front(df_merged:pd.DataFrame) -> pd.DataFrame:
    my_column = df_merged.pop('Team')
    my_column1 = df_merged.pop('Year')
    my_column2 = df_merged.pop('Superbowl_Winner')
    my_column3 = df_merged.pop('Superbowl_Loser_Team')
    my_column4 = df_merged.pop('Superbowl_Loser')
    my_column5 =  df_merged.pop('Wins')
    my_column6 = df_merged.pop('Losses')
    my_column7 = df_merged.pop('Ties')
    df_merged.insert(0, my_column.name, my_column)
    df_merged.insert(1, my_column1.name, my_column1)
    df_merged.insert(2, my_column2.name, my_column2)
    df_merged.insert(3, my_column3.name, my_column3)
    df_merged.insert(4, my_column4.name, my_column4)
    df_merged.insert(5, my_column5.name, my_column5)
    df_merged.insert(6, my_column6.name, my_column6)
    df_merged.insert(7, my_column7.name, my_column7)
    
    return df_merged[:-12]

#Merges all of the Dataframes and sorts them by year
def merge_n_sort(Dataframes: list) -> pd.DataFrame:
    #print(type(Dataframes[0]))
    superbowl_winners = Dataframes[0]
    overall_df_to_merge = Dataframes[1:-4] #includes everything except the records dfs and superbowl winners
    records_dfs = Dataframes[-4:] #includes only the records dfs

    #merge and sort the records dfs
    records_dfs_merged = reduce(lambda left, right: pd.merge(left, right, on=['Wins','Losses','Ties','Team','Year'],
                                                    how='outer'), records_dfs).fillna(-99999)
    records_dfs_merged.sort_values(by=['Year'], inplace = True)

    #Merge and sort the Superbowl_winners
    superbowl_merged = reduce(lambda left, right: pd.merge(left, right, on=['Team', 'Year'],
                                                    how='outer'), [superbowl_winners,records_dfs_merged]).fillna(0)
    overall_df_to_merge.append(superbowl_merged)

    #merge all dfs with the newly merged records
    df_merged = reduce(lambda left, right: pd.merge(left, right, on=['Team', 'Year'],
                                                    how='outer'), overall_df_to_merge).fillna(-99999)
    df_merged = Team_n_year_n_records_to_front(df_merged)

    return df_merged.sort_values(by=['Year'])


#Executable
path ='/Users/matthew/Google Drive/MSBA Grad Program/MSBA FALL quarter/BANA 212 (Data and Programming Analytics)/NFL Final project/NFL Excel Sheets/'
filenames = get_list_of_filenames(path)
Dataframes = get_list_of_dataframes(filenames)
df_merged = merge_n_sort(Dataframes)
df_merged.to_excel("NFL-merged.xlsx")






