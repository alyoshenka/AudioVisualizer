import matplotlib.pyplot as plt
import numpy as np
import librosa
import librosa.display
import pygame
import pygame.mixer as pymixer
import math

import raylibpy

audio = [
    'Music/Little Dark Age.wav',
    'Music/Strobe.wav',
    'Music/There Might Be Coffee.wav'
]

DB = 80 # decibel range/offset

song_name = audio[0]
dur = 60 # audio duration (s)

# y = audio time series
# sr = sampling rate of y
y, sr = librosa.load(song_name, duration=dur)
stft = np.abs(librosa.stft(y, hop_length=512, n_fft=2048*4))
spec = librosa.amplitude_to_db(stft, ref=np.max)
freqs = librosa.core.fft_frequencies(n_fft=2048*4)
times = librosa.core.frames_to_time(np.arange(spec.shape[1]), sr=sr, hop_length=512, n_fft=2048*4)
time_index_ratio = len(times) / times[len(times)-1]
freq_index_ratio = len(freqs) / freqs[len(freqs)-1]

f_max = 6000 # maximum frequency sampled
f_min = 100 # minimum frequency sampled
f_cols = 32 # frequency columns
f_rows = 8
pix_size = 20
f_step = math.ceil((f_max - f_min) / f_cols)
bar_freqs = np.arange(f_min, f_max, f_step)

width = f_cols * pix_size
height = f_rows * pix_size


# display spectrogram of song
def display_song(spec, song_name):
    librosa.display.specshow(spec, y_axis='log', x_axis='time')
    plt.title(song_name)
    plt.colorbar(format='%+2.0f dB')
    plt.tight_layout()
    plt.show()

# decibel volume, (-80, 0)
def get_decibel(spec, time, tir, freq, fir):
    return spec[int(freq * fir)][int(time * tir)]

# song time
def get_time():
    return pygame.time.get_ticks() / 1000

# return ca -> cb with t%
def color_lerp(ca, cb, t):
    r = ca.r * (1-t) + cb.r * t 
    g = ca.g * (1-t) + cb.g * t 
    b = ca.b * (1-t) + cb.b * t 
    return raylibpy.Color(r, g, b, 255)

# return color given volume
def lerp_color(db):
    t = db % 10 / 10
    if db == 0:
        return raylibpy.Color(raylibpy.BLACK)
    elif db < 10:
        return color_lerp(raylibpy.WHITE, raylibpy.BLUE, t)
    elif db < 20:
        return color_lerp(raylibpy.BLUE, raylibpy.GREEN, t)
    elif db < 30:
        return color_lerp(raylibpy.GREEN, raylibpy.YELLOW, t)
    elif db < 40:
        return color_lerp(raylibpy.YELLOW, raylibpy.ORANGE, t)
    elif db < 50:
        return color_lerp(raylibpy.ORANGE, raylibpy.RED, t)
    elif db < 60:
        return color_lerp(raylibpy.RED, raylibpy.PURPLE, t)
    else:
        return raylibpy.Color(raylibpy.PURPLE)

# return frequency-decibel values
def get_dbs(spec, t, bar_freqs, tir, fir):
    dbs = []
    for i in range(len(bar_freqs)):
        f = bar_freqs[i]
        db = get_decibel(spec, t, tir, f, fir) + DB
        dbs.append(db)
    return dbs

# convert decibel values to (index, color) array
def dbs_to_board_data(dbs, w=32, h=8):
    data = []

    for i in range(len(dbs)):
        db = dbs[i]
        column = i
        color = lerp_color(db)
        cnt = math.ceil(db / (DB / h))
        base = h * column + (h - 1)
        for j in range(cnt):
            idx = base - j
            data.append([idx, color])

    return data

# dbs: array of decibel values (0-80)
# draw color/height bars
def draw_bars(dbs):
    for i in range(len(dbs)):
        db = dbs[i]
        x = i * pix_size
        y = height - (round(db / (DB / f_rows)) * pix_size)
        #y= 160 - db * 2
        #y=0
        w = pix_size
        h = height - y
        #h=160
        c = lerp_color(db)
        raylibpy.draw_rectangle(x, y, w, h, c)

# data: an array of (index, color) pairs
# (not taking into account reversal)
# emulate display board
def display_on_board(data, w=32, h=8, s=pix_size/2, o=pix_size):
    
    # return (x, y) from index
    def get_coords(idx):
        col = int(idx / h)
        row = idx % h
        x = col * o + o / 2
        y = row * o + o / 2
        return x, y

    # dat = [idx, color]
    # draw "light"
    def draw_led(dat):
        x, y = get_coords(dat[0])
        raylibpy.draw_circle(x, y, s, dat[1])

    for dat in data:
        draw_led(dat)
    

# main application function
def main():
    #display_song(spec, song_name)

    pymixer.init()
    pymixer.music.load(song_name)
    pymixer.music.play()

    raylibpy.init_window(width, height, song_name)
    raylibpy.set_target_fps(60)

    pygame.init()

    t = get_time()
    while not raylibpy.window_should_close() and t < dur:

        raylibpy.begin_drawing()
        raylibpy.clear_background(raylibpy.BLACK)

        t = get_time()
        if t < dur:
            dbs = get_dbs(spec, t, bar_freqs, time_index_ratio, freq_index_ratio)
            b_data = dbs_to_board_data(dbs)
            display_on_board(b_data)

        raylibpy.end_drawing()


main()
