import pyxel
from components.Brick import Brick
from components.Level import Difficulty, Level

class Level03(Level):
  def __init__(self):
    super().__init__(3, Difficulty.EASY)
  def load_level(self):
    self.bricks_layout.set_bricks(
      Brick(1, 1, pyxel.width/2-1, 10, 1, pyxel.COLOR_BROWN),
      Brick(pyxel.width/2+1, 1, pyxel.width/2-1, 10, 1, pyxel.COLOR_CYAN)
    )