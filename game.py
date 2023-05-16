import pygame as pg
import random

class Game:

  def __init__(self,window,segments,food,blockSize,crr,pd,ww,wh):
    self.window = window
    self.segments = segments
    self.defSegments = segments
    self.food = food
    self.defFood = food
    self.blockSize = blockSize
    self.crr = crr
    self.pd = pd
    self.ww = ww
    self.wh = wh
    self.score = 0


  def setBlock(self,x,y,color=(0,0,255)):
    pg.draw.rect(self.window, color, ((x * self.blockSize) + self.crr[0], (y * self.blockSize) + self.crr[1], self.blockSize, self.blockSize))

  def draw(self):
    for i in range(len(self.segments)):
      self.setBlock(self.segments[i][0], self.segments[i][1])
    for i in range(len(self.food)):
      self.setBlock(self.food[i][0], self.food[i][1], color=(0,255,0))

  def anyMove(self,direction):
    old = self.segments.pop(0)
    head = self.segments[len(self.segments) - 1]
    if direction == 'left':
      self.segments.append([head[0] - 1, head[1]])
    elif direction == 'right':
      self.segments.append([head[0] + 1, head[1]])
    elif direction == 'up':
      self.segments.append([head[0], head[1] - 1])
    elif direction == 'down':
      self.segments.append([head[0], head[1] + 1])
  def move(self,nd):
    if nd == 'left':
      self.anyMove('left')
      self.pd = 'left'
    if nd == 'right':
      self.anyMove('right')
      self.pd = 'right'
    if nd == 'up':
      self.anyMove('up')
      self.pd = 'up'
    if nd == 'down':
      self.anyMove('down')
      self.pd = 'down'
    cl = self.onCollision()
    if cl == 'wall':
      self.gameOver()
    elif cl == 'self':
      self.gameOver()
    elif cl == 'food':
      self.score += 1
      self.food.pop(self.food.index(self.segments[len(self.segments) - 1]))
      print(self.score)
      # self.setFood()
      self.addSegment(self.pd)

  def moveLeft(self):
    self.move('left')
  def moveRight(self):
    self.move('right')
  def moveUp(self):
    self.move('up')
  def moveDown(self):
    self.move('down')
  


  def onCollision(self):
    head = self.segments[len(self.segments) - 1]
    for i in range(len(self.segments) - 1):
      if (self.segments[i][0] == head[0]) and (self.segments[i][1] == head[1]):
        return 'self'
    if ((head[0] == -1) or (head[0] == self.ww)) or ((head[1] == -1) or (head[1] == self.wh)):
      return 'wall'
    for i in range(len(self.food)):
      if (self.food[i][0] == head[0]) and (self.food[i][1] == head[1]):
        return 'food'
  
  def setFood(self,isRandom = True,x = 0, y = 0):
    x = random.randint(0,self.ww - 1)
    y = random.randint(0,self.wh - 1)
    ok = 0
    while ok != len(self.segments)+len(self.food):
      for i in range(len(self.segments)):
        if x == self.segments[i][0] and y == self.segments[i][1]:
          x = random.randint(0,self.ww - 1)
          y = random.randint(0,self.wh - 1)
        else:
          ok += 1
      for i in range(len(self.food)):
        if x == self.food[i][0] and y == self.food[i][0]:
          x = random.randint(0,self.ww - 1)
          y = random.randint(0,self.wh - 1)
        else:
          ok += 1
        
    self.food.append([x,y])

  def addSegment(self,dir):
    old = self.segments[0]
    if dir == 'left':
      self.segments.insert(0,[old[0] - 1, old[1]])
    elif dir == 'right':
      self.segments.insert(0,[old[0] + 1, old[1]])
    elif dir == 'up':
      self.segments.insert(0,[old[0], old[1] - 1])
    elif dir == 'down':
      self.segments.insert(0,[old[0], old[1] + 1])

  def gameOver(self):
    self.score = 0
    print("gameOver")
    self.segments = [
      [10,10],
      [11,10],
      [12,10],
      [13,10],
      [14,10]
    ]   
    self.food = [[16,10]]
    self.draw()
  

  def returnSegments():
    return self.segments
  def returnFood():
    return self.food