__author__ = 'Nixon'


from pymongo import MongoClient
import configurations
import time
from AudioPlayer import AudioPlayer


class Playlist:

    SIZE = 5
    RECENTLY_PLAYED_TIMEOUT_SEC = 60*30
    song_list = list()
    song_list_title_pair = list()
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
        songs = list(coll.find({}).sort("upvotes", 1))
        if len(songs) == len(self.recently_played):
            self.recently_played = dict()
        while len(self.song_list) < self.SIZE and len(songs) > 0:
            song = songs.pop(0)
            index = song['artist'] + "-" + song['title']
            if  index not in self.song_list_title_pair and index not in self.recently_played:
                self.song_list.append(song)
                self.song_list_title_pair.append(index)
            elif index in self.song_list_title_pair:
                self.song_list[self.song_list_title_pair.index(index)]['upvotes'] = song['upvotes']

    def clean_recently_played(self):
        new_list = dict()
        now = time.time()
        for song in self.recently_played:
            if (now - song['last_played']) < self.RECENTLY_PLAYED_TIMEOUT_SEC:
                new_list[song['title'] + "-" + song['artist']] = song
        self.recently_played = new_list

    def play_next_song(self):
        if len(self.song_list) == 0:
            self.update_song_list()

        if len(self.song_list) != 0:
            song = self.song_list.pop(0)
            index = song['artist'] + "-" + song['title']
            self.song_list_title_pair.remove(index)
            self.audioPlayer.play(song)
            return True
        return False

    def is_initial(self):
        return self.audioPlayer.is_initial()