import pygame as pg
from settings import *

class ObjectRenderer:
    def __init__(self, game):
        self.game = game
        self.screen = game.screen
        self.wall_textures = self.load_wall_textures()
        self.sky_image = self.get_texture('textures/sky.png', (WIDTH, HALF_HEIGHT))
        self.sky_offset = 0
        self.blood_screen = self.get_texture('textures/blood_screen.png', (WIDTH, HEIGHT))
        self.digit_size = 80
        self.digit_images = [self.get_texture(f'textures/digits/{i}.png', [self.digit_size] * 2) for i in range(11)]
        self.digits = dict(zip(map(str, range(11)), self.digit_images))
        self.game_over_image = self.get_texture('textures/game_over.png', (WIDTH, HEIGHT))

    def draw(self):
        self.draw_background()
        self.render_game_objects()
        self.draw_player_health()
        self.draw_score()

    def game_over(self):
        self.screen.blit(self.game_over_image, (0, 0))
        
    def draw_player_health(self):
        health = str(self.game.player.health)
        for i, char in enumerate(health):
            self.screen.blit(self.digits[char], (i * self.digit_size, 0))
        self.screen.blit(self.digits['10'], (len(health) * self.digit_size, 0)) 
        

    def player_damage(self):
        self.screen.blit(self.blood_screen, (0, 0))
        pg.display.flip()
        pg.time.delay(10)

    def draw_background(self):
        self.sky_offset = (self.sky_offset + 4.5 * self.game.player.rel) % WIDTH
        self.screen.blit(self.sky_image, (-self.sky_offset, 0))
        self.screen.blit(self.sky_image, (-self.sky_offset + WIDTH, 0))

        pg.draw.rect(self.screen, FLOOR_COLOR, (0, HALF_HEIGHT, WIDTH, HEIGHT))

    def render_game_objects(self):
        list_objects = sorted(self.game.raycasting.objects_to_render, key=lambda t: t[0], reverse=True)
        for depth, pos, texture in list_objects:
            self.screen.blit(texture, pos)

    @staticmethod
    def get_texture(path, res=(TEXTURE_SIZE, TEXTURE_SIZE)):
        texture = pg.image.load(path).convert_alpha()
        return pg.transform.scale(texture, res)
    
    def load_wall_textures(self):
        return {
            1: self.get_texture("textures/bricks.png"),
            2: self.get_texture("textures/blood_wall1.png"),
            3: self.get_texture("textures/blood_wall2.png"),
            4: self.get_texture("textures/noblood_wall.png"),
            5: self.get_texture("textures/symbol_wall.png"),
        }
    
    def draw_score(self):
        """Desenha a pontuação na tela"""
        if hasattr(self.game, 'score_manager'):
            self.game.score_manager.draw_score(self.screen)