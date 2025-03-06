import SimpleGUICS2Pygame.simpleguics2pygame as simplegui
from walls import Wall
import math

class MapGenerator:
    def __init__(self, map_array, canvas_width, canvas_height):
        self.map = map_array
        self.canvas_width = canvas_width
        self.canvas_height = canvas_height
        self.walls = []
        self.generate_walls()

    def generate_walls(self):
        # Calculate cell dimensions based on map size and canvas dimensions
        rows = len(self.map)
        cols = len(self.map[0])
        
        cell_width = self.canvas_width / cols
        cell_height = self.canvas_height / rows
        
        # Generate horizontal walls
        for row in range(rows):
            wall_start = None
            for col in range(cols):
                is_wall = self.map[row][col] == 1
                # If we find a wall and haven't started a segment yet
                if is_wall and wall_start is None:
                    wall_start = col
                # If we had a wall segment and hit a non-wall or the end
                elif (not is_wall or col == cols - 1) and wall_start is not None:
                    # If we're at the end and it's a wall, extend to include this cell
                    end_col = col if not is_wall else col + 1
                    # Create the wall
                    x1 = wall_start * cell_width
                    y1 = row * cell_height
                    x2 = end_col * cell_width
                    
                    # Create top and bottom walls of the segment
                    self.walls.append(Wall(x1, y1, x2, y1))  # Top wall
                    self.walls.append(Wall(x1, y1 + cell_height, x2, y1 + cell_height))  # Bottom wall
                    
                    wall_start = None
        
        # Generate vertical walls
        for col in range(cols):
            wall_start = None
            for row in range(rows):
                is_wall = self.map[row][col] == 1
                # If we find a wall and haven't started a segment yet
                if is_wall and wall_start is None:
                    wall_start = row
                # If we had a wall segment and hit a non-wall or the end
                elif (not is_wall or row == rows - 1) and wall_start is not None:
                    # If we're at the end and it's a wall, extend to include this cell
                    end_row = row if not is_wall else row + 1
                    # Create the wall
                    x1 = col * cell_width
                    y1 = wall_start * cell_height
                    y2 = end_row * cell_height
                    
                    # Create left and right walls of the segment
                    self.walls.append(Wall(x1, y1, x1, y2))  # Left wall
                    self.walls.append(Wall(x1 + cell_width, y1, x1 + cell_width, y2))  # Right wall
                    
                    wall_start = None

    def draw_walls(self, canvas):
        for wall in self.walls:
            wall.draw(canvas)

    def get_walls(self):
        return self.walls