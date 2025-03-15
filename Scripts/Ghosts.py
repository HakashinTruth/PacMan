import SimpleGUICS2Pygame.simpleguics2pygame as simplegui
from sprite_animations import Spritesheet
from utils import Vector
import math

class Ghost:
    def __init__(self, pos, vel, spriteimgs, rows, columns, width, height):
        print("Ghost initialized!")
        self.width = width
        self.height = height
        self.pos = pos
        self.vel = Vector(0, 0)  # Start with zero velocity
        self.step = 0
        self.current_direction = None  # No initial direction
        self.spriteimgs = Spritesheet(spriteimgs, rows, columns)
        self.speed = 2  # Keep the 2x speed from previous update
        self.radius = 16  # Increased from 16 to 20

        # Input rate control variables
        self.input_frame_counter = 0
        self.main_fps = 60  # Assuming main game runs at 60fps
        self.input_fps = 30   # Target input processing rate
        self.input_interval = self.main_fps // self.input_fps

    def draw(self, canvas):
        # Convert Vector to tuple
        pos_tuple = (self.pos.x, self.pos.y)
        # Pass rotation to the draw method
        self.spriteimgs.draw(canvas, pos_tuple, scale=1.25)
    
    def process_input(self, pacman):
        # Increment frame counter
        self.input_frame_counter += 1
        
        # Only process input at the desired rate (every 4 frames for 15fps if main game is 60fps)
        if self.input_frame_counter >= self.input_interval:
            # Reset counter
            self.input_frame_counter = 0

            if pacman.vel == Vector(0,0):

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

    def next_frame(self):
        self.spriteimgs.next_frame()
    
    def stop(self):
        self.vel = Vector(0, 0)

    def offset_l(self):
        return self.pos.x - self.radius  # Use radius for offset
    
    def offset_r(self):
        return self.pos.x + self.radius  # Use radius for offset
            
