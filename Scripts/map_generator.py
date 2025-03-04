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

        # Generate walls for blue blocks (1)
        for row in range(rows):
            for col in range(cols):
                if self.map[row][col] == 1:
                    # Calculate wall positions with slight reduction to create gaps
                    x1 = col * cell_width + 1  # Small offset
                    y1 = row * cell_height + 1  # Small offset
                    x2 = x1 + cell_width - 2  # Slight reduction
                    y2 = y1 + cell_height - 2  # Slight reduction

                    # Create walls for each side of the block
                    # Left wall
                    self.walls.append(Wall(x1, y1, x1, y2))
                    # Right wall
                    self.walls.append(Wall(x2, y1, x2, y2))
                    # Top wall
                    self.walls.append(Wall(x1, y1, x2, y1))
                    # Bottom wall
                    self.walls.append(Wall(x1, y2, x2, y2))

    def draw_walls(self, canvas):
        for wall in self.walls:
            wall.draw(canvas)

    def get_walls(self):
        return self.walls