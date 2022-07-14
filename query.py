from tabulate import tabulate
from py2neo import Node,Relationship,Graph
from py2neo import NodeMatcher,RelationshipMatcher


graph = Graph("http://localhost:7474/browser/")

#This function is used to remove redundant [] in the list
def func(x):
    return [a for b in x for a in func(b)] if isinstance(x, list) else [x]


def queryWithAcronym(acronym):
    query = acronym
    #Add the ID and label of the node itself to the properties of the node to facilitate subsequent queries
    a = f'''match (n)
        set n.ID = id(n)
        set n.label = labels(n)[0]'''

    graph.run(a)

    node_matcher = NodeMatcher(graph)

    node = list(node_matcher.match().where(acronym = query))

    ID = []
    IDwithRelation = []


    for i in range(0,len(node)):
        ID.append(node[i]['ID'])

    for i in range(0,len(ID)):
        b = f'''match(n)-[r:same]-(m) 
                WHERE n.ID ={ID[i]}  
                RETURN m.ID'''
        IDwithRelation.append(graph.run(b).data())

    IDwithRelation = func(IDwithRelation)

    for i in range(0, len(IDwithRelation)):
        ID.append(IDwithRelation[i]['m.ID'])
    ID = list(set(ID))

    finalnode = []
    for i in range(0,len(ID)):
        node = list(node_matcher.match().where(ID = ID[i]))
        finalnode.append(node)

    finalnode = func(finalnode)
    return finalnode


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

    return realResult

input = input('Acronym is? :')
a = queryWithAcronym(input)
answer = [majorityVote(a)]
print(tabulate(answer, headers=["Acronym", "City", "Country", "StartDate",'EndDate','Year','Dblp url','WikiCfp url','WikiData url','ConfRef url']))