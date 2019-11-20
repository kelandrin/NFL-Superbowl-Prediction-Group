# -*- coding: utf-8 -*-
"""
Created on Wed Nov 20 00:08:17 2019

@author: Liz
"""
#convert object column to integer
import pandas as pd
from pandas import Series
import numpy as np

nfl = pd.read_excel("NFL-merged.xlsx")
list(nfl.columns)
print(nfl["Offense_game_stats_TO"].dtypes)

#replace str'-'
def convert_int(i):
    nfl[i] = nfl[i].replace('-',np.NaN)
    nfl[i] = nfl[i].fillna(0)
    return nfl.astype({i:int})

convert_int("Offense_game_stats_TO")
nfl["Offense_game_stats_TO"]
nfl["Offense_game_stats_TO"] = list(map(int,nfl["Offense_game_stats_TO"]))