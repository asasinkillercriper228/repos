from pygame import *
import sys

game = True
finish = False

WINDOW_SIZE = (700, 500)


window = display.set_mode(WINDOW_SIZE)
display.set_caption('Jungle maze')

clock = time.Clock()
FPS = 60


font.init()
font = font.Font(None, 70)
mixer.init()
mixer.music.load('jungles.ogg')
mixer.music.play()
win = font.render('YOU WIN!', True, (255,209,0))
lose = font.render('YOU LOSE!', True, (255,0,0))

class GameSprite(sprite.Sprite):
    def __init__(self, Image, SIZE, x=0, y=0):
        super().__init__()

        self.image = transform.scale(
            image.load(Image),
            SIZE
        )
        self.rect = self.image.get_rect()
        self.Speed = 0

        self.x = x
        self.y = y

        self.rect.x = self.x
        self.rect.y = self.y
    def check_collide(self, Target):
        global finish
        if sprite.collide_rect(self, Target):
            money = mixer.Sound('money.ogg')
            money.play()
            window.blit(win, (200, 200))
            finish = True
        return finish
            
    def show(self, Window):
        self.update()
        self.rect.x = self.x
        self.rect.y = self.y
        Window.blit(self.image, (self.rect.x, self.rect.y))

class Player(GameSprite):
    def __init__(self, Image, SIZE, x=0, y=0):
        super().__init__(Image, SIZE,x,y)

        self.Speed = 5

    def Control(self, Keys):
        if Keys[K_UP]:
            if self.y > 0:
                self.y-=self.Speed
        if Keys[K_DOWN]:
            if self.y < WINDOW_SIZE[1]-100:
                self.y+=self.Speed
        if Keys[K_RIGHT]:
            if self.x < WINDOW_SIZE[0]-100:
                self.x+=self.Speed
        if Keys[K_LEFT]:
            if self.x > 0:
                self.x-=self.Speed

class Enemy(GameSprite):
    def __init__(self, Image, SIZE, x=0, y=0):
        super().__init__(Image, SIZE,x,y)
    
        self.offset = 0
        self.Speed = 3

    def check_collide(self, Target):
        global finish
        if sprite.collide_rect(self, Target):
            kick = mixer.Sound('kick.ogg')
            kick.play()
            window.blit(lose, (200, 200))
            finish = True
        return finish
            
    

    def automatic_move(self):
        if self.offset <= -60:
            self.Speed = 3
        elif self.offset >= 60:
            self.Speed = -3
        self.offset += self.Speed
        self.x += self.Speed


Background = GameSprite('background.jpg', WINDOW_SIZE)
Main_Character = Player('hero.png', (60,60), 100,250)
gold = GameSprite('treasure.png', (60,60), 500,400)
Cyborg = Enemy('cyborg.png', (60,60), 500, 300)

while game:
    Background.show(window)

     
    Main_Character.show(window)
    Cyborg.show(window)
    gold.show(window)

    for Event in event.get():
        if Event.type == QUIT:
            game = False
    if finish != True:
        KeysPressed = key.get_pressed()
        Main_Character.Control(KeysPressed)
        Cyborg.automatic_move()

        l = Cyborg.check_collide(Main_Character)
        w = gold.check_collide(Main_Character)
        if l == True or w == True:
            finish =True
        

    clock.tick(FPS)
    display.update()
