from math import atan, pi, sqrt
import pyxel

from components.Rect import Edge
from components.Vector import Axis, Vector
from utils import round_angle


class Ball:

  DEFAULT_SPEED = 2
  DEFAULT_RADIUS = 3
  DEFAULT_COLOR = pyxel.COLOR_WHITE

  def __init__(self, x, y, color=None, radius=None, vx=None, vy=None) -> None:
    self.radius = radius or Ball.DEFAULT_RADIUS
    self.x = x
    self.y = y
    self.v = Vector(vx or 0, vy or -Ball.DEFAULT_SPEED)
    self.color = color or Ball.DEFAULT_COLOR
  
  def set_speed(self, speed=None):
    self.v.set_length(speed or Ball.DEFAULT_SPEED)
  
  def draw(self):
    pyxel.circ(self.x, self.y, self.radius, self.color)

  def update(self):
    delta_x = round(self.v.x)
    delta_y = round(self.v.y)
    self.x += delta_x
    self.y += delta_y
    return self.check_border_collision()

  def check_border_collision(self):
    if (self.x + self.radius >= pyxel.width):
      self.x = pyxel.width - self.radius
      self.v.reflect_angle_by(Axis.Y)
      return Edge.RIGHT
    if (self.x - self.radius <= 0):
      self.x = self.radius
      self.v.reflect_angle_by(Axis.Y)
      return Edge.LEFT
    if (self.y - self.radius <= 0):
      self.y = self.radius
      self.v.reflect_angle_by(Axis.X)
      return Edge.TOP
    if (self.y + self.radius >= pyxel.height):
      self.y = pyxel.height - self.radius
      self.v.reflect_angle_by(Axis.X)
      return Edge.BOTTOM

  def check_rect_collision(self, rect):
    if (self.x >= rect.x and self.x <= rect.x+rect.width):
      if (self.y+self.radius >= rect.y and self.y+self.radius <= rect.y+rect.height):
        self.y = rect.y-self.radius-1
        self.v.reflect_angle_by(Axis.X)
        return Edge.TOP
      if (self.y-self.radius <= rect.y+rect.height and self.y-self.radius>=rect.y):
        self.y = rect.y+rect.height+self.radius+1
        self.v.reflect_angle_by(Axis.X)
        return Edge.BOTTOM
    if (self.y >= rect.y and self.y <= rect.y+rect.height):
      if (self.x+self.radius >= rect.x and self.x+self.radius <= rect.x+rect.width):
        self.x = rect.x-self.radius-1
        self.v.reflect_angle_by(Axis.Y)
        return Edge.LEFT
      if (self.x-self.radius <= rect.x + rect.width and self.x-self.radius >= rect.x):
        self.x = rect.x+rect.width+self.radius+1
        self.v.reflect_angle_by(Axis.Y)
        return Edge.RIGHT

  def skew_angle_after_bottom_bar_collision(self, bottom_bar):
    Y_OFFSET = 4
    collision_x = self.x
    center_x = bottom_bar.x+bottom_bar.width/2
    delta_x = center_x - collision_x
    delta_y = bottom_bar.height + self.radius + Y_OFFSET
    new_angle = atan(delta_y/delta_x) if delta_x != 0 else -pi/2
    if delta_x > 0:
      new_angle += -pi

    new_angle = round_angle(new_angle, 6, pi)

    self.v.set_angle(new_angle)
  
  def speed(self):
    return sqrt(self.v.x**2+self.v.y**2)
