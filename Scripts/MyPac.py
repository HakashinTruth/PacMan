import SimpleGUICS2Pygame.simpleguics2pygame as simplegui
from sprite_animations import Spritesheet
from utils import Vector
import math

class PacMan:
    def __init__(self, pos, vel, keys, spriteimgs, rows, columns):
        print("PacMan initialized!")
        self.pos = pos
        self.vel = Vector(0, 0)  # Start with zero velocity
        self.keys = keys
        self.step = 0
        self.rotation = 0  # Initialize rotation (0 = facing right)
        self.current_direction = None  # No initial direction
        self.spriteimgs = Spritesheet(spriteimgs, rows, columns)
        self.speed = 1.5  # Keep the 2x speed from previous update
        self.radius = 16  # Increased from 16 to 20

    def draw(self, canvas):
        # Convert Vector to tuple
        pos_tuple = (self.pos.x, self.pos.y)
        # Pass rotation to the draw method
        self.spriteimgs.draw(canvas, pos_tuple, self.rotation, scale=1.25)  # Slightly larger scale

    def update(self):
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
        if self.pos.x > 448:  # Right edge
            self.pos.x = 0
        elif self.pos.x < 0:  # Left edge
            self.pos.x = 448
    
        # Vertical wrap
        if self.pos.y > 512:  # Bottom edge
            self.pos.y = 0
        elif self.pos.y < 0:  # Top edge
            self.pos.y = 512

    def next_frame(self):
        self.spriteimgs.next_frame()
    
    def stop(self):
        self.vel = Vector(0, 0)

    def offset_l(self):
        return self.pos.x - self.radius  # Use radius for offset
    
    def offset_r(self):
        return self.pos.x + self.radius  # Use radius for offset