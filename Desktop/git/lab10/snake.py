import pygame , sys , random
import psycopg2
pygame.init()

conn = psycopg2.connect(
    dbname='postgres',
    user='postgres',
    host='localhost',
    port=5432
)
cur = conn.cursor()

cur.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id SERIAL PRIMARY KEY,
        username VARCHAR(100) UNIQUE NOT NULL
    );
""")

cur.execute("""
    CREATE TABLE IF NOT EXISTS scores (
        id SERIAL PRIMARY KEY,
        user_id INTEGER REFERENCES users(id),
        score INTEGER DEFAULT 0,
        level INTEGER DEFAULT 1
    );
""")
conn.commit()



#setting the display
SCREEN_WIDTH , SCREEN_LENGTH = 600 , 600
screen = pygame.display.set_mode((SCREEN_LENGTH , SCREEN_WIDTH))
FPS = pygame.time.Clock()
BLOCK_SIZE = 30  #block size
speed = 5   #speed of snake
score = 0   #our score
level = 1


#creating a text for score
Font = pygame.font.Font("/System/Library/Fonts/Supplemental/Arial Black.ttf" , 50)
score_txt = Font.render("0" , True , "White")
score_rect = score_txt.get_rect(center=(SCREEN_LENGTH/2 , SCREEN_WIDTH/2))

def get_username():
    input_box = pygame.Rect(150, 250, 300, 50)
    color_inactive = pygame.Color('White')
    color_active = pygame.Color('Red')
    color = color_inactive
    active = False
    username = ''
    font = pygame.font.Font(None, 40)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                if input_box.collidepoint(event.pos):
                    active = not active
                else:
                    active = False
                color = color_active if active else color_inactive

            if event.type == pygame.KEYDOWN:
                if active:
                    if event.key == pygame.K_RETURN:
                        return username
                    elif event.key == pygame.K_BACKSPACE:
                        username = username[:-1]
                    else:
                        if len(username) < 15:
                            username += event.unicode

        screen.fill("black")
        txt_surface = font.render(username, True, color)
        width = max(300, txt_surface.get_width()+10)
        input_box.w = width
        screen.blit(txt_surface, (input_box.x+5, input_box.y+5))
        pygame.draw.rect(screen, color, input_box, 2)

        pygame.display.flip()
        FPS.tick(30)


def pause():
    screen.fill("Black")
    txt = pygame.font.Font(None , 40)
    txt_surface = txt.render("Game paused" , True , "White")


#creating a squared grid
def DrawGrid():
    for x in range (0 , SCREEN_LENGTH , BLOCK_SIZE):
        for y in range(0 , SCREEN_WIDTH , BLOCK_SIZE):
            rect = pygame.Rect(x , y , BLOCK_SIZE , BLOCK_SIZE)
            pygame.draw.rect(screen , "#3c3c3b" , rect , 1)



#snake class
class Snake:
    def __init__(self):
        self.x , self.y = BLOCK_SIZE , BLOCK_SIZE
        self.xdir = 1   #xdir , if 1=right , -1=left , 0=none
        self.ydir = 0   #ydir , if 1=up , -1=down , 0=none
        self.head = pygame.Rect(self.x , self.y , BLOCK_SIZE , BLOCK_SIZE)   #snake head
        self.body = [pygame.Rect(self.x-BLOCK_SIZE , self.y , BLOCK_SIZE , BLOCK_SIZE)]   #snake body
        self.dead = False
    def update(self):

        global apple    
        global speed
        global score
        global level

        if self.dead:       #renewing every setting after being dead
            self.x , self.y = BLOCK_SIZE , BLOCK_SIZE
            self.head = pygame.Rect(self.x , self.y , BLOCK_SIZE , BLOCK_SIZE)
            self.body = [pygame.Rect(self.x-BLOCK_SIZE , self.y , BLOCK_SIZE , BLOCK_SIZE)]
            self.xdir = 1      
            self.ydir = 0
            self.dead = False
            apple = Apple()
            speed = 5
            score = 0
            level = 1

        #collision 
        for square in self.body:
            if self.head.x == square.x and self.head.y == square.y:
                self.dead = True
            if self.head.x not in range(0 , SCREEN_LENGTH) or self.head.y not in range(0, SCREEN_WIDTH):
                self.dead = True

        #snake moving
        self.body.append(self.head)  #appending a block ahead of body so there will be no off-range errors
        for i in range(len(self.body)-1):  
            self.body[i].x , self.body[i].y = self.body[i+1].x , self.body[i+1].y   #moving each body block forward
        self.head.x += self.xdir * BLOCK_SIZE      #moving head by moving its position by one block
        self.head.y += self.ydir * BLOCK_SIZE      
        self.body.remove(self.head)


#apple class
class Apple:
    def __init__(self):
        self.x = int(random.randint(0 , SCREEN_LENGTH)/BLOCK_SIZE) * BLOCK_SIZE  #landing apples right on grid
        self.y = int(random.randint(0, SCREEN_WIDTH)/BLOCK_SIZE) * BLOCK_SIZE
        self.rect = pygame.Rect(self.x , self.y , BLOCK_SIZE , BLOCK_SIZE)  #apple size
        self.spawn_time = pygame.time.get_ticks()  #starting timer from moment of spawn of an apple
        self.Font1 = pygame.font.Font("/System/Library/Fonts/Supplemental/Arial Black.ttf" , 10)
    def update(self):
        pygame.draw.rect(screen , "Red" , self.rect)    #appending on the screen

#initializing our objects
DrawGrid()
snake = Snake()
apple = Apple()

count = 0
paused = False
on = True
username = get_username()
while on:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            on = False
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_DOWN and not paused:
                snake.ydir = 1
                snake.xdir = 0
            if event.key == pygame.K_UP and not paused:
                snake.ydir = -1
                snake.xdir = 0
            if event.key == pygame.K_LEFT and not paused:
                snake.ydir = 0
                snake.xdir = -1
            if event.key == pygame.K_RIGHT and not paused:
                snake.ydir = 0
                snake.xdir = 1
            if event.key == pygame.K_p:
                paused = not paused

    screen.fill("Black")
    DrawGrid()

    if not paused:
        snake.update()

        if pygame.time.get_ticks() - apple.spawn_time > 10000:
            apple = Apple()

        if snake.head.x == apple.x and snake.head.y == apple.y:
            snake.body.append(pygame.Rect(square.x, square.y, BLOCK_SIZE, BLOCK_SIZE))
            apple = Apple()
            score += 1
            if score % 5 == 0:
                speed += 0.8
                level += 1

    apple.update()

    score_txt = Font.render(f"{level}", True, "White")
    screen.blit(score_txt, score_rect)

    pygame.draw.rect(screen, 'Yellow', snake.head)
    for square in snake.body:
        pygame.draw.rect(screen, "Green", square)

    if paused:
        txt = pygame.font.Font(None, 40)
        pause_msg = txt.render("Game Paused. Press P to resume", True, "White")
        pause_rect = pause_msg.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_LENGTH // 2))
        screen.blit(pause_msg, pause_rect)

    pygame.display.update()
    FPS.tick(speed if not paused else 60)

pygame.quit()