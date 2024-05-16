### Collisions ###

### Importing Packets
import pygame
import os
import sys
from random import randint

### Defining Collision Handlers
def bulletCollisionHandler(tanks, shots, spriteGroup):
    for tank in tanks:
        tankCollisionInfo = tank.collisionInfo
        for shot in shots:
            shotCollisionInfo = shot.collisionInfo
            distance, _ = ((tankCollisionInfo[0] - shotCollisionInfo[0]).rotate(-90)).as_polar()
            if distance < tankCollisionInfo[1] + shotCollisionInfo[1]:
                tank.damage = shot.damage
                shot.destroy(shots, spriteGroup)

def crateCollisionHandler(tanks, crates):
    tankCollisionInfo = tanks[0].collisionInfo
    for crate in crates:
        crateCollisionInfo = crate.collisionInfo
        distance, _ = ((tankCollisionInfo[0] - crateCollisionInfo[0]).rotate(-90)).as_polar()
        if distance < tankCollisionInfo[1] + crateCollisionInfo[1]:
            crate.loot(crates, tanks[0])

def tankCollisionHandler(tanks):
    raise NotImplementedError()
    for tank1 in tanks:
        for tank2 in tanks:
            if tank1 != tank2:
                pass
