import pyxel
from components.Rect import Rect
from utils import print_centered_text

class Brick(Rect):
  def __init__(self, x, y, width, height, health, color=pyxel.COLOR_WHITE) -> None:
    super().__init__(x, y, width, height)
    self.health = health
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
    print_centered_text(self.x+self.width/2, self.y+self.height/2, str(self.health), pyxel.COLOR_WHITE)