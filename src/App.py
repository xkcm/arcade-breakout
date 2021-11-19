
from math import ceil, pi
from random import choice, random
import pyxel

from components.Ball import Ball
from components.BottomBar import BottomBar
from components.Brick import Brick
from components.Button import Button
from components.Level import Level, State
from components.PowerUp import PowerUp, PowerUpType
from components.Rect import Edge
from levels.Level01 import Level01
from levels.Level02 import Level02
from utils import Align, constrain, print_aligned_text, random_color, round_angle


class App:

  # static properties
  FPS = 60
  WIDTH = 256
  HEIGHT = 256
  VERSION = "1.0.0"


  def __init__(self) -> None:

    self.levels: list[Level] = []
    self.current_level: Level = None
    self.level_state = State.OUTGAME

    self.button_focus = 0
    self.buttons: list[Button] = []
    self.config_button_focus()

    self.power_ups: list[PowerUp] = []
    self.balls: list[Ball] = []

    pyxel.init(App.WIDTH, App.HEIGHT, fps=App.FPS, scale=3, caption="Breakout")
    pyxel.load("../resources.pyxres")

    self.init_components()
    self.load_levels()

  def run(self):
    self.show_main_menu()
    pyxel.run(self.update, self.draw)

  def show_main_menu(self):
    pyxel.cls(0)

    ### LAYOUT [65 pixels height] 46 / 2 = 23
    # 8 pixels "ARCADE BREAKOUT" [-23]
    # 5 pixels spacing [-15]
    # 14 pixels button [-10]
    # 5 pixels spacing [+4]
    # 14 pixels button [+9]
    # 5 pixels spacing [+14]
    # 14 pixels button [+28]
    #############################

    pyxel.blt(App.WIDTH/2-34.5, App.HEIGHT/2-23, 0, 0, 0, 69, 8)
    self.create_buttons(
      Button(App.WIDTH/2-34.5, App.HEIGHT/2-10, 69, 14, pyxel.COLOR_WHITE, pyxel.COLOR_BLACK),
      Button(App.WIDTH/2-34.5, App.HEIGHT/2+9, 69, 14, pyxel.COLOR_WHITE, pyxel.COLOR_BLACK),
      Button(App.WIDTH/2-34.5, App.HEIGHT/2+28, 69, 14, pyxel.COLOR_WHITE, pyxel.COLOR_BLACK)
    )
    self.buttons[0].set_text("PLAY")
    self.buttons[0].set_action(lambda: self.load_level(self.levels[0]))
    self.buttons[1].set_text("BROWSE LEVELS")
    self.buttons[1].set_action(self.load_levels_menu)
    self.buttons[2].set_text("QUIT")
    self.buttons[2].set_action(pyxel.quit)

    self.config_button_focus()

    print_aligned_text(2, App.HEIGHT-2, "by xkcm", pyxel.COLOR_NAVY, Align.LEFT | Align.BOTTOM)
    print_aligned_text(App.WIDTH-2, App.HEIGHT-2, App.VERSION, pyxel.COLOR_ORANGE, Align.RIGHT | Align.BOTTOM)
  
  def load_levels_menu(self, page=1):
    pyxel.cls(0)
    n = 9
    n_per_page = n*(n-1)
    levels_count = len(self.levels)
    pages = ceil(levels_count/float(n_per_page))
    f = (page-1)*n_per_page
    t = f+n_per_page
    s = 5
    w = (App.WIDTH - (n+1)*s) / n
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
      page_button_width = (App.WIDTH - (page_buttons+1)*page_buttons_spacing) / page_buttons
      page_from = int(constrain(page - page_buttons/2+1, 1, pages))
      page_to = int(constrain(page_from + page_buttons-1, 1, pages))
      if page_to - page_from + 1 < page_buttons:
        page_from = int(constrain(page_to - page_buttons + 1, 1, pages))
      for i in range(page_from, page_to+1):
        buttons.append(
          Button(
            (i-page_from)*(page_buttons_spacing+page_button_width)+page_buttons_spacing,
            App.HEIGHT - 2 - page_button_width,
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
        print_aligned_text(3, App.HEIGHT - 5 - page_button_width, f"PAGE {page}/{pages}", pyxel.COLOR_PURPLE, Align.LEFT | Align.BOTTOM)
    self.create_buttons(*buttons)
    self.config_button_focus(-n, n, -1, 1, 1)

  def load_level(self, level: Level):
    self.current_level = level
    self.current_level.bricks_layout.clear_bricks()
    self.current_level.load_level()
    self.level_state = State.INGAME
    self.init_components()

  def load_levels(self):
    self.levels = [
      Level01(),
      Level02()
    ]

  def spawn_power_up(self, type: PowerUpType, spawn_pos: list[int]):

    action = None
    action_on_end = None

    if type is PowerUpType.BAR_EXTENSION:
      action = lambda: self.bottom_bar.set_width(BottomBar.DEFAULT_WIDTH*2)
      action_on_end = lambda: self.bottom_bar.set_width()
    elif type is PowerUpType.TRIPLE_BALL:
      def spawn_3_balls():
        for _ in range(3):
          random_ball = choice(self.balls)
          new_ball = self.spawn_ball(random_ball.x, random_ball.y, color=random_color(exclude=["COLOR_BLACK"]))
          random_angle = round_angle(random()*2*pi, 12, 2*pi)-pi
          if random_angle == 0 or random_angle == pi or random_angle == -pi:
            random_angle = choice([-pi/2, pi/2])
          new_ball.v.set_angle(random_angle)
      action = spawn_3_balls
    elif type is PowerUpType.SLOW_DOWN:
      action = lambda: self.bottom_bar.set_speed(BottomBar.DEFAULT_SPEED/2)
      action_on_end = lambda: self.bottom_bar.set_speed()
    elif type is PowerUpType.SPEED_UP:
      action = lambda: self.bottom_bar.set_speed(BottomBar.DEFAULT_SPEED*2)
      action_on_end = lambda: self.bottom_bar.set_speed()
    
    power_up = PowerUp.spawn(type, spawn_pos, (action, action_on_end))
    self.power_ups.append(power_up)

  def clear_power_ups(self):
    self.power_ups = []
  
  def spawn_ball(self, x, y, vx=None, vy=None, color=pyxel.COLOR_WHITE):
    if vx is None and vy is None:
      pass
    new_ball = Ball(x=x, y=y, color=color)
    self.balls.append(new_ball)
    return new_ball

  def check_balls(self):
    pass
  
  def clear_balls(self):
    self.balls: list[Ball] = []

  def init_components(self):
    self.bottom_bar = BottomBar(height=5)
    
    self.clear_balls()
    self.spawn_ball(self.bottom_bar.x+self.bottom_bar.width/2, self.bottom_bar.y-3, -Ball.DEFAULT_SPEED, 0, pyxel.COLOR_WHITE)
    self.clear_power_ups()

  def update(self):
    if self.current_level is not None:
      if self.level_state == State.INGAME:
        if pyxel.btn(pyxel.KEY_LEFT): self.bottom_bar.move_left()
        if pyxel.btn(pyxel.KEY_RIGHT): self.bottom_bar.move_right()
        
        for power_up in self.power_ups:
          if power_up.update(self.bottom_bar):
            self.power_ups.remove(power_up)

        for ball in self.balls:
          edge = ball.update()
          bottom_bar_edge = ball.check_rect_collision(self.bottom_bar)

          if edge is not None:
            pyxel.play(0, 0)
          if edge == Edge.BOTTOM:
            self.balls.remove(ball)
          if len(self.balls) == 0:
            return self.game_over()
          if bottom_bar_edge == Edge.TOP:
            ball.skew_angle_after_bottom_bar_collision(self.bottom_bar)

          collision_status, collision_brick = self.current_level.bricks_layout.check_for_ball_collision(ball)
          if collision_status == 1:
            pyxel.play(0, 0)
          if collision_status == 2:
            pyxel.play(0, 4)
            if random() < self.current_level.chance_of_power_up:
              self.spawn_power_up(PowerUp.random(), [collision_brick.x+collision_brick.width/2, collision_brick.y+collision_brick.height/2])

        if self.current_level.bricks_layout.size() == 0:
          return self.victory()
        
        
      
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
        self.current_level.bricks_layout.draw()

        for ball in self.balls:
          ball.draw()

        for power_up in self.power_ups:
          power_up.draw()
        
        print_aligned_text(2, self.bottom_bar.y-6-pyxel.FONT_HEIGHT*2, f"Power-up probability: {self.current_level.chance_of_power_up}", pyxel.COLOR_ORANGE, Align.LEFT | Align.BOTTOM)
        print_aligned_text(2, self.bottom_bar.y-4-pyxel.FONT_HEIGHT, f"Difficulty: {self.current_level.difficulty.name}", pyxel.COLOR_RED, Align.LEFT | Align.BOTTOM)
        print_aligned_text(2, self.bottom_bar.y-2, f"Level {self.current_level.level_no}", pyxel.COLOR_WHITE, Align.LEFT | Align.BOTTOM)
    
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
    pyxel.play(0, 2)
    pyxel.cls(0)

    ### LAYOUT [43 pixels height] 43 / 2 = 21.5
    # 5 pixels text [-21.5]
    # 5 pixels spacing [-16.5]
    # 14 pixels button [-11.5]
    # 5 pixels spacing [+2.5]
    # 14 pixels button [+7.5]
    #########################

    print_aligned_text(App.WIDTH/2, App.HEIGHT/2-21.5, "GAME OVER", pyxel.COLOR_RED, Align.X_CENTER | Align.TOP)
    self.create_buttons(
      Button(App.WIDTH/2-25, App.HEIGHT/2+pyxel.FONT_HEIGHT-11.5, 50, 14, pyxel.COLOR_WHITE, pyxel.COLOR_BLACK),
      Button(App.WIDTH/2-25, App.HEIGHT/2+pyxel.FONT_HEIGHT+7.5, 50, 14, pyxel.COLOR_WHITE, pyxel.COLOR_BLACK)
    )
    self.buttons[0].set_text("PLAY AGAIN")
    self.buttons[0].set_action(self.play_again)
    self.buttons[1].set_text("MENU")
    self.buttons[1].set_action(self.show_main_menu)
    self.draw_buttons()
    self.config_button_focus()
  
  def victory(self):
    self.level_state = State.VICTORY
    pyxel.play(0, 3)
    pyxel.cls(0)

    ### LAYOUT [43 pixels height] 43 / 2 = 21.5
    # 5 pixels text [-21.5]
    # 5 pixels spacing [-16.5]
    # 14 pixels button [-11.5]
    # 5 pixels spacing [+2.5]
    # 14 pixels button [+7.5]
    #########################

    print_aligned_text(App.WIDTH/2, App.HEIGHT/2-21.5, "CONGRATULATIONS, YOU WON!", pyxel.COLOR_GREEN, Align.X_CENTER | Align.TOP)
    self.create_buttons(
      Button(App.WIDTH/2 - 25, App.HEIGHT/2-11.5, 50, 14, pyxel.COLOR_WHITE, pyxel.COLOR_BLACK),
      Button(App.WIDTH/2 - 25, App.HEIGHT/2+7.5, 50, 14, pyxel.COLOR_WHITE, pyxel.COLOR_BLACK)
    )
    next_index = self.next_level_index()
    if next_index is None:
      self.buttons[0].set_text("PLAY AGAIN")
      self.buttons[0].set_action(self.play_again)
    else:
      self.buttons[0].set_text("NEXT LEVEL")
      self.buttons[0].set_action(lambda: self.load_level(self.levels[next_index]))  
    self.buttons[1].set_text("MENU")
    self.buttons[1].set_action(self.show_main_menu)
    self.draw_buttons()
    self.config_button_focus()

  def play_again(self):
    return self.load_level(self.current_level)

  def next_level_index(self):
    index = self.levels.index(self.current_level)
    if index + 1 >= len(self.levels): return None
    return index + 1

  def draw_buttons(self):
    for btn in self.buttons: btn.draw()

  def button_pressed(self):
    self.buttons[self.button_focus].pressed()


if __name__ == "__main__":
  app = App()
  app.run()
