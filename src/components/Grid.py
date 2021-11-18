
from components.Ball import Ball
from components.Brick import Brick


class Grid:
  def __init__(self) -> None:
    self.bricks: list[Brick] = []
  
  def append_bricks(self, *bricks):
    self.bricks += list(bricks)
  
  def set_bricks(self, *bricks):
    self.bricks = list(bricks)
  
  def clear_bricks(self):
    self.bricks = []
    
  def draw(self):
    for brick in self.bricks:
      brick.draw()
  
  def destroy_brick(self, brick):
    self.bricks.remove(brick)

  def size(self):
    return len(self.bricks)

  def check_for_ball_collision(self, ball: Ball):
    for brick in self.bricks:
      collided = ball.check_rect_collision(brick)
      if (collided):
        brick_health = brick.was_hit(collided)
        if brick_health == 0: self.destroy_brick(brick)
