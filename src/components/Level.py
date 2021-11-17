
from enum import Enum

from components.Grid import Grid

class State(Enum):
  FAILED = 0
  INGAME = 1
  VICTORY = 2

class Level:
  def __init__(self, level_no):
    self.bricks_layout = Grid()
    self.level_no = level_no
    
  def load_level(self):
    pass
