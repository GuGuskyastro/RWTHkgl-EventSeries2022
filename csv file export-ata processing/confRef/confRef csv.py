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
cursor.execute("select lookupAcronym, city, country, year, startDate, endDate,seriesId,seriesTitle, url,title from event_confref")
with open('confRefEvent.csv', 'w', encoding='utf-8', newline="") as f:
    writer = csv.writer(f)
    writer.writerow(['acronym', 'city', 'country', 'year','startDate', 'endDate', 'series','seriesTitle','url','title'])
    writer.writerows(cursor)
    print("finish writing")

#remove the exact same line
data = pd.read_csv('confRefEvent.csv')
duplicated_data = data.drop_duplicates(keep='first', inplace=False)
duplicated_data.to_csv('confRefEvent.csv',encoding='utf-8',index=False)
print('remove exact duplicate lines')

#Format dates by using pandas
df = pd.read_csv('confRefEvent.csv')
df['startDate'] = pd.to_datetime(df['startDate'],errors = 'coerce')
df['endDate'] = pd.to_datetime(df['endDate'],errors = 'coerce')
df.to_csv('confRefEvent.csv',encoding='utf-8',index=False)
print('Uniform date format')

p.yearNormalization('confRefEvent.csv')
p.delWorkShop('confRefEvent.csv')

p.FilterWithCountry('confRefEvent.csv')


conn.close()