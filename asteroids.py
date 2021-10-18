import pygame, sys
import objects

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
        if event.type == pygame.MOUSEBUTTONDOWN:
            #shoot
            pass
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                x = player.position.x
                y = player.position.y
                velo = player.direction * 3 + player.velocity
                projectiles.append(objects.Projectile(x,y,velo))
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        #player.move(-3, 0)
        player.rotate(-1)
    elif keys[pygame.K_RIGHT]:
        player.rotate(1)
    elif keys[pygame.K_UP]:
        player.addVelocity(0.1)
    elif keys[pygame.K_UP]:
        player.removeVelocity(0.1)


    for asteroid in asteroids:
        if asteroid.collider(player):
            running = False
        for i, projectile in enumerate(projectiles):
            if asteroid.collider(projectile):
                new = asteroid.split()
                for n in new:
                    asteroids.append(n)
                projectiles.remove(projectile)
                asteroids.remove(asteroid)

    
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
    #input()