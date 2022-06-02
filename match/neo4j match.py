import csv
import pandas as pd
from py2neo import Graph, Node, Relationship

graph = Graph("http://localhost:7474/browser/")

#Create nodes to import csv data from each data source.
def addWikiCfp():

    with open('wikiCfpEvent.csv','r',encoding='utf-8') as f:
        reader = csv.reader(f)
        data = list(reader)
    for i in range(1,len(data)):
        wikiCfpNode = Node('wikiCfp',title = data[i][0],acronym = data[i][1],startDate = data[i][4], endDate = data[i][5])
        graph.create(wikiCfpNode)

def addWikiData():
    with open('wikidataEvent.csv','r',encoding='utf-8') as f:
        reader = csv.reader(f)
        data = list(reader)
    for i in range(1,len(data)):
        wikiDataNode = Node('wikiData',title = data[i][0],acronym = data[i][1],startDate = data[i][5], endDate = data[i][6])
        graph.create(wikiDataNode)

def addConfRef():
    with open('confRefEvent.csv','r',encoding='utf-8') as f:
        reader = csv.reader(f)
        data = list(reader)
    for i in range(1,len(data)):
        confRefNode = Node('confRef',acronym = data[i][1],startDate = data[i][4], endDate = data[i][5])
        graph.create(confRefNode)

addWikiCfp()
addWikiData()
addConfRef()

#Create relationship and match
def matchSameAcronymAndDate():
    wikicfpAnddata = ''' Match(a:wikiCfp) Match(b:wikiData) 
                         WHERE a.acronym = b.acronym AND NOT a.acronym = "" 
                         AND a.startDate = b.startDate AND a.endDate = b.endDate 
                         MERGE (a)-[:same]-(b) '''

    wikicfpAndconfref = '''Match(a:wikiCfp) Match(b:confRef) 
                           WHERE a.acronym = b.acronym AND NOT a.acronym = "" 
                           AND a.startDate = b.startDate AND a.endDate = b.endDate 
                           MERGE (a)-[:same]-(b) '''

    wikidataAndconfref = '''Match(a:wikiData) Match(b:confRef) 
                            WHERE a.acronym = b.acronym AND NOT a.acronym = "" 
                            AND a.startDate = b.startDate AND a.endDate = b.endDate 
                            MERGE (a)-[:same]-(b) '''

    graph.run(wikicfpAnddata)
    graph.run(wikicfpAndconfref)
    graph.run(wikidataAndconfref)


matchSameAcronymAndDate()

print('finish')