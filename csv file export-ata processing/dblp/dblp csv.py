import csv
import sqlite3
import pandas as pd
import ParsingAndNormalization as p

#Set the path to the local EventCorpus-sqlite database
conn = sqlite3.connect("D:\database\EventCorpus.db")
cur = conn.cursor()
print("Database opened successfully")

#Import query content into csv file
cursor = conn.cursor()
cursor.execute("select title, acronym, city, country, startDate, endDate, year, eventId, series,url from event_dblp")
with open('dblpEvent.csv', 'w', encoding='utf-8', newline="") as f:
    writer = csv.writer(f)
    writer.writerow(['title', 'acronym','city', 'country', 'startDate', 'endDate', 'year', 'eventId','series','url'])
    writer.writerows(cursor)
    print("finish writing")

#Read the title, use the title parsing function to get new time data, and add it to the csv file.
with open('dblpEvent.csv','r',encoding='utf-8') as f:
    reader = csv.reader(f)
    title = [row[0] for row in reader]

with open('dblpEvent.csv','r',encoding='utf-8')as f:
    reader = csv.reader(f)
    startDate = [row[4] for row in reader]

with open('dblpEvent.csv','r',encoding='utf-8')as f:
    reader = csv.reader(f)
    endDate = [row[5] for row in reader]



for i in range(1,len(title)):
    finalDate = p.dateParse(title[i])
    if startDate[i] == "":
        startDate[i] = finalDate['finalStartDate']
    if endDate[i] == "":
        endDate[i] = finalDate['finalEndDate']

for n in range(1,len(title)):
    finalDate2 = p.oneDayEventdateParse(title[n])
    if startDate[n] == "":
        startDate[n] = finalDate2['finalStartDate']
    if endDate[n] == "":
        endDate[n] = finalDate2['finalEndDate']


del startDate[0]
del endDate[0]

df = pd.read_csv('dblpEvent.csv',header=0)
df.drop('startDate',axis=1,inplace=True)
df.insert(4,'startDate',startDate)
df.drop('endDate',axis=1,inplace=True)
df.insert(5,'endDate',endDate)
df['startDate'] = pd.to_datetime(df['startDate'],errors = 'coerce')
df['endDate'] = pd.to_datetime(df['endDate'],errors = 'coerce')
df.to_csv('dblpEvent.csv',encoding='utf-8',index=False)

p.delWorkShop('dblpEvent.csv')
p.yearNormalization('dblpEvent.csv')
p.FilterWithCountry('dblpEvent.csv')


