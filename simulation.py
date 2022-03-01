from os import environ
environ['PYGAME_HIDE_SUPPORT_PROMPT'] = '1'

import pygame
import objects
import NeuralNet as nn
display_width = display_height = 500
black = (0,0,0)
white = (255,255,255)



def run(player):
    pygame.init()
    tickcount = 0
    score = 0

    running = True
    clock = pygame.time.Clock()
    screen = pygame.display.set_mode((display_width, display_height))
    pygame.display.set_caption("Asteroids")

    projectiles = []

    asteroids = [objects.Asteroid() for i in range(10)]

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        for asteroid in asteroids:
            if asteroid.collider(player):
                running = False
            for i, projectile in enumerate(projectiles):
                if asteroid.collider(projectile):
                    score += 2
                    new = asteroid.split()
                    for n in new:
                        asteroids.append(n)
                    projectiles.remove(projectile)
                    asteroids.remove(asteroid)

        
        screen.fill(black)
        
        for projectile in projectiles:
            projectile.update()
            projectile.show(screen)

        vision = player.check_vision(asteroids)
        projectiles = projectiles + player.update(vision)
        player.show(screen)

        for asteroid in asteroids:
            asteroid.update()
            asteroid.show(screen)
        

        pygame.display.update()
        pygame.display.flip()
        clock.tick(60)
        tickcount += 1
        #input()

        if len(projectiles) > 20:
            projectiles = projectiles[-20:]

    score += (tickcount/60) / 2
    return {'score': score, 'player': player}

if __name__ == "__main__":
    player = objects.AISpaceship(brain=nn.Brain([0 for i in range(25)], [0,0,0,0,0]))
    print(run(player=player))