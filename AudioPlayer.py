__author__ = 'Nixon'

import pafy
from subprocess import Popen, PIPE
import configurations
import time
import glob


class States:
    INITIAL = 1
    PLAYING = 2
    STOPPED = 3
    PAUSED = 4


class AudioPlayer:

    song = None
    state = States.INITIAL
    startup = -1

    def __init__(self):
        self.mplayer = None

    def play(self, song=None):
        if self.state == States.INITIAL or self.state == States.STOPPED:
            self.song = song
            index = configurations.BUFFERED_TEMP_LOCATION + "-" + self.song['artist'] + "-" + self.song['title']
            available = list(glob.glob(index + "*"))
            if len(available) > 0:
                location = available.pop(0)
            else:
                stream = pafy.new(song['youtube_link']).getbestaudio()
                location = index+"."+stream.extension
                stream.download(filepath=location)
            print(location)
            self.mplayer = Popen(["mplayer", "-slave", "-really-quiet", location], stdin=PIPE)
            self.startup = int(time.time())
            self.state = States.PLAYING
        elif self.state == States.PAUSED:
            self.mplayer.stdin.write(b"p\n")
            self.mplayer.stdin.flush()
            self.state = States.PLAYING

    def pause(self):
        self.mplayer.write(b"p\n")
        self.mplayer.flush()
        self.state = States.PAUSED

    def stop(self):
        self.mplayer.kill()
        self.state = States.STOPPED

    def is_dying(self):
        return time.time() > (self.song.duration-5+self.startup)

    def is_stopped(self):
        if self.state == States.STOPPED:
            return True
        elif self.state == States.INITIAL:
            return False
        elif self.mplayer.poll() is None:
            self.state = States.STOPPED

        return self.state == States.STOPPED

    def is_initial(self):
        return self.state == States.INITIAL
