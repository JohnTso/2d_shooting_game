import pygame as pg
import const, math


class Bullet(pg.sprite.Sprite):

    def __init__(self, pos, r_ang, mx, my, game):
        super().__init__()
        self.game = game
        self.image = self.game.b
        self.x = pos[0]
        self.y = pos[1]
        self.rise = my - self.y
        self.run = mx - self.x
        self.angle = math.atan2(self.rise, self.run)
        self.image = pg.transform.rotate(self.image, r_ang)
        self.rect = self.image.get_rect(center=(pos))
        self.speed = 20
        self.damage = 5
        self.text = pg.font.SysFont("roman", 30)

    def draw(self, x, y):
        self.bx = x
        self.by = y
        self.rect = pg.Surface.get_rect(self.image, topleft=(x,y))
        mx = -self.rect[2]+10
        my = -self.rect[3]+10
        self.rect = self.rect.inflate(mx, my)
        # pg.draw.rect(screen, YELLOW, self.rect)
        self.game.screen.blit(self.image, (self.bx, self.by))
        if 0 > self.bx or self.bx > const.width or 0 > self.by or self.by > const.height:
            self.game.acc_text_sur = self.text.render(f'Accuracy: {int(self.game.hits * (100 / self.game.shots))}%', False, const.red)
            self.game.player.bullets.remove(self)
            self.kill()