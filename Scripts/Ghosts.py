import SimpleGUICS2Pygame.simpleguics2pygame as simplegui
from sprite_animations import Spritesheet
from utils import Vector
import math

class Ghost:
    def __init__(self, pos, vel, spriteimgs, rows, columns, width, height):
        self.width = width
        self.height = height
        self.pos = pos
        self.vel = Vector(0, -1)  # Start with -1 velocity
        self.step = 0
        self.current_direction = "up"  # No initial direction
        self.spriteimgs = Spritesheet(spriteimgs, rows, columns)
        self.speed = 1  # Keep the 2x speed from previous update
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
         
    def update(self):
        # Process input at controlled rate
        self.process_input()
        
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
        
        # Constrain ghost within screen boundaries (assuming self.width and self.height are screen dimensions)
        # Horizontal boundaries
        if self.pos.x > self.width - self.radius:
            self.pos.x = self.width - self.radius
            self.current_direction = "left"  # Reverse direction
        elif self.pos.x < self.radius:
            self.pos.x = self.radius
            self.current_direction = "right"
        
        # Vertical boundaries
        if self.pos.y > self.height - self.radius:
            self.pos.y = self.height - self.radius
            self.current_direction = "up"  # Reverse direction
        elif self.pos.y < self.radius:
            self.pos.y = self.radius
            self.current_direction = "down"

    def next_frame(self):
        self.spriteimgs.next_frame()
    
    def stop(self):
        self.vel = Vector(0, 0)

    def offset_l(self):
        return self.pos.x - self.radius  # Use radius for offset
    
    def offset_r(self):
        return self.pos.x + self.radius  # Use radius for offset
    
    def reset_position(self):
        self.pos = Vector(self.width/2, self.height/2)