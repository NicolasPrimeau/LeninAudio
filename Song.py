__author__ = 'Nixon'


import urllib.request
import urllib.parse
import re
import configurations
import pafy
from pymongo import MongoClient


class SongError(SystemError):
    pass


class Song:
    artist = None
    title = None
    youtube_link = None
    duration = None
    upvotes = 0

    def __init__(self, artist, title, youtube_link=None, duration=None, upvotes=0):
        self.artist = artist.lower()
        self.title = title.lower()
        self.youtube_link = youtube_link
        self.duration = duration
        self.upvotes = upvotes
        self._gather_info()

    def _gather_info(self):
        client = MongoClient()
        coll = client[configurations.DB.NAME][configurations.DB.COLLECTIONS.SONGS]
        this = dict()
        this['artist'] = self.artist
        this['title'] = self.title
        cnt = 0
        f = None
        for song in coll.find(this):
            f = song
            cnt += 1
        if cnt > 1:
            raise SongError("More than one song with title and artist!")
        elif f is None:
            self._find_song()
            self.store()
        else:
            self.duration = f['duration']
            self.youtube_link = f['youtube_link']
            self.upvotes = f['upvotes']

    def _find_song(self):
        if self.error():
            raise SongError("Song object in illegal state")
        query_string = urllib.parse.urlencode({"search_query" : self.artist + " " + self.title})
        html_content = urllib.request.urlopen("http://www.youtube.com/results?" + query_string)
        search_results = re.findall(r'href=\"\/watch\?v=(.{11})', html_content.read().decode())
        top_result = "http://www.youtube.com/watch?v=" + search_results[0]
        self.youtube_link = top_result
        pf = pafy.new(top_result)
        self.duration = pf.duration

    def error(self):
        return self.artist is None or self.title is None

    def store(self):
        client = MongoClient()
        coll = client[configurations.DB.NAME][configurations.DB.COLLECTIONS.SONGS]
        this = dict()
        this['artist'] = self.artist
        this['title'] = self.title
        update = dict()
        update['artist'] = self.artist
        update['title'] = self.title
        update['duration'] = self.duration
        update['youtube_link'] = self.youtube_link
        update['upvotes'] = self.upvotes
        coll.update(this, update, upsert=True)
        client.close()

    def downvote(self):
        self.upvotes -= 1
        self.__update_ranking()

    def upvote(self):
        self.upvotes += 1
        self.__update_ranking()

    def __update_ranking(self):
        client = MongoClient()
        coll = client[configurations.DB.NAME][configurations.DB.COLLECTIONS.SONGS]
        this = dict()
        this['artist'] = self.artist
        this['title'] = self.title
        update = dict()
        update['upvotes'] = self.upvotes
        update['artist'] = self.artist
        update['title'] = self.title
        update['duration'] = self.duration
        update['youtube_link'] = self.youtube_link
        coll.update(this, update, upsert=False)
        client.close()


