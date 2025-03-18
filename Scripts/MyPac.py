import SimpleGUICS2Pygame.simpleguics2pygame as simplegui
from sprite_animations import Spritesheet
from utils import Vector
import math

class PacMan:
    def __init__(self, pos, vel, keys, spriteimgs, rows, columns, width, height):
        print("PacMan initialized!")
        self.width=width
        self.height=height
        self.pos = pos
        self.vel = Vector(0, 0)  # Start with zero velocity
        self.keys = keys
        self.step = 0
        self.rotation = 0  # Initialize rotation (0 = facing right)
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
        self.spriteimgs.draw(canvas, pos_tuple, self.rotation, scale=1.25)  # Slightly larger scale

    def process_input(self):
        # Increment frame counter
        self.input_frame_counter += 1
        
        # Only process input at the desired rate (every 4 frames for 15fps if main game is 60fps)
        if self.input_frame_counter >= self.input_interval:
            # Reset counter
            self.input_frame_counter = 0
            
            # Check for new direction input
            if self.keys.right:
                self.current_direction = "right"
                self.keys.right = False  # Reset key state after reading
            elif self.keys.left:
                self.current_direction = "left"
                self.keys.left = False  # Reset key state after reading
            elif self.keys.up:
                self.current_direction = "up"
                self.keys.up = False  # Reset key state after reading
            elif self.keys.down:
                self.current_direction = "down"
                self.keys.down = False  # Reset key state after reading

    def update(self):
        # Process input at controlled rate
        self.process_input()
        
        # Apply velocity based on current direction
        self.vel = Vector(0, 0)  # Reset velocity
    
        if self.current_direction == "right":
            self.vel = Vector(self.speed, 0)
            self.rotation = 0
        elif self.current_direction == "left":
            self.vel = Vector(-self.speed, 0)
            self.rotation = math.pi
        elif self.current_direction == "up":
            self.vel = Vector(0, -self.speed)
            self.rotation = -math.pi / 2
        elif self.current_direction == "down":
            self.vel = Vector(0, self.speed)
            self.rotation = math.pi / 2
    
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

    def collidedWithPoint(self, entity):
        xPac = self.pos.x
        xEntity = entity.pos.x

        yPac = self.pos.y
        yEntity = entity.pos.y
        return xPac < (xEntity + entity.radius*2) and (xPac + self.radius) > xEntity and yPac < (yEntity + entity.radius*2) and (yPac + self.radius) > yEntity

    def next_frame(self):
        self.spriteimgs.next_frame()
    
    def stop(self):
        self.vel = Vector(0, 0)

    def offset_l(self):
        return self.pos.x - self.radius  # Use radius for offset
    
    def offset_r(self):
        return self.pos.x + self.radius  # Use radius for offset
    
    def reset_position(self):
        self.pos = Vector(self.width/2, self.height/5)