import math
from random import random, randint
from time import sleep

import pygame
from pygame.rect import Rect    # Shorthand
from pygame._sdl2 import Window

pygame.init()
WIN_WIDTH = 465; WIN_HEIGHT = 350			# Same dimensions as the Scratch iframe

score : int = 0

def random_number(min : float, max : float) -> float:
	return random() * (max-min) + min		# random() returns a result between 0 and 1