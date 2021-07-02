import requests
from bs4 import BeautifulSoup


def procces_elem(num):
    inf10[num][0] = tables[num].find('div', {'class': 'prodName'}).text.rstrip().strip('\n')  # Название оффера
    inf10[num][1] = tables[num].find("img")["src"]  # ссылка на изображение
    inf10[num][2] = tables[num].find('div', {'class': 'prodSku'}).text.strip().strip('ID: ')  # id оффера
    inf10[num][3] = tables[num].find('div', {'class': 'sProdStatus'}).text.strip('\n') # активный или нет

    infovals = tables[num].find_all('span', {'class': 'sInfoVal'})

    inf10[num][4] = infovals[0].text  # CR
    if inf10[num][4] == '':
        inf10[num][4] = '-'
    inf10[num][5] = infovals[1].text  # Апрув
    if inf10[num][5] == '':
        inf10[num][5] = '-'
    inf10[num][6] = infovals[2].text  # Категория
    inf10[num][7] = infovals[3].text.strip('\n')  # Страна

    if (infovals[3].text.strip('\n') == 'Все страны') or (infovals[3].text.strip('\n') == 'Временно остановлен.'):
        inf10[num][8] = infovals[3].text.strip('\n')  # Стоимость !!!ОБРАБОТКА ИСКЛЮЧЕНИЙ, ЕСЛИ СТОИМОСТЬ И ОТЧИСЛЕНИЯ НЕ УКАЗАНЫ!!!
        inf10[num][9] = infovals[3].text.strip('\n')  # Отчисления
    else:
        inf10[num][8] = infovals[4].text.strip('\n')  # Стоимость
        inf10[num][9] = infovals[5].text.strip('\n')  # Отчисления

    inf10[num][10] = tables[num].find("a")["href"] #ссылка на оффер

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

r = requests.get('https://cpa.house/webmaster/offers/index/720', headers=headers)
print(r.status_code)

with open('test.html', 'w') as output_file:
  output_file.write(r.text)

soup = BeautifulSoup(r.text)
tables = soup.find_all('div', {'class': 'prodContentBlock'})

inf10 = [[''] * 11 for i in range(10)]

for i in range(len(tables)):
    procces_elem(i)

for item in inf10:
    print(item, '\n')