import raylibpy

def display_waveform_dic(wv):
    w = 800.0
    h = 400

    cnt = len(wv)
    x = w / cnt

    m = 0
    for key in wv:
        n = abs(wv.get(key))
        if n > m:
            m = n
    
    y = 150.0 / m

    raylibpy.init_window(w, h, 'win')

    raylibpy.begin_drawing()
    raylibpy.clear_background(raylibpy.RAYWHITE)

    for key in wv:
        num = wv.get(key)

        X = x * key
        Y = num * y + h / 2

        raylibpy.draw_circle(X, Y, 1, raylibpy.BLUE)

    raylibpy.end_drawing()

    while not raylibpy.window_should_close():
        continue
    
    raylibpy.close_window()

def display_waveform(wv):

    w = 800.0
    h = 400

    cnt = len(wv)
    x = w / cnt

    m = 0
    for num in wv:
        n = abs(num)
        if n > m:
            m = n
    
    y = 40.0 / m

    raylibpy.init_window(w, h, 'win')

    raylibpy.begin_drawing()
    raylibpy.clear_background(raylibpy.RAYWHITE)

    for i in range(cnt - 1):
        num = wv[i]
        num2 = wv[i + 1]

        X = x * i
        Y = num * y + h / 2

        X2 = x * (i+1)
        Y2 = num2 * y + h / 2

        raylibpy.draw_line(X, Y, X2, Y2, raylibpy.BLUE)

    raylibpy.end_drawing()

    while not raylibpy.window_should_close():
        continue
    
    raylibpy.close_window()