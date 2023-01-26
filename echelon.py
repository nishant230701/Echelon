from bs4 import BeautifulSoup
import requests
from collections import namedtuple


def extractText(arr, mode):
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


r = requests.get('https://genius.com')


soup = BeautifulSoup(r.text, 'html.parser')


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
for song in songs:
    print(song)