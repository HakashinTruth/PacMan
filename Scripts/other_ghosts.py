import SimpleGUICS2Pygame.simpleguics2pygame as simplegui
from sprite_animations import Spritesheet
from utils import Vector
from Ghosts import Ghost  
import math
import random

class OtherGhost(Ghost):
    def __init__(self, pos, vel, spriteimgs, rows, columns, width, height):
        super().__init__(pos, vel, spriteimgs, rows, columns, width, height)
        self.directions = ["left", "right", "up", "down"]
        self.random_move_timer = 0
        self.set_new_random_interval()

    def set_new_random_interval(self):
        # Set a random interval between 3 and 5 seconds (in frames)
        self.random_move_timer = random.randint(180, 300)

    def process_input(self, pacman):
        # Increment the frame counter
        self.input_frame_counter += 1
        if self.input_frame_counter >= self.input_interval:
            self.input_frame_counter = 0
            
            # Calculate the Euclidean distance between ghost and Pac-Man
            dx = pacman.pos.x - self.pos.x
            dy = pacman.pos.y - self.pos.y
            distance = math.sqrt(dx * dx + dy * dy)
            
            if distance <= 60:
                # Follow Pac-Man (using logic similar to GreenGhost)
                x_difference = abs(dx)
                y_difference = abs(dy)
                if (pacman.pos.x <= self.pos.x) and (pacman.pos.y <= self.pos.y):
                    self.current_direction = "left" if x_difference >= y_difference else "up"
                elif (pacman.pos.x >= self.pos.x) and (pacman.pos.y <= self.pos.y):
                    self.current_direction = "right" if x_difference >= y_difference else "up"
                elif (pacman.pos.x <= self.pos.x) and (pacman.pos.y >= self.pos.y):
                    self.current_direction = "left" if x_difference >= y_difference else "down"
                elif (pacman.pos.x >= self.pos.x) and (pacman.pos.y >= self.pos.y):
                    self.current_direction = "right" if x_difference >= y_difference else "down"
            else:
                # Pac-Man is not within 100 pixels, so use random movement.
                self.random_move_timer -= self.input_interval
                if self.random_move_timer <= 0:
                    self.current_direction = random.choice(self.directions)
                    self.set_new_random_interval()

    def update(self, pacman):
        # Process input using the updated behavior
        self.process_input(pacman)
        
        # Set velocity based on the current direction
        self.vel = Vector(0, 0)
        if self.current_direction == "right":
            self.vel = Vector(self.speed, 0)
        elif self.current_direction == "left":
            self.vel = Vector(-self.speed, 0)
        elif self.current_direction == "up":
            self.vel = Vector(0, -self.speed)
        elif self.current_direction == "down":
            self.vel = Vector(0, self.speed)
        
        # Update position
        self.pos.add(self.vel)
        
        # Constrain ghost within screen boundaries (using ghost radius)
        if self.pos.x > self.width - self.radius:
            self.pos.x = self.width - self.radius
            self.current_direction = "left"
        elif self.pos.x < self.radius:
            self.pos.x = self.radius
            self.current_direction = "right"
        if self.pos.y > self.height - self.radius:
            self.pos.y = self.height - self.radius
            self.current_direction = "up"
        elif self.pos.y < self.radius:
            self.pos.y = self.radius
            self.current_direction = "down"
