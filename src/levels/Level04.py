import pyxel
from components.Brick import Brick
from components.Level import Difficulty, Level

class Level04(Level):
  def __init__(self):
    super().__init__(
      4,
      Difficulty.MODERATE,
      0.63
    )
  def load_level(self):
    self.bricks_layout.clear_bricks()
    color_pallete = [
      pyxel.COLOR_PINK,
      pyxel.COLOR_BLACK,
      pyxel.COLOR_LIME
    ]
    ix_color = lambda i: color_pallete[i % len(color_pallete)]
    for i in range(16):
      x = i*Brick.DEFAULT_WIDTH
      health = (
        1 if i < 4 or i > 11 else
        (10 if (i >= 4 and i < 6) or (i > 9 and i <= 11) else 20 )
      )
      self.bricks_layout.append_bricks(
        Brick(x=x, y=128, color=ix_color(i), health=health)
      )
      if i == 0 or i == 15:
        self.bricks_layout.append_bricks(
          Brick(x=x, y=144, health=1, color=ix_color(i+1)),
          Brick(x=x, y=160, health=1, color=ix_color(i+2)),
          Brick(x=x, y=176, health=1, color=ix_color(i+2)),
          Brick(x=x, y=192, health=10, color=ix_color(i+3))
        )
      if i == 1 or i == 14:
        self.bricks_layout.append_bricks(
          Brick(x=x, y=144, health=1, color=ix_color(i+1)),
          Brick(x=x, y=160, health=1, color=ix_color(i+2)),
          Brick(x=x, y=176, health=10, color=ix_color(i+3))
        )
      if i == 2 or i == 13:
        self.bricks_layout.append_bricks(
          Brick(x=x, y=144, health=1, color=ix_color(i+1)),
          Brick(x=x, y=160, health=10, color=ix_color(i+2))
        )
      if i == 3 or i == 12:
        self.bricks_layout.append_bricks(
          Brick(x=x, y=144, health=10, color=ix_color(i+1))
        )