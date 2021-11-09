from math import pi
import pyxel

from components.BottomBar import BottomBar
from components.Ball import Ball
from components.Brick import Brick
from components.Grid import Grid

class App:
  def __init__(self) -> None:
    self.width = 256
    self.height = 256
    self.fps = 60
    self.grid = []

    pyxel.init(self.width, self.height, fps=self.fps, scale=3, caption="Breakout")

    self.initComponents()

    pyxel.run(self.update, self.draw)

  def initComponents(self):
    self.bottomBar = BottomBar(height=5, width=35)
    self.ball = Ball(radius=2.5, x=self.width/2, y=self.height/2, v=1, angle=pi/4)
    self.brickGrid = Grid()
    self.initGrid()

  def initGrid(self):
    self.brickGrid.appendBricks(
      Brick(1, 1, 10, 10, pyxel.COLOR_DARKBLUE),
      Brick(12, 1, 10, 10, pyxel.COLOR_GREEN),
      Brick(1, 12, 10, 10, pyxel.COLOR_PEACH)
    )

  def update(self):
    if pyxel.btn(pyxel.KEY_LEFT): self.bottomBar.moveLeft(2)
    if pyxel.btn(pyxel.KEY_RIGHT): self.bottomBar.moveRight(2)
    self.ball.update()
    self.ball.checkRectCollision(self.bottomBar)
    self.brickGrid.checkForBallCollision(self.ball)

  def draw(self):
    pyxel.cls(0)
    self.bottomBar.draw()
    self.ball.draw()
    self.brickGrid.draw()

App()
