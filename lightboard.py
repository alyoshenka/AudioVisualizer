import raylibpy

from boardled import BoardLED
from pulse import M as M

class LightBoard():
    """a board of lights"""

    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.dot_size = 7
        self.offset = 25
        self.count = self.width * self.height

        self.pulses = []
        self.leds = []
        self.create_leds()

    def create_leds(self):
        count = self.width * self.height
        print(count)
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
        for x in range(min(len(wv_queue), int(self.width/ 2))):
            x_left = 251 - x * self.height
            x_right = 267 + x * self.height
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
            


        