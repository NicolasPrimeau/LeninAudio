__author__ = 'Nixon'


from pymongo import MongoClient
import configurations
import time
from AudioPlayer import AudioPlayer


class Playlist:

    SIZE = 5
    RECENTLY_PLAYED_TIMEOUT_SEC = 60*30
    song_list = list()
    recently_played = dict()
    audioPlayer = None

    def __init__(self):
        self.audioPlayer = AudioPlayer()
        self.update_song_list()

    def update_song_list(self):
        if len(self.song_list) == self.SIZE:
            return
        self.clean_recently_played()
        client = MongoClient()
        coll = client[configurations.DB.NAME][configurations.DB.COLLECTIONS.SONGS]
        songs = list(coll.find({}).sort("upvotes", -1))
        if len(songs) == len(self.recently_played):
            self.recently_played = dict()
        self.song_list = list()
        while len(self.song_list) < self.SIZE and len(songs) > 0:
            song = songs.pop(0)
            if song['_id'] not in self.recently_played:
                self.song_list.append(song)
        client.close()

    def clean_recently_played(self):
        new_list = dict()
        now = int(time.time())
        for song in self.recently_played:
            if (now - self.recently_played[song]) < self.RECENTLY_PLAYED_TIMEOUT_SEC:
                new_list[song] = self.recently_played[song]
        self.recently_played = new_list

    def play_next_song(self):
        print("wat")
        if len(self.song_list) == 0:
            self.update_song_list()

        if len(self.song_list) != 0:
            song = self.song_list.pop(0)
            self.recently_played[song['_id']] = int(time.time())
            self.audioPlayer.play(song)
            return True
        return False

    def is_initial(self):
        return self.audioPlayer.is_initial()