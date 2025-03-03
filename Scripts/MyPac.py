import simpleguitk as simplegui
from MainGame import Vector
from sprite_animations import Spritesheet
class PacMan:
    def __init__(self, pos, vel, keys, spriteimgs, rows, columns):
        print("PacMan initialized!")
        self.pos = pos
        self.vel = vel
        self.keys = keys
        self.step = 0
        self.spriteimgs = Spritesheet(spriteimgs, rows, columns)

    def draw(self, canvas):
        self.spriteimgs.draw(canvas, self.pos)

    def update(self):
        if self.keys.right:
            self.vel.add(Vector(1, 0))
            self.step = -1
        elif self.keys.left:
            self.vel.add(Vector(-1, 0))
            self.step = +1
        else:
            self.step = 0
        if self.keys.up:
            self.vel.add(Vector(0, -1))
            self.step = 0
        if not self.keys.up:
            self.vel.add(Vector(0, 1))
            self.step = 0
        self.pos.add(self.vel)

    def next_frame(self):
        self.spriteimgs.next_frame()

    

    