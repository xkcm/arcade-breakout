import pyxel
from components.Brick import Brick
from components.Level import Difficulty, Level
class Level02(Level):
  def __init__(self):
    super().__init__(
      2,
      Difficulty.EASY,
      0.85
    )
  def load_level(self):
    self.bricks_layout.clear_bricks()
    color_palette = [pyxel.COLOR_CYAN, pyxel.COLOR_GREEN, pyxel.COLOR_NAVY]
    for i in range(3):
      for j in range(16):
        y = 80+i*2*Brick.DEFAULT_HEIGHT
        x = j*Brick.DEFAULT_WIDTH
        self.bricks_layout.append_bricks(
          Brick(x=x, y=y, color=color_palette[(i+j)%len(color_palette)], health=3-i)
        )
