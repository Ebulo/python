import random
import sys
import pygame
from pygame.locals import *

# Global Variables for the game
pygame.init()

font = pygame.font.Font('freesansbold.ttf', 32)
FPS = 32
SCREENWIDTH = 289
SCREENHEIGHT = 511
SCREEN = pygame.display.set_mode((SCREENWIDTH, SCREENHEIGHT))
GROUNDY = SCREENHEIGHT * 0.8
GAMESPRITES = {}
GAMESOUNDS = {}
PLAYER = 'gallery/sprites/bird.png'
BACKGROUND = 'gallery/sprites/background.png'
PIPE = 'gallery/sprites/pipe.png'
score = 0
start = font.render("Hit Space To start", True, (100, 20, 20))
text = font.render("High Score", True, (0, 255, 0))


def welcomeScreen():
    """
    Shows Welcome images on the screen.
    """
    playerx = int(SCREENWIDTH/5)
    playery = int((SCREENHEIGHT - GAMESPRITES['player'].get_height())/2)
    # messagex = int((SCREENWIDTH - GAMESPRITES['message'].get_width())/2)
    # messagey = int(SCREENHEIGHT * 0.13)
    basex = 0

    while True:
        for event in pygame.event.get():
            # if User Clicks on any BUtton Then Perform Something.

            if event.type == QUIT or (event.type == KEYDOWN and event.type == K_ESCAPE):
                pygame.quit()
                sys.exit()

                # If User press a certain Key Then start The Game
            elif event.type == KEYDOWN and (event.key == K_SPACE or event.key == K_UP):
                return
            else:
                SCREEN.blit(GAMESPRITES['background'], (0, 0))
                SCREEN.blit(GAMESPRITES['player'], (playerx, playery))
                # SCREEN.blit(GAMESPRITES['message'], (messagex, messagey))
                SCREEN.blit(GAMESPRITES['base'], (basex, GROUNDY))
                SCREEN.blit(start, (10, 450))
                
                try:
                    reader = open("gallery/data.txt", "r")
                    scoreboard = []
                    for i in reader:
                        scoreboard.append(int(i))
                    max_score = max(max(scoreboard), score)

                    xpos = SCREENWIDTH/2 - 20
                    SCREEN.blit(text, (xpos-60, 20))
                    for j in str(max_score):
                        j = int(j)
                        SCREEN.blit(GAMESPRITES['numbers'][j], (xpos, SCREENHEIGHT*0.12))
                        xpos += GAMESPRITES['numbers'][j].get_width()
                except:
                    wr = open("gallery/data.txt", "a")
                    wr.write("0 \n 0")

                pygame.display.update()
                FPSCLOCK.tick(FPS)


def mainGame():
    try:
        score = 0
        playerx = int(SCREENWIDTH/5)
        playery = int(SCREENWIDTH/2)
        basex = 0

        # Create Two Pipes for bllitting
        newPipe1 = getRandomPipe()
        newPipe2 = getRandomPipe()

        # Lists of Upper pipes.
        upperPipes = [
            {'x':SCREENWIDTH+200, 'y':newPipe1[0]['y']},
            {'x':SCREENWIDTH+200 + (SCREENWIDTH/2), 'y':newPipe2[0]['y']}
        ]
        
        # Lists of Lower pipes.
        lowerPipes = [
            {'x':SCREENWIDTH+200, 'y':newPipe1[1]['y']},
            {'x':SCREENWIDTH+200 + (SCREENWIDTH/2), 'y':newPipe2[1]['y']},
        ]

        pipeVelX = -4

        playerVelY = -9
        playerMaxVelY = 10
        # playerMinVelY = -8
        playerAccY = 1

        playerFlapAccv = -8 # Velocity while flapping
        playerFlapped = False # It is true only when the bird is flapping


        while True:
            for event in pygame.event.get():
                if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                    pygame.quit()
                    sys.exit()
                if event.type == KEYDOWN and (event.key == K_SPACE or event.key == K_UP):
                    if playery > 0:
                        playerVelY = playerFlapAccv                                             # HERE IS THE ERROR
                        playerFlapped = True
                        GAMESOUNDS['wing'].play()

            crashTest = isCollide(playerx, playery, upperPipes, lowerPipes)
            if crashTest:
                return
            
            # Check for Score
            playerMidPos = playerx + GAMESPRITES['player'].get_width()/2
            for pipe in upperPipes:
                pipeMidPos = pipe['x'] + GAMESPRITES['pipe'][0].get_width()/2
                if pipeMidPos <= playerMidPos < pipeMidPos + 4:
                    score += 1
                    GAMESOUNDS['point'].play()


            if playerVelY < playerMaxVelY and not playerFlapped:
                playerVelY += playerAccY

            if playerFlapped:
                playerFlapped = False
            playerHeight = GAMESPRITES['player'].get_height()
            playery = playery + min(playerVelY, GROUNDY - playery - playerHeight)

            for upperPipe, lowerPipe in zip(upperPipes, lowerPipes):
                upperPipe['x'] += pipeVelX
                lowerPipe['x'] += pipeVelX

            # Add a new pipe when the first is about to go to the left most.
            if 0 < upperPipes[0]['x']<5:
                newpipe = getRandomPipe()
                upperPipes.append(newpipe[0])
                lowerPipes.append(newpipe[1])

            # if the pipe is out of the screen then remove it
            if upperPipes[0]['x'] < -GAMESPRITES['pipe'][0].get_width():
                upperPipes.pop(0)
                lowerPipes.pop(0)

            # Lets blit our sprites
            SCREEN.blit(GAMESPRITES['background'], (0, 0))
            for upperPipe, lowerPipe in zip(upperPipes, lowerPipes):
                SCREEN.blit(GAMESPRITES['pipe'][0], (upperPipe['x'], upperPipe['y']))
                SCREEN.blit(GAMESPRITES['pipe'][1], (lowerPipe['x'], lowerPipe['y']))

            SCREEN.blit(GAMESPRITES['base'], (basex, GROUNDY))
            SCREEN.blit(GAMESPRITES['player'], (playerx, playery))
            myDigits = [int(x) for x in list(str(score))]
            width = 0
            for digit in myDigits:
                width += GAMESPRITES['numbers'][digit].get_width()
            Xofset = (SCREENWIDTH - width)/2

            for digit in myDigits:
                SCREEN.blit(GAMESPRITES['numbers'][digit], (Xofset, SCREENHEIGHT*0.12))
                Xofset += GAMESPRITES['numbers'][digit].get_width()
            pygame.display.update()
            FPSCLOCK.tick(FPS)
    finally:
        writer = open("gallery/data.txt", "a")
        writer.write("0")
        writer.write(f"{score}\n")


def isCollide(playerx, playery, upperPipes, lowerPipes):
    if playery > GROUNDY - 25 or playery<0:
        GAMESOUNDS['hit'].play()
        return True
    for pipe in upperPipes:
        pipeHeight = GAMESPRITES['pipe'][0].get_height()
        if (playery < pipeHeight + pipe['y'] and abs(playerx - pipe['x']) < GAMESPRITES['pipe'][0].get_width()-20):
            GAMESOUNDS['hit'].play()
            return True
    
    for pipe in lowerPipes:
        if (playery + GAMESPRITES['player'].get_height() > pipe['y'] and abs(playerx - pipe['x']) < GAMESPRITES['pipe'][0].get_width()-20):
            GAMESOUNDS['hit'].play()
            return True

    return False


def getRandomPipe():
    # Get the Pipes in action.

    pipeHeight = GAMESPRITES['pipe'][0].get_height()
    offset = SCREENHEIGHT/3
    y2 = offset + random.randrange(0, int(SCREENHEIGHT - GAMESPRITES['base'].get_height() - 1.2*offset))
    pipex = SCREENWIDTH + 10
    y1 = pipeHeight - y2 + offset
    pipe = [
        {'x':pipex, 'y': -y1},
        {'x':pipex, 'y': y2}
    ]
    return pipe

if __name__ == "__main__":
    # From here We will be coding for the instructions of the game
    pygame.init()   # initialized with pygame, the pygame modules
    FPSCLOCK = pygame.time.Clock()
    pygame.display.set_caption("Flappy Bird")
    GAMESPRITES['numbers'] = (
        pygame.image.load('gallery/sprites/0.png').convert_alpha(),
        pygame.image.load('gallery/sprites/1.png').convert_alpha(),
        pygame.image.load('gallery/sprites/2.png').convert_alpha(),
        pygame.image.load('gallery/sprites/3.png').convert_alpha(),
        pygame.image.load('gallery/sprites/4.png').convert_alpha(),
        pygame.image.load('gallery/sprites/5.png').convert_alpha(),
        pygame.image.load('gallery/sprites/6.png').convert_alpha(),
        pygame.image.load('gallery/sprites/7.png').convert_alpha(),
        pygame.image.load('gallery/sprites/8.png').convert_alpha(),
        pygame.image.load('gallery/sprites/9.png').convert_alpha(),
    )
    # GAMESPRITES['message'] = pygame.image.load('gallery/sprites/message.png').convert_alpha()
    GAMESPRITES['base'] = pygame.image.load('gallery/sprites/base.png').convert_alpha()
    GAMESPRITES['pipe'] = (
        pygame.transform.rotate(pygame.image.load(PIPE).convert_alpha(), 180),
        pygame.image.load(PIPE).convert_alpha()
    )
    GAMESPRITES['background'] = pygame.image.load(BACKGROUND).convert()
    GAMESPRITES['player'] = pygame.image.load(PLAYER).convert_alpha()

    # Game Sounds
    GAMESOUNDS['die'] = pygame.mixer.Sound('gallery/audio/die.wav')
    GAMESOUNDS['hit'] = pygame.mixer.Sound('gallery/audio/hit.wav')
    GAMESOUNDS['point'] = pygame.mixer.Sound('gallery/audio/point.wav')
    GAMESOUNDS['swoosh'] = pygame.mixer.Sound('gallery/audio/swoosh.wav')
    GAMESOUNDS['wing'] = pygame.mixer.Sound('gallery/audio/wing.wav')

    while True:
        welcomeScreen() # Whenever A player clicks then it will start
        mainGame()  # This is the main Game Function
