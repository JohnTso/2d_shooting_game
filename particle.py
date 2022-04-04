import pygame as pg

class Particle(pg.sprite.Sprite):

    def __init__(self, type, game):
        super().__init__()
        self.change_in_y = 0
        self.alpha = 225
        if type == "coin":
            self.image = game.gold_particle
        elif type == "hp":
            self.image = game.hp_particle

    def draw(self, px, py, screen):
        if self.change_in_y < -15:
            self.kill()
        self.image.set_alpha(self.alpha)
        self.alpha -= 5
        self.change_in_y -= 1
        screen.blit(self.image, (px+5, py+self.change_in_y))
