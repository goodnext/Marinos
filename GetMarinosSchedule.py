from pprint import pprint
from urllib3 import PoolManager
import requests
from bs4 import BeautifulSoup
import csv
import re
import unicodedata

#マルチバイトが含まれているか確認するためのメソッド
def is_japanese(string):
    for ch in string:
        name = unicodedata.name(ch) 
        if "CJK UNIFIED" in name \
        or "HIRAGANA" in name \
        or "KATAKANA" in name:
            return True
    return False

def main():
    POOL_MNG = PoolManager()
    TARGET_URL = "https://www.f-marinos.com/match/schedule-results/"
    HTML = requests.get(TARGET_URL)

    SOUP = BeautifulSoup(HTML.content, "html.parser")

    schedule_table = SOUP.findAll("table",{"class":"table_contents"})

    with open('marinos_schedule.csv', 'w') as csv_file:
        fieldnames = ['Subject','Start Date','Start Time','End Date','All Day Event','Description','Location','Private']
        csv_dict = {}
        writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
        writer.writeheader()
        cnt = 0
        for schedule_rows in schedule_table:
            cnt += 1
            if cnt == 100:
                break
            rows = schedule_rows.find_all("tr")
            for row in rows:
                #会場取得
                venue = row.findAll("td")[4].get_text()
                venue_list = venue.split()
                csv_dict['Location'] = venue_list[1]
                

                #対戦チーム取得
                vs_teams = row.findAll("td")[2].get_text()
                vs_teams_list = vs_teams.split()

                csv_dict['Subject']  = "【" + venue_list[0] + "】" + row.findAll("td")[1].get_text() + " " + vs_teams_list[0]

                #スケジュール部分抜き出し
                play_date = row.findAll("td")[0].get_text()
                play_date_list = play_date.split()
                
                #開始日
                csv_dict['Start Date'] = '2019/' + play_date_list[0]
                csv_dict['Start Date'] = re.sub('\(.*\)$',"",csv_dict['Start Date'])
                #開始時間
                if (is_japanese(play_date_list[2]) == True):
                    csv_dict['Start Time'] = ""
                else:
                    csv_dict['Start Time'] = play_date_list[2]
                writer.writerow(csv_dict)

if __name__ == "__main__":
    main()

    
