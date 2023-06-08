def move(snake1, snake2, food):
    # Implement your player 2 controller logic here
    # You have access to the position of snake1, snake2, and food
    # Return the desired direction of movement for snake2 as dx, dy
    
    head_x, head_y = snake2[0]
    food_x, food_y = food

    # Calculate the desired direction based on the position of the food
    if head_y < food_y:
        return "DOWN"
    elif head_y > food_y:
        return "UP"
    elif head_x < food_x:
        return "RIGHT"
    elif head_x > food_x:
        return "LEFT"