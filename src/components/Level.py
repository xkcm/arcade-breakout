
from enum import Enum

from components.Grid import Grid

class State(Enum):
  FAILED = 0
  INGAME = 1
  VICTORY = 2
  OUTGAME = 3

class Difficulty(Enum):
  NOOB = 0
  EASY = 1
  MEDIOCRE = 2
  MODERATE = 3
  MEDIUM = 4
  HARD = 5
  REALLY_HARD = 6
  EXTREME = 7
  LEGENDARY = 8

class Level:
  def __init__(self, level_no, difficulty, chance_of_power_up):
    self.bricks_layout = Grid()
    self.level_no = level_no
    self.difficulty: Difficulty = difficulty
    self.chance_of_power_up = chance_of_power_up

  def load_level(self):
    pass
