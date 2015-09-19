__author__ = 'Nixon'


from pymongo import MongoClient
import configurations
import time

class Playlist:
    song_list = list()
    recently_played = dict()

    def __init__(self):
        self.update_song_list()

    def update_song_list(self):
        self.song_list = list()
        self.clean_recently_played()
        client = MongoClient()
        coll = client[configurations.DB.NAME][configurations.DB.COLLECTIONS.SONGS]
        songs = list(coll.find({}, limit=50).sort("upvotes", 1))
        while len(self.song_list) < 10:
            song = songs.pop(0)
            if song['title'] + "-"+song['artist'] not in self.recently_played:
                self.song_list.append(song)

    def clean_recently_played(self):
        new_list = dict()
        now = time.time()
        for song in self.recently_played:
            if (now - song['last_played']) < (60*30):
                new_list[song['title'] + "-" + song['artist']] = song
        self.recently_played = new_list

    def play_next_song(self):
