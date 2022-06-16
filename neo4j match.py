import csv
import pandas as pd
from py2neo import Graph, Node, Relationship

graph = Graph("http://localhost:7474/browser/")
graph.delete_all()

#Create nodes to import csv data from each data source.
def addWikiCfp():
    with open('wikiCfpEvent.csv','r',encoding='utf-8') as f:
        reader = csv.reader(f)
        data = list(reader)
    for i in range(1,len(data)):
        wikiCfpNode = Node('wikiCfp',title = data[i][0],acronym = data[i][1],city = data[i][2],country = data[i][3],startDate = data[i][4], endDate = data[i][5],year = data[i][6],seriesTitle= data[i][8],url = data[i][9],wikicfpid = data[i][10])
        graph.create(wikiCfpNode)

def addWikiData():
    with open('wikidataEvent.csv','r',encoding='utf-8') as f:
        reader = csv.reader(f)
        data = list(reader)
    for i in range(1,len(data)):
        wikiDataNode = Node('wikiData',title = data[i][0],acronym = data[i][1],city = data[i][3],country = data[i][4],startDate = data[i][5], endDate = data[i][6],year = data[i][7],wikicfpid = data[i][8],dblpid = data[i][9],seriesTitle= data[i][10],url = data[i][11],describedAtUrl = data[i][12])
        graph.create(wikiDataNode)

def addConfRef():
    with open('confRefEvent.csv','r',encoding='utf-8') as f:
        reader = csv.reader(f)
        data = list(reader)
    for i in range(1,len(data)):
        confRefNode = Node('confRef',acronym = data[i][1],city = data[i][2],country = data[i][3],startDate = data[i][4], endDate = data[i][5],year = data[i][6],series = data[i][7],seriesTitle= data[i][8],url = data[i][9])
        graph.create(confRefNode)

def adddblp():
    with open('dblpEvent.csv','r',encoding='utf-8') as f:
        reader = csv.reader(f)
        data = list(reader)
    for i in range(1,len(data)):
        dblpNode = Node('dblp',title = data[i][0],acronym = data[i][1],city = data[i][2],country = data[i][3],startDate = data[i][4], endDate = data[i][5],year = data[i][6],eventid = data[i][7],series = data[i][8],url = data[i][9])
        graph.create(dblpNode)


adddblp()
addConfRef()
addWikiData()
addWikiCfp()

#Match two data with the same link
def matchSameLink():
    sameDblpId = '''Match(a:wikiData) Match(b:dblp)
                   WHERE a.dblpid = b.eventid
                   MERGE (a)-[:same]-(b)'''

    sameDblpLink = '''Match(a:wikiData) Match(b:dblp)
                   WHERE a.describedAtUrl = b.url
                   MERGE (a)-[:same]-(b)'''

    sameWikiCfpId = '''Match(a:wikiData) Match(b:wikiCfp)
                   WHERE a.wikicfpid = b.wikicfpid
                   MERGE (a)-[:same]-(b)'''

    graph.run(sameDblpId)
    graph.run(sameDblpLink)
    graph.run(sameWikiCfpId)

#Create relationship and match
def matchSameAcronymAndDate():
    #Build two lists of node classes, ensuring that each node class matches the other node classes at least once
    a = ['wikiData', 'wikiCfp', 'confRef', 'dblp']
    b = ['wikiData', 'wikiCfp', 'confRef', 'dblp']
    for i in range(0, len(a)):
        n = i + 1
        while n < len(b):
            sameAcronymAndDate = f'''Match(a:{a[i]}) Match(b:{b[n]}) 
                                 WHERE a.acronym = b.acronym AND NOT a.acronym = "" 
                                 AND a.startDate = b.startDate AND a.endDate = b.endDate 
                                 MERGE (a)-[:same]-(b) '''
            graph.run(sameAcronymAndDate)
            n = n + 1

def matchSameAcronymAndLocation():
    a = ['wikiData', 'wikiCfp', 'confRef', 'dblp']
    b = ['wikiData', 'wikiCfp', 'confRef', 'dblp']
    for i in range(0, len(a)):
        n = i + 1
        while n < len(b):
            sameAcronymAndLocation = f'''Match(a:{a[i]}) Match(b:{b[n]}) 
                                 WHERE a.acronym = b.acronym AND NOT a.acronym = "" 
                                 AND a.city = b.city AND a.country = b.country
                                 MERGE (a)-[:same]-(b) '''
            graph.run(sameAcronymAndLocation)
            n = n + 1

def matchSameSeriesidAndDate():
    sameSeriesidAndDate = '''Match(a:confRef) Match(b:dblp)
                       WHERE a.series = b.series AND NOT a.series = ""
                       And a.year = b.year And Not a.year = ""
                       MERGE (a)-[:same]-(b)'''
    graph.run(sameSeriesidAndDate)

def matchSameSeriesTitleAndDate():
    a = ['wikiData', 'wikiCfp', 'confRef']
    b = ['wikiData', 'wikiCfp', 'confRef']
    for i in range(0, len(a)):
        n = i + 1
        while n < len(b):
            sameSeriesTitleAndDate = f'''Match(a:{a[i]}) Match(b:{b[n]}) 
                                 WHERE a.seiresTitle = b.seriesTitle AND NOT a.seriesTitle = "" 
                                 AND a.year = b.year AND NOT a.year = ""
                                 MERGE (a)-[:same]-(b) '''
            graph.run(sameSeriesTitleAndDate)
            n = n + 1

def matchSameAcronym():
    a = ['wikiData', 'wikiCfp', 'confRef', 'dblp']
    b = ['wikiData', 'wikiCfp', 'confRef', 'dblp']
    for i in range(0, len(a)):
        n = i + 1
        while n < len(b):
            sameAcronymAndLocation = f'''Match(a:{a[i]}) Match(b:{b[n]}) 
                                 WHERE a.acronym = b.acronym AND NOT a.acronym = "" 
                                 MERGE (a)-[:sameAcronym]-(b) '''
            graph.run(sameAcronymAndLocation)
            n = n + 1

matchSameLink()
matchSameAcronymAndDate()
matchSameAcronymAndLocation()
matchSameSeriesidAndDate()
matchSameSeriesTitleAndDate()
matchSameAcronym()


print('finish')