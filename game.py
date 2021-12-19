import contextlib
import os
from conts import WIDTH, HEIGHT
with contextlib.redirect_stdout(None):
    import pygame

from client_view import ClientView

while True:
    name = input('Please enter your name: ')
    if 0 < len(name) < 20:
        client_view = ClientView(name)
        break
    else:
        print('Error, name only 1 to 19 chars')

os.environ['SDL_VIDEO_WINDOW_POS'] = '%d,%d' % (0, 30)

window = pygame.display.set_mode((WIDTH, HEIGHT))
client_view.set_client_window(window)

client_view.main()
