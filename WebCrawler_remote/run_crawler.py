import requests
from bs4 import BeautifulSoup
import numpy as np
import pandas as pd
import datetime
import time
from fake_useragent import UserAgent
import pandas as pd
import random
import datetime
import logging
import datetime
import smtplib
import mimetypes
from email.mime.multipart import MIMEMultipart
from email import encoders
from email.message import Message
from email.mime.audio import MIMEAudio
from email.mime.base import MIMEBase
from email.mime.image import MIMEImage
from email.mime.text import MIMEText
import os
path_now = os.getcwd()

today = datetime.date.today().strftime('%Y%m%d')
FORMAT = '%(asctime)s %(levelname)s: %(message)s'
errorfile = path_now+'/Error Record/'+today+'ErrorReport.log'

data_path = path_now+'/標案資料最新紀錄.csv'

try:
    latest = pd.read_csv(data_path)
    try:
        ldate = latest['公告日'][0]
        today = datetime.date.today().strftime('%Y%m%d')
        ltoday = str(int(today[0:4])-1911)+'/'+today[4:6]+'/'+today[6:8]

        start_date = ldate
        end_date = ltoday
        key_words = ['資安','資訊安全','資通安全','個人資料','個資','隱私','防禦','攻防','諮詢','顧問','研究',
                   '雲端','科技','資訊','人工智慧','AI','風險','5G','區塊鏈','IoT','物聯網','數位','行銷','數據'
                    ,'分析','去識別','驗證','資料']

        final_df = pd.DataFrame([])

        for key_word in key_words:
            print("---------------開始"+key_word+"標案爬蟲---------------")
            param = {"method": "search",
            'searchMethod': 'true',
            'tenderUpdate':'' ,
            'searchTarget':'' ,
            'orgName': '',
            'orgId':'' ,
            'hid_1': '1',
            'tenderName': key_word,
            'tenderId': '',
            'tenderType': 'tenderDeclaration',
            'tenderWay': '1,2,3,4,5,6,7,10,12',
            'tenderDateRadio': 'on',
            'tenderStartDateStr': start_date,
            'tenderEndDateStr': end_date,
            'tenderStartDate': start_date,
            'tenderEndDate': end_date,
            'isSpdt': 'N',
            'proctrgCate': '',
            'btnQuery': '查詢',
            'hadUpdated': ''}

            head = 'https://web.pcc.gov.tw/tps/pss/tender.do?searchMode=common&searchType=basic&method=search&isSpdt=&pageIndex='

            headers = {
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
            "Accept-Encoding": "gzip, deflate, br",
            "Accept-Language": "zh-TW,zh;q=0.9,en-US;q=0.8,en;q=0.7",
            "Cache-Control": "max-age=0",
            "Connection": "keep-alive",
            "Host": "web.pcc.gov.tw",
            "Referer": "https://web.pcc.gov.tw/tps/pss/tender.do?searchMode=common&searchType=basic",
            "Cookie": "NSC_xfc_qfstjtufodf=ffffffff09081f7945525d5f4f58455e445a4a423660; cookiesession1=5135051C4FVUFANQLOEMHML6X8QC5058; JSESSIONID=0000u6QnCl9DTQaxTTMG_SRcSEB:14nuu9h0k; NSC_xfc_jqw6_qfstjtufodf=00000000234c1f310b110d790a110e1122081e113660",
            "sec-ch-ua-mobile": "?0",
            "Sec-Fetch-Dest": "document",
            "Sec-Fetch-Mode": "navigate",
            "Sec-Fetch-Site": "same-origin",
            "Sec-Fetch-User": "?1",
            "Upgrade-Insecure-Requests": "1",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.106 Safari/537.36"
            }

            my_df = pd.DataFrame([])

            url = head + str(1)
            response = requests.post(url,data = param,headers = headers)
            soup = BeautifulSoup(response.text,features="html.parser")
            test = soup.find_all('a',style="color: #444444;")
            if test==[]:
                pages = 1
            else:
                pages = int(test[-1]['href'][-1])

            for i in range(0,pages):
                time.sleep(15)
                url = head + str(i+1)
                response = requests.post(url,data = param,headers = headers)
                soup = BeautifulSoup(response.text,features="html.parser") 
                data = soup.find_all('a')

                href = []
                title = []

                for i in range(0,len(data)):
                    try:
                        title = title + [data[i]['title']]
                        href = href + [data[i]['href']]
                    except:
                        break

                df = pd.DataFrame({
                    'href':href,
                    'title':title
                })

                ind = []
                for i in range(0,len(df)):
                    if key_word not in df['title'][i]:
                        ind = ind + [i]
                df = df.drop(index = ind)
                my_df = pd.concat([my_df,df])
            my_df = my_df.reset_index()
            amount = len(my_df)
            print("總共{}筆資料,預計約{}分鐘後完成".format(amount,amount*0.25))

            cases = pd.DataFrame([])

            try:
                if my_df['title'][0] == '前往 技師與工程技術顧問公司管理資訊系統(另開視窗)':
                    my_df = my_df.drop(index = 0).reset_index()
                    
                headers = {
                "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
                "Accept-Encoding": "gzip, deflate, br",
                "Accept-Language": "zh-TW,zh;q=0.9,en-US;q=0.8,en;q=0.7",
                "Cache-Control": "max-age=0",
                "Connection": "keep-alive",
                "Host": "web.pcc.gov.tw",
                "Referer": "https://web.pcc.gov.tw/tps/pss/tender.do?searchMode=common&searchType=basic",
                "Cookie": "NSC_xfc_qfstjtufodf=ffffffff09081f7945525d5f4f58455e445a4a423660; cookiesession1=5135051C4FVUFANQLOEMHML6X8QC5058; JSESSIONID=0000u6QnCl9DTQaxTTMG_SRcSEB:14nuu9h0k; NSC_xfc_jqw6_qfstjtufodf=00000000234c1f310b110d790a110e1122081e113660",
                "sec-ch-ua-mobile": "?0",
                "Sec-Fetch-Dest": "document",
                "Sec-Fetch-Mode": "navigate",
                "Sec-Fetch-Site": "same-origin",
                "Sec-Fetch-User": "?1",
                "Upgrade-Insecure-Requests": "1",
                }

                for i in range(0,len(my_df)):    
                    time.sleep(15)
                    key = my_df['href'][i].split('F&primaryKey=')[1]
                    web = 'https://web.pcc.gov.tw/tps/tpam/main/tps/tpam/tpam_tender_detail.do?searchMode=common&scope=F&primaryKey='+str(key)
                    link = requests.get(web,headers = headers)
                    soup = BeautifulSoup(link.text,features="html.parser") 

                    blue = soup.find_all('th',bgcolor="#DAEBED", width="25%")
                    yellow = soup.find_all('th',bgcolor="#FFFF99", width="25%")
                    green = soup.find_all('th',bgcolor="#CAEDAF", width="25%")
                    orange = soup.find_all('th',bgcolor="#FFDD83", width="25%")
                    alist = blue+yellow+green+orange
                    mylist = []
                    for i in range(0,len(alist)):
                        txt = alist[i].text.replace('\r','').replace('\t','').replace('\n','')
                        mylist+=[txt]

                    blist = soup.find_all('td', bgcolor="#EFF1F1",width="75%")[0:len(mylist)]
                    content = []
                    for i in range(0,len(blist)):
                        txt = blist[i].text.replace('\r','').replace('\t','').replace('\n','')
                        content+=[txt]    
                    mylist = mylist + ['連結']
                    content = content + [web]

                    one_case = pd.DataFrame({
                        'content':content
                    },index = mylist)

                    cases = pd.concat([cases,one_case],axis = 1)

                cases = cases.transpose()

                df = pd.DataFrame({
                    'Status':'',
                    '發起人':'EY_Crawler',
                    '電子領標':'TBD',
                    '電子領標日':'',
                    '爬蟲執行時間':datetime.date.today().strftime('%Y/%m/%d'),
                    '公告日':list(cases['公告日']),
                    '截止投標':list(cases['截止投標']),
                    '開標時間':list(cases['開標時間']),
                    '金額':list(cases['預算金額']),
                    'WD':'',
                    '專案結束日':'',
                    '招標方式':list(cases['招標方式']),
                    '決標方式':list(cases['決標方式']),
                    '機關名稱':list(cases['機關名稱']),
                    '單位名稱':list(cases['單位名稱']),
                    '標案名稱':list(cases['標案名稱']),
                    '聯絡人':list(cases['聯絡人']),
                    '聯絡電話':list(cases['聯絡電話']),
                    '電子郵件信箱':list(cases['電子郵件信箱']),
                    '標的分類':list(cases['標的分類']),
                    '連結':list(cases['連結']),
                    '關鍵字':key_word
                })
            except:
                df = pd.DataFrame([])

            final_df = pd.concat([final_df,df])

        try:
            final_df = final_df.drop_duplicates(subset = '標案名稱').reset_index().drop(columns = 'index')
            d = final_df['公告日'].copy()
            for i in range(len(d)):
                try:
                    year = str(int(d[i].split('/')[0])+1911)
                    d[i]=year+d[i].split('/')[1]+d[i].split('/')[2]
                except:
                    d[i]=end_date
            d=pd.to_datetime(d,format='%Y%m%d')
            final_df['date'] = d
            final_df = final_df.sort_values(by = 'date',ascending = False)
            final_df = final_df.drop(columns = 'date')
        except:
            final_df = final_df
        
        sd = start_date.split('/')[0]+start_date.split('/')[1]+start_date.split('/')[2]
        ed = end_date.split('/')[0]+end_date.split('/')[1]+end_date.split('/')[2]
        final_df.to_csv(path_now+'/Weekly Bid Data/標案資料'+sd+'-'+ed+'.csv',index = None,encoding = 'utf-8_sig')

        new_data = pd.concat([final_df,latest]).drop_duplicates(subset = '標案名稱')
        new_data = new_data.reset_index().drop(columns = 'index')

        new_data.to_csv(data_path,index = None,encoding = 'utf-8_sig')
        scenario = 1
    except:
        logging.basicConfig(handlers=[logging.FileHandler(errorfile, 'a', 'utf-8')],level=logging.ERROR, format=FORMAT)
        logging.error('Catch an exception.', exc_info=True)
        scenario = 2
except:
    try:
        print('目前尚無標案紀錄！')
        YN = input('是否進行資料抓取? 請輸入"Y"或"N"')
        while YN not in ['Y','N']:
            YN = input('請輸入正確的字符("Y"或"N")')
        if YN=='Y':
            final_df = pd.DataFrame([])
            start_date = input('請輸入起始時間，格式為:民國年/月/日，例如:109/01/05 ')
            end_date = input('請輸入結束時間，格式為:民國年/月/日，例如:110/12/31 ')
            key_words = ['資安','資訊安全','資通安全','個人資料','個資','隱私','防禦','攻防','諮詢','顧問','研究',
                    '雲端','科技','資訊','人工智慧','AI','風險','5G','區塊鏈','IoT','物聯網','數位','行銷','數據'
                    ,'分析','去識別','驗證','資料']

            for key_word in key_words:
                print("---------------開始"+key_word+"標案爬蟲---------------")
                param = {"method": "search",
                'searchMethod': 'true',
                'tenderUpdate':'' ,
                'searchTarget':'' ,
                'orgName': '',
                'orgId':'' ,
                'hid_1': '1',
                'tenderName': key_word,
                'tenderId': '',
                'tenderType': 'tenderDeclaration',
                'tenderWay': '1,2,3,4,5,6,7,10,12',
                'tenderDateRadio': 'on',
                'tenderStartDateStr': start_date,
                'tenderEndDateStr': end_date,
                'tenderStartDate': start_date,
                'tenderEndDate': end_date,
                'isSpdt': 'N',
                'proctrgCate': '',
                'btnQuery': '查詢',
                'hadUpdated': ''}

                head = 'https://web.pcc.gov.tw/tps/pss/tender.do?searchMode=common&searchType=basic&method=search&isSpdt=&pageIndex='

                headers = {
                "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
                "Accept-Encoding": "gzip, deflate, br",
                "Accept-Language": "zh-TW,zh;q=0.9,en-US;q=0.8,en;q=0.7",
                "Cache-Control": "max-age=0",
                "Connection": "keep-alive",
                "Host": "web.pcc.gov.tw",
                "Referer": "https://web.pcc.gov.tw/tps/pss/tender.do?searchMode=common&searchType=basic",
                "Cookie": "NSC_xfc_qfstjtufodf=ffffffff09081f7945525d5f4f58455e445a4a423660; cookiesession1=5135051C4FVUFANQLOEMHML6X8QC5058; JSESSIONID=0000u6QnCl9DTQaxTTMG_SRcSEB:14nuu9h0k; NSC_xfc_jqw6_qfstjtufodf=00000000234c1f310b110d790a110e1122081e113660",
                "sec-ch-ua-mobile": "?0",
                "Sec-Fetch-Dest": "document",
                "Sec-Fetch-Mode": "navigate",
                "Sec-Fetch-Site": "same-origin",
                "Sec-Fetch-User": "?1",
                "Upgrade-Insecure-Requests": "1",
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.106 Safari/537.36"
                }

                my_df = pd.DataFrame([])

                url = head + str(1)
                response = requests.post(url,data = param,headers = headers)
                soup = BeautifulSoup(response.text,features="html.parser")
                test = soup.find_all('a',style="color: #444444;")
                if test==[]:
                    pages = 1
                else:
                    pages = int(test[-1]['href'][-1])

                for i in range(0,pages):
                    time.sleep(15)
                    url = head + str(i+1)
                    response = requests.post(url,data = param,headers = headers)
                    soup = BeautifulSoup(response.text,features="html.parser") 
                    data = soup.find_all('a')

                    href = []
                    title = []

                    for i in range(0,len(data)):
                        try:
                            title = title + [data[i]['title']]
                            href = href + [data[i]['href']]
                        except:
                            break

                    df = pd.DataFrame({
                        'href':href,
                        'title':title
                    })

                    ind = []
                    for i in range(0,len(df)):
                        if key_word not in df['title'][i]:
                            ind = ind + [i]
                    df = df.drop(index = ind)
                    my_df = pd.concat([my_df,df])
                my_df = my_df.reset_index()
                
                amount = len(my_df)
                print("總共{}筆資料,預計約{}分鐘後完成".format(amount,amount*0.25))

                cases = pd.DataFrame([])

                try:
                    if my_df['title'][0] == '前往 技師與工程技術顧問公司管理資訊系統(另開視窗)':
                        my_df = my_df.drop(index = 0).reset_index()
                    headers = {
                    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
                    "Accept-Encoding": "gzip, deflate, br",
                    "Accept-Language": "zh-TW,zh;q=0.9,en-US;q=0.8,en;q=0.7",
                    "Cache-Control": "max-age=0",
                    "Connection": "keep-alive",
                    "Host": "web.pcc.gov.tw",
                    "Referer": "https://web.pcc.gov.tw/tps/pss/tender.do?searchMode=common&searchType=basic",
                    "Cookie": "NSC_xfc_qfstjtufodf=ffffffff09081f7945525d5f4f58455e445a4a423660; cookiesession1=5135051C4FVUFANQLOEMHML6X8QC5058; JSESSIONID=0000u6QnCl9DTQaxTTMG_SRcSEB:14nuu9h0k; NSC_xfc_jqw6_qfstjtufodf=00000000234c1f310b110d790a110e1122081e113660",
                    "sec-ch-ua-mobile": "?0",
                    "Sec-Fetch-Dest": "document",
                    "Sec-Fetch-Mode": "navigate",
                    "Sec-Fetch-Site": "same-origin",
                    "Sec-Fetch-User": "?1",
                    "Upgrade-Insecure-Requests": "1",
                    }

                    for i in range(0,len(my_df)):    
                        time.sleep(15)
                        key = my_df['href'][i].split('F&primaryKey=')[1]
                        web = 'https://web.pcc.gov.tw/tps/tpam/main/tps/tpam/tpam_tender_detail.do?searchMode=common&scope=F&primaryKey='+str(key)
                        link = requests.get(web,headers = headers)
                        soup = BeautifulSoup(link.text,features="html.parser") 

                        blue = soup.find_all('th',bgcolor="#DAEBED", width="25%")
                        yellow = soup.find_all('th',bgcolor="#FFFF99", width="25%")
                        green = soup.find_all('th',bgcolor="#CAEDAF", width="25%")
                        orange = soup.find_all('th',bgcolor="#FFDD83", width="25%")
                        alist = blue+yellow+green+orange
                        mylist = []
                        for i in range(0,len(alist)):
                            txt = alist[i].text.replace('\r','').replace('\t','').replace('\n','')
                            mylist+=[txt]

                        blist = soup.find_all('td', bgcolor="#EFF1F1",width="75%")[0:len(mylist)]
                        content = []
                        for i in range(0,len(blist)):
                            txt = blist[i].text.replace('\r','').replace('\t','').replace('\n','')
                            content+=[txt]    
                        mylist = mylist + ['連結']
                        content = content + [web]

                        one_case = pd.DataFrame({
                            'content':content
                        },index = mylist)

                        cases = pd.concat([cases,one_case],axis = 1)

                    cases = cases.transpose()

                    df = pd.DataFrame({
                        'Status':'',
                        '發起人':'EY_Crawler',
                        '電子領標':'TBD',
                        '電子領標日':'',
                        '爬蟲執行時間':datetime.date.today().strftime('%Y/%m/%d'),
                        '公告日':list(cases['公告日']),
                        '截止投標':list(cases['截止投標']),
                        '開標時間':list(cases['開標時間']),
                        '金額':list(cases['預算金額']),
                        'WD':'',
                        '專案結束日':'',
                        '招標方式':list(cases['招標方式']),
                        '決標方式':list(cases['決標方式']),
                        '機關名稱':list(cases['機關名稱']),
                        '單位名稱':list(cases['單位名稱']),
                        '標案名稱':list(cases['標案名稱']),
                        '聯絡人':list(cases['聯絡人']),
                        '聯絡電話':list(cases['聯絡電話']),
                        '電子郵件信箱':list(cases['電子郵件信箱']),
                        '標的分類':list(cases['標的分類']),
                        '連結':list(cases['連結']),
                        '關鍵字':key_word
                    })
                except:
                    df = pd.DataFrame([])

                final_df = pd.concat([final_df,df])

            final_df = final_df.drop_duplicates(subset = '標案名稱').reset_index().drop(columns = 'index')
            d = final_df['公告日'].copy()
            for i in range(len(d)):
                try:
                    year = str(int(d[i].split('/')[0])+1911)
                    d[i]=year+d[i].split('/')[1]+d[i].split('/')[2]
                except:
                    d[i]=end_date
            d=pd.to_datetime(d,format='%Y%m%d')
            final_df['date'] = d
            final_df = final_df.sort_values(by = 'date',ascending = False)
            final_df = final_df.drop(columns = 'date')
            sd = start_date.split('/')[0]+start_date.split('/')[1]+start_date.split('/')[2]
            ed = end_date.split('/')[0]+end_date.split('/')[1]+end_date.split('/')[2]
            
            final_df.to_csv(data_path,index = None,encoding = 'utf-8_sig')
            final_df.to_csv(path_now+'/Weekly Bid Data/標案資料'+sd+'-'+ed+'.csv',index = None,encoding = 'utf-8_sig')
            scenario = 3
        elif YN=='N':
            print('結束程式')
            scenario = 4
    except:
        logging.basicConfig(handlers=[logging.FileHandler(errorfile, 'a', 'utf-8')],level=logging.ERROR, format=FORMAT)
        logging.error('Catch an exception.', exc_info=True)   
        scenario = 5     

#寄信
content = MIMEMultipart()  #建立MIMEMultipart物件

if scenario in [1,3]:
    num = []
    for i in key_words:
        a = len(final_df[final_df['關鍵字']==i])
        num = num+[a]
    dit = dict()
    for i,j in zip(key_words,num):
        dit[i] = j
    text = "今日標案資料更新已完成，附檔為今日進度。\n\n各關鍵字標案數量:"
    for i in key_words:
        text = text+'\n'+i+' : '+str(dit[i])

if scenario==1:
    fileToSend = path_now+'/Weekly Bid Data/標案資料'+sd+'-'+ed+'.csv'
    content["subject"] = today+"標案資料更新"  
    part = MIMEText(text, _charset="UTF-8")
    receivers = ['sean.he.huang@tw.ey.com,Christina.Tseng@tw.ey.com,Thomas.Wan@tw.ey.com,Chia.Ming.Chou@tw.ey.com,Wei.JW.Bai@tw.ey.com,Chienkuang.CK.Chao@tw.ey.com,Leo.LH.Weng@tw.ey.com,Hedi.CH.Ho.Chiang@tw.ey.com,Eureka.Fu@tw.ey.com,Tim.PT.Chou@tw.ey.com,Charlie.CH.Hsu@tw.ey.com']
    bcc = ["show19970117@gmail.com,EY.TW.Digitals@gmail.com"]
    content['BCC'] = ','.join(bcc)
elif scenario==2:
    fileToSend =  errorfile  
    content["subject"] = today+"標案資料更新錯誤匯報"  
    part = MIMEText("今日標案資料更新發生異常！請參閱附檔的錯誤報告。", _charset="UTF-8")
    receivers = ['show19970117@gmail.com,sean.he.huang@tw.ey.com,EY.TW.Digitals@gmail.com']
elif scenario==3:
    fileToSend = path_now+'/Weekly Bid Data/標案資料'+sd+'-'+ed+'.csv'
    content["subject"] = today+"標案資料更新"  
    part = MIMEText(text, _charset="UTF-8")
    receivers = ['sean.he.huang@tw.ey.com,Christina.Tseng@tw.ey.com,Thomas.Wan@tw.ey.com,Chia.Ming.Chou@tw.ey.com,Wei.JW.Bai@tw.ey.com,Chienkuang.CK.Chao@tw.ey.com,Leo.LH.Weng@tw.ey.com,Hedi.CH.Ho.Chiang@tw.ey.com,Eureka.Fu@tw.ey.com,Tim.PT.Chou@tw.ey.com,Charlie.CH.Hsu@tw.ey.com']
    bcc = ["show19970117@gmail.com,EY.TW.Digitals@gmail.com"]
    content['BCC'] = ','.join(bcc)
elif scenario==4:
    quit()
elif scenario==5:
    fileToSend =  errorfile 
    content["subject"] = today+"標案資料更新錯誤匯報"  
    part = MIMEText("今日標案資料更新發生異常！請參閱附檔的錯誤報告。", _charset="UTF-8")
    receivers = ['show19970117@gmail.com,sean.he.huang@tw.ey.com,EY.TW.Digitals@gmail.com']


content["from"] = "EY.TW.Digitals@gmail.com"  #寄件者
content["to"] = ','.join(receivers) #收件者
content.attach(part)

import smtplib
ctype, encoding = mimetypes.guess_type(fileToSend)
if ctype is None or encoding is not None:
    ctype = "application/octet-stream"
maintype, subtype = ctype.split("/", 1)

fp = open(fileToSend,encoding = 'utf-8')
attachment = MIMEText(fp.read(), 'base64', 'utf-8')
fp.close()
if scenario in [1,3]:
    attachment.add_header("Content-Disposition", "attachment", filename='標案資料'+sd+'-'+ed+'.csv')
elif scenario in [2,5]:
    attachment.add_header("Content-Disposition", "attachment", filename=today+'ErrorReport.log')
content.attach(attachment)

with smtplib.SMTP(host="smtp.gmail.com", port="587") as smtp:  # 設定SMTP伺服器
    try:
        smtp.ehlo()  # 驗證SMTP伺服器
        smtp.starttls()  # 建立加密傳輸
        smtp.login("EY.TW.Digitals@gmail.com", "zmcbhlulntvswoby")  # 登入寄件者gmail
        smtp.send_message(content)  # 寄送郵件
        print("Complete!")
    except Exception as e:
        print("Error message: ", e)