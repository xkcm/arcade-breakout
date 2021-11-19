from enum import Enum
from random import choice

import pyxel
from utils import milis

from components.BottomBar import BottomBar
from components.Rect import Rect


class PowerUpType(Enum):
  BAR_EXTENSION = 0
  TRIPLE_BALL = 1
  SPEED_UP = 2
  SLOW_DOWN = 3

class PowerUp(Rect):

  DEFAULT_SPEED = 1

  def __init__(self, x, y, width, height, type: PowerUpType, image_pos: list[int], lifespan=None) -> None:
    super().__init__(x, y, width, height)
    self.type = type
    self.image_pos = image_pos
    self.y_acceleration = PowerUp.DEFAULT_SPEED
    self.action = None
    self.lifespan = lifespan
    self.activated_at = None

    self.drawable = True
  
  def should_be_dead(self):
    if self.lifespan is None or self.activated_at is None: return False
    return self.activated_at + self.lifespan < milis()

  def draw(self):
    if not self.drawable: return
    pyxel.blt(self.x, self.y, 0, self.image_pos[0], self.image_pos[1], self.width, self.height)
  
  def collided(self):
    pyxel.play(1, 1)
    self.activated_at = milis()
    self.drawable = False
    if self.action is not None: self.action()

  def update(self, bottom_bar: BottomBar):
    if self.should_be_dead():
      if self.end_action is not None: self.end_action()
      return True

    if not self.drawable: return False

    if self.x+self.width > bottom_bar.x and self.x < bottom_bar.x+bottom_bar.width and self.y+self.height > bottom_bar.y:
      self.collided()
      return False

    self.y += self.y_acceleration
    if self.y > pyxel.height:
      self.drawable = False
    return False
  
  def set_action(self, action):
    self.action = action
  
  def set_end_action(self, action):
    self.end_action = action
  

  @staticmethod
  def spawn(type: PowerUpType, spawn_pos: list[int], action):
    w = 8
    h = 8
    image_pos = []
    lifespan = 15*1000
    if type is PowerUpType.BAR_EXTENSION:
      image_pos = [0, 8]
    elif type is PowerUpType.SLOW_DOWN:
      image_pos = [16, 8]
    elif type is PowerUpType.SPEED_UP:
      image_pos = [24, 8]
    elif type is PowerUpType.TRIPLE_BALL:
      image_pos = [8, 8]
      lifespan = 0
    power_up = PowerUp(x=spawn_pos[0], y=spawn_pos[1], width=w, height=h, type=type, image_pos=image_pos, lifespan=lifespan)
    power_up.set_action(action[0])
    power_up.set_end_action(action[1])
    return power_up

  @staticmethod
  def random():
    return PowerUpType[choice(list(filter(lambda s: not s.startswith("__"), dir(PowerUpType))))]
