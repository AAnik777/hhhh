#Создай собственный Шутер!
 
from pygame import *
from random import randint 
 
class GameSprite(sprite.Sprite):
    def __init__(self, player_image, player_x, player_y, player_speed, size_x=65,size_y=65):
        super().__init__()
        self.image = transform.scale(image.load(player_image),(size_x,size_y))
        self.speed = player_speed
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y
 
    def reset(self):
        window.blit(self.image,(self.rect.x, self.rect.y))
 
class Player(GameSprite):
    def update(self):
        keys = key.get_pressed()
        if keys[K_a] and self.rect.x > 5:
            self.rect.x -= self.speed   
        if keys[K_d] and self.rect.x < 620:
            self.rect.x += self.speed   
        if keys[K_w] and self.rect.y > 5:
            self.rect.y -= self.speed 
        if keys[K_s] and self.rect.y < 420:
            self.rect.y += self.speed   
 
class Enemy(GameSprite):
    def update(self):
        global lost
        self.rect.y += self.speed
        if self.rect.y > 500:
            lost += 1
            self.rect.x = randint(0,600)
            self.rect.y = 0
 
class Asteroid(GameSprite):
    def update(self):
        global lost
        self.rect.y += self.speed
        if self.rect.y > 500:
            lost += 1
            self.rect.x = randint(0,600)
            self.rect.y = 0
 
 
 
class Bullet(GameSprite):
    def update(self):
        self.rect.y -= self.speed
        if self.rect.y < 0:
            self.kill() 
 
 
win_width = 700
win_height = 500
window = display.set_mode((win_width, win_height))
display.set_caption("cosmic guns")
background = transform.scale(image.load('galaxy.jpg'), (win_width, win_height))
lost = 0
score = 0
 
font.init()
font1 = font.SysFont('Arial',36)
font2 = font.SysFont('Arial',44)
font3 = font.SysFont('Arial',70)
 
mixer.init()
mixer.music.load("space.ogg")
mixer.music.play()
mixer.music.set_volume(0.2)
game = True
finish = False
 
fireTimer = 0
FPS = 60
clock = time.Clock()
player = Player('rocket.png',5,win_height - 80,4)

 
 
bullets = sprite.Group()
kick = mixer.Sound('fire.ogg')
 
 
monsters = sprite.Group()
for i in range(5):
    monsters.add(Enemy('ufo.png', randint(0,600),randint(-100,0),1))

asteroids = sprite.Group()
for i in range(1):
    asteroids.add(Asteroid('asteroid.png', randint(0,600),randint(-100,0),2))

finish = False
 
last_bullet_time = 0
bullet_delay = 1000
 
while game:
    for e in event.get():
        if e.type == QUIT:
            game = False
    
    if finish == False:


        window.blit(background,(0,0))
        player.reset()
        player.update()
        monsters.update()
        monsters.draw(window)
        asteroids.update()
        asteroids.draw(window)
    
        bullets.update()
        bullets.draw(window)
        if key.get_pressed()[K_SPACE] and fireTimer >20:
            bullets.add(Bullet('bullet.png', player.rect.x + 28, player.rect.y - 35 ,2,10,35))
            fireTimer = 0
            kick.play()
    
        hits = sprite.groupcollide(monsters,bullets,True,True)
        for hit in hits:
            monsters.add(Enemy('ufo.png', randint(0,600),randint(-100,0),2))
            score += 1

        if sprite.spritecollide(player, asteroids, False):
            lost += 1
            text_lose = font2.render(
                'Увы, но Ваш корабль потерпел крушение!', 1, (255,50,50)
                )
            window.blit(text_lose, (32,215))
            finish = True

        if lost == 3:
            text_lose = font2.render(
                'Увы, но Ваша задача провалена!', 1, (255,50,50)
                )
            window.blit(text_lose, (102,215))
            finish = True

        if score == 10:
            text_win = font3.render(
                'Поздравляю, Вы победили!', 1, (90,255,90)
                )
            window.blit(text_win, (10,225))
            finish = True
    
        text_score = font1.render(
        'Попаданий' + str(score), 1, (255,255,255)
        )
    
        text_lose = font1.render(
        'Пропущено:' + str(lost), 1, (255, 255, 255)
        )
    
        window.blit(text_lose, (0,20))
        window.blit(text_score,(0,50))
    display.update()
    clock.tick(FPS)               
    fireTimer+=1