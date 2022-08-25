import math
from py2neo import Graph
import re

graph = Graph("http://localhost:7474/browser/")


delRelation = "MATCH ()-[r]-() DELETE r"
graph.run(delRelation)

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
                                 AND a.startDate = b.startDate AND a.endDate = b.endDate AND NOT a.startDate = ""
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
                                 AND a.city = b.city AND a.country = b.country AND NOT a.city = "" AND NOT a.country = ""
                                 MERGE (a)-[:same]-(b) '''
            graph.run(sameAcronymAndLocation)
            n = n + 1


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


matchSameLink()
matchSameAcronymAndDate()
matchSameAcronymAndLocation()
matchSameSeriesTitleAndDate()




def func(x):
    return [a for b in x for a in func(b)] if isinstance(x, list) else [x]

def cosSimilar(node1,node2):
    dataGroup = set(node1).union(set(node2))


    word_dict = dict()
    i = 0
    for word in dataGroup:
        word_dict[word] = i
        i += 1

    node1Code = [word_dict[word] for word in node1]

    node1Code = [0] * len(word_dict)
    for word in node1:
        node1Code[word_dict[word]]+=1

    node2Code = [word_dict[word] for word in node2]

    node2Code = [0] * len(word_dict)
    for word in node2:
        node2Code[word_dict[word]]+=1


    # cos-similar
    sum = 0
    sq1 = 0
    sq2 = 0
    for i in range(len(node1Code)):
        sum += node1Code[i] * node2Code[i]
        sq1 += pow(node1Code[i], 2)
        sq2 += pow(node2Code[i], 2)

    try:
        result = round(float(sum) / (math.sqrt(sq1) * math.sqrt(sq2)), 2)
    except ZeroDivisionError:
        result = 0.0

    return result


def compareNode(nodelist):
    for i in range (0,len(nodelist)):
        n = i + 1
        label1 = nodelist[i]['n']['label']
        node1 = []
        if label1 == 'dblp':
            str1 = nodelist[i]['n']['title']
        else:
            str1 = nodelist[i]['n']['seriesTitle']
        if str1 is not None:
            if nodelist[i]['n']['label'] == 'dblp':
                node1 = dblpTitleExtract(str1)
            else:
                node1 = list(set(str1.split()).difference(set(unUsedWord)))

        node1.append(nodelist[i]['n']['acronym'])
        node1.append(nodelist[i]['n']['city'])
        node1.append(nodelist[i]['n']['country'])
        node1.append(nodelist[i]['n']['startDate'])
        node1.append(nodelist[i]['n']['endDate'])
        node1.append(nodelist[i]['n']['year'])

        node1 = list(set(node1))
        if '' in node1:
            node1.remove('')

        for n in range (n,len(nodelist)):
            label2 = nodelist[n]['n']['label']
            if label1 == label2:
                continue

            node2 = []
            if label2 == 'dblp':
                str2 = nodelist[n]['n']['title']
            else:
                str2 = nodelist[n]['n']['seriesTitle']

            if str2 is not None:
                if nodelist[n]['n']['label'] == 'dblp':
                    node2 = dblpTitleExtract(str2)
                else:
                    node2 = list(set(str2.split()).difference(set(unUsedWord)))


            node2.append(nodelist[n]['n']['acronym'])
            node2.append(nodelist[n]['n']['city'])
            node2.append(nodelist[n]['n']['country'])
            node2.append(nodelist[n]['n']['startDate'])
            node2.append(nodelist[n]['n']['endDate'])
            node2.append(nodelist[n]['n']['year'])

            node2 = list(set(node2))
            if '' in node2:
                node2.remove('')


            if cosSimilar(node1,node2) > 0.71:
                a = "{(a)-[r:same]-(b)}"
                highSimilar = f'''Match(a),(b)
                                where a.ID = {nodelist[i]['n']['ID']} and b.ID = {nodelist[n]['n']['ID']} 
                                And not exists {a}
                                MERGE (a)-[:highSimilar]-(b) '''
                graph.run(highSimilar)

def dblpTitleExtract(text):
    #Extract the content before the first comma
    pattern = re.compile('^[^,]*(?=,)')
    result = re.findall(pattern,text)
    separate = re.compile('[a-zA-Z]+')
    if result != []:
        result = list(set(re.findall(separate,result[0])))
        result = list(set(result).difference(set(unUsedWord)))

    return result



##Collection of useless words
unUsedWord = ['','the','a','an','and','at','of', 'in', 'on', 'to','by' 'above', 'over','below', 'under', 'beside','behind','between',
              'during','through','from','since','with','within','Twenty','Thirty','Forty','Fifty','Sixty','Seventy',
              'First','Second','Third','Fourth','Fifth','Sixth','Seventh','Eighth','Ninth','Tenth',
              'Eleventh','Twelfth','Thirteenth','Fourteenth','Fifteenth','Sixteenth','Seventeenth','Eighteenth','Nineteenth','th'
             'International' 'Conference']

yearlist = list(range(1950, 2023))

for i in yearlist:
    test = f'''match (n)
            where n.year = '{i}'
            return n '''
    nodelist = list(graph.run(test).data())
    nodelist = func(nodelist)
    compareNode(nodelist)
    print(str(i)+ ' is Finish')

