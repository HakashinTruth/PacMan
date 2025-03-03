import SimpleGUICS2Pygame.simpleguics2pygame as simplegui
import math
from MyPac import PacMan
from utils import Vector

class Keyboard:  # Keyboard class
    def __init__(self):
        self.right = False
        self.left = False
        self.up = False
        self.down = False
        self.step = 0
        
    def keyDown(self, key):
        if key == simplegui.KEY_MAP["right"]:
            self.right = True
            self.left = False
            self.up = False
            self.down = False
        elif key == simplegui.KEY_MAP["left"]:
            self.left = True
            self.right = False
            self.up = False
            self.down = False
        elif key == simplegui.KEY_MAP["up"]:
            self.up = True
            self.down = False
            self.right = False
            self.left = False
        elif key == simplegui.KEY_MAP["down"]:
            self.down = True
            self.up = False
            self.right = False
            self.left = False

    def keyUp(self, key):
        if key == simplegui.KEY_MAP["right"]:
            self.right = False
        if key == simplegui.KEY_MAP["left"]:
            self.left = False
        if key == simplegui.KEY_MAP["up"]:
            self.up = False
        if key == simplegui.KEY_MAP["down"]:
            self.down = False

class Interaction:
    def __init__(self, pacman, keyboard):
        self.pacman = pacman
        self.keyboard = keyboard

    def update(self):
        # No need to handle velocity here anymore
        pass  # Interaction now handled directly in PacMan's update()
        
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

kbd = Keyboard()
clock = Clock()
pacman = PacMan(Vector(400, 300), Vector(0, 0), kbd, "https://i.postimg.cc/Z0k4dWCw/PacMan.png", 1, 8)
interaction = Interaction(pacman, kbd)

# Constants:
CANVAS_WIDTH = 800
CANVAS_HEIGHT = 600
# Constants (adjust frame duration for smoother animation)
FRAME_DURATION = 10  # Higher = slower animation

def draw(canvas):
    clock.tick()
    if clock.transition(FRAME_DURATION):
        pacman.next_frame()
    pacman.update()  # Handle movement and direction here
    pacman.draw(canvas)

frame = simplegui.create_frame('PacMan', CANVAS_WIDTH, CANVAS_HEIGHT)
frame.set_draw_handler(draw)
frame.set_keydown_handler(kbd.keyDown)
frame.set_keyup_handler(kbd.keyUp)  # Add key release handler
frame.start()