import pyxel

from components.Rect import Edge
from components.Vector import Axis, Vector


class Ball:
  def __init__(self, radius, x, y, v, angle) -> None:
    self.radius = radius
    self.x = x
    self.y = y
    self.v = Vector()
    self.v.setPolar(v, angle)
  
  def draw(self):
    pyxel.circ(self.x, self.y, self.radius, 7)

  def update(self):
    deltaX = round(self.v.x)
    deltaY = round(self.v.y)
    self.x += deltaX
    self.y += deltaY
    self.checkBorderCollision()

  def checkBorderCollision(self):
    if (self.x + self.radius >= pyxel.width):
      self.x = pyxel.width - self.radius
      self.v.reflectAngleBy(Axis.Y)
      return Edge.RIGHT
    if (self.x - self.radius <= 0):
      self.x = self.radius
      self.v.reflectAngleBy(Axis.Y)
      return Edge.LEFT
    if (self.y - self.radius <= 0):
      self.y = self.radius
      self.v.reflectAngleBy(Axis.X)
      return Edge.TOP
    if (self.y + self.radius >= pyxel.height):
      self.y = pyxel.height - self.radius
      self.v.reflectAngleBy(Axis.X)
      return Edge.BOTTOM

  def checkRectCollision(self, rect):
    if (self.x >= rect.x and self.x <= rect.x+rect.width):
      if (self.y+self.radius >= rect.y and self.y+self.radius <= rect.y+rect.height):
        self.y = rect.y-self.radius
        self.v.reflectAngleBy(Axis.X)
        return Edge.TOP
      if (self.y-self.radius <= rect.y+rect.height and self.y-self.radius>=rect.y):
        self.y = rect.y+rect.height+self.radius
        self.v.reflectAngleBy(Axis.X)
        return Edge.BOTTOM
    if (self.y >= rect.y and self.y <= rect.y+rect.height):
      if (self.x+self.radius >= rect.x and self.x+self.radius <= rect.x+rect.width):
        self.x = rect.x-self.radius
        self.v.reflectAngleBy(Axis.Y)
        return Edge.LEFT
      if (self.x-self.radius <= rect.x + rect.width and self.x-self.radius >= rect.x):
        self.x = rect.x+rect.width+self.radius
        self.v.reflectAngleBy(Axis.Y)
        return Edge.RIGHT
