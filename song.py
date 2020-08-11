import librosa
import pygame.mixer as musicplayer
import math
import numpy

from spectrogram import Spectrogram

# calc song data and then store in bin file 
# easier retrieval??

class Song:
    """a song that can be played"""

    def __init__(self, songFile):
        self.songFile = songFile
        self.pos = 0

        self.waveform = None
        self.sampling_rate = 0 
        self.tempo = 0
        self.beat_frames = None
        self.beat_times = None
        self.spectrogram = None
        self.max_wv = 0
        self.min_wv = 0

    def save(self, fileName=None):
        """serialize song data"""
        return False

    def load(self, fileName):
        """deserialize song data"""
        return False

    def extract(self):
        """calculate song data"""

        wv, sr = librosa.load(self.songFile)
        self.waveform = wv
        self.sampling_rate = sr

        tempo, frames = librosa.beat.beat_track(y=wv, sr=sr)
        times = librosa.frames_to_time(frames, sr=sr)
        self.tempo = tempo
        self.beat_frames = frames
        self.beat_times = times

        # self.spectrogram = librosa.feature.melspectrogram(y=wv)
        self.spectrogram = Spectrogram(wv)

        for num in wv:
            if num > self.max_wv:
                self.max_wv = num
            if num < self.min_wv:
                self.min_wv = num

    def extract_partial(self, dr, s):
        wv, sr = librosa.load(self.songFile, duration=dr, sr=s)

    def setup(self):
        """load up song for playing"""
        musicplayer.init()
        musicplayer.music.load(self.songFile)

    def play(self):
        musicplayer.music.play()

    def pause(self):
        musicplayer.music.pause()

    def position(self):
        return musicplayer.music.get_pos() / 1000

    def spectro_frame(self):
        """current spectrogram column"""
        # MAGIC NUMBER BAD
        dur = 30 # !       
        song_percent = self.position() / dur
        spectro_idx = int(self.spectrogram.width * song_percent)
        
        ret = []
        for i in range(len(self.spectrogram.graph) - 1):
            ret.append(self.spectrogram.graph[i][spectro_idx])
        return ret

    def current_amplitude(self):
        """current volume"""
        # MAGIC NUMBER BAD
        dur = 30 # !       
        song_percent = self.position() / dur
        wv_idx = math.ceil(len(self.waveform) * song_percent)
        #print(self.position())
        return self.waveform[wv_idx]

    def max_wv_val(self):
        ret = 0
        for val in self.waveform:
            ret = max(ret, abs(val))
        return ret
