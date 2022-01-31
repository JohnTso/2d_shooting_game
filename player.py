import pygame as pg
import const, math

from zombie import Zombie
from bullet import Bullet

class Player(pg.sprite.Sprite):
    def __init__(self, hp, speed, game):
        super().__init__()
        self.game = game
        self.hp = hp
        self.speed = speed
        self.x = 500
        self.y = 500
        self.bullets = []
        self.zombies = []
        self.image = game.ani_l[0]
        self.rect = pg.Surface.get_rect(self.image, topleft=(self.x, self.y))
        self.rect = self.rect.inflate(-40, -30)
        pg.draw.rect(self.game.screen, const.black, pg.Rect(self.x-2, self.y-15, 103, 10), 2)
        pg.draw.rect(self.game.screen, const.green, pg.Rect(self.x, self.y-13, self.hp, 6))
        self.game.screen.blit(self.game.hp_heart, (self.x-15, self.y-27))
        self.hits = 1

    def draw_player(self, x, y, frame):
        if self.hp <= 0:
            pg.quit()
            quit()
        self.x = x+500
        self.y = y+500
        self.image = self.game.ani_l[frame-1]
        
        if self.game.face_r:
            self.image = pg.transform.flip(self.image, True, False)
        self.rect = pg.Surface.get_rect(self.image, topleft=(self.x+5, self.y))
        self.rect = self.rect.inflate(-40, -30)
        pg.draw.rect(self.game.screen, const.black, pg.Rect(self.x-2, self.y-16, 102, 10), 2)
        pg.draw.rect(self.game.screen, (2.55*(100-self.hp), 2.55*self.hp, 0), pg.Rect(self.x, self.y-13, self.hp, 6))
        self.game.screen.blit(self.game.hp_heart, (self.x-15, self.y-27))
        self.game.screen.blit(self.image, (self.x, self.y))


    def draw_gun(self, x, y):
        self.mx = x
        self.my = y
        self.gun_x = self.x + 5
        self.gun_y = self.y + 30
        self.angle = int(360-math.atan2(self.my-self.y, self.mx-self.x)*180/math.pi)-90
        rotated_gun = pg.transform.rotate(self.game.gun, self.angle)
        self.game.screen.blit(rotated_gun,(self.gun_x, self.gun_y))

    def update_bullets(self):
        text = pg.font.SysFont("roman", 30)
        if self.bullets:

            for bullet in self.bullets:
                hits = pg.sprite.spritecollide(bullet, self.game.zombies, False)
                if hits:
                    self.bullets.remove(bullet)
                    for hit in hits:
                        self.game.hits = self.hits
                        self.acc = int(self.hits * (100 / self.game.shots))
                        if self.acc > 100:
                            self.acc = 100
                        self.game.acc_text_sur = text.render(f'Accuracy: {self.acc}%', False, const.red)
                        self.hits += 1
                        self.game.screen.blit(self.game.explo, (bullet.x, bullet.y))
                        hit.hp -= bullet.damage
                        bullet.kill()

                bullet.x += math.cos(bullet.angle) * bullet.speed
                bullet.y += math.sin(bullet.angle) * bullet.speed
                bullet.draw(bullet.x, bullet.y)

    def update_zombies(self):
        if self.zombies:

            for zombie in self.zombies:

                zombie.x += math.cos(zombie.angle) * zombie.speed
                zombie.y += math.sin(zombie.angle) * zombie.speed
                zombie.draw(zombie.x, zombie.y, self.x+10, self.y)


    def generate_bullet(self, mx, my):
        b = Bullet((self.gun_x, self.gun_y), self.angle, mx, my, self.game)
        self.bullets.append(b)


    def generate_zombies(self):
        z = Zombie(self.x, self.y, self.game)
        self.zombies.append(z)
        self.game.zombies.add(z)