import SimpleGUICS2Pygame.simpleguics2pygame as simplegui
from walls import Wall
from Points import Point
from utils import Vector
import math

class MapGenerator:
    def __init__(self, map_array, canvas_width, canvas_height):
        self.map = map_array
        self.canvas_width = canvas_width
        self.canvas_height = canvas_height
        self.walls = []
        self.square=[]
        self.points=[]
        self.generate_walls()

    def generate_walls(self):
        wallcolor="Blue"
        innerWallcolor="Black"
        border=1
        innerBorder=3
        print("Drawing map")
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
                    self.walls.append(Wall(x1, y1, x2, y1,cell_height,cell_width,border,wallcolor))  # Top wall
                    self.walls.append(Wall(x1, y1 + cell_height, x2, y1 + cell_height,cell_height,cell_width,border,wallcolor))  # Bottom wall
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
                    self.walls.append(Wall(x1, y1, x1, y2,cell_height,cell_width,border,wallcolor))  # Left wall
                    self.walls.append(Wall(x1 + cell_width, y1, x1 + cell_width, y2,cell_height,cell_width,border,wallcolor))  # Right wall
                    wall_start = None
        
        #display map ui ontop of existing lines to give illusion of a thick wall      
        for row in range(rows):
            for col in range(cols):
                xpos = col * cell_width - innerBorder
                ypos = row * cell_height - innerBorder
                if self.map[row][col] == 1:
                    self.square.append(Wall(xpos+innerBorder, ypos+innerBorder, xpos+innerBorder + cell_width, ypos+innerBorder + cell_height, cell_height, cell_width,innerBorder,wallcolor))
                    self.square.append(Wall(xpos+(2*innerBorder), ypos+(2*innerBorder), xpos + cell_width, ypos + cell_height, cell_height, cell_width,innerBorder,innerWallcolor))
                    if col >0 and self.map[row][col-1]==1:
                        self.square.append(Wall(xpos-(2*innerBorder), ypos+(2*innerBorder), (xpos) + cell_width, ypos + cell_height, cell_height, cell_width,innerBorder,innerWallcolor))
                    if row >0 and self.map[row-1][col]==1:
                        self.square.append(Wall(xpos+(2*innerBorder), ypos-(2*innerBorder), xpos + cell_width, (ypos-(2*innerBorder)) + cell_height, cell_height, cell_width,innerBorder,innerWallcolor))
       
        for row in range(rows):
            for col in range(cols):
                xpos=col*cell_width +cell_width/2
                ypos = row*cell_height +cell_height/2
                if self.map[row][col]==2:
                    self.points.append(Point(Vector(xpos,ypos),1,8,self.canvas_width,self.canvas_height))
                    
                 
                
          
 #not being used
    def draw_walls(self, canvas):
        for wall in self.walls:
            wall.draw(canvas)
        for sq in self.square:
            sq.draw(canvas)
        


    def get_walls(self):
        return self.walls