#!/usr/bin/env python
# coding: utf-8

# In[134]:


# modules we will use
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# read in all our data
nfl_data = pd.read_csv("NFL-merged.csv", skiprows = 0)

# set seed for reproducibility
np.random.seed(0) 


# In[135]:


# number of rows and columns
nfl_data.shape
# to get the column names
# nfl_data.names[:231] - code is wrong need to fix


# In[136]:


# number of dimensions
nfl_data.ndim


# In[ ]:


# look at first few rows of the nfl_data file
# nfl_data.sample(5)
nfl_data.head(5)


# In[ ]:


# look at last few rows of the nfl_data file
nfl_data.tail(5)


# In[ ]:


# to get the datatype
nfl_data.dtypes


# In[ ]:


# to change the data type
# nfl_data['Offense_scoring_2-PT'].astype(str)


# In[ ]:


# get the number of missing data points per column
missing_values_count = nfl_data.isnull().sum()

# look at the number of missing points in the first ten columns
missing_values_count[0:231]


# In[8]:


# how many total missing values do we have?
total_cells = np.product(nfl_data.shape)
total_missing = missing_values_count.sum()

# percent of data that is missing
(total_missing/total_cells) * 100


# In[ ]:


# get basic statistics on dataframe 
nfl_data.describe()


# In[ ]:


# get basic statistics of one column
nfl_data['Offense_scoring_2-PT'].describe()


# In[ ]:


# replace all NA's with -99999 - need to update it doesn't work
nfl_data.fillna(-99999)


# In[ ]:


# looping through to see column names
for col in nfl_data.columns: 
    print(col) 


# In[ ]:


# change column names with .1 .2 .3 to correct names
#nfl_data.rename(columns={'oldName1': 'newName1', 'oldName2': 'newName2'}, inplace=True)
nfl_data.rename(columns={'Offense_offensive_line_1st' : 'Offense_offensive_line_rush_left_1st_downs',
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
                         'Offense_field_goals_Pct_1-19' : 'Offense_field_goals_A-M_20-29',
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

# loop through data columns 
for col in nfl_data.columns: 
    print(col) 


# In[ ]:


# view data column
# nfl_data.Offense_rushing_Lng
# nfl_data['Offense_rushing_Lng']
nfl_data.iloc[:,21]


# In[139]:


# get column index from column name
# nfl_data.columns.get_loc('Offense_rushing_Lng':'Offense_passing_Lng')
def column_index(nfl_data, query_cols):
    cols = nfl_data.columns.values
    sidx = np.argsort(cols)
    return sidx[np.searchsorted(cols,query_cols,sorter=sidx)]
column_index(nfl_data, ['Offense_rushing_Lng', 
                        'Offense_passing_Lng',
                        'Offense_kick_returns_Lng',
                        'Offense_punt_returns_Lng',
                        'Defense_rushing_Lng',
                        'Defense_passing_Lng',
                        'Defense_interceptions_Lng'
                        'Offense_punt_returns_Lng'])


# In[140]:


# get column name from column location
nfl_data.iloc[:,22].name


# In[ ]:


# split T's from Touchdowns numeric variables
new = nfl_data['Offense_rushing_Lng'].str.split('(\d+)([A-Za-z]+)', expand=True)
new = new.loc[:,[1,2]]
new.rename(columns={1:'Yds', 2:'TD'}, inplace=True)
print(new)


# In[142]:


# insert new columns in the nfl_data dataframe
# nfl_data.insert(21, "new", True) 
# nfl_data.append(new)
# nfl_data.insert(22, column, value, allow_duplicates = False)
yds = new.pop('Yds')
td = new.pop('TD')
nfl_data.insert(22,'Yds', yds)
nfl_data.insert(23,'TD', td)


# In[153]:


nfl_data.shape


# In[ ]:


nfl_data[nfl_data.columns[22:24]]

