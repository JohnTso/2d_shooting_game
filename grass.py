import pygame as pg
import random

class Grass:

    def __init__(self, game):
        self.game = game
        self.image = pg.image.load("images/grass.png")
        pg.transform.scale(self.image, (random.randint(15,20),random.randint(15,20)))
        self.x = random.randint(-100, 1500)
        self.y = random.randint(-100, 1500)
    
    def draw(self):
        self.game.screen.blit(self.image, (self.x, self.y))
