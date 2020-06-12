
import raylibpy
import time

from loaddata import waveform, beats, play_song, music_time, spectro
from lightboard import LightBoard
from pulse import *

import librosa
import numpy as np

filename = "Music/The Veldt.wav"
#filename = "Music/Little Dark Age.wav"
#filename = "Tones/100Hz.wav"

dur = 120
sr = 22050
wv, sr = waveform(filename, dr=dur, s=sr)
#from displaydata import all_specshows, chromas
#all_specshows(wv, sr)
#chromas(wv, sr)
beat_times, tempo = beats(wv, sr)
#spec = spectro(wv)
#chroma = librosa.feature.chroma_stft(y=wv, sr=sr)
#c_cnt = len(chroma[0])
#c_idx = 0

import math
spectro = librosa.amplitude_to_db(np.abs(librosa.stft(wv)), ref=np.max)
s_height = len(spectro) # number of frequencies
s_width = len(spectro[0]) # length of song
s_subdivides = 8 # number frequency subdivides
s_step = s_height / (1.0 * s_subdivides) # frequency subdivide length

s_start_pow = 5 # 0
s_end_pow = 13
max_freq = 8192 # max spectrogram frequency (2^13)
max_db = 80 # max decibel volume

# calculate waveform data
max_wv = 0
for num in wv:
    max_wv = max(max_wv, abs(num))
print("max_wv: ", max_wv)
wv_step = max_wv / 12.0

w = 64
h = 32
board = LightBoard(w, h, dot_size=4, offset=12)
cnt = board.count
"""
for i in range(len(board.leds)):
    row = i % h
    c = raylibpy.Color(raylibpy.GRAY)
    if row < 2:
        c = raylibpy.Color(raylibpy.PURPLE)
    elif row < 4:
        c = raylibpy.Color(raylibpy.RED)
    elif row < 6:
        c = raylibpy.Color(raylibpy.ORANGE)
    elif row < 8:
        c = raylibpy.Color(raylibpy.YELLOW)
    elif row < 10:
        c = raylibpy.Color(raylibpy.GREEN)
    elif row < 12:
        c = raylibpy.Color(raylibpy.BLUE)
    elif row == 15:
        c = raylibpy.Color(raylibpy.PURPLE)
    c.a = 0
    board.leds[i].color = c
"""
c = raylibpy.Color(raylibpy.BLUE)
c.a = 0
for led in board.leds:
    led.color = raylibpy.Color(c)
wv_queue = []

eps = 0.01

pulses = []
beat_directions = [ L, R ]

raylibpy.set_target_fps(60)
raylibpy.init_window(800, 400, 'leds')

while not raylibpy.is_window_ready():
    time.sleep(0.1)

beat_idx = 0
#next_beat = beat_times[beat_idx]
raylibpy.set_target_fps(60)
play_song(filename)
while not raylibpy.window_should_close():

    # get times
    music_pos = music_time()
    ft = raylibpy.get_frame_time()
    tt = raylibpy.get_time() # + ft
        
    board.reset_leds()

    s_idx = int((music_pos / dur) * s_width)
    totals = []

    a = 5 # don't change this
    # stop
    st = (s_end_pow - s_start_pow + 1) * a
    # for each frequency subdivision
    for freq_div in range(s_start_pow, st):
        b = -1
        t = -1
        if freq_div < s_start_pow + s_start_pow:
            step = freq_div - s_start_pow
            if step == 0:
                b = 0
                t = 3
            elif step == 1:
                b = 3
                t = 8
            elif step == 2:
                b = 8
                t = 16
            elif step == 3:
                b = 16
                t = 32
            elif step == 4:
                b = 32
                t = 64
            else:
                print(freq_div - s_start_pow)
                assert(False)
        else:           
            cur_pow = freq_div / a + s_start_pow - 1
            #print("cur_pow: ", cur_pow)
            # bottom value
            b = pow(2, cur_pow)
            # top value
            t = pow(2, cur_pow + (1.0 / a))

        # bottom index
        b_idx = math.floor(b / max_freq * s_height) 
        # top index 
        t_idx = math.ceil(t / max_freq * s_height)
        # print("b: ", b, ", t: ", t)
        # print("b_idx: ", b_idx, ", t_idx ", t_idx)
        total = 0
        for freq_idx in range(b_idx, t_idx):
            val = spectro[freq_idx][s_idx]
            total = total + val
        avg = total / (1.0 * t_idx - b_idx) + max_db

        totals.append(avg)

    for x in range(len(totals)):
        height = int(round(totals[x] / 3))
        for y in range(height):
            idx = 94 + x * h - y
            board.leds[idx].full()

    """
    percents = []
    t = 0
    for i in totals:
        t = t + i
    for i in totals:
        num = 1.0 * i / t
        percents.append(num)
    
    
    for x in range(len(percents)):
        height = int(round((percents[x] * 200)))
        #print(height)
        for y in range(height):
            idx = 94 + x * h - y
            board.leds[idx].full()

    """

    """
    c_idx = int((music_pos / dur) * c_cnt)
    for pitch in range(len(chroma)):
        val = chroma[pitch][c_idx]
        height = int(val * 12)
        
        mid_idx = 174 + pitch * h
        for disp in range(height):
            cur_idx = mid_idx - disp
            board.leds[cur_idx].full()
    """

    """
    # get wv val
    wv_val = abs(int(wv[int(music_pos * sr)] / wv_step))
    wv_queue.insert(0, wv_val)    
    # apply waveform  
    board.draw_amplitude_mirror(wv_queue)
    # clip queue
    if(len(wv_queue) > w / 2):
        wv_queue.pop(len(wv_queue) - 1)

    # check beats
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

    #board.update_leds(ft)   
    """

    # draw
    raylibpy.begin_drawing()
    raylibpy.clear_background(raylibpy.BLACK)
    board.draw_leds()

    txt = "{:.2f} s".format(music_pos)
    raylibpy.draw_text(txt, 720, 20, 20, raylibpy.GREEN)

    raylibpy.end_drawing()

raylibpy.close_window()