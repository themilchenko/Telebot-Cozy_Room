import lyricsgenius
import config

import requests
from bs4 import BeautifulSoup as BS

genius = lyricsgenius.Genius(config.TOKEN_GEN)

def get_popularity_songs(ar):
    artist = genius.search_artist(ar, max_songs=5, sort='popularity')
    counter = 1
    result_str = ''
    for i in artist.songs:
        result_str += 'Song ' + str(counter) + ': ' + str(i.title) + '\n'
        counter += 1
    return result_str

def find_lyrics_song(artist_, song_):
        song = genius.search_song(artist_, song_)
        return song.lyrics

def find_top_artists():
    url = 'https://genius.com/#top-songs'
    response = requests.get(url)
    soup = BS(response.text, 'html')

    title = soup.find_all('h4', class_='ChartSongdesktop__Artist-sc-18658hh-5 kiggdb')
    name = soup.find_all('div', class_='ChartSongdesktop__Title-sc-18658hh-3 fODYHn')

    res_str = ''

    res = dict(zip(title, name))
    counter = 1

    for keys, values in res.items():
        res_str += str(counter) + '. ' + keys.text + ' - ' + values.text + '\n'
        counter += 1

    return res_str
    