import pygame
import time
import random

# Initialize pygame
pygame.init()

# Colors (RGB)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (213, 50, 80)
GREEN = (0, 255, 0)
BLUE = (50, 153, 213)
YELLOW = (255, 255, 102)

# Display dimensions
WIDTH = 600
HEIGHT = 400
BLOCK_SIZE = 20

# Font
font_style = pygame.font.SysFont("bahnschrift", 25)
score_font = pygame.font.SysFont("comicsansms", 35)

# Setup the screen
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Caterpillar Game")

# Clock to control the game speed
clock = pygame.time.Clock()

# Score display function
def display_score(score):
    value = score_font.render("Your Score: " + str(score), True, WHITE)
    screen.blit(value, [0, 0])

# Game Over Message
def game_over_message():
    message = font_style.render("Game Over! Press Q-Quit or C-Play Again", True, RED)
    screen.blit(message, [WIDTH / 6, HEIGHT / 3])

# The main game loop function
def gameLoop():
    game_over = False
    game_close = False

    # Initial snake position and movement
    x1 = WIDTH / 2
    y1 = HEIGHT / 2
    x1_change = 0
    y1_change = 0

    snake_body = []
    snake_length = 1

    # Randomize food position
    foodx = round(random.randrange(0, WIDTH - BLOCK_SIZE) / BLOCK_SIZE) * BLOCK_SIZE
    foody = round(random.randrange(0, HEIGHT - BLOCK_SIZE) / BLOCK_SIZE) * BLOCK_SIZE

    while not game_over:

        while game_close:
            screen.fill(BLACK)
            game_over_message()
            display_score(snake_length - 1)
            pygame.display.update()

            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        game_over = True
                        game_close = False
                    if event.key == pygame.K_c:
                        gameLoop()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_over = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    x1_change = -BLOCK_SIZE
                    y1_change = 0
                elif event.key == pygame.K_RIGHT:
                    x1_change = BLOCK_SIZE
                    y1_change = 0
                elif event.key == pygame.K_UP:
                    y1_change = -BLOCK_SIZE
                    x1_change = 0
                elif event.key == pygame.K_DOWN:
                    y1_change = BLOCK_SIZE
                    x1_change = 0

        if x1 >= WIDTH or x1 < 0 or y1 >= HEIGHT or y1 < 0:
            game_close = True
        x1 += x1_change
        y1 += y1_change
        screen.fill(BLUE)

        # Draw food (as a green rectangle)
        pygame.draw.rect(screen, GREEN, [foodx, foody, BLOCK_SIZE, BLOCK_SIZE])

        # Snake movement
        snake_head = []
        snake_head.append(x1)
        snake_head.append(y1)
        snake_body.append(snake_head)

        if len(snake_body) > snake_length:
            del snake_body[0]

        for x in snake_body[:-1]:
            if x == snake_head:
                game_close = True

        # Draw the snake (as black rectangles)
        for segment in snake_body:
            pygame.draw.rect(screen, BLACK, [segment[0], segment[1], BLOCK_SIZE, BLOCK_SIZE])

        display_score(snake_length - 1)

        pygame.display.update()

        # Check if the snake eats the food
        if x1 == foodx and y1 == foody:
            foodx = round(random.randrange(0, WIDTH - BLOCK_SIZE) / BLOCK_SIZE) * BLOCK_SIZE
            foody = round(random.randrange(0, HEIGHT - BLOCK_SIZE) / BLOCK_SIZE) * BLOCK_SIZE
            snake_length += 1

        # Control game speed
        clock.tick(15)

    pygame.quit()
    quit()

# Run the game
gameLoop()
