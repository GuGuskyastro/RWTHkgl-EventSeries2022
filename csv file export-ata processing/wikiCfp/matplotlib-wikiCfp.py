import csv
from matplotlib import pyplot as plt
from datetime import datetime
import ParsingAndNormalization as p

def creatCountryDiagramm():
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
        countryInfo.sort(key=lambda s:s['numbers'])
    print(countryInfo)

    #Create a graph for capturing data
    x=[]
    y=[]
    for Info in countryInfo:
        x.append(Info["countryName"])
        y.append(Info["numbers"])

    plt.figure(figsize=(20, 50))
    plt.barh(x,y)
    plt.title("The number of occurrences in each country by WikiData")
    plt.xlabel('Numbers')
    plt.ylabel('countryName')
    plt.savefig('wikiCfpCountry.png')

def creatMonthDurationDiagramm():
    with open('wikiCfpEvent.csv', 'r', encoding='utf-8') as f:
        reader = csv.reader(f)
        startDate = [row[4] for row in reader]
    with open('wikiCfpEvent.csv', 'r', encoding='utf-8') as f:
        reader = csv.reader(f)
        endDate = [row[5] for row in reader]

    monthDuration = []
    durationCount = {}

    for i in range(1,len(startDate)):
        if startDate[i] != "" and endDate[i] != "":
            realStartDate = datetime.strptime(startDate[i],"%Y-%m-%d")
            realEndDate = datetime.strptime(endDate[i],"%Y-%m-%d")
            duration = p.monthDifferenceCalculation(realStartDate,realEndDate)
        else: duration = 'No Date Infomation'
        monthDuration.append(duration)

    for i in set(monthDuration):
        durationCount[i] = monthDuration.count(i)

    durationResult = []
    for n in durationCount:
        durationresult = {"Duration": n, "numbers": durationCount[n]}
        durationResult.append(durationresult)
        durationResult.sort(key=lambda s:s['numbers'])

    print(durationResult)

    x = []
    y = []
    for n in durationResult:
        x.append(n["Duration"])
        y.append(n["numbers"])

    plt.figure(figsize=(20, 30))
    plt.barh(x,y)
    plt.title("Duration of meeting in wikidata")
    plt.xlabel('numbers')
    plt.ylabel('Duration')
    plt.savefig('wikiCfpDuration.png')


creatCountryDiagramm()
creatMonthDurationDiagramm()