#створи гру "Лабіринт"!
import pygame

width = 800
height = 600

FPS = 60

size = (width, height)

window = pygame.display.set_mode(size)

background = pygame.transform.scale(
    pygame.image.load("background.jpg"),
    size
)
clock = pygame.time.Clock()

class GameSprite(pygame.sprite.Sprite):
    def __init__(self, image, x,y, speed):
        self.image = pygame.transform.scale(
        pygame.image.load(image),
        (65,80)
        )
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

        self.speed = speed

    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))


class Player(GameSprite):
    def update(self):
        keys_pressed = pygame.key.get_pressed()

        if keys_pressed[pygame.K_UP]:
            if self.rect.y > 0:
                self.rect.y -= self.speed
            else:
                self.rect.y = height-75

        if keys_pressed[pygame.K_DOWN]:
            if self.rect.y < height-85:
                self.rect.y += self.speed
            else:
                self.rect.y = 0

        if keys_pressed[pygame.K_RIGHT]:
            if self.rect.x < width-70:
                self.rect.x += self.speed

        if keys_pressed[pygame.K_LEFT]:
            if self.rect.x > 0:
                self.rect.x -= self.speed
        
class Enemy(GameSprite):
    direction = "left"

    def update(self):


        if self.rect.x <= width/2+250:
            self.direction = "right"
        elif self.rect.x >= width-70:
            self.direction = "left"


        if self.direction == "left":
            self.rect.x -= self.speed
        elif self.direction == "right":
            self.rect.x += self.speed
        
  
class Wall(pygame.sprite.Sprite):
    def __init__(self, r,g,b, x,y, lenght, width ):
        super().__init__()
        self.color = (r,g,b)
        self.rect = pygame.Rect(x,y, lenght, width)

    def draw(self):
        pygame.draw.rect(window, self.color, self.rect )




player = Player("hero.png", 100, 500, 5)
enemy = Enemy("cyborg.png", width-80, 280, 4)
gold = GameSprite("treasure.png",width-100, height-100, 0)     


test_wall = Wall(255,10,105, 20,20, 1,10)

walls = [
    Wall(5,155,10, 110,110, 300,100),
    Wall(105,105,10, 250,200, 300,500),
    Wall(10,105,10, 250,150, 150,10),
    Wall(255,105,10, 300,400, 200,10)
]

pygame.mixer.init()
pygame.mixer.music.load("jungles.ogg")
pygame.mixer.music.play()
pygame.mixer.music.stop()

game_over = False


finish = False

pygame.font.init()
font1 = pygame.font.Font(None,70)
text_win = font1.render("Ти переміг :)", True, (0,255,0))

text_lose = font1.render("Ти програв :(", True, (255,0,0))

while not game_over:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game_over = True

    if not finish:
       
       window.blit(background, (0,0))
       player.update()
       player.reset()

       enemy.update()
       enemy.reset()

       gold.reset()

       test_wall.draw()

       for w in walls:
           w.draw()

    if pygame.sprite.collide_rect(player,gold):
       finish = True
       window.blit(text_win, (width/3, height/3))

    wall_collision = any(pygame.sprite.collide_rect(player, w)for w in walls)
    if pygame.sprite.collide_rect(player,enemy) or wall_collision:
        finish = True
        window.blit(text_lose, (width/3, height/3))





    pygame.display.update()
    clock.tick(FPS)