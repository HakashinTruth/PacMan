import SimpleGUICS2Pygame.simpleguics2pygame as simplegui
from utils import Vector
import math

class Wall:
    def __init__(self, x1, y1, x2, y2, border, color, rightleft):
        if rightleft not in ('r', 'l', 't', 'b'):
            raise ValueError("Use 'r', 'l', 't', or 'b' for wall orientation")
        
        self.x1 = x1
        self.y1 = y1
        self.x2 = x2
        self.y2 = y2
        self.border = border
        self.color = color
        self.rightleft = rightleft
        
        # Determine normal vector based on wall orientation
        if self.rightleft == 'r':
            self.normal = Vector(1, 0)
        elif self.rightleft == 'l':
            self.normal = Vector(-1, 0)
        elif self.rightleft == 't':
            self.normal = Vector(0, 1)
        else:  # bottom wall
            self.normal = Vector(0, -1)

    def draw(self, canvas):
        canvas.draw_line((self.x1, self.y1), (self.x2, self.y2), self.border * 2 + 1, self.color)
    
    def hit(self, pacman):
        # Use Pac-Man's radius for collision detection
        pac_radius = pacman.radius
        
        # Check horizontal walls (left/right)
        if self.rightleft in ['l', 'r']:
            # Check vertical overlap
            vertical_overlap = (min(self.y1, self.y2) <= pacman.pos.y <= max(self.y1, self.y2))
            
            # Check horizontal collision
            if vertical_overlap:
                if self.rightleft == 'l':
                    # Check if Pac-Man's left edge is at or beyond the wall
                    return pacman.offset_l() <= self.x1
                else:  # right wall
                    # Check if Pac-Man's right edge is at or beyond the wall
                    return pacman.offset_r() >= self.x1
        
        # Check vertical walls (top/bottom)
        elif self.rightleft in ['t', 'b']:
            # Check horizontal overlap
            horizontal_overlap = (min(self.x1, self.x2) <= pacman.pos.x <= max(self.x1, self.x2))
            
            # Check vertical collision
            if horizontal_overlap:
                if self.rightleft == 't':
                    # Check if Pac-Man's top edge is at or above the wall
                    return pacman.pos.y - pac_radius <= self.y1
                else:  # bottom wall
                    # Check if Pac-Man's bottom edge is at or below the wall
                    return pacman.pos.y + pac_radius >= self.y1
        
        return False