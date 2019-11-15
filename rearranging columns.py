# -*- coding: utf-8 -*-
"""
Created on Thu Nov 14 13:59:29 2019

@author: vedan
"""

from bs4 import BeautifulSoup
import pandas as pd
import requests
import numpy as np


data = pd.read_excel(r'C:\Users\vedan\Desktop\studies\UCI\Fall Semester\Data and Programming Analytics\project files\NFL-merged.xlsx')


def rearrange_and_space(data):
    cols = list(data.columns.values)
    count = 0

    new_cols = ['Team','Year']
    temp = []
    for iterator in range(227):        
        if cols[iterator+2][-2:] == "Rk":
            new_cols.append(cols[iterator+2])
        else:
            temp.append(cols[iterator+2])
            count = count+1

    for iterator in range(count):
        new_cols.append(temp[iterator])
    
#for iterator in range(229):
#    if (' ' in new_cols[iterator]):
#        new_cols[iterator] = new_cols[iterator].replace(' ', '_')
#    else:
#        dummy = dummy+1
    
#new_cols = [x.replace(" ", "_") for x in new_cols]

#for i in new_cols:
#    split = i.split()
#    if len(split)==2:
#        string = split[0] + '_' + split[1]
#        print(string)
#    new_cols = string

    data = data[new_cols]

 
    new_list = []
    for i in data.columns:
        split = i.split()
        if len(split)==2:
            string = split[0] + '_' + split[1]
            new_list.append(string)
        else:
            new_list.append(i)

    print(len(new_list))

    data.columns = new_list
    for i in data.columns:
        print(i)



