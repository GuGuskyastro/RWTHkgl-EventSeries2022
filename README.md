# RWTH kgl-EventSeries2022
Welcome to the hands-on project of the Knowledge Graph Working Group at RWTH Aachen University!<br>


This project is part of the knowledge graph lab under RWTH Lehrstuhl für Informatik 5. For more detailed code information and usage instructions, please refer to the following documents.<br>


+ [Project Introduction](#project-introduction)

+ [Background data introduction](#background-data-introduction)
 
+ [Knowledge graph construction](#knowledge-graph-construction)

+ [Inquiry and display](#inquiry-and-display)

+ [References and Acknowledgments](#references-and-acknowledgments)


## Project Introduction

The content of this practice is a knowledge graph project centered on the field of scientific conferences, which is used to aggregate attribute descriptions of scientific conferences from different databases, and finally return an integrated node for each conference.<br>

Users can query the abbreviation of the desired meeting through a simple interactive page, and return the data table of the entire meeting series after analysis by the background program.

+ ### Example of query result：
![image](https://github.com/GuGuskyastro/RWTHkgl-EventSeries2022/blob/main/image/Query%20example.png?raw=true)

+ ### Current operating environment of the project：

### python : 

```
 python 3.10
```

### Graph database for building knowledge graphs :

```
neo4j 4.46
```
Neo4j is a graph database management system developed by Neo4j, Inc.It is also the core of this project for building a knowledge graph.<br>

For the use and specific instructions of neo4j, please refer to the [official documentation](https://neo4j.com/docs/)

### Libraries for data processing and analysis：
```
matplotlib 3.5.2 

numpy 1.22.3

pandas 1.4.2
```
Pandas and numpy are good friends when using python for data processing and numerical analysis, which help us filter and process the raw content of each data source.
Matplotlib is a python and NumPy-based plotting library that helps us visualize analytical data.

### Rest of the package that will be used：
```
py2neo 2021.2.3

streamlit 1.12.0
```
py2neo is the corresponding driver of neo4j in python, which is convenient for developers to use python to process data in neo4j.<br>

Streamlit turns data scripts into shareable web apps in minutes only in pure Python. No front-end experience is required to develop an interactive interface that helps us present query results to users.

***Precautions：To clone the project and run it, make sure to keep the extension package as consistent as possible***

+ ### Files that need to be run to start the project

```
 neo4jMatch.py
 
 cosSimilar.py
```
These two files perform the task of building the knowledge graph and adding relationships. The addition of about 150,000 nodes takes less than 10 minutes, the construction of the basic relationship takes about 1 minute, and the relationship process using cosine similarity takes about 2-3 hours. So please be patient while running the second file, the completed year-relation-addition will also be shown in your IDE.

```
 web.py
```
When starting the steamlit-based interactive page, you need to open the project directory in the command line terminal and use the 'streamlit run' command to run the file, the browser will automatically jump to the usage page.

+ ### The main file directory of the project
The main file directory of the project is shown in the figure, and some image files are not displayed.

```
kgl-commencases
├─ csvFileExport-ataProcessing               # Raw data collection for each data source
│  ├─confRef                                 # Data source name
│  │      confRef csv.py                     # Raw data extraction and preprocessing
│  │      confRefEvent.csv                   # Raw data table
│  │      matplotlib-confRef.py              # Plot file for analysis data
│  │      
│  ├─dblp
│  │      dblp csv.py
│  │      dblpEvent.csv
│  │      matplotlib-dblp.py
│  │      
│  ├─wikiCfp
│  │      matplotlib-wikiCfp.py
│  │      wikiCfp csv.py
│  │      wikiCfpEvent.csv
│  │      
│  └─WikiData
│          matplotlib-wikidata.py
│          wikidata csv.py
│          wikidataEvent.csv
│          
├─ DataProcessingAndMatching                # Knowledge graph construction
│  ├─ neo4jMatch.py                         # Import data table content into Neo4j , establishment of basic relationships
│  ├─ cosSimilar.py                         # Cosine Similarity Algorithm Supplement to creat relationships
│  ├─ confRefEvent.csv
│  ├─ dblpEvent.csv
│  ├─ wikiCfpEvent.csv
│  └─ wikidataEvent.csv
│      
├─ queryAndWebpage                             
│  ├─ Query.py                              # Background query algorithm
│  └─ web.py                                # Interactive page display of query results
│          
├─ similarTest
│  └─ cosSimilarTest.py                     # Plot file for analyzing similarity algorithm thresholds
|
├─ ParsingAndNormalization.py               # Method function based on data processing
└─ requirements.txt

```

## Background data introduction
The data structure of this project is mainly saved in csv files. On the one hand, it is easy to process in python. On the other hand, the cypher command of Neo4j also supports the direct writing of csv files. <br>

The construction of knowledge graphs often requires operations such as crawling to obtain the required data. This project uses the sqlite database from [ConferenceCorpus](https://github.com/WolfgangFahl/ConferenceCorpus). If you need to see the original database, please consult the documentation of the ConferenceCorpus library and download, the extracted csv file is also already stored in the directory. The original data extraction file of this project needs to be connected to the local sqlite library(For example confRef csv.py). So if you need to modify or consult raw data, please modify your own local link to databse.<br>

At present, this project contains the data tables of the four data sources shown in the catalog. At the same time, the scope of the data used is defined according to the goal of commen cases, we have screened the country and the duration of the conference to a certain extent. A list of definitions can be found in the tool function file,Related analysis graphs are also stored in the directory


## Knowledge graph construction

The knowledge graph itself is actually a graph of relationships between nodes, which can be described by triples, namely `entity  A - relationship - entity B  `. Import the collected and processed csv file data into the neo4j library through file `neo4j match.py` and generate entities and relationships. Picture shows an example corresponding to a meeting event.

![image](https://github.com/GuGuskyastro/RWTHkgl-EventSeries2022/blob/main/image/T4~9T0YB%5DVCKZ5O8KAKTI3E.png)

In order to make the knowledge graph as complete as possible, we design a matching algorithm based on cosine similarity, which is used to calculate the similarity of the attributes and contents of two nodes and create relationships for eligible nodes.<br>

The similarity itself is a relative concept, so we need to set a threshold to define "similarity". By testing the similarity algorithm of some manually-corrected conference events, we found that the similarity value of the same event is often greater than 0.7, while the similarity of different events is basically between 0.3 and 0.6. It can be considered that 0.7 is an optional threshold. <br>

The following figure is an analysis chart for AHS events, the rest of the examples can be found in the similarTest directory
![image](https://github.com/GuGuskyastro/RWTHkgl-EventSeries2022/blob/main/similarTest/AHS.png)
![image](https://github.com/GuGuskyastro/RWTHkgl-EventSeries2022/blob/main/similarTest/AHS-False.png)

## Inquiry and display

We designed a query method based on meeting abbreviations, that is, the user enters the meeting abbreviation they want to query on the front end, and then the background queries all the nodes in the knowledge graph that meet the conditions and all nodes that have a relationship path based on the abbreviation, and analyzes all nodes. Returns an "integration node" that aggregates key information. <br>

However, due to the possibility of a meeting with a duplicate name, it is necessary to judge whether the abbreviation has a duplicate name event every time. The picture shows a typical example of a conference with the same name. For meetings with the same name, each "part graph" will return an integration node.<br>

![image](https://github.com/GuGuskyastro/RWTHkgl-EventSeries2022/blob/main/image/%60C%602%60Y%40F%60%7DN%60%7BVTTXQ%5BF~%7BC.png)

In addition, in order to ensure the correctness of the integration nodes as much as possible, we will still check the correctness of the queried relationship graph. When the graph is found to have incorrectly matched nodes, the relationship nodes constructed based on cosine similarity are ignored when integrating entities. With the help of the above two detection functions, we can build the query structure as shown in the figure.<br>
![image](https://github.com/GuGuskyastro/RWTHkgl-EventSeries2022/blob/main/image/Query%20stru.png)

After the query for the input series is completed, the list content is added to the html table, and finally returned to the user and displayed on the interactive page,  an example of the query result shown at the [beginning of the document](#example-of-query-result) is obtained.


## References and Acknowledgments
Before this project was launched, I didn't know much about knowledge graphs. When searching for information in csdn, I accidentally read a knowledge graph project based on the medical field. [This project](https://github.com/baiyang2464/chatbot-base-on-Knowledge-Graph) has given me a lot of help and inspiration in understanding the structure of knowledge graph.<br>

The completion of the project is also inseparable from the help of two team supervisors in the research group. Heartfelt thanks to [Wolfgang Fahl](https://github.com/WolfgangFahl) and [Tim Holzheim](https://github.com/tholzheim)!
