### Spawners ###

### Importing Packets
import pygame
import os
import sys
from random import randint
from objects import *

### Defining Subroutines
def spawnPlayer(objList, sprGroup, WIDTH, HEIGHT):
    player = Player()
    player.pos = pygame.math.Vector2(WIDTH/2, HEIGHT/2)
    objList.insert(0, player)
    sprGroup.add(player)
    player.createTop(sprGroup)

def spawnEnemy(objList, sprGroup, WIDTH, HEIGHT):
    enemy = Enemy()
    while not enemy.checkSpawnPos(objList[0].pos, WIDTH, HEIGHT):
        enemy.pos = pygame.math.Vector2(randint(0, WIDTH), randint(0, HEIGHT))
    objList.append(enemy)
    sprGroup.add(enemy)
    enemy.createTop(sprGroup)
