import math
from random import random
from time import sleep

import pygame
from pygame.rect import Rect    # Shorthand
from pygame._sdl2 import Window

pygame.init()

WIN_WIDTH = 465; WIN_HEIGHT = 350			# Same dimensions as the Scratch iframe
window = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))

pygame.display.set_caption("Shooting training.")    # The window's title

score : int = 0

def random_number(min : float, max : float) -> float:
	return random() * (max-min) + min		# random() returns a result between 0 and 1