### Board ###

### Importing Packets
import pygame
import os
import sys
from random import randint

### Defining Subroutines
def fillBoard(WIDTH, HEIGHT, board):
    NUMTILES = 28
    TILESIZE = 32
    if WIDTH % TILESIZE == 0:
        width = WIDTH // TILESIZE
    else:
        width = (WIDTH // TILESIZE) + 1
    if HEIGHT % TILESIZE == 0:
        height = HEIGHT // TILESIZE
    else:
        height = (HEIGHT // TILESIZE) + 1
    boardData = [[randint(0, NUMTILES - 1) for _ in range(0, width)] for _ in range(0, height)]
    for rowIndex, row in enumerate(boardData):
        for columnIndex, value in enumerate(row):
            board.blit(pygame.image.load(os.path.join(os.path.dirname(__file__),'Sprites',f'tile{value:03d}.png')), [columnIndex * TILESIZE, rowIndex * TILESIZE])
