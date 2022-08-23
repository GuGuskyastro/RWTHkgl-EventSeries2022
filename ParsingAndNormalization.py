import re
import pandas as pd
import numpy as np

#This file contains some functions that may be used when manipulating data


#This function is used to calculate the difference between the months of a date and to make a histogram.
def monthDifferenceCalculation(startDate, endDate):
    flag = True
    if startDate > endDate:
        startDate, endDate = endDate, startDate
        flag = False
    year_diff = endDate.year - startDate.year
    end_month = year_diff * 12 + endDate.month
    difference = end_month - startDate.month
    if flag is True:
        return str(difference) + ' Month'
    else: return str(-difference) + ' Month'



#This date parser function is used to handle the large number of headers in dblp that cover time information,Regular expressions can continue to improve
def dateParse(text):
    y = None
    startMonth = None
    endMonth = None
    startDay = None
    endDay = None
    finalStartDate = None
    finalEndDate = None

    #Extract the four digit number in the title, which is the year(Consider adding limits of 19 and 20)
    year_pattern = re.compile(r'\d{4}')
    year = re.search(year_pattern, text)
    if year is not None:
        y = year.group()

    # Digitize the date
    monthNormal = {
        'January': '1',
        'February': '2',
        'March': '3',
        'April': '4',
        'May': '5',
        'June': '6',
        'July': '7',
        'August': '8',
        'September': '9',
        'October': '10',
        'November': '11',
        'December': '12',
    }

    #Extract literal month and numeric date
    month_pattern = re.compile('January|February|March|April|May|June|July|August|September|October|November|December', re.I)
    month = re.findall(month_pattern,text)

    #The duration of the meeting is within 1 month
    if len(month) == 1:
        startMonth = month[0]
        endMonth = month[0]
        day_pattern = re.compile('(\d{2}-+\d{2})|(\d{1}-+\d{2})|(\d{1}-+\d{1})')
        day = re.search(day_pattern,text)
        if day is not None:
            d = day.group()
            d_pattern = re.compile('\d+')
            startdayAndendDay = re.findall(d_pattern, d)
            startDay = startdayAndendDay[0]
            endDay = startdayAndendDay[1]

    #The duration of the meeting is more than 1 month
    if len(month) == 2:
        startMonth = month[0]
        endMonth = month[1]
        day_pattern = re.compile('\d{2} |\d{1} ')
        day = re.findall(day_pattern, text)
        if len(day) == 2:
            startDay = day[0]
            endDay = day[1]

    #Convert month to number
    if startMonth is not None and endMonth is not None:
        for n in monthNormal:
            startMonth = startMonth.replace(n, monthNormal[n])
            endMonth = endMonth.replace(n, monthNormal[n])

    #Temporarily empty for unparseable dates
    if y is not None and startMonth is not None and startDay is not None:
        finalStartDate = y + '-' + startMonth + '-' + startDay
    else: finalStartDate = ""

    if y is not None and endMonth is not None and endDay is not None:
        finalEndDate = y + '-' + endMonth + '-' + endDay
    else:finalEndDate = ""

    result = {}
    result['title'] = text
    result['finalStartDate'] = finalStartDate
    result['finalEndDate'] = finalEndDate
    return result

#Use pandas functions to unify date formats
def dateNormalization(file_name):
    df = pd.read_csv(file_name)
    df['startDate'] = pd.to_datetime(df['startDate'], errors='coerce')
    df['endDate'] = pd.to_datetime(df['endDate'], errors='coerce')
    df.to_csv(file_name, encoding='utf-8', index=False)

#This function is used to remove eg 01-01 dates in confRef due to parsing errors
def deleteWrongStartAndEndDate(filename,n,m,modifiedfilename):

    wrongStartDate = filename.startDate.str.endswith('01-01')
    wrongEndDate = filename.endDate.str.endswith('01-01')

    a = filename['startDate']
    b = filename['endDate']

    for i in range(0, len(a)):
        if wrongStartDate[i] is True:
            a[i] = np.nan
        if wrongEndDate[i] is True:
            b[i] = np.nan

    filename.drop('startDate', axis=1, inplace=True)
    filename.drop('endDate', axis=1, inplace=True)
    filename.insert(n, 'startDate', a)
    filename.insert(m, 'endDate', b)
    filename.to_csv(modifiedfilename, encoding='utf-8', index=False)

#Unify the year of the data source as an integer(with wikiCfpId).
def yearandIdNormalization(filename):
    df = pd.read_csv(filename)
    df['year'] = df['year'].astype('Int64')
    df['wikiCfpid'] = df['wikiCfpid'].astype('Int64')
    df.to_csv(filename, encoding='utf-8', index=False)
    print('Year revision completed')

def yearNormalization(filename):
    df = pd.read_csv(filename)
    df['year'] = df['year'].astype('Int64')
    df.to_csv(filename, encoding='utf-8', index=False)
    print('Year revision completed')

#del workshop node from all source
def delWorkShop(filename):
    df = pd.read_csv(filename)
    df.fillna('', inplace=True)
    df.drop(df[df['title'].str.contains('workshop')].index, inplace=True)
    df.drop(df[df['title'].str.contains('Workshop')].index, inplace=True)
    df.to_csv(filename,encoding='utf-8', index=False)
    print('del workshop completed')


#Filter nodes that meet the common cases countries, based on 0.2% of the total number
def FilterWithCountry(filename):
    df = pd.read_csv(filename)
    # >0.2%
    countryList = ['','United States of America','Germany','France','Italy',"People's Republic of China",'Canada','Spain','South Korea',
                   'Japan','United Kingdom','Australia','Portugal','Austria','India','Greece','Poland','Brazil','Switzerland','Russia',
                   'Kingdom of the Netherlands','Sweden','Czech Republic','Singapore','South Korea','Belgium','Finland','United Arab Emirates',
                   'Mexico','Hungary','Norway','Turkey','New Zealand','Cyprus','Denmark','Malaysia','Romania','Thailand','Indonesia','Egypt',
                   'Vietnam','Bulgaria','Israel','Morocco','Cuba','Slovenia','Chile','Ireland','Estonia','South Africa','Switzerland','Philippines',
                   'Croatia','Tunisia','Iran']

    df.fillna('', inplace=True)

    df.replace('Taiwan',"People's Republic of China",inplace=True)
    df.replace('China',"People's Republic of China",inplace=True)
    df.replace('Netherlands','Kingdom of the Netherlands',inplace=True)
    df.replace('The Netherlands','Kingdom of the Netherlands',inplace=True)
    df.replace('USA','United States of America',inplace=True)
    df.replace('UK','United Kingdom',inplace=True)

    for i in df['country']:
        if i not in countryList:
            df.drop(df[df['country'] == i].index,inplace=True)

    df.to_csv(filename,encoding='utf-8', index=False)
    print('Country Filter success')