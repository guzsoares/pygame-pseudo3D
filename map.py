import pygame as pg

# A = AIR
# 1 = WALL
A = False

minimap = [[1,1,1,1,1,1,1,1,3,3,2,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4],
           [1,A,A,A,A,A,A,1,2,A,2,4,4,4,4,4,A,A,A,A,A,A,A,A,A,A,A,A,A,A,A,4],
           [1,A,A,1,1,1,1,1,3,A,3,2,2,2,3,4,A,A,A,A,A,A,A,A,A,A,A,A,A,A,A,4],
           [1,A,A,A,A,A,A,1,2,A,A,A,A,A,2,4,A,A,A,A,A,A,4,4,A,A,A,A,A,A,A,4],
           [1,A,A,A,A,A,A,1,2,A,A,A,A,A,3,4,A,A,A,A,A,A,4,4,A,A,A,A,A,A,A,4],
           [1,A,A,1,1,1,1,1,2,A,A,A,A,A,3,4,A,A,A,A,A,A,4,4,A,A,A,A,A,A,A,4],
           [1,A,A,1,3,2,2,3,3,A,A,A,A,A,2,4,A,A,A,A,A,A,4,4,A,A,A,A,A,A,A,4],
           [1,A,A,A,A,A,A,A,A,A,A,A,A,A,2,4,A,A,A,A,A,A,A,A,A,A,A,A,A,A,A,4],
           [1,A,A,1,3,A,A,A,A,A,A,A,A,A,2,4,A,A,A,A,A,A,A,A,A,A,A,A,A,A,A,4],
           [1,A,A,1,2,A,3,2,2,2,3,2,3,2,3,4,A,A,A,A,A,A,A,A,A,A,A,A,4,A,A,4],
           [1,A,A,1,2,A,A,A,A,A,A,A,A,A,A,A,A,A,A,A,A,A,A,A,A,A,A,A,4,A,A,4],
           [1,A,A,1,3,A,A,A,A,A,A,A,2,2,3,4,A,A,A,A,A,A,A,A,A,A,A,A,4,A,A,4],
           [1,1,1,1,3,3,2,2,2,3,3,2,2,2,2,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4]]

class Map:
    def __init__(self, game):
        self.game = game
        self.minimap = minimap
        self.worldmap = {}
        self.get_map()

    # gera um dicionário com as coordenadas das paredes
    def get_map(self):
        for j, row in enumerate(self.minimap):
            for i, value in enumerate(row):
                if value:
                    self.worldmap[(i, j)] = value
                    print(self.worldmap)

    def draw(self):
        [pg.draw.rect(self.game.screen, "darkgray", (x * 100, y * 100, 100, 100), 2) for x, y in self.worldmap]



