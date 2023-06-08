import pygame
import random

# Initialize Pygame
pygame.init()

# Set up the game window
width, height = 640, 480
window = pygame.display.set_mode((width, height))
pygame.display.set_caption("Snake Game - Two Players")

# Define colors
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
RED = (255, 0, 0)

# Define the size of each grid cell
cell_size = 20

# Calculate the number of cells in the grid
grid_width = width // cell_size
grid_height = height // cell_size

# Set up the clock to control the frame rate
clock = pygame.time.Clock()

# Define the initial state of the game
snake1 = [(grid_width // 4, grid_height // 2)]
snake2 = [(grid_width * 3 // 4, grid_height // 2)]
food = (random.randint(0, grid_width - 1), random.randint(0, grid_height - 1))
direction1 = "RIGHT"
direction2 = "LEFT"

# Game loop
running = True
while running:
    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP and direction1 != "DOWN":
                direction1 = "UP"
            elif event.key == pygame.K_DOWN and direction1 != "UP":
                direction1 = "DOWN"
            elif event.key == pygame.K_LEFT and direction1 != "RIGHT":
                direction1 = "LEFT"
            elif event.key == pygame.K_RIGHT and direction1 != "LEFT":
                direction1 = "RIGHT"
            elif event.key == pygame.K_w and direction2 != "DOWN":
                direction2 = "UP"
            elif event.key == pygame.K_s and direction2 != "UP":
                direction2 = "DOWN"
            elif event.key == pygame.K_a and direction2 != "RIGHT":
                direction2 = "LEFT"
            elif event.key == pygame.K_d and direction2 != "LEFT":
                direction2 = "RIGHT"

    # Update snake positions
    head1 = snake1[0]
    if direction1 == "UP":
        new_head1 = (head1[0], head1[1] - 1)
    elif direction1 == "DOWN":
        new_head1 = (head1[0], head1[1] + 1)
    elif direction1 == "LEFT":
        new_head1 = (head1[0] - 1, head1[1])
    elif direction1 == "RIGHT":
        new_head1 = (head1[0] + 1, head1[1])

    head2 = snake2[0]
    if direction2 == "UP":
        new_head2 = (head2[0], head2[1] - 1)
    elif direction2 == "DOWN":
        new_head2 = (head2[0], head2[1] + 1)
    elif direction2 == "LEFT":
        new_head2 = (head2[0] - 1, head2[1])
    elif direction2 == "RIGHT":
        new_head2 = (head2[0] + 1, head2[1])

    # Check for collisions
    if (
        new_head1[0] < 0
        or new_head1[0] >= grid_width
        or new_head1[1] < 0
        or new_head1[1] >= grid_height
        or new_head1 in snake1
    ) or (
        new_head2[0] < 0
        or new_head2[0] >= grid_width
        or new_head2[1] < 0
        or new_head2[1] >= grid_height
        or new_head2 in snake2
    ):
        running = False

    # Check if the snakes have eaten the food
    if new_head1 == food:
        food = (random.randint(0, grid_width - 1), random.randint(0, grid_height - 1))
    else:
        snake1.pop()

    if new_head2 == food:
        food = (random.randint(0, grid_width - 1), random.randint(0, grid_height - 1))
    else:
        snake2.pop()

    snake1.insert(0, new_head1)
    snake2.insert(0, new_head2)

    # Clear the window
    window.fill(BLACK)

    # Draw the snakes
    for segment in snake1:
        pygame.draw.rect(
            window, GREEN, (segment[0] * cell_size, segment[1] * cell_size, cell_size, cell_size)
        )
    for segment in snake2:
        pygame.draw.rect(
            window, BLUE, (segment[0] * cell_size, segment[1] * cell_size, cell_size, cell_size)
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
