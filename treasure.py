import pygame as pg
import random, math

class Treasure(pg.sprite.Sprite):

    def __init__(self, x, y):
        super().__init__()
        self.x = x
        self.y = y
        self.coin_flip = random.randint(0, 1)

        if self.coin_flip:
            self.image = pg.image.load("images/coin.png")
            self.type = 'coin'
        else:
            self.image = pg.image.load("images/aid.png")
            self.type = 'hp'

        self.rect = self.image.get_rect(center = (self.x, self.y))
        self.angle = 0

    def draw(self, game):
        self.rect = self.image.get_rect(center = (self.x, self.y))
        if self not in game.treasures:
            self.kill()
        self.new_width = round(math.sin(self.angle) * self.rect.width)
        self.angle += .05
        self.rot_image = self.image if self.new_width >= 0 else pg.transform.flip(self.image, True, False) 
        self.rot_image = pg.transform.scale(self.rot_image, (abs(self.new_width), self.rect.height))
        game.screen.blit(self.rot_image, self.rot_image.get_rect(center = (self.x, self.y)))




