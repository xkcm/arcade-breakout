from pyxel import FONT_HEIGHT, FONT_WIDTH, text

def print_text(x, y, s, color):
  width = len(s)*FONT_WIDTH-1
  text(x-width/2, y-FONT_HEIGHT/2, s, color)