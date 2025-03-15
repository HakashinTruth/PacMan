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
    
    def process_input(self):
        # Increment frame counter
        self.input_frame_counter += 1
        
        # Only process input at the desired rate (every 4 frames for 15fps if main game is 60fps)
        if self.input_frame_counter >= self.input_interval:
            # Reset counter
            self.input_frame_counter = 0

            if self.vel == Vector(0,0):
              print(self.vel, " ", self.pos)

              self.current_direction = self.directions[random.randint(0,3)]
    




