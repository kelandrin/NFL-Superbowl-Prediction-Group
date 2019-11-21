import pandas as pd
import numpy as np
pd.set_option('display.width', 400)
#pd.set_option('display.max_rows', None)

df = pd.read_excel("NFL-merged.xlsx")

#change column names
df.rename(columns={'Offense_offensive_line_1st' : 'Offense_offensive_line_rush_left_1st_downs',
                         'Offense_offensive_line_Neg' : 'Offense_offensive_line_rush_left_stuff',
                         'Offense_offensive_line_+10Y' : 'Offense_offensive_line_rush_left_+10Y',
                         'Offense_offensive_line_Pwr' : 'Offense_offensive_line_rush_left_Pwr',
                         'Offense_offensive_line_1st.1': 'Offense_offensive_line_rush_center_1st_downs',
                         'Offense_offensive_line_Neg.1': 'Offense_offensive_line_rush_center_stuff',
                         'Offense_offensive_line_+10Y.1' : 'Offense_offensive_line_rush_center_+10Y',
                         'Offense_offensive_line_Pwr.1' : 'Offense_offensive_line_rush_center_Pwr',
                         'Offense_offensive_line_1st.2' : 'Offense_offensive_line_rush_right_1st_downs',
                         'Offense_offensive_line_Neg.2' : 'Offense_offensive_line_rush_right_stuff',
                         'Offense_offensive_line_+10Y.2' : 'Offense_offensive_line_rush_right_+10Y',
                         'Offense_offensive_line_Pwr.2' : 'Offense_offensive_line_rush_right_Pwr',
                         'Offense_kick_returns_Ret' : 'Offense_kick_returns',
                         'Offense_kick_returns_Avg' : 'Offense_kick_returns_Yds_Avg',
                         'Offense_kick_returns_Ret.1' : 'Offense_punt_returns',
                         'Offense_kick_returns_RetY' : 'Offense_punt_returns_Yds',
                         'Offense_kick_returns_Avg.1' : 'Offense_punt_returns_Yds_Avg',
                         'Offense_kick_returns_Lng.1' : 'Offense_punt_returns_Lng',
                         'Offense_kick_returns_TD.1' : 'Offense_punt_returns_TD',
                         'Offense_kick_returns_20+.1' : 'Offense_punt_returns_20+',
                         'Offense_kick_returns_40+.1' : 'Offense_punt_returns_40+',
                         'Offense_kick_returns_FC.1' : 'Offense_punt_returns_FC',
                         'Offense_kick_returns_FUM.1' : 'Offense_punt_returns_FUM',
                         'Offense_kicking_Ret' : 'Offense_kicking_returns',
                         'Offense_kicking_Avg.1' : 'Offense_kicking_returns_Avg',
                         'Offense_field_goals_A-M' : 'Offense_field_goals_A-M_1-19',
                         'Offense_field_goals_Pct.1' : 'Offense_field_goals_Pct_1-19',
                         'Offense_field_goals_A-M.1' : 'Offense_field_goals_A-M_20-29',
                         'Offense_field_goals_Pct.2' : 'Offense_field_goals_Pct_20-29',
                         'Offense_field_goals_A-M.2' : 'Offense_field_goals_A-M_30-39',
                         'Offense_field_goals_Pct.3' : 'Offense_field_goals_Pct_30-39',
                         'Offense_field_goals_A-M.3' : 'Offense_field_goals_A-M_40-49',
                         'Offense_field_goals_Pct.4' : 'Offense_field_goals_Pct_40-49',
                         'Offense_field_goals_A-M.4' : 'Offense_field_goals_A-M_50plus',
                         'Offense_field_goals_Pct.5' : 'Offense_field_goals_Pct_50plus',
                         'Offense_field_goals_Pct.6' : 'Offense_field_goals_XP Pct',
                         'Offense_field_goals_Blk.1' : 'Offense_field_goals_XK Blk',
                        },
                inplace=True)


#changing time of possession to datetime.time
def change_time_type(df:pd.DataFrame) ->pd.DataFrame:
    for i in df.columns:
        if i.endswith('ToP/G'):
            if i == 'Defense_game_stats_ToP/G':
                df[i] = df[i].str.replace('--', '0:00')
            df[i] = pd.to_datetime(df[i], format='%M:%S').dt.time
    return df

#take out any spaces in column names
def remove_space_in_col_name(df:pd.DataFrame) -> pd.DataFrame:
    new_list = []
    for i in df.columns:
        split = i.split()
        if len(split)==2:
            string = split[0] + '_' + split[1]
            new_list.append(string)
        else:
            new_list.append(i)

    df.columns = new_list
    return df

def split_function(nfl_data:pd.DataFrame) -> pd.DataFrame:

    for i in nfl_data.columns:

            if i.startswith('Offense_field_goals_A-M'):

                #split every A-M column into two columns in the dataframe at '-'
                new = nfl_data[i].str.split('-', n = 1, expand = True)

                #find location of the A-M column and split the column name to remove 'A-M'
                location = nfl_data.columns.get_loc(i)
                split_values = i.split('_')

                #change the name of new columns
                new_name_1 = split_values [0] + '_' + split_values [1] + '_' + split_values [2] + '_' + '_Attempts_' + split_values [4]
                new_name_2 = split_values [0] + '_' + split_values [1] + '_' + split_values [2] + '_' + '_Made_' + split_values [4]

                #replace missing value with -99999
                new[0] = new[0].replace('', -99999.9, regex=True)
                new[1] = new[1].replace('-', -99999.9, regex=True)

                #change data type of two new columns from string to integer
                new[0] = new[0].astype(int)
                new[1] = new[1].astype(int)

                #insert two new columns to the right of orginal A-M column
                nfl_data.insert(location + 1, new_name_1, new[0])
                nfl_data.insert(location + 2, new_name_2, new[1])

                #drop the original A-M column
                nfl_data.drop(columns =[i], inplace = True)

    return nfl_data

def _split_T_in_col(nfl: pd.DataFrame, column: pd.Series):

    x = column.replace('T', '', regex=True)
    y = column.replace('^-?\d+', '', regex=True)

    y.where(y == 'T',other = 1,inplace = True)
    y.where(y != 'T', other=0,inplace = True )

    x.name = column.name
    y.name = column.name + "_T"

    nfl[x.name] = x
    nfl[y.name] = y

def split_T(nfl_data: pd.DataFrame) -> pd.DataFrame:

    for col in nfl_data.columns:

        if col.endswith('_Lng'):
            _split_T_in_col(nfl_data,nfl_data[col])
            location = nfl_data.columns.get_loc(col)
            popped = nfl_data.pop(col + '_T')
            nfl_data.insert(location + 1, popped.name, popped)

    return nfl_data

def replace_data_to_largeneg(df:pd.DataFrame) -> pd.DataFrame:
    return df.replace("--", -99999)

def remove_commas(df:pd.DataFrame) -> pd.DataFrame:
    cols_to_check = [i for i in df.columns]
    df[cols_to_check] = df[cols_to_check].replace({',': ''}, regex=True)
    return df

def change_column_types_int(df:pd.DataFrame) -> pd.DataFrame:
    for col, dtype in zip(df.columns, df.dtypes):
        if dtype == object:
            try:
                df[col] = df[col].astype(int)
            except:
                continue
    return df

def convert_to_int(df:pd.DataFrame,i:str) ->pd.DataFrame:
    df[i] = df[i].replace('-',np.NaN)
    df[i] = df[i].fillna(-99999)
    df[i] = list(map(int, df[i]))
    return df.astype({i:int})

def change_column_types_float(df: pd.DataFrame) -> pd.DataFrame:
    for col, dtype in zip(df.columns, df.dtypes):
        if dtype == object:
            try:
                df[col].astype(np.float64)
                df[col] = pd.to_numeric(df[col], errors='coerce')
                df = df.replace(np.nan, -99999.9, regex=True)
            except:
                continue
    return df

def Categorize(df:pd.DataFrame,list_to_categorize:list) ->pd.DataFrame:
    for i in list_to_categorize:
        df[i] = df[i].astype('category')
    return df


#Executable
df = change_time_type(df)
df = remove_space_in_col_name(df)
df = split_function(df)
df = split_T(df)
df = replace_data_to_largeneg(df)
df = remove_commas(df)
df = change_column_types_int(df)
df = change_column_types_float(df)
df = convert_to_int(df,"Offense_game_stats_TO")
df = Categorize(df, ["Team","Superbowl_Winner","Superbowl_Loser_Team","Superbowl_Loser"])

### check all "objects" to see what we have left to clean
listx = []
for i,j in zip(df.columns,df.dtypes):
    if j == object :
        listx.append(i)
        print(df[i])

df.to_excel('Clean_Merged_Data.xlsx')





