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
    level = 0
    score = 0
    total_shot = 0
    moved = False

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
            if projectile.update():
                projectiles.remove(projectile)
            else:
                projectile.show(screen)

        vision = player.check_vision(asteroids)
        new_projectiles = player.update(vision)
        projectiles = projectiles + new_projectiles
        player.show(screen)

        for asteroid in asteroids:
            asteroid.update()
            asteroid.show(screen)
        

        pygame.display.update()
        pygame.display.flip()
        clock.tick(2000)
        tickcount += 1
        #input()

        if len(projectiles) > 20:
            projectiles = projectiles[-20:]

        if len(asteroids) == 0:
            score += 30
            level += 1
            asteroids = [objects.Asteroid() for i in range(10 + level*2)]
            player.position = pygame.Vector2((250, 250))
            player.velocity = pygame.Vector2((0, 0))
            player.direction = pygame.Vector2(objects.UP)
        total_shot += len(new_projectiles)

    if player.position.x != 250 or player.position.y != 250:
        moved = True

    score += (tickcount/60) / 2 # incentivise for staying alive
    score -= (total_shot*0.5) # make it so that shooting is not as incentivised
    score += (int(moved)*40) #movement bonus
    return {'score': score, 'player': player}

if __name__ == "__main__":
    player = objects.AISpaceship(brain=nn.Brain([0 for i in range(25)], [0,0,0,0,0]))
    print(run(player=player))