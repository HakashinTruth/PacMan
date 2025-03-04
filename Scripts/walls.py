import SimpleGUICS2Pygame.simpleguics2pygame as simplegui
from utils import Vector
import math

class Wall:
    def __init__(self, x1, y1, x2, y2, border=5, color='blue'):
        self.x1 = x1
        self.y1 = y1
        self.x2 = x2
        self.y2 = y2
        self.border = border
        self.color = color

    def draw(self, canvas):
        canvas.draw_line((self.x1, self.y1), (self.x2, self.y2), self.border * 2 + 1, self.color)
    
    def hit(self, pacman):
        # Use Pac-Man's radius for collision detection
        pac_radius = pacman.radius
        
        # Check if wall is horizontal or vertical
        is_horizontal = abs(self.y1 - self.y2) < abs(self.x1 - self.x2)
        
        if is_horizontal:
            # Horizontal wall
            # Check if Pac-Man is within the wall's horizontal range
            x_inside = (min(self.x1, self.x2) <= pacman.pos.x <= max(self.x1, self.x2))
            
            # Check vertical collision
            y_collision = (
                abs(pacman.pos.y - self.y1) <= pac_radius
            )
            
            return x_inside and y_collision
        
        else:
            # Vertical wall
            # Check if Pac-Man is within the wall's vertical range
            y_inside = (min(self.y1, self.y2) <= pacman.pos.y <= max(self.y1, self.y2))
            
            # Check horizontal collision
            x_collision = (
                abs(pacman.pos.x - self.x1) <= pac_radius
            )
            
            return y_inside and x_collision