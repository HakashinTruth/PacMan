import SimpleGUICS2Pygame.simpleguics2pygame as simplegui
from sprite_animations import Spritesheet
from utils import Vector

class PacMan:
    def __init__(self, pos, vel, keys, spriteimgs, rows, columns):
        print("PacMan initialized!")
        self.pos = pos
        self.vel = vel
        self.keys = keys
        self.step = 0
        self.rotation = 0  # Initialize rotation (0 = facing right)
        self.spriteimgs = Spritesheet(spriteimgs, rows, columns)

    def draw(self, canvas):
        # Convert Vector to tuple
        pos_tuple = (self.pos.x, self.pos.y)
        # Pass rotation to the draw method
        self.spriteimgs.draw(canvas, pos_tuple, self.rotation)

    def update(self):
        # Reset velocity to prevent continuous acceleration
        self.vel = Vector(0, 0)
    
        # Apply velocity based on keyboard input (use a fixed speed value)
        speed = 3  # Adjust this value to control Pac-Man's movement speed
    
        # Set rotation based on direction
        if self.keys.right:
            self.vel = Vector(speed, 0)
            self.rotation = 0  # Right = 0 degrees (default orientation)
        elif self.keys.left:
            self.vel = Vector(-speed, 0)
            self.rotation = 180  # Left = 180 degrees
        elif self.keys.up:
            self.vel = Vector(0, -speed)
            self.rotation = 270  # Up = 270 degrees
        elif self.keys.down:
            self.vel = Vector(0, speed)
            self.rotation = 90  # Down = 90 degrees
    
        # Update position
        self.pos.add(self.vel)
    
        # Add boundary checks
        if self.pos.x < 0:
            self.pos.x = 0
        elif self.pos.x > 800:  # Use your CANVAS_WIDTH
            self.pos.x = 800
        if self.pos.y < 0:
            self.pos.y = 0
        elif self.pos.y > 600:  # Use your CANVAS_HEIGHT
            self.pos.y = 600

    def next_frame(self):
        self.spriteimgs.next_frame()