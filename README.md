# Snakes

This is a simple implementation of the classic Snake game using Python and Pygame.

## How to Play

1. **Objective:** The objective of the game is to control your snake, eat food, and avoid colliding with walls or the opponent's snake.

2. **Controls:** Each player controls their own snake using separate player controller scripts. The snake can move in four directions: UP, DOWN, LEFT, and RIGHT.

3. **Eating Food:** The game area contains food items represented by red squares. When a snake eats a food item, it grows longer, and the player earns a point.

4. **Collision Detection:**
   - If a snake's head collides with its own body, it results in a game over.
   - If a snake's head collides with the opponent's snake, it results in a game over.
   - If a snake's head collides with the walls, it results in a game over.

5. **Scoring:** Each player has their own score displayed at the top wall of the game area. The score increases by one each time a player's snake eats food.

6. **Game Over:** When a game over occurs, the game displays a game over screen showing the winner (if any) and the reason for the game over (e.g., snake collision, wall collision).

7. **Restarting the Game:** After a game over, the game can be restarted by closing the game window and running it again.

## Player Controller Scripts

The game allows each player to control their snake by providing a custom player controller script. These scripts should follow the provided template and provide the desired logic for controlling the snake's movement. The scripts should be named and provided as command-line arguments when running the game.

Please refer to the `player_controller_template.py` file for an example player controller script.

## Dependencies

- Python 3.x
- Pygame library

## Running the Game

1. Make sure you have Python and Pygame installed.

2. Clone the repository or download the source code files.

3. Open a terminal or command prompt and navigate to the project directory.

4. Run the following command to start the game:

   ```shell
   python snake_game.py --player1_script player1_controller.py --player2_script player2_controller.py
