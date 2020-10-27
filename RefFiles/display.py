# beat tracking example
# https://librosa.github.io/librosa/tutorial.html


#from __future__ import print_function
import librosa
import librosa.display

import matplotlib.pyplot as plt

import raylibpy
from raylibpy import RAYWHITE, BLUE

def lib_disp(wv, sr):
    # monophobic s
    plt.figure()
    plt.subplot(2, 1, 1)
    librosa.display.waveplot(wv, sr=sr)
    plt.title('Mono')

    """
    y_harm, y_perc = librosa.effects.hpss(y)
    plt.subplot(2, 1, 2)
    librosa.display.waveplot(y_harm, sr=sr, alpha=0.25)
    librosa.display.waveplot(y_perc, sr=sr, color='r', alpha=0.5)
    plt.title('Harmonic + Percussive')
    plt.tight_layout()
    """

    plt.show()

def ray_disp(wv):   
    raylibpy.init_window(1000, 400, 'win')

    raylibpy.begin_drawing()
    raylibpy.clear_background(RAYWHITE)
    for i in range(40000):
        x = i / 40
        y = wv[i] * 400 + 200
        raylibpy.draw_circle(x, y, 1, BLUE)
        #print(x, ", ", y)
    raylibpy.end_drawing()
    while not raylibpy.window_should_close():
        continue
    raylibpy.close_window()
