import requests
import json
import random
from bs4 import BeautifulSoup
import time
import csv
import pandas as pd 

headers={
    'user-agent': "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.198 Safari/537.36"
}

url="https://www.advratings.com/top-asset-management-firms?fbclid=IwAR1mTeKQcjOUmFvaBvrHKKB-xqUCcrWxac861K2r_p75ngunUvQkqV0Z7Vw"
source = requests.get(url, headers = headers)
source.encoding = 'utf-8'
text = source.text
soup = BeautifulSoup(text,'lxml')
fund = soup.find_all('td')[5:]
rank = []
company = []
country = []
AUM = []
BalanceSheet = []
for i in range(len(fund)):
    item = fund[i].text
    if i%5==0:
        rank = rank + [item]
    elif i%5==1:
        company = company + [item]
    elif i%5==2:
        country = country + [item]
    elif i%5==3:
        AUM = AUM + [item]
    elif i%5==4:
        BalanceSheet = BalanceSheet + [item]
df = pd.DataFrame({
    'Rank':rank,
    'Company':company,
    'Country':country,
    'Total AUM, US$b':AUM,
    'Balance sheet':BalanceSheet
})

df.to_csv('global_fund_corp_rank.csv',index = None)