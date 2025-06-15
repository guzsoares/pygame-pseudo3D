from settings import *
import pygame as pg
import math

class RayCasting:
    def __init__(self, game):
        self.game = game

    def raycast(self):
        ox, oy = self.game.player.pos
        x_map, y_map = self.game.player.map_pos

        ray_angle = self.game.player.angle - HALF_FOV + 0.0001
        for ray in range(NUM_RAYS):
            ray_angle_sin = math.sin(ray_angle)
            ray_angle_cos = math.cos(ray_angle)

            # verifica as colisões horizontais
            y_hor, dy = (y_map + 1, 1) if ray_angle_sin > 0 else (y_map - 0.000001, -1)

            depth_hor = (y_hor - oy) / ray_angle_sin
            x_hor = ox + depth_hor * ray_angle_cos

            delta_depth = dy / ray_angle_sin
            dx = delta_depth * ray_angle_cos

            for i in range(MAX_DEPTH):
                tile_hor = int(x_hor), int(y_hor)
                if tile_hor in self.game.map.worldmap:
                    break
                x_hor += dx
                y_hor += dy
                depth_hor += delta_depth

            # verifica as colisões verticais
            x_vert, dx = (x_map + 1, 1) if ray_angle_cos > 0 else (x_map - 0.000001, -1)

            depth_vert = (x_vert - ox) / ray_angle_cos
            y_vert = oy + depth_vert * ray_angle_sin

            delta_depth = dx / ray_angle_cos
            dy = delta_depth * ray_angle_sin

            for i in range(MAX_DEPTH):
                tile_vert = int(x_vert), int(y_vert)
                if tile_vert in self.game.map.worldmap:
                    break
                x_vert += dx
                y_vert += dy
                depth_vert += delta_depth

            if depth_vert < depth_hor:
                depth = depth_vert
            else:
                depth = depth_hor

            # draw for debug
            #pg.draw.line(self.game.screen, "red", (100 * ox, 100 * oy), (100 * ox + 100 * depth * ray_angle_cos, 100 * oy + 100 * depth * ray_angle_sin), 2)

            # corrige a profundidade para a inclinação do jogador
            depth *= math.cos(self.game.player.angle - ray_angle)

            proj_height = SCREEN_DIST / (depth + 0.0001)

            # draw pseudo 3d walls
            color = [255 / (1 + depth ** 5 * 0.0002)] * 3
            pg.draw.rect(self.game.screen, color, (ray * SCALE, HALF_HEIGHT - proj_height // 2, SCALE, proj_height))


            ray_angle += DELTA_ANGLE
            

    def update(self):
        self.raycast()