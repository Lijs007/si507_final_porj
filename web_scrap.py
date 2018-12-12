import requests
import json
from bs4 import BeautifulSoup
import sqlite3 as sqlite
# url = 'https://stats.nba.com/players/traditional/?sort=PTS&dir=-1'
# html = requests.get(url, headers={'User-Agent': 'SI_CLASS'}).text
name_lookup = {'TOR':1, 'DEN':2, 'LAC':3, 'MIL':4, 'OKC':5, 'PHI':6, 'GSW':7, 'DET':8, 'LAL':9, 'MEM':10\
, 'IND':11, 'BOS':12, 'POR':13, 'DAL':14, 'MIN':15, 'ORL':16, 'SAC':17, 'NOP':18, 'CHA':19, 'HOU':20\
, 'SAS':21, 'UTA':22, 'WAS':23, 'MIA':24, 'BKN':25, 'NYK':26, 'CLE':27, 'ATL':28, 'CHI':29, 'PHX':30}
fr = open('../player.html','r')
html = fr.read()
fr.close()
soup = BeautifulSoup(html, 'html.parser')
thead = soup.find('thead')
ths = thead.find_all('th')

headlist = []
for th in ths[1:30]:
	headlist.append(th.text)

conn = sqlite.connect('final.sqlite')
cur = conn.cursor()

statement = '''
    DROP TABLE IF EXISTS 'Players';
'''
cur.execute(statement)

statement = '''
    CREATE TABLE 'Players' (
        'Id' INTEGER PRIMARY KEY AUTOINCREMENT,
        '{}' TEXT NOT NULL,
        '{}' INTEGER NOT NULL
        ''' + ",'{}' DECIMAL" * 27 + ');'

cur.execute(statement.format(*headlist))
#print(statement.format(*headlist))
conn.commit()

tbody = soup.find('tbody')
trs = tbody.find_all('tr')

statement = 'INSERT INTO "Players" '
statement += 'VALUES (?' + ', ?'*29 + ')'

for tr in trs:
	value_list = (None,)
	tds = tr.find_all('td')
	for td in tds[1:30]:
		try:
			#print(td.find(a).text)
			txt = td.find(a).text
		except:
			#print(td.text)
			txt = td.text
		if len(txt) == 3:
			try:
				txt = name_lookup[txt]
			except:
				pass
		value_list += (txt,)
	#print(value_list)


	cur.execute(statement, value_list)

conn.commit()


fr = open('../team.html','r')
html = fr.read()
fr.close()
soup = BeautifulSoup(html, 'html.parser')
thead = soup.find('thead')
ths = thead.find_all('th')

headlist = []
for th in ths[1:28]:
	headlist.append(th.text)

conn = sqlite.connect('final.sqlite')
cur = conn.cursor()

statement = '''
    DROP TABLE IF EXISTS 'Teams';
'''
cur.execute(statement)

statement = '''
    CREATE TABLE 'Teams' (
        'Id' INTEGER PRIMARY KEY AUTOINCREMENT,
        '{}' TEXT NOT NULL
        ''' + ",'{}' DECIMAL" * 26 + ');'

cur.execute(statement.format(*headlist))
#print(statement.format(*headlist))
conn.commit()

tbody = soup.find('tbody')
trs = tbody.find_all('tr')

statement = 'INSERT INTO "Teams" '
statement += 'VALUES (?' + ', ?'*27 + ')'

for tr in trs:
	value_list = (None,)
	tds = tr.find_all('td')
	for td in tds[1:28]:
		try:
			#print(td.find(a).text)
			value_list += (td.find(a).text,)
		except:
			#print(td.text)
			value_list += (td.text,)
	#print(value_list)


	cur.execute(statement, value_list)

conn.commit()



conn.close()