import pyxel
from components.Brick import Brick
from components.Level import Difficulty, Level

class Level05(Level):
  def __init__(self):
    super().__init__(
      5,
      Difficulty.MEDIUM,
      0.6
    )
  def load_level(self):
    self.bricks_layout.clear_bricks()
    color_pallete = [
      pyxel.COLOR_BLACK,
      pyxel.COLOR_CYAN
    ]
    ix_color = lambda i: color_pallete[i % len(color_pallete)]
    self.bricks_layout.append_bricks(
      Brick(x=0, y=64, health=20),
      Brick(x=240, y=64, health=20),

      Brick(x=0, y=80, health=5, color=ix_color(1)),
      Brick(x=16, y=80, health=20),
      Brick(x=224, y=80, health=20),
      Brick(x=240, y=80, health=5, color=ix_color(1)),

      Brick(x=0, y=96, health=2, color=ix_color(2)),
      Brick(x=16, y=96, health=5, color=ix_color(3)),
      Brick(x=32, y=96, health=20),
      Brick(x=208, y=96, health=20),
      Brick(x=224, y=96, health=5, color=ix_color(3)),
      Brick(x=240, y=96, health=2, color=ix_color(2)),

      Brick(x=0, y=160, health=20),
      Brick(x=240, y=160, health=20),

      Brick(x=0, y=144, health=5, color=ix_color(1)),
      Brick(x=16, y=144, health=20),
      Brick(x=224, y=144, health=20),
      Brick(x=240, y=144, health=5, color=ix_color(1)),

      Brick(x=0, y=128, health=2, color=ix_color(2)),
      Brick(x=16, y=128, health=5, color=ix_color(3)),
      Brick(x=32, y=128, health=20),
      Brick(x=208, y=128, health=20),
      Brick(x=224, y=128, health=5, color=ix_color(3)),
      Brick(x=240, y=128, health=2, color=ix_color(2)),

      Brick(x=0, y=112, health=1, color=ix_color(3)),
      Brick(x=16, y=112, health=5, color=ix_color(4)),
      Brick(x=32, y=112, health=30, color=ix_color(5)),
      Brick(x=48, y=112, health=20),
      Brick(x=240, y=112, health=1, color=ix_color(3)),
      Brick(x=224, y=112, health=5, color=ix_color(4)),
      Brick(x=208, y=112, health=30, color=ix_color(5)),
      Brick(x=192, y=112, health=20)
    )
    