# -*- coding: utf-8 -*-
"""
Created on Fri Nov  1 12:40:51 2019

@author: vedant / Matthew
"""

from bs4 import BeautifulSoup
import pandas as pd
import requests
import numpy as np

#Defining NFL category object
class NFL_category_obj:
    def __init__ (self, nfl_tuple: tuple):

        data_list = nfl_tuple[0].split(",")

        if data_list[0] == "Offense":
            self.tm_opp = "TM"
            self.fense = "Offense"
        else:
            self.tm_opp = "OPP"
            self.fense = "Defense"

        self.category = data_list[1].upper()
        self.columns = data_list[2:]
        self.columns_not_wanted = nfl_tuple[1]

#Offensive strings
o1 = 'Offense,Game_Stats,Rk,Team,G,Pts/G,TotPts,Scrm Plys,Yds/G,Yds/P,1st/G,3rd Md,3rd Att,3rd Pct,4th Md,4th Att,4th Pct,Pen,Pen Yds,ToP/G,FUM,Lost,TO,Year'
o2 = 'Offense,Passing,Rk,Team,G,Pts/G,TotPts,Comp,Att,Pct,Att/G,Yds,Avg,Yds/G,TD,Int,1st,1st%,Lng,20+,40+,Sck,Rate,Year'
o3 = 'Offense,rushing,Rk,Team,G,Pts/G,TotPts,Att,Att/G,Yds,Avg,Yds/G,TD,Lng,1st,1st%,20+,40+,FUM,Year'
o4 = 'Offense,receiving,Rk,Team,G,Pts/G,TotPts,Rec,Yds,Avg,Yds/G,Lng,TD,20+,40+,1st,1st%,FUM,Year'
o5 = 'Offense,kicking,Rk,Team,G,Pts/G,TotPts,KO,Yds,OOB,Avg,TB,Pct,Ret,Avg,TD,OSK,OSKR,Year'
o6 = 'Offense,field_goals,Rk,Team,G,Pts/G,TotPts,FGM,FG Att,Pct,Blk,Lng,A-M,Pct,A-M,Pct,A-M,Pct,A-M,Pct,A-M,Pct,XPM,XP Att,Pct,Blk,Year'
o7 = 'Offense,kick_returns,Rk,Team,G,Pts/G,TotPts,Ret,Yds,Avg,Lng,TD,20+,40+,FC,FUM,Ret,RetY,Avg,Lng,TD,20+,40+,FC,FUM,Year'
o8 = 'Offense,punting,Rk,Team,G,Pts/G,TotPts,Punts,Yds,Net Yds,Lng,Avg,Net Avg,Blk,OOB,Dn,IN 20,TB,FC,Ret,RetY,TD,Year'
o9 = 'Offense,scoring,Rk,Team,G,Pts/G,TotPts,Pts,Pts/G,Rsh,Rec,PRet,KRet,INT,FUM,Blk FG,Blk Pnt,XPM,FGM,SFTY,2-PT,Year'
o10 = 'Offense,touchdowns,Rk,Team,G,Pts/G,TotPts,Total,Rsh,Rec,Ret,Def,Year'
o11 = 'Offense,Offensive_line,Rk,Team,Exp,Att,Yds,Avg,TDs,1st,Neg,+10Y,Pwr,1st,Neg,+10Y,Pwr,1st,Neg,+10Y,Pwr,Sacks,QB Hits,Year'

#Defensive strings
d1 = 'Defense,Game_Stats,Rk,Team,G,Pts/G,TotPts,Scrm Plys,Yds/G,Yds/P,1st/G,3rd Md,3rd Att,3rd Pct,4th Md,4th Att,4th Pct,Pen,Pen Yds,ToP/G,FUM,Lost,Year'
d2 = 'Defense,Passing,Rk,Team,G,Pts/G,TotPts,Comp,Att,Pct,Att/G,Yds,Avg,Yds/G,TD,Int,1st,1st%,Lng,20+,40+,Sck,Rate,Year'
d3 = 'Defense,rushing,Rk,Team,G,Pts/G,TotPts,Att,Att/G,Yds,Avg,Yds/G,TD,Lng,1st,1st%,20+,40+,FUM,Year'
d4 = 'Defense,receiving,Rk,Team,G,Pts/G,TotPts,Rec,Yds,Avg,Yds/G,Lng,TD,20+,40+,1st,1st%,FUM,Year'
d5 = 'Defense,Scoring,Rk,Team,G,Pts/G,TotPts,Pts,Pts/G,Rsh,Rec,PRet,KRet,INT,FUM,Blk FG,Blk Pnt,XPM,FGM,SFTY,2-PT,Year'
d6 = 'Defense,touchdowns,Rk,Team,G,Pts/G,TotPts,Total,Rsh,Rec,Ret,Def,Year'
d7 = 'Defense,Tackles,Rk,Team,G,Pts/G,TotPts,Comb,Total,Ast,Sck,SFTY,PDef,Int,TDs,Yds,Lng,FF,Rec,TD,Year'
d8 = 'Defense,interceptions,Rk,Team,G,Pts/G,TotPts,Comb,Total,Ast,Sck,SFTY,PDef,Int,TDs,Yds,Lng,FF,Rec,TD,Year'

#Creating tuples of (offense/defense string, list_of_cols_not_wanted)
list_of_tables = [(o1,[]),(o2,['G','Pts/G','TotPts','TD']),(o3,['G','Pts/G','TotPts','TD']),
                           (o4,['G','Pts/G','TotPts','Rec','Avg','Yds/G','Lng','TD','20+','40+','1st','1st%']),
                           (o5,['G','Pts/G','TotPts']),(o6,['G','Pts/G','TotPts']),(o7,['G','Pts/G','TotPts']),
                           (o8,['G','Pts/G','TotPts']),(o9,['G','Pts/G','TotPts','Pts','Pts/G','Rsh','Rec','PRet','KRet','XPM','FGM']),
                           (o10,['G','Pts/G','TotPts','Ret',]),(o11,['Att','Yds','Avg','TDs']),
                           (d1,[]),(d2,['G','Pts/G','TotPts','TD']),(d3,['G','Pts/G','TotPts','TD']),
                           (d4,['G','Pts/G','TotPts','Rec','Avg','Yds/G','Lng','TD','20+','40+','1st','1st%']),
                           (d5,['G','Pts/G','TotPts','Pts','Pts/G','Rsh','Rec']),(d6,['G','Pts/G','TotPts']),
                           (d7,['G','Pts/G','TotPts','SFTY','PDef','Int','TDs','Yds','Lng']),(d8,['G','Pts/G','TotPts','Comb','Total','Ast','Sck','SFTY','FF','Rec','TD'])]


#Creating NFL category objects out of tables
list_of_NFL_category_objs = []
for table in list_of_tables:
    list_of_NFL_category_objs.append(NFL_category_obj(table))


#Function takes in an nfl object and scrapes the relevant tables from NFL.com. Writes scraped material to excel.
def scraper(nfl: object, offensive_category = 'null', defensive_category = 'null'):

    #Setting offensive / defensive category for url
    if nfl.tm_opp == "TM":
        offensive_category = nfl.category
    else:
        defensive_category = nfl.category

    print("###########################################")
    print(nfl.fense + '_' + nfl.category)

    #Create dataframe
    answer = pd.DataFrame(columns=(nfl.columns))
    i = 0

    for iterator in range(53):
        #making soup
        url = 'http://www.nfl.com/stats/categorystats?archive=true&conference=null&role=' + nfl.tm_opp + '&offensiveStatisticCategory=' + offensive_category + '&defensiveStatisticCategory=' + defensive_category + '&season='+str(iterator+1967)+'&seasonType=REG&tabSeq=2&qualified=false&Submit=Go'
        page = requests.get(url)
        soup = BeautifulSoup(page.text,'lxml')
        table = soup.find('table', {'id':['result']})

        #Attempt to scrape
        try:
            table_body = table.find('tbody')
            rows = table_body.find_all('tr')
            for row in rows:
                cols = row.find_all('td')
                cols = [ele.text.strip() for ele in cols]
                cols.append(iterator+1967)
                answer.loc[i] = list(cols)
                i = i+1

        #catches the error when there is no table to scrape
        except AttributeError:
            continue

    #drop repeated columns
    answer.drop(columns=nfl.columns_not_wanted, inplace=True)

    #add fense and category to file name
    answer = answer.add_prefix(str(nfl.fense) + '_' + str(nfl.category).lower() + '_')

    #write to excel
    answer.to_excel(nfl.fense + '_' + nfl.category + ".xlsx")

#Call Scraper function on each nfl_category_obj
for nfl_obj in list_of_NFL_category_objs:
    scraper(nfl_obj)