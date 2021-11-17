
import pyxel

from components.Ball import Ball
from components.BottomBar import BottomBar
from components.Button import Button
from components.Level import Level, State
from components.Rect import Edge
from levels.Level01 import Level01
from utils import print_text


class App:

  def __init__(self) -> None:
    self.width = 256
    self.height = 256
    self.fps = 60

    self.levels: list[Level] = []
    self.current_level: Level = None

    self.button_focus = 0
    self.buttons: list[Button] = []

    pyxel.init(self.width, self.height, fps=self.fps, scale=3, caption="Breakout")

    self.init_components()
    self.load_levels()

  def run(self):
    pyxel.run(self.update, self.draw)

  def show_main_menu(self):
    pass
  
  def load_levels_menu(self):
    pass

  def load_level(self, level: Level):
    self.current_level = level
    self.current_level.load_level()
    self.level_state = State.INGAME
    self.init_components()

  def load_levels(self):
    self.levels = [
      Level01()
    ]

  def init_components(self):
    self.bottom_bar = BottomBar(height=5, width=35)
    self.ball = Ball(
      radius = 3,
      x = self.bottom_bar.x+self.bottom_bar.width/2,
      y = self.bottom_bar.y-3,
      vx = 0,
      vy = -2,
      color = pyxel.COLOR_WHITE
    )

  def update(self):
    if self.current_level is not None:
      if self.level_state == State.INGAME:
        if pyxel.btn(pyxel.KEY_LEFT): self.bottom_bar.move_left(2)
        if pyxel.btn(pyxel.KEY_RIGHT): self.bottom_bar.move_right(2)
        
        edge = self.ball.update()
        if edge == Edge.BOTTOM:
          return self.game_over()
        if self.current_level.bricks_layout.size() == 0:
          return self.victory()
        if self.ball.check_rect_collision(self.bottom_bar):
          self.ball.skew_angle_after_bottom_bar_collision(self.bottom_bar)
        
        self.current_level.bricks_layout.check_for_ball_collision(self.ball)
      
    if (self.level_state is not State.INGAME and self.current_level is not None) or self.current_level is None:
      if pyxel.btnr(pyxel.KEY_DOWN): self.change_button_focus(1)
      elif pyxel.btnr(pyxel.KEY_UP): self.change_button_focus(-1)
      elif pyxel.btnr(pyxel.KEY_ENTER): self.button_pressed()

  def draw(self):
    if self.current_level is not None:
      if self.level_state == State.INGAME:
        pyxel.cls(0)
        self.bottom_bar.draw()
        self.ball.draw()
        self.current_level.bricks_layout.draw()
        pyxel.text(2, self.bottom_bar.y-pyxel.FONT_HEIGHT-2, f"Level {self.current_level.level_no}", pyxel.COLOR_WHITE)
    
    if (self.level_state is not State.INGAME and self.current_level is not None) or self.current_level is None:
      for i in range(len(self.buttons)):
        self.buttons[i].unfocus()
        if i == self.button_focus:
          self.buttons[i].focus()
      self.draw_buttons()
  
  def change_button_focus(self, val):
    self.button_focus += val
    if self.button_focus < 0: self.button_focus = len(self.buttons)-1
    self.button_focus %= len(self.buttons)
  
  def create_buttons(self, *buttons):
    self.button_focus = 0
    self.buttons = list(buttons)
  
  def game_over(self):
    self.level_state = State.FAILED
    pyxel.cls(0)
    print_text(self.width/2, self.height/2, "GAME OVER", pyxel.COLOR_WHITE)
    self.create_buttons(
      Button(self.width/2-25, self.height/2+pyxel.FONT_HEIGHT+5, 50, 14, pyxel.COLOR_WHITE, pyxel.COLOR_BLACK),
      Button(self.width/2-25, self.height/2+pyxel.FONT_HEIGHT+24, 50, 14, pyxel.COLOR_WHITE, pyxel.COLOR_BLACK)
    )
    self.buttons[0].set_text("PLAY AGAIN")
    self.buttons[0].set_action(self.play_again)
    self.buttons[1].set_text("MENU")
    self.buttons[1].set_action(self.show_main_menu)
    self.draw_buttons()
  
  def victory(self):
    self.level_state = State.VICTORY
    pyxel.cls(0)
    print_text(self.width/2, self.height/2, "YOU WON!", pyxel.COLOR_GREEN)
    self.create_buttons(
      Button(self.width/2 - 25, self.height/2+pyxel.FONT_HEIGHT+5, 50, 14, pyxel.COLOR_WHITE, pyxel.COLOR_BLACK),
      Button(self.width/2 - 25, self.height/2+pyxel.FONT_HEIGHT+24, 50, 14, pyxel.COLOR_WHITE, pyxel.COLOR_BLACK)
    )
    self.buttons[0].set_text("PLAY AGAIN")
    self.buttons[0].set_action(self.play_again)
    self.buttons[1].set_text("MENU")
    self.buttons[1].set_action(self.show_main_menu)
    self.draw_buttons()

  def play_again(self):
    return self.load_level(self.current_level)
  def draw_buttons(self):
    for btn in self.buttons: btn.draw()

  def button_pressed(self):
    if self.button_focus > len(self.buttons): return
    self.buttons[self.button_focus].pressed()


if __name__ == "__main__":
  app = App()
  app.load_level(app.levels[0])
  app.run()
