import pyaudio
import struct
import numpy as np
import matplotlib.pyplot as plt
from scipy.fftpack import fft

import time


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

fig, (ax, ax2) = plt.subplots(2, figsize=(15, 8))
ax.set_title('AUDIO WAVEFORM')
ax.set_xlabel('samples')
ax.set_ylabel('volume')

x = np.arange(0, 2 * CHUNK, 2)
x_fft = np.linspace(0, RATE, CHUNK)

line, = ax.plot(x, np.random.rand(CHUNK), '-', lw=2)
line_fft, = ax2.semilogx(x_fft, np.random.rand(CHUNK), '-', lw=2)

ax.set_ylim(0, 255)
ax.set_xlim(0, CHUNK) 
ax2.set_xlim(20, RATE / 4) 
ax2.set_ylim(0, 0.5)

plt.show(block=False)

start_time = time.time()
frames = 0


import msvcrt
while not (msvcrt.kbhit() and msvcrt.getch() == chr(27).encode()):
    try:
        data = stream.read(CHUNK)

        # convert
        # len data = 2 * len(chunk)
        # wrap
        data_int = struct.unpack(str(2 * CHUNK) + 'B', data)
        data_np = np.array(data_int, dtype='b')[1::2] + 128

        

        line.set_ydata(data_np)
        y_fft = fft(data_int)
        y_data = np.abs(y_fft[0:CHUNK]) * 2 / (256 * CHUNK)
        
        line_fft.set_ydata(y_data)

        

        fig.canvas.draw()
        fig.canvas.flush_events()
    except:
        i = 0

    frames = frames + 1

end_time = time.time()
elapsed_time = end_time - start_time

fps = frames / elapsed_time
print('{0} / {1} = {2} fps'.format(frames, elapsed_time, fps))

