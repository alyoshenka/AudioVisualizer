import pygame
import pygame.mixer as pymixer

from defines import *
from utils import *

import display

import raylibpy


# main application function
def main():
    pymixer.init()
    pymixer.music.load(song_name)
    pymixer.music.play()   

    pygame.init()

    disp = display.Display()

    t = get_time()
    while should_continue() and t < dur:
        disp.draw()
        
if __name__ == '__main__':
    main()
