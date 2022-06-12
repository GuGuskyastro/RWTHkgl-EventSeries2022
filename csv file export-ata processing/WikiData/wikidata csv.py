import csv
import sqlite3
import pandas as pd


#Set the path to the local EventCorpus-sqlite database
conn = sqlite3.connect("D:\database\EventCorpus.db")
cur = conn.cursor()
print("Database opened successfully")

#Import query content into csv file
cursor = conn.cursor()
cursor.execute("select title, acronym, ordinal, city, country, startDate, endDate, year, wikiCfpid, dblpid, url,describedAtUrl from event_wikidata")
with open('wikidataEvent.csv', 'w', encoding='utf-8', newline="") as f:
    writer = csv.writer(f)
    writer.writerow(['title', 'acronym', 'ordinal', 'city', 'country', 'startDate', 'endDate', 'year', 'wikiCfpid', 'dblpid','url','describedAtUrl'])
    writer.writerows(cursor)
    print("finish writing")

#remove the exact same line
#TODO For partially duplicated lines, keep the most complete line?
data = pd.read_csv('wikidataEvent.csv')
duplicated_data = data.drop_duplicates(subset=['acronym'],keep='first', inplace=False)
duplicated_data.to_csv('wikidataEvent.csv',encoding='utf-8',index=False)
print('remove exact duplicate lines')

#Format dates by using pandas
df = pd.read_csv('wikidataEvent.csv')
df['startDate'] = pd.to_datetime(df['startDate'],errors = 'coerce')
df['endDate'] = pd.to_datetime(df['endDate'],errors = 'coerce')
df.to_csv('wikidataEvent.csv',encoding='utf-8',index=False)
print('Uniform date format')



conn.close()

