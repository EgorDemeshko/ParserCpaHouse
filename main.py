import requests
from bs4 import BeautifulSoup
import time
import json, codecs

def procces_elem(num, num_otn):
    inf_offers[num]['name'] = all_offers[num_otn].find('div', {'class': 'prodName'}).text.rstrip().strip('\n')  # Название оффера
    inf_offers[num]['img'] = all_offers[num_otn].find("img")["src"]  # ссылка на изображение
    inf_offers[num]['id'] = all_offers[num_otn].find('div', {'class': 'prodSku'}).text.strip().strip('ID: ')  # id оффера
    inf_offers[num]['active'] = all_offers[num_otn].find('div', {'class': 'sProdStatus'}).text.strip('\n') # активный или нет

    infovals = all_offers[num_otn].find_all('span', {'class': 'sInfoVal'})

    inf_offers[num]['cr'] = infovals[0].text  # CR
    if inf_offers[num]['cr'] == '':
        inf_offers[num]['cr'] = 'null'
    inf_offers[num]['approve'] = infovals[1].text  # Апрув
    if inf_offers[num]['approve'] == '':
        inf_offers[num]['approve'] = 'null'
    inf_offers[num]['category'] = infovals[2].text  # Категория
    inf_offers[num]['country'] = infovals[3].text.strip('\n')  # Страна

    if (infovals[3].text.strip('\n') == 'Все страны') or (infovals[3].text.strip('\n') == 'Временно остановлен.'):
        inf_offers[num]['cost'] = infovals[3].text.strip('\n')  # Стоимость !!!ОБРАБОТКА ИСКЛЮЧЕНИЙ, ЕСЛИ СТОИМОСТЬ И ОТЧИСЛЕНИЯ НЕ УКАЗАНЫ!!!
        inf_offers[num]['deductiond'] = infovals[3].text.strip('\n')  # Отчисления
    else:
        inf_offers[num]['cost'] = infovals[4].text.strip('\n')  # Стоимость
        inf_offers[num]['deductions'] = infovals[5].text.strip('\n')  # Отчисления

    inf_offers[num]['href'] = all_offers[num_otn].find("a")["href"] #ссылка на оффер

headers = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    'Accept-Encoding': 'gzip, deflate, br',
    'Accept-Language': 'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7',
    'Cache-Control': 'max-age=0',
    'Connection': 'keep-alive',
    'Cookie': 'SLG_GWPT_Show_Hide_tmp=1; SLG_wptGlobTipTmp=1; ci_session=f0o7peb1vc0nebb9d82bjrqs6jdnr09o',
    'Host': 'cpa.house',
    'Referer': 'https://cpa.house/login',
    'sec-ch-ua': '"Opera";v="77", "Chromium";v="91", ";Not A Brand";v="99"',
    'sec-ch-ua-mobile': '?1',
    'Sec-Fetch-Dest': 'document',
    'Sec-Fetch-Mode': 'navigate',
    'Sec-Fetch-Site': 'same-origin',
    'Sec-Fetch-User': '?1',
    'Upgrade-Insecure-Requests': '1',
    'User-Agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.114 Mobile Safari/537.36'
}

r = requests.get('https://cpa.house/webmaster/offers', headers=headers)
print(r.status_code)
soup = BeautifulSoup(r.text)

count_offers = int(soup.find('span', {'class': 'count-offers'}).text)   # количество офферов (всего)


all_offers = soup.find_all('div', {'class': 'prodContentBlock'})

inf_offers = {a: {'name': '', 'img': '', 'id': '', 'active': '', 'cr': '', 'approve': '', 'category': '', 'country': '', 'cost': '', 'deductions': '', 'href': ''} for a in range(1, count_offers+1)}  # создание словаря для всех офферов

for i in range(1, len(all_offers)):
    procces_elem(i, i)

count_offers = int(soup.find('span', {'class': 'count-offers'}).text)
print(count_offers)


for i in range(10, count_offers, 10):
    url = 'https://cpa.house/webmaster/offers/index/' + str(i)
    r = requests.get(url=url, headers=headers)
    print(r.status_code)
    soup = BeautifulSoup(r.text)

    count_offers = int(soup.find('span', {'class': 'count-offers'}).text)  # количество офферов (всего)

    all_offers = soup.find_all('div', {'class': 'prodContentBlock'})

    for j in range(1, len(all_offers)):
        num = (i-10) + j
        procces_elem(num, j)

print(inf_offers)

#with open('data.json', 'wb') as f:
#    json.dump(data, codecs.getwriter('utf-8')(f), ensure_ascii=False)

