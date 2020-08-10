
import raylibpy
import time

from loaddata import waveform, beats, play_song, music_time, spectro
from lightboard import LightBoard
from song import Song
from pulse import *

import librosa
import numpy as np

# ToDo

# allow play/pause of song

# music file
filename = "Music/Strobe30.wav"
#filename = "Music/The Veldt.wav"
#filename = "Music/Little Dark Age.wav"
#filename = "Tones/100Hz.wav"
#filename = "Tones/1kHz.wav"

#spec = spectro(wv)
#chroma = librosa.feature.chroma_stft(y=wv, sr=sr)
#c_cnt = len(chroma[0])
#c_idx = 0

s = Song(filename)
s.setup()
s.extract()

w = 64
h = 32
board = LightBoard(w, h, dot_size=4, offset=12)
board.set_rainbow_16()
cnt = board.count
#board.set_color_clear(raylibpy.BLUE)
mult = board.waveform_multiplier(s.max_wv_val())

wv_queue = []
pulses = []
beat_directions = [ L, R ]

raylibpy.set_target_fps(60)
raylibpy.init_window(800, 400, 'leds')

# synchronize song with window
while not raylibpy.is_window_ready():
    time.sleep(0.1)

beat_idx = 0
#next_beat = beat_times[beat_idx]
s.play()
while not raylibpy.window_should_close():

    # get times
    music_pos = s.position()
    ft = raylibpy.get_frame_time()
    tt = raylibpy.get_time() # + ft
        
    board.reset_leds()
    #board.draw_spectrogram(s.spectro_frame())  

    # get wv val
    wv_val = abs(int(s.current_amplitude() * mult))
    wv_queue.insert(0, wv_val)    
    # apply waveform  
    board.draw_amplitude_mirror(wv_queue)
    # clip queue
    if(len(wv_queue) > w / 2):
        wv_queue.pop(len(wv_queue) - 1)

    # check beats
    """
    if music_pos <= next_beat and music_pos + ft + eps > next_beat:
        p = Pulse(start_time=tt, jump_time=0.01, fade_amount=10, jump_fade=15)
        pulses.append(p)
        beat_idx = beat_idx + 1
        next_beat = beat_times[beat_idx]

    # run pulses
    board.draw_beat_pulse(pulses, beat_directions, tt)

    # get rid of old pulses
    to_delete = []
    for p in pulses:
        if tt - p.start_time > 3:
            to_delete.append(p)
    for p in to_delete:
        pulses.remove(p)
"""
    #board.update_leds(ft)   


    # draw
    raylibpy.begin_drawing()
    raylibpy.clear_background(raylibpy.BLACK)
    board.draw_leds()

    txt = "{:.2f} s".format(music_pos)
    raylibpy.draw_text(txt, 720, 20, 20, raylibpy.GREEN)

    raylibpy.end_drawing()

raylibpy.close_window()