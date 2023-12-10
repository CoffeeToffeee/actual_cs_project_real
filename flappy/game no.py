import pygame
import sys
import random

# Initialize Pygame
pygame.init()

# Set up the game window
width, height = 800, 600
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption('Flappy Bird')

# Colors
black = (0, 0, 0)
white = (255, 255, 255)

# Game variables
clock = pygame.time.Clock()
gravity = 1
bird_velocity = 0
bird_position = [100, height // 2]
pipe_width = 50
pipe_height = 300
pipe_gap = 150
pipe_velocity = 5
pipes = []

def draw_bird(position):
    pygame.draw.rect(screen, white, pygame.Rect(position[0], position[1], 50, 50))

def draw_pipe(pipe):
    pygame.draw.rect(screen, white, pygame.Rect(pipe['x'], 0, pipe_width, pipe['height_top']))
    pygame.draw.rect(screen, white, pygame.Rect(pipe['x'], pipe['height_bottom'], pipe_width, height - pipe['height_bottom']))

def generate_pipe():
    height_top = random.randint(50, height - pipe_gap - 50)
    return {'x': width, 'height_top': height_top, 'height_bottom': height_top + pipe_gap}

def check_collision(pipe):
    if bird_position[1] < pipe['height_top'] or bird_position[1] > pipe['height_bottom']:
        if pipe['x'] < bird_position[0] < pipe['x'] + pipe_width:
            return True
    return False

# Game loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Gravity and bird movement
    bird_velocity += gravity
    bird_position[1] += bird_velocity

    # Generate pipes
    if len(pipes) == 0 or pipes[-1]['x'] < width - 300:
        pipes.append(generate_pipe())

    # Move pipes
    for pipe in pipes:
        pipe['x'] -= pipe_velocity

    # Check for collisions with pipes
    for pipe in pipes:
        if check_collision(pipe):
            print("Game Over!")
            running = False

    # Remove off-screen pipes
    pipes = [pipe for pipe in pipes if pipe['x'] + pipe_width > 0]

    # Draw background
    screen.fill(black)

    # Draw pipes
    for pipe in pipes:
        draw_pipe(pipe)

    # Draw bird
    draw_bird(bird_position)

    # Update the display
    pygame.display.flip()

    # Set the frame rate
    clock.tick(30)

# Quit Pygame
pygame.quit()
sys.exit()
