# создай свой персональный ад!
from pygame import *
from random import *

#создание окошка
window =display.set_mode((1600,900), RESIZABLE)
display.set_caption('Битва за Беларусь!')

#классы, функции, террористы!
class GameSprite(sprite.Sprite):
    def __init__(self,player_image, player_x, player_y, size_x, size_y, player_speed):
        sprite.Sprite.__init__(self)
        self.image = transform.scale(image.load(player_image), (size_x, size_y))
        self.speed = player_speed
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y

    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))

class Player(GameSprite):
    #управление танком
    def update(self):
        keys = key.get_pressed()
        if keys[K_a] and self.rect.x > 5:
            self.rect.x -= self.speed
        if keys [K_d] and self.rect.x < 1600 - 80:
            self.rect.x += self.speed

#стрельба
    def fire(self):
        bullet = Bullet('bullet.png', self.rect.centerx, self.rect.top, 15, 20, -15)
        bullets.add(bullet)

class Bullet (GameSprite):
    #движение картохи
    def update(self):
        self.rect.y += self.speed
        if self.rect.y < 0:
            self.kill()

#ПИНДОСЫ
class Enemy(GameSprite):
    #движениепиндоса
    def update(self):
        self.rect.y += self.speed
        global lost
        # исчезновение пиндоса
        if self.rect.y > win_height:
            self.rect.x = randint(80, win_width - 80)
            self.rect.y = 0
            lost = lost + 1


win_width = 1600
    

#добавления ресурсов для прилжения
background = transform.scale(image.load('galaxy.jpg'), (1600,900))

#кораблик лукашенко
ship = Player ('rocket.png', 5 , 600, 300, 300, 10)

#АТАКУЮЩИЕПИНДОСЫ
monsters = sprite.Group()
for i in range (1, 6):
    monster = Enemy ('asteroid.png', randint (80, win_width - 80) -40, 80, 50, 100, randint(1,5))
    monsters.add(monster)

#счет
score = 0 #счет положительных 
lost = 0 #пропущенные
bullets = sprite.Group()

#музыка
mixer.init()
mixer.music.load('space.ogg')
mixer.music.play()


#параметры игры
finish = False
game = True
clock = time.Clock()
FPS = 60
max_lost = 1
goal = 29
font.init()
font2 = font.SysFont("Arial", 40)

    


# игровой цикл, что бы игра работала
while game:

    for e in event.get():
        if e.type == QUIT:
            game = False
            
        elif e.type == KEYDOWN:
            if e.key == K_SPACE:
                print ('огонь')
                # fire_sound.play()
                ship.fire()
 
    if finish != True:
        window.blit(background, (0, 8))
        #движения челов
        ship.update()

        # обновляем их в новом местоположении

        ship.reset()

        collides = sprite.groupcollide(monsters,bullets, True, True)
        for c in collides:
            score = score + 1
            monster = Enemy(img_enemy, randint(80, win_width - 80),
                            -40, 80, 50, randint(1,5))
            monster.add(monster)

        if sprite.spritecollide(ship, monsters, False) or lost >= max_lost:
            finish = True 
            window.blit(lose, (200, 200))

        if score >= goal:
            finish = True
            window.blit(win, (200, 200))

        text = font2.render ('Счёт:' + str (score), 1, (255, 255, 255))
        window.blit(text, (10, 20))

        text_lose = font2.render ('Пропущено:' + str(lost), 1, (255, 255, 255))
        window.blit(text_lose, (10, 50))

    else:
        finish = False
        score = 0
        lost = 0

        for b in bullets:
            b.kill()
        for m in monsters:
            m.kill()

        time.delay (3000)
        
        for i in range (1, 6):
            monster = Enemy (img_enemy, randint(80, win_width - 80) -40, 80, 50, randint (1, 5))
            monsters.add(monster)
    
    display.update()

    clock.tick(FPS)
