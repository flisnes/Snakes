import pygame
import random
import importlib
import argparse

# Create an argument parser
parser = argparse.ArgumentParser(description="Snake Game")

# Add arguments for player controller script filenames
parser.add_argument("player1_script", help="Filename of the player 1 controller script")
parser.add_argument("player2_script", help="Filename of the player 2 controller script")

# Parse the command-line arguments
args = parser.parse_args()

# Initialize Pygame
pygame.init()

# Set up the game window
width, height = 800, 600
window = pygame.display.set_mode((width, height))
pygame.display.set_caption("Snake Game - Two Players")

# Define colors
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
RED = (255, 0, 0)
WHITE = (255, 255, 255)

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

# Define the game state
game_over = False
winner = None

# Import player controller scripts
player1_controller = __import__(args.player1_script.replace(".py", "").replace(".\\", ""))
player2_controller = __import__(args.player2_script.replace(".py", "").replace(".\\", ""))

def generate_food(snake1, snake2):
    while True:
        food_x = random.randint(0, grid_width - 1)
        food_y = random.randint(0, grid_height - 1)

        # Check if the generated food position is not occupied by any snake
        if (food_x, food_y) not in snake1 and (food_x, food_y) not in snake2:
            return food_x, food_y

# Functions to display game over message
def display_game_over(winner, game_over_reason):
    font = pygame.font.Font(None, 36)
    if winner == 0:
        top_text = "Game Over - Tie!"
    elif winner == 1:
        top_text = "Game Over - Player 1 Wins!"
    elif winner == 2:
        top_text = "Game Over - Player 2 Wins!"

    bottom_text = game_over_reason

    top_text_render = font.render(top_text, True, WHITE)
    bottom_text_render = font.render(bottom_text, True, WHITE)

    top_text_rect = top_text_render.get_rect(center=(grid_width * cell_size // 2, grid_height * cell_size // 2 - 20))
    bottom_text_rect = bottom_text_render.get_rect(center=(grid_width * cell_size // 2, grid_height * cell_size // 2 + 20))

    window.blit(top_text_render, top_text_rect)
    window.blit(bottom_text_render, bottom_text_rect)

# Game loop
while not game_over:
    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game_over = True

    # Call the player controller functions
    direction1 = player1_controller.move(snake1, snake2, food, direction1)
    direction2 = player2_controller.move(snake2, snake1, food, direction2)

    # Update snake positions
    if not game_over:
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

        # Check for collisions with walls and other snakes
        if (
            new_head1[0] < 0
            or new_head1[0] >= grid_width
            or new_head1[1] < 0
            or new_head1[1] >= grid_height
        ):
            collision1 = True
            collision1_reason = "Snake 1 collided with the wall"
        elif (
            new_head1 in snake1
        ):
            collision1 = True
            collision1_reason = "Snake 1 collided with itself"
        elif (
            new_head1 in snake2
        ):
            collision1 = True
            collision1_reason = "Snake 1 collided with Snake 2"
        else:
            collision1 = False
        
        if (
            new_head2[0] < 0
            or new_head2[0] >= grid_width
            or new_head2[1] < 0
            or new_head2[1] >= grid_height
        ):
            collision2 = True
            collision2_reason = "Snake 2 collided with the wall"
        elif (
            new_head2 in snake2
        ):
            collision2 = True
            collision2_reason = "Snake 2 collided with itself"
        elif (
            new_head2 in snake1
        ):
            collision2 = True
            collision2_reason = "Snake 2 collided with Snake 1"
        else:
            collision2 = False

        # Determine the game over state
        if collision1 and collision2:
            game_over = True
            game_over_reason = collision1_reason + " while " + collision2_reason
            winner = 0
        elif collision1:
            game_over = True
            game_over_reason = collision1_reason
            winner = 2
        elif collision2:
            game_over = True
            game_over_reason = collision2_reason
            winner = 1

        # Check if the snakes have eaten the food
        if new_head1 == food:
            food = generate_food(snake1, snake2)
        else:
            snake1.pop()

        if new_head2 == food:
            food = generate_food(snake1, snake2)
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
    clock.tick(16)

# Game over loop
window.fill(BLACK)
display_game_over(winner, game_over_reason)
pygame.display.flip()

# Keep the game window open until the user closes it
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

# Quit the game
pygame.quit()