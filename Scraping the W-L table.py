# -*- coding: utf-8 -*-
"""
Created on Thu Nov  7 14:24:30 2019

@author: vedan
"""

from bs4 import BeautifulSoup
import pandas as pd
import requests
import numpy as np

data = []
data2 = []
data3 = []
data4 = []
data5 = []
data6 = []
dummy = 0
count = 0


#extracting 1967-1969
for iterator in range(3):
    data2 = []
    dummy = 0
    url = 'https://www.pro-football-reference.com/years/'+str(1967+iterator)+'/?fbclid=IwAR0e5yh3DnxvXdo9QjnutpqeDalmDsylERCbEGcusCAT4152LfkPRA0muMU'
    page = requests.get(url)
    soup = BeautifulSoup(page.text,'lxml')
    table = soup.findAll('table', {'id':['NFL']})
    table_body = table[0].find('tbody')

    rows = table_body.find_all('tr')
    for row in rows:
        cols = row.find_all('td')
        cols = [ele.text.strip() for ele in cols]
        data.append([ele for ele in cols if ele])
    

    rows = table_body.find_all('th')
    for row in rows:
        cols = row.find_all('a')
        cols = [ele.text.strip() for ele in cols]
        data2.append([ele for ele in cols if ele])
    
    for i in range(20):
        if i==0 or i==5 or i==10 or i==15:
            dummy = dummy + 1
        else:
            data[i+(iterator*20)].append(data2[i-dummy])


#extracting AFC rankings
for iterator in range(49):
    data4 = []
    dummy = 0
    url = 'https://www.pro-football-reference.com/years/'+str(1970+iterator)+'/?fbclid=IwAR0e5yh3DnxvXdo9QjnutpqeDalmDsylERCbEGcusCAT4152LfkPRA0muMU'
    page = requests.get(url)
    soup = BeautifulSoup(page.text,'lxml')
    table = soup.findAll('table', {'id':['AFC']})
    table_body = table[0].find('tbody')

    rows = table_body.find_all('tr')
    for row in rows:
        cols = row.find_all('td')
        cols = [ele.text.strip() for ele in cols]
        data3.append([ele for ele in cols if ele])
    

    rows = table_body.find_all('th')
    for row in rows:
        cols = row.find_all('a')
        cols = [ele.text.strip() for ele in cols]
        data4.append([ele for ele in cols if ele])
    
    for i in range(len(data4)):
        if data3[i+count][0] =='AFC East' or data3[i+count][0] =='AFC Central' or data3[i+count][0] =='AFC West':
            dummy = dummy + 1
        else:
            data3[i+count].append(data4[i-dummy])
    count = count + len(data4)        

#extracting NFC rankings
for iterator in range(49):
    data6 = []
    dummy = 0
    url = 'https://www.pro-football-reference.com/years/'+str(1970+iterator)+'/?fbclid=IwAR0e5yh3DnxvXdo9QjnutpqeDalmDsylERCbEGcusCAT4152LfkPRA0muMU'
    page = requests.get(url)
    soup = BeautifulSoup(page.text,'lxml')
    table = soup.findAll('table', {'id':['NFC']})
    table_body = table[0].find('tbody')

    rows = table_body.find_all('tr')
    for row in rows:
        cols = row.find_all('td')
        cols = [ele.text.strip() for ele in cols]
        data5.append([ele for ele in cols if ele])
    
    rows = table_body.find_all('th')
    for row in rows:
        cols = row.find_all('a')
        cols = [ele.text.strip() for ele in cols]
        data6.append([ele for ele in cols if ele])
    
    for i in range(len(data6)):
        if i==0 or i==6 or i==11:
            dummy = dummy + 1
        else:
            data5[i+(iterator*16)].append(data6[i-dummy])

#data = pd.DataFrame(data)
#data3 = pd.DataFrame(data3)
#data5 = pd.DataFrame(data5)
#data.to_excel(r'C:\Users\vedan\Desktop\studies\UCI\Fall Semester\Data and Programming Analytics\project files\NFL.xlsx')
#data3.to_excel(r'C:\Users\vedan\Desktop\studies\UCI\Fall Semester\Data and Programming Analytics\project files\AFC.xlsx')
#data5.to_excel(r'C:\Users\vedan\Desktop\studies\UCI\Fall Semester\Data and Programming Analytics\project files\NFC.xlsx')