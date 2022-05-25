import csv
from matplotlib import pyplot as plt

#print country label
with open('wikiCfpEvent.csv', 'r', encoding='utf-8') as f:
    reader = csv.reader(f)
    country = [row[3] for row in reader]
#print(country)

#Count the number of occurrences of each country
result = {}
for i in set(country):
    result[i] = country.count(i)
#print(result)

#Create a new storage list for statistical results
countryInfo = []
for n in result:
    countryInfos = {"countryName": n, "numbers": result[n]}
    countryInfo.append(countryInfos)
    countryInfo.sort(key=lambda s: s['numbers'])
print(countryInfo)

#Create a graph for capturing data
x=[]
y=[]
for Info in countryInfo:
    x.append(Info["countryName"])
    y.append(Info["numbers"])

plt.figure(figsize=(20, 50))
plt.barh(x,y)
plt.title("The number of occurrences in each country by wikiCfp")
plt.xlabel('Numbers')
plt.ylabel('countryName')
plt.savefig('wikiCfp.png')