import pygame , time , sys
from random import randint
from pygame.locals import *
pygame.init()
screen = pygame.display.set_mode((400 , 600))
bgimage = pygame.image.load("lab8/racer_elements/AnimatedStreet.png")

FPS = pygame.time.Clock()

#counting number of coins
count = 0

font = pygame.font.SysFont("Verdana" , 60)
game_over = font.render("Game over" , True , "Black")
coins_txt = font.render(f"{count}" , True , "Black")

class Coin(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("lab9/racer_elements/coin.png")
        self.image = pygame.transform.scale(self.image , (30, 30))
        self.rect = self.image.get_rect()
        self.rect.center = (randint(30 , 330) , randint(250 , 400))

    def spawn(self , screen):
        screen.blit(self.image , self.rect)


class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("lab8/racer_elements/Enemy.png")
        self.rect = self.image.get_rect()
        self.rect.center = (randint(30, 330) , 0)
        self.speed = 5

    def move(self):
        self.rect.move_ip(0 , self.speed) #enemy car speed
        if self.rect.top > 600 :
            self.rect.top = -60
            self.rect.center = (randint(30, 330) , 0) #reset enemy car position
    def draw(self , screen):
        screen.blit(self.image , self.rect)


class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("lab8/racer_elements/Player.png")   #my car png
        self.rect = self.image.get_rect()  #drawing rectangle around my png so i can allocate its position
        self.rect.center = (200 , 550)  #starting position
    def update(self):
        pressed_keys = pygame.key.get_pressed()

        if self.rect.top>0:   #top off-screen limit
            if pressed_keys[K_UP]:
                self.rect.move_ip(0 , -3)

        if self.rect.bottom<600:   #bottom off-screen limit
            if pressed_keys[K_DOWN]:
                self.rect.move_ip(0 , 3)

        if self.rect.left > 0:    #left off-screen limit
          if pressed_keys[K_LEFT]:
              self.rect.move_ip(-3, 0)

        if self.rect.right < 400:   #right off-screen limit
            if pressed_keys[K_RIGHT]:
                self.rect.move_ip(3, 0)
    def draw(self , screen):
        screen.blit(self.image , self.rect)

pygame.mixer.music.load("lab8/racer_elements/background.wav") 
pygame.mixer.music.play(-1) #loop background music


#initializing classes
on = True
P1 = Player()
E1 = Enemy()
C1 = Coin()

#group enemies and coins
enemies = pygame.sprite.Group()
enemies.add(E1)
coins = pygame.sprite.Group()
coins.add(C1)

#add all sprites to the sprites group
all_sprites = pygame.sprite.Group()
all_sprites.add(P1)
all_sprites.add(E1)
all_sprites.add(C1)

while on:
    screen.blit(bgimage , (0 , 0)) #background image
    screen.blit(coins_txt , (300 , 500)) #appearing text on the screen

    P1.update()
    E1.move()

    C1.spawn(screen)
    P1.draw(screen)
    E1.draw(screen)

    pygame.display.update()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            on = False

    if pygame.sprite.spritecollideany(P1 , enemies): #collision detection with enemy
        pygame.mixer.music.stop()
        pygame.mixer.Sound("lab8/racer_elements/crash.wav").play()
        time.sleep(2)
        screen.fill("Red")
        screen.blit(game_over , (30 , 250))
        pygame.display.update()
        time.sleep(2)
        pygame.quit()
        sys.exit()

    if pygame.sprite.spritecollideany(P1, coins): #collision detection with coin
        count += 1
        coins_txt = font.render(f"{count}", True, "Black")  #update coin counter text
        for coin in coins:
            coin.kill()  # Remove the collected coin
        C1 = Coin()  # Create a new coin
        coins.add(C1)
        all_sprites.add(C1)
        if count % 5 == 0:  #increases speed every 5 coin
            E1.speed += 1
    
    FPS.tick(60) #limit frame rate

pygame.quit()
