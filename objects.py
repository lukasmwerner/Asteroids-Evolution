from typing import List
import pygame
import random
import math

from pygame.math import Vector2

from NeuralNet import Brain

UP = pygame.Vector2(0, -1)



class PygameObject(object):
    __DEBUG__ = False
    def __init__(self, image, x,y, velocity, size = 16,):
        self.image = pygame.image.load(image)
        self.size = size
        self.img_size = size
        self.image = pygame.transform.scale(self.image, (size,size))
        self.position = pygame.Vector2((x,y))
        self.velocity = pygame.Vector2(velocity)
        self.direction = pygame.Vector2(UP)

    def show(self, screen: pygame.display):
        img = pygame.transform.rotozoom(self.image, self.direction.angle_to(UP), 1)
        img_size = pygame.Vector2(img.get_size())
        blit_position = self.position - img_size * 0.5
        if self.__DEBUG__:
            pygame.draw.circle(screen, (255, 0, 0), self.position, self.size)
        screen.blit(img, blit_position)

    def update(self):
        self.position = self.position + self.velocity

        if self.position.x < 0:
            self.position.x = 500
        elif self.position.x > 500:
            self.position.x = 0
        if self.position.y < 0:
            self.position.y = 500
        elif self.position.y > 500:
            self.position.y = 0

    def rotate(self, direction = 1):
        self.direction.rotate_ip(3*direction)

    def addVelocity(self,velo):
        self.velocity += self.direction * velo
    def removeVelocity(self, velo):
        self.velocity -= self.direction * velo

    def collider(self, other) -> bool:
        distance = self.position.distance_to(other.position)
        return distance < self.size + other.size
        otherBoundsCollider = pygame.Rect(other.position.x, other.position.y, other.size, other.size)
        selfCollider = pygame.Rect(self.position.x, self.position.y, self.size, self.size)
        return selfCollider.colliderect(otherBoundsCollider)


pi = math.pi

def PointsInCircum(r,c,n=5):
    return [
        (c[0]+math.cos(2*pi/n*x)*r,
        c[1]+math.sin(2*pi/n*x)*r) 
        for x in range(0,n+1)
    ]

class Projectile(PygameObject):
    def __init__(self, x, y, velocity: pygame.Vector2, size=6):
        super().__init__("assets/block.png", x, y, 0.5, size=size)
        self.velocity = Vector2(velocity)
        self.decay = 1000
    def update(self):
        self.decay -= 1
        if self.decay <= 0:
            return True
        super().update()
    

class Asteroid(PygameObject):
    def __init__(self, image="assets/asteroid.png", x=-1, y=-1, size=-1):

        if x == -1 and y == -1:    
            rand_x = random.randrange(0, 500, 10)
            rand_y = random.randrange(0, 500, 10)
            if rand_x > 150 and rand_x < 350:
                if rand_y > 150 and rand_y < 350:
                    if rand_x > 150 and rand_x < 350:
                        rand_x += 200 * random.choice([-1, 1])
                    if rand_y > 150 and rand_y < 350:
                        rand_y += 200 * random.choice([-1, 1])
            if size == -1:
                size=random.randrange(16, 64, 8)
            super().__init__(image, rand_x,rand_y, 0.05, size)
            self.rotate(random.randrange(1, 10)* random.choice([-1, 1]))
        else:
            if size == -1:
                size=random.randrange(16, 64, 8)
            super().__init__(image, x,y, 0.05, size)
            self.rotate(random.randrange(1, 10)* random.choice([-1, 1])) 
        self.addVelocity(random.random())
        if self.size == 64:
            self.img_size = 120
        elif self.size == 32:
            self.img_size = 64
        elif self.size == 16:
            self.img_size = 32
    
    def update(self):
        super().update()

    def set_position(self, x,y):
        self.position.x = x
        self.position.y = y

    def split(self):
        asteroids = []
        for _ in range(2):
            ss = self.size/2
            if ss > 8:
                a = Asteroid(x=self.position.x, y=self.position.y, size=ss)
                a.addVelocity(random.random())
                asteroids.append(a)
        self.size = 0
        return asteroids

class Spaceship(PygameObject):
    def __init__(self, image="assets/spaceship.png", size = 32):
        super().__init__(image, 250, 250, 0, size)
        self.size = 18
        self.img_size = 32
        self.ray_points = PointsInCircum(40, self.position, n=10) + PointsInCircum(80, self.position, n=6)
        
    def update(self):
        super().update()
        self.ray_points = PointsInCircum(40, self.position, n=10) + PointsInCircum(80, self.position, n=6)

    def show(self, screen: pygame.display):
        super().show(screen)
        for pt in self.ray_points:
            pygame.draw.circle(screen, (0, 255, 255), (pt[0], pt[1]), 4)

    def asteroid_in_range(self, asteroid: Asteroid)->List[bool]:
        vision = []
        for pt in self.ray_points:
            vision.append(asteroid.collider(PygameObject(image="assets/asteroid.png", x=pt[0], y=pt[1], velocity=0, size=1)))
        return vision
    
    def check_vision(self, asteroids: List[Asteroid])->List[bool]:
        vision = [False for i in range (len(self.ray_points))]
        for asteroid in asteroids:
            results = self.asteroid_in_range(asteroid)
            for i in range(len(results)):
                if results[i]:
                    vision[i] = True
        return vision
    

spaceship_img = pygame.image.load("assets/spaceship.png")
spaceship_img = pygame.transform.scale(spaceship_img, (32,32))

class AISpaceship(PygameObject):
    def __init__(self, brain: Brain):
        self.brain = brain
        image="assets/spaceship.png" 
        size = 32
        super().__init__(image, 250, 250, 0, size)
        del self.image
        self.size = 18
        self.img_size = 32
        self.ray_points = PointsInCircum(40, self.position, n=10) + PointsInCircum(80, self.position, n=6)    

    def update(self, visionAsteroids: List[bool]) -> List[Projectile]:
        super().update()
        asteroids = [int(i) for i in visionAsteroids]

        normX = self.position.x / 500
        normY = self.position.y / 500
        normVeloX = self.velocity.x / 500
        normVeloY = self.velocity.y / 500
        directionX = self.direction.x
        directionY = self.direction.y
        inputs = asteroids + [normX, normY, normVeloX, normVeloY, directionX, directionY]
        self.actions = self.brain.predict(inputs = inputs)

        projectiles = []
        if self.actions[0] > 0.5:
            self.rotate(1)
        if self.actions[1] > 0.5:
            self.rotate(-1)
        if self.actions[2] > 0.5:
            self.addVelocity(0.05)
        if self.actions[3] > 0.5:
            self.addVelocity(-0.05)
        if self.actions[4] > 0.5:
            x = self.position.x
            y = self.position.y
            velo = self.direction * 3 + self.velocity
            projectiles.append(Projectile(x,y,velo))
        self.ray_points = PointsInCircum(40, self.position, n=10) + PointsInCircum(80, self.position, n=6)
        return projectiles

    def show(self, screen: pygame.display):
        img = pygame.transform.rotozoom(spaceship_img, self.direction.angle_to(UP), 1)
        img_size = pygame.Vector2(img.get_size())
        blit_position = self.position - img_size * 0.5
        if self.__DEBUG__:
            pygame.draw.circle(screen, (255, 0, 0), self.position, self.size)
        screen.blit(img, blit_position)

        for pt in self.ray_points:
            pygame.draw.circle(screen, (0, 255, 255), (pt[0], pt[1]), 4)

    def asteroid_in_range(self, asteroid: Asteroid)->List[bool]:
        vision = []
        for pt in self.ray_points:
            vision.append(asteroid.collider(PygameObject(image="assets/asteroid.png", x=pt[0], y=pt[1], velocity=0, size=1)))
        return vision
    
    def check_vision(self, asteroids: List[Asteroid])->List[bool]:
        vision = [False for i in range (len(self.ray_points))]
        for asteroid in asteroids:
            results = self.asteroid_in_range(asteroid)
            for i in range(len(results)):
                if results[i]:
                    vision[i] = True
        return vision

    def mutate(self, amt):
        self.brain.mutate(amt)

