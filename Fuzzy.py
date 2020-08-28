import pandas as pd
from fuzzywuzzy import fuzz
from fuzzywuzzy import process
import codecs

import csv

#read APIsName.csv
#return a list of API names
csvfile2 = open('APIsName.csv','rb')
reader2 = csv.reader(codecs.iterdecode(csvfile2, 'utf-8'))
names = [row[1][:-4] for row in reader2][1:]


#read googleplay.csv
#return a list of google API names
csvfile = open('googleplay.csv','rb')
reader = csv.reader(codecs.iterdecode(csvfile, 'utf-8'))
column_google = [row[4] for row in reader][1:]


#read appstore.csv
#return a list of apple API names
csvfile = open('appstore.csv','rb')
reader = csv.reader(codecs.iterdecode(csvfile, 'utf-8'))
column_apple = [row[3] for row in reader][1:]



result_google = []
name_google =[]
score_google =[]

result_apple = []
name_apple =[]
score_apple =[]

for name in names:
    result_google.append(process.extractOne(name, column_google,scorer=fuzz.token_sort_ratio))
    
    result_apple.append(process.extractOne(name, column_apple,scorer=fuzz.token_sort_ratio))


for tuples in result_google:
    name_google.append(tuples[0])
    score_google.append(tuples[1])

for tuples in result_apple:
    name_apple.append(tuples[0])
    score_apple.append(tuples[1])


data = pd.read_csv('APIsName.csv')
print (data)


data['NAME_GOOGLE'] = name_google
data['SCORE_GOOGLE'] = score_google

data['NAME_APPLE'] = name_apple
data['SCORE_APPLE'] = score_apple

data.to_csv('output.csv',mode = 'a',index=False)

