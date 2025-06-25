from sprite_object import *

class ObjectHandler:
    def __init__(self, game):
        self.game = game
        self.sprite_list = []
        self.static_sprite_path = 'sprites/static_sprites/'
        self.animated_sprite_path = 'sprites/animated_sprites/'
        add_sprite = self.add_sprite

        # sprites
        add_sprite(SpriteObject(game))
        add_sprite(AnimatedSprite(game))

    def update(self):
        for sprite in self.sprite_list:
            sprite.update()

    def add_sprite(self, sprite):
        self.sprite_list.append(sprite)