import pyxel
from components.Rect import Rect
import utils

class Button(Rect):
  def __init__(self, x, y, w, h, color, focus_text_color, text_color=None, focus_color=None) -> None:
    super().__init__(x, y, w, h)
    self.text = ""
    self.color = color
    self.focus_text_color = focus_text_color
    self.focus_color = focus_color or self.color
    self.text_color = text_color or self.color
    self.focused = False
    self.action = None
  
  def set_text(self, text):
    self.text = text
  
  def set_action(self, action):
    self.action = action
  
  def set_color(self, color):
    self.color = color
  
  def set_text_color(self, text_color):
    self.text_color = text_color

  def set_focus_color(self, color):
    self.focus_color = color
  
  def set_focus_text_color(self, text_color):
    self.focus_text_color = text_color
  
  def draw(self):
    if not self.focused:
      pyxel.rectb(self.x, self.y, self.width, self.height, self.color)
      text_color = self.text_color
    else:
      pyxel.rect(self.x, self.y, self.width, self.height, self.focus_color)
      text_color = self.focus_text_color
    utils.print_centered_text(self.x+self.width/2, self.y+self.height/2, self.text, text_color)

  def focus(self):
    self.focused = True
  
  def unfocus(self):
    super().draw(pyxel.COLOR_BLACK)
    self.focused = False
  
  def pressed(self):
    self.action()
    
  
