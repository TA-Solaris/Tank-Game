### Objects ###

### Importing Packets
import pygame
import os
import sys
from random import randint

### Defining Classes
class Tank(pygame.sprite.Sprite):
    def __init__(self):
        ### Pygame Sprite
        pygame.sprite.Sprite.__init__(self)
        self.images = []

        ### Object Variables
        self._MOVESPEED = 1.5
        self._ROTSPEED = 1.6
        self.HPMAX = 100
        self._pos = pygame.math.Vector2(0, 0)
        self._vel = pygame.math.Vector2(0, 0)
        self._angle = randint(0, 360)
        self._anglevel = 0
        self._COOLDOWNTIME = 60
        self._shootcooldown = 0
        self._RADIUS = 16
        self._HITRADIUS = 16

    @property
    def pos(self):
        return self._pos
    
    @pos.setter
    def pos(self, n_pos):
        if n_pos.x >= 0 and n_pos.y >= 0:
            self._pos.x, self._pos.y = n_pos.x, n_pos.y
    
    @property
    def HPMAX(self):
        raise NameError()
    
    @HPMAX.setter
    def HPMAX(self, n_HPVALUE):
        self._HPMAX = n_HPVALUE
        self._hp = n_HPVALUE
    
    @property
    def damage(self):
        raise NameError()

    @damage.setter
    def damage(self, amount):
        self._hp += -amount
    
    @property
    def collisionInfo(self):
        return [self._pos, self._HITRADIUS]
    
    def drawTread(self, bgSurface):
        tread = pygame.image.load(os.path.join(os.path.dirname(__file__),'Sprites','tanktread.png')).convert()
        tread.convert_alpha()
        tread.set_colorkey([0, 0, 255])
        tread = pygame.transform.rotate(tread, 360 - self._angle)
        treadrect = tread.get_rect()
        treadrect.center = self._pos
        bgSurface.blit(tread, [treadrect.left, treadrect.top])

    def drawImageBox(self, screen):
        WHITE = [255, 255, 255]
        pygame.draw.rect(screen, WHITE, self.rect, 2)
    
    def drawHitbox(self, screen):
        YELLOW = [255, 255, 0]
        pygame.draw.circle(screen, YELLOW, [int(self._pos.x), int(self._pos.y)], self._HITRADIUS, 2)
    
    def leftTurn(self):
        self._anglevel = -self._ROTSPEED
    
    def rightTurn(self):
        self._anglevel = self._ROTSPEED
    
    def stopTurn(self):
        self._anglevel = 0
    
    def forwardMove(self):
        self._vel = pygame.math.Vector2(0, -self._MOVESPEED).rotate(self._angle)
        self._anglevel = 0
    
    def backwardMove(self):
        self._vel = pygame.math.Vector2(0, self._MOVESPEED / 2).rotate(self._angle)
        self._anglevel = 0
    
    def stopMove(self):
        self._vel = self._vel = pygame.math.Vector2(0, 0)

    def shoot(self, shotList, spriteGroup):
        if self._shootcooldown == 0:
            self.top.shoot(shotList, spriteGroup)
            self._shootcooldown += self._COOLDOWNTIME
    
    def checkPos(self, WIDTH, HEIGHT, tankList, spriteGroup):
        if self._pos.x < -self._RADIUS or self._pos.y < -self._RADIUS or self._pos.x > WIDTH + self._RADIUS or self._pos.y > HEIGHT + self._RADIUS:
            self.destroy(tankList, spriteGroup)

    def destroy(self, tankList, spriteGroup):
        self.top.destroy(spriteGroup)
        spriteGroup.remove(self)
        tankList.remove(self)

class Player(Tank):
    def __init__(self):
        ### Calling Tanks Constructor
        super().__init__()

        ### Pygame Sprite
        img = pygame.image.load(os.path.join(os.path.dirname(__file__),'Sprites','tankbase1.png')).convert()
        img.convert_alpha()
        img.set_colorkey([0, 0, 255])
        self.images.append(img)
        self.image = self.images[0]
        self.rect = self.image.get_rect()

        ### Object Variables
        self._BOOSTMULTIPLIER = 2
        self._boostflag= False
        self._BOOSTMAX = 100
        self._boost = self._BOOSTMAX
    
    def heal(self, amount):
        self._hp += amount
        if self._hp > self._HPMAX:
            self._hp = self._HPMAX

    def createTop(self, spriteGroup):
        self.top = PlayerTop(self._pos, self._angle)
        spriteGroup.add(self.top)

    def drawStatus(self, screen, debug, debugFont):
        SCALE = 3

        BLACK = [0, 0, 0]
        RED = [255, 0, 0]
        GREEN = [0, 255, 0]
        CYAN = [0, 255, 255]
        GREY = [211,211,211]

        pygame.draw.rect(screen, BLACK, [4, 4, self._HPMAX * SCALE + 2, 5 * SCALE + 2])
        pygame.draw.rect(screen, BLACK, [4, 4 + 5 * (SCALE + 1), self._BOOSTMAX * SCALE + 2, 5 * SCALE + 2])
        pygame.draw.rect(screen, RED, [5, 5, self._HPMAX * SCALE, 5 * SCALE])
        pygame.draw.rect(screen, GREY, [5, 5 * (SCALE + 2), self._BOOSTMAX * SCALE, 5 * SCALE])
        if self._hp > 0:
            pygame.draw.rect(screen, GREEN, [5, 5, self._hp * SCALE, 5 * SCALE])
        if self._boost > 0:
            pygame.draw.rect(screen, CYAN, [5, 5 * (SCALE + 2), self._boost * SCALE, 5 * SCALE])
        if debug:
            screen.blit(debugFont.render(f"{self._hp} / {self._HPMAX}", False, BLACK), (5, 5))
            screen.blit(debugFont.render(f"{self._boost} / {self._BOOSTMAX}", False, BLACK), (5, 5 * (SCALE + 2)))
            screen.blit(debugFont.render(f"Player Pos (X / Y): {self._pos.x} / {self._pos.y}", False, BLACK), (5, 5 * (SCALE + 5)))
            screen.blit(debugFont.render(f"Player Facing: {self._angle}", False, BLACK), (5, 5 * (SCALE + 5) + 15))
            velSpeed, velAngle = (self._vel.rotate(-90)).as_polar()
            if velSpeed > 0:
                velAngle += 180
            screen.blit(debugFont.render(f"Player Velocity (Speed / Angle): {velSpeed} / {velAngle}", False, BLACK), (5, 5 * (SCALE + 5) + (15 * 2)))
            screen.blit(debugFont.render(f"Player Rotatioanl Velocity: {self._anglevel}", False, BLACK), (5, 5 * (SCALE + 5) + (15 * 3)))
            screen.blit(debugFont.render(f"Player Shot Cooldown: {self._shootcooldown}", False, BLACK), (5, 5 * (SCALE + 5) + (15 * 4)))
            screen.blit(debugFont.render(f"Player Top Facing: {self.top.facing}", False, BLACK), (5, 5 * (SCALE + 5) + (15 * 5)))
    
    def checkPos(self, WIDTH, HEIGHT, tankList, spriteGroup):
        if self._pos.x < 0:
            self._pos.x = 0
        if self._pos.y < 0:
            self._pos.y = 0
        if self._pos.x > WIDTH:
            self._pos.x = WIDTH
        if self._pos.y > HEIGHT:
            self._pos.y = HEIGHT
        self.rect.center = self._pos

    def fetchInput(self, event, tankList, shotList, spriteGroup):
        if event.type == pygame.KEYDOWN:
            if self._vel == pygame.math.Vector2(0, 0):
                if event.key == ord('a'):
                    self.leftTurn()
                if event.key == ord('d'):
                    self.rightTurn()
            if event.key == ord('w'):
                self.forwardMove()
            if event.key == ord('s'):
                self.backwardMove()
            if event.key == pygame.K_LSHIFT:
                self._boostflag= True
        
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                self.shoot(shotList, spriteGroup)

        if event.type == pygame.KEYUP:
            if event.key == ord('a') or event.key == ord('d'):
                self.stopTurn()
            if event.key == ord('w') or event.key == ord('s'):
                self.stopMove()
            if event.key == pygame.K_LSHIFT:
                self._boostflag= False
    
    def update(self, bgSurface):
        if self._boostflag:
            self._angle = (self._angle + self._anglevel * self._ROTSPEED * self._BOOSTMULTIPLIER) % 360
            self._pos += self._vel * self._BOOSTMULTIPLIER
            self._boost += -1
            if self._boost <= 0:
                self._boostflag= False
        else:
            self._angle = (self._angle + self._anglevel * self._ROTSPEED) % 360
            self._pos += self._vel
            if self._boost < self._BOOSTMAX and self._vel == pygame.math.Vector2(0, 0) and self._anglevel == 0:
                self._boost += 1
            elif self._boost < self._BOOSTMAX:
                self._boost += 0.25
            if self._boost > self._BOOSTMAX:
                self._boost = self._BOOSTMAX
        self.image = pygame.transform.rotate(self.images[0], 360 - self._angle)
        self.rect = self.image.get_rect()
        self.rect.center = self._pos
        self.top.update(self._pos, pygame.mouse.get_pos())
        self.drawTread(bgSurface)
        if self._shootcooldown > 0:
            self._shootcooldown += -1

class Enemy(Tank):
    def __init__(self):
        ### Calling Tanks Constructor
        super().__init__()

        ### Pygame Sprite
        img = pygame.image.load(os.path.join(os.path.dirname(__file__),'Sprites','tankbase2.png')).convert()
        img.convert_alpha()
        img.set_colorkey([0, 0, 255])
        self.images.append(img)
        self.image = self.images[0]
        self.rect = self.image.get_rect()

        ### Object Variables
        self._SPAWNBAND = 64
        self._DISTANCERANGE = randint(140, 280)
        self._ANGLERANGE = randint(15, 25)
        self._ABNORMALITY = randint(40, 120)

        ### Making them worse than the player (because they are way to hard)
        self._COOLDOWNTIME = 200
        self.HPMAX = 20
        self._MOVESPEED = 1
        self._ROTSPEED = 1
    
    def createTop(self, spriteGroup):
        self.top = EnemyTop(self._pos, self._angle)
        spriteGroup.add(self.top)
    
    def drawStatus(self, screen):
        HEIGHTABOVE = 9
        LENGTH = 33

        BLACK = [0, 0, 0]
        RED = [255, 0, 0]
        GREEN = [0, 255, 0]

        pygame.draw.rect(screen, BLACK, [self._pos.x - 18, self._pos.y - (16 + HEIGHTABOVE), LENGTH + 2, 7])
        pygame.draw.rect(screen, RED, [self._pos.x - 17, self._pos.y - (15 + HEIGHTABOVE), LENGTH, 5])
        if self._hp > 0:
            pygame.draw.rect(screen, GREEN, [self._pos.x - 17, self._pos.y - (15 + HEIGHTABOVE), (self._hp * LENGTH) // self._HPMAX, 5])
    
    def fetchPath(self, tankList, shotList, spriteGroup):
        testVector = tankList[0].pos - self._pos
        distance, angle = (testVector.rotate(-90)).as_polar()
        angle += 180
        abnormality = randint(0, self._ABNORMALITY)
        if self._angle > angle:
            testAngle = self._angle - angle
        else:
            testAngle = angle - self._angle
        if distance <= self._DISTANCERANGE:
            self.stopMove()
            self.stopTurn()
            self.shoot(shotList, spriteGroup)
        elif abs(self._angle - angle) < self._ANGLERANGE or (360 - abs(self._angle - angle)) < self._ANGLERANGE:
            self.forwardMove()
            self.stopTurn()
        elif abnormality <= 20:
            if abnormality == 1:
                self.shoot(shotList, spriteGroup)
            else:
                self.forwardMove()
                self.stopTurn()
        else:
            self.rotateTowardAngle(angle)
            self.stopMove()

    def rotateTowardAngle(self, angle):
        if self._angle > angle:
            testAngle = self._angle - angle
            if testAngle > 360 - testAngle:
                self.rightTurn()
                self.stopMove()
            else:
                self.leftTurn()
                self.stopMove()
        else:
            testAngle = angle - self._angle
            if testAngle > 360 - testAngle:
                self.leftTurn()
                self.stopMove()
            else:
                self.rightTurn()
                self.stopMove()
    
    def checkPos(self, WIDTH, HEIGHT, tankList, lootList, spriteGroup):
        if self._pos.x < -self._RADIUS or self._pos.y < -self._RADIUS or self._pos.x > WIDTH + self._RADIUS or self._pos.y > HEIGHT + self._RADIUS:
            self.destroy(tankList, lootList, spriteGroup)

    def checkSpawnPos(self, playerPos, WIDTH, HEIGHT):
        testVector = playerPos - self._pos
        distance, _ = (testVector.rotate(-90)).as_polar()
        if self._pos.x >= self._SPAWNBAND and self._pos.y >= self._SPAWNBAND and self._pos.x <= WIDTH - self._SPAWNBAND and self._pos.y <= HEIGHT - self._SPAWNBAND and distance > self._DISTANCERANGE:
            return True
        else:
            return False

    def update(self, tankList, shotList, lootList, spriteGroup, bgSurface):
        self.fetchPath(tankList, shotList, spriteGroup)
        self._angle = (self._angle + self._anglevel * self._ROTSPEED) % 360
        self.image = pygame.transform.rotate(self.images[0], 360 - self._angle)
        self.rect = self.image.get_rect()
        self._pos += self._vel
        self.rect.center = self._pos
        self.top.update(self._pos, tankList[0].pos)
        self.drawTread(bgSurface)
        if self._hp <= 0:
            ash = pygame.image.load(os.path.join(os.path.dirname(__file__),'Sprites','ash.png')).convert()
            ash.convert_alpha()
            ash.set_colorkey([0, 0, 255])
            ashrect = ash.get_rect()
            ashrect.center = self._pos
            bgSurface.blit(ash, [ashrect.left, ashrect.top])
            self.destroy(tankList, lootList, spriteGroup)
        if self._shootcooldown > 0:
            self._shootcooldown += -1
        
    def destroy(self, tankList, lootList, spriteGroup):
        chance = randint(0, 2)
        if chance == 1 or chance == 2:
            medCrate = MedicalCrate(self._pos)
            lootList.append(medCrate)
        super().destroy(tankList, spriteGroup)

class TankTop(pygame.sprite.Sprite):
    def __init__(self, pos, angle):
        ### Pygame Sprite
        pygame.sprite.Sprite.__init__(self)
        self.images = []

        ### Object Variables
        self._ROTSPEED = 1.6
        self._pos = pos
        self._angle = angle
        self._anglevel = 0
    
    @property
    def facing(self):
        return self._angle

    def leftTurn(self):
        self._anglevel = -self._ROTSPEED
    
    def rightTurn(self):
        self._anglevel = self._ROTSPEED
    
    def stopTurn(self):
        self._anglevel = 0
    
    def rotateTowardAngle(self, angle):
        if self._angle > angle:
            testAngle = self._angle - angle
            if testAngle > 360 - testAngle:
                self.rightTurn()
            else:
                self.leftTurn()
        else:
            testAngle = angle - self._angle
            if testAngle > 360 - testAngle:
                self.leftTurn()
            else:
                self.rightTurn()

    def update(self, pos, otherPos):
        _, angle = ((otherPos - pos).rotate(-90)).as_polar()
        angle += 180
        self.rotateTowardAngle(angle)
        self._angle = (self._angle + self._anglevel * self._ROTSPEED) % 360
        self._pos = pos
        self.image = pygame.transform.rotate(self.images[0], 360 - self._angle)
        self.rect = self.image.get_rect()
        self.rect.center = self._pos
    
    def shoot(self, shotList, spriteGroup):
        newShell = Shell(self._angle, self._pos)
        shotList.append(newShell)
        spriteGroup.add(newShell)
    
    def destroy(self, spriteGroup):
        spriteGroup.remove(self)

class PlayerTop(TankTop):
    def __init__(self, pos, angle):
        ### Calling Tanktops Constructor
        super().__init__(pos, angle)

        ### Pygame Sprite
        img = pygame.image.load(os.path.join(os.path.dirname(__file__),'Sprites','tanktop1.png')).convert()
        img.convert_alpha()
        img.set_colorkey([0, 0, 255])
        self.images.append(img)
        self.image = self.images[0]
        self.rect = self.image.get_rect()

class EnemyTop(TankTop):
    def __init__(self, pos, angle):
        ### Calling Tanks Constructor
        super().__init__(pos, angle)

        ### Pygame Sprite
        img = pygame.image.load(os.path.join(os.path.dirname(__file__),'Sprites','tanktop2.png')).convert()
        img.convert_alpha()
        img.set_colorkey([0, 0, 255])
        self.images.append(img)
        self.image = self.images[0]
        self.rect = self.image.get_rect()

class Shell(pygame.sprite.Sprite):
    def __init__(self, ANGLE, pos):
        ### Object Variables
        self._RADIUS = 4
        self._ANGLE = ANGLE
        self._pos = pygame.math.Vector2(pos.x, pos.y) + pygame.math.Vector2(0, -20).rotate(self._ANGLE)
        self._MAXVELOCITY = 6
        self._VEL = pygame.math.Vector2(0, -self._MAXVELOCITY).rotate(self._ANGLE)
        self._damage = 5

        ### Pygame Sprite
        pygame.sprite.Sprite.__init__(self)
        self.images = []
        img = pygame.image.load(os.path.join(os.path.dirname(__file__),'Sprites','shell.png')).convert()
        img.convert_alpha()
        img.set_colorkey([0, 0, 255])
        self.images.append(img)
        self.image = self.images[0]
        self.image = pygame.transform.rotate(self.images[0], 360 - self._ANGLE)
        self.rect = self.image.get_rect()
        self._HITRADIUS = 6
    
    @property
    def collisionInfo(self):
        return [self._pos, self._HITRADIUS]
    
    @property
    def damage(self):
        return self._damage
    
    def drawImageBox(self, screen):
        WHITE = [255, 255, 255]
        pygame.draw.rect(screen, WHITE, self.rect, 2)
    
    def drawHitbox(self, screen):
        YELLOW = [255, 255, 0]
        pygame.draw.circle(screen, YELLOW, [int(self._pos.x), int(self._pos.y)], self._HITRADIUS, 2)
    
    def checkPos(self, WIDTH, HEIGHT, shotList, spriteGroup):
        if self._pos.x < -self._RADIUS or self._pos.y < -self._RADIUS or self._pos.x > WIDTH + self._RADIUS or self._pos.y > HEIGHT + self._RADIUS:
            self.destroy(shotList, spriteGroup)

    def update(self):
        self._pos += self._VEL
        self.rect.center = self._pos

    def destroy(self, shotList, spriteGroup):
        spriteGroup.remove(self)
        shotList.remove(self)

class LootCrate(pygame.sprite.Sprite):
    def __init__(self, pos):
        ### Pygame Sprite
        pygame.sprite.Sprite.__init__(self)
        self.images = []
        img = pygame.image.load(os.path.join(os.path.dirname(__file__),'Sprites','lootcrate.png')).convert()
        img.convert_alpha()
        img.set_colorkey([0, 0, 255])
        self.images.append(img)
        self.image = self.images[0]
        self.rect = self.image.get_rect()
        self.rect.center = pos

        ### Object Variables
        self._pos = pos
        self._HITRADIUS = 9
    
    @property
    def collisionInfo(self):
        return [self._pos, self._HITRADIUS]
    
    def drawImageBox(self, screen):
        WHITE = [255, 255, 255]
        pygame.draw.rect(screen, WHITE, self.rect, 2)
    
    def drawHitbox(self, screen):
        YELLOW = [255, 255, 0]
        pygame.draw.circle(screen, YELLOW, [int(self._pos.x), int(self._pos.y)], self._HITRADIUS, 2)
    
    def loot(self, lootList):
        self.destroy(lootList)
    
    def draw(self, screen):
        screen.blit(self.image, self.rect)

    def destroy(self, lootList):
        lootList.remove(self)

class MedicalCrate(LootCrate):
    def __init__(self, pos):
        ### Calling LootCrates Constructor
        super().__init__(pos)

        ### Pygame Sprite
        img = pygame.image.load(os.path.join(os.path.dirname(__file__),'Sprites','lootcrate1.png')).convert()
        img.convert_alpha()
        img.set_colorkey([0, 0, 255])
        self.images.insert(0, img)
        self.image = self.images[0]
        self.rect = self.image.get_rect()
        self.rect.center = self._pos

        ### Object Variables
        self._HEALAMOUNT = 20
    
    def loot(self, lootList, player):
        player.heal(self._HEALAMOUNT)
        super().loot(lootList)
