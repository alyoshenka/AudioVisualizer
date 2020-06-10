import raylibpy

from boardled import BoardLED

class LightBoard():

    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.dot_size = 7
        self.offset = 25

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

    # reset all leds alpha = 0
    def reset_leds(self):
        for led in self.leds:
            led.color.a = 0
            


        