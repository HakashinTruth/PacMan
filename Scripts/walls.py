import SimpleGUICS2Pygame.simpleguics2pygame as simplegui
from utils import Vector
import math

class Wall:
    def __init__(self, x1, y1, x2, y2,cell_height,cell_width, border, color):
        self.x1 = x1
        self.y1 = y1
        self.x2 = x2
        self.y2 = y2
        self.border = border
        self.color = color
        self.cellHeight=cell_height
        self.cellWidth=cell_width

    def draw(self, canvas):
        canvas.draw_polygon([(self.x1,self.y1),(self.x2,self.y1),(self.x2,self.y2),(self.x1,self.y2)],self.border,self.color,self.color)
        #canvas.draw_line((self.x1, self.y1), (self.x2, self.y2), self.border * 2 + 1, self.color)
    '''
    def hit(self, pacman):
        # Use Pac-Man's radius for collision detection
        pac_radius = pacman.radius
        
        # Check if wall is horizontal or vertical
        is_horizontal = abs(self.y1 - self.y2) < abs(self.x1 - self.x2)
        is_vertical = not is_horizontal
        if is_horizontal:
            # Horizontal wall
            # Check if Pac-Man is within the wall's horizontal range
            x_inside = (min(self.x1, self.x2) <= pacman.pos.x <= max(self.x1, self.x2))
            
            # Check vertical collision
            y_collision = (
                abs(pacman.pos.y - self.y1) <= pac_radius
            )
            pacman.stop()
            return x_inside and y_collision
        
        if is_vertical:
            # Vertical wall
            # Check if Pac-Man is within the wall's vertical range
            y_inside = (min(self.y1, self.y2) <= pacman.pos.y <= max(self.y1, self.y2))
            
            # Check horizontal collision
            x_collision = (
                abs(pacman.pos.x - self.x1) <= pac_radius
            )
            pacman.stop()
            return y_inside and x_collision
    '''
    def hit(self, pacman):
        # Use Pac-Man's radius for collision detection
        # Check if wall is in the way of pacman's direction
        # Check if pacman within the wall's range
        '''
        if (self.y1 == self.y2) and pacman.current_direction == "right":
            depth = abs(pacman.pos.x - self.x1)
            pacman.stop()
            return (pacman.pos.x + pacman.radius) > (self.x1 - self.border) and (depth >= 0 and depth <= pacman.radius)
        if (self.y1 == self.y2) and pacman.current_direction == "left":
            depth = abs(self.x1 - pacman.pos.x)
            pacman.stop()
            return (pacman.pos.x - pacman.radius) < (self.x1 + self.border) and (depth >= 0 and depth <= pacman.radius)
        if (self.x1 == self.x2) and pacman.current_direction == "down":
            depth = abs(pacman.pos.y - self.y1)
            pacman.stop()
            return (pacman.pos.y + pacman.radius) > (self.y1 - self.border) and (depth >= 0 and depth <= pacman.radius)
        if (self.x1 == self.x2) and pacman.current_direction == "up":
            depth = abs(self.y1 - pacman.pos.y)
            pacman.stop()
            return (pacman.pos.y - pacman.radius) < (self.y1 + self.border) and (depth >= 0 and depth <= pacman.radius)
        
        '''
        # Use Pac-Man's radius for collision detection
        # Check if wall is in the way of pacman's direction
        # Check if pacman within the wall's range
        pac_direction = pacman.current_direction
        pac_radius = pacman.radius
        if pac_direction == "right":
            x_collision = (self.x1 - pacman.radius <= pacman.pos.x <= self.x1)

            y_inside = (min(self.y1, self.y2) - pacman.radius/2 <= pacman.pos.y <= max(self.y1, self.y2) + pacman.radius/2)
            pacman.stop()
            return y_inside > 0 and x_collision > 0
        elif pac_direction == "left":
            x_collision = (abs(pacman.pos.x - self.x2) <= pac_radius)
            y_inside = (min(self.y1, self.y2) - pacman.radius/2 <= pacman.pos.y <= max(self.y1, self.y2) + pacman.radius/2)
            pacman.stop()
            return y_inside > 0 and x_collision > 0
        elif pac_direction == "up":
            x_inside = (min(self.x1, self.x2) - pacman.radius/2 <= pacman.pos.x <= max(self.x1, self.x2) + pacman.radius/2)
            y_collision = (abs(pacman.pos.y - self.y2) <= pac_radius)
            pacman.stop()
            return y_collision > 0 and x_inside > 0
        elif pac_direction == "down":
            x_inside = (min(self.x1, self.x2) - pacman.radius/2 <= pacman.pos.x <= max(self.x1, self.x2) + pacman.radius/2)
            y_collision = (abs(pacman.pos.y - self.y1) <= pac_radius)
            pacman.stop()
            return y_collision > 0 and x_inside > 0
        elif pacman.radius > self.y1 + self.border and pacman.radius < self.y2 + self.border and pacman.radius  > self.x1 + self.border and pacman.radius  < self.x2 + self.border:
            pacman.stop()
            return True
        
        
    
    