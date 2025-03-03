import simpleguitk as simplegui

class Spritesheet:
    def __init__(self, sprite_url, rows, columns):
        self.sprite_image = simplegui.load_image(sprite_url)
        self.rows = rows
        self.cols = columns
        self.sprite_width = self.sprite_image.get_width()
        self.sprite_height = self.sprite_image.get_height()
        self.frame_width = self.sprite_width / self.cols
        self.frame_height = self.sprite_height / self.rows
        self.frame_centers = [
            [(col * self.frame_width + self.frame_width / 2,
              row * self.frame_height + self.frame_height / 2)
             for col in range(self.cols)]
            for row in range(self.rows)
        ]
        self.current_frame = (0, 0)  # (row, col)

    def draw(self, canvas, position):
        center_x, center_y = self.frame_centers[self.current_frame[0]][self.current_frame[1]]
        canvas.draw_image(self.sprite_image,
                          (center_x, center_y), (self.frame_width, self.frame_height),
                          position, (self.frame_width, self.frame_height))

    def next_frame(self):
        row, col = self.current_frame
        col = (col + 1) % self.cols
        if col == 0:
            row = (row + 1) % self.rows
        self.current_frame = (row, col)