import pyxel
from components.Brick import Brick
from components.Level import Difficulty, Level
from random import randint

from utils import random_color

class Level02(Level):
  def __init__(self):
    super().__init__(
      2,
      Difficulty.EASY,
      0.85
    )
  def load_level(self):
    bricks_in_row = 16
    brick_width = pyxel.width / bricks_in_row
    for i in range(bricks_in_row):
      self.bricks_layout.append_bricks(
        Brick(i*brick_width, pyxel.height/2-brick_width, brick_width, brick_width, randint(2, 10), random_color())
      )