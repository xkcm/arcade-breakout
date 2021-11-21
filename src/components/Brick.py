import pyxel
from components.Rect import Rect
from utils import print_centered_text

class Brick(Rect):
  DEFAULT_WIDTH = 16
  DEFAULT_HEIGHT = 16
  DEFAULT_HEALTH = 1
  def __init__(self, x, y, width=None, height=None, health=None, color=pyxel.COLOR_WHITE) -> None:
    super().__init__(x, y, width or Brick.DEFAULT_WIDTH, height or Brick.DEFAULT_HEIGHT)
    self.health = health or Brick.DEFAULT_HEALTH
    self.set_color(color)
  
  def draw(self):
    super().draw(self.color)
    self.print_health()
  
  def set_color(self, color):
    self.color = color

  def was_hit(self, edge):
    self.health -= 1
    return self.health
  
  def print_health(self):
    print_centered_text(self.x+self.width/2, self.y+self.height/2, str(self.health), (pyxel.COLOR_WHITE if self.color != pyxel.COLOR_WHITE else pyxel.COLOR_BLACK))