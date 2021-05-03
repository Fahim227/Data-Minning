from bs4 import BeautifulSoup
from urllib import request as rqst
import re
import pandas as pd
import concurrent.futures
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time, json
from selenium.common.exceptions import WebDriverException

source = "https://www.racingpost.com"
driverlink = "C:/Users/user/Downloads/chromedriver_win32/chromedriver.exe"
MAX_THREADS = 30
eventj = []

def pageTwo(pageTwourl, horse_name):
    tm = time.time()
    # print(pageTwourl)
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    driver = webdriver.Chrome(options=chrome_options)  # options=chrome_options

    for i in range(0,100):
        driver.get(pageTwourl)
        driver.implicitly_wait(3)
        # content = driver.execute_script("return document.documentElement.outerHTML")
        html = driver.page_source
        soup = BeautifulSoup(html, "lxml")
        # time.sleep(5)
        table = soup.find('table', {'class': 'ui-table hp-formTable ui-table_type1 ui-table_sortable'})
        if table != None:
            print("page 2 done in:", i + 1)
            break
        else:
            i += 1
            print("page 2 trying:", i + 1)
            continue
    page_two_dataList = []
    try:
        table_body = table.find('tbody', {'class': 'ui-table__body'})
        table_datas = table_body.findAll('tr', {'class': 'ui-table__row'})
        # i = 0

        for data in table_datas:
            try:
                try:
                    date = data.find('a', {'class': "ui-link ui-link_table js-popupLink"}).get_text(strip=True)
                except:
                    pass
                try:
                    date_link = data.find('a', {'class': "ui-link ui-link_table js-popupLink"})['href']
                except:
                    pass
                keyword, winning_time = pageThree(source + date_link, horse_name)
                try:
                    course = data.find("span", {"class": "hidden-lg-up"}).get_text(strip=True)
                except:
                    course = "null"
                try:
                    Class = data.find("span")
                    Class.a.decompose()
                    Class.find('span', {'class': 'hidden-sm-up'}).decompose()
                    Class.find('span', {'class': 'hidden-xs-down'})
                    Class = Class.get_text(strip=True)
                except:
                    Class = "null"
                try:
                    price_money = data.find(class_="hidden-xs-down").get_text(strip=True)
                except:
                    price_money = "null"
                try:
                    table_cell = data.findAll(class_="ui-table__cell")
                    distance = table_cell[2].get_text(strip=True)
                    wgt = table_cell[4].get_text(strip=True)
                    pos = table_cell[5].find('strong').get_text(strip=True)
                    total_horses = table_cell[5]
                    total_horses.strong.decompose()
                    total_horses.a.decompose()
                    total_horses = total_horses.get_text(strip=True).replace('/', "")
                    SP = table_cell[6].get_text(strip=True)
                    jokey = table_cell[7].find('a').get_text(strip=True)
                except:
                    wgt = "null"
                    pos = "null"
                    total_horses = "null"
                    SP = "null"
                    jokey = "null"
                # print(date, date_link, " ", " ", course, " ",Class, " ", price_money, " ", distance, " ", wgt, " ", pos, " ", total_horses, " ", SP, " ", jokey)
                # print("Keyword:", keyword)
                # print("Winning:", winning_time)
                pagetwo = {
                    'each_horse_race_date': date,
                    'course': course,
                    'each_race_class': Class,
                    'each_race_price_money': price_money,
                    'each_race_wgt': wgt,
                    'each_race_pos': pos,
                    'each_race_SP': SP,
                    'each_race_jokey': jokey,
                    'each_race_keyword': keyword,
                    'each_race_winning_time': winning_time,
                    'each_race_total_horses': total_horses,
                }
                page_two_dataList.append(pagetwo)
            except:
                pagetwo = {
                    'each_horse_race_date': "null",
                    'course': "null",
                    'each_race_class': "null",
                    'each_race_price_money': "null",
                    'each_race_wgt': "null",
                    'each_race_pos': "null",
                    'each_race_SP': "null",
                    'each_race_jokey': "null",
                    'each_race_keyword': "null",
                    'each_race_winning_time': "null",
                }
                page_two_dataList.append(pagetwo)
        return page_two_dataList
    except:
        pagetwo = {
            'each_horse_race_date': "null",
            'course': "null",
            'each_race_class': "null",
            'each_race_price_money': "null",
            'each_race_wgt': "null",
            'each_race_pos': "null",
            'each_race_SP': "null",
            'each_race_jokey': "null",
            'each_race_keyword': "null",
            'each_race_winning_time': "null",
        }
        page_two_dataList.append(pagetwo)
        return page_two_dataList
        pass
    print(time.time() - tm)


def pageThree(pageThreeurl, target_horse_name):
    print(pageThreeurl)
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    driver = webdriver.Chrome(driverlink, options=chrome_options)  # options=chrome_options

    for i in range(0,100):
        driver.get(pageThreeurl)
        driver.implicitly_wait(5)
        content = driver.execute_script("return document.documentElement.outerHTML")
        soup = BeautifulSoup(content, "html.parser")
        main_row = soup.findAll('tr', {'class': 'rp-horseTable__mainRow'})
        if main_row != None:
            i += 1
            print("Page 3 done in:", i + 1)
            break
        else:
            print("Page 3 trying:", i + 1)
            i += 1
            continue
    try:
        i = 0
        target_comment = 0
        for row in main_row:
            horse_name = row.find('td', {'class': 'rp-horseTable__horseCell'}).find('div',
                                                                                    {
                                                                                        'class': 'rp-horseTable__info'}).find(
                'a', {'class': 'rp-horseTable__horse__name'}).get_text(strip=True)
            if horse_name.lower() == target_horse_name.lower():
                target_comment = i
            i += 1
        # print(target_comment)
        try:
            keywords = soup.find('tbody').findAll('tr', {'class': 'rp-horseTable__commentRow'})
            keyword = re.sub(r"\s", "", keywords[target_comment].get_text(strip=True))
        except:
            keyword = "null"

        try:
            target_wining_time = re.sub(r"\s", "",
                                        soup.find('div', {'class': 'rp-raceInfo'}).findAll('li')[0].findAll('span', {
                                            'class': 'rp-raceInfo__value'})[2].get_text(strip=True))
        except:
            target_wining_time = "null"
        return keyword, target_wining_time
    except:
        return "null", "null"
    time.sleep(2)


def pageOne(pageurl):
    chrome_options = Options()
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--headless")
    driver = webdriver.Chrome(options=chrome_options)  # options=chrome_options
    try:
        i = 0
        while True:
            print("running", i)
            driver.get(pageurl)
            driver.implicitly_wait(3)
            html = driver.page_source
            # pageurl = rqst.urlopen(pageurl)
            soup = BeautifulSoup(html, "lxml")
            topleft = soup.find('div', {'class': 'RC-courseHeader'})
            if topleft != None:
                # print("page 1 done in : ", i + 1)
                i += 1
                break
            else:
                i += 1
                # print("page 1 trying: ", i+1)
                continue
    except WebDriverException:
        pass
    # content = driver.execute_script("return document.documentElement.outerHTML")  # rqst.urlopen(url)

    try:
        time = re.sub(r"\s", "", topleft.find('span', {'class': 'RC-courseHeader__time'}).get_text())
    except:
        time = "null"
    try:
        try:
            data = topleft.find('h1', {'class': 'ui-h1 RC-courseHeader__name'}).get_text(strip=True).split(" ", 2)
            meeting = re.sub(r"\s", "", data[0])
            surface = re.sub(r"\s", "", data[1])
            print(meeting, surface)
        except:
            meeting = topleft.find('h1', {'class': 'ui-h1 RC-courseHeader__name'}).get_text(strip=True)
            print(meeting)
    except:
        meeting = "null"
        print(meeting)
    try:
        date = topleft.find('span', {'class': 'RC-courseHeader__date'}).get_text(" ", strip=True)
    except:
        date = "null"
    try:
        distance = re.sub(r"\s", "", topleft.find('strong', {'class': 'RC-cardHeader__distance'}).get_text())
    except:
        distance = "null"
    try:
        Class = topleft.find('span', {'data-test-selector': 'RC-header__raceClass'}).get_text(strip=True)
    except:
        Class = "null"
    try:
        required_age = topleft.find('span', {'data-test-selector': 'RC-header__rpAges'}).get_text(strip=True)
    except:
        required_age = "null"
    try:
        surface = topleft.find('span', {'class': 'RC-courseHeader__surface hidden-sm-down'}).get_text(strip=True)
    except:
        surface = "null"

    print("")
    table = soup.find('div', {'class': 'RC-runnerRowWrapper'})
    horsesData = []
    print(1)
    try:
        all_table_datas = table.findAll('div', {'class': 'RC-runnerRow'})
        for data in all_table_datas:
            try:
                racecard_num = data.find('span', {'data-test-selector': 'RC-cardPage-runnerNumber-no'}).get_text(
                    strip=True)
            except:
                racecard_num = "null"
            try:
                draw = data.find('span', {'data-test-selector': 'RC-cardPage-runnerNumber-draw'}).get_text(strip=True)
            except:
                draw = "null"
            try:
                form = data.find('span', {'data-test-selector': 'RC-cardPage-runnerForm'}).get_text(strip=True)
            except:
                form = "null"
            try:
                horse_name = data.find('a', {'class': 'RC-runnerName'}).get_text(strip=True)
            except:
                horse_name = "null"
            try:
                abbreviations = data.find('div', {'class': 'RC-runnerStats'})
                abbreviations = abbreviations.findAll('div', {'class': 'RC-runnerStats__cdbf'})
                abbr = ""
                for abb in abbreviations:
                    abbr += abb.get_text(strip=True) + " "
                # print("abb: ",abbr)
            except:
                abbr = "null"
                print("abb: ", abbreviations)
            try:
                horse_link = data.find('a', {'class': 'RC-runnerName'})['href']
            except:
                horse_link = "null"
            try:
                last_run = data.find('div', {'data-test-selector': 'RC-cardPage-runnerStats-lastRun'}).get_text(
                    strip=True)
            except:
                last_run = "null"
            try:
                age = data.find('span', {'data-test-selector': 'RC-cardPage-runnerAge'}).get_text(strip=True)
            except:
                age = "null"
            try:
                weight = data.find('span', {'data-test-selector': 'RC-cardPage-runnerWgt-carried'}).get_text(strip=True)
                weight = weight[:1] + "-" + weight[1:]
            except:
                weight = "null"
            try:
                jokey = data.find('div', {'class': 'RC-runnerInfo RC-runnerInfo_jockey'}).get_text(strip=True)[2:]
            except:
                jokey = "null"
            try:
                trainer = data.find('div', {'class': 'RC-runnerInfo RC-runnerInfo_trainer'}).get_text(strip=True)[2:]
            except:
                trainer = "null"
            try:
                ts = data.find('span', {'class': 'RC-runnerTs'}).get_text(strip=True)
            except:
                ts = "null"
            try:
                rpr = data.find('span', {'class': 'RC-runnerRpr'}).get_text(strip=True)
            except:
                rpr = "null"
            # print(racecard_num, " ", draw, " ", form, " ", horse_name, " ", horse_link, " ", age, " ", weight, " ",jokey, " ", trainer, " ", ts, " ", rpr)
            pageTwoDataList = pageTwo(source + horse_link, horse_name)
            # print(2)
            horse = {
                'horse_name': horse_name,
                'abbreviations': abbr,
                'racecard_num': racecard_num,
                'draw': draw,
                'form': form,
                'age': age,
                'weight': weight,
                'surface': surface,
                'jokey': jokey,
                'trainer': trainer,
                'ts': ts,
                'rpr': rpr,
                'last_run': last_run,
                'racecard_num': racecard_num,
                'pagetwodatalist': pageTwoDataList
            }
            print(json.dumps(horse))
            horsesData.append(horse)
    except:
        print("Table Error")
        horse = {
            'horse_name': "null",
            'racecard_num': "null",
            'draw': "null",
            'form': "null",
            'age': "null",
            'weight': "null",
            'jokey': "null",
            'trainer': "null",
            'ts': "null",
            'rpr': "null",
            'last_run': "null",
            'racecard_num': "null",
            'pagetwodatalist': "null"
        }
        horsesData.append(horse)
        pass
    trainer_stats = []
    jokey_stats = []
    horse_stats = []
    try:
        # stats = driver.find_element_by_class_name("RC-accordion__statsRow")
        # stats_table = stats.find_elements_by_tag_name("tbody")
        # print("Null")
        # print(len(stats_table))
        chrome_options = Options()
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("--no-sandbox")
        driver2 = webdriver.Chrome(options=chrome_options)

        for i in range(0,100):
            driver2.get(pageurl)
            driver2.implicitly_wait(5)
            html2 = driver2.page_source
            soup2 = BeautifulSoup(html2, "html.parser")
            stats = soup2.find('section', {'data-accordion-row': 'stats'})
            if stats != None:
                print("Done in: ", i + 1)
                break

            else:
                i += 1
                print("failed", i + 1)
                continue
        try:
            stats_table = stats.findAll('tbody', {'class': 'RC-stats__tableBody'})
        except:
            stats_table = []
        print(len(stats_table))
        print("Stats Details:..........")
        try:
            stats_data_list = stats_table[0].findAll('tr', {'class': 'ui-table__row'})
        except:
            stats_data_list = []
        for stat in stats_data_list:
            try:
                trainer_name = stat.find('td', {'class': 'RC-stats__nameColumn'}).get_text(strip=True)
            except:
                trainer_name = "null"
            try:
                winning = re.sub(r"\s", "",
                                 stat.find('td', {'data-test-selector': 'RC-lastWinsRuns__row'}).get_text(strip=True))
            except:
                winning = "null"
            try:
                last_percent = re.sub(r"\s", "",
                                      stat.find('td', {'data-test-selector': 'RC-lastPercent__row'}).get_text(
                                          strip=True))
            except:
                last_percent = "null"
            try:
                overAll_winning = re.sub(r"\s", "",
                                         stat.find('td', {'data-test-selector': 'RC-overallWinsRuns__row'}).get_text(
                                             strip=True))
            except:
                overAll_winning = "null"
            try:
                overAll_percent = re.sub(r"\s", "",
                                         stat.find('td', {'data-test-selector': 'RC-overallPercent__row'}).get_text(
                                             strip=True))
            except:
                overAll_percent = "null"
            # print(trainer_name, " ", winning, " ", last_percent, " ", overAll_winning, " ", overAll_percent)
            trainer = {
                "trainer_name": trainer_name,
                "winning": winning,
                "last_percent": last_percent,
                "overAll_winning": overAll_winning,
                "overAll_parcent": overAll_percent
            }
            trainer_stats.append(trainer)
            print(json.dumps(trainer))
        print("Jokey Details:..........")
        jokey_data_list = stats_table[1].findAll('tr', {'class': 'ui-table__row'})
        for jokey in jokey_data_list:
            try:
                jokey_name = jokey.find('td', {'class': 'RC-stats__nameColumn'}).get_text(strip=True)
            except:
                jokey_name = "null"
            try:
                winning = re.sub(r"\s", "",
                                 jokey.find('td', {'data-test-selector': 'RC-lastWinsRuns__row'}).get_text(strip=True))
            except:
                winning = "null"
            try:
                last_percent = re.sub(r"\s", "",
                                      jokey.find('td', {'data-test-selector': 'RC-lastPercent__row'}).get_text(
                                          strip=True))
            except:
                last_percent = "null"
            try:
                overAll_winning = re.sub(r"\s", "",
                                         jokey.find('td', {'data-test-selector': 'RC-overallWinsRuns__row'}).get_text(
                                             strip=True))
            except:
                overAll_winning = "null"
            try:
                overAll_percent = re.sub(r"\s", "",
                                         jokey.find('td', {'data-test-selector': 'RC-overallPercent__row'}).get_text(
                                             strip=True))
            except:
                overAll_percent = "null"
            # print(jokey_name, " ", winning, " ", last_percent, " ", overAll_winning, " ", overAll_percent)
            jokey= {
                "jokey_name": jokey_name,
                "winning": winning,
                "last_percent": last_percent,
                "overAll_winning": overAll_winning,
                "overAll_parcent": overAll_percent
            }
            jokey_stats.append(jokey)
            print(json.dumps(jokey))
        print("Horse Details:..........")
        horse_data_list = stats_table[2].findAll('tr', {'class': 'ui-table__row'})
        for horse in horse_data_list:
            try:
                horse_name = horse.find('td', {'class': 'RC-stats__horseNameColumn'}).get_text(strip=True)
            except:
                horse_name = "null"
            try:
                going_wins = re.sub(r"\s", "",
                                    horse.find('td', {'data-test-selector': 'RC-goingWinsRuns__row'}).get_text(
                                        strip=True))
            except:
                going_wins = "null"
            try:
                going_percent = re.sub(r"\s", "",
                                       horse.find('td', {'data-test-selector': 'RC-goingPercent__row'}).get_text(
                                           strip=True))
            except:
                going_percent = "null"

            try:
                distance_winning = re.sub(r"\s", "",
                                          horse.find('td', {'data-test-selector': 'RC-distanceWinsRuns__row'}).get_text(
                                              strip=True))
            except:
                distance_winning = "null"
            try:
                course_percent = re.sub(r"\s", "",
                                        horse.find('td', {'data-test-selector': 'RC-coursePercent__row'}).get_text(
                                            strip=True))
            except:
                course_percent = "null"
            # print(horse_name, " ", going_wins, " ", going_percent, " ", distance_winning, " ", course_percent)
            horse= {
                "horse_name": horse_name,
                "going_wins": going_wins,
                "going_parcent": going_percent,
                "distance_winning": distance_winning,
                "course_percent": course_percent
            }
            horse_stats.append(horse)
            print(json.dumps(horse))
    except:
        print("Really Null")
        pass
    event = {
        'time': time,
        'meeting': meeting,
        'date': date,
        'distance': distance,
        'class': Class,
        'required_age': required_age,
        'horses': horsesData,
        'trainer_stats': trainer_stats,
        'jokey_stats': jokey_stats,
        'horse_stats': horse_stats
    }
    eventj.append(event)
    print(json.dumps(event))
    """with open('jfile.json', 'r+') as outfile:
        data = json.load(outfile)
        data.update(event)
        outfile.seek(0)
        json.dump(data, outfile)
    """

    time.sleep(3)
    # return event


# Press the green button in the gutter to run the script.
if __name__ == '__main__':

    past = time.time()
    baseurl = "/racecards/"
    # page3 = "/results/46/pontefract/2021-04-19/780397"
    # target_horse = "Smullen"
    # keyword, winning_time = pageThree(source + page3, target_horse)
    # print(keyword, winning_time)
    # page = rqst.urlopen(source + baseurl)
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    driver = webdriver.Chrome(options=chrome_options)  # options=chrome_options
    while True:
        driver.get(source + baseurl)
        driver.implicitly_wait(5)
        html = driver.page_source
        # content = driver.execute_script("return document.documentElement.outerHTML")
        soup = BeautifulSoup(html, "html.parser")
        allSections = soup.findAll("section", {"class": "ui-accordion__row"})
        if len(allSections) != 0:
            break
        else:
            print("Loop")
            continue
    # all = driver.find_elements_by_class_name("ui-accordion__row")
    print(len(allSections))
    # section1 = allSections[3]
    # races = section1.find("div", {"class": "RC-meetingList"}).findAll("div", {"class": "RC-meetingItem"})
    # page1 = source + races[3].find('a')['href']
    # print(page1)
    # print(pageOne(page1))
    racesurlList = []
    resultInJson = []
    for section in allSections:
        races = section.find("div", {"class": "RC-meetingList"}).findAll("div", {"class": "RC-meetingItem"})
        for race in races:
            page = source + race.find('a')['href']
            racesurlList.append(page)

    # all urls in resulturlList
    print(len(racesurlList))
    threads = min(MAX_THREADS, len(racesurlList))

    with concurrent.futures.ThreadPoolExecutor(max_workers=threads) as executor:
        executor.map(pageOne, racesurlList)

    """for pg in racesurlList:
        tm = time.time()
        print(pg)
        resultInJson.append(json.dumps(pageOne(pg)))
        print(time.time() - tm)
        print("\n")
    # print(resultInJson)
    with open('jfile.json', 'a') as outfile:
        json.dump(resultInJson, outfile)"""
    with open('realAllData.json', 'a') as outfile:
        json.dump(eventj, outfile)
    """data = json.load(open('data.json'))
    print(data[1])
    with open('realAllData.json', 'a') as outfile:
        json.dump(data[1], outfile)"""
    print(time.time() - past)
