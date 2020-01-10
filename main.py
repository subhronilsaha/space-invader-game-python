import pygame
import random
import math
from pygame import mixer

# Initialize Pygame
pygame.init()

# Create game screen
screen = pygame.display.set_mode((800, 600))

# Set title
pygame.display.set_caption("Space game")
icon = pygame.image.load('spaceship.png')
pygame.display.set_icon(icon)

# Player
playerImg = pygame.image.load('spaceship.png')
playerX = 370
playerY = 480
playerPositionChange = 0

def player(x, y):
    screen.blit(playerImg, (x, y))

# Enemy Alien
num_of_aliens = 6
alienImg = []
alienX = []
alienY = []
alienXChange = []
alienYChange = []

for i in range(num_of_aliens):
    alienImg.append(pygame.image.load('alien.png'))
    alienX.append(random.randint(30,700))
    alienY.append(random.randint(20, 150))
    alienXChange.append(3)
    alienYChange.append(50)

def alien(x, y, i):
    screen.blit(alienImg[i], (x, y))

# Bullets
bulletImg = pygame.image.load('bullet.png')
bulletX = 0
bulletY = 480
bulletXChange = 0
bulletYChange = 15
bulletState = 'ready' # States => 'ready': Bullet invisible; 'fire': Bullet Fired

def fire_bullet(x, y):
    global bulletState
    bulletState = 'fire'
    screen.blit(bulletImg, (x + 16, y + 10))

# Score
scoreValue = 0

font = pygame.font.Font('freesansbold.ttf', 30)
textX = 10
textY = 15

def display_score(x, y):
    score = font.render("Score: " + str(scoreValue), True, (0, 255, 0))
    screen.blit(score, (x, y))

# Collision Logic
def collides(alienX, alienY, bulletX, bulletY):
    distance = math.sqrt((math.pow(alienX - bulletX, 2)) + (math.pow(alienY - bulletY, 2)))
    if distance < 27:
        return True
    return False

# Game Over
gameover_font = pygame.font.Font('freesansbold.ttf', 80)

def game_over():
    gameover_text = gameover_font.render("GAME OVER", True, (255, 0, 0))
    screen.blit(gameover_text, (150, 250))

# Game loop
running = True
while running:

    screen.fill((0, 0, 0))

    for event in pygame.event.get():
        # Window is closed
        if event.type == pygame.QUIT:
            running = False
        
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                playerPositionChange -= 5
            if event.key == pygame.K_RIGHT:
                playerPositionChange += 5
            if event.key == pygame.K_SPACE:
                if bulletState == 'ready':
                    bulletSound = mixer.Sound('laser.wav')
                    bulletSound.play()
                    bulletX = playerX
                    fire_bullet(playerX, bulletY)
        
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                playerPositionChange = 0

    #Player movement
    playerX += playerPositionChange 
    
    if playerX < 30: # Boundaries
        playerX = 30
    if playerX > 700:
        playerX = 700

    player(playerX, playerY)
    
    # Enemy movement
    for i in range(num_of_aliens):
        alienX[i] += alienXChange[i]

        if alienY[i] >= 480:
            for j in range(num_of_aliens):
                alienY[j] = 800

            game_over()
            break

        if alienX[i] <= 30:
            alienXChange[i] = 3
            alienY[i] += alienYChange[i]
        elif alienX[i] >= 700:
            alienXChange[i] = -3
            alienY[i] += alienYChange[i]

        # Collision
        collision = collides(alienX[i], alienY[i], bulletX, bulletY)
        if collision:
            pop_sound = mixer.Sound('pop.wav')
            pop_sound.play()
            bulletY = 480
            bulletState = 'ready'
            scoreValue += 1
            alienX[i] = random.randint(30,700)
            alienY[i] = random.randint(20, 150)
        
        alien(alienX[i], alienY[i], i)


    # Bullet Movement
    if bulletY <= 0:
        bulletState = 'ready'
        bulletY = 480
    
    if bulletState == 'fire':
        fire_bullet(bulletX, bulletY)
        bulletY -= bulletYChange

    # Display Score
    display_score(textX, textY)

    pygame.display.update()