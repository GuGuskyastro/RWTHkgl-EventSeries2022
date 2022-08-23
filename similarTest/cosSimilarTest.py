import math
import numpy as np
from py2neo import Node,Relationship,Graph
import csv
import pandas as pd
import re
from matplotlib import pyplot as plt


graph = Graph("http://localhost:7474/browser/")

def func(x):
    return [a for b in x for a in func(b)] if isinstance(x, list) else [x]

def cosSimilar(node1,node2):
    dataGroup = set(node1).union(set(node2))


    word_dict = dict()
    i = 0
    for word in dataGroup:
        word_dict[word] = i
        i += 1

    #print(word_dict)

    node1Code = [word_dict[word] for word in node1]

    node1Code = [0] * len(word_dict)
    for word in node1:
        node1Code[word_dict[word]]+=1
    #print(node1Code)

    node2Code = [word_dict[word] for word in node2]

    node2Code = [0] * len(word_dict)
    for word in node2:
        node2Code[word_dict[word]]+=1
    #print(node2Code)

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
    #print(result)
    return result


def compareNode(nodelist):
    cosResult = []
    for i in range (0,len(nodelist)):
        node1 = []
        str1 = nodelist['seriesTitle'][i]
        if str1 != 'none':
            if nodelist['label'][i] == 'dblp':
                node1 = dblpTitleExtract(str1)
            else: node1 = list(set(str1.split()).difference(set(unUsedWord)))


        node1.append(nodelist['acronym'][i])
        node1.append(nodelist['city'][i])
        node1.append(nodelist['country'][i])
        node1.append(nodelist['startDate'][i])
        node1.append(nodelist['endDate'][i])
        node1.append(nodelist['year'][i])

        node1 = list(set(node1))
        if 'none' in node1:
            node1.remove('none')


        n = i+1
        for n in range (n,len(nodelist)):
            node2 = []
            str2 = nodelist['seriesTitle'][n]
            if str2 != 'none' :
                if nodelist['label'][n] == 'dblp':
                    node2 = dblpTitleExtract(str2)
                else:node2 = list(set(str2.split()).difference(set(unUsedWord)))

            node2.append(nodelist['acronym'][n])
            node2.append(nodelist['city'][n])
            node2.append(nodelist['country'][n])
            node2.append(nodelist['startDate'][n])
            node2.append(nodelist['endDate'][n])
            node2.append(nodelist['year'][n])

            node2 = list(set(node2))
            if 'none' in node2:
                node2.remove('none')


            if nodelist['year'][i] == nodelist['year'][n]:
                cosResult.append(cosSimilar(node1,node2))
    return cosResult


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
              'Eleventh','Twelfth','Thirteenth','Fourteenth','Fifteenth','Sixteenth','Seventeenth','Eighteenth','Nineteenth','th']


df = pd.read_csv('AAAI.csv', encoding ='gbk')
df.fillna('none', inplace=True)
df1 = pd.read_csv('ACII.csv', encoding ='gbk')
df1.fillna('none', inplace=True)
df2 = pd.read_csv('ACISP.csv', encoding ='gbk')
df2.fillna('none', inplace=True)
df3 = pd.read_csv('AHS.csv', encoding ='gbk')
df3.fillna('none', inplace=True)


AAAI = compareNode(df)
ACII = compareNode(df1)
ACISP = compareNode(df2)
AHS = compareNode(df3)
AAAI.sort(key=float)
ACII.sort(key=float)
ACISP.sort(key=float)
AHS.sort(key=float)

resultAAAI = {}
for i in set(AHS):
    resultAAAI[i] = AHS.count(i)

AAAIInfo = []
for n in resultAAAI:
    AAAIInfos = {"cosSimilar": n, "numbers": resultAAAI[n]}
    AAAIInfo.append(AAAIInfos)
    AAAIInfo.sort(key=lambda s: s['cosSimilar'])


x = []
y = []
for info in AAAIInfo:
    x.append(info['cosSimilar'])
    y.append(info['numbers'])
print(x)
print(y)

plt.figure(figsize=(27, 12))
plt.stem(x, y)
plt.title("AHS")
plt.xlabel('cosSimilar')
plt.ylabel('numbers')
x_ticks = np.arange(0.4,1,0.01)
plt.xticks(x_ticks)
plt.xticks(rotation=-45)
plt.savefig('AHS.png')