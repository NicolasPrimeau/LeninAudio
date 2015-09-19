__author__ = 'Nixon'

from flask import Flask, render_template, request
from pymongo import MongoClient
import configurations
from Song import Song
import json
import string

app = Flask(__name__)


@app.route("/")
def main():
    return render_template("base.html")


@app.route('/_submit_song', methods=['POST'])
def _submit_song():
    title = request.form['title']
    artist = request.form['artist']
    song = Song(artist, title)
    song.store()
    return json.dumps({"code" : 404})


@app.route("/_get_song_listing.json", methods=["GET"])
def _get_song_listing():
    client = MongoClient()
    coll = client[configurations.DB.NAME][configurations.DB.COLLECTIONS.SONGS]
    songs = dict()
    songs['songs'] = list()
    for song in coll.find({}, limit=50).sort("upvotes", 1):
        del song["_id"]
        song['title'] = string.capwords(song['title'])
        song['artist'] = string.capwords(song['artist'])
        songs['songs'].append(song)
    client.close()

    return str(songs).replace("'", '"')



if __name__ == "__main__":
    app.run()