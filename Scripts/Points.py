import SimpleGUICS2Pygame.simpleguics2pygame as simplegui
from sprite_animations import Spritesheet
from utils import Vector
 
class Point:
    def __init__(self, pos, rows, columns, width, height):
        print("Ghost initialized!")
        self.width = width
        self.height = height
        self.pos = pos
        self.vel = Vector(0, 0)
        self.spriteimgs = Spritesheet(r"C:\Users\Student\OneDrive\Desktop\project\PacMan\pacmanPack\CoinTransparent.png", rows, columns)
        self.radius = 3 
        # Input rate control variables
        self.input_frame_counter = 0
        self.main_fps = 60  # Assuming main game runs at 60fps
        self.input_fps = 30   # Target input processing rate
        self.input_interval = self.main_fps // self.input_fps
        
    def draw(self, canvas):
        # Convert Vector to tuple
        
        # Pass rotation to the draw method
        self.spriteimgs.draw(canvas, self.pos, scale=1.25)
        
    def next_frame(self):
        self.spriteimgs.next_frame()
    
    def pointCollision(self):
        
         