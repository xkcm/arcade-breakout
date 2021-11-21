import pyxel
from components.Brick import Brick
from components.Level import Difficulty, Level

class Level03(Level):
  def __init__(self):
    super().__init__(
      3,
      Difficulty.MEDIOCRE,
      0.7
    )
  def load_level(self):
    self.bricks_layout.clear_bricks()
    color_pallete = [
      pyxel.COLOR_BROWN,
      pyxel.COLOR_YELLOW,
      pyxel.COLOR_PURPLE
    ]
    ix_color = lambda i: color_pallete[i % len(color_pallete)]
    for i in range(10):
      x = 48+i*Brick.DEFAULT_WIDTH
      self.bricks_layout.append_bricks(
        Brick(x=x, y=144, color=ix_color(i), health=15)
      )
    for i in range(14):
      x = 16+i*Brick.DEFAULT_WIDTH
      health = 10 + (5-i if i < 5 else (i-8 if i > 8 else 0))
      self.bricks_layout.append_bricks(
        Brick(x=x, y=32, health=health, color=ix_color(i))
      )
    for i in range(4):
      y = 64+i*Brick.DEFAULT_HEIGHT
      self.bricks_layout.append_bricks(
        Brick(x=48, y=y, color=ix_color(i), health=11),
        Brick(x=192, y=y, color=ix_color(i+1), health=11),
        Brick(x=96, y=y, color=ix_color(i), health=10),
        Brick(x=144, y=y, color=ix_color(i+1), health=10)
      )
      if i == 0 or i == 3:
        self.bricks_layout.append_bricks(
          Brick(x=112, y=y, color=ix_color(i+2), health=10),
          Brick(x=128, y=y, color=ix_color(i), health=10)
        )
      else:
        self.bricks_layout.append_bricks(
          Brick(x=112, y=y, color=ix_color(i+2), health=1),
          Brick(x=128, y=y, color=ix_color(i), health=1)
        )
