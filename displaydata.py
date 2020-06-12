import raylibpy

import matplotlib.pyplot as plt
import librosa
import librosa.display
import numpy as np

# used for debugging purposes to visualize data

def display_waveform_dic(wv):
    w = 800.0
    h = 400

    cnt = len(wv)
    x = w / cnt

    m = 0
    for key in wv:
        n = abs(wv.get(key))
        if n > m:
            m = n
    
    y = 150.0 / m

    raylibpy.init_window(w, h, 'win')

    raylibpy.begin_drawing()
    raylibpy.clear_background(raylibpy.RAYWHITE)

    for key in wv:
        num = wv.get(key)

        X = x * key
        Y = num * y + h / 2

        raylibpy.draw_circle(X, Y, 1, raylibpy.BLUE)

    raylibpy.end_drawing()

    while not raylibpy.window_should_close():
        continue
    
    raylibpy.close_window()

def display_waveform(wv):

    w = 800.0
    h = 400

    cnt = len(wv)
    x = w / cnt

    m = 0
    for num in wv:
        n = abs(num)
        if n > m:
            m = n
    
    y = 40.0 / m

    raylibpy.init_window(w, h, 'win')

    raylibpy.begin_drawing()
    raylibpy.clear_background(raylibpy.RAYWHITE)

    for i in range(cnt - 1):
        num = wv[i]
        num2 = wv[i + 1]

        X = x * i
        Y = num * y + h / 2

        X2 = x * (i+1)
        Y2 = num2 * y + h / 2

        raylibpy.draw_line(X, Y, X2, Y2, raylibpy.BLUE)

    raylibpy.end_drawing()

    while not raylibpy.window_should_close():
        continue
    
    raylibpy.close_window()

# NOT MY CODE, RIPPED DIRECTLY FROM LIBROSA 
def all_specshows(y, sr):
    # Visualize an STFT power spectrum
    plt.figure(figsize=(12, 8))
    D = librosa.amplitude_to_db(np.abs(librosa.stft(y)), ref=np.max)
    plt.subplot(4, 2, 1)
    librosa.display.specshow(D, y_axis='linear')
    plt.colorbar(format='%+2.0f dB')
    plt.title('Linear-frequency power spectrogram')

    # Or on a logarithmic scale
    plt.subplot(4, 2, 2)
    librosa.display.specshow(D, y_axis='log')
    plt.colorbar(format='%+2.0f dB')
    plt.title('Log-frequency power spectrogram')

    # Or use a CQT scale
    CQT = librosa.amplitude_to_db(np.abs(librosa.cqt(y, sr=sr)), ref=np.max)
    plt.subplot(4, 2, 3)
    librosa.display.specshow(CQT, y_axis='cqt_note')
    plt.colorbar(format='%+2.0f dB')
    plt.title('Constant-Q power spectrogram (note)')
    plt.subplot(4, 2, 4)
    librosa.display.specshow(CQT, y_axis='cqt_hz')
    plt.colorbar(format='%+2.0f dB')
    plt.title('Constant-Q power spectrogram (Hz)')

    # Draw a chromagram with pitch classes
    C = librosa.feature.chroma_cqt(y=y, sr=sr)
    plt.subplot(4, 2, 5)
    librosa.display.specshow(C, y_axis='chroma')
    plt.colorbar()
    plt.title('Chromagram')

    # Force a grayscale colormap (white -> black)
    plt.subplot(4, 2, 6)
    librosa.display.specshow(D, cmap='gray_r', y_axis='linear')
    plt.colorbar(format='%+2.0f dB')
    plt.title('Linear power spectrogram (grayscale)')

    # Draw time markers automatically
    plt.subplot(4, 2, 7)
    librosa.display.specshow(D, x_axis='time', y_axis='log')
    plt.colorbar(format='%+2.0f dB')
    plt.title('Log power spectrogram')

    # Draw a tempogram with BPM markers
    plt.subplot(4, 2, 8)
    Tgram = librosa.feature.tempogram(y=y, sr=sr)
    librosa.display.specshow(Tgram, x_axis='time', y_axis='tempo')
    plt.colorbar()
    plt.title('Tempogram')
    plt.tight_layout()

    plt.show()

def chromas(y, sr):
    plt.figure()
    C = librosa.feature.chroma_cqt(y=y, sr=sr)
    tempo, beat_f = librosa.beat.beat_track(y=y, sr=sr, trim=False)
    beat_f = librosa.util.fix_frames(beat_f, x_max=C.shape[1])
    Csync = librosa.util.sync(C, beat_f, aggregate=np.median)
    beat_t = librosa.frames_to_time(beat_f, sr=sr)

    ax1 = plt.subplot(2,1,1)
    librosa.display.specshow(C, y_axis='chroma', x_axis='time')
    plt.title('Chroma (linear time)')

    ax2 = plt.subplot(2,1,2, sharex=ax1)
    librosa.display.specshow(Csync, y_axis='chroma', x_axis='time', x_coords=beat_t)
    plt.title('Chroma (beat time)')

    plt.tight_layout()
    plt.show()