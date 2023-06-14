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
width, height = 400, 400
window = pygame.display.set_mode((width, height))
pygame.display.set_caption("Snake Game - Two Players")

# Define colors
BLACK = (0, 0, 0)
GREEN = (50, 200, 50)
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
food = (random.randint(1, grid_width - 2), random.randint(1, grid_height - 2))
walls = [
    (x, 0) for x in range(grid_width)] + [(x, grid_height - 1) for x in range(grid_width)] + [(0, y) for y in range(grid_height)] + [(grid_width - 1, y) for y in range(grid_height)
]
direction1 = "RIGHT"
direction2 = "LEFT"

# Define the game state
game_over = False
winner = 0
snake1_score = 0
snake2_score = 0

# Import player controller scripts
player1_controller = __import__(args.player1_script.replace(".py", "").replace(".\\", ""))
player2_controller = __import__(args.player2_script.replace(".py", "").replace(".\\", ""))

def generate_food(snake1, snake2):
    while True:
        food_x = random.randint(1, grid_width - 2)
        food_y = random.randint(1, grid_height - 2)

        # Check if the generated food position is not occupied by any snake
        if (food_x, food_y) not in snake1 and (food_x, food_y) not in snake2:
            return food_x, food_y
        
def check_collision(new_head1, new_head2, snake1, snake2):

    game_over_reason = ""
    winner = 0

    # Check collisions with other snake
    if new_head1 in snake2 or new_head1 == new_head2:
            winner += 2
            game_over_reason = "Snake 1 collided with snake 2"
    
    if new_head2 in snake1 or new_head2 == new_head1:
            winner += 1
            game_over_reason = "Snake 2 collided with snake 1" # Need to redo game over reason

    # Check collisions with self
    if new_head1 in snake1:
            winner += 2
            game_over_reason = "Snake 1 collided with itself"

    if new_head2 in snake2:
            winner += 1
            game_over_reason = "Snake 2 collided with itself"
    
    # Check collisions with wall
    if new_head1 in walls or snake1 in walls:
            winner += 2
            game_over_reason = "Snake 1 collided with the wall"
    
    if new_head2 in walls or snake2 in walls:
            winner += 1
            game_over_reason = "Snake 2 collided with the wall"
    
    return winner, game_over_reason

# Functions to display game over message
def display_game_over(winner, game_over_reason):
    font = pygame.font.Font(None, 36)
    if winner == 3:
        top_text = "Game Over - Tie!"
    elif winner == 1:
        top_text = "Game Over - Player 1 Wins!"
    elif winner == 2:
        top_text = "Game Over - Player 2 Wins!"

    bottom_text = game_over_reason

    top_text_render = font.render(top_text, True, WHITE)
    bottom_text_render = font.render(bottom_text, True, WHITE)

    top_text_rect = top_text_render.get_rect(center=(grid_width * cell_size // 2, grid_height * cell_size // 2 - cell_size))
    bottom_text_rect = bottom_text_render.get_rect(center=(grid_width * cell_size // 2, grid_height * cell_size // 2 + cell_size))

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

        winner, game_over_reason = check_collision(new_head1, new_head2, snake1, snake2)

        if game_over_reason != "":
            game_over = True
            break

        # Check if the snakes have eaten the food
        if new_head1 == food:
            food = generate_food(snake1, snake2)
            snake1_score += 1
        else:
            snake1.pop()

        if new_head2 == food:
            food = generate_food(snake1, snake2)
            snake2_score += 1
        else:
            snake2.pop()

        snake1.insert(0, new_head1)
        snake2.insert(0, new_head2)

    # Clear the window
    window.fill(BLACK)

    # Draw the walls
    for brick in walls:
        pygame.draw.rect(
            window, WHITE, (brick[0] * cell_size, brick[1] * cell_size, cell_size, cell_size)
        )

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

    # Draw the scores
    font = pygame.font.Font(None, 24)
    score_text1 = font.render(str(snake1_score), True, GREEN)
    score_text2 = font.render(str(snake2_score), True, BLUE)
    window.blit(score_text1, (0, 0))
    window.blit(score_text2, (grid_width*cell_size - cell_size, 0))

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