#เตรียมข้อมูลสำหรับเขียนโปรแกรม
import os

import pygame
import random
from  pygame import mixer

#Game Setup

pygame.mixer.init()
pygame.init()


pygame.mixer.quit()
pygame.mixer.init(frequency=22050, size=-16, channels=2, buffer=512)
pygame.init()

bg_music = "soud.mp3"
if os.path.exists(bg_music):
    mixer.music.load(bg_music)
    mixer.music.play(-1)
    mixer.music.set_volume(0.7)
else:
    print(f"⚠️ Warning: ไม่พบไฟล์เสียง '{bg_music}', จะเล่นเกมต่อไปโดยไม่มีเพลงพื้นหลัง")

RunGame = True
GameOver = False
GameScore = 0
CountShoot = 0
S_WIDTH = 700
S_HEIGHT = 760
FPS = 30



#กำหนดหน้าต่างของเกม

Window = pygame.display.set_mode((S_WIDTH,S_HEIGHT))
ClockFPS = pygame.time.Clock()
pygame.display.set_icon(pygame.image.load("f7a0af7c76cb837c53fe92dc93369d0e-Photoroom.png"))

##### สร้างคลาสจรวด ######

class SpaceShip(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load('image01-Photoroom (1).png')
        self.rect = self.image.get_rect()
        self.rect.centerx = S_WIDTH / 2
        self.rect.bottom = S_HEIGHT - 10
        self.speed_x = 0
        self.speed_y = 0
        self.laser_sound = "AnyConv.com__202502121512.mp3"
        if os.path.exists(self.laser_sound):
            self.laser_sfx = mixer.Sound(self.laser_sound)
        else:
            self.laser_sfx = None

    def update(self):
        self.rect.x += self.speed_x
        self.rect.y += self.speed_y
        if self.rect.right > S_WIDTH:
            self.rect.right = S_WIDTH
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.top < 0:
            self.rect.top = 0
        if self.rect.bottom > S_HEIGHT:
            self.rect.bottom = S_HEIGHT

    def ShootLaser(self):
        ObjectLaser = Laser(self.rect.centerx, self.rect.top)
        All_Sprite_Show.add(ObjectLaser)
        All_Laser.add(ObjectLaser)

        if self.laser_sfx:
            self.laser_sfx.play()


########## สร้างคลาสกระสุน #############

class Laser(pygame.sprite.Sprite):
    def __init__(self, pX , pY):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load('image02-Photoroom.png')
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
        self.image = pygame.image.load('image03-Photoroom.png')
        self.rect = self.image.get_rect()
        self.rect.x = random.randrange(70,S_WIDTH-70)
        self.rect.y = random.randrange(-150,-100)
        self.speed = random.randrange(1,5)

    def update(self):
        self.rect.y += self.speed
        if self.rect.top > S_HEIGHT:
            self.kill()
            MakeAsteroid()

class Asteroid2(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load('image04-Photoroom.png')
        self.rect = self.image.get_rect()
        self.rect.x = random.randrange(50, S_WIDTH - 50)
        self.rect.y = random.randrange(-200, -100)
        self.speed = random.randrange(2, 6)

    def update(self):
        self.rect.y += self.speed
        if self.rect.top > S_HEIGHT:
            self.kill()
            MakeAsteroid2()

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

# ฟังก์ชันสร้างอุกกาบาตชนิดที่ 2
def MakeAsteroid2():
    Object_ats = Asteroid2()
    All_Sprite_Show.add(Object_ats)
    All_Asteroid.add(Object_ats)

for i in range(5):
    MakeAsteroid()

# Set font

font_score = pygame.font.Font('tahoma.ttf',20)
font_gameover = pygame.font.Font('tahomabd.ttf',40)

def ShowScore():
    text_score = font_score.render('Score : {}'.format(GameScore),True,(255,0,0))
    Window.blit(text_score,(30,10))


########## Loop game ##############

while RunGame:
    Window.blit(pygame.image.load("imageee (1).png"),(0,0))
    ShowScore()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            RunGame = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and CountShoot < 5:
                Player.ShootLaser()
                CountShoot += 1

            if event.key == pygame.K_RIGHT:
                Player.speed_x = 5
            if event.key == pygame.K_LEFT:
                Player.speed_x = -5
            if event.key == pygame.K_UP:
                Player.speed_y = -5
            if event.key == pygame.K_DOWN:
                Player.speed_y = 5

        elif event.type == pygame.KEYUP:
            if event.key in [pygame.K_LEFT, pygame.K_RIGHT]:
                Player.speed_x = 0
            if event.key in [pygame.K_UP, pygame.K_DOWN]:
                Player.speed_y = 0

                    
    # การตรวจสอบการชนกันของวัตถุ

    for asteroid in All_Asteroid:
        if pygame.sprite.spritecollide(asteroid, All_Laser, True):
            GameScore += 150
            asteroid.kill()

            explosion_sound = "so1.mp3" if isinstance(asteroid, Asteroid) else "so2.mp3"

            if os.path.exists(explosion_sound):
                mixer.Sound(explosion_sound).play()

            MakeAsteroid()
            MakeAsteroid2()
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
        Window.blit(pygame.image.load('Premium Vector _ Silhouette of three cowboys riding horses in desert background vector.jpg'),(0,0))
        ShowScore()
        text_gameover = font_gameover.render('Game Over',True,(255,0,0))
        Window.blit(text_gameover, (S_WIDTH / 4 , S_HEIGHT / 2))
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                RunGame = True

pygame.quit()