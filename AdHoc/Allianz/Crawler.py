import requests
import pandas as pd
from bs4 import BeautifulSoup

def get_web_page(url):
    resp = requests.get(
        url=url
    )
    if resp.status_code != 200:
        print('Invalid url:', resp.url)
        return None
    else:
        return resp.text

def get_table(page):
    soup = BeautifulSoup(page, 'html.parser')
    table = soup.find('table', 'wfb0c')
    columns = [th.text for th in table.find('tr', id = 'oScrollMenu').find_all('td', 'wfb3c')]
    rows = table.find_all('tr')[2:]
    data = list()
    for r in rows:
        bank = [t.text for t in r.find_all('td')]
        data.append(bank)
    df = pd.DataFrame(data, columns=columns)
    
    return df 


if __name__ == '__main__':
    url = 'https://www.yesfund.com.tw/w/wp/wp00.djhtm'
    page = get_web_page(url)
    df = get_table(page)
    df.to_csv('基金投信公司總表.csv', index=False, encoding='utf-8-sig')