from enum import Enum
import pyxel

class Edge(Enum):
  TOP = 0
  RIGHT = 1
  BOTTOM = 2
  LEFT = 3

class Rect:
  def __init__(self, x, y, width, height) -> None:
    self.x = x
    self.y = y
    self.width = width
    self.height = height

  def draw(self, color=0):
    pyxel.rect(self.x, self.y, self.width, self.height, color)