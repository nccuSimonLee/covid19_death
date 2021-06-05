import requests
from bs4 import BeautifulSoup as bs
import re
import tqdm

def request_death_data(url):
    res = requests.get(url)
    soup = bs(res.text, 'html.parser')
    editor_box = soup.select_one('.editor_Box')
    death_data = []
    for p in editor_box.select('p'):
        if p.select('span') and p.text.find('死亡日') > -1:
            death_data.append(p_to_data(p))
    return death_data

def p_to_data(p):
    rows = [row for row in p.text.split('\n') if row]
    data = {'id': rows[0]}
    for row in rows[1:]:
        field, val = row.split('：')
        data[field] = val
    return data

def main():
    with open('source_urls.txt', 'r') as f:
        source_urls = f.read().splitlines()
    
    death_data = []
    for url in tqdm.tqdm(source_urls):
        death_data.extend(request_death_data(url))
        
    fields = ['id', '發病日', '確診日', '死亡日', '疾病史', '感染源', '接觸者']
    with open('covid19_death_data.csv', 'w') as f:
        f.write(','.join(fields) + '\n')
        for data in death_data:
            f.write(','.join([data[f] for f in fields]) + '\n')
    
    return

if __name__ == '__main__':
    main()
