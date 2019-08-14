from pymongo import MongoClient
import re
import collections
import numpy as np
import matplotlib.pyplot as plt
import random

client = MongoClient()

client = MongoClient('mongodb://localhost:27017')

db = client.lyrics_analysis
lyrics = db.lyrics

albums = lyrics.find({}, {"album": 1})

albums_list = [document["album"] for document in albums]
all_albums = list(dict.fromkeys(albums_list))
print(all_albums)

all_lyrics = lyrics.find({}, {"lyrics": 1})

all_lyrics_list = [document["lyrics"] for document in all_lyrics]
joined_string = " ".join(all_lyrics_list)

print(all_lyrics_list[0])
words_in_song = re.findall(r'\w+', all_lyrics_list[0].lower())
print(words_in_song)

#cnt_song = collections.Counter()
#for word in words_in_song:
#    cnt_song[word] += 1

#print(cnt_song)
#unique_words_in_song = {x : cnt_song[x] for x in cnt_song if cnt_song[x] <= 1}
#print(len(unique_words_in_song))


words = re.findall(r'\w+',joined_string.lower())
print(words)

cnt = collections.Counter()
for word in words:
    cnt[word] += 1

unique_words = {x : cnt[x] for x in cnt if cnt[x] <= 1}

print(unique_words)
print(len(unique_words))

unique_words_all = []

#For loop: albums
for album in all_albums:
    print(album)
    album_lyrics = lyrics.find({"album": album}, {"lyrics": 1})
    unique_words_album = []

    for document in album_lyrics:
        words_in_album = re.findall(r'\w+', document["lyrics"].lower())
        cnt_album = collections.Counter()
        for word in words_in_album:
            cnt_album[word] += 1

        unique_words_in_song = {k: unique_words[k] for k in unique_words if k in cnt_album and unique_words[k] == cnt_album[k]}
        print(unique_words_in_song)
        unique_words_album.append(len(unique_words_in_song))

    unique_words_all.append(unique_words_album)

print(unique_words_all)

#del unique_words_all[1]
#del all_albums[1]
y= unique_words_all
x = all_albums

for xe, ye in zip(x, y):
    color = np.random.rand(3,)
    plt.scatter([xe] * len(ye), ye, edgecolor=color, c='white')

plt.axes().set_xticklabels(all_albums)
plt.xticks(rotation=90)

#fig_size = plt.rcParams["figure.figsize"]
#print(fig_size)
#fig_size[0] = 20
#fig_size[1] = 10
#print(fig_size)
#plt.rcParams["figure.figsize"] = fig_size

plt.tight_layout()
plt.savefig('unique_words.png')
plt.show()

#unique_words_in_song = {k: unique_words[k] for k in unique_words if k in cnt_song and unique_words[k] == cnt_song[k]}
#print(unique_words_in_song)
#print(len(unique_words_in_song))