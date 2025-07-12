from sprite_object import *
from npc import *
import pygame as pg
import random
import math

class ObjectHandler:
    def __init__(self, game):
        self.game = game
        self.sprite_list = []
        self.npc_list = []
        self.npc_sprite_path = 'sprites/npc/'
        self.static_sprite_path = 'sprites/static_sprites/'
        self.animated_sprite_path = 'sprites/animated_sprites/'
        add_sprite = self.add_sprite
        add_npc = self.add_npc
        self.npc_positions = {}
        
        # Enemy spawning system
        self.spawn_timer = 0
        self.spawn_delay = 5000  # 5 seconds in milliseconds
        self.min_spawn_distance = 8  # minimum distance from player
        self.max_spawn_distance = 15  # maximum distance from player
        self.max_enemies = 15  # maximum enemies on map at once
        
        # Enemy classes with their spawn weights
        self.enemy_classes = {
            SoldierNPC: 50,  # higher = more common
            CacoDemonNPC: 30,
            CyberDemonNPC: 10  # rare but powerful
        }

        # sprites
        add_sprite(SpriteObject(game))
        add_sprite(AnimatedSprite(game))

        # Initial enemies
        add_npc(SoldierNPC(game, pos=(8.5, 4.5)))
        add_npc(CacoDemonNPC(game, pos=(3.5, 4.5)))

    def update(self):
        self.npc_positions = {npc.map_pos for npc in self.npc_list if npc.alive}
        
        # Update sprites and NPCs
        for sprite in self.sprite_list:
            sprite.update()
        for npc in self.npc_list:
            npc.update()
        
        # Remove NPCs only after death animation is complete
        self.npc_list = [npc for npc in self.npc_list if self.should_keep_npc(npc)]
        
        # Handle enemy spawning
        self.handle_spawning()

    def should_keep_npc(self, npc):
        """Determine if an NPC should be kept in the list"""
        # Keep alive NPCs
        if npc.alive:
            return True
        
        # Check if this NPC just died and hasn't been scored yet
        if not hasattr(npc, 'scored'):
            # Add points for killing this enemy
            if hasattr(self.game, 'score_manager'):
                enemy_type = npc.__class__.__name__
                points = self.game.score_manager.add_points(enemy_type)
                # Adicionar ponto flutuante na posição do inimigo
                self.game.score_manager.add_floating_point(points, (npc.x, npc.y))
            npc.scored = True  # Mark as scored to avoid double scoring
        
        # Keep dead NPCs until their death animation is complete
        if hasattr(npc, 'frame_counter') and hasattr(npc, 'death_images'):
            return npc.frame_counter < len(npc.death_images) - 1
        
        # If we can't determine animation state, keep for a short time
        return False

    def handle_spawning(self):
        """Handle the enemy spawning system with time delays"""
        current_time = pg.time.get_ticks()
        
        # Count only alive NPCs for spawning limit
        alive_enemy_count = sum(1 for npc in self.npc_list if npc.alive)
        
        # Check if it's time to spawn and we haven't reached max enemies
        if (current_time - self.spawn_timer > self.spawn_delay and 
            alive_enemy_count < self.max_enemies):
            
            spawn_pos = self.find_valid_spawn_position()
            if spawn_pos:
                enemy_class = self.select_enemy_class_for_zone(spawn_pos)
                self.spawn_enemy(enemy_class, spawn_pos)
                self.spawn_timer = current_time
                
                # Adjust difficulty and spawn delay
                self.adjust_spawn_delay_by_difficulty()

    def find_valid_spawn_position(self):
        """Find a valid position to spawn an enemy near but not too close to the player"""
        player_x, player_y = self.game.player.pos
        
        # Try multiple times to find a valid position
        for _ in range(50):
            # Generate random angle and distance
            angle = random.uniform(0, 2 * math.pi)
            distance = random.uniform(self.min_spawn_distance, self.max_spawn_distance)
            
            # Calculate potential spawn position
            spawn_x = player_x + distance * math.cos(angle)
            spawn_y = player_y + distance * math.sin(angle)
            
            # Check if position is valid (not in wall, within map bounds)
            if self.is_valid_spawn_position(spawn_x, spawn_y):
                return (spawn_x, spawn_y)
        
        return None

    def is_valid_spawn_position(self, x, y):
        """Check if a position is valid for spawning (not in wall, within bounds)"""
        # Check map boundaries
        map_width = len(self.game.map.minimap[0])
        map_height = len(self.game.map.minimap)
        
        if x < 1 or x >= map_width - 1 or y < 1 or y >= map_height - 1:
            return False
        
        # Check if position is not in a wall
        if (int(x), int(y)) in self.game.map.worldmap:
            return False
        
        # Check if position is not too close to existing NPCs
        for npc in self.npc_list:
            if npc.alive:
                dist = math.sqrt((x - npc.x) ** 2 + (y - npc.y) ** 2)
                if dist < 3:  # minimum distance between NPCs
                    return False
        
        return True

    def select_enemy_class(self):
        """Select an enemy class based on weighted probabilities"""
        # Create weighted list
        weighted_choices = []
        for enemy_class, weight in self.enemy_classes.items():
            weighted_choices.extend([enemy_class] * weight)
        
        return random.choice(weighted_choices)

    def spawn_enemy(self, enemy_class, position):
        """Spawn a specific enemy class at the given position"""
        # Create NPC instance directly using the class
        npc = enemy_class(self.game, pos=position)
        
        # Add some variety to stats (optional)
        npc.health += random.randint(-20, 20)
        if hasattr(npc, 'speed'):
            npc.speed += random.uniform(-0.005, 0.005)
        
        self.add_npc(npc)
        print(f"Spawned {enemy_class.__name__} at position {position}")

    def add_npc(self, npc):
        self.npc_list.append(npc)

    def add_sprite(self, sprite):
        self.sprite_list.append(sprite)

    def get_map_zone(self, x, y):
        """Determine which themed zone of the map the position is in"""
        map_width = len(self.game.map.minimap[0])
        map_height = len(self.game.map.minimap)
        
        # Define zones based on map layout
        if y < map_height * 0.5:  # Top half
            if x < map_width * 0.4:
                return 'brick_zone'  # Top-left
            elif x < map_width * 0.8:
                return 'blood_zone'  # Top-middle
            else:
                return 'blood2_zone'  # Top-right
        else:  # Bottom half
            if x < map_width * 0.5:
                return 'clean_zone'  # Bottom-left
            else:
                return 'symbol_zone'  # Bottom-right

    def get_zone_enemy_preference(self, zone):
        """Get enemy class preferences for different zones"""
        zone_preferences = {
            'brick_zone': {SoldierNPC: 60, CacoDemonNPC: 30, CyberDemonNPC: 10},
            'blood_zone': {CacoDemonNPC: 50, SoldierNPC: 35, CyberDemonNPC: 15},
            'blood2_zone': {CacoDemonNPC: 45, CyberDemonNPC: 35, SoldierNPC: 20},
            'clean_zone': {SoldierNPC: 70, CacoDemonNPC: 20, CyberDemonNPC: 10},
            'symbol_zone': {CyberDemonNPC: 50, CacoDemonNPC: 30, SoldierNPC: 20}
        }
        return zone_preferences.get(zone, self.enemy_classes)

    def select_enemy_class_for_zone(self, spawn_pos):
        """Select enemy class based on spawn zone"""
        zone = self.get_map_zone(spawn_pos[0], spawn_pos[1])
        zone_preferences = self.get_zone_enemy_preference(zone)
        
        # Create weighted list based on zone preferences
        weighted_choices = []
        for enemy_class, weight in zone_preferences.items():
            weighted_choices.extend([enemy_class] * weight)
        
        return random.choice(weighted_choices)

    def adjust_spawn_delay_by_difficulty(self):
        """Adjust spawn delay based on game progression (more enemies = higher difficulty)"""
        alive_enemy_count = sum(1 for npc in self.npc_list if npc.alive)
        
        # Reduce spawn delay as more enemies are killed (increase difficulty)
        base_delay = 5000
        if alive_enemy_count < 3:
            self.spawn_delay = random.randint(2000, 4000)  # Faster spawning when few enemies
        elif alive_enemy_count < 6:
            self.spawn_delay = random.randint(3000, 6000)
        else:
            self.spawn_delay = random.randint(5000, 8000)  # Slower when many enemies

    def force_spawn(self):
        """Manually trigger enemy spawn (useful for testing)"""
        spawn_pos = self.find_valid_spawn_position()
        if spawn_pos:
            enemy_class = self.select_enemy_class_for_zone(spawn_pos)
            self.spawn_enemy(enemy_class, spawn_pos)
            return True
        return False

    def get_spawn_info(self):
        """Get information about current spawning state"""
        current_time = pg.time.get_ticks()
        time_until_spawn = max(0, self.spawn_delay - (current_time - self.spawn_timer))
        alive_enemy_count = sum(1 for npc in self.npc_list if npc.alive)
        
        return {
            'current_enemies': alive_enemy_count,
            'max_enemies': self.max_enemies,
            'time_until_spawn': time_until_spawn / 1000.0,  # Convert to seconds
            'spawn_delay': self.spawn_delay / 1000.0
        }