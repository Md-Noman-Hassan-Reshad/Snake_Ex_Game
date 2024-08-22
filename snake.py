import pygame
from random import randint
import os

# pygame setup
pygame.init()
pygame.mixer.init()

screen_width, screen_height = 900, 600
game_window = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("SnakeWithReshad")
bg_img1 = pygame.image.load("Screen/bg.jpg")
bg_img1 = pygame.transform.scale(bg_img1, (screen_width, screen_height)).convert_alpha()
bg_img2 = pygame.image.load("Screen/bg2.jpg")
bg_img2 = pygame.transform.scale(bg_img2, (screen_width, screen_height)).convert_alpha()
pygame.display.update()

# Colors
white = (255, 255, 255)
red = (255, 0, 0)
black = (0, 0, 0)

clock = pygame.time.Clock()
fps = 40


def text_screen(text, color, x, y):
    font = pygame.font.SysFont("", 40)
    screen_text = font.render(text, True, color)
    game_window.blit(screen_text, [x, y])


def plot_snake(game_window, color, snake_list, snake_size):
    for x, y in snake_list:
        pygame.draw.rect(game_window, color, [x, y, snake_size, snake_size])


def welcome():
    pygame.mixer.music.load("Music/wc.mp3")
    pygame.mixer.music.play(-1)
    exit_game = False
    while not exit_game:
        game_window.blit(bg_img1, (0, 0))
        text_screen("Welcome to PLAY WITH EX", black, 250, 200)
        text_screen("Press space bar to play", black, 280, 250)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit_game = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    game_loop()
        pygame.display.update()
        clock.tick(fps)


def game_loop():
    pygame.mixer.music.stop()
    pygame.mixer.music.load("Music/bgm.mp3")
    pygame.mixer.music.play(-1)
    # Game specific variables
    exit_game = False
    game_over = False
    snake_x, snake_y, snake_size = 45, 300, 15
    food_x, food_y = randint(20, screen_width - 20), randint(40, screen_height - 40)
    velocity_x, velocity_y, init_velocity = 0, 0, 3
    score = 0
    snake_list = []
    snake_len = 1

    if not os.path.exists("high_score.txt"):
        with open("high_score.txt", "w") as f:
            f.write("0")
    with open("high_score.txt", "r") as f:
        high_score = f.read()

    while not exit_game:
        if game_over:
            with open("high_score.txt", "w") as f:
                f.write(str(high_score))
            # game_window.fill(white)
            game_window.blit(bg_img1, (0, 0))
            text_screen("Game Over! Press Enter to Continue", red, 200, 250)
            text_screen(f"Score: {score}", red, 200, 290)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    exit_game = True

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        game_loop()

        else:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    exit_game = True

                # handle keys here
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RIGHT:
                        velocity_x = init_velocity
                        velocity_y = 0

                    if event.key == pygame.K_LEFT:
                        velocity_x -= init_velocity
                        velocity_y = 0

                    if event.key == pygame.K_UP:
                        velocity_y -= init_velocity
                        velocity_x = 0

                    if event.key == pygame.K_DOWN:
                        velocity_y += init_velocity
                        velocity_x = 0

            snake_x += velocity_x
            snake_y += velocity_y
            head = [snake_x, snake_y]
            snake_list.append(head)

            if len(snake_list) > snake_len:
                del snake_list[0]

            if snake_x < 0 or snake_x > screen_width or snake_y < 0 or snake_y > screen_height or head in snake_list[:-1]:
                game_over = True
                pygame.mixer.music.stop()
                pygame.mixer.music.load("Music/game_over.wav")
                pygame.mixer.music.play()

            if abs(snake_x - food_x) < 10 and abs(snake_y - food_y) < 10:
                food_sound = pygame.mixer.Sound("Music/eating_food.wav")
                food_sound.play()
                score += 10
                init_velocity += 0.2
                food_x, food_y = randint(20, screen_width - 20), randint(20, screen_height - 20)
                snake_len += 3
                if score > int(high_score):
                    high_score = score

            # game_window.fill(white)
            game_window.blit(bg_img2, (0, 0))
            # Food
            pygame.draw.rect(game_window, red, [food_x, food_y, snake_size, snake_size])
            # Snake
            plot_snake(game_window, black, snake_list, snake_size)

            text_screen(f"Score: {score}    High Score: {high_score}", red, 5, 5)

        pygame.display.update()
        # flip() the display to put your work on screen
        # pygame.display.flip()
        clock.tick(fps)
    pygame.quit()
    quit()


welcome()
