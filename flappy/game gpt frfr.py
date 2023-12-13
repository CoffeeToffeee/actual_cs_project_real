import random
import sys
import pygame
from pygame.locals import *
import os

# Initialize Pygame
pygame.init()

# Set window dimensions
window_width = 1280
window_height = 720
window = pygame.display.set_mode((window_width, window_height))

# Define paths for images and sounds
script_dir = os.path.dirname(os.path.abspath(__file__))
images_path = os.path.join(script_dir, 'images')
sounds_path = os.path.join(script_dir, 'sounds')

# Load images
background_image = os.path.join(images_path, 'background1.jpg')
yeplayer_image = os.path.join(images_path, 'kanye (Custom).png')
sealevel_image = os.path.join(images_path, 'base.jpg')
pipeimage = os.path.join(images_path, 'pipe.png')

# Load sounds
def load_sound(file_name):
    sound_path = os.path.join(sounds_path, file_name)
    sound = pygame.mixer.Sound(sound_path)
    return sound

# Set up game parameters
elevation = window_height * 0.8
framepersecond = 30
your_score = 0
pipe_vel_x = -10
ye_velocity_y = -9
ye_max_vel_y = 10
ye_min_vel_y = -8
ye_acc_y = 1
ye_mid_pos = window_width / 5 + pygame.image.load(yeplayer_image).get_width() / 2
ye_flap_velocity = -12
ye_flapped = False
pipe_height = pygame.image.load(pipeimage).get_height()
offset = window_height / 3
cooldown = 0.1

# Function to create a pipe
def create_pipe():
    y2 = offset + random.randrange(0, int(window_height - pygame.image.load(sealevel_image).get_height() - 1.2 * offset))
    pipe_x = window_width + 10
    y1 = pipe_height - y2 + offset
    return [
        {'x': pipe_x, 'y': -y1},
        {'x': pipe_x, 'y': y2}
    ]

# Main game loop
def flappy_ye():
    global ye_velocity_y, ye_flapped, your_score
    horizontal = int(window_width / 5)
    vertical = int(window_height / 2)
    ground = 0

    first_pipe = create_pipe()
    second_pipe = create_pipe()
    down_pipes = [
        {'x': window_width + 300 - offset, 'y': first_pipe[1]['y']},
        {'x': window_width + 300 - offset + (window_width / 2), 'y': second_pipe[1]['y']},
    ]
    up_pipes = [
        {'x': window_width + 300 - offset, 'y': first_pipe[0]['y']},
        {'x': window_width + 200 - offset + (window_width / 2), 'y': second_pipe[0]['y']},
    ]

    kanye_flap_sound = load_sound('kanye 14.mp3')

    while True:
        for event in pygame.event.get():
            if event.type == event.type == KEYDOWN and event.key == K_ESCAPE:
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN and (event.key == K_SPACE):
                ye_velocity_y = ye_flap_velocity
                ye_flapped = True
                kanye_flap_sound.play()

        game_over = is_game_over(horizontal, vertical, up_pipes, down_pipes)
        if game_over:
            load_sound('kanye 1.mp3').play()
            return

        for pipe in up_pipes:
            pipe_mid_pos = pipe['x'] + pygame.image.load(pipeimage).get_width() / 2
            if pipe_mid_pos <= ye_mid_pos < pipe_mid_pos:
                your_score += 1
                print(f"Your score is {your_score}")

        if ye_velocity_y < ye_max_vel_y and not ye_flapped:
            ye_velocity_y += ye_acc_y

        if ye_flapped:
            ye_flapped = False

        player_height = pygame.image.load(yeplayer_image).get_height()
        vertical = vertical + ye_velocity_y

        for upper_pipe, lower_pipe in zip(up_pipes, down_pipes):
            upper_pipe['x'] += pipe_vel_x
            lower_pipe['x'] += pipe_vel_x

        if 0 < up_pipes[0]['x'] < 20:
            new_pipe = create_pipe()
            up_pipes.append(new_pipe[0])
            down_pipes.append(new_pipe[1])

        if 0 < up_pipes[0]['x'] < 5:
            new_pipe = create_pipe()
            up_pipes.append(new_pipe[0])

        window.blit(pygame.image.load(background_image).convert_alpha(), (0, 0))
        for upper_pipe, lower_pipe in zip(up_pipes, down_pipes):
            window.blit(pygame.transform.rotate(pygame.image.load(pipeimage).convert_alpha(), 180),
                        (upper_pipe['x'], upper_pipe['y']))
            window.blit(pygame.image.load(pipeimage).convert_alpha(),
                        (lower_pipe['x'], lower_pipe['y']))

        window.blit(pygame.image.load(sealevel_image).convert_alpha(), (ground, elevation))
        window.blit(pygame.image.load(yeplayer_image).convert_alpha(), (horizontal, vertical))

        pygame.display.update()
        pygame.time.Clock().tick(framepersecond)

# Function to check if the game is over
def is_game_over(horizontal, vertical, up_pipes, down_pipes):
    if vertical > elevation or vertical < 0:
        return True
    ye_mid_pos = horizontal + pygame.image.load(yeplayer_image).get_width() / 2

    for pipe in down_pipes:
        if (vertical + pygame.image.load(yeplayer_image).get_height() > pipe['y'] and
                abs(horizontal - (pipe['x']) * 2) < pygame.image.load(pipeimage).get_width()):
            return True
    return False

if __name__ == "__main__":
    print("WELCOME TO THE FLAPPY BIRD GAME")
    print("Press space or enter to start the game")

    while True:
        horizontal = int(window_width / 5)
        vertical = int((window_height - pygame.image.load(yeplayer_image).get_height()) / 2)
        ground = 0
        while True:
            for event in pygame.event.get():
                if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                    pygame.quit()
                    sys.exit()
                elif event.type == KEYDOWN and (event.key == K_SPACE or event.key == K_UP):
                    flappy_ye()
                else:
                    window.blit(pygame.image.load(background_image).convert_alpha(), (0, 0))
                    window.blit(pygame.image.load(yeplayer_image).convert_alpha(), (horizontal, vertical))
                    window.blit(pygame.image.load(sealevel_image).convert_alpha(), (ground, elevation))
                    pygame.display.update()
                    pygame.time.Clock().tick(framepersecond)
