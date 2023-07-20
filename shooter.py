from pygame import *
from random import randint


class GameSprite(sprite.Sprite):
    def __init__(self, player_image, player_x, player_y, size_x, size_y, player_speed):
        sprite.Sprite.__init__(self)
        self.image = transform.scale(image.load(player_image), (size_x, size_y))
        self.speed = player_speed
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y

    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))


class Player(GameSprite):
    def init(self, player_image, player_x, player_y, size_x, size_y, player_speed):
        super().__init__(player_image, player_x, player_y, size_x, size_y, player_speed)

    def update(self):
        keys = key.get_pressed()
        if keys[K_LEFT] and self.rect.x > 5:
            self.rect.x -= self.speed
        if keys[K_RIGHT] and self.rect.x < 620:
            self.rect.x += self.speed

    def fire(self):
        bullet = Bullet('bullet.png', self.rect.centerx, self.rect.top, 15, 20,15)
        bullets.add(bullet)


class Enemy(GameSprite):
    def update(self):
        self.rect.y += self.speed
        global lost
        if self.rect.y > 500:
            self.rect.x = randint(80, 620)
            self.rect.y = 0
            lost = lost + 1


class Bullet(GameSprite):
    def update(self):
        self.rect.y -= self.speed
        if self.rect.y < 0:
            self.kill()


window = display.set_mode((700, 500))
display.set_caption("Shooter")
background = transform.scale(image.load("galaxy.jpg"), (700, 500))

mixer.init()
mixer.music.load("space.ogg")
fire_sound = mixer.Sound('fire.ogg')

ship = Player("rocket.png", 5, 400, 80, 100, 10)
monsters = sprite.Group()
for i in range(5):
    monster = Enemy('ufo.png', randint(80, 620), -40, 80, 50, randint(1, 5))
    monsters.add(monster)
bullets = sprite.Group()
lost = 0
score = 0
font.init()
font1 = font.SysFont('Arial', 36)
font2 = font.SysFont('Arial', 80)

win = font2.render('YOU WIN!', 1, (255, 255, 255))
lose = font2.render('YOU LOSE!', 1, (255, 255, 255))

finish = False
game = True
while game:
    for e in event.get():
        if e.type == QUIT:
            game = False
        elif e.type == KEYDOWN:
            if e.key == K_SPACE:
                fire_sound.play()
                ship.fire()

    if lost > 5:
        window.blit(lose, (10, 20))
        finish = True

    elif score >= 10:
        window.blit(win, (10, 20))
        finish = True

    if not finish:
        window.blit(background, (0, 0))
        text = font1.render("Счёт" + str(score), 1, (255, 255, 255))
        window.blit(text, (10, 20))
        text_lose = font1.render("Пропущено:" + str(lost), 1, (255, 255, 255))
        window.blit(text_lose, (10, 50))
        ship.update()
        ship.reset()
        monsters.update()
        monsters.draw(window)
        bullets.update()
        bullets.draw(window)

        display.update()

    time.delay(50)