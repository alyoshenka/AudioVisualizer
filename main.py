import matplotlib.pyplot as plt
import numpy as np
import librosa
import librosa.display
import pygame
import pygame.mixer as pymixer

import raylibpy


def display_song(spec, song_name):
    librosa.display.specshow(spec, y_axis='log', x_axis='time')
    plt.title(song_name)
    plt.colorbar(format='%+2.0f dB')
    plt.tight_layout()
    plt.show()


def get_decibel(spec, time, tir, freq, fir):
    return spec[int(freq * fir)][int(time * tir)]


def get_time():
    return pygame.time.get_ticks() / 1000


def draw_bars(spec, t,  bar_freqs, freqs, tir, fir):
    for i in range(len(bar_freqs)):
        f = bar_freqs[i]
        db = get_decibel(spec, t, tir, f, fir) + 80 
        x = i * 10
        y = 400 - db * 2
        w = 10
        h = db * 2
        #print(db, x, y, w, h)
        raylibpy.draw_rectangle(x, y, w, h, raylibpy.GREEN)


def main():
    song_name = 'Music/Little Dark Age.wav'
    dur = 45
    # y = audio time series
    # sr = sampling rate of y
    y, sr = librosa.load(song_name, duration=dur)
    stft = np.abs(librosa.stft(y, hop_length=512, n_fft=2048*4))
    spec = librosa.amplitude_to_db(stft, ref=np.max)
    freqs = librosa.core.fft_frequencies(n_fft=2048*4)
    times = librosa.core.frames_to_time(np.arange(spec.shape[1]), sr=sr, hop_length=512, n_fft=2048*4)
    time_index_ratio = len(times) / times[len(times)-1]
    freq_index_ratio = len(freqs) / freqs[len(freqs)-1]

    bar_freqs = np.arange(100, 8000, 100)

    #display_song(spec, song_name)

    pymixer.init()
    pymixer.music.load(song_name)
    pymixer.music.play()

    raylibpy.init_window(800, 400, song_name)

    pygame.init()

    while not raylibpy.window_should_close():

        raylibpy.begin_drawing()
        raylibpy.clear_background(raylibpy.BLACK)

        t = get_time()
        if t < dur:
            draw_bars(spec, t, bar_freqs, freqs, time_index_ratio, freq_index_ratio)

        raylibpy.end_drawing()


main()
