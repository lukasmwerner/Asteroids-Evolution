from os import environ
environ['PYGAME_HIDE_SUPPORT_PROMPT'] = '1'

import pygame
import objects
import NeuralNet as nn
pygame.init()

def run(player):
    score = 0

    pygame.init()
    display_width = display_height = 500
    screen = pygame.display.set_mode((display_width, display_height))
    pygame.display.set_caption("Asteroids")

    running = True
    clock = pygame.time.Clock()

    black = (0,0,0)
    white = (255,255,255)

    player = objects.Spaceship()
    projectiles = []

    asteroids = [objects.Asteroid() for i in range(10)]

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    x = player.position.x
                    y = player.position.y
                    velo = player.direction * 3 + player.velocity
                    projectiles.append(objects.Projectile(x,y,velo))
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            player.rotate(-1)
        elif keys[pygame.K_RIGHT]:
            player.rotate(1)
        elif keys[pygame.K_UP]:
            player.addVelocity(0.1)
        elif keys[pygame.K_UP]:
            player.removeVelocity(0.1)
        elif keys[pygame.K_SPACE]:
            for new in asteroids[largest].split():
                asteroids.append(new)


        for asteroid in asteroids:
            if asteroid.collider(player):
                running = False
            for i, projectile in enumerate(projectiles):
                if asteroid.collider(projectile):
                    score += 1
                    new = asteroid.split()
                    for n in new:
                        asteroids.append(n)
                    projectiles.remove(projectile)
                    asteroids.remove(asteroid)

        # could also just see the distance for all asteroids and then write them down if they are within the view circle and the save their distances and positions
        
        screen.fill(black)
        
        for projectile in projectiles:
            projectile.update()
            projectile.show(screen)

        player.update()
        player.show(screen)
        
        for asteroid in asteroids:
            asteroid.update()
            asteroid.show(screen)

        pygame.display.update()
        pygame.display.flip()
        clock.tick(60)


    return {'score': score, 'player': player}

if __name__ == "__main__":
    run()