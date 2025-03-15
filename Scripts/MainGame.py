import SimpleGUICS2Pygame.simpleguics2pygame as simplegui
import math
from MyPac import PacMan
from utils import Vector
from walls import Wall
from map_generator import MapGenerator
from Ghosts import Ghost
from green_ghost import GreenGhost
from other_ghosts import OtherGhost

class Keyboard:
    def __init__(self):
        self.right = False
        self.left = False
        self.up = False
        self.down = False
        self.step = 0
    
    def keyDown(self, key):
        # Set only the pressed key to True, leave others as they are
        if key == simplegui.KEY_MAP["right"]:
            self.right = True
        elif key == simplegui.KEY_MAP["left"]:
            self.left = True
        elif key == simplegui.KEY_MAP["up"]:
            self.up = True
        elif key == simplegui.KEY_MAP["down"]:
            self.down = True

class Interaction:
    def __init__(self, pacman, ghosts, keyboard, walls, squares):
        self.pacman = pacman
        self.ghosts = ghosts
        self.keyboard = keyboard
        self.walls = walls
        self.last_collision = None  # Track the last wall collided with

    def update(self):
        # Reset last collision
        self.last_collision = None
        
        # Check for wall collisions
        for wall in self.walls:
            if wall.hit(self.pacman):
                # Stop Pac-Man when hitting a wall
                self.pacman.stop()
                self.last_collision = wall
                
                
                # Broad collision handling
                if wall.x1 == wall.x2:  # Vertical wall
                    if self.pacman.pos.x < wall.x1:
                        self.pacman.pos.x = wall.x1 - self.pacman.radius
                    else:
                        self.pacman.pos.x = wall.x1 + self.pacman.radius
                else:  # Horizontal wall
                    if self.pacman.pos.y < wall.y1:
                        self.pacman.pos.y = wall.y1 - self.pacman.radius
                    else:
                        self.pacman.pos.y = wall.y1 + self.pacman.radius
                
                break  # Stop checking after first collision
        
        for wall in self.walls:
            for ghost in self.ghosts:
                if wall.hit(ghost):
                    # Stop Pac-Man when hitting a wall
                    ghost.stop()
                    self.last_collision = wall
                    
                    
                    # Broad collision handling
                    if wall.x1 == wall.x2:  # Vertical wall
                        if ghost.pos.x < wall.x1:
                            ghost.pos.x = wall.x1 - ghost.radius
                        else:
                            ghost.pos.x = wall.x1 + ghost.radius
                    else:  # Horizontal wall
                        if ghost.pos.y < wall.y1:
                            ghost.pos.y = wall.y1 - ghost.radius
                        else:
                            ghost.pos.y = wall.y1 + ghost.radius
                    break

                
class Clock:
    def __init__(self, time=0):
        self.time = time

    def tick(self):
        self.time += 1

    def transition(self, frame_duration):
        if self.time >= frame_duration:
            self.time = 0
            return True
        return False

# Constants
#this also fixes jitter problem
CANVAS_WIDTH = 640  # 2x original 224
CANVAS_HEIGHT = 695  # 2x original 256
FRAME_DURATION = 10  # Higher = slower animation
arr=[ 
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    [1, 2, 2, 2, 2, 2, 2, 2, 2, 2, 1, 2, 2, 2, 2, 2, 2, 2, 2, 2, 1],
    [1, 2, 1, 1, 1, 2, 1, 1, 1, 2, 1, 2, 1, 1, 1, 2, 1, 1, 1, 2, 1],
    [1, 2, 1, 1, 1, 2, 1, 1, 1, 2, 1, 2, 1, 1, 1, 2, 1, 1, 1, 2, 1],
    [1, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 1],
    [1, 2, 1, 1, 1, 2, 1, 2, 1, 1, 1, 1, 1, 2, 1, 2, 1, 1, 1, 2, 1],
    [1, 2, 2, 2, 2, 2, 1, 2, 2, 2, 1, 2, 2, 2, 1, 2, 2, 2, 2, 2, 1],
    [1, 1, 1, 1, 1, 2, 1, 1, 1, 2, 1, 2, 1, 1, 1, 2, 1, 1, 1, 1, 1],
    [0, 0, 0, 0, 1, 2, 1, 2, 2, 2, 2, 2, 2, 2, 1, 2, 1, 0, 0, 0, 0],
    [1, 1, 1, 1, 1, 2, 1, 2, 1, 1, 2, 1, 1, 2, 1, 2, 1, 1, 1, 1, 1],
    [2, 2, 2, 2, 2, 2, 2, 2, 1, 2, 2, 2, 1, 2, 2, 2, 2, 2, 2, 2, 2],
    [1, 1, 1, 1, 1, 2, 1, 2, 1, 2, 2, 2, 1, 2, 1, 2, 1, 1, 1, 1, 1],
    [0, 0, 0, 0, 1, 2, 1, 2, 1, 1, 1, 1, 1, 2, 1, 2, 1, 0, 0, 0, 0],
    [0, 0, 0, 0, 1, 2, 1, 2, 2, 2, 2, 2, 2, 2, 1, 2, 1, 0, 0, 0, 0],
    [1, 1, 1, 1, 1, 2, 2, 2, 1, 1, 1, 1, 1, 2, 2, 2, 1, 1, 1, 1, 1],
    [1, 2, 2, 2, 2, 2, 2, 2, 2, 2, 1, 2, 2, 2, 2, 2, 2, 2, 2, 2, 1],
    [1, 2, 1, 1, 1, 2, 1, 1, 1, 2, 1, 2, 1, 1, 1, 2, 1, 1, 1, 2, 1],
    [1, 2, 2, 2, 1, 2, 2, 2, 2, 2, 1, 2, 2, 2, 2, 2, 1, 2, 2, 2, 1],
    [1, 1, 2, 2, 1, 2, 1, 2, 1, 1, 1, 1, 1, 2, 1, 2, 1, 2, 2, 1, 1],
    [1, 2, 2, 2, 2, 2, 1, 2, 2, 2, 1, 2, 2, 2, 1, 2, 2, 2, 2, 2, 1],
    [1, 2, 1, 1, 1, 1, 1, 1, 1, 2, 1, 2, 1, 1, 1, 1, 1, 1, 1, 2, 1],
    [1, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 1],
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
]
# Keyboard and game setup
kbd = Keyboard()
clock = Clock()
greenGhost = GreenGhost(Vector(CANVAS_WIDTH/2, CANVAS_HEIGHT/2), Vector(1,0), "/Users/dreniskastrati/Downloads/PacManProject/PacMan/pacmanPack/greenGhost.png", 1, 8, CANVAS_WIDTH, CANVAS_HEIGHT)
blueGhost = OtherGhost(Vector(CANVAS_WIDTH/2, CANVAS_HEIGHT/2), Vector(1,0), "/Users/dreniskastrati/Downloads/PacManProject/PacMan/pacmanPack/blueGhost.png", 1, 8, CANVAS_WIDTH, CANVAS_HEIGHT)
redGhost = OtherGhost(Vector(CANVAS_WIDTH/2, CANVAS_HEIGHT/2), Vector(1,0), "/Users/dreniskastrati/Downloads/PacManProject/PacMan/pacmanPack/redGhost.png", 1, 8, CANVAS_WIDTH, CANVAS_HEIGHT)
orangeGhost = OtherGhost(Vector(CANVAS_WIDTH/2, CANVAS_HEIGHT/2), Vector(1,0), "/Users/dreniskastrati/Downloads/PacManProject/PacMan/pacmanPack/orangeGhost.png", 1, 8, CANVAS_WIDTH, CANVAS_HEIGHT)

Ghosts = [greenGhost, blueGhost, redGhost, orangeGhost]
pacman = PacMan(Vector(CANVAS_WIDTH/2, CANVAS_HEIGHT/5), Vector(0, 0), kbd, "/Users/dreniskastrati/Downloads/PacManProject/PacMan/pacmanPack/PacMan.png", 1, 8,CANVAS_WIDTH,CANVAS_HEIGHT)
Mg = MapGenerator(arr, CANVAS_WIDTH, CANVAS_HEIGHT)
# Wall creation
'''
walls = [
    Wall(0, 0, 0, CANVAS_HEIGHT/3),  # Left wall
    Wall(0, 2*CANVAS_HEIGHT/3, 0, CANVAS_HEIGHT),  # LEFT WALL
    Wall(CANVAS_WIDTH, 0, CANVAS_WIDTH, CANVAS_HEIGHT/3), 
    Wall(CANVAS_WIDTH, 2*CANVAS_HEIGHT/3, CANVAS_WIDTH, CANVAS_HEIGHT),
    Wall(0, 0, CANVAS_WIDTH, 0),  # Top wall
    Wall(0, CANVAS_HEIGHT, CANVAS_WIDTH, CANVAS_HEIGHT),  # Bottom wall
    Wall(0, CANVAS_HEIGHT/3, CANVAS_WIDTH/5, CANVAS_HEIGHT/3),  # Bottom middle section left
    Wall(4*CANVAS_WIDTH/5, CANVAS_HEIGHT/3, CANVAS_WIDTH, CANVAS_HEIGHT/3),  # Bottom middle section right
    Wall(0, 2*CANVAS_HEIGHT/3, CANVAS_WIDTH/5, 2*CANVAS_HEIGHT/3),  # Top middle section left
    Wall(4*CANVAS_WIDTH/5, 2*CANVAS_HEIGHT/3, CANVAS_WIDTH, 2*CANVAS_HEIGHT/3)  # Top middle section right
]'''
interaction = Interaction(pacman, Ghosts, kbd, Mg.walls,Mg.square)

def draw(canvas):
    interaction.update()
    for wall in Mg.walls:
        wall.draw(canvas)
    for sq in Mg.square:
        sq.draw(canvas)

    clock.tick()
    if clock.transition(FRAME_DURATION):
        pacman.next_frame()
    # Handle movement and direction here
    
    for ghost in Ghosts:
        if type(ghost) == GreenGhost:
            ghost.update(pacman)
        else:
            ghost.update()
        ghost.draw(canvas)

    pacman.update()
    pacman.draw(canvas)

    #print(ghost.current_direction, " ", ghost.vel)

# Create frame and start the game
frame = simplegui.create_frame('PacMan', CANVAS_WIDTH, CANVAS_HEIGHT)
frame.set_draw_handler(draw)
frame.set_keydown_handler(kbd.keyDown)
frame.start()