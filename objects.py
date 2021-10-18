import pygame
import random
import math

from pygame.math import Vector2

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


import math
pi = math.pi

def PointsInCircum(r,c,n=5):
    return [
        (c[0]+math.cos(2*pi/n*x)*r,
        c[1]+math.sin(2*pi/n*x)*r) 
        for x in range(0,n+1)
    ]

class Spaceship(PygameObject):
    def __init__(self, image="assets/spaceship.png", size = 32):
        super().__init__(image, 250, 250, 0, size)
        self.size = 18
        self.img_size = 32
        self.ray_points = PointsInCircum(80, self.position, n=10)
        
    def update(self):
        super().update()
        self.ray_points = PointsInCircum(80, self.position, n=10)

    def show(self, screen: pygame.display):
        super().show(screen)
        for pt in self.ray_points:
            pygame.draw.circle(screen, (0, 255, 255), (pt[0], pt[1]), 4)

    
class Asteroid(PygameObject):
    def __init__(self, image="assets/asteroid.png", x=-1, y=-1, size=-1):

        if x == -1 and y == -1:    
            rand_x = random.randrange(0, 500, 10)
            rand_y = random.randrange(0, 500, 10)
            if rand_x > 300 and rand_x < 400:
                if rand_y > 300 and rand_y < 400:
                    if rand_x > 300 and rand_x < 400:
                        rand_x += 100 * random.choice([-1, 1])
                    if rand_y > 300 and rand_y < 400:
                        rand_y += 100 * random.choice([-1, 1])
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

class Projectile(PygameObject):
    def __init__(self, x, y, velocity: pygame.Vector2, size=6):
        super().__init__("assets/block.png", x, y, 0.5, size=size)
        self.velocity = Vector2(velocity)
    