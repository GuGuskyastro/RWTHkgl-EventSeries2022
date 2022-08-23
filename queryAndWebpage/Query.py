import re
import pandas as pd
from py2neo import Graph
from py2neo import NodeMatcher

graph = Graph("http://localhost:7474/browser/")
yearlist = list(range(1950, 2023))

#This function is used to remove all redundant [] in the list
def func(x):
    return [a for b in x for a in func(b)] if isinstance(x, list) else [x]
#This function is used to remove one redundant [] in the list
def funcOne(x):
    a = []
    for i in x:
        if type(i) is list:
            for j in i:
                a.append(j)
    return a


def queryWithAcronym(acronym):
    node_matcher = NodeMatcher(graph)
    result = []
    empty = ""
    #Do deep path searches for events with the same acronym, return the IDs of total nodes
    id = f'''match(n)-[*..6]-(m) 
            where n.acronym ='{acronym}' 
            return DISTINCT n.ID,m.ID'''

    #If the search result is empty, return an empty list directly
    if graph.run(id).data() == []:
        return empty

    ID = pd.DataFrame(graph.run(id).data())
    IDList1 = list(set(ID['m.ID']))
    IDList2 = list(set(ID['n.ID']))

    #At this point IDlist contains all matching node IDs
    IDList = list(set(IDList1+IDList2))
    print(IDList)

    #Confirm that the abbreviation corresponds to a unique event by comparing a deep search of a node
    if checkSameAcronym(IDList) is True:
        finalnode = []

        if checkkorrectMatch(IDList) is True:

            for i in range(0, len(IDList)):
                node = list(node_matcher.match().where(ID=IDList[i]))
                finalnode.append(node)
            finalnode = func(finalnode)
            result.append(majorityVote(finalnode))
            return result

        #If a matching problem is detected, only the nodes of the same relationship are matched
        else:
            newid = f'''match(n)-[r:same*]-(m) 
                       where n.acronym ='{acronym}' 
                       return DISTINCT n.ID,m.ID'''
            newID = pd.DataFrame(graph.run(newid).data())
            newIDList1 = list(set(newID['m.ID']))
            newIDList2 = list(set(newID['n.ID']))
            newIDList = list(set(newIDList1 + newIDList2))

            for i in range(0, len(newIDList)):
                node = list(node_matcher.match().where(ID=newIDList[i]))
                finalnode.append(node)
            finalnode = func(finalnode)
            result.append(majorityVote(finalnode))
            return result

    else:
        n = 0
        print(IDList[n])
        while len(IDList) > 0:
            deepSearch = f'''match(n)-[*..6]-(m) 
                where n.ID = {IDList[n]} 
                return DISTINCT n.ID,m.ID'''

            deepSearchID = pd.DataFrame(graph.run(deepSearch).data())
            deepSearchIDList1 = list(set(deepSearchID['m.ID']))
            deepSearchIDList2 = list(set(deepSearchID['n.ID']))
            deepSearchIDList = list(set(deepSearchIDList1 + deepSearchIDList2))

            finalnode = []

            if checkkorrectMatch(deepSearchIDList) is True:
                for i in range(0, len(deepSearchIDList)):
                    node = list(node_matcher.match().where(ID=deepSearchIDList[i]))
                    finalnode.append(node)


                finalnode = func(finalnode)
                result.append(majorityVote(finalnode))
                IDList = list(set(IDList).difference(set(deepSearchIDList)))


            else: #注意独立节点事件
                a = 0
                checkAcronym = f'''match(n) where n.ID = {deepSearchIDList[a]} return n.acronym '''

                while graph.run(checkAcronym).data()[0]['n.acronym'] != acronym:
                    a += 1
                    checkAcronym = f'''match(n) where n.ID = {deepSearchIDList[a]} return n.acronym '''


                newid = f'''match(n)-[r:same*]-(m) 
                           where n.ID ={deepSearchIDList[a]}
                           return DISTINCT n.ID,m.ID'''

                newID = pd.DataFrame(graph.run(newid).data())
                newIDList1 = list(set(newID['m.ID']))
                newIDList2 = list(set(newID['n.ID']))
                newIDList = list(set(newIDList1 + newIDList2))

                for i in range(0, len(newIDList)):
                    node = list(node_matcher.match().where(ID=newIDList[i]))
                    finalnode.append(node)
                finalnode = func(finalnode)
                result.append(majorityVote(finalnode))

                IDList = list(set(IDList).difference(set(deepSearchIDList)))


        return result


#If the deep search result of a node does not match the total node list, can be considered that this acronym represents different events
def checkSameAcronym(idList):
    deepSearch = f'''match(n)-[*..6]-(m) 
    where n.ID = {idList[0]} 
    return DISTINCT n.ID,m.ID'''

    deepSearchID = pd.DataFrame(graph.run(deepSearch).data())
    deepSearchIDList1 = list(set(deepSearchID['m.ID']))
    deepSearchIDList2 = list(set(deepSearchID['n.ID']))
    deepSearchIDList = list(set(deepSearchIDList1 + deepSearchIDList2))
    print(deepSearchIDList)

    if set(idList) == set(deepSearchIDList):
        print('1')
        return True
    if set(idList) != set(deepSearchIDList):
        print('2')
        return False

#There is still the possibility of incorrect matching of the "highSimilar" relationship.
# Check whether the nodes of the same data source but different series are matched to determine whether they are correctly matched

def checkkorrectMatch(idList):

    list = f'''UNWIND {idList} as x
            MATCH(n)
            where n.ID = x 
            return n.label,n.series,n.url'''

    df = pd.DataFrame(graph.run(list).data())

    for i in range(0, len(df) - 1):
        a = df['n.label'][i]
        b = df['n.series'][i]
        c = df['n.url'][i]
        if a == 'dblp':
            for n in (i + 1, len(df) - 1):
                if df['n.label'][n] == 'dblp' and df['n.series'][n] != b:
                    print('error')
                    return False
        if a == 'confRef':
            for n in (i + 1, len(df) - 1):
                if df['n.label'][n] == 'confRef' and df['n.series'][n] != b:
                    print('error')
                    return False
        if a == 'wikiData':
            for n in (i + 1, len(df) - 1):
                if df['n.label'][n] == 'wikiData' and df['n.url'][n] != c:
                    print('error')
                    return False
    print('ok')
    return True




def majorityVote(list):

    acronym = []
    city = []
    country = []
    startDate = []
    endDate = []
    year = []

    sign = [acronym, city, country, startDate, endDate, year]

    for a in range(0, len(list)):
        acronym.append(list[a]['acronym'])
        city.append(list[a]['city'])
        country.append(list[a]['country'])
        startDate.append(list[a]['startDate'])
        endDate.append(list[a]['endDate'])
        year.append(list[a]['year'])

    realResult = []
    for k in range(0, len(sign)):
        result = {}

        for i in set(sign[k]):
            result[i] = sign[k].count(i)

        resultInfo = []
        for n in result:
            resultInfos = {"result": n, "numbers": result[n]}
            resultInfo.append(resultInfos)
            resultInfo.sort(key=lambda s: s['numbers'])

        for i in range(0, len(resultInfo)):
            if resultInfo[i]['result'] == "":
                resultInfo[i]['numbers'] = 0
        number = 0
        majority = ''

        for i in range(0, len(resultInfo)):
            if resultInfo[i]['numbers'] > number:
                majority = resultInfo[i]['result']
        realResult.append(majority)

    realResult.append('')
    realResult.append('')
    realResult.append('')
    realResult.append('')
    for i in range(0,len(list)):
        if list[i]['label'] == 'dblp':
            realResult[6] = (list[i]['url'])

        if list[i]['label'] == 'wikiCfp':
            realResult[7] = (list[i]['url'])

        if list[i]['label'] == 'wikiData':
            realResult[8] = (list[i]['url'])

        if list[i]['label'] == 'confRef':
            realResult[9] = (list[i]['url'])
    print(realResult)
    return realResult


def acronymParser(text,year):
    acrony_pattern = re.compile('[a-zA-Z]+')
    result = re.findall(acrony_pattern, text)
    acronym = str(result[0]) + ' ' + str(year)
    return acronym


def outPut(input):
    answer = []
    for i in range(0,len(yearlist)):
        Acronym = acronymParser(input,yearlist[i])
        answer.append(queryWithAcronym(Acronym))

    return answer

