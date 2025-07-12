import os
import pygame as pg
import math

class ScoreManager:
    def __init__(self, game):
        self.game = game
        self.current_score = 0
        self.highscore = 0
        self.highscore_file = 'highscore.txt'
        
        self.enemy_points = {
            'NPC': 50,
            'SoldierNPC': 100,
            'CacoDemonNPC': 200,
            'CyberDemonNPC': 500
        }
        
        self.new_record_timer = 0
        self.new_record_duration = 3000
        self.show_new_record = False
        
        self.floating_points = []
        
        self.enemies_killed = {
            'NPC': 0,
            'SoldierNPC': 0,
            'CacoDemonNPC': 0,
            'CyberDemonNPC': 0
        }
        self.total_enemies_killed = 0
        
        self.load_highscore()
        
        self.font = pg.font.Font(None, 36)
        self.small_font = pg.font.Font(None, 24)
        self.big_font = pg.font.Font(None, 48)
        self.floating_font = pg.font.Font(None, 28)
        
    def load_highscore(self):
        try:
            if os.path.exists(self.highscore_file):
                with open(self.highscore_file, 'r') as file:
                    self.highscore = int(file.read().strip())
            else:
                self.highscore = 0
        except (ValueError, FileNotFoundError):
            self.highscore = 0
            
    def save_highscore(self):
        try:
            with open(self.highscore_file, 'w') as file:
                file.write(str(self.highscore))
        except Exception as e:
            print(f"Erro ao salvar highscore: {e}")
            
    def add_points(self, enemy_type):
        points = self.enemy_points.get(enemy_type, 50)
        old_score = self.current_score
        self.current_score += points
        
        if enemy_type in self.enemies_killed:
            self.enemies_killed[enemy_type] += 1
        self.total_enemies_killed += 1
        
        if self.current_score > self.highscore:
            if old_score <= self.highscore:
                self.show_new_record = True
                self.new_record_timer = pg.time.get_ticks()
            self.highscore = self.current_score
            self.save_highscore()
            
        print(f"Inimigo {enemy_type} morto! +{points} pontos. Score: {self.current_score}")
        return points
        
    def reset_score(self):
        self.current_score = 0
        self.show_new_record = False
        self.enemies_killed = {
            'NPC': 0,
            'SoldierNPC': 0,
            'CacoDemonNPC': 0,
            'CyberDemonNPC': 0
        }
        self.total_enemies_killed = 0
        self.floating_points = []
        
    def draw_score(self, screen):
        self.update_floating_points()
        
        score_text = self.font.render(f"Pontuacao: {self.current_score}", True, (255, 255, 255))
        screen.blit(score_text, (10, 90))
        
        highscore_color = (255, 215, 0) if self.current_score == self.highscore and self.current_score > 0 else (200, 200, 200)
        highscore_text = self.small_font.render(f"Melhor pontuacao': {self.highscore}", True, highscore_color)
        screen.blit(highscore_text, (10, 120))
        
        self.draw_floating_points(screen)
        
        if self.show_new_record:
            current_time = pg.time.get_ticks()
            if current_time - self.new_record_timer < self.new_record_duration:
                alpha = int(127.5 * (1 + math.sin((current_time - self.new_record_timer) * 0.01)))
                record_text = self.big_font.render("Novo Recorde!", True, (255, 0, 0))
                record_surface = pg.Surface(record_text.get_size())
                record_surface.set_alpha(alpha)
                record_surface.blit(record_text, (0, 0))
                
                screen_width = screen.get_width()
                text_width = record_text.get_width()
                screen.blit(record_surface, ((screen_width - text_width) // 2, 150))
            else:
                self.show_new_record = False
        
    def add_floating_point(self, points, pos):
        floating_point = {
            'points': points,
            'pos': pos,
            'timer': pg.time.get_ticks(),
            'duration': 2000
        }
        self.floating_points.append(floating_point)
        
    def update_floating_points(self):
        current_time = pg.time.get_ticks()
        self.floating_points = [fp for fp in self.floating_points 
                               if current_time - fp['timer'] < fp['duration']]
        
    def draw_floating_points(self, screen):
        current_time = pg.time.get_ticks()
        
        for fp in self.floating_points:
            elapsed = current_time - fp['timer']
            progress = elapsed / fp['duration']
            
            if progress < 1.0:
                screen_x = int(fp['pos'][0] * 50 + 200)
                screen_y = int(fp['pos'][1] * 50 + 200 - (progress * 50))
                
                alpha = int(255 * (1 - progress))
                color = (0, 255, 0) if fp['points'] > 0 else (255, 0, 0)
                
                text = self.floating_font.render(f"+{fp['points']}", True, color)
                text_surface = pg.Surface(text.get_size())
                text_surface.set_alpha(alpha)
                text_surface.blit(text, (0, 0))
                
                if 0 <= screen_x <= screen.get_width() and 0 <= screen_y <= screen.get_height():
                    screen.blit(text_surface, (screen_x, screen_y))

    def get_score_info(self):
        return {
            'current_score': self.current_score,
            'highscore': self.highscore,
            'is_new_record': self.current_score == self.highscore and self.current_score > 0
        }
