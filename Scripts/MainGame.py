import simpleguitk as simplegui
import math
from MyPac import PacMan

class Vector: # Vector class
    def __init__(self, x=0, y=0):
        self.x = x
        self.y = y

    def __str__(self):
        return f"({self.x},{self.y})"

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

    def __ne__(self, other):
        return not self.__eq__(other)

    def get_p(self):
        return (self.x, self.y)

    def copy(self):
        return Vector(self.x, self.y)

    def add(self, other):
        self.x += other.x
        self.y += other.y
        return self

    def __add__(self, other):
        return self.copy().add(other)

    def negate(self):
        return self.multiply(-1)

    def __neg__(self):
        return self.copy().negate()

    def subtract(self, other):
        return self.add(-other)

    def __sub__(self, other):
        return self.copy().subtract(other)

    def multiply(self, k):
        self.x *= k
        self.y *= k
        return self

    def __mul__(self, k):
        return self.copy().multiply(k)

    def __rmul__(self, k):
        return self.copy().multiply(k)

    def divide(self, k):
        return self.multiply(1 / k)

    def __truediv__(self, k):
        return self.copy().divide(k)

    def normalize(self):
        return self.divide(self.length())

    def get_normalized(self):
        return self.copy().normalize()

    def dot(self, other):
        return self.x * other.x + self.y * other.y

    def length(self):
        return math.sqrt(self.x**2 + self.y**2)

    def length_squared(self):
        return self.x**2 + self.y**2

    def reflect(self, normal):
        n = normal.copy()
        n.multiply(2 * self.dot(normal))
        self.subtract(n)
        return self

    def angle(self, other):
        return math.acos(self.dot(other) / (self.length() * other.length()))

    def rotate_anti(self):
        self.x, self.y = -self.y, self.x
        return self

    def rotate_rad(self, theta):
        rx = self.x * math.cos(theta) - self.y * math.sin(theta)
        ry = self.x * math.sin(theta) + self.y * math.cos(theta)
        self.x, self.y = rx, ry
        return self

    def rotate(self, theta):
        theta_rad = theta / 180 * math.pi
        return self.rotate_rad(theta_rad)

    def get_proj(self, vec):
        unit = vec.get_normalized()
        return unit.multiply(self.dot(unit))
class Keyboard: # Keyboard class
    def __init__(self):
        self.right = False
        self.left = False
        self.up = False
        self.down = False
        self.step = 0
    def keyDown(self, key):
        if key == simplegui.KEY_MAP["right"]: # If the right arrow key is pressed
            self.right = True
            self.step = -1
        if key == simplegui.KEY_MAP["left"]: # If the left arrow key is pressed
            self.left = True
            self.step = +1
        if key == simplegui.KEY_MAP["up"]:  # If the up arrow key is pressed
            self.up = True
            self.step = +1
        if key == simplegui.KEY_MAP["down"]: # If the down arrow key is pressed
            self.down = True
            self.step = -1
class Interaction: # Interaction class
    def __init__(self, pacman, keyboard):
        self.pacman = pacman
        self.keyboard = keyboard

    def update(self):
        if self.keyboard.right:
            self.pacman.vel.add(Vector(1, 0))
            self.pacman.step = self.keyboard.step
            
        elif self.keyboard.left:
            self.pacman.vel.add(Vector(-1, 0))
            self.pacman.step = self.keyboard.step
        
        else:
            self.pacman.step = 0
        if self.keyboard.up:
            self.pacman.vel.add(Vector(0, -1))
            self.pacman.step = self.keyboard.step
        elif self.keyboard.down:
            self.pacman.vel.add(Vector(0, 1))
            self.pacman.step = self.keyboard.step
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
pacman = PacMan(Vector(400, 300), Vector(0, 0), kbd, 'Pacman\\pacmanPack\\Pacman.png', 1, 8)
interaction = Interaction(pacman, kbd)

#constants:
CANVAS_WIDTH = 800
CANVAS_HEIGHT = 600
FRAME_DURATION = 5

def draw(canvas):
    clock.tick()
    if clock.transition(FRAME_DURATION):
        pacman.next_frame()
    interaction.update()
    pacman.update()
    pacman.draw(canvas)

frame = simplegui.create_frame('PacMan', CANVAS_WIDTH, CANVAS_HEIGHT)
frame.set_draw_handler(draw)
frame.set_keydown_handler(kbd.keyDown)
frame.start()
