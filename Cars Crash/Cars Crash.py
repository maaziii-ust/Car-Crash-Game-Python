import pygame
import random
import sys

pygame.init()

# Window
screen_width = 800
screen_height = 600
gameWindow = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Car Racing Game")

# Colors
white = (255, 255, 255)
black = (0, 0, 0)
red = (200, 0, 0)
blue = (0, 0, 200)

# Clock
clock = pygame.time.Clock()
FPS = 60

# Fonts
font = pygame.font.SysFont(None, 40)
big_font = pygame.font.SysFont(None, 70)

# Player car
car_width = 50
car_height = 90
car_x = screen_width // 2 - car_width // 2
car_y = screen_height - car_height - 20
car_speed = 7

# Enemy car
enemy_width = 50
enemy_height = 90
enemy_x = random.randint(100, screen_width - 150)
enemy_y = -100
enemy_speed = 6

# Road
road_left = 150
road_right = screen_width - 150

score = 0
game_over = False


def show_text(text, font, color, x, y):
    render = font.render(text, True, color)
    gameWindow.blit(render, (x, y))


def draw_window():
    gameWindow.fill(black)  # road background

    # Road borders
    pygame.draw.line(gameWindow, white, (road_left, 0), (road_left, screen_height), 5)
    pygame.draw.line(gameWindow, white, (road_right, 0), (road_right, screen_height), 5)

    # Player car
    pygame.draw.rect(gameWindow, blue, (car_x, car_y, car_width, car_height))

    # Enemy car
    pygame.draw.rect(gameWindow, red, (enemy_x, enemy_y, enemy_width, enemy_height))

    # Score
    show_text("Score: " + str(score), font, white, 10, 10)


def check_collision():
    car_rect = pygame.Rect(car_x, car_y, car_width, car_height)
    enemy_rect = pygame.Rect(enemy_x, enemy_y, enemy_width, enemy_height)
    return car_rect.colliderect(enemy_rect)


# Main Loop
while True:

    clock.tick(FPS)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if game_over and event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN:
                # Restart game
                car_x = screen_width // 2 - car_width // 2
                enemy_y = -100
                score = 0
                enemy_speed = 6
                game_over = False

    keys = pygame.key.get_pressed()

    if not game_over:
        # Player movement
        if keys[pygame.K_LEFT] and car_x > road_left:
            car_x -= car_speed
        if keys[pygame.K_RIGHT] and car_x + car_width < road_right:
            car_x += car_speed

        # Enemy movement
        enemy_y += enemy_speed

        # Enemy reset
        if enemy_y > screen_height:
            enemy_y = -100
            enemy_x = random.randint(road_left + 10, road_right - enemy_width - 10)
            score += 1
            enemy_speed += 0.3  # difficulty increase

        # Collision
        if check_collision():
            game_over = True

        draw_window()

    else:
        gameWindow.fill(black)
        show_text("GAME OVER", big_font, red, screen_width // 2 - 160, screen_height // 2 - 60)
        show_text("Press ENTER to Restart", font, white, screen_width // 2 - 170, screen_height // 2)
        show_text("Final Score: " + str(score), font, white, screen_width // 2 - 90, screen_height // 2 + 40)

    pygame.display.update()
