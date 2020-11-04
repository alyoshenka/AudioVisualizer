import pyaudio
import struct
import numpy as np
from scipy.fftpack import fft
import raylibpy


CHUNK = 1024 * 4 # audio samples / frame
FORMAT = pyaudio.paInt16 # something about bytes
CHANNELS = 1
RATE = 44100 # samples / second

p = pyaudio.PyAudio()
stream = p.open(
    format=FORMAT,
    channels=CHANNELS,
    rate=RATE,
    input=True,
    output=True,
    frames_per_buffer=CHUNK
)

x = np.arange(0, 2 * CHUNK, 2)
x_fft = np.linspace(0, RATE, CHUNK)

raylibpy.init_window(1004, 300, 'raylib vis')
raylibpy.set_target_fps(60)

while not raylibpy.window_should_close():

    
    data = stream.read(CHUNK)
    # convert
    # len data = 2 * len(chunk)
    # wrap
    data_int = struct.unpack(str(2 * CHUNK) + 'B', data)
    data_np = np.array(data_int, dtype='b')[1::2] + 128
    y_fft = fft(data_int)
    y_data = np.abs(y_fft[0:CHUNK]) * 2 / (256 * CHUNK)  
        

    raylibpy.begin_drawing()
    raylibpy.clear_background(raylibpy.BLACK)

    for i in range(10, len(y_data) // 8):
        val = y_data[i]
        w = 2    
        x = 2 * int(i) - 10
        h = val * 500
        y = 300 - h       
        raylibpy.draw_rectangle(x, y, w, h, raylibpy.WHITE)

        raylibpy.draw_rectangle(62, 290, 1, 10, raylibpy.WHITE)

        # this breaks the display
        #raylibpy.draw_text(str(raylibpy.get_fps()) + ' fps', 750, 10, 15, raylibpy.DARKGREEN)

        #print(val, x, y, w, h)

    raylibpy.end_drawing()

raylibpy.close_window()