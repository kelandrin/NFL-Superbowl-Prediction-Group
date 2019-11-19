# -*- coding: utf-8 -*-
"""
Created on Thu Nov  7 14:24:30 2019

@author: vedan/matthew
"""
from bs4 import BeautifulSoup
import pandas as pd
import requests

#Gathers the team name from the table
def get_team_names(table_body, data_list:list):
    rows = table_body.find_all('th')
    for row in rows:
        cols = row.find_all('a')
        cols = [ele.text.strip() for ele in cols]
        for ele in cols:
            if ele:
                print(ele)
                data_list.append(ele)

#Makes the beautiful soup from the NFL string
def make_soup(year:int, conference:str) -> BeautifulSoup:

    url = 'https://www.pro-football-reference.com/years/' + str(
        year) + '/?fbclid=IwAR0e5yh3DnxvXdo9QjnutpqeDalmDsylERCbEGcusCAT4152LfkPRA0muMU'

    if conference == 'AFL':
        url = 'https://www.pro-football-reference.com/years/' + str(year) + '_AFL'

    page = requests.get(url)
    soup = BeautifulSoup(page.text,'lxml')
    table = soup.findAll('table', {'id':[conference]})
    table_body = table[0].find('tbody')
    return table_body

def quick_clean(df:pd.DataFrame) -> pd.DataFrame:

    #select relevant columns
    clean_df = df.iloc[:,[0,1,2,12,13]]
    #rename columns
    clean_df.columns = ['Wins', 'Losses', 'Ties','Year', 'Team']
    #Change data types to ints
    clean_df['Wins'] = clean_df['Wins'].astype(int)
    clean_df['Losses'] = clean_df['Losses'].astype(int)
    clean_df['Ties'] = clean_df['Ties'].astype(int)

    return clean_df

#Scrapes NFL W-L-Tie based on conferences [NFL,AFC,NFC]
def conference_scrape(conference: str) -> pd.DataFrame:
    ready_for_df = []

    if conference == 'NFL' or conference == 'AFL':
        times = 3
        start_year = 1967
    else:
        times = 50
        start_year = 1970

    for iterator in range(times):
        temp_data =[]
        teams = []
        year = start_year + iterator
        table_body = make_soup(year, conference)
        get_team_names(table_body, teams)

        rows = table_body.find_all('tr')
        for row in rows:
            if len(row.text) > 15:
                cols = row.find_all('td')
                cols = [ele.text.strip() for ele in cols]
                cols.append(year)
                if '.' in cols[2]:
                    cols.insert(2,0)
                temp_data.append(cols)

        for i, j in enumerate(temp_data):
            print("i")
            print(i)
            print("j")
            print(j)
            j.append(teams[i])

        for i in temp_data:
            ready_for_df.append(i)

    df = pd.DataFrame(ready_for_df)
    return quick_clean(df)

#executable
AFL = conference_scrape("AFL")
NFL = conference_scrape("NFL")
NFC = conference_scrape("NFC")
AFC = conference_scrape("AFC")

print(AFL)
print(AFC)
print(NFL)
print(NFC)
NFL.to_excel('NFL_records.xlsx')
AFC.to_excel('AFC_records.xlsx')
NFC.to_excel('NFC_records.xlsx')
AFL.to_excel('AFL_records.xlsx')