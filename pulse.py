unit = 256
M = unit - 1

N = -1 # none
U = 1 # up
D = 2 # down
L = 3 # left
R = 4 # right

class Pulse:
    """generic linear fade pulse"""

    # fade speed of one means brightness 
    # fades 256 in 1 second
    # not currently correct ^


    def __init__(self, fade_amount=10, start_time=0, jump_time=-1, jump_fade=15):
        self.fade_amount = fade_amount # how much to fade each cycle
        self.start_time = start_time # fade start time
        self.jump_time = jump_time # time to next index
        self.jump_fade = jump_fade # amount to fade each jump

    def reset(self, new_time):
        """reset time to take alpha from"""
        self.start_time = new_time

    def brightness(self, time):
        """alpha value as given time"""
        delta_time = time - self.start_time
        # return max(0, unit - (self.fade_speed * unit) * delta_time)
        return 255

    def offset_dict(self, elapsed_time, idx, width, height, direction):
        """alpha offsets in given direction
            self inclusive"""

        time = elapsed_time - self.start_time

        # if no jump
        # return self brightness
        if self.jump_time < 0:
            print('no jump')
            return { idx: self.brightness(time) }
        
        # if pulse = line
        # return line of brightness
        if self.jump_time == 0:
            print('line')
            a = self.brightness(time)
            ret = { idx: a }
            return ret
            
         # alpha of start index
        start_a = M - self.fade_amount * int(time / self.jump_time)
        # length of pulse
        length = int(time / self.jump_time) + 1

        ret = {}
        
        # calculate all alphas
        for i in range(length):
            # index to calculate alpha
            if direction == L:
                cur_idx = idx - i * height
            elif direction == R: 
                cur_idx = idx + i * height
            elif direction == U:
                cur_idx = idx - i
            elif direction == D:
                cur_idx = idx + i
            else:
                cur_idx = idx

            # alpha value
            cur_a = start_a - i * self.jump_fade
            if cur_a >= 0 and cur_a < width * height:
                ret[cur_idx] = cur_a

        return ret

            

