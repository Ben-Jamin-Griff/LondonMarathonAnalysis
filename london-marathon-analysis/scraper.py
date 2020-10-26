import requests
from bs4 import BeautifulSoup
#import pandas as pd
import numpy as np
import re
import time
import datetime
import pickle

begin_time = datetime.datetime.now()

# Functions
def createPageData(entries, year):
    if len(entries) == 2:
        return
    pageData = []
    for idx, i in enumerate(entries):
        idx +=1
        if idx == len(entries):
            return pageData
        row = entries[idx].select('div.list-field')
        name = entries[idx].select('h4.list-field')[0].getText()[:-6]
        country = entries[idx].select('h4.list-field')[0].getText()[-4:-1]
        link = entries[idx].select('a', href=True)[0]['href']
        link = 'https://results.virginmoneylondonmarathon.com/' + str(year) + '/' + str(link)
        splits = getSplits(link)
        entry = []
        for idx, j in enumerate(row):
            rowValue = row[idx].getText()
            entry.append(rowValue)
        entry.insert(3, name)
        entry.insert(4, country)
        entry = entry[:-1]
        entry = entry + splits
        pageData.append(entry)
    return pageData

def getSplits(link):
    #time.sleep(1)
    resLink = requests.get(link)
    soupLink = BeautifulSoup(resLink.text, 'html.parser')
    splits = []
    status = soupLink.select('td.f-race_status')[0].getText()
    matched = re.match('Finished',status)
    if matched:
        splits.append(status)
        split5k = soupLink.select('tr.f-time_01')[0].getText()[13:21]
        splits.append(split5k)
        split10k = soupLink.select('tr.f-time_02')[0].getText()[14:22]
        splits.append(split10k)
        split15k = soupLink.select('tr.f-time_03')[0].getText()[14:22]
        splits.append(split15k)
        split20k = soupLink.select('tr.f-time_04')[0].getText()[14:22]
        splits.append(split20k)
        splitHalf = soupLink.select('tr.f-time_05')[0].getText()[15:23]
        splits.append(splitHalf)
        split25k = soupLink.select('tr.f-time_06')[0].getText()[14:22]
        splits.append(split25k)
        split30k = soupLink.select('tr.f-time_07')[0].getText()[14:22]
        splits.append(split30k)
        split35k = soupLink.select('tr.f-time_08')[0].getText()[14:22]
        splits.append(split35k)
        split40k = soupLink.select('tr.f-time_09')[0].getText()[14:22]
        splits.append(split40k)
        splitFinish = soupLink.select('tr.f-time_finish_netto')[0].getText()[13:21]
        splits.append(splitFinish)
    else:
        splits.append(status)
        splits.append('-')
        splits.append('-')
        splits.append('-')
        splits.append('-')
        splits.append('-')
        splits.append('-')
        splits.append('-')
        splits.append('-')
        splits.append('-')
        splits.append('-')
    return splits

def createColumnData(entries):
    columnData = []
    firstRow = entries[0].select('div.list-field')
    for idx, i in enumerate(firstRow):
        if idx == 4:
            rowValue = firstRow[idx].getText()[4:]
            columnData.append(rowValue)
        elif idx == 5:
            rowValue = firstRow[idx].getText()[13:]
            columnData.append(rowValue)
        elif idx == 6:
            rowValue = firstRow[idx].getText()[8:]
            columnData.append(rowValue)
        elif idx == 7:
            rowValue = firstRow[idx].getText()[4:]
            columnData.append(rowValue)
        elif idx == 8:
            rowValue = firstRow[idx].getText()[6:]
            columnData.append(rowValue)
        elif idx == 9:
            rowValue = firstRow[idx].getText()
        else:
            rowValue = firstRow[idx].getText()
            columnData.append(rowValue)
    columnData.insert(4, 'Country')
    columnData.append('Status')
    columnData.append('5K Split')
    columnData.append('10K Split')
    columnData.append('15K Split')
    columnData.append('20K Split')
    columnData.append('Half Split')
    columnData.append('25K Split')
    columnData.append('30K Split')
    columnData.append('35K Split')
    columnData.append('40K Split')
    columnData.append('Finish Split')
    return columnData

def cleanData(pageData):
    try:
        for idx, i in enumerate(pageData):
            row = pageData[idx]
            for idxx, j in enumerate(row):
                if idxx == 3:
                    a_string = row[idxx]
                    alphanumeric = ""
                    for character in a_string:
                        if character.isalnum():
                            alphanumeric += character
                    row[idxx] = alphanumeric
                if idxx == 5:
                    row[idxx] = row[idxx][4:]
                elif idxx == 6:
                    row[idxx] = row[idxx][13:]
                elif idxx == 7:
                    row[idxx] = row[idxx][8:]
                elif idxx == 8:
                    row[idxx] = row[idxx][4:]
                elif idxx == 9:
                    row[idxx] = row[idxx][6:]
            pageData[idx] = row
        return pageData
    except:
        print('pageData is empty')
        return

# Collecting all data
year = 2019
yearCounter = 0
page = 1
flag = 0
while year == 2019:
    print(year)
    print(yearCounter)
    while flag == 0 and page < 5:
        try:
            print(page)
            if page == 1:
                #time.sleep(1)
                res = requests.get('https://results.virginmoneylondonmarathon.com/' + str(year) + '/?page=' + str(page) + '&event=MAS&pid=search')
                soup = BeautifulSoup(res.text, 'html.parser')
                entries = soup.select('li.list-group-item.row')
                columnData = createColumnData(entries)
                pageData = createPageData(entries, year)
                print(pageData)
                pageData = cleanData(pageData)
                print(pageData)
                #data = pd.DataFrame(data = None, columns = columnData)
                for idx, i in enumerate(pageData):
                    rowData = pageData[idx]
                    a_series = pd.Series(rowData, index = data.columns)
                    data = data.append(a_series, ignore_index=True)
                page += 1
            else:
                #time.sleep(1)
                res = requests.get('https://results.virginmoneylondonmarathon.com/' + str(year) + '/?page=' + str(page) + '&event=MAS&pid=search')
                soup = BeautifulSoup(res.text, 'html.parser')
                entries = soup.select('li.list-group-item.row')
                pageData = createPageData(entries, year)
                pageData = cleanData(pageData)
                for idx, i in enumerate(pageData):
                    rowData = pageData[idx]
                    a_series = pd.Series(rowData, index = data.columns)
                    data = data.append(a_series, ignore_index=True)
                page += 1
        except:
            print("Oops! No data on this page...")
            flag = 1
    year -= 1
    yearCounter += 1
    page = 1
    flag = 0

#data.to_pickle('./data/results_test.pkl')
print(data.head())
print(datetime.datetime.now() - begin_time)
