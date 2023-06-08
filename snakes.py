import pygame
import random

# Initialize Pygame
pygame.init()

# Set up the game window
width, height = 640, 480
window = pygame.display.set_mode((width, height))
pygame.display.set_caption("Snake Game")

# Define colors
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
RED = (255, 0, 0)

# Define the size of each grid cell
cell_size = 20

# Calculate the number of cells in the grid
grid_width = width // cell_size
grid_height = height // cell_size

# Set up the clock to control the frame rate
clock = pygame.time.Clock()

# Define the initial state of the game
snake = [(grid_width // 2, grid_height // 2)]
food = (random.randint(0, grid_width - 1), random.randint(0, grid_height - 1))
direction = "RIGHT"

# Game loop
running = True
while running:
    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP and direction != "DOWN":
                direction = "UP"
            elif event.key == pygame.K_DOWN and direction != "UP":
                direction = "DOWN"
            elif event.key == pygame.K_LEFT and direction != "RIGHT":
                direction = "LEFT"
            elif event.key == pygame.K_RIGHT and direction != "LEFT":
                direction = "RIGHT"

    # Update snake position
    head = snake[0]
    if direction == "UP":
        new_head = (head[0], head[1] - 1)
    elif direction == "DOWN":
        new_head = (head[0], head[1] + 1)
    elif direction == "LEFT":
        new_head = (head[0] - 1, head[1])
    elif direction == "RIGHT":
        new_head = (head[0] + 1, head[1])

    # Check for collisions
    if (
        new_head[0] < 0
        or new_head[0] >= grid_width
        or new_head[1] < 0
        or new_head[1] >= grid_height
        or new_head in snake
    ):
        running = False

    # Check if the snake has eaten the food
    if new_head == food:
        food = (random.randint(0, grid_width - 1), random.randint(0, grid_height - 1))
    else:
        snake.pop()

    snake.insert(0, new_head)

    # Clear the window
    window.fill(BLACK)

    # Draw the snake
    for segment in snake:
        pygame.draw.rect(
            window, GREEN, (segment[0] * cell_size, segment[1] * cell_size, cell_size, cell_size)
        )

    # Draw the food
    pygame.draw.rect(
        window, RED, (food[0] * cell_size, food[1] * cell_size, cell_size, cell_size)
    )

    # Update the display
    pygame.display.flip()

    # Control the frame rate
    clock.tick(10)

# Quit the game
pygame.quit()
