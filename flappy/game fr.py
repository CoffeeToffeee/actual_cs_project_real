import random   
import sys  
import pygame 
from pygame.locals import *

window_w = 1728
window_h = 1080

window = pygame.display.set_mode((window_w, window_h))    
elevation = window_h * 0.8
game_images = {}       
framepersecond = 32

#Images (change)
pipeimage = "C:\\Users\\Dell-pc\\Documents\\HGL\\11-G Heritage 2023\\CS STUFF\\flappy\\images\\pipe.png"
background_image = "C:\\Users\\Dell-pc\\Documents\\HGL\\11-G Heritage 2023\\CS STUFF\\flappy\\images\\background1.jpg"
birdplayer_image = "C:\\Users\\Dell-pc\\Documents\\HGL\\11-G Heritage 2023\\CS STUFF\\flappy\\images\\kanye (Custom).png"
sealevel_image = "C:\\Users\\Dell-pc\\Documents\\HGL\\11-G Heritage 2023\\CS STUFF\\flappy\\images\\base.jpg"

# program where the game starts 
if __name__ == "__main__": 

    #actual things now 
    pygame.init()
    framepersecond_clock = pygame.time.Clock() 

    pygame.display.set_caption('Ye Bird')   


    #this is the part where we load all the images up
    game_images['scoreimages'] = ( 
            pygame.image.load("C:\\Users\\Dell-pc\\Documents\\HGL\\11-G Heritage 2023\\CS STUFF\\flappy\\images\\0.png").convert_alpha(), 
            pygame.image.load("C:\\Users\\Dell-pc\\Documents\\HGL\\11-G Heritage 2023\\CS STUFF\\flappy\\images\\1.png").convert_alpha(), 
            pygame.image.load("C:\\Users\\Dell-pc\\Documents\\HGL\\11-G Heritage 2023\\CS STUFF\\flappy\\images\\2.png").convert_alpha(), 
            pygame.image.load("C:\\Users\\Dell-pc\\Documents\\HGL\\11-G Heritage 2023\\CS STUFF\\flappy\\images\\3.png").convert_alpha(), 
            pygame.image.load("C:\\Users\\Dell-pc\\Documents\\HGL\\11-G Heritage 2023\\CS STUFF\\flappy\\images\\4.png").convert_alpha(),         
            pygame.image.load("C:\\Users\\Dell-pc\\Documents\\HGL\\11-G Heritage 2023\\CS STUFF\\flappy\\images\\5.png").convert_alpha(), 
            pygame.image.load("C:\\Users\\Dell-pc\\Documents\\HGL\\11-G Heritage 2023\\CS STUFF\\flappy\\images\\6.png").convert_alpha(), 
            pygame.image.load("C:\\Users\\Dell-pc\\Documents\\HGL\\11-G Heritage 2023\\CS STUFF\\flappy\\images\\7.png").convert_alpha(), 
            pygame.image.load("C:\\Users\\Dell-pc\\Documents\\HGL\\11-G Heritage 2023\\CS STUFF\\flappy\\images\\8.png").convert_alpha(), 
            pygame.image.load("C:\\Users\\Dell-pc\\Documents\\HGL\\11-G Heritage 2023\\CS STUFF\\flappy\\images\\9.png").convert_alpha() 
        ) 
    game_images['flappybird'] = pygame.image.load(birdplayer_image).convert_alpha()                   
    game_images['sea_level'] = pygame.image.load(sealevel_image).convert_alpha() 
    game_images['background'] = pygame.image.load(background_image).convert_alpha() 
    game_images['pipeimage'] = (pygame.transform.rotate(pygame.image.load(pipeimage) 
                                                            .convert_alpha(), 
                                                            180), 
                                    pygame.image.load(pipeimage).convert_alpha()) 

    print("WELCOME TO YE BuRD") 
    print("Press space or enter to start the game") 


def createPipe(): 
        offset = window_h/3
        pipeHeight = game_images['pipeimage'][0].get_height() 
        
        # generating random height of pipes 
        y2 = offset + random.randrange(0, int(window_h- game_images['sea_level'].get_height() - 1.2 * offset))   
        pipeX = window_w + 10
        y1 = pipeHeight - y2 + offset 
        pipe = [ 
            
            # upper Pipe 
            {'x': pipeX, 'y': -y1}, 
            
            # lower Pipe 
            {'x': pipeX, 'y': y2}   
        ] 
        return pipe

def flappygame(): 
    your_score = 0
    horizontal = int(window_w/5) 
    vertical = int(window_w/2) 
    ground = 0
    mytempheight = 100
  
    # Generating two pipes for blitting on window 
    first_pipe = createPipe() 
    second_pipe = createPipe() 
  
    # List containing lower pipes 
    down_pipes = [ 
        {'x': window_w+300-mytempheight, 
         'y': first_pipe[1]['y']}, 
        {'x': window_w+300-mytempheight+(window_w/2), 
         'y': second_pipe[1]['y']}, 
    ] 
  
    # List Containing upper pipes  
    up_pipes = [ 
        {'x': window_w+300-mytempheight, 
         'y': first_pipe[0]['y']}, 
        {'x': window_w+200-mytempheight+(window_w/2), 
         'y': second_pipe[0]['y']}, 
    ] 
  
    pipeVelX = -4 #pipe velocity along x 
  
    bird_velocity_y = -9  # bird velocity 
    bird_Max_Vel_Y = 10   
    bird_Min_Vel_Y = -8
    birdAccY = 1
      
     # velocity while flapping 
    bird_flap_velocity = -8
      
    # It is true only when the bird is flapping 
    bird_flapped = False  
    while True: 
         
        # Handling the key pressing events 
        for event in pygame.event.get(): 
            if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE): 
                pygame.quit() 
                sys.exit() 
            if event.type == KEYDOWN and (event.key == K_SPACE or event.key == K_UP): 
                if vertical > 0: 
                    bird_velocity_y = bird_flap_velocity 
                    bird_flapped = True
  
        # This function will return true if the flappybird is crashed 
        game_over = isGameOver(horizontal, vertical, up_pipes, down_pipes) 
        if game_over: 
            return
  
        # check for your_score 
        playerMidPos = horizontal + game_images['flappybird'].get_w()/2
        for pipe in up_pipes: 
            pipeMidPos = pipe['x'] + game_images['pipeimage'][0].get_w()/2
            if pipeMidPos <= playerMidPos < pipeMidPos + 4: 
                  # Printing the score 
                your_score += 1
                print(f"Your your_score is {your_score}") 
  
        if bird_velocity_y < bird_Max_Vel_Y and not bird_flapped: 
            bird_velocity_y += birdAccY 
  
        if bird_flapped: 
            bird_flapped = False
        playerHeight = game_images['flappybird'].get_height() 
        vertical = vertical + min(bird_velocity_y, elevation - vertical - playerHeight) 
  
        # move pipes to the left 
        for upperPipe, lowerPipe in zip(up_pipes, down_pipes): 
            upperPipe['x'] += pipeVelX 
            lowerPipe['x'] += pipeVelX 
  
        # Add a new pipe when the first is about 
        # to cross the leftmost part of the screen 
        if 0 < up_pipes[0]['x'] < 5: 
            newpipe = createPipe() 
            up_pipes.append(newpipe[0]) 
            down_pipes.append(newpipe[1]) 
  
        # if the pipe is out of the screen, remove it 
        if up_pipes[0]['x'] < -game_images['pipeimage'][0].get_width(): 
            up_pipes.pop(0) 
            down_pipes.pop(0) 
  
        # Lets blit our game images now 
        window.blit(game_images['background'], (0, 0)) 
        for upperPipe, lowerPipe in zip(up_pipes, down_pipes): 
            window.blit(game_images['pipeimage'][0], 
                        (upperPipe['x'], upperPipe['y'])) 
            window.blit(game_images['pipeimage'][1], 
                        (lowerPipe['x'], lowerPipe['y'])) 
  
        window.blit(game_images['sea_level'], (ground, elevation)) 
        window.blit(game_images['flappybird'], (horizontal, vertical)) 
          
        # Fetching the digits of score. 
        numbers = [int(x) for x in list(str(your_score))] 
        width = 0
          
        # finding the width of score images from numbers. 
        for num in numbers: 
            width += game_images['scoreimages'][num].get_width() 
        Xoffset = (window_w - width)/1.1
          
        # Blitting the images on the window. 
        for num in numbers: 
            window.blit(game_images['scoreimages'][num], (Xoffset, window_w*0.02)) 
            Xoffset += game_images['scoreimages'][num].get_width() 
              
        # Refreshing the game window and displaying the score. 
        pygame.display.update() 
          
        # Set the framepersecond 
        framepersecond_clock.tick(framepersecond)



def isGameOver(horizontal, vertical, up_pipes, down_pipes): 
        if vertical > elevation - 25 or vertical < 0:  
            return True
    
        # Checking if bird hits the upper pipe or not 
        for pipe in up_pipes:     
            pipeHeight = game_images['pipeimage'][0].get_height() 
            if(vertical < pipeHeight + pipe['y']  
            and abs(horizontal - pipe['x']) < game_images['pipeimage'][0].get_width()): 
                return True
                
        # Checking if bird hits the lower pipe or not 
        for pipe in down_pipes: 
            if (vertical + game_images['flappybird'].get_height() > pipe['y']) and abs(horizontal - pipe['x']) < game_images['pipeimage'][0].get_width(): 
                return True
        return False




while True:  
    # sets the coordinates of flappy bird 
    horizontal = int(window_w/5) 
    vertical = int((window_h - game_images['flappybird'].get_height())/2) 
    
    # for selevel 
    ground = 0  
    while True: 
        for event in pygame.event.get(): 

            # if user clicks on cross button, close the game 
            if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE): 
                pygame.quit() 
                
                # Exit the program 
                sys.exit()    

            # If the user presses space or up key, start the game for them 
            elif event.type == KEYDOWN and (event.key == K_SPACE or event.key == K_UP): 
                flappygame() 
            
            # if user doesn't press anykey Nothing happen 
            else: 
                window.blit(game_images['background'], (0, 0)) 
                window.blit(game_images['flappybird'], (horizontal, vertical)) 
                window.blit(game_images['sea_level'], (ground, elevation)) 
                
                # Just Refresh the screen 
                pygame.display.update()         
                
                # set the rate of frame per second 
                framepersecond_clock.tick(framepersecond)




    



    # Checking if bird is above the sealevel. 
    




