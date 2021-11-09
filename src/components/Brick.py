import pyxel
from components.Rect import Rect

class Brick(Rect):
  def __init__(self, x, y, width, height, color=pyxel.COLOR_WHITE) -> None:
    super().__init__(x, y, width, height)
    self.health = 7
    self.setColor(color)
  
  def draw(self):
    super().draw(self.color)
    self.printHealth()
  
  def setColor(self, color):
    self.color = color

  def wasHit(self, edge):
    self.health -= 1
    return self.health
  
  def printHealth(self):
    pyxel.text(self.x+4, self.y+3, str(self.health), pyxel.COLOR_WHITE)