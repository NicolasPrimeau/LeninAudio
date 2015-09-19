__author__ = 'Nixon'


from pymongo import MongoClient

class Playlist:
    song_list = list()

    def __init__(self):
        client = MongoClient

