import numpy as np
import librosa

 # max spectrogram frequency (2^13)
max_freq = 8192 # 4096 (2^12) could be used
# max decibel volume
max_db = 80 
# 2^13 = 8192
end_pow = 13
# 2^5 = 64
sec_pow = 5
# 13 - 5 = 8
subdivides = 16

freq_subdivides = [0, 32, 64, 91, \
    128, 181, 256, 362, 512, 724, 1024, \
    1448, 2048, 2896, 4096, 5793, 8192]
freq_total = 0
for sub in freq_subdivides:
    freq_total = freq_total + sub

# number of values
spectro_size = 1025

class Spectrogram:
    """spectro data for lightboard"""

    def __init__(self, wv):

        # spectrogram (not sure why a_to_db)
        self.graph = librosa.amplitude_to_db(np.abs(librosa.stft(wv)), ref=np.max)
        # number of frequencies (vertical) (1025)
        self.height = len(self.graph)
        # number of frames (horizontal)
        self.width = len(self.graph[0])
        # ?
        self.step = self.height / (1.0 * subdivides)

    

