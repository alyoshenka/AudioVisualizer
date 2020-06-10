#from playsound import playsound
import librosa
import pygame.mixer as py_music

import displaydata

def waveform(filename):
    # load audio as waveform y
    # store samping rate as sr
    wv, sr = librosa.load(filename, duration=30)
    return wv, sr

def beats(wv, sr):
    # default beat tracker
    tempo, beat_frames = librosa.beat.beat_track(y=wv, sr=sr)
    #print('Estimated tempo: {:.2f} beats per minute'.format(tempo))

    # convert frame indices of beat events into timestamps
    beat_times = librosa.frames_to_time(beat_frames, sr=sr)

    return beat_times, tempo

def play_song(filename, mute=False):
    py_music.init()
    py_music.music.load(filename)
    if mute:
        py_music.music.set_volume(0)
    py_music.music.play()

def music_time():
    return py_music.music.get_pos() / 1000

"""

filename = "Music/Little Dark Age.wav"
wv, sr = waveform(filename)

m = 0
for num in wv:
    m = max(m, abs(num))
print(m)

new_wv = {}
for i in range(len(wv)):
    num = wv[i]
    if abs(num) > 0.05:
        new_wv[i] = num

displaydata.display_waveform_dic(new_wv)
#displaydata.display_waveform(wv)
"""