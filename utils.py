import librosa
import librosa.display
import matplotlib.pyplot as plt
import raylibpy
import math
import numpy as np
import pygame
import pygame.mixer as pymixer

from defines import *

# y = audio time series
# sr = sampling rate of y
y, sr = librosa.load(song_name, duration=dur)
stft = np.abs(librosa.stft(y, hop_length=512, n_fft=2048*4))
spec = librosa.amplitude_to_db(stft, ref=np.max)
freqs = librosa.core.fft_frequencies(n_fft=2048*4)
times = librosa.core.frames_to_time(np.arange(spec.shape[1]), sr=sr, hop_length=512, n_fft=2048*4)
time_index_ratio = len(times) / times[len(times)-1]
freq_index_ratio = len(freqs) / freqs[len(freqs)-1]


f_step = math.ceil((f_max - f_min) / f_cols)
bar_freqs = np.arange(f_min, f_max, f_step)



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

# get exit condition, dependent on os
def should_continue():
    return not raylibpy.window_should_close()