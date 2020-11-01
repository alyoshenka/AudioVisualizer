from defines import *
from utils import *

width = f_cols * pix_size
height = f_rows * pix_size 

# convert decibel values to (index, color) array
def dbs_to_board_data(dbs, w=32, h=8):
    data = []

    for i in range(len(dbs)):
        db = dbs[i]
        column = i
        color = lerp_color(db)
        cnt = math.ceil(db / (DB / h))
        base = h * column + (h - 1)
        for j in range(cnt):
            idx = base - j
            data.append([idx, color])

    return data

# dbs: array of decibel values (0-80)
# draw color/height bars
def draw_bars(dbs):
    for i in range(len(dbs)):
        db = dbs[i]
        x = i * pix_size
        y = height - (round(db / (DB / f_rows)) * pix_size)
        #y= 160 - db * 2
        #y=0
        w = pix_size
        h = height - y
        #h=160
        c = lerp_color(db)
        raylibpy.draw_rectangle(x, y, w, h, c)

# data: an array of (index, color) pairs
# (not taking into account reversal)
# emulate display board
def display_on_board(data, w=32, h=8, s=pix_size/2, o=pix_size):
    
    # return (x, y) from index
    def get_coords(idx):
        col = int(idx / h)
        row = idx % h
        x = col * o + o / 2
        y = row * o + o / 2
        return x, y

    # dat = [idx, color]
    # draw "light"
    def draw_led(dat):
        x, y = get_coords(dat[0])
        raylibpy.draw_circle(x, y, s, dat[1])

    for dat in data:
        draw_led(dat)   

class Display:

    def __init__(self):
        raylibpy.init_window(width, height, song_name)
        raylibpy.set_target_fps(60)

    def draw(self):
        raylibpy.begin_drawing()
        raylibpy.clear_background(raylibpy.BLACK)

        t = get_time()
        if t < dur:
            dbs = get_dbs(spec, t, bar_freqs, time_index_ratio, freq_index_ratio)
            b_data = dbs_to_board_data(dbs)
            display_on_board(b_data)

        raylibpy.end_drawing()

    
