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
    self.default_speed = 1
  def move_x(self, x):
    self.x = x
    if (self.x+self.width > pyxel.width): self.x = pyxel.width-self.width
    if (self.x<0): self.x=0
  def move_right(self, units=None):
    if (units is None): units = self.default_speed
    self.move_x(self.x+units)
  def move_left(self, units=None):
    if (units is None): units = self.default_speed
    self.move_x(self.x-units)
  def draw(self):
    super().draw(pyxel.COLOR_WHITE)
  def set_speed(self, speed):
    self.default_speed = speed
