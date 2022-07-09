import pandas as pd
import os
import json 
from scrap import *
from dataBaseConnection import *

os.system("clear")
os.system("echo [*] Automation Started\n")

# Counter for Scrapping Data
count = 1

# Loading country code and Asin parameters from gven CSV file
data = pd.read_csv ('./Amazon Scraping - Sheet1.csv')   
df = pd.DataFrame(data, columns= ['Asin','country'])

# Itterating in Data Frame of given CSV file and Scrapping the required Data
for index, row in df.iloc[:40].iterrows():
    scrap(str(row['Asin']),row['country'])
    print("[ "+str(count)+" ] Done")    # Maintaing the count for Scrapped Data
    count = count+1

os.system("clear")

# Storing Data in MYSQL DataBase
dumpInDatabase(jsonData)
os.system("echo [*] Updateded Database with Product Information")

# Saving Required Data in fliesystem
with open('data.json', 'w', encoding='utf-8') as f:
    json.dump(jsonData, f, ensure_ascii=False, indent=4)
    os.system("echo [*] File created with Product Information")

    
os.system("echo [*] Automation Ended\n")
