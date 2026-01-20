#เตรียมข้อมูลสำหรับเขียนโปรแกรม
import pygame
import random
from  pygame import mixer

from pygame.examples.aliens import Player

#Game Setup

pygame.init() #ประกาศให้ไลบารี่ pygame เริ่มทำงาน
RunGame = True
GameOver = False
GameScore = 0
CountShoot = 0
S_WIDTH = 500
S_HEIGHT = 600
FPS = 30

#กำหนดหน้าต่างของเกม

Window = pygame.display.set_mode((S_WIDTH,S_HEIGHT))
ClockFPS = pygame.time.Clock()
pygame.display.set_icon(pygame.image.load("rocket.png"))

##### สร้างคลาสจรวด ######

class SpaceShip(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load('spaceship.png')
        self.rect = self.image.get_rect()
        self.rect.centerx = S_WIDTH/2
        self.rect.bottom = S_HEIGHT - 10
        self.speed = 0

    def update(self):
        self.speed = 0
        KeyHit = pygame.key.get_pressed()
        if KeyHit[pygame.K_RIGHT]:
            self.speed = 5
        if KeyHit[pygame.K_LEFT]:
            self.speed = -5
        self.rect.x += self.speed
        if self.rect.right > S_WIDTH:
            self.rect.right = S_WIDTH
        if self.rect.left < 0:
            self.rect.left = 0

    def ShootLaser(self):
        ObjectLaser = Laser(self.rect.centerx, self.rect.top)
        All_Sprite_Show.add(ObjectLaser)
        All_Laser.add(ObjectLaser)
        #mixer.music.load('laser_S.wav')
        # mixer.music.play(1)

########## สร้างคลาสกระสุน #############

class Laser(pygame.sprite.Sprite):
    def __init__(self, pX , pY):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load('laser_P.png')
        self.rect = self.image.get_rect()
        self.rect.centerx = pX
        self.rect.bottom = pY
        self.speed = 10
    def update(self):
        global CountShoot
        self.rect.y -= self.speed
        if self.rect.bottom < 0:
            self.kill()
            CountShoot -= 1

#### สร้างคลาสอุกาบาต ###

class Asteroid(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load('asteroid.png')
        self.rect = self.image.get_rect()
        self.rect.x = random.randrange(70,S_WIDTH-70)
        self.rect.y = random.randrange(-150,-100)
        self.speed = random.randrange(1,5)
    def update(self):
        self.rect.y += self.speed
        if self.rect.top > S_HEIGHT:
            self.kill()
            MakeAsteroid()

# สร้างกลุ่มของ Object

All_Sprite_Show = pygame.sprite.Group()
All_Laser = pygame.sprite.Group()
All_Asteroid = pygame.sprite.Group()


Player = SpaceShip() # สร้าง Object ของยานผู้เล่น
All_Sprite_Show.add(Player)

# ฟังก์ชันสร้างอุกาบาต
def MakeAsteroid():
    Object_ats = Asteroid()
    All_Sprite_Show.add(Object_ats)
    All_Asteroid.add(Object_ats)


for i in range(10):
    MakeAsteroid()


# Set font

font_score = pygame.font.Font('tahoma.ttf',20)
font_gameover = pygame.font.Font('tahomabd.ttf',40)

def ShowScore():
    text_score = font_score.render('Score : {}'.format(GameScore),True,(255,0,0))
    Window.blit(text_score,(30,10))


########## Loop game ##############

while RunGame:
    Window.blit(pygame.image.load("BGSpace.jpg"),(0,0))
    ShowScore()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            RunGame = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                if CountShoot < 5:
                    Player.ShootLaser()
                    CountShoot += 1

    # การตรวจสอบการชนกันของวัตถุ
    CheckHits = pygame.sprite.groupcollide(All_Asteroid,All_Laser,True,True)
    if CheckHits:
        GameScore += 150
        MakeAsteroid()
        CountShoot -= 1

    CheckHits = pygame.sprite.spritecollide(Player,All_Asteroid,True)
    if CheckHits:
        RunGame = False
        GameOver = True

    All_Sprite_Show.update()
    All_Sprite_Show.draw(Window)

    pygame.display.update()
    ClockFPS.tick(FPS)

####### Game Over #######

if GameOver:
    while not  RunGame:
        Window.blit(pygame.image.load('BGSpace.jpg'),(0,0))
        ShowScore()
        text_gameover = font_gameover.render('Game Over',True,(255,0,0))
        Window.blit(text_gameover, (S_WIDTH / 4 , S_HEIGHT / 2))
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                RunGame = True

pygame.quit()