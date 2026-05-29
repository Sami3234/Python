import pygame
import random

pygame.init()

width = 600
height = 400

screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Snake Game Task 2")

white = (255, 255, 255)
black = (0, 0, 0)
green = (0, 255, 0)
red = (255, 0, 0)
yellow = (255, 255, 0)
gray = (100, 100, 100)

snake_block = 10
clock = pygame.time.Clock()
font = pygame.font.SysFont(None, 30)

obstacles = [
    [150, 100, 100, 10],
    [350, 250, 100, 10],
    [250, 170, 10, 80]
]

def show_score(score):
    value = font.render("Score: " + str(score), True, black)
    screen.blit(value, [10, 10])

def draw_snake(snake_list):
    for block in snake_list:
        pygame.draw.rect(screen, green, [block[0], block[1], snake_block, snake_block])

def new_food():
    x = round(random.randrange(0, width - snake_block) / 10.0) * 10.0
    y = round(random.randrange(0, height - snake_block) / 10.0) * 10.0
    return x, y

def hit_obstacle(x, y):
    snake_rect = pygame.Rect(x, y, snake_block, snake_block)
    for obstacle in obstacles:
        obstacle_rect = pygame.Rect(obstacle[0], obstacle[1], obstacle[2], obstacle[3])
        if snake_rect.colliderect(obstacle_rect):
            return True
    return False

def game_loop():
    game_over = False
    game_close = False

    x1 = width / 2
    y1 = height / 2

    x1_change = 0
    y1_change = 0

    snake_list = []
    snake_length = 1

    foodx, foody = new_food()
    yellow_foodx, yellow_foody = new_food()

    score = 0
    speed = 15

    while not game_over:

        while game_close:
            screen.fill(white)
            message = font.render("Game Over! Press C to Play Again or Q to Quit", True, red)
            screen.blit(message, [45, height / 2])
            show_score(score)
            pygame.display.update()

            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        game_over = True
                        game_close = False
                    if event.key == pygame.K_c:
                        game_loop()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_over = True

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    x1_change = -snake_block
                    y1_change = 0
                elif event.key == pygame.K_RIGHT:
                    x1_change = snake_block
                    y1_change = 0
                elif event.key == pygame.K_UP:
                    y1_change = -snake_block
                    x1_change = 0
                elif event.key == pygame.K_DOWN:
                    y1_change = snake_block
                    x1_change = 0

        if score > 100:
            speed = 30

        x1 += x1_change
        y1 += y1_change

        if x1 >= width or x1 < 0 or y1 >= height or y1 < 0:
            game_close = True

        if hit_obstacle(x1, y1):
            game_close = True

        screen.fill(white)

        pygame.draw.rect(screen, red, [foodx, foody, snake_block, snake_block])

        if score > 150:
            pygame.draw.rect(screen, yellow, [yellow_foodx, yellow_foody, snake_block, snake_block])

        for obstacle in obstacles:
            pygame.draw.rect(screen, gray, obstacle)

        snake_head = [x1, y1]
        snake_list.append(snake_head)

        if len(snake_list) > snake_length:
            del snake_list[0]

        for block in snake_list[:-1]:
            if block == snake_head:
                game_close = True

        draw_snake(snake_list)
        show_score(score)

        pygame.display.update()

        if x1 == foodx and y1 == foody:
            foodx, foody = new_food()
            snake_length += 1
            score += 10

        if score > 150 and x1 == yellow_foodx and y1 == yellow_foody:
            yellow_foodx, yellow_foody = new_food()
            snake_length += 2
            score += 20

        clock.tick(speed)

    pygame.quit()
    quit()

game_loop()