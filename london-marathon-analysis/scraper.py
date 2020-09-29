import requests
from bs4 import BeautifulSoup
import pandas as pd
import numpy as np

# Functions
def createPageData(entries):
    pageData = []
    for idx, i in enumerate(entries):
        row = entries[idx].select('div.list-field')
        entry = []
        for idx, j in enumerate(row):
            rowValue = row[idx].getText()
            entry.append(rowValue)
        pageData.append(entry)
    return pageData

def cleanData(pageData):
    for idx, i in enumerate(pageData):
        row = pageData[idx]
        for idxx, j in enumerate(row):
            if idxx == 3:
                row[idxx] = row[idxx][4:]
            elif idxx == 4:
                row[idxx] = row[idxx][13:]
            elif idxx == 5:
                row[idxx] = row[idxx][8:]
            elif idxx == 6:
                row[idxx] = row[idxx][4:]
            elif idxx == 7:
                row[idxx] = row[idxx][6:]
        pageData[idx] = row
    return pageData

# Collecting the 2019 data
page = 1
flag = 0
while flag == 0:
    try:
        if page == 1:
            res = requests.get('https://results.virginmoneylondonmarathon.com/2019/?page=' + str(page) + '&event=MAS&pid=search')
            soup = BeautifulSoup(res.text, 'html.parser')
            entries = soup.select('li.list-group-item.row')
            pageData = createPageData(entries)
            data = pd.DataFrame(data = None, columns = pageData[0][:3] + pageData[0][4:-1])
            pageData = pageData[1:]
            pageData = cleanData(pageData)
            for idx, i in enumerate(pageData):
                rowData = pageData[idx][:-1]
                a_series = pd.Series(rowData, index = data.columns)
                data = data.append(a_series, ignore_index=True)
            page += 1
        else:
            res = requests.get('https://results.virginmoneylondonmarathon.com/2019/?page=' + str(page) + '&event=MAS&pid=search')
            soup = BeautifulSoup(res.text, 'html.parser')
            entries = soup.select('li.list-group-item.row')
            pageData = createPageData(entries)
            pageData = pageData[1:]
            pageData = cleanData(pageData)
            for idx, i in enumerate(pageData):
                rowData = pageData[idx][:-1]
                a_series = pd.Series(rowData, index = data.columns)
                data = data.append(a_series, ignore_index=True)
            page += 1
    except ValueError:
        print("Oops! No values on this page...")
        flag = 1

data.to_csv('./data/results2019.csv', index=False)