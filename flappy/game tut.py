import random
import sys
import pygame
from pygame.locals import *

window_width = 1280
window_height = 720

# Set height and width of window
window = pygame.display.set_mode((window_width, window_height))
elevation = window_height * 0.8
framepersecond = 30
pipeimage = "C:\\Users\\Dell-pc\\Documents\\HGL\\11-G Heritage 2023\\CS STUFF\\flappy\\images\\pipe.png"
background_image = "C:\\Users\\Dell-pc\\Documents\\HGL\\11-G Heritage 2023\\CS STUFF\\flappy\\images\\background1.jpg"
yeplayer_image = "C:\\Users\\Dell-pc\\Documents\\HGL\\11-G Heritage 2023\\CS STUFF\\flappy\\images\\kanye (Custom).png"
sealevel_image = "C:\\Users\\Dell-pc\\Documents\\HGL\\11-G Heritage 2023\\CS STUFF\\flappy\\images\\base.jpg"


def flappy_ye(game_images):
    your_score = 0
    horizontal = int(window_width / 5)
    vertical = int(window_height / 2)
    ground = 0
    mytempheight = 100

    # Generating two pipes for blitting on window
    first_pipe = create_pipe()
    second_pipe = create_pipe()

    # List containing lower pipes
    down_pipes = [
        {'rect': pygame.Rect(window_width + 300 - mytempheight, first_pipe[1]['y'], game_images['pipeimage'][1].get_width(), game_images['pipeimage'][1].get_height())},
        {'rect': pygame.Rect(window_width + 300 - mytempheight + (window_width / 2), second_pipe[1]['y'], game_images['pipeimage'][1].get_width(), game_images['pipeimage'][1].get_height())},
    ]

    # List Containing upper pipes
    up_pipes = [
        {'rect': pygame.Rect(window_width + 300 - mytempheight, first_pipe[0]['y'], game_images['pipeimage'][0].get_width(), game_images['pipeimage'][0].get_height())},
        {'rect': pygame.Rect(window_width + 200 - mytempheight + (window_width / 2), second_pipe[0]['y'], game_images['pipeimage'][0].get_width(), game_images['pipeimage'][0].get_height())},
    ]

    # various velocities (omg physics reference?!)

    # pipe
    pipe_vel_x = -10

    # kanye
    ye_velocity_y = -9
    ye_max_vel_y = 10
    ye_min_vel_y = -8
    ye_acc_y = 1

    # kanye but flapping
    ye_flap_velocity = -12
    ye_flapped = False

    while True:
        for event in pygame.event.get():
            if event.type == event.type == KEYDOWN and event.key == K_ESCAPE:
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN and (event.key == BUTTON_LEFT or event.key == K_SPACE):
                if vertical > 0:
                    ye_velocity_y = ye_flap_velocity
                    ye_flapped = True

        # This will return true when kanye crashes
        game_over = is_game_over(horizontal, vertical, player_rect, up_pipes, down_pipes, game_images)
        if game_over:
            return

        # check for your_score
        player_mid_pos = horizontal + game_images['yebird'].get_width() / 2
        for pipe in up_pipes:
            pipe_mid_pos = pipe['rect'].left + game_images['pipeimage'][0].get_width() / 2
            if pipe_mid_pos <= player_mid_pos < pipe_mid_pos + 4:
                your_score += 1
                print(f"Your your_score is {your_score}")

        if ye_velocity_y < ye_max_vel_y and not ye_flapped:
            ye_velocity_y += ye_acc_y

        if ye_flapped:
            ye_flapped = False
        player_height = game_images['yebird'].get_height()
        vertical = vertical + min(ye_velocity_y, elevation - vertical - player_height)

        # move pipes to the left
        for pipe in up_pipes + down_pipes:
            pipe['rect'].left += pipe_vel_x

        # Add a new pipe when the first is about to cross the leftmost part of the screen
        if 0 < up_pipes[0]['rect'].left < 5:
            new_pipe = create_pipe()
            up_pipes.append(new_pipe[0])
            down_pipes.append(new_pipe[1])

        # if the pipe is out of the screen, remove it
        if up_pipes[0]['rect'].right < 0:
            up_pipes.pop(0)
            down_pipes.pop(0)

        # Lets blit our game images now
        window.blit(game_images['background'], (0, 0))
        for upper_pipe, lower_pipe in zip(up_pipes, down_pipes):
            window.blit(game_images['pipeimage'][0], upper_pipe['rect'].topleft)
            window.blit(game_images['pipeimage'][1], lower_pipe['rect'].topleft)

        window.blit(game_images['sea_level'], (ground, elevation))
        window.blit(game_images['yebird'], (horizontal, vertical))

        # Fetching the digits of score.
        numbers = [int(x) for x in list(str(your_score))]
        width = 0

        # finding the width of score images from numbers.
        for num in numbers:
            width += game_images['scoreimages'][num].get_width()
        Xoffset = (window_width - width) / 1.1

        # Blitting the images on the window.
        for num in numbers:
            window.blit(game_images['scoreimages'][num],
                        (Xoffset, window_width * 0.02))
            Xoffset += game_images['scoreimages'][num].get_width()

        # Refreshing the game window and displaying the score.
        pygame.display.update()
        pygame.time.Clock().tick(framepersecond)


def is_game_over(horizontal, vertical, player_rect, up_pipes, down_pipes, game_images):
    if vertical > elevation or vertical < 100 or horizontal == game_images['pipeimage'][0].get_width():
        return True

    for pipe in up_pipes + down_pipes:
        if player_rect.colliderect(pipe['rect']):
            return True

    return False


def create_pipe():
    offset = window_height / 3
    pipe_height = game_images['pipeimage'][0].get_height()
    y2 = offset + random.randrange(
        0, int(window_height - game_images['sea_level'].get_height() - 1.2 * offset))
    pipe_x = window_width + 10
    y1 = pipe_height - y2 + offset
    pipe = [
        # upper Pipe
        {'rect': pygame.Rect(pipe_x, -y1, game_images['pipeimage'][0].get_width(), game_images['pipeimage'][0].get_height())},

        # lower Pipe
        {'rect': pygame.Rect(pipe_x, y2, game_images['pipeimage'][1].get_width(), game_images['pipeimage'][1].get_height())}
    ]
    return pipe

if __name__ == "__main__":
    pygame.init()
    pygame.display.set_caption('Flappy Ye')

    # this is where we load all the images and do other image things
    game_images = {
        'scoreimages': [
            # thank you chaticus gpt <3
            pygame.image.load(f"C:\\Users\\Dell-pc\\Documents\\HGL\\11-G Heritage 2023\\CS STUFF\\flappy\\images\\{i}.png").convert_alpha()
            for i in range(10)
        ],
        'yebird': pygame.image.load(yeplayer_image).convert_alpha(),
        'sea_level': pygame.image.load(sealevel_image).convert_alpha(),
        'background': pygame.image.load(background_image).convert_alpha(),
        'pipeimage': [
            pygame.transform.rotate(pygame.image.load(pipeimage).convert_alpha(), 180),
            pygame.image.load(pipeimage).convert_alpha()
        ],
    }

    print("WELCOME TO THE FLAPPY BIRD GAME")
    print("Press space or enter to start the game")

    while True:
        horizontal = int(window_width / 5)
        vertical = int((window_height - game_images['yebird'].get_height()) / 2)
        ground = 0
        player_rect = game_images['yebird'].get_rect()

        while True:
            for event in pygame.event.get():
                if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                    pygame.quit()
                    sys.exit()
                elif event.type == KEYDOWN and (event.key == K_SPACE or event.key == K_UP):
                    flappy_ye(game_images)
                else:
                    window.blit(game_images['background'], (0, 0))
                    window.blit(game_images['yebird'], (horizontal, vertical))
                    window.blit(game_images['sea_level'], (ground, elevation))
                    pygame.display.update()
                    pygame.time.Clock().tick(framepersecond)

