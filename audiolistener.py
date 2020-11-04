# https://swharden.com/blog/2016-07-19-realtime-audio-visualization-in-python/

import pyaudio
import numpy as np


class AudioListener:
    def __init__(self, chunk=512*8, sr=44100):
        
        self.chunk = chunk # number of data points to read at a time
        self.sr = sr # time resolution of the recording device (Hz)

        self.p=pyaudio.PyAudio() # start the PyAudio class

    def get_audio(self):
        self.stream=self.p.open(format=pyaudio.paFloat32,channels=1,rate=self.sr,input=True,
                frames_per_buffer=self.chunk) #uses default input device

        data = np.frombuffer(self.stream.read(self.chunk),dtype=np.float32)

        return data

    def close(self):
        # close the stream gracefully
        self.stream.stop_stream()
        self.stream.close()
        self.p.terminate()
    
def display_external_audio():
    a = AudioListener()

    import raylibpy

    raylibpy.init_window(1024, 300, 'external audio')
    raylibpy.set_target_fps(60)

    while not raylibpy.window_should_close():

        d = a.get_audio()
        stft = np.abs(librosa.stft(d, n_fft=512, hop_length=1))
        spec = librosa.amplitude_to_db(stft, ref=np.max)

        raylibpy.begin_drawing()
        raylibpy.clear_background(raylibpy.DARKBLUE)
        
        print(0)
        for i in range(len(spec)):
            val = (spec[i][0] + 80)
            
            x = i * 4
            y = 300 - val
            w = 4
            h = val

            print(val)

            raylibpy.draw_rectangle(x, y, w, h, raylibpy.GREEN)
        

        raylibpy.end_drawing()

    a.close()



