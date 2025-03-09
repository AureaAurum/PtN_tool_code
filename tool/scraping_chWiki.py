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

# 現在のフォルダを取得
currentdir = Path(__file__).parent

characters = {}
en = {}
zh = {}

def download_image(url, file_path):
  r = requests.get(url, stream=True)

  if r.status_code == 200:
    with open(file_path, "wb") as f:
      f.write(r.content)

# 既存のキャラクターデータを読み込み
path = currentdir / r'../public/json/characters.json'
existing_titles = []
uncompleted_titles = []
zhpath = currentdir / r'../locales/zh/zh_characters.json'
zhlocale = {}

with open(zhpath, 'r', encoding='UTF-8') as f:
    zhlocale = json.load(f)
with open(currentdir / '../locales/zh/zh_characters.json', 'r', encoding='utf-8') as f:
    data = json.load(f)
    existing_titles = list(data.values())
with open(path, "r", encoding="utf-8") as f:
    c = json.load(f)
    for name, stats in c["Characters"].items():
        if stats.get("naikai") not in ("狂念", "囁き", "亡骸"):
            uncompleted_titles.append(zhlocale[name])
print(f"uncompleted:{uncompleted_titles}")

# resp-tabs-container内のclassがtxdの要素を取得
if resp_tabs_container:
    txd_elements = resp_tabs_container.find_all(class_='txd')
    missing = []
    if not txd_elements:
        raise ValueError("wikiの仕様変更の可能性あり")
    # txd要素の下にあるa要素からhref属性とtitle属性を取得
    for txd_element in txd_elements:
        a_element = txd_element.find('a')
        if a_element:
            href = a_element.get('href')
            character_url = "https://wiki.biligame.com/" + href
            title = a_element.get('title')
            # 既存のキャラクターデータに存在しない場合のみスクレイピング
            if title not in existing_titles or title in uncompleted_titles:
                response = requests.get(character_url)

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
                    materials = target_element.select("table:nth-child(1)>tbody>tr:nth-child(1)>td>div>a")
                    sin = materials[0]['title']
                    rankup_material1 = materials[1]['title']
                    rankup_material2 = materials[2]['title']
                    skill_material = target_element.select("table:nth-child(2)>tbody>tr:nth-child(4)>td>div>a")[1]['title']
                    if skill_material == "狄斯币" or rankup_material1 == "狄斯币" or rankup_material2 == "狄斯币":
                        missing.append(title)
                        print(f"{title} skipped")
                        continue
                    naikai = target_element.select("table:nth-child(2)>tbody>tr:nth-child(8)>td>div>a")[2]['title']
                    if naikai not in ("内海亡骸", "内海呓语", "内海狂念"):
                        missing.append(title)
                        print(f"{title} の内海が不正です。")
                        naikai = "dummy"
                    condition = {"level":1,"target_level":90,"ru1":"false","ru2":"false","ru3":"false","slv":[1,1,1,1],"target_slv": [10, 10, 10, 10]}
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
                time.sleep(2)
    print(f"missing: {missing}, found: {list(characters.keys())}")
else:
    print("指定されたクラスが見つかりませんでした。")

if  any(characters):
    if ("Echo" in characters):
        characters["Echo"]["naikai"]="狂念"

    # 現在の日付と時刻を取得
    current_datetime = datetime.datetime.now()
    # 現在の日付と時刻を文字列に変換
    current_datetime_str = current_datetime.strftime("%Y-%m-%d %H:%M:%S")
    chjson = {}
    try:
        with open(path, 'r', encoding='UTF-8') as f:
            read_data = json.load(f)
        read_data["createdDate"] = current_datetime_str
        read_data["Characters"].update(characters)
        with open(path, 'w', encoding='UTF-8') as f:
            json.dump(read_data, f, indent=2, ensure_ascii=False)
    except FileNotFoundError:
        chjson["createdDate"] = current_datetime_str
        chjson["Characters"] = characters
        with open(path, mode="w", encoding='UTF-8') as f:
            json.dump(chjson, f, indent=2, ensure_ascii=False)

    enpath = currentdir / r'../locales/en/en_characters.json'
    enlocale = {}
    with open(enpath, 'r', encoding='UTF-8') as f:
        enlocale = json.load(f)
    enlocale.update(en)

    with open(enpath, 'w', encoding='UTF-8') as f:
        json.dump(enlocale, f, indent=2, ensure_ascii=False)

    zhpath = currentdir / r'../locales/zh/zh_characters.json'
    zhlocale = {}
    with open(zhpath, 'r', encoding='UTF-8') as f:
        zhlocale = json.load(f)
    zhlocale.update(zh)
    with open(zhpath, 'w', encoding='UTF-8') as f:
        json.dump(zhlocale, f, indent=2, ensure_ascii=False)


    with open(currentdir / r'./translate.yaml', encoding='utf-8') as readYaml:
        yaml = yaml.load(readYaml, Loader=yaml.Loader)
    with open(currentdir / r'../public/json/characters.json',"rt", encoding='utf-8') as readParameter:
        parameter = readParameter.read()
    with open(currentdir / r'../public/json/characters.json',"wt", encoding='utf-8') as writeParameter:
        #print(parameter.encode('utf-8'))
        for item in yaml['replace']:
            #print(f"index:{item['index']} before:{item['before']} after:{item['after']}")
            #parameter = parameter.replace(str(item['before']),str(item['after']))
            parameter = re.sub(str(item['before']+'(?![\u4E00-\u9FFF])'),str(item['after']),parameter)
        writeParameter.write(parameter)
