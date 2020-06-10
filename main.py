
import raylibpy
import time

from loaddata import waveform, beats, play_song, music_time
from lightboard import LightBoard
from pulse import *


filename = "Music/Little Dark Age.wav"

wv, sr = waveform(filename)
beat_times, tempo = beats(wv, sr)

# calculate waveform data
max_wv = 0
for num in wv:
    max_wv = max(max_wv, abs(num))
print("max_wv: ", max_wv)
wv_step = max_wv / 12.0

w = 32
h = 16
cnt = w * h
board = LightBoard(w, h)
for i in range(len(board.leds)):
    row = i % h
    c = raylibpy.Color(raylibpy.GRAY)
    if row < 2:
        c = raylibpy.Color(raylibpy.PURPLE)
    elif row < 4:
        c = raylibpy.Color(raylibpy.RED)
    elif row < 6:
        c = raylibpy.Color(raylibpy.ORANGE)
    elif row < 8:
        c = raylibpy.Color(raylibpy.YELLOW)
    elif row < 10:
        c = raylibpy.Color(raylibpy.GREEN)
    elif row < 12:
        c = raylibpy.Color(raylibpy.BLUE)
    elif row == 15:
        c = raylibpy.Color(raylibpy.PURPLE)
    c.a = 0
    board.leds[i].color = c
wv_queue = []

eps = 0.01

pulses = []
beat_directions = [ L, R ]

raylibpy.set_target_fps(60)
raylibpy.init_window(800, 400, 'leds')

while not raylibpy.is_window_ready():
    time.sleep(0.1)

beat_idx = 0
#next_beat = beat_times[beat_idx]
raylibpy.set_target_fps(60)
play_song(filename)
while not raylibpy.window_should_close():

    # get times
    music_pos = music_time()
    tt = raylibpy.get_time()
    ft = raylibpy.get_frame_time()
        
    board.reset_leds()

    # get wv val
    wv_val = abs(int(wv[int(music_pos * sr)] / wv_step))
    wv_queue.insert(0, wv_val)
    
    # apply waveform
    
    for X in range(min(len(wv_queue), int(w / 2))):
        x1 = 251 - X * h # 12th row, left
        x2 = 267 + X * h # 12th row, right
        val = wv_queue[X]
        for i in range(val):
            board.leds[x1 - i].color.a = 255
            board.leds[x2 - i].color.a = 255

        if(len(wv_queue) > w / 2):
            wv_queue.pop(len(wv_queue) - 1)

    """
    # check beats
    if music_pos <= next_beat and music_pos + ft + eps > next_beat:
        p = Pulse(start_time=tt, jump_time=0.01, fade_amount=10, jump_fade=15)
        pulses.append(p)
        beat_idx = beat_idx + 1
        next_beat = beat_times[beat_idx]

    # run pulses
    to_delete = []
    for p in pulses:
        for d in beat_directions:
            offset = p.offset_dict(tt, 255, w, h, d)
            for key in offset:
                if key >= 0 and key < cnt:
                    a = board.leds[key].color.a + offset.get(key)
                    if a > M:
                        a = M
                    board.leds[key].color.a = a

        if tt - p.start_time > 3:
            to_delete.append(p)

    # get rid of old pulses
    for p in to_delete:
        pulses.remove(p)
    """

    #board.update_leds(ft)   

    raylibpy.begin_drawing()
    raylibpy.clear_background(raylibpy.BLACK)

    board.draw_leds()

    raylibpy.end_drawing()
raylibpy.close_window()