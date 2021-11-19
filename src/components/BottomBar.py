import pyxel

from components.Rect import Rect

class BottomBar(Rect):

  DEFAULT_WIDTH = 35
  DEFAULT_SPEED = 2

  def __init__(self, height, width=None, x=None, y=None) -> None:
    width = width or BottomBar.DEFAULT_WIDTH
    super().__init__(
      width=width,
      height=height,
      x=x or (pyxel.width-width)/2,
      y=y or pyxel.height - (1.1*height)
    )
    self.speed = BottomBar.DEFAULT_SPEED

  def move_x(self, x):
    self.x = x
    if (self.x+self.width > pyxel.width): self.x = pyxel.width-self.width
    if (self.x<0): self.x=0

  def move_right(self):
    self.move_x(self.x+self.speed)

  def move_left(self):
    self.move_x(self.x-self.speed)

  def draw(self):
    super().draw(pyxel.COLOR_WHITE)

  def set_speed(self, speed=None):
    self.speed = speed or BottomBar.DEFAULT_SPEED

  def set_width(self, new_width=None):
    new_width = new_width or BottomBar.DEFAULT_WIDTH
    self.move_x(self.x - (new_width-self.width)/2)
    self.width = new_width