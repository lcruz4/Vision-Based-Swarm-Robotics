from connSetup import *
import sys
from math import *
import time
import motor

#This function initializes the communication sockets, receives the task,
#calculates the destination points, flashes led sequence and returns the
#calculated points
def initialize():
  ret = []
  msg = connDict['c'][0].recv(99)	#no timeout
  print("task received "+msg)#DEBUG
  task = msg.split()		#should be "circle x,y radius"
  task[2] = int(task[2])

  if(task[0] == "circle"):
    radslice = (360/iplen)*(pi/180)
    center = task[1].split(",")
    center[0] = int(center[0])
    center[1] = int(center[1])
    for i in range(iplen):
      dx = task[2]*cos(i*radslice)
      dy = task[2]*sin(i*radslice)
      ret.append([int(center[0]+dx),int(center[1]+dy)])
  print("points calculated:")#DEBUG
  print(ret)#DEBUG
  flashSeq()
  return ret

#calculates led sequence using the last byte of the robot's IP address
#and flashes the sequence at XHz
def flashSeq():
  s = myIP.split(".")
  seq = int(s[-1])
  print("mySeq "+str(seq))#DEBUG
  bit = 0
  motor.ledOn()
  time.sleep(0.5)
  motor.ledOff()
  t = time.time()
  while(bit<8):
    weight = 128>>bit
    if(seq>=weight):
      seq = seq - weight
      motor.ledOn()
      time.sleep(0.5 - (time.time()-t))
    else:
      motor.ledOff()
      time.sleep(0.5 - (time.time()-t))
    t = time.time()
    bit = bit + 1
  motor.ledOff()

#calculates the average distance of the robot calling the function. This
#function takes in the list of destination points and the location of the
#calling robot. This function will call shareAvgDist which communicates the
#calling robot's average distance and then returns a list of all the robots'
#average distances. It then checks if the calling robot's avg distance is the
#max avgerage distance and returns the closest point to that robot if it is.
#otherwise it returns [-1,-1]
def maxAvgDist(pnts,loc):
  distTot = 0
  minPnt = [XMAX,YMAX]
  for p in pnts:
    xdist = fabs(p[0] - loc[0])
    ydist = fabs(p[1] - loc[1])
    dist = sqrt(pow(xdist,2)+pow(ydist,2))
    minDist = sqrt(pow(minPnt[0],2)+pow(minPnt[1],2))
    distTot = distTot + dist
    if(dist < minDist):
      minPnt = [int(p[0]),int(p[1])]

  avgDist = distTot/len(pnts)
  print("avgDist "+str(avgDist))#DEBUG
  distList = shareAvgDist(avgDist)
  print("DistList ")#DEBUG
  print(distList)#DEBUG
  if(int(avgDist)==max(distList)):
    return minPnt
  else:
    return [-1,-1]

#waits for the vision system to send the robot its location and returns it.
def getLoc():
  while(1):
    try:
      msg = connDict['c'][0].recv(99)
      msg = msg.split()
      locxy,angle = msg[-1].split(':')
      listxy= locxy.split(',')
      listxy[0] = int(listxy[0])
      listxy[1] = int(listxy[1])
      listxy.append(int(angle))
      return listxy
    except:
      pass

#moves the robot forward at the given velocity
def goForward(vel):
  #motor.forward(vel)
  print("GOING FORWARD!!")

#stops the robot
def goStop():
  #motor.stop()
  print("STOP!!")

def pivotRight():
  print("PIVOT RIGHT!!!")

def pivotLeft():
  print("PIVOT LEFT!!!")

#sets all the server sockets' timeouts to the given timeout
def setTimeouts(timeout):
  for soc in connDict:
    connDict[soc][0].settimeout(timeout)

#Shares the number value provided with all other robots. Returns a list of
#all the robots' values.
def shareAvgDist(dist):
  lDist = []
  dist = str(int(dist))
  lDist.append(int(dist))
  distList = []
  distList.append(int(dist))
  nameList = [name for name in connDict]
  nameList.remove('c')
#  print("len connDict:%d\nlen nameList:%d",%(len(connDict),len(nameList)))
  done = False
  count = 0

  while(not done):
    if(len(distList)==len(connDict)):
      done = True
      print("Done sharing avgDist")#DEBUG
      for soc in csoc:
        csoc[soc].send("done ".encode())
        for dist in distList:
          csoc[soc].send((str(dist)+" ").encode())
    else:
      for dist in distList:
        csoc[nameList[count%len(nameList)]].send((str(dist)+" ").encode())

    for soc in connDict:
      try:
        if(soc != 'c'):
          sDist = connDict[soc][0].recv(99)
          lDist = sDist.split()
      except:
        pass
      if("done" in lDist):
        lDist.remove("done")
        for dist in lDist:
          if(not (int(dist) in distList)):
            distList.append(int(dist))
        while(len(distList)<len(connDict)):
          try:
            if(soc != 'c'):
              sDist = connDict[soc][0].recv(99)
              lDist = sDist.split()
              for dist in lDist:
                if(not (int(dist) in distList)):
                  distList.append(int(dist))
          except:
            pass
        done = True
        break
      else:
        for dist in lDist:
          if(not (int(dist) in distList)):
            distList.append(int(dist))
    print(distList)#DEBUG
    count = count + 1
  return distList

#Takes in a list of paths containing an initial and destination point, it
#also takes the calling robot's location (inital point) and destination
#It figures out the linear path of the robot given the two points and checks
#for intersections with any other path. If an intersection occurs it is saved
#in a dictionary indexed by the robot's name and returns that dictionary
def checkPaths(paths,i,f):
  m = (f[1]-i[1])/(f[0]-i[0])
  b = i[1]-m*i[0]
  ret = {}
  for name in paths:
    try:	#in case of divide by zero errors
      mi = ((paths[name][1][1]-paths[name][0][1])/
          (paths[name][1][0]-paths[name][0][0]))
      bi = paths[name][0][1]-mi*paths[name][0][0]
      X = (b-bi)*(1/(mi-m))
      Y = m*X + b
      if(X>=min([i[0],f[0]]) and X<=max([i[0],f[0]]) and
          Y>=min([i[1],f[1]]) and Y<=max([i[1],f[1]])):
        ret[name]=[int(X),int(Y)]
        print("Intersection with "+name+" at:")#DEBUG
        print(ret[name])#DEBUG
    except:
      pass

  return ret
