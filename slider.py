import pygame
import sys
from pygame.locals import *

# Initialize Pygame
pygame.init()
pygame.mixer.init()

# Set up the display
screen = pygame.display.set_mode((640, 480))
pygame.display.set_caption('Volume Slider Example')

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)

# Slider settings
slider_x = 305
slider_y = 120
slider_width = 200
slider_height = 20
slider_pos = 100  # Starting position

# Load and play music
# pygame.mixer.music.load('Sound/crunch.wav')
# pygame.mixer.music.play(-1)  # Loop music indefinitely

def draw_slider(screen, x, y, width, height, pos):
    pygame.draw.rect(screen, WHITE, (x, y, width, height))
    pygame.draw.rect(screen, RED, (x + pos, y, 10, height))

def main():
    running = True
    global slider_pos
    while running:
        for event in pygame.event.get():
            if event.type == QUIT:
                running = False
            elif event.type == MOUSEBUTTONDOWN:
                if event.pos[0] > slider_x and event.pos[0] < slider_x + slider_width and event.pos[1] > slider_y and event.pos[1] < slider_y + slider_height:
                    slider_pos = event.pos[0] - slider_x
                    volume = slider_pos / slider_width
                    pygame.mixer.music.set_volume(volume)

        # Update the display
        screen.fill(BLACK)
        draw_slider(screen, slider_x, slider_y, slider_width, slider_height, slider_pos)
        pygame.display.flip()

    pygame.quit()
    sys.exit()

if __name__ == '__main__':
    main()