import raylibpy

CLEAR = raylibpy.Color(0, 0, 0, 0)

class BoardLED:

    def __init__(self, index, color=CLEAR):
        self.index = index
        self.color = color
        self.fade_speed = 0
    
    def should_draw(self):
        return (self.color.r > 0 or self.color.g > 0 or self.color.b > 0) and self.color.a > 0

    def fade(self, amount):
        self.color.a = self.color.a - amount
        if self.color.a < 0:
            self.color.a = 0

    def update(self, delta_time):
        if self.fade_speed > 0:
            self.fade(self.fade_speed * delta_time)

    def draw(self, x, y, size):
        if self.should_draw():
            raylibpy.draw_circle(x, y, size, self.color)
    
    def pulse(self, pulse):
        self.color = raylibpy.Color(pulse.color)
        self.fade_speed = pulse.fade_speed # this should be designed differently


