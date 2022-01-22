import random, math, const
import pygame as pg

class Zombie(pg.sprite.Sprite):

    def __init__(self, px, py, game):
        super().__init__()
        self.game = game
        self.hp = random.randint(40,50)
        self.hp_copy = self.hp
        self.damage = random.randint(5, 10)
        spawn_x = [0, 1000]
        spawn_y = [0, 500, 1000]
        self.x = random.sample(spawn_x, 2)[0]
        self.y = random.sample(spawn_y, 3)[0]
        self.rise = py - self.y
        self.run = px - self.x
        self.angle = math.atan2(self.rise, self.run)
        self.rect = pg.Rect(self.x+12, self.y, 50, 70)
        self.speed = random.randint(2, 4)
        self.dmg_cooldown = 0
        self.image = self.game.zom_enemy
        self.aid = False


    def draw(self, x, y, px, py):

        if self.hp <= 0:
            self.game.player.zombies.remove(self)
            self.game.zombies.remove(self)
            self.kill()

        self.x = x
        self.y = y
        self.rise = py - self.y
        self.run = px - self.x
        self.angle = math.atan2(self.rise, self.run)
        self.rot_ang = int(360-self.angle*180/math.pi) - 90
        rotated_knife = pg.transform.rotate(self.game.knife, self.rot_ang)
        # self.rect = pg.Surface.get_rect(knife, topleft=(self.x, self.y))
        # self.rect = self.rect.inflate(-30, -27)
        # self.rect[2] += 5
        self.rect = pg.Surface.get_rect(self.game.zom_enemy, topleft=(self.x, self.y))
        self.rect = self.rect.inflate(-25, -20)
        # pg.draw.ellipse(screen, self.color, pg.Rect(x, y, 50, 70))
        self.game.screen.blit(self.image, (x, y))
        self.game.screen.blit(rotated_knife, (x-20, y-15))
        g = 2.55*(self.hp * 100/self.hp_copy)
        r = 2.55*(self.hp_copy-self.hp)
        if 0 < r < 255 and 0 < g < 255:
            pg.draw.rect(self.game.screen, const.black, pg.Rect(self.x-2 + self.hp_copy//3, self.y-16, self.hp_copy+3, 10), 2)
            pg.draw.rect(self.game.screen, (r, g, 0), pg.Rect(self.x + self.hp_copy//3, self.y-13, self.hp, 6))
        else:
            pg.draw.rect(self.game.screen, const.black, pg.Rect(self.x - 2 + self.hp_copy//3, self.y-16, self.hp_copy+3, 10), 2)
            pg.draw.rect(self.game.screen, const.green, pg.Rect(self.x + self.hp_copy//3, self.y-13, self.hp, 6))
        # pg.draw.rect(screen, YELLOW, self.rect)