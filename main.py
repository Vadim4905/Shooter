#https://pixabay.com/ru/
#https://incompetech.com/music/royalty-free/music.html
# git init
# git add .
# git commit -m 'коментарій'
# git remote add ім'я посилання
# git push ім'я master
#pyinstaller --onefile main.py --windowed    
from pygame import *
from random import randint
import os
import sys
import time as t
sys.path.append(os.path.join(os.path.abspath(__file__+'/..'),'levels'))
import level1 as lv1
import level2 as lv2
import level3 as lv3

space_ost = os.path.join(os.path.abspath(__file__+'/..'),'ost','space.ogg')
explosion_ost= os.path.join(os.path.abspath(__file__+'/..'),'ost','explosion.ogg')
fire_ost = os.path.join(os.path.abspath(__file__+'/..'),'ost','fire.ogg')
victory_ost = os.path.join(os.path.abspath(__file__+'/..'),'ost','victory.ogg')

galaxy_img = os.path.join(os.path.abspath(__file__+'/..'),'pictures','galaxy.jpg')
bullet_img = os.path.join(os.path.abspath(__file__+'/..'),'pictures','bullet.png')
rocket_img = os.path.join(os.path.abspath(__file__+'/..'),'pictures','rocket.png')
ufo1_img = os.path.join(os.path.abspath(__file__+'/..'),'pictures','ufo1.png')
ufo2_img = os.path.join(os.path.abspath(__file__+'/..'),'pictures','ufo2.png')
ufo3_img = os.path.join(os.path.abspath(__file__+'/..'),'pictures','ufo3.png')
red_button = os.path.join(os.path.abspath(__file__+'/..'),'pictures','red_button.png')
green_button = os.path.join(os.path.abspath(__file__+'/..'),'pictures','green_button.png')

ufo1_img = transform.scale(image.load(ufo1_img),(100,50))
ufo2_img = transform.scale(image.load(ufo2_img),(100,50))
ufo3_img = transform.scale(image.load(ufo3_img),(100,50))


class Level():
    def __init__(self,monsters,monsters_amount,name):
        self.ship  = Player(100,390,rocket_img,70,100)
        self.score = 0
        self.miss = 0
        self.all_monsters = monsters
        self.name = name 
        self.monster_data = monsters.copy()
        self.monsters  = sprite.Group()
        self.bullets = sprite.Group()
        self.finish = False
        self.monsters_amount = monsters_amount
        
               

    def update(self):
        score_lb = font1.render(f'Monsters left: {len(self.all_monsters)+len(self.monsters)}',True,(255,255,255))
        miss_lb = font1.render(f'Missed: {self.miss}/3',True,(255,255,255))

        self.ship.update()
        self.ship.draw()

        self.monsters.update()
        self.monsters.draw(window)

        self.bullets.update()
        self.bullets.draw(window)
        
        window.blit(score_lb,(10,20))
        window.blit(miss_lb,(10,50))

    def name_representation(self):
        window.blit(background,(0,0))
        lb = font.Font(None,100).render(self.name,True,	(255,248,220))
        window.blit(lb,(250,200))
        display.update()
        time.delay(2000)

class GameSprite(sprite.Sprite):
    def __init__(self,x,y,img,width,height):
        super().__init__()
        try:
            self.image = transform.scale(image.load(img),(width,height))
        except:
            self.image = img
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y


    def draw(self):
        window.blit(self.image,(self.rect.x,self.rect.y))        

class Button(GameSprite):
    def __init__(self,x,y,img,width,height,text,font_size,shift_x,shift_y):
        super().__init__(x,y,img,width,height)
        self.text = text
        self.font_size=font_size
        self.shift_x = shift_x
        self.shift_y = shift_y
        #317 x 74
        #4.2

    def draw(self):
        window.blit(self.image,(self.rect.x,self.rect.y))
        lb = font.Font(None,self.font_size).render(self.text,True,(0,0,0))
        window.blit(lb,(self.rect.x+self.shift_x,self.rect.y+self.shift_y,))

    def collidepoint(self,x,y):
        return self.rect.collidepoint(x,y)
        
class Game_Menu():
    def __init__(self):
        self.start_but = Button(230,100,green_button,210,50,'Start game',30,50,15)
        self.quit_but = Button(230,300,red_button,210,50,'Quit',30,75,15)
        self.level_num = -1
        monsters1 = [Weak(100,50)for i in range(lv1.weak)]+[Normal(100,50)for i in range(lv1.normal)]+[Strong(100,50)for i in range(lv1.hard)]
        monsters2 = [Weak(100,50)for i in range(lv2.weak)]+[Normal(100,50)for i in range(lv2.normal)]+[Strong(100,50)for i in range(lv2.hard)]
        monsters3 = [Weak(100,50)for i in range(lv3.weak)]+[Normal(100,50)for i in range(lv3.normal)]+[Strong(100,50)for i in range(lv3.hard)]
        level1 =Level(monsters1,lv1.monsters_amount,lv1.name)
        level2 =Level(monsters2,lv2.monsters_amount,lv2.name)
        level3 =Level(monsters3,lv3.monsters_amount,lv3.name)
        self.levels = [level1,level2,level3]

    def update(self):
        self.start_but.draw()
        self.quit_but.draw()
    
    def mouse_button_event(self,x,y):
        if self.start_but.collidepoint(x,y):
            self.next_level()
        if self.quit_but.collidepoint(x,y):
            exit()

    def next_level(self):
        global level
        self.level_num += 1

                
        level = self.levels[self.level_num]
        level.name_representation()
        start_game()

    def restart(self):
        global level
        level_num = self.level_num
        self.__init__()
        self.level_num = level_num
        level = self.levels[self.level_num]
        level.name_representation()

class Player(GameSprite):
    def __init__(self,x,y,img,width,height):
        super().__init__(x,y,img,width,height)
        #1302x1920
        self.speed = 5
    
    def update(self):
        keys_pressed = key.get_pressed() 
        if keys_pressed[K_LEFT] and self.rect.x >0:
            self.rect.x -= self.speed
        if keys_pressed[K_RIGHT] and self.rect.right < win_width :
            self.rect.x += self.speed
            
    def fire(self):
        bullet = Bullet(self.rect.centerx,self.rect.top,bullet_img,5,20)
        level.bullets.add(bullet)
        fire.play() 

class Enemy(GameSprite):
    def __init__(self,img,width,height):
        #1280x649
        x = randint(0,win_width-width)
        y = -height
        super().__init__(x,y,img,width,height) 
        self.num = 0

    def update(self):
        global miss
        if self.num % 3 == 0:
            self.rect.y += self.speed
        self.num += 1

        if self.health <= 0:
            level.score += 1
            self.kill()

        if self.rect.y > win_height:
            self.kill()
            level.miss += 1


class Weak(Enemy):
    def __init__(self,width,height):
        self.speed = 4
        self.health = 1
        super().__init__(ufo1_img,width,height)

class Normal(Enemy):
    def __init__(self,width,height):
        self.speed = 3
        self.health = 2
        super().__init__(ufo2_img,width,height)

class Strong(Enemy):
    def __init__(self,width,height):
        self.speed = 2
        self.health = 4
        super().__init__(ufo3_img,width,height)

    


class Bullet(GameSprite):
    def __init__(self,x,y,img,width,height):
        super().__init__(x,y,img,width,height)
        self.speed = 10
    
    def update(self):
        self.rect.y -= self.speed
        if self.rect.y < 0:
            self.kill()
    

mixer.init()
font.init()

font1 = font.Font(None,20)
font2 = font.Font(None,80)
font3 = font.Font(None,60)

win1_lb = font2.render('YOU WIN!',True,(255,215,0))
win2_lb = font3.render('Press ENTER if you want go on',True,(255,215,0))
lost1_lb = font2.render('YOU LOST!',True,(255,0,0))
lost2_lb = font3.render('Press ENTER if you want restart',True,(255,0,0))

#создай окно игры
win_width = 700
win_height = 500
window  = display.set_mode((win_width, win_height))
display.set_caption('Shooter')
FPS = 60
clock = time.Clock()

mixer.music.load(space_ost)
mixer.music.play(-1)

fire = mixer.Sound(fire_ost)
explosion = mixer.Sound(explosion_ost)
victory = mixer.Sound(victory_ost)

background = transform.scale(image.load(galaxy_img),(win_width, win_height))

start = t.time()

print(t.time()-start)


def start_game():
    global level
    while True:
        window.blit(background,(0,0))
        if not level.finish:
            level.update()

        for e in event.get():
            if e.type == QUIT:
                exit()
            if e.type == KEYDOWN:
                if e.key == K_SPACE and not level.finish:
                    level.ship.fire()

        sprites_list = sprite.groupcollide(level.monsters,level.bullets,False,True)
        for enemy in sprites_list:
            enemy.health -= 1
            

        monsters = []
        for i in range(level.monsters_amount -  len(level.monsters)):
            try:
                num = randint(0,len(level.all_monsters)-1)
                monsters.append(level.all_monsters[num])
                level.all_monsters.pop(num)
            except ValueError:
                pass
            
        level.monsters.add(monsters)

        if sprite.spritecollide(level.ship,level.monsters,False) and not level.finish:
            explosion.play()

        if sprite.spritecollide(level.ship,level.monsters,False)  or level.miss >= 3:
            window.blit(lost1_lb,(200,150))
            window.blit(lost2_lb,(40,300))
            level.finish = True
            if key.get_pressed()[K_RETURN ]:
                game_menu.restart()
            
        
        if not level.all_monsters and len(level.monsters) == 0:
            if game_menu.level_num == len(game_menu.levels) -1:
                victory.play() 
                game_menu.__init__()
            window.blit(win1_lb,(200,150))
            window.blit(win2_lb,(50,300))
            level.finish = True
            if key.get_pressed()[K_RETURN ]:
                return

        display.update()
        clock.tick(FPS)  

game_menu = Game_Menu()
def main():
    while True:
        window.blit(background,(0,0))
        game_menu.update()
        for e in event.get():
            if e.type == QUIT:
                exit()
            if e.type == MOUSEBUTTONDOWN and e.button == 1:
                game_menu.mouse_button_event(*e.pos)
        if game_menu.level_num != -1:
            game_menu.next_level()
        display.update()
        clock.tick(FPS)  
main()
