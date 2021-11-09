import pyxel

from components.Rect import Rect

class BottomBar(Rect):
  def __init__(self, width, height, x=None, y=None) -> None:
    super().__init__(
      width=width,
      height=height,
      x=x or (pyxel.width-width)/2,
      y=y or pyxel.height - (1.1*height)
    )
    self.defaultSpeed = 1
  def moveX(self, x):
    self.x = x
    if (self.x+self.width > pyxel.width): self.x = pyxel.width-self.width
    if (self.x<0): self.x=0
  def moveRight(self, units=None):
    if (units is None): units = self.defaultSpeed
    self.moveX(self.x+units)
  def moveLeft(self, units=None):
    if (units is None): units = self.defaultSpeed
    self.moveX(self.x-units)
  def draw(self):
    super().draw(7)
