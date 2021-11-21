from enum import Enum
from math import atan, cos, sin, sqrt, pi

class Axis(Enum):
  X = 0
  Y = 1

class Vector:
  def __init__(self, x=0, y=0) -> None:
    self.__x = x
    self.__y = y
    self.__recalculate_polar()
  
  @property
  def x(self):
    return self.__x
  @x.setter
  def x(self, value):
    self.__x = value
    self.__recalculate_polar()
  @property
  def y(self):
    return self.__y
  @y.setter
  def y(self, value):
    self.__y = value
    self.__recalculate_polar()
  @property
  def angle(self):
    return self.__angle

  def __recalculate_polar(self):
    self.__angle = atan(self.__y/self.__x) if self.__y != 0 and self.__x != 0 else 0
    self.__r = sqrt(self.__x**2+self.__y**2)
  def __recalculate_components_lengths(self):
    self.__x = cos(self.__angle)*self.__r
    self.__y = sin(self.__angle)*self.__r

  def change_angle(self, deltaTheta):
    self.set_angle(self.__angle + deltaTheta)

  def reflect_angle_by(self, axis):
    if axis == Axis.Y:
      self.x = -self.x
    elif axis == Axis.X:
      self.y = -self.y

  def set_angle(self, newTheta):
    self.__angle = newTheta
    if self.__angle > pi: self.__angle = -4*pi+self.__angle
    elif self.__angle < -pi: self.__angle = 4*pi+self.__angle
    self.__recalculate_components_lengths()
  
  def set_polar(self, r, angle):
    self.__angle = angle
    self.__r = r
    self.__recalculate_components_lengths()
  
  def set_length(self, length):
    self.__r = length
    self.__recalculate_components_lengths()

