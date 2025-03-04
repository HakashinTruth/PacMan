import SimpleGUICS2Pygame.simpleguics2pygame as simplegui
import math
from MyPac import PacMan
from utils import Vector
from walls import Wall

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
    def __init__(self, pacman, keyboard, walls):
        self.pacman = pacman
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
                
                # Precise wall collision handling
                if wall.rightleft == 'l':
                    # Push Pac-Man slightly to the right of the left wall
                    self.pacman.pos.x = wall.x1 + self.pacman.radius + 1
                elif wall.rightleft == 'r':
                    # Push Pac-Man slightly to the left of the right wall
                    self.pacman.pos.x = wall.x1 - self.pacman.radius - 1
                elif wall.rightleft == 't':
                    # Push Pac-Man slightly below the top wall
                    self.pacman.pos.y = wall.y1 + self.pacman.radius + 1
                elif wall.rightleft == 'b':
                    # Push Pac-Man slightly above the bottom wall
                    self.pacman.pos.y = wall.y1 - self.pacman.radius - 1
                
                break  # Stop checking after first collision
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
CANVAS_WIDTH = 448  # 2x original 224
CANVAS_HEIGHT = 512  # 2x original 256
# Constants (adjust frame duration for smoother animation)
FRAME_DURATION = 10  # Higher = slower animation

# Keyboard and game setup
kbd = Keyboard()
clock = Clock()
pacman = PacMan(Vector(224, 280), Vector(0, 0), kbd, "https://i.postimg.cc/Z0k4dWCw/PacMan.png", 1, 8)

# Updated wall creation to cover all sides of the game area
walls = [
    Wall(0, 0, 0, CANVAS_HEIGHT, 10, 'blue', 'l'),     # Left wall
    Wall(CANVAS_WIDTH, 0, CANVAS_WIDTH, CANVAS_HEIGHT, 10, 'blue', 'r'),  # Right wall
    Wall(0, 0, CANVAS_WIDTH, 0, 10, 'blue', 't'),      # Top wall
    Wall(0, CANVAS_HEIGHT, CANVAS_WIDTH, CANVAS_HEIGHT, 10, 'blue', 'b')  # Bottom wall
]

interaction = Interaction(pacman, kbd, walls)

def draw(canvas):
    interaction.update()
    for wall in walls:
        wall.draw(canvas)
    clock.tick()
    if clock.transition(FRAME_DURATION):
        pacman.next_frame()
    pacman.update()  # Handle movement and direction here
    pacman.draw(canvas)

# Create frame and start the game
frame = simplegui.create_frame('PacMan', CANVAS_WIDTH, CANVAS_HEIGHT)
frame.set_draw_handler(draw)
frame.set_keydown_handler(kbd.keyDown)
frame.start()