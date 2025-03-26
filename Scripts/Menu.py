import SimpleGUICS2Pygame.simpleguics2pygame as simplegui
import random
import math
from MyPac import PacMan
from utils import Vector
from walls import Wall
from map_generator import MapGenerator
from Ghosts import Ghost
from Points import Point
from green_ghost import GreenGhost
from other_ghosts import OtherGhost

# Game states
MENU = "menu"
PLAYING = "playing"
PAUSED = "paused"
CREDITS = "credits"
WIN = "win"
LOSE = "lose"
game_state = MENU

# Game constants
CANVAS_WIDTH = 640
CANVAS_HEIGHT = 695

# Game objects (initialized when game starts)
Mg = None
pacman = None
Ghosts = []
interaction = None
kbd = None
clock = None

# Starry background
stars = [(random.randint(0, CANVAS_WIDTH), random.randint(0, CANVAS_HEIGHT)) for _ in range(50)]
light = simplegui.load_image("https://i.ibb.co/21YDG7fm/light.png")
image_width = light.get_width()
image_height = light.get_height()

# Map layout (from MainGame.py)
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

class Keyboard:
    def __init__(self):
        self.right = False
        self.left = False
        self.up = False
        self.down = False
        self.step = 0

    def keyDown(self, key):
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

def initialize_game():
    global Mg, pacman, Ghosts, interaction, kbd, clock
    kbd = Keyboard()
    clock = Clock()
    Mg = MapGenerator(arr, CANVAS_WIDTH, CANVAS_HEIGHT)
    greenGhost = GreenGhost(Vector(CANVAS_WIDTH/2, CANVAS_HEIGHT/2), Vector(0,0), "https://i.postimg.cc/Xqysd90Q/green-Ghost.png", 1, 8, CANVAS_WIDTH, CANVAS_HEIGHT)
    blueGhost = OtherGhost(Vector(CANVAS_WIDTH/2, CANVAS_HEIGHT/2), Vector(0,0), "https://i.postimg.cc/bJS5H7xx/blue-Ghost.png", 1, 8, CANVAS_WIDTH, CANVAS_HEIGHT)
    redGhost = OtherGhost(Vector(CANVAS_WIDTH/2, CANVAS_HEIGHT/2), Vector(0,0), "https://i.postimg.cc/kXmHKhBS/redGhost.png", 1, 8, CANVAS_WIDTH, CANVAS_HEIGHT)
    orangeGhost = OtherGhost(Vector(CANVAS_WIDTH/2, CANVAS_HEIGHT/2), Vector(0,0), "https://i.postimg.cc/c4RVzGVT/orange-Ghost.png", 1, 8, CANVAS_WIDTH, CANVAS_HEIGHT)
    Ghosts = [blueGhost, redGhost, orangeGhost, greenGhost]
    pacman = PacMan(Vector(CANVAS_WIDTH/2, CANVAS_HEIGHT/5), Vector(0, 0), kbd, "https://i.postimg.cc/pTrGVgcN/PacMan.png", 1, 8,CANVAS_WIDTH,CANVAS_HEIGHT)
    interaction = Interaction(pacman, Ghosts, kbd, Mg.walls, Mg.square, Mg.points)

def draw_menu(canvas):
    canvas.draw_polygon([[0, 0], [CANVAS_WIDTH, 0], [CANVAS_WIDTH, CANVAS_HEIGHT], [0, CANVAS_HEIGHT]], 1, "Black", "Black")
    for star in stars:
        canvas.draw_circle(star, 2, 1, "White", "White")
    title = "PAC-MAN"
    title_width = frame.get_canvas_textwidth(title, 70, "monospace")
    canvas.draw_text(title, ((CANVAS_WIDTH - title_width)/2, 150), 70, "Yellow", "monospace")
    draw_button(canvas, "Play", CANVAS_WIDTH/2 - 100, 250)
    draw_button(canvas, "Credits", CANVAS_WIDTH/2 - 100, 350)

def draw_playing(canvas):
    interaction.update()
    for wall in Mg.walls:
        wall.draw(canvas)
    for sq in Mg.square:
        sq.draw(canvas)
    for p in Mg.points:
        p.draw(canvas)
    clock.tick()
    if clock.transition(10):
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

def draw_paused(canvas):
    canvas.draw_polygon([[0, 0], [500, 0], [500, 400]], 1, "Black", "Black")
    canvas.draw_text("Paused", (180, 80), 40, "Red", "monospace")
    draw_button(canvas, "Resume", 150, 160)
    draw_button(canvas, "Quit", 150, 260)

def draw_credits(canvas):
    canvas.draw_polygon([[0, 0], [500, 0], [500, 400]], 1, "Black", "Black")
    credits_title = "Credits"
    title_width = frame.get_canvas_textwidth(credits_title, 40, "monospace")
    title_x = (500 - title_width) / 2
    canvas.draw_text(credits_title, (title_x, 80), 40, "Yellow", "monospace")
    canvas.draw_line((title_x, 90), (title_x + title_width, 90), 3, "Yellow")

def draw_win(canvas):
    canvas.draw_polygon([[0, 0], [CANVAS_WIDTH, 0], [CANVAS_WIDTH, CANVAS_HEIGHT], [0, CANVAS_HEIGHT]], 1, "Black", "Black")
    canvas.draw_text("YOU WIN!", (200, 300), 50, "Yellow", "monospace")
    draw_button(canvas, "Restart", 220, 400)

def draw_lose(canvas):
    canvas.draw_polygon([[0, 0], [CANVAS_WIDTH, 0], [CANVAS_WIDTH, CANVAS_HEIGHT], [0, CANVAS_HEIGHT]], 1, "Black", "Black")
    canvas.draw_text("GAME OVER", (180, 300), 50, "Red", "monospace")
    draw_button(canvas, "Restart", 220, 400)

def draw_button(canvas, text, x, y, width=200, height=60):
    canvas.draw_polygon([[x, y], [x + width, y], [x + width, y + height], [x, y + height]], 3, "Yellow", "Blue")
    text_x = x + (width - frame.get_canvas_textwidth(text, 30, "monospace")) // 2
    canvas.draw_text(text, (text_x, y + 40), 30, "White", "monospace")

def draw(canvas):
    if game_state == MENU:
        draw_menu(canvas)
    elif game_state == PLAYING:
        draw_playing(canvas)
    elif game_state == PAUSED:
        draw_paused(canvas)
    elif game_state == CREDITS:
        draw_credits(canvas)
    elif game_state == WIN:
        draw_win(canvas)
    elif game_state == LOSE:
        draw_lose(canvas)

def click(pos):
    global game_state
    x, y = pos
    if game_state == MENU:
        if CANVAS_WIDTH/2 - 100 <= x <= CANVAS_WIDTH/2 + 100:
            if 250 <= y <= 310:
                initialize_game()
                game_state = PLAYING
                frame.set_keydown_handler(kbd.keyDown)
            elif 350 <= y <= 410:
                game_state = CREDITS
    elif game_state in [WIN, LOSE]:
        if 220 <= x <= 420 and 400 <= y <= 460:
            initialize_game()
            game_state = PLAYING
            frame.set_keydown_handler(kbd.keyDown)

frame = simplegui.create_frame("Pac-Man", CANVAS_WIDTH, CANVAS_HEIGHT)
frame.set_draw_handler(draw)
frame.set_mouseclick_handler(click)
frame.start()
