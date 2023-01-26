from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options as FirefoxOptions
import time
import json

# Number of songs from top charts
SONG_LIMIT = 50

def extractText(arr, mode):
    '''arr: [rank, title, artist, views, link] for each song'''
    if mode == 'listofdicts':
        songs = []
        for rank, title, artist, views, link in arr:
            song = {'rank': rank.text, 'title': title.text, 'artist': artist.text, 'views': views.text, 'link': link.get('href')}
            songs.append(song)
        
        return songs
    
    if mode == 'listoflists':
        songs = []
        for rank, title, artist, views, link in arr:
            song = [rank.text, title.text, artist.text, views.text, link.get('href')]
            songs.append(song)
        
        return songs

# Don't open firefox window on screen
options = FirefoxOptions()
options.add_argument('--headless')

driver = webdriver.Firefox(options=options)
driver.get('https://genius.com')

# 
for _ in range(SONG_LIMIT // 10 - 1):
    elem = driver.find_element(By.XPATH, '/html/body/div[1]/div/div[5]/div[2]/div/div[3]/div')
    elem.click()
    time.sleep(5) # give 5 seconds rest between first click and finding the [see more] button again


soup = BeautifulSoup(driver.page_source, 'html.parser')

# findAll -> param1 : tag , param2 : class of the tag
artistnames = soup.findAll('h4', 'ChartSongdesktop__Artist-sc-18658hh-5 kiggdb')
songnames = soup.findAll('div', 'ChartSongdesktop__Title-sc-18658hh-3 fODYHn')
views = soup.findAll('span', 'TextLabel-sc-8kw9oj-0 knRXtG')
ranks = soup.findAll('div', 'ChartItemdesktop__Rank-sc-3bmioe-1 tDViA')
links = soup.findAll('a', 'PageGriddesktop-a6v82w-0 ChartItemdesktop__Row-sc-3bmioe-0 qsIlk')


chart = []
for i in range(len(artistnames)):
    song = [ranks[i],songnames[i],artistnames[i],views[i],links[i]]
    chart.append(song)

songs = extractText(chart, 'listofdicts')

# write charts in charts.txt file in json format
with open('charts.txt', 'w') as f:
    f.write(json.dumps(songs))