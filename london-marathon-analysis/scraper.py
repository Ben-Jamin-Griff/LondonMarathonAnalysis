import requests
from bs4 import BeautifulSoup

res = requests.get('https://results.virginmoneylondonmarathon.com/2019/?page=1&event=MAS&pid=search')
soup = BeautifulSoup(res.text, 'html.parser')
entries = soup.select('li.list-group-item.row')

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

pageData = createPageData(entries)

print(pageData[1])

#entries = soup.select('li.list-group-item.row')
#entry1 = entries[0].select('div.list-field')
#entry2 = entries[1].select('div.list-field')
#entry3 = entries[2].select('div.list-field')

#print(f'length of entries {len(entries)}')
#print(f'length of divs in entry 1 {len(entry1)}')
#print(f'length of divs in entry 2 {len(entry2)}')
#print(f'length of divs in entry 2 {len(entry3)}')