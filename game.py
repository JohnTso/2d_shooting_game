import pygame as pg
import time, os, random
import const

from zombie import Zombie
from player import Player
from grass import Grass
from menu import Menu


class Game():

    def __init__(self):
        self.screen = screen
        self.zombies = pg.sprite.Group()
        self.load_images()
        self.player = Player(100, 7, self)
        self.running = True
        self.x, self.y = 0,0
        self.t1 = 0
        self.spawn_time = 0
        self.clock = pg.time.Clock()
        self.frame = 0
        self.frame_update = 0
        self.face_r = False
        self.key_list = []
        self.shots = 0
        self.hits = 0
        self.fps_time = 0
        self.fps = 0
        self.fps_count = 0
        self.grass_list = []
        self.volume = 50
        for _ in range(random.randint(30, 60)):
            g = Grass(self)
            self.grass_list.append(g)


    def load_images(self):
        self.gun = pg.image.load("images/gun.png")
        self.b = pg.image.load("images/bullet.png")
        self.aim_b = pg.image.load("images/aimbutton.png")
        self.explo = pg.image.load("images/explosion.png")
        self.zom_enemy = pg.image.load("images/enemy.png")
        self.hp_heart = pg.image.load("images/hp_icon.png")
        self.aid = pg.image.load("images/aid.png")
        self.knife = pg.image.load("images/knife.png")

        player_images = os.listdir("images/player")
        player_images.sort()
        self.ani_l = []
        for f in player_images[1:]:
            i = pg.image.load(f"images/player/{f}")
            self.ani_l.append(i)

    def update(self, f):
        screen.fill(const.gray)
        self.pos = pg.mouse.get_pos()
        for grass in self.grass_list:
            grass.draw()
        # pg.draw.rect(screen, const.yellow, pg.Rect(-self.player.x+400, -self.player.y+400, 1500, 1500), 7)
        text = pg.font.SysFont('Roman', 30)
        self.fps_text = text.render(f"FPS: {self.fps}", False, const.black)
        screen.blit(self.fps_text, (400, 10))
        if not self.shots:
            self.acc_text_sur = text.render('Accuracy: n/a', False, const.red)
            screen.blit(self.acc_text_sur, (10,10))
        else:
            screen.blit(self.acc_text_sur, (10,10))
        screen.blit(self.aim_b, (self.pos[0]-25, self.pos[1]-25))
        self.player.update_bullets()
        self.player.update_zombies()
        self.player.draw_player(self.x, self.y, f)
        self.player.draw_gun(self.pos[0], self.pos[1])
        pg.display.flip()
        self.fps_count += 1
        

    def run(self):

        if self.running:
            pg.mixer.music.set_volume(0.01*self.volume)
            pg.mixer.music.unpause()
            
        while self.running:

            if time.time() - self.spawn_time >= 5.5:
                self.spawn_time = time.time()
                self.player.generate_zombies()
            
            if time.time() - self.fps_time > 1:
                self.fps_time = time.time()
                self.fps = self.fps_count
                self.fps_count = 0

            dmg = pg.sprite.spritecollide(self.player, self.zombies, False)
            for d in dmg:
                if time.time() - d.dmg_cooldown >= 0.7:
                    d.dmg_cooldown = time.time()
                    self.player.hp -= d.damage

            self.clock.tick(60)
            pos = pg.mouse.get_pos()
            self.update(self.frame)
            pg.display.flip()
            keys = pg.key.get_pressed()
            for ev in pg.event.get():
                if ev.type == pg.QUIT:
                    quit()

                pg.key.set_repeat(25, 25)
                if ev.type == pg.KEYDOWN:
                    
                    if ev.key == pg.K_a:
                        self.face_r = True
                        self.x -= self.player.speed
                        if time.time() - self.frame_update > 0.12:
                            self.frame_update = time.time()
                            self.frame += 1
                            if self.frame > 12:
                                self.frame = 1
                        for grass in self.grass_list:
                            grass.x += 7
    

                    elif ev.key == pg.K_s: 
                        self.y += self.player.speed
                        if time.time() - self.frame_update > 0.12:
                            self.frame_update = time.time()
                            self.frame += 1
                            if self.frame > 12:
                                self.frame = 1
                        for grass in self.grass_list:
                            grass.y -= 7


                    elif ev.key == pg.K_d:
                        self.face_r = False
                        self.x += self.player.speed
                        if time.time() - self.frame_update > 0.12:
                            self.frame_update = time.time()
                            self.frame += 1
                            if self.frame > 12:
                                self.frame = 1
                        for grass in self.grass_list:
                            grass.x -= 7

                    elif ev.key == pg.K_w:
                        self.y -= self.player.speed
                        if time.time() - self.frame_update > 0.12:
                            self.frame_update = time.time()
                            self.frame += 1
                            if self.frame > 12:
                                self.frame = 1
                        for grass in self.grass_list:
                            grass.y += 7

                    if ev.key == pg.K_SPACE:
                        if time.time() - self.t1 >= 0.3:
                            self.shots += 1
                            self.t1 = time.time()
                            screen.blit(self.explo, (self.player.gun_x, self.player.gun_y))
                            self.player.generate_bullet(pos[0]-25, pos[1]-25)
                    
                    elif (keys[pg.K_a] or keys[pg.K_s] or keys[pg.K_d] or keys[pg.K_w]) and keys[pg.K_SPACE]:
                        
                        if time.time() - self.t1 >= 0.5:
                            self.shots += 1
                            self.t1 = time.time()
                            screen.blit(self.explo, (self.player.gun_x, self.player.gun_y))
                            self.player.generate_bullet(pos[0]-25, pos[1]-25)
    
                    if keys[pg.K_p]:
                        self.running = False

        if not self.running:
            pg.mouse.set_visible(True)
            pg.mixer.music.pause()
            self.menu = Menu()
            self.fade = pg.Surface((1000, 1000))
            self.fade.fill((0,0,0))
            self.fade.set_alpha(150)
            self.screen.blit(self.fade, (0,0))

            while not self.running:
                pos = pg.mouse.get_pos()
                for ev in pg.event.get():
                    self.menu.update(pos[0], pos[1], self,  pg.mouse.get_pressed(num_buttons=3)[0])
                    if ev.type == pg.QUIT:
                        quit()
                    elif ev.type == pg.KEYDOWN:
                        if ev.key == pg.K_o:
                            self.running = True
                            self.run()
                pg.display.flip()

if __name__ == "__main__":
    pg.init()
    screen = pg.display.set_mode((const.width, const.height))
    pg.display.set_caption("2D shooting game")
    pg.font.init()
    game = Game()
    pg.draw.rect(screen, const.black, pg.Rect(500,500,50,50))
    pg.mixer.music.load("straightfuse.mp3")
    pg.mixer.music.play(-1)
    pg.mixer.music.set_volume(0.2*game.volume)
    pg.mouse.set_visible(False)
    game.run()