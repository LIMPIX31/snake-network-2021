import pygame as pg
import numpy as np
import random
import json

pg.font.init()
f1 = pg.font.Font('font.ttf', 10)
f2 = pg.font.Font('font.ttf', 20)


class Sensors:
  def __init__(self,segments,food,ww,wh,window,winwidth,winheight,blockSize):
    self.ww = int(ww)
    self.wh = int(wh)
    self.gridBias = 10
    self.letSensor = []
    self.foodSensor = []
    self.window = window
    self.winw = winwidth
    self.winh = winheight
    self.blockSize = 40
    self.sensorSize = 5
    self.snb = 1
    self.tdir = [0,0,0,0]

    # self.N0 = np.zeros(((((self.sensorSize*2)+1)**2)*2+4+1 + self.snb,2))
    # self.N1 = np.zeros((121+self.snb,2))
    # self.N2 = np.zeros((16+self.snb,2))
    # self.N3 = np.zeros((4,2))

    self.W0 = np.zeros((11,11,4))
    self.W1 = np.zeros((11,11,4))

    self.W0[4][5][1] = 1

    # for i in range(len(self.W0)):
    #   for j in range(len(self.W0[i])):
    #     self.W0[i][j]= random.random()
    # for i in range(len(self.W1)):
    #   for j in range(len(self.W1[i])):
    #     self.W1[i][j]= random.random()
    # for i in range(len(self.W2)):
    #   for j in range(len(self.W2[i])):
    #     self.W2[i][j]= random.random()

  def init(self,segments,food):
    self.segments = segments
    self.food = food
    self.grid = []

    # self.weights = []
    # for i in range((self.sensorSize*2)+1):
    #   self.weights.append([])
    #   for j in range((self.sensorSize*2)+1):
    #     self.weights[i].append([0,0,0,0])
    # self.weightsLet = self.weights
    # self.weightsFood = self.weights


  def genGrid(self,save = False):
    grid = []
    for i in range(self.wh + self.gridBias*2):
      grid.append([])
      for j in range(self.ww  + self.gridBias*2):
        grid[i].append(0)
    
    letNum = -1
    foodNum = 1
    
    for a in range(self.wh):
      grid[a + self.gridBias][-1 + self.gridBias] = letNum
      grid[a + self.gridBias][self.wh + self.gridBias] = letNum
    for b in range(self.ww):
      grid[-1 + self.gridBias][b + self.gridBias] = letNum
      grid[self.ww + self.gridBias][b + self.gridBias] = letNum

    for c in range(len(self.segments)):
      grid[self.segments[c][1] + self.gridBias][self.segments[c][0] + self.gridBias] = letNum
    for d in range(len(self.food)):
      grid[self.food[d][1] + self.gridBias][self.food[d][0] + self.gridBias] = foodNum
    
    if save: self.grid = grid
    return grid

  def getSensor(self,stype,grid,pos):
    size = self.sensorSize
    sensor = []
    sensor = grid[((pos[1] + self.gridBias) - size):((pos[1] + self.gridBias) + size+1)]
    for i in range(len(sensor)):
      sensor[i] = sensor[i][(pos[0] + self.gridBias) - size : (pos[0] + self.gridBias) + size+1]
    for i in range(len(sensor)):
      for j in range(len(sensor[i])):
        if stype == 'let' and sensor[i][j] == 1:
          sensor[i][j] = 0
        elif stype == 'food' and sensor[i][j] == -1:
          sensor[i][j] = 0
        elif sensor[i][j] == -1:
            sensor[i][j] = 1
        else:
          pass
    return sensor

  def drawSensors(self,sensor,type):
    relx = 850
    rely = 50
    pg.draw.rect(self.window,(255,255,255),(relx,rely,self.blockSize*self.sensorSize*2,self.blockSize*self.sensorSize*2),1)
    for i in range(len(sensor)):
      for j in range(len(sensor[i])):
        rrelx = relx+(j*self.blockSize)
        rrely = rely+(i*self.blockSize)
        if sensor[i][j] != 0:
          pg.draw.rect(self.window,(255,255,0),(relx+(j*self.blockSize),rely+(i*self.blockSize),self.blockSize,self.blockSize))
        if type == 'let':
          wt1 = f1.render(str(int(self.W0[j][i][2])), 0, (80, 80, 80))
          wt2 = f1.render(str(int(self.W0[j][i][0])), 0, (80, 80, 80))
          wt3 = f1.render(str(int(self.W0[j][i][1])), 0, (80, 80, 80))
          wt4 = f1.render(str(int(self.W0[j][i][3])), 0, (80, 80, 80))
          self.window.blit(wt1, (rrelx + (self.blockSize/2)-3, rrely))
          self.window.blit(wt2, (rrelx+7, rrely + (self.blockSize/2)-8))
          self.window.blit(wt3, (rrelx+self.blockSize-12, rrely + (self.blockSize/2)-8))
          self.window.blit(wt4, (rrelx + (self.blockSize/2)-3, rrely+self.blockSize-15))
        elif type == 'food':
          wt1 = f1.render(str(int(self.W1[j][i][2])), 0, (80, 80, 80))
          wt2 = f1.render(str(int(self.W1[j][i][0])), 0, (80, 80, 80))
          wt3 = f1.render(str(int(self.W1[j][i][1])), 0, (80, 80, 80))
          wt4 = f1.render(str(int(self.W1[j][i][3])), 0, (80, 80, 80))
          self.window.blit(wt1, (rrelx + (self.blockSize/2)-3, rrely))
          self.window.blit(wt2, (rrelx+7, rrely + (self.blockSize/2)-8))
          self.window.blit(wt3, (rrelx+self.blockSize-12, rrely + (self.blockSize/2)-8))
          self.window.blit(wt4, (rrelx + (self.blockSize/2)-3, rrely+self.blockSize-15))
        
        pg.draw.rect(self.window,(127,127,127),(rrelx,rrely,self.blockSize,self.blockSize),1)
        


  def getNeuralMove(self,sensor1,sensor2,dir):

    left = 0
    right = 0
    up = 0
    down = 0


    for i in range(len(sensor1)):
      for j in range(len(sensor1[i])):
        if sensor1[i][j] == 1:
          left += int(self.W0[j][i][0])
          right += int(self.W0[j][i][1])
          up += int(self.W0[j][i][2])
          down += int(self.W0[j][i][3])
    for i in range(len(sensor2)):
      for j in range(len(sensor2[i])):
        if sensor2[i][j] == 1:
          left += int(self.W1[j][i][0])
          right += int(self.W1[j][i][1])
          up += int(self.W1[j][i][2])
          down += int(self.W1[j][i][3])
    sdir=[left,right,up,down]
    sdir0 = [0,0,0,0]

    maxsdir = max(sdir)
    if sdir[0] == maxsdir:
      sdir0[0] = 1
    if sdir[1] == maxsdir:
      sdir0[1] = 1
    if sdir[2] == maxsdir:
      sdir0[2] = 1
    if sdir[3] == maxsdir:
      sdir0[3] = 1

    a = 0
    for i in range(3):
      a += sdir0[i]
    if a > 1:
      while a != 1:
        rand = random.randint(0,3)
        if sdir0[rand] == 1:
          sdir0[rand] = 0
          a -= 1
      

    if sdir0[dir] != 1:
      self.setWeights(1,sensor1,sensor2,dir)
      self.setWeights(0,sensor1,sensor2,sdir0.index(1))

      

    

    
  def setWeights(self,p,sensor1,sensor2,dir):
    for i in range(len(sensor1)):
      for j in range(len(sensor1[i])):
        if sensor1[i][j] == 1:
          if p == 0:
            self.W0[j][i][dir] -= 1
          elif p == 1:
            self.W0[j][i][dir] += 1
    for i in range(len(sensor2)):
      for j in range(len(sensor2[i])):
        if sensor2[i][j] == 1:
          if p == 0:
            self.W1[j][i][dir] -= 1
          elif p == 1:
            self.W1[j][i][dir] += 1



  def drawNeuralMove(self,res,sensor1,sensor2):
    left = 0
    right = 0
    up = 0
    down = 0

    for i in range(len(sensor1)):
      for j in range(len(sensor1[i])):
        if sensor1[i][j] == 1:
          left += int(self.W0[j][i][0])
          right += int(self.W0[j][i][1])
          up += int(self.W0[j][i][2])
          down += int(self.W0[j][i][3])
    for i in range(len(sensor2)):
      for j in range(len(sensor2[i])):
        if sensor2[i][j] == 1:
          left += int(self.W1[j][i][0])
          right += int(self.W1[j][i][1])
          up += int(self.W1[j][i][2])
          down += int(self.W1[j][i][3])


    self.RCW()

    resmax = max([left,right,up,down])
    if resmax == left:
      pg.draw.rect(self.window,(50,0,255),(985,565,60,60))
    if resmax == right:
      pg.draw.rect(self.window,(50,0,255),(1115,565,60,60))
    if resmax == up:
      pg.draw.rect(self.window,(50,0,255),(1050,500,60,60))
    if resmax == down:
      pg.draw.rect(self.window,(50,0,255),(1050,630,60,60))

    pg.draw.rect(self.window,(255,255,255),(1050,500,60,60),2)
    pg.draw.rect(self.window,(255,255,255),(985,565,60,60),2)
    pg.draw.rect(self.window,(255,255,255),(1050,630,60,60),2)
    pg.draw.rect(self.window,(255,255,255),(1115,565,60,60),2)

    keys = keys = pg.key.get_pressed()
    if keys[pg.K_a] and self.tdir[0] == 0:
      self.tdir[0] = 1
      pg.draw.rect(self.window,(255,0,0),(985,565,60,60),3)
    elif keys[pg.K_a] and self.tdir[0] == 1:
      self.tdir[0] = 0
    if keys[pg.K_d] and self.tdir[1] == 0:
      self.tdir[1] = 1
      pg.draw.rect(self.window,(255,0,0),(1115,565,60,60),3)
    elif keys[pg.K_d] and self.tdir[1] == 1:
      self.tdir[1] = 0
    if keys[pg.K_w] and self.tdir[2] == 0:
      self.tdir[2] = 1
      pg.draw.rect(self.window,(255,0,0),(1050,500,60,60),3)
    elif keys[pg.K_w] and self.tdir[2] == 1:
      self.tdir[2] = 0
    if keys[pg.K_s] and self.tdir[3] == 0:
      self.tdir[3] = 1
      pg.draw.rect(self.window,(255,0,0),(1050,630,60,60),3)
    elif keys[pg.K_s] and self.tdir[3] == 1:
      self.tdir[3] = 0
    if self.tdir[0] == 1:
      pg.draw.rect(self.window,(255,0,0),(985,565,60,60),3)
    if self.tdir[1] == 1:
      pg.draw.rect(self.window,(255,0,0),(1115,565,60,60),3)
    if self.tdir[2] == 1:
      pg.draw.rect(self.window,(255,0,0),(1050,500,60,60),3)
    if self.tdir[3] == 1:
      pg.draw.rect(self.window,(255,0,0),(1050,630,60,60),3)

    upt = f2.render(str(up),0,(255,255,255))
    leftt = f2.render(str(left),0,(255,255,255))
    rightt = f2.render(str(right),0,(255,255,255))
    downt = f2.render(str(down),0,(255,255,255))

    self.window.blit(upt,(1060,518))
    self.window.blit(leftt,(995,582))
    self.window.blit(rightt,(1128,582))
    self.window.blit(downt,(1060,645))

    return [left,right,up,down]

  def RCW(self):
    self.W0[5][5] = [0,0,0,0]
    self.W1[5][5] = [0,0,0,0]

  def neuralMove(self,res):
    maxres = max(res)
    if res[0]==maxres:
      return 'left'
    if res[1]==maxres:
      return 'right'
    if res[2]==maxres:
      return 'up'
    if res[3]==maxres:
      return 'down'
    self.W0[random.randint(0,11)][random.randint(0,11)][random.randint(0,4)] += random.randint(-5,5)
    self.W1[random.randint(0,11)][random.randint(0,11)][random.randint(0,4)] += random.randint(-5,5)