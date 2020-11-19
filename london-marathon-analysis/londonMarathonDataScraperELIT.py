import requests
from bs4 import BeautifulSoup
import numpy as np
import re
import time
import datetime
import pickle

begin_time = datetime.datetime.now()

# Functions
def createPageData(entries, year):
    if len(entries) == 2:
        print('...no data in entries')
        return
    pageData = []
    for idx, i in enumerate(entries):
        idx +=1
        if idx == len(entries):
            print('...returning page data')
            return pageData
        if year == 2019:
            row = entries[idx].select('div.list-field')
            name = entries[idx].select('h4.list-field')[0].getText()
            link = entries[idx].select('a')[0]['href']
        elif year < 2019 and year > 2009:
            row = entries[idx].find_all('td')
            name = row[3].getText()
            link = row[3].select('a')[0]['href']
        link = 'https://results.virginmoneylondonmarathon.com/' + str(year) + '/' + str(link)
        splits = getSplits(link)
        entry = []
        for idx, j in enumerate(row):
            rowValue = row[idx].getText()
            entry.append(rowValue)
        entry.pop(3)
        entry.insert(3, name)
        entry = entry[:-1]
        entry = entry + splits
        if year < 2019 and year > 2009:
            entry.pop(4)
        pageData.append(entry)
    return pageData

def getSplits(link):
    resLink = requests.get(link)
    soupLink = BeautifulSoup(resLink.text, 'html.parser')
    splits = []
    try:
        status = soupLink.select('td.f-race_status')[0].getText()
    except:
        status = 'Finished'
    matched = re.match('Finished',status)
    if matched:
        try:
            club = soupLink.select('td.f-club')[0].getText()
            splits.append(club)
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
        except:
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
        splits.append('-')
    return splits

def createColumnData():
    columnData = []
    columnData.insert(0, 'Place (Overall)')
    columnData.insert(1, 'Place (Gender)')
    columnData.insert(2, 'Place (Category)')
    columnData.insert(3, 'Name')
    columnData.insert(4, 'Runner Number')
    columnData.insert(5, 'Category')
    columnData.insert(6, 'Half')
    columnData.insert(7, 'Finish')
    columnData.insert(8, 'Club')
    columnData.insert(9,'Status')
    columnData.insert(10,'5K Split')
    columnData.insert(11,'10K Split')
    columnData.insert(12,'15K Split')
    columnData.insert(13,'20K Split')
    columnData.insert(14,'Half Split')
    columnData.insert(15,'25K Split')
    columnData.insert(16,'30K Split')
    columnData.insert(17,'35K Split')
    columnData.insert(18,'40K Split')
    columnData.insert(19,'Finish Split')
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
while flag == 0 and year > 2012:
    print(year)
    while flag == 0:
        try:
            print(page)
            if page == 1:
                time.sleep(1)
                res = requests.get('https://results.virginmoneylondonmarathon.com/' + str(year) + '/?page=' + str(page) + '&event=ELIT&pid=search')
                soup = BeautifulSoup(res.text, 'html.parser')
                if year == 2019:
                    entries = soup.select('li.list-group-item.row')
                elif year < 2019 and year > 2009:
                    table = soup.find("table")
                    entries = table.findAll('tr')
                columnData = createColumnData()
                pageData = createPageData(entries, year)
                data = {}
                for var in columnData:
                	data[var] = []
                for idx, i in enumerate(pageData):
                    rowData = pageData[idx]
                    for rowIdx, rowValue in enumerate(rowData):
                    	data[columnData[rowIdx]].append(rowValue)
                page += 1
            else:
                time.sleep(1)
                res = requests.get('https://results.virginmoneylondonmarathon.com/' + str(year) + '/?page=' + str(page) + '&event=ELIT&pid=search')
                soup = BeautifulSoup(res.text, 'html.parser')
                if year == 2019:
                    entries = soup.select('li.list-group-item.row')
                elif year < 2019 and year > 2009:
                    table = soup.find("table")
                    entries = table.findAll('tr')
                pageData = createPageData(entries, year)
                for idx, i in enumerate(pageData):
                    rowData = pageData[idx]
                    for rowIdx, rowValue in enumerate(rowData):
                    	data[columnData[rowIdx]].append(rowValue)
                page += 1
        except:
            print("Oops! Something went wrong...")
            flag = 1
    year -= 1
    yearCounter += 1
    page = 1
    flag = 0
    with open('scrape_' + str(year+1) + '_ELIT.pkl', 'wb') as handle:
        pickle.dump(data, handle, protocol=pickle.HIGHEST_PROTOCOL)

print(datetime.datetime.now() - begin_time)