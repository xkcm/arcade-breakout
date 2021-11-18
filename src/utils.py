
import pyxel
import random

class Align:
  LEFT = 0b1
  X_CENTER = 0b10
  RIGHT = 0b100
  TOP = 0b1000
  Y_CENTER = 0b10000
  BOTTOM = 0b100000

def print_centered_text(x, y, s, color):
  return print_aligned_text(x, y, s, color, Align.X_CENTER | Align.Y_CENTER)

def print_aligned_text(x, y, s, color, align):
  s = str(s)
  width = len(s)*pyxel.FONT_WIDTH-1
  height = pyxel.FONT_HEIGHT
  if align & Align.X_CENTER:
    x -= width/2
  elif align & Align.RIGHT:
    x -= width
  if align & Align.Y_CENTER:
    y -= height/2
  elif align & Align.BOTTOM:
    y -= height
  pyxel.text(x, y, s, color)

def random_color():
  keys = pyxel.__dict__.keys()
  keys = [*filter(lambda key: key.startswith("COLOR_") and key != "COLOR_COUNT", keys)]
  color = random.choice(keys)
  return pyxel.__dict__.get(color)

def constrain(n, minn, maxn):
  return max(min(maxn, n), minn)