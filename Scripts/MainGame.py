import SimpleGUICS2Pygame.simpleguics2pygame as simplegui
import math
import random
from MyPac import PacMan
from utils import Vector
from walls import Wall
from map_generator import MapGenerator
from Ghosts import Ghost
from Points import Point
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
    
    def __init__(self, pacman, ghosts, keyboard, walls, squares, points):
        self.pacman = pacman
        self.ghosts = ghosts
        self.keyboard = keyboard
        self.walls = walls
        self.points = points
        self.last_collision = None  # Track the last wall collided with
        self.lives = 1
        self.score = 0

    def update(self):
        # Check wall collisions with Pac-Man first
        for wall in self.walls:
            if wall.hit(self.pacman):
                self.pacman.stop()
                self.last_collision = wall
                # Adjust Pac-Man's position based on the wall orientation
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
                break  # Only process one wall collision per update

        # Then check collision with points (iterate over a copy if you'll remove elements)
        for point in self.points[:]:
            if self.pacman.collidedWithPoint(point):
                self.points.remove(point)
                self.score += 10

        # Check collision with ghosts separately
        for ghost in self.ghosts:
            if self.pacman.collidedWithPoint(ghost):
                self.lives -= 1
                self.pacman.reset_position()
                
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
    [2, 2, 2, 2, 2, 2, 2, 2, 1, 1, 2, 1, 1, 2, 2, 2, 2, 2, 2, 2, 2],
    [1, 1, 1, 1, 1, 2, 1, 2, 1, 1, 2, 1, 1, 2, 1, 2, 1, 1, 1, 1, 1],
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
greenGhost = GreenGhost(Vector(CANVAS_WIDTH/2, CANVAS_HEIGHT/2), Vector(0,0), "https://i.postimg.cc/Xqysd90Q/green-Ghost.png", 1, 8, CANVAS_WIDTH, CANVAS_HEIGHT)
blueGhost = OtherGhost(Vector(CANVAS_WIDTH/2, CANVAS_HEIGHT/2), Vector(0,0), "https://i.postimg.cc/bJS5H7xx/blue-Ghost.png", 1, 8, CANVAS_WIDTH, CANVAS_HEIGHT)
redGhost = OtherGhost(Vector(CANVAS_WIDTH/2, CANVAS_HEIGHT/2), Vector(0,0), "https://i.postimg.cc/kXmHKhBS/redGhost.png", 1, 8, CANVAS_WIDTH, CANVAS_HEIGHT)
orangeGhost = OtherGhost(Vector(CANVAS_WIDTH/2, CANVAS_HEIGHT/2), Vector(0,0), "https://i.postimg.cc/c4RVzGVT/orange-Ghost.png", 1, 8, CANVAS_WIDTH, CANVAS_HEIGHT)


Ghosts = [blueGhost,redGhost, orangeGhost,greenGhost]
pacman = PacMan(Vector(CANVAS_WIDTH/2, CANVAS_HEIGHT/5), Vector(0, 0), kbd, "https://i.postimg.cc/pTrGVgcN/PacMan.png", 1, 8,CANVAS_WIDTH,CANVAS_HEIGHT)
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
interaction = Interaction(pacman, Ghosts, kbd, Mg.walls,Mg.square, Mg.points)
#light = simplegui.load_image("https://i.ibb.co/M5K7ttPG/light-1.png")
light = simplegui.load_image("https://i.ibb.co/21YDG7fm/light.png")
image_width = light.get_width()
image_height = light.get_height()
def draw(canvas):
    interaction.update()
    for wall in Mg.walls:
        wall.draw(canvas)
    for sq in Mg.square:
        sq.draw(canvas)
    for p in Mg.points:
        p.draw(canvas)
    clock.tick()
    if clock.transition(FRAME_DURATION):
        pacman.next_frame()
        for ghost in Ghosts:
            ghost.next_frame()
    # Handle movement and direction here
    
    for ghost in Ghosts:
        ghost.update(pacman)
        ghost.draw(canvas)
    dest_center = (pacman.pos.x, pacman.pos.y)
    canvas.draw_image(light,  # source
                      (image_width/2, image_height/2),  # source center
                      (image_width, image_height),      # source size
                      dest_center,                      # destination center (pacman's position)
                      (image_width, image_height),      # destination size
                      0)                                # rotation (in radians)
    pacman.update()
    pacman.draw(canvas)
    canvas.draw_text("Lives remaining: " + str(interaction.lives), (10,18), 18, "White")
    canvas.draw_text("Score: " + str(interaction.score), (CANVAS_WIDTH -100,18), 18, "White")

    #print(ghost.current_direction, " ", ghost.vel)

# Create frame and start the game
frame = simplegui.create_frame('PacMan', CANVAS_WIDTH, CANVAS_HEIGHT)
frame.set_draw_handler(draw)
frame.set_keydown_handler(kbd.keyDown)
frame.start()