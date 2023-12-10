import random
import sys
import pygame
from pygame.locals import *

# Constants
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600
ELEVATION = WINDOW_HEIGHT * 0.8
FRAME_PER_SECOND = 30
PIPE_IMAGE = "path_to_pipe_image.png"
BACKGROUND_IMAGE = "path_to_background_image.jpg"
BIRD_IMAGE = "path_to_bird_image.png"
BASE_IMAGE = "path_to_base_image.jpg"

# Initialize Pygame
pygame.init()

# Function to load sounds
def load_sound(file_path):
    pygame.mixer.init()
    sound = pygame.mixer.Sound(file_path)
    return sound

# Function to create a pipe
def create_pipe():
    offset = WINDOW_HEIGHT / 3
    pipe_height = PIPE_IMAGES[0].get_height()
    y2 = offset + random.randrange(
        0, int(WINDOW_HEIGHT - BASE_IMAGE.get_height() - 1.2 * offset)
    )
    pipe_x = WINDOW_WIDTH + 10
    y1 = pipe_height - y2 + offset
    pipe = [
        # Upper Pipe
        {"x": pipe_x, "y": -y1},
        # Lower Pipe
        {"x": pipe_x, "y": y2},
    ]
    return pipe

# Function to check if the bird collides with pipes or goes out of bounds
def is_game_over(horizontal, vertical, up_pipes, down_pipes):
    if vertical > ELEVATION or vertical < 0:
        return True

    for pipe in up_pipes + down_pipes:
        if (
            vertical + BIRD_IMAGE.get_height() > pipe["y"]
            and abs(horizontal - pipe["x"]) < PIPE_IMAGES[0].get_width()
        ):
            return True

    return False

# Function to run the Flappy Bird game
def flappy_bird():
    pygame.init()
    window = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    pygame.display.set_caption("Flappy Bird")

    # Load game images
    BACKGROUND_IMAGE = pygame.image.load(BACKGROUND_IMAGE).convert_alpha()
    BIRD_IMAGE = pygame.image.load(BIRD_IMAGE).convert_alpha()
    BASE_IMAGE = pygame.image.load(BASE_IMAGE).convert_alpha()
    PIPE_IMAGES = [
        pygame.transform.rotate(pygame.image.load(PIPE_IMAGE).convert_alpha(), 180),
        pygame.image.load(PIPE_IMAGE).convert_alpha(),
    ]

    # Load sounds
    FLAP_SOUND = load_sound("path_to_flap_sound.wav")

    your_score = 0

    horizontal = int(WINDOW_WIDTH / 5)
    vertical = int(WINDOW_HEIGHT / 2)
    ground = 0

    # Pipes to be blitted
    up_pipes = []
    down_pipes = []

    # Velocities and acceleration
    pipe_vel_x = -5
    ye_velocity_y = -9
    ye_max_vel_y = 10
    ye_min_vel_y = -8
    ye_acc_y = 1
    ye_flap_velocity = -12
    ye_flapped = False

    while True:
        for event in pygame.event.get():
            if event.type == QUIT or (
                event.type == KEYDOWN and event.key == K_ESCAPE
            ):
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN and (event.key == K_SPACE or event.key == K_UP):
                ye_velocity_y = ye_flap_velocity
                ye_flapped = True
                FLAP_SOUND.play()

        # This will return true when the bird crashes
        game_over = is_game_over(horizontal, vertical, up_pipes, down_pipes)
        if game_over:
            print(f"Your score is {your_score}")
            return

        # Check for score
        for pipe in up_pipes:
            if pipe["x"] + PIPE_IMAGES[0].get_width() < horizontal < pipe["x"] + PIPE_IMAGES[0].get_width() + 5:
                your_score += 1
                print(f"Your score is {your_score}")

        # Normal bird physics when not flapping
        if ye_velocity_y < ye_max_vel_y and not ye_flapped:
            ye_velocity_y += ye_acc_y

        # Flappy moment
        if ye_flapped:
            ye_flapped = False

        # Bird physics regardless of flap
        player_height = BIRD_IMAGE.get_height()
        vertical = vertical + ye_velocity_y

        # Pipe motion
        for pipe in up_pipes + down_pipes:
            pipe["x"] += pipe_vel_x

        # Add a new pipe when the first is about to cross the leftmost part of the screen
        if 0 < up_pipes[0]["x"] < 20:
            new_pipe = create_pipe()
            up_pipes.append(new_pipe[0])
            down_pipes.append(new_pipe[1])

        # Remove pipes that are out of the screen
        if up_pipes and up_pipes[0]["x"] < -PIPE_IMAGES[0].get_width():
            up_pipes.pop(0)
            down_pipes.pop(0)

        # Blit game images
        window.blit(BACKGROUND_IMAGE, (0, 0))
        for upper_pipe, lower_pipe in zip(up_pipes, down_pipes):
            window.blit(PIPE_IMAGES[0], (upper_pipe["x"], upper_pipe["y"]))
            window.blit(PIPE_IMAGES[1], (lower_pipe["x"], lower_pipe["y"]))

        window.blit(BASE_IMAGE, (ground, ELEVATION))
        window.blit(BIRD_IMAGE, (horizontal, vertical))

        # Refreshing the game window
        pygame.display.update()
        pygame.time.Clock().tick(FRAME_PER_SECOND)

if __name__ == "__main__":
    print("WELCOME TO THE FLAPPY BIRD GAME")
    print("Press space or enter to start the game")

    while True:
        for event in pygame.event.get():
            if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                pygame.quit()
                sys.exit()
            elif event.type == KEYDOWN and (event.key == K_SPACE or event.key == K_UP):
                flappy_bird()
            else:
                # Handle any other events
                pass
