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
        #canvas.draw_line((self.x1, self.y1), (self.x2, self.y2), self.border * 2 + 1, "white")
        canvas.draw_polygon([(self.x1,self.y1),(self.x2,self.y1),(self.x2,self.y2),(self.x1,self.y2)],self.border,self.color,self.color)
        
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
    def hit(self, entity, ghost=False):
        if not ghost:
            # Preliminary bounding box check for performance (optimized for Pac-Man)
            min_x = min(self.x1, self.x2)
            max_x = max(self.x1, self.x2)
            min_y = min(self.y1, self.y2)
            max_y = max(self.y1, self.y2)
            if (entity.pos.x < min_x - 50 or entity.pos.x > max_x + 50 or
                entity.pos.y < min_y - 50 or entity.pos.y > max_y + 50):
                return False

            # Use Pac-Man's directional collision logic
            pac_direction = entity.current_direction
            pac_radius = entity.radius
            if pac_direction == "right":
                x_collision = (self.x1 - pac_radius <= entity.pos.x <= self.x1)
                y_inside = (min(self.y1, self.y2) - pac_radius/2 <= entity.pos.y <= max(self.y1, self.y2) + pac_radius/2)
                if x_collision and y_inside:
                    entity.stop()
                    return True
            elif pac_direction == "left":
                x_collision = (abs(entity.pos.x - self.x2) <= pac_radius)
                y_inside = (min(self.y1, self.y2) - pac_radius/2 <= entity.pos.y <= max(self.y1, self.y2) + pac_radius/2)
                if x_collision and y_inside:
                    entity.stop()
                    return True
            elif pac_direction == "up":
                x_inside = (min(self.x1, self.x2) - pac_radius/2 <= entity.pos.x <= max(self.x1, self.x2) + pac_radius/2)
                y_collision = (abs(entity.pos.y - self.y2) <= pac_radius)
                if x_inside and y_collision:
                    entity.stop()
                    return True
            elif pac_direction == "down":
                x_inside = (min(self.x1, self.x2) - pac_radius/2 <= entity.pos.x <= max(self.x1, self.x2) + pac_radius/2)
                y_collision = (abs(entity.pos.y - self.y1) <= pac_radius)
                if x_inside and y_collision:
                    entity.stop()
                    return True
            return False
        else:
            # For ghosts, use a simple collision detection that doesn't rely on direction.
            # Assume walls are either horizontal or vertical.
            if abs(self.y1 - self.y2) < abs(self.x1 - self.x2):  # horizontal wall
                if min(self.x1, self.x2) <= entity.pos.x <= max(self.x1, self.x2) and abs(entity.pos.y - self.y1) <= entity.radius:
                    entity.stop()
                    return True
            else:  # vertical wall
                if min(self.y1, self.y2) <= entity.pos.y <= max(self.y1, self.y2) and abs(entity.pos.x - self.x1) <= entity.radius:
                    entity.stop()
                    return True
            return False
