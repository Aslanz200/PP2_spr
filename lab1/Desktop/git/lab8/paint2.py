import pygame
pygame.init()


#colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)


#setting up screen
screen_size = (700 , 700)
screen = pygame.display.set_mode(screen_size)
screen.fill(WHITE)

radius = 10
circles = [pygame.draw.circle(screen , BLACK , 0 , radius)]




#main while loop
on = True
while on:

    pygame.display.update()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            on = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                pos = event.pos
                print(pos)
                #circles.append(pygame.draw.circle(screen , BLACK , pos , center=radius))
                screen.blit(circles)

pygame.quit()