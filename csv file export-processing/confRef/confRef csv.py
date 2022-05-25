import csv
import sqlite3
import pandas as pd

#Set the path to the local EventCorpus-sqlite database
conn = sqlite3.connect("D:\database\EventCorpus.db")
cur = conn.cursor()
print("Database opened successfully")

#Import query content into csv file
cursor = conn.cursor()
cursor.execute("select acronym, lookupAcronym, city, country, startDate, endDate, year, url from event_confref")
with open('confRefEvent.csv', 'w', encoding='utf-8', newline="") as f:
    writer = csv.writer(f)
    writer.writerow(['seriesAcronym', 'acronym', 'city', 'country', 'startDate', 'endDate', 'year', 'url'])
    writer.writerows(cursor)
    print("finish writing")

#remove the exact same line
#TODO For partially duplicated lines, keep the most complete line?
data = pd.read_csv('confRefEvent.csv')
duplicated_data = data.drop_duplicates(keep='first', inplace=False)
duplicated_data.to_csv('confRefEvent.csv',encoding='utf-8',index=False)
print('remove exact duplicate lines')

conn.close()