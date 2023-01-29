import time
import yaml
import psycopg2
import schedule
from bs4 import BeautifulSoup
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options as FirefoxOptions

# Number of songs from top charts
SONG_LIMIT = 50
# Credentials
credentials = yaml.safe_load(open('credentials.yml'))
host = credentials['database']['host']
dbname = credentials['database']['dbname']
user = credentials['database']['user']
password = credentials['database']['password']

# Construct connection string

conn_string = f"host={host} port=5432 dbname={dbname} user={user} password={password} sslmode=require"

def extractText(arr):
    '''arr: [rank, title, artist, views, link] for each song'''
    for rank, title, artist, views, link, timestamp in arr:
        song = [int(rank.text), (title.text).replace('\u200b',''), artist.text, float(views.text[:-1]), link.get('href'),str(timestamp)]
        cursor.execute("INSERT INTO charts (ranks, songnames, artistnames, views, links, timestamp) VALUES (%s, %s, %s, %s, %s, %s);", (song[0],song[1],song[2],song[3],song[4],song[5]))
    return 

# Don't open firefox window on screen
def main(): 
    conn = psycopg2.connect(conn_string)
    print("Connection established")
    cursor = conn.cursor()
    cursor.execute("CREATE TABLE IF NOT EXISTS charts (ranks INT, songnames VARCHAR(150), artistnames VARCHAR(150), views FLOAT, links VARCHAR(2048), timestamp TIMESTAMP default NULL);")

    options = FirefoxOptions()
    options.add_argument('--headless')
    driver = webdriver.Firefox(options=options)
    driver.get('https://genius.com')
    for _ in range(SONG_LIMIT // 10 - 1): 
        elem = driver.find_element(By.XPATH, '/html/body/div[1]/div/div[5]/div[2]/div/div[3]/div')
        elem.click()
        time.sleep(5) # give 5 seconds rest between first click and finding the [see more] button again


    soup = BeautifulSoup(driver.page_source, 'html.parser')
    driver.quit()
    # findAll -> param1 : tag , param2 : class of the tag
    artistnames = soup.findAll('h4', 'ChartSongdesktop__Artist-sc-18658hh-5 kiggdb')
    songnames = soup.findAll('div', 'ChartSongdesktop__Title-sc-18658hh-3 fODYHn')
    views = soup.findAll('span', 'TextLabel-sc-8kw9oj-0 knRXtG')
    ranks = soup.findAll('div', 'ChartItemdesktop__Rank-sc-3bmioe-1 tDViA')
    links = soup.findAll('a', 'PageGriddesktop-a6v82w-0 ChartItemdesktop__Row-sc-3bmioe-0 qsIlk')
    timestamp = datetime.now()

    chart = []
    for i in range(len(artistnames)):
        song = [ranks[i],songnames[i],artistnames[i],views[i+7],links[i],timestamp]
        chart.append(song)
    songs = extractText(chart)
    conn.commit()
    cursor.close()
    conn.close()


schedule.every().day.at("12:00").do(main)
schedule.every().day.at("00:00").do(main)

while True:
    schedule.run_pending()
    time.sleep(60)