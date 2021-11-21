import pyxel
from components.Brick import Brick
from components.Level import Difficulty, Level

class Level01(Level):
  def __init__(self):
    super().__init__(
      1,
      Difficulty.NOOB,
      0.9
    )
  def load_level(self):
    self.bricks_layout.set_bricks(
      Brick(x=96, y=80, color=pyxel.COLOR_LIGHTBLUE),
      Brick(x=112, y=80, color=pyxel.COLOR_ORANGE),
      Brick(x=128, y=80, color=pyxel.COLOR_LIGHTBLUE),
      Brick(x=144, y=80, color=pyxel.COLOR_ORANGE),

      Brick(x=96, y=96, color=pyxel.COLOR_ORANGE),
      Brick(x=96, y=112, color=pyxel.COLOR_LIGHTBLUE),
      Brick(x=96, y=128, color=pyxel.COLOR_ORANGE),

      Brick(x=144, y=96, color=pyxel.COLOR_LIGHTBLUE),
      Brick(x=144, y=112, color=pyxel.COLOR_ORANGE),
      Brick(x=144, y=128, color=pyxel.COLOR_LIGHTBLUE)
    )