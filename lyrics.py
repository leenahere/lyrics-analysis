import requests
from bs4 import BeautifulSoup
import os

from pymongo import MongoClient
#client = MongoClient()

client = MongoClient('mongodb://localhost:27017')

db = client.lyrics_analysis

CLIENT_ACCESS_TOKEN = os.environ.get("ACCESS_TOKEN")

base_url = 'https://api.genius.com'

token = 'Bearer {}'.format(CLIENT_ACCESS_TOKEN)
headers = {'Authorization': token}

for i in range(1,5):
    url = 'https://api.genius.com/artists/658/songs?per_page=50&page=' + str(i)
    r = requests.get(url, headers=headers)
    print(r.text)
    data = r.json()
    for song in data['response']['songs']:
        # Get song title
        title = song['title']

        # Get album for each song through another API call
        song_id = str(song['id'])
        album_url = 'https://api.genius.com/songs/' + song_id
        r_album = requests.get(album_url, headers=headers)
        album_data = r_album.json()
        album = ''
        if album_data['response']['song']['album'] != None:
            album = album_data['response']['song']['album']['name']
        print(album)
        print(type(album))

        # Get song lyrics
        URL = song['url']
        page = requests.get(URL)
        html = BeautifulSoup(page.text, "html.parser")  # Extract the page's HTML as a string
        lyrics_scraped = html.find("div", class_="lyrics").get_text() # Scrape the song lyrics from the HTML
        print(lyrics_scraped)

        # Insert into db
        lyrics = db.lyrics
        lyrics_data = {
            'title': title,
            'album': album,
            'lyrics': lyrics_scraped
        }
        result = lyrics.insert_one(lyrics_data)

        print('One post: {0}'.format(result.inserted_id))