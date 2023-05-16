import pygame as pg
import numpy as np
import colorama as cr
import sensors
from game import *
import json

cr.init()

winwidth = 1350
winheight = 800

window = pg.display.set_mode((winwidth,winheight))
pg.display.set_caption("Neural Network for SnakeGame")
icon = pg.image.load('icon.png')
pg.display.set_icon(icon)
clock = pg.time.Clock()


# vars
width = 800
height = 800
blockSize = 20
ww = width / blockSize
wh = height / blockSize
crr = [0,0]
pd = 'right'
defSegments=[
  [10,10],
  [11,10],
  [12,10],
  [13,10],
  [14,10]
]
segments = defSegments
defFood = [[16,10]]
food = defFood
file = 'bots/1.json'

sgame = Game(window,segments,food,blockSize,crr,pd,ww,wh)



sns = sensors.Sensors(segments,food,ww,wh,window,winwidth,winheight,blockSize)


def game():
  runs = 0
  run = True
  drawMode = 'let'
  res = [0,0,0,0]
  working = False
  while run:
    runs += 1
    for e in pg.event.get():
      if e.type == pg.QUIT:
        run = False
        pg.quit()
        quit()
    window.fill((255,255,255))
    pg.draw.rect(window,(0,0,0),(0,0,winwidth,winheight))
    pg.draw.rect(window,(255,255,255),(0,0,800,800),1)

    sns.init(sgame.segments,sgame.food)
    sns.drawSensors(sns.getSensor(drawMode,sns.genGrid(),sgame.segments[-1]),drawMode)
    res = sns.drawNeuralMove(res,sns.getSensor('let',sns.genGrid(),sgame.segments[-1]),sns.getSensor('food',sns.genGrid(),sgame.segments[-1]))

    keys = pg.key.get_pressed()
    sgame.draw()
    if keys[pg.K_LEFT]:
      sns.getNeuralMove(sns.getSensor('let',sns.genGrid(),sgame.segments[-1]),sns.getSensor('food',sns.genGrid(),sgame.segments[-1]),0)
      sgame.moveLeft()
    if keys[pg.K_RIGHT]:
      sns.getNeuralMove(sns.getSensor('let',sns.genGrid(),sgame.segments[-1]),sns.getSensor('food',sns.genGrid(),sgame.segments[-1]),1)
      sgame.moveRight()
    if keys[pg.K_UP]:
      sns.getNeuralMove(sns.getSensor('let',sns.genGrid(),sgame.segments[-1]),sns.getSensor('food',sns.genGrid(),sgame.segments[-1]),2)
      sgame.moveUp()
    if keys[pg.K_DOWN]:
      sns.getNeuralMove(sns.getSensor('let',sns.genGrid(),sgame.segments[-1]),sns.getSensor('food',sns.genGrid(),sgame.segments[-1]),3)
      sgame.moveDown()
    if keys[pg.K_l]:
      drawMode = 'let'
    if keys[pg.K_f]:
      drawMode = 'food'
    
    nmove = sns.neuralMove(res)
    if keys[pg.K_g]:
      sgame.setFood()
    
    if keys[pg.K_r]:
      working = True
    else:
      working = False
    if working == True:
      if nmove == 'left':
        sgame.moveLeft()
      elif nmove == 'right':
        sgame.moveRight()
      elif nmove == 'up':
        sgame.moveUp()
      elif nmove == 'down':
        sgame.moveDown()

    if keys[pg.K_n]:
      jsw = {
        "weightsLet":sns.W0.tolist(),
        "weightsFood":sns.W1.tolist()
      }


      with open(file,'w') as sw:
        json.dump(jsw,sw)
    if keys[pg.K_p]:
      with open(file,'r') as sw:
        gsw = json.load(sw)
        sns.W0 = np.array(gsw['weightsLet'])
        sns.W1 = np.array(gsw['weightsFood'])

    
    sgame.draw()
    pg.display.update()
    clock.tick(10)
    





game()


