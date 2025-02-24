import requests
from bs4 import BeautifulSoup

url = 'https://ipdb.030101.xyz/bestcf/'

response = requests.get(url)
soup = BeautifulSoup(response.text, 'html.parser')

ips = []
for row in soup.find_all('tr')[1:]:  # 跳过表头
    cols = row.find_all('td')
    ip = cols[0].text.strip()
    ips.append(ip)

with open('ips.txt', 'w') as file:
    for ip in sorted(set(ips)):  # 去重并排序
        file.write(f'{ip}\n')
