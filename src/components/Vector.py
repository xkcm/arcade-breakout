from enum import Enum
from math import atan, cos, sin, sqrt, pi

class Axis(Enum):
  X = 0
  Y = 1

class Vector:
  def __init__(self, x=0, y=0) -> None:
    self.x = x
    self.y = y
    self.angle = atan(x/y) if y != 0 and x != 0 else 0
    self.r = sqrt(x*x+y*y)

  def recalculateComponentsLengths(self):
    self.x = cos(self.angle)*self.r
    self.y = sin(self.angle)*self.r

  def changeAngle(self, deltaTheta):
    self.setAngle(self.angle + deltaTheta)

  def reflectAngleBy(self, axis):
    print(f"Reflecting by {axis}")
    if axis == Axis.Y:
      self.setAngle(pi - self.angle)
    elif axis == Axis.X:
      self.setAngle(-self.angle)

  def setAngle(self, newTheta):
    self.angle = newTheta
    if self.angle > pi: self.angle = -4*pi+self.angle
    elif self.angle < -pi: self.angle = 4*pi+self.angle
    self.recalculateComponentsLengths()
  
  def setPolar(self, r, angle):
    self.angle = angle
    self.r = r
    self.recalculateComponentsLengths()

