from vector import *

window = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))

WINDOW_VECTOR : Vector = Vector(WIN_WIDTH, WIN_HEIGHT); SCREEN_CENTER : Vector = WINDOW_VECTOR / 2

pygame.display.set_caption("Shooting training.")    # The window's title