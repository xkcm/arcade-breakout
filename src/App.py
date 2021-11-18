
from math import ceil
import pyxel
from copy import copy, deepcopy

from components.Ball import Ball
from components.BottomBar import BottomBar
from components.Button import Button
from components.Level import Level, State
from components.Rect import Edge
from levels.Level01 import Level01
from levels.Level02 import Level02
from utils import Align, constrain, print_aligned_text


class App:

  def __init__(self) -> None:
    self.width = 256
    self.height = 256
    self.fps = 60

    self.levels: list[Level] = []
    self.current_level: Level = None
    self.level_state = State.OUTGAME

    self.button_focus = 0
    self.buttons: list[Button] = []
    self.config_button_focus()

    pyxel.init(self.width, self.height, fps=self.fps, scale=3, caption="Breakout")
    pyxel.load("../resources.pyxres")

    self.init_components()
    self.load_levels()

  def run(self):
    self.show_main_menu()
    pyxel.run(self.update, self.draw)

  def show_main_menu(self):
    pyxel.cls(0)

    ### LAYOUT [46 pixels height] 46 / 2 = 23
    # 8 pixels "ARCADE BREAKOUT" [-23]
    # 5 pixels spacing [-15]
    # 14 pixels button [-10]
    # 5 pixels spacing [+4]
    # 14 pixels button [+9]
    #############################

    pyxel.blt(self.width/2-34.5, self.height/2-23, 0, 0, 0, 69, 8)
    self.create_buttons(
      Button(self.width/2-34.5, self.height/2-10, 69, 14, pyxel.COLOR_WHITE, pyxel.COLOR_BLACK),
      Button(self.width/2-34.5, self.height/2+9, 69, 14, pyxel.COLOR_WHITE, pyxel.COLOR_BLACK),
      Button(self.width/2-34.5, self.height/2+28, 69, 14, pyxel.COLOR_WHITE, pyxel.COLOR_BLACK)
    )
    self.buttons[0].set_text("PLAY")
    self.buttons[0].set_action(lambda: self.load_level(self.levels[0]))
    self.buttons[1].set_text("BROWSE LEVELS")
    self.buttons[1].set_action(self.load_levels_menu)
    self.buttons[2].set_text("QUIT")
    self.buttons[2].set_action(pyxel.quit)

    self.config_button_focus()

    print_aligned_text(2, self.height-2, "by xkcm", pyxel.COLOR_NAVY, Align.LEFT | Align.BOTTOM)
    print_aligned_text(self.width-2, self.height-2, "1.0.0", pyxel.COLOR_ORANGE, Align.RIGHT | Align.BOTTOM)
  
  def load_levels_menu(self, page=1):
    pyxel.cls(0)
    n = 9
    n_per_page = n*(n-1)
    levels_count = len(self.levels)
    pages = ceil(levels_count/float(n_per_page))
    f = (page-1)*n_per_page
    t = f+n_per_page
    s = 5
    w = (self.width - (n+1)*s) / n
    buttons: list[Button] = []
    for i, level in enumerate(self.levels[f:t]):
      buttons.append(
        Button((i%n)*(s+w)+s, ((i)//n)*(s+w)+s, w, w, pyxel.COLOR_WHITE, pyxel.COLOR_BLACK)
      )
      buttons[-1].set_text(level.level_no)
      buttons[-1].set_action(lambda l=level: self.load_level(l))
    if pages > 1:
      page_buttons = 13
      page_buttons_spacing = 3
      page_button_width = (self.width - (page_buttons+1)*page_buttons_spacing) / page_buttons
      page_from = int(constrain(page - page_buttons/2+1, 1, pages))
      page_to = int(constrain(page_from + page_buttons-1, 1, pages))
      if page_to - page_from + 1 < page_buttons:
        page_from = int(constrain(page_to - page_buttons + 1, 1, pages))
      for i in range(page_from, page_to+1):
        buttons.append(
          Button(
            (i-page_from)*(page_buttons_spacing+page_button_width)+page_buttons_spacing,
            self.height - 2 - page_button_width,
            page_button_width,
            page_button_width,
            color=pyxel.COLOR_BLACK,
            text_color=pyxel.COLOR_WHITE,
            focus_color=pyxel.COLOR_BLACK,
            focus_text_color=pyxel.COLOR_DARKBLUE
          )
        )
        buttons[-1].set_text(i)
        buttons[-1].set_action(lambda p=i: self.load_levels_menu(p))
        if i == page: buttons[-1].set_text_color(pyxel.COLOR_PURPLE)
        print_aligned_text(3, self.height - 5 - page_button_width, f"PAGE {page}/{pages}", pyxel.COLOR_PURPLE, Align.LEFT | Align.BOTTOM)
    self.create_buttons(*buttons)
    self.config_button_focus(-n, n, -1, 1, 1)

  def load_level(self, level: Level):
    self.current_level = level
    self.current_level.load_level()
    self.level_state = State.INGAME
    self.init_components()

  def load_levels(self):
    self.levels = [
      Level01(),
      Level02()
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
        bottom_bar_edge = self.ball.check_rect_collision(self.bottom_bar)

        if edge == Edge.BOTTOM or (bottom_bar_edge != Edge.TOP and bottom_bar_edge is not None):
          return self.game_over()
        if bottom_bar_edge:
          print(f"Ball hit bottom_bar at {bottom_bar_edge}")
          self.ball.skew_angle_after_bottom_bar_collision(self.bottom_bar)

        if self.current_level.bricks_layout.size() == 0:
          return self.victory()
        
        self.current_level.bricks_layout.check_for_ball_collision(self.ball)
      
    if (self.level_state is not State.INGAME and self.current_level is not None) or self.current_level is None:
      if pyxel.btnr(pyxel.KEY_DOWN): self.change_button_focus(self.down_key_change)
      elif pyxel.btnr(pyxel.KEY_UP): self.change_button_focus(self.up_key_change)
      elif pyxel.btnr(pyxel.KEY_LEFT): self.change_button_focus(self.left_key_change)
      elif pyxel.btnr(pyxel.KEY_RIGHT): self.change_button_focus(self.right_key_change)
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
      for i, btn in enumerate(self.buttons):
        btn.unfocus()
        if i == self.button_focus:
          btn.focus()
      self.draw_buttons()
  
  def change_button_focus(self, val):
    self.button_focus += val
    buttons_count = len(self.buttons)
    if self.focus_index_overflow_behavior == 0:
      if self.button_focus < 0:
        self.button_focus = buttons_count - 1
      else:
        self.button_focus %= buttons_count
    elif self.focus_index_overflow_behavior == 1:
      if self.button_focus < 0:
        self.button_focus = 0
      elif self.button_focus >= buttons_count:
        self.button_focus = buttons_count - 1
  
  def create_buttons(self, *buttons):
    self.button_focus = 0
    self.buttons = list(buttons)
  
  def config_button_focus(self, up_key_change=-1, down_key_change=1, left_key_change=0, right_key_change=0, focus_index_overflow_behavior=0):
    self.left_key_change = left_key_change
    self.right_key_change = right_key_change
    self.up_key_change = up_key_change
    self.down_key_change = down_key_change
    self.focus_index_overflow_behavior = focus_index_overflow_behavior
  
  def game_over(self):
    self.level_state = State.FAILED
    pyxel.cls(0)

    ### LAYOUT [43 pixels height] 43 / 2 = 21.5
    # 5 pixels text [-21.5]
    # 5 pixels spacing [-16.5]
    # 14 pixels button [-11.5]
    # 5 pixels spacing [+2.5]
    # 14 pixels button [+7.5]
    #########################

    print_aligned_text(self.width/2, self.height/2-21.5, "GAME OVER", pyxel.COLOR_RED, Align.X_CENTER | Align.TOP)
    self.create_buttons(
      Button(self.width/2-25, self.height/2+pyxel.FONT_HEIGHT-11.5, 50, 14, pyxel.COLOR_WHITE, pyxel.COLOR_BLACK),
      Button(self.width/2-25, self.height/2+pyxel.FONT_HEIGHT+7.5, 50, 14, pyxel.COLOR_WHITE, pyxel.COLOR_BLACK)
    )
    self.buttons[0].set_text("PLAY AGAIN")
    self.buttons[0].set_action(self.play_again)
    self.buttons[1].set_text("MENU")
    self.buttons[1].set_action(self.show_main_menu)
    self.draw_buttons()
    self.config_button_focus()
  
  def victory(self):
    self.level_state = State.VICTORY
    pyxel.cls(0)

    ### LAYOUT [43 pixels height] 43 / 2 = 21.5
    # 5 pixels text [-21.5]
    # 5 pixels spacing [-16.5]
    # 14 pixels button [-11.5]
    # 5 pixels spacing [+2.5]
    # 14 pixels button [+7.5]
    #########################

    print_aligned_text(self.width/2, self.height/2-21.5, "CONGRATULATIONS, YOU WON!", pyxel.COLOR_GREEN, Align.X_CENTER | Align.TOP)
    self.create_buttons(
      Button(self.width/2 - 25, self.height/2-11.5, 50, 14, pyxel.COLOR_WHITE, pyxel.COLOR_BLACK),
      Button(self.width/2 - 25, self.height/2+7.5, 50, 14, pyxel.COLOR_WHITE, pyxel.COLOR_BLACK)
    )
    self.buttons[0].set_text("PLAY AGAIN")
    self.buttons[0].set_action(self.play_again)
    self.buttons[1].set_text("MENU")
    self.buttons[1].set_action(self.show_main_menu)
    self.draw_buttons()
    self.config_button_focus()

  def play_again(self):
    return self.load_level(self.current_level)

  def draw_buttons(self):
    for btn in self.buttons: btn.draw()

  def button_pressed(self):
    self.buttons[self.button_focus].pressed()


if __name__ == "__main__":
  app = App()
  app.run()
