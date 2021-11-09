
class Grid:
  def __init__(self) -> None:
    self.bricks = []
  
  def appendBricks(self, *bricks):
    print(bricks)
    for brick in bricks:
      self.bricks.append(brick)
    
  def draw(self):
    for brick in self.bricks:
      brick.draw()
  
  def destroyBrick(self, brick):
    self.bricks.remove(brick)

  def checkForBallCollision(self, ball):
    for brick in self.bricks:
      collided = ball.checkRectCollision(brick)
      if (collided):
        brickHealth = brick.wasHit(collided)
        if brickHealth == 0: self.destroyBrick(brick)
