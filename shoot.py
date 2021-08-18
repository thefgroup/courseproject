
import pygame, random, sys, time
from pygame.locals import *

#set up some variables
WINDOWWIDTH = 1024
WINDOWHEIGHT = 600
FPS = 60

MAXGOTTENPASS = 10
GHOSTSIZE = 70 #includes newKindGhost
ADDNEWGHOSTRATE = 30
ADDNEWKINDGHOST = ADDNEWGHOSTRATE

NORMALGHOSTSPEED = 2
NEWKINDGHOSTSPEED = NORMALGHOSTSPEED / 2

PLAYERMOVERATE = 15
BULLETSPEED = 10
ADDNEWBULLETRATE = 15

TEXTCOLOR = (255, 255, 255)
RED = (255, 0, 0)

def terminate(): 
    pygame.quit() 
    sys.exit() 

def waitForPlayerToPressKey():
    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                terminate()
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE: # pressing escape quits
                    terminate()
                if event.key == K_RETURN:
                    return

def playerHasHitGhost(playerRect, ghost):
    for z in ghost:
        if playerRect.colliderect(z['rect']):
            return True
    return False

def bulletHasHitGhost(bullets, ghost):
    for b in bullets:
        if b['rect'].colliderect(z['rect']):
            bullets.remove(b)
            return True
    return False

def bulletHasHitCrawler(bullets, newKindGhost):
    for b in bullets:
        if b['rect'].colliderect(c['rect']):
            bullets.remove(b)
            return True
    return False

def drawText(text, font, surface, x, y):
    textobj = font.render(text, 1, TEXTCOLOR)
    textrect = textobj.get_rect()
    textrect.topleft = (x, y)
    surface.blit(textobj, textrect)

# set up pygame, the window, and the mouse cursor
pygame.init()
mainClock = pygame.time.Clock()
windowSurface = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT))#, pygame.FULLSCREEN)
pygame.display.set_caption('Ghost Forest')
pygame.mouse.set_visible(False)

# set up fonts
font = pygame.font.SysFont(None, 48)

# set up sounds
gameOverSound = pygame.mixer.Sound('gameover.wav')
pygame.mixer.music.load('grasswalk.mp3')

# set up images
playerImage = pygame.image.load('CuteShooter.png')
playerRect = playerImage.get_rect()

bulletImage = pygame.image.load('FireShoot.png')
bulletRect = bulletImage.get_rect()

ghostImage = pygame.image.load('tree.png')
newKindGhostImage = pygame.image.load('blinky.png')

backgroundImage = pygame.image.load('hantu3.jpg')
rescaledBackground = pygame.transform.scale(backgroundImage, (WINDOWWIDTH, WINDOWHEIGHT))

# show the "Start" screen
windowSurface.blit(rescaledBackground, (0, 0))
windowSurface.blit(playerImage, (WINDOWWIDTH / 2.3, WINDOWHEIGHT - 110))
drawText('Ghost Forest by team F', font, windowSurface, (WINDOWWIDTH / 3), (WINDOWHEIGHT / 4))
drawText('Press Enter to start', font, windowSurface, (WINDOWWIDTH / 2.7) - 5, (WINDOWHEIGHT / 3) + 50)
pygame.display.update()
waitForPlayerToPressKey()
while True:
    # set up the start of the game
    
    ghost = []
    newKindGhost = []
    bullets = []

    ghostGottenPast = 0
    score = 0
    
    playerRect.topleft = (50, WINDOWHEIGHT /2)
    moveLeft = moveRight = False
    moveUp=moveDown = False
    shoot = False
    
    ghostAddCounter = 0
    newKindGhostAddCounter = 0
    bulletAddCounter = 40
    pygame.mixer.music.play(-1, 0.0)


    while True: # the game loop runs while the game part is playing
        for event in pygame.event.get():
            if event.type == QUIT:
                terminate()

            if event.type == KEYDOWN:
                if event.key == K_UP or event.key == ord('w'):
                    moveDown = False
                    moveUp = True
                if event.key == K_DOWN or event.key == ord('s'):
                    moveUp = False
                    moveDown = True

                if event.key == K_SPACE:
                    shoot = True

            if event.type == KEYUP:
                if event.key == K_ESCAPE:
                        terminate()

                if event.key == K_UP or event.key == ord('w'):
                    moveUp = False
                if event.key == K_DOWN or event.key == ord('s'):
                    moveDown = False
                
                if event.key == K_SPACE:
                    shoot = False

        # Add new ghost at the top of the screen, if needed.
        ghostAddCounter += 1
        if ghostAddCounter == ADDNEWKINDGHOST:
            ghostAddCounter = 0
            ghostSize = GHOSTSIZE       
            newGhost = {'rect': pygame.Rect(WINDOWWIDTH, random.randint(10,WINDOWHEIGHT-ghostSize-10), ghostSize, ghostSize),
                        'surface':pygame.transform.scale(ghostImage, (ghostSize, ghostSize)),
                        }

            ghost.append(newGhost)

        # Add new newKindGhosts at the top of the screen, if needed.
        newKindGhostAddCounter += 1
        if newKindGhostAddCounter == ADDNEWGHOSTRATE:
            newKindGhostAddCounter = 0
            newKindGhostsize = GHOSTSIZE
            newCrawler = {'rect': pygame.Rect(WINDOWWIDTH, random.randint(10,WINDOWHEIGHT-newKindGhostsize-10), newKindGhostsize, newKindGhostsize),
                        'surface':pygame.transform.scale(newKindGhostImage, (newKindGhostsize, newKindGhostsize)),
                        }
            newKindGhost.append(newCrawler)


        # add new bullet
        bulletAddCounter += 1
        if bulletAddCounter >= ADDNEWBULLETRATE and shoot == True:
            bulletAddCounter = 0
            newBullet = {'rect':pygame.Rect(playerRect.centerx+10, playerRect.centery-25, bulletRect.width, bulletRect.height),
						 'surface':pygame.transform.scale(bulletImage, (bulletRect.width, bulletRect.height)),
						}
            bullets.append(newBullet)

        # Move the player around.
        if moveUp and playerRect.top > 30:
            playerRect.move_ip(0,-1 * PLAYERMOVERATE)
        if moveDown and playerRect.bottom < WINDOWHEIGHT-10:
            playerRect.move_ip(0,PLAYERMOVERATE)

        # Move the ghost down.
        for z in ghost:
            z['rect'].move_ip(-1*NORMALGHOSTSPEED, 0)

        # Move the newKindGhost down.
        for c in newKindGhost:
            c['rect'].move_ip(-1*NEWKINDGHOSTSPEED,0)

        # move the bullet
        for b in bullets:
            b['rect'].move_ip(1 * BULLETSPEED, 0)

# Delete ghost that have fallen past the bottom.
        for z in ghost[:]:
            if z['rect'].left < 0:
                ghost.remove(z)
                ghostGottenPast += 1

        # Delete newKindGhost that have fallen past the bottom.
        for c in newKindGhost[:]:
            if c['rect'].left <0:
                newKindGhost.remove(c)
                ghostGottenPast += 1
        
        for b in bullets[:]:
            if b['rect'].right>WINDOWWIDTH:
                bullets.remove(b)
                
        # check if the bullet has hit the ghost
        for z in ghost:
            if bulletHasHitGhost(bullets, ghost):
                score += 1
                ghost.remove(z)
    
        for c in newKindGhost:
            if bulletHasHitCrawler(bullets, newKindGhost):
                score += 1
                newKindGhost.remove(c)     
# Draw the game world on the window.
        windowSurface.blit(rescaledBackground, (0, 0))

        # Draw the player's rectangle, rails
        windowSurface.blit(playerImage, playerRect)

        # Draw each baddie
        for z in ghost:
            windowSurface.blit(z['surface'], z['rect'])

        for c in newKindGhost:
            windowSurface.blit(c['surface'], c['rect'])

        # draw each bullet
        for b in bullets:
            windowSurface.blit(b['surface'], b['rect'])

        # Draw the score and how many ghost got past
        drawText('ghost gotten past: %s' % (ghostGottenPast), font, windowSurface, 10, 20)
        drawText('score: %s' % (score), font, windowSurface, 10, 50)

        # update the display
        pygame.display.update()
            
        # Check if any of the ghost has hit the player.
        if playerHasHitGhost(playerRect, ghost):
            break
        if playerHasHitGhost(playerRect, newKindGhost):
           break
        
        # check if score is over MAXGOTTENPASS which means game over
        if ghostGottenPast >= MAXGOTTENPASS:
            break

        mainClock.tick(FPS)

    # Stop the game and show the "Game Over" screen.
    pygame.mixer.music.stop()
    gameOverSound.play()
    time.sleep(1)
    if ghostGottenPast >= MAXGOTTENPASS:
        windowSurface.blit(rescaledBackground, (0, 0))
        windowSurface.blit(playerImage, (WINDOWWIDTH / 2, WINDOWHEIGHT - 70))
        drawText('score: %s' % (score), font, windowSurface, 10, 30)
        drawText('GAME OVER', font, windowSurface, (WINDOWWIDTH / 3), (WINDOWHEIGHT / 3))
        drawText('YOUR COUNTRY HAS BEEN DESTROIED', font, windowSurface, (WINDOWWIDTH / 4)- 80, (WINDOWHEIGHT / 3) + 100)
        drawText('Press enter to play again or escape to exit', font, windowSurface, (WINDOWWIDTH / 4) - 80, (WINDOWHEIGHT / 3) + 150)
        pygame.display.update()
        waitForPlayerToPressKey()
    if playerHasHitGhost(playerRect, ghost):
        windowSurface.blit(rescaledBackground, (0, 0))
        windowSurface.blit(playerImage, (WINDOWWIDTH / 2, WINDOWHEIGHT - 70))
        drawText('score: %s' % (score), font, windowSurface, 10, 30)
        drawText('GAME OVER', font, windowSurface, (WINDOWWIDTH / 3), (WINDOWHEIGHT / 3))
        drawText('YOU HAVE BEEN KISSED BY THE ZOMMBIE', font, windowSurface, (WINDOWWIDTH / 4) - 80, (WINDOWHEIGHT / 3) +100)
        drawText('Press enter to play again or escape to exit', font, windowSurface, (WINDOWWIDTH / 4) - 80, (WINDOWHEIGHT / 3) + 150)
        pygame.display.update()
        waitForPlayerToPressKey()
    gameOverSound.stop()
