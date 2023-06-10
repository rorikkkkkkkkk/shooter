from pygame import *
from random import randint
from time import time as timer

class GameSprite(sprite.Sprite):
    def __init__(self, player_image, player_x, player_y, size_x, size_y, player_speed):
        self.image = transform.scale(image.load(player_image), (size_x, size_y))
        self.speed = player_speed
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y

    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))

class Player(GameSprite):
    def __init__(self, player_image, player_x, player_y, size_x, size_y, player_speed):
        super().__init__(player_image, player_x, player_y, size_x, size_y, player_speed)
    def update(self):
        keys = key.get_pressed()
        if keys[K_LEFT] and self.rect.x > 5:
            self.rect.x -= self.speed
        if keys[K_RIGHT] and self.rect.x < 620:
            self.rect.x += self.speed

    def fire(self):
        bullet = Bullet('bullet.png', self.rect.centerx-7, self.rect.top, 15, 20, 15)
        bullets.add(bullet)

class Enemy(sprite.Sprite):
    def __init__(self, player_image, player_x, player_y, size_x, size_y, player_speed):
        super().__init__()
        self.image = transform.scale(image.load(player_image), (size_x, size_y))
        self.speed = player_speed
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y
    def update(self):
        self.rect.y += self.speed
        global lost
        if self.rect.y > 500:
            self.rect.x = randint(80, 620)
            self.rect.y = 0
            lost += 1
    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))

class Bullet(sprite.Sprite):
    def __init__(self, player_image, player_x, player_y, size_x, size_y, player_speed):
        super().__init__()
        self.image = transform.scale(image.load(player_image), (size_x, size_y))
        self.speed = player_speed
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y
    def update(self):
        self.rect.y -= self.speed
        if self.rect.y < 0:
            self.kill()
    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))

asteroids = sprite.Group()
for i in range(3):
    asteroid = Enemy('asteroid.png', randint(30, 670), -40, 80, 50, randint(1, 7))
    asteroids.add(asteroid)

monsters = sprite.Group()
for i in range(5):
    monster = Enemy('ufo.png', randint(80, 620), -40, 80, 50, randint(1, 5))
    monsters.add(monster)

bullets = sprite.Group()

display.set_caption('Cosmo Shooter')
window = display.set_mode((700, 500))
background = transform.scale(image.load('galaxy.jpg'), (700, 500))

mixer.init()
mixer.music.load('space.ogg')
mixer.music.play()
fire_sound = mixer.Sound('fire.ogg')

ship = Player('rocket.png', 5, 400, 80, 100, 10)


goal = 20
lost = 0
max_lost = 15
win = 0
score = 0
life = 5
num_fire = 0

font.init()
font1 = font.SysFont('Arial', 36)
font2 = font.SysFont('Arial', 80)
win = font2.render('YOU WIN!', 1, (0, 255, 0))
lose = font2.render('YOU LOSE!', 1, (255, 0, 0))

finish = False
game = True
real_load = False

while game:
    for e in event.get():
        if e.type == QUIT:
            game = False
        elif e.type == KEYDOWN:
            if e.key == K_SPACE:
                if num_fire < 5 and real_load == False:
                    num_fire += 1
                    fire_sound.play()
                    ship.fire()
                if num_fire >= 5 and real_load == False:
                    last_time = timer()
                    real_load = True

    if not finish:
        window.blit(background, (0, 0))

        ship.update()
        ship.reset()

        monsters.update()
        monsters.draw(window)

        bullets.update()
        bullets.draw(window)

        asteroids.update()
        asteroids.draw(window)

        collides = sprite.groupcollide(monsters, bullets, True, True)

        if real_load == True:
            now_time = timer()
            if now_time - last_time < 2:
                reload = font1.render('Reloading!', 1, (150, 0, 0))
                window.blit(reload, (260, 460))
            else:
                num_fire = 0
                real_load = False

        for c in collides:
            score = score + 1
            monster = Enemy('ufo.png', randint(80, 620), -40, 80, 50, randint(1, 5))
            monsters.add(monster)

        bna_collides = sprite.groupcollide(bullets, asteroids, True, False)

        if sprite.spritecollide(ship, monsters, False) or sprite.spritecollide(ship, asteroids, False):
            sprite.spritecollide(ship, monsters, True)
            sprite.spritecollide(ship, asteroids, True)
            life -= 1

        if life == 0 or lost >= max_lost:
            finish = True
            window.blit(lose, (200, 200))

        if score >= goal:
            finish = True
            window.blit(win, (200, 200))

        text_life = font1.render(str(life), 1, (255, 255, 255))
        window.blit(text_life, (650, 10))
        text = font1.render('Счет: '+str(score), 1, (255, 255, 255))
        window.blit(text, (10, 20))
        text_lose = font1.render('Пропущено:'+str(lost), 1, (255, 255, 255))
        window.blit(text_lose, (10, 50))

    display.update()
    time.delay(50)
