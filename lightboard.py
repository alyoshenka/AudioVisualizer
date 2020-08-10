import raylibpy
import math

from boardled import BoardLED
from pulse import M as M
from spectrogram import spectro_size, max_db, \
    freq_subdivides, freq_total


class LightBoard():
    """a board of lights"""

    # width: number of dot columns
    # height: number of dot rows
    # dot_size: dot radius
    # offset: distance between dot centers
    def __init__(self, width, height, dot_size=7, offset=25):
        self.width = width
        self.height = height
        self.dot_size = dot_size
        self.offset = offset
        self.count = self.width * self.height # number of dots

        self.pulses = []
        self.leds = []
        self.create_leds()

    def create_leds(self):
        """initialize led array"""
        count = self.width * self.height
        for i in range(count):
            led = BoardLED(i)
            self.leds.append(led)      

    def update_leds(self, delta_time):
        for led in self.leds:
            led.update(delta_time)
    
    def draw_leds(self):
        count = self.width * self.height
        for i in range(count):
            x = i // self.height * self.offset + self.offset / 2
            y = i % self.height * self.offset + self.offset / 2
            self.leds[i].draw(x, y, self.dot_size)

    def draw_amplitude_mirror(self, wv_queue):
        """draw music amplitude mirrored across vertical axis"""
        # MAGIC NUMBER BAD
        for x in range(min(len(wv_queue), int(self.width/ 2))):
            x_left = 991 - x * self.height
            x_right = 1023 + x * self.height
            for i in range(wv_queue[x]):
                self.leds[x_left - i].full()
                self.leds[x_right - i].full()
            
    def draw_beat_pulse(self, pulses, pulse_dirs, time):
        """draw pulsing beat"""
        for p in pulses:
            for d in pulse_dirs:
                offset = p.offset_dict(time, 255, self.width, self.height, d)
                for key in offset:
                    if key >= 0 and key < self.count:
                        # constrain to max rgb value
                        a = min(M, self.leds[key].color.a + offset.get(key))
                        self.leds[key].color.a = a

    # reset all leds alpha = 0
    def reset_leds(self):
        for led in self.leds:
            led.empty()

    def set_color_clear(self, color):
        """set all leds to one color, with alpha = 0"""
        color.a = 0
        for led in self.leds:
            led.color = raylibpy.Color(color)


    def set_rainbow_16(self):
        """set leds to rainbow based on height"""
        for i in range(len(self.leds)):
            row = i % self.height
            comp = self.height / 8
            c = raylibpy.GRAY
            if row < comp * 3:
                c = raylibpy.PURPLE
            elif row < comp * 4:
                c = raylibpy.RED
            elif row < comp * 5:
                c = raylibpy.ORANGE
            elif row < comp * 6:
                c = raylibpy.YELLOW
            elif row < comp * 7:
                c = raylibpy.GREEN
            elif row < comp * 8:
                c = raylibpy.BLUE
            else:
                c = raylibpy.PURPLE
            c = raylibpy.Color(c)
            c.a = 0
            self.leds[i].color = c
        
    def draw_spectrogram(self, spec_col):
        """draws frequency view from given column (time based)"""

        # frequency intensity
        totals = []
        
        # get average for each frequency subdivide
        for i in range(len(freq_subdivides) - 1):
            low = freq_subdivides[i]
            high = freq_subdivides[i+1]

            min_idx = math.floor(1.0 * low / freq_total * spectro_size)
            max_idx = math.ceil(1.0 * high / freq_total * spectro_size)

            if(max_idx > len(spec_col)):
                max_idx = len(spec_col) - 1

            diff = max_idx - min_idx
            sub_total = 0
            for i in range(min_idx, max_idx):
                sub_total = sub_total + spec_col[i]
            val = sub_total / diff + max_db
            totals.append(val)

        # MAGIC NUMBERS BAD
        # apply average towards graph height
        for x in range(len(totals)):
            height = int(round(totals[x] / 3))
            for y in range(height):
                idx = 94 + x * self.height - y
                self.leds[idx].full()

    def draw_amplitude(self, vol_col):
        """draws amplitude (volume) view from specific column"""
        return False

    def waveform_multiplier(self, max_wv):
        """returns multiplier for waveform height"""

        # NOT THE BEST WAY TO DO THIS
        return self.height / max_wv
        