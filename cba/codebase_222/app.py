import pygame
import random
import sys

# Initialize Pygame
pygame.init()

# Constants
WIDTH, HEIGHT = 800, 600
GROUND_HEIGHT = 50
MOLE_WIDTH, MOLE_HEIGHT = 50, 50
FPS = 60

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BROWN = (165, 42, 42)

# Setup display
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Whack-a-Mole")

# Game variables
clock = pygame.time.Clock()
moles = []
score = 0

# Main game loop
running = True
while running:
    clock.tick(FPS)
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    
    screen.fill(BROWN)
    
    pygame.display.flip()

pygame.quit()
sys.exit()
