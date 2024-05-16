### Tank Game - Ed Potter ###

### Importing Packets
import pygame
import os
import sys
from random import randint
from spawners import *
from collisions import *
from board import *

### __name__ Guard
if __name__ == "__main__":
    ### Initialising the pygame
    pygame.init()
    pygame.font.init()
    pygame.display.set_caption("Tank Game")

    debugFont = pygame.font.SysFont('Arial', 14)

    SIZE = WIDTH, HEIGHT = 800, 640
    screen = pygame.display.set_mode(SIZE)

    board = pygame.Surface(SIZE)
    fillBoard(WIDTH, HEIGHT, board)

    all_sprites_list = pygame.sprite.Group()

    tanks = []
    shots = []
    crates = []

    spawnPlayer(tanks, all_sprites_list, WIDTH, HEIGHT)

    ### Running the game
    FPSClock = pygame.time.Clock()
    FPS = 60
    Continue = True
    debug = False

    while Continue:
        ### Wipe the screen
        screen.blit(board, [0, 0])
        
        ### Go though events
        for event in pygame.event.get():
            if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                Continue = False
            if event.type == pygame.KEYDOWN and event.key == ord("i"):
                if debug:
                    debug = False
                else:
                    debug = True

            ### Getting Player Input
            tanks[0].fetchInput(event, tanks, shots, all_sprites_list)
        
        ### Updating Tank Positions
        tanks[0].update(board)
        tanks[0].checkPos(WIDTH, HEIGHT, tanks, all_sprites_list)
        for tank in tanks[1:]:
            tank.update(tanks, shots, crates, all_sprites_list, board)
            tank.checkPos(WIDTH, HEIGHT, tanks, crates, all_sprites_list)

        ### Basic Enemy Spawning
        if len(tanks) < 4:
            spawnEnemy(tanks, all_sprites_list, WIDTH, HEIGHT)

        ### Updating Shot Positions
        for shot in shots:
            shot.update()
            shot.checkPos(WIDTH, HEIGHT, shots, all_sprites_list)
        
        ### Handling Collisions
        bulletCollisionHandler(tanks, shots, all_sprites_list)
        crateCollisionHandler(tanks, crates)

        ### Drawing Sprites and Status'
        for crate in crates:
            crate.draw(screen)
        all_sprites_list.draw(screen)
        tanks[0].drawStatus(screen, debug, debugFont)
        for tank in tanks[1:]:
            tank.drawStatus(screen)
        if debug:
            for tank in tanks:
                tank.drawImageBox(screen)
                tank.drawHitbox(screen)
            for shot in shots:
                shot.drawImageBox(screen)
                shot.drawHitbox(screen)
            for crate in crates:
                crate.drawImageBox(screen)
                crate.drawHitbox(screen)
        pygame.display.flip()

        FPSClock.tick(FPS)

    pygame.quit()
