import SimpleGUICS2Pygame.simpleguics2pygame as simplegui
from sprite_animations import Spritesheet
from utils import Vector
from Ghosts import Ghost
import math

class GreenGhost(Ghost):
    def __init__(self, pos, vel, spriteimgs, rows, columns, width, height):
        super().__init__(pos, vel, spriteimgs, rows, columns, width, height)
  
    
    def process_input(self, pacman):
        # Increment frame counter
        self.input_frame_counter += 1
        
        # Only process input at the desired rate (every 4 frames for 15fps if main game is 60fps)
        if self.input_frame_counter >= self.input_interval:
            # Reset counter
            self.input_frame_counter = 0

            #if pacman.vel == Vector(0,0):
            #print(pacman.vel, " ", pacman.pos)

            x_difference = abs(pacman.pos.x - self.pos.x)
            y_difference = abs(pacman.pos.y - self.pos.y)

            if (pacman.pos.x <= self.pos.x) and (pacman.pos.y <= self.pos.y):

                if x_difference >= y_difference:
                    self.current_direction = "left"
                else:
                    self.current_direction = "up"

            if (pacman.pos.x >= self.pos.x) and (pacman.pos.y <= self.pos.y):

                if x_difference >= y_difference:
                    self.current_direction = "right"
                else:
                    self.current_direction = "up"

            if (pacman.pos.x <= self.pos.x) and (pacman.pos.y >= self.pos.y):

                if x_difference >= y_difference:
                    self.current_direction = "left"
                else:
                    self.current_direction = "down"
            
            if (pacman.pos.x >= self.pos.x) and (pacman.pos.y >= self.pos.y):

                if x_difference >= y_difference:
                    self.current_direction = "right"
                else:
                    self.current_direction = "down"

    def update(self, pacman):
        # Process input at controlled rate
        self.process_input(pacman)
        
        # Apply velocity based on current direction
        self.vel = Vector(0, 0)  # Reset velocity
    
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
    
        # Simplified wrap-around logic
        # Horizontal wrap
        if self.pos.x > self.width:  # Right edge
            self.pos.x = 0
        elif self.pos.x < 0:  # Left edge
            self.pos.x = self.width
    
        # Vertical wrap
        if self.pos.y > self.height:  # Bottom edge
            self.pos.y = 0
        elif self.pos.y < 0:  # Top edge
            self.pos.y = self.height

                
                    
 