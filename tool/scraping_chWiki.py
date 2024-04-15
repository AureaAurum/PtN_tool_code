import requests
from pathlib import Path
import json
import time
from bs4 import BeautifulSoup
import datetime
import yaml
import re


# スクレイピングしたいURL
url = 'https://wiki.biligame.com/wqmt/%E9%A6%96%E9%A1%B5'

# ページの内容を取得
response = requests.get(url)

# ページのコンテンツをBeautiful Soupで解析
soup = BeautifulSoup(response.text, 'html.parser')

# classがresp-tabs-containerの要素を取得
resp_tabs_container = soup.find('div', class_='resp-tabs-container')
currentdir = Path(__file__).parent

characters = {}
en = {}
zh = {}

def download_image(url, file_path):
  r = requests.get(url, stream=True)

  if r.status_code == 200:
    with open(file_path, "wb") as f:
      f.write(r.content)


# resp-tabs-container内のclassがtxzの要素を取得
if resp_tabs_container:
    txz_elements = resp_tabs_container.find_all(class_='txz')
    missing = []
    # txz要素の下にあるa要素からhref属性とtitle属性を取得
    for txz_element in txz_elements:
        a_element = txz_element.find('a')
        if a_element:
            href = a_element.get('href')
            url = "https://wiki.biligame.com/" + href
            title = a_element.find('span').text
            response = requests.get(url)

            # ページのコンテンツをBeautiful Soupで解析
            soup = BeautifulSoup(response.text, 'html.parser')
                        # CSSセレクタを使用して要素を取得
            target_element = soup.select_one('#mw-content-text > div > div.row > div:nth-child(1) > div.main-line-wrap > div > div > div:nth-child(4)')
            target_element2 = soup.select_one('#mw-content-text > div > div.row > div:nth-child(1) > table:nth-child(2) > tbody > tr:nth-child(2) > td:nth-child(4)')
            target_element3 = soup.select_one('#mw-content-text > div > div.row > div:nth-child(1) > div.visible-md.visible-sm.visible-lg > table > tbody > tr:nth-child(3) > td > a:nth-child(1) > img')
            englishname = soup.select_one('#mw-content-text > div > div.row > div:nth-child(2) > div.main-line-wrap > div > div > div:nth-child(1) > table:nth-child(1) > tbody > tr:nth-child(4) > td:nth-child(4)')
            # 要素が存在するか確認
            if target_element and target_element2 and target_element3 and englishname:
                english = englishname.get_text(strip=True)
                rarity = target_element2.get_text(strip=True)
                sin = target_element.select("table:nth-child(1)>tbody>tr:nth-child(1)>td>a")[0].get_text(strip=True)
                rankup_material1 = target_element.select("table:nth-child(1)>tbody>tr:nth-child(1)>td>a")[1].get_text(strip=True)
                rankup_material2 = target_element.select("table:nth-child(1)>tbody>tr:nth-child(1)>td>a")[2].get_text(strip=True)
                skill_material = target_element.select("table:nth-child(2)>tbody>tr:nth-child(4)>td>a")[1].get_text(strip=True)
                if skill_material == "狄斯币 " or rankup_material1 == "狄斯币 " or rankup_material2 == "狄斯币 ":
                    missing.append(title)
                    continue
                naikai = target_element.select("table:nth-child(2)>tbody>tr:nth-child(8)>td>a")[2].get_text(strip=True)
                condition = {"level":1,"ru1":"false","ru2":"false","ru3":"false","slv":[1,1,1,1],"target_slv": [10, 10, 10, 10]}
                character = {"rarity":rarity,"name":english,"ename":english, "sin":sin, "rankup_material1":rankup_material1,"rankup_material2":rankup_material2,"skill_material":skill_material, "naikai":naikai,"condition":condition}
                characters[english] = character
                en[english] = english
                zh[english] = title


                img = currentdir / f'../public/img/characters/{english}.png'
                if not img.exists():
                    print("image downloading...")
                    url = target_element3.get('src')
                    download_image(url, currentdir / f'../public/img/characters/{english}.png')
                print(f'{title}, {english} done')
            else:
                print(f"{title}, {english} が見つかりませんでした。")
                missing.append(title)
            time.sleep(1)
    print(f"missing: {missing}")
else:
    print("指定されたクラスが見つかりませんでした。")

if  any(characters):

    characters["Echo"]["naikai"]="狂念"

    # 現在の日付と時刻を取得
    current_datetime = datetime.datetime.now()
    # 現在の日付と時刻を文字列に変換
    current_datetime_str = current_datetime.strftime("%Y-%m-%d %H:%M:%S")
    chjson = {}
    chjson["createdDate"] = current_datetime_str
    chjson["Characters"] = characters
    path = currentdir / r'../public/json/characters.json'
    json_file = open(path, mode="w", encoding='UTF-8')
    json.dump(chjson, json_file, indent=2, ensure_ascii=False)
    json_file.close()
    enpath = currentdir / r'../locales/en/en_characters.json'
    en_file = open(enpath, mode="w", encoding='UTF-8')
    json.dump(en, en_file, indent=2, ensure_ascii=False)
    en_file.close()
    zhpath = currentdir / r'../locales/zh/zh_characters.json'
    zh_file = open(zhpath, mode="w", encoding='UTF-8')
    json.dump(zh, zh_file, indent=2, ensure_ascii=False)
    zh_file.close()

with open(currentdir / r'./translate.yaml', encoding='utf-8') as readYaml:
    yaml = yaml.load(readYaml, Loader=yaml.Loader)

with open(currentdir / r'../public/json/characters.json',"rt", encoding='utf-8') as readParameter:
    parameter = readParameter.read()

with open(currentdir / r'../public/json/characters.json',"wt", encoding='utf-8') as writeParameter:
    print(parameter.encode('utf-8'))

    for item in yaml['replace']:
        print(f"index:{item['index']} before:{item['before']} after:{item['after']}")
        #parameter = parameter.replace(str(item['before']),str(item['after']))
        parameter = re.sub(str(item['before']+'(?![\u4E00-\u9FFF])'),str(item['after']),parameter)
    print(parameter.encode('utf-8'))
    writeParameter.write(parameter)
