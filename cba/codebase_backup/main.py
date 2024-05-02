import pygame
import random

# Initialize Pygame
pygame.init()

# Constants
WIDTH, HEIGHT = 800, 600
GRID_SIZE = 20
GAME_SPEED = 10

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)

# Game Variables
snake = [(WIDTH // 2, HEIGHT // 2)]
direction = (0, 0)
food = (random.randint(0, WIDTH // GRID_SIZE - 1) * GRID_SIZE, random.randint(0, HEIGHT // GRID_SIZE - 1) * GRID_SIZE)

# Set up game window
win = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Snake Game")

# Main game loop
def main():
    global direction, snake, food
    clock = pygame.time.Clock()
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
        
        keys = pygame.key.get_pressed()
        if keys[pygame.K_UP]:
            direction = (0, -GRID_SIZE)
        elif keys[pygame.K_DOWN]:
            direction = (0, GRID_SIZE)
        elif keys[pygame.K_LEFT]:
            direction = (-GRID_SIZE, 0)
        elif keys[pygame.K_RIGHT]:
            direction = (GRID_SIZE, 0)
        
        new_head = (snake[0][0] + direction[0], snake[0][1] + direction[1])
        if new_head in snake[1:] or not 0 <= new_head[0] < WIDTH or not 0 <= new_head[1] < HEIGHT:
            # Game Over
            pygame.quit()
            quit()
        
        snake.insert(0, new_head)
        if new_head == food:
            food = (random.randint(0, WIDTH // GRID_SIZE - 1) * GRID_SIZE, random.randint(0, HEIGHT // GRID_SIZE - 1) * GRID_SIZE)
        else:
            snake.pop()
        
        # Draw
        win.fill(BLACK)
        pygame.draw.rect(win, WHITE, (*food, GRID_SIZE, GRID_SIZE))
        for segment in snake:
            pygame.draw.rect(win, GREEN, (*segment, GRID_SIZE, GRID_SIZE))
        pygame.display.update()

        clock.tick(GAME_SPEED)

if __name__ == "__main__":
    main()
