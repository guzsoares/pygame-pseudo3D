from settings import *
import pygame as pg
import math

class RayCasting:
    def __init__(self, game):
        self.game = game
        self.raycast_result = []
        self.objects_to_render = []
        self.textures = self.game.object_renderer.wall_textures

    def get_objects_to_render(self):
        self.objects_to_render = []
        for ray, values in enumerate(self.raycast_result):
            depth, proj_height, texture, offset = values
            
            if proj_height < HEIGHT:
                wall_column = self.textures[texture].subsurface(offset * (TEXTURE_SIZE - SCALE), 0, SCALE, TEXTURE_SIZE)
                wall_column = pg.transform.scale(wall_column, (SCALE, proj_height))
                wall_pos = (ray * SCALE, HALF_HEIGHT - proj_height // 2)
            else:
                texture_height = TEXTURE_SIZE * HEIGHT / proj_height
                wall_column = self.textures[texture].subsurface(offset * (TEXTURE_SIZE - SCALE), HALF_TEXTURE_SIZE - texture_height // 2, SCALE, texture_height)
                wall_column = pg.transform.scale(wall_column, (SCALE, HEIGHT))
                wall_pos = (ray * SCALE, 0)

            self.objects_to_render.append((depth, wall_pos, wall_column))

    def raycast(self):
        self.raycast_result = []
        ox, oy = self.game.player.pos
        x_map, y_map = self.game.player.map_pos

        texture_vert, texture_hor = 1, 1

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
                    texture_hor = self.game.map.worldmap[tile_hor]
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
                    texture_vert = self.game.map.worldmap[tile_vert]
                    break
                x_vert += dx
                y_vert += dy
                depth_vert += delta_depth

            if depth_vert < depth_hor:
                depth = depth_vert
                texture = texture_vert
                y_vert %= 1
                offset = y_vert if ray_angle_cos > 0 else 1 - y_vert
            else:
                depth = depth_hor
                texture = texture_hor
                x_hor %= 1
                offset = x_hor if ray_angle_sin > 0 else 1 - x_hor

            # draw for debug
            pg.draw.line(self.game.screen, "red", (100 * ox, 100 * oy), (100 * ox + 100 * depth * ray_angle_cos, 100 * oy + 100 * depth * ray_angle_sin), 2)

            # corrige a profundidade para a inclinação do jogador
            depth *= math.cos(self.game.player.angle - ray_angle)

            proj_height = SCREEN_DIST / (depth + 0.0001)

            self.raycast_result.append((depth, proj_height, texture, offset))

            ray_angle += DELTA_ANGLE
            

    def update(self):
        self.raycast()
        self.get_objects_to_render()