import pandas as pd
import requests
from bs4 import BeautifulSoup
import numpy as np


def get_url(month):
    url = f'https://www.basketball-reference.com/leagues/NBA_2025_games-{month}.html'
    return url

def fixtures_heading():
    '''
    Creates an empty dataframe with column headings 
    '''
    response = requests.get(get_url('december'))
    soup = BeautifulSoup(response.text, 'html.parser')
    table = soup.find('table',class_ = {'suppress_glossary', 'sortable', 'stats_table', 'now_sortable'})
    headings = [th.text for th in table.find('thead').find_all('th')]
    headings[3] = 'PTS_Visitor'
    headings[5] = 'PTS_Home'
    fixtures = pd.DataFrame(columns=headings)
    return fixtures

def add_table_data(table, dataframe):
    table_body = table.find('tbody')
    for row in table_body.find_all('tr'):
        data = []
        row_date = row.find('th')
        data.append(row_date.text)
        for td in row.find_all('td'):
            data.append(td.text) 
        dataframe.loc[len(dataframe)] = data

def load_fixtures()-> pd.DataFrame:
    '''
    load fixtures
    returns: pd.DataFrame
    '''
    print('Loading Fixtures from url')
    df = fixtures_heading()
    months = ['october', 'november', 'december', 'january', 'february', 'march', 'april']
    for month in months:
        url = get_url(month)
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')
        table = soup.find('table',class_ = {'suppress_glossary', 'sortable', 'stats_table', 'now_sortable'}) 
        add_table_data(table, df)
    df.replace('', np.nan, inplace = True)
    return df

def completed_fixtures(df: pd.DataFrame)-> pd.DataFrame:
    '''
    Take the whole schedule and returns the completed fixtures
    '''
    completed = df.dropna(subset=['PTS_Visitor', 'PTS_Home'])
    #Removing the in-season tournament
    completed = completed[completed['Notes'] != 'In-Season Tournament']
    completed['PTS_Home'] = completed['PTS_Home'].astype(int)
    completed['PTS_Visitor'] = completed['PTS_Visitor'].astype(int)
    return completed