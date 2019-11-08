from bs4 import BeautifulSoup
import pandas as pd
import requests
import numpy as np



answer = pd.DataFrame({'Wins':[],'Losses':[],'Ties':[],'Team':[]})
#i = 1970
#Function takes in an nfl object and scrapes the relevant tables from NFL.com. Writes scraped material to excel.
def scraper(nfl: pd.DataFrame):
    for iterator in range(1):
        i = 1967
        #making soup
        url = 'https://www.pro-football-reference.com/years/' + str(i)
        page = requests.get(url)
        soup = BeautifulSoup(page.text,'html.parser')
        #row = soup.find('tr',{'data-row'})
        headers = soup.findAll('tr',{'thead onecell':[]})


        for i in headers:
            row = soup.findAll('tr',{"data-row": []})
            for j in row:
                for k in j.children:
                    try:
                        #teams = soup.find('a',{'href':[]})
                        print(k)
                        if k.attrs['data-stat'] in ['wins','losses','ties','team']:
                            print(k.string)
                        #print(teams)
                            #answer.loc[k] = list(k.string)
                            #print(k.string)
                    except:
                        continue


    #print(answer.head())
                    #print(k.findAll('td'))
                    #print(k.attrs)
                    #print(type(k))

                    #print(k)
                    #data = k.find('td')
                    #print(data)
                    #print(k.string)
                #stats = j.findAll('th',{'data-stat'})
                #stats = j.findAll('th',{'data-stat':['wins','losses','ties']})
                #wins':[],'losses':[],'ties':[]}})
                #print(stats)
                #print(j)
                #stats = j.findAll('data-stat',{'wins':[],'losses':[],'ties':[]})
                #team =  row.findAll('a',{'href':[]})
                #print(j)
                #print(stats)
                #print(j)
            #for i in row:
                #print(soup.findAll('td'))
            #print(i.findAll('data-stat'))


        #print(row)

        #for i in row:
        #    print(i)
            #if "wins" in i:
            #    print(i)
            # for j in i:
            #     col = j.find('td')
            #     print(col)
            # for j in i:
            #     :
            #         print(q)
            #print(row.children.string)
            #print(row.children)
            #for i in row.children:
            #    print(i.string)




        #print(row)
        #print(soup.prettify())
        #body = soup.find('body')
        #table = soup.find('main', {'data-radium':['true']})
        #tr = soup.find('table',{'class':['css-rhj265']})
        #print(tr)

        #print(table)
        #print(body.prettify())
        #table = body.find('table')
        #print(table)
'''
        table_body = table.find('tbody')
        rows = table_body.find_all('tr')
        for row in rows:
            cols = row.find_all('td')
            cols = [ele.text.strip() for ele in cols]
            cols.append(iterator + 1967)
            answer.loc[i] = list(cols)
            i = i + 1
'''
        #print(soup.prettify())
        #table = soup.find('table', {'id':['result']})
        #for tr in soup.find_all('tr'):
        #    tds = tr.find_all('td')
        #    print(tds)
        #table = soup.find('table')
        #for i in table:
        #    print(i)
        #Attempt to scrape

        #table_body = table.find('tbody')
        # rows = table_body.find_all('tr')
        # for row in rows:
        #     cols = row.find_all('td')
        #     cols = [ele.text.strip() for ele in cols]
        #     print(cols)
        #     #cols.append(iterator+1967)
        #     answer.loc[i] = list(cols)
        #     i = i+1

scraper(answer)