import pygame as pg 
import const
class Menu:

    def __init__(self):
        self.volume = 50
        self.back_to_game = False
        self.volume_button = pg.Rect(350,250,200,50)
        self.volume_d_button = pg.Rect(300,350,50,50)
        self.volume_u_button = pg.Rect(550,350,50,50)
        self.back_to_game_button = pg.Rect(350,350,200,50)
        self.text = pg.font.SysFont('Arial', 30)
        self.vol_text = pg.font.SysFont('Arial', 25)
        self.btg_text = self.text.render("Back to Game", False, const.white)
        
    
    def update(self, mx, my, game, click):
        self.volume_text = self.vol_text.render(f"Volume: {game.volume}%", False, const.white)
        pg.draw.rect(game.screen, const.light_gray, self.back_to_game_button)
        pg.draw.rect(game.screen, const.light_gray, self.volume_button)
        pg.draw.rect(game.screen, const.white, self.volume_d_button)
        pg.draw.rect(game.screen, const.white, self.volume_u_button)

        game.screen.blit(self.btg_text, (355, 255))
        game.screen.blit(self.volume_text, (365, 360))
        if 350 < mx < 550:
            if 250 < my < 300:
                self.btg_text = self.text.render("Back to Game", False, const.blue)
                if click:
                    game.running = True
                    game.run()
            else:
                self.btg_text = self.text.render("Back to Game", False, const.white)
        elif 350 < my < 400:
            if 300 < mx < 350:
                self.volume_text = self.vol_text.render(f"Volume: {game.volume}%", False, const.blue)
                pg.draw.rect(game.screen, const.blue, self.volume_d_button)
                if click:
                    pg.draw.rect(game.screen, const.red, self.volume_d_button)
                    if game.volume:
                        game.volume -= 1
            elif 550 < mx < 600:
                self.volume_text = self.vol_text.render(f"Volume: {game.volume}%", False, const.blue)
                pg.draw.rect(game.screen, const.blue, self.volume_u_button)
                if click:
                    pg.draw.rect(game.screen, const.red, self.volume_u_button)
                    if game.volume < 100:
                        game.volume += 1



        