import re
import requests
import pandas as pd

"""
raspa bootlegs do http://www.bobsboots.com criando um
dataset com a pontuação e ano de lançamento de cada boot
"""

MAIN_URL = 'http://www.bobsboots.com/CDs/'
pages = ['A-E_cd_index.html', 'F-K_cd_index.html', 'L-P_cd_index.html',
                 'Q-T_cd_index.html', 'U-Z_cd_index.html']

info_list = list()

for page in pages:
    r = requests.get(f'{MAIN_URL}{page}')
    texto = r.text
    sufixs = re.findall(r'cd-\w+.html', texto)

    for i, sufix in enumerate(sufixs):
        link = MAIN_URL + sufix

        if requests.get(link):
            source_code = requests.get(link).text

            title_raw = re.findall(r'title>([\w\s,.\'()/]+)\b(.*?)\2', source_code)
            title = title_raw[0]

            year_raw = re.findall(r'eleased:[="^#&,;\-@<>\w\s/.]+(\d{4})[&\s+<?](.*?)\2', source_code)
            if not bool(year_raw):
                year_raw = ['-']
            year = year_raw[0][0]

            stars_raw = re.findall(r'grade.html">(.+)(\d?)\sstars\2', source_code)
            if not bool(stars_raw):
                stars_raw = ['-']
            stars = re.findall(r'\d+', stars_raw[0][0])

            result = [title[0], year, stars, link]
            print(i, result)

            info_list.append(result)

df = pd.DataFrame(info_list, columns=['title', 'year', 'stars', 'link'])
print(df.head())