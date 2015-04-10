from connSetup import *
import sys
from math import *
import motor

def intialize():
  ret = []
  msg = connDict['c'][0].recv(99)	#no timeout
  task = msg.split()		#should be "circle x,y radius"
  task[2] = int(task[2])

  if(task[0] == "circle"):
    radslice = (360/iplen)*(pi/180)
    center = task[1].split(",")
    center[0] = int(center[0])
    center[1] = int(center[1])
    for i in IPlen:
      dx = task[2]*cos(i*radslice)
      dy = task[2]*sin(i*radslice)
      ret.append(center[0]+dx,center[1]+dy)
  return ret

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
      minPnt = p

  avgDist = distTot/len(pnts)
  distList = shareAvgDist(avgDist)
  if(avgDist==min(distList)):
    return minPnt
  else:
    return [-1,-1]

def getLoc():
  while(1):
    try:
      locxy = connDict['c'][0].recv(7)
      listxy= locxy.split(',')
      listxy[0] = int(listxy[0])
      listxy[1] = int(listxy[1])
      return listxy
    except:
      pass

def goForward(vel):
  motor.forward(vel)

def goStop():
  motor.stop()

def setTimeouts(timeout):
  for soc in connDict:
    connDict[soc][0].settimeout(timeout)

def shareAvgDist(dist):
  lDist = []
  lDist.append(str(dist))
  distList = []
  distList.append(dist)
  nameList = [i[1] for i in IPlist]
  done = False
  count = 0

  while(not done):
    if(len(distList)==len(csoc)-1):
      done = True
      for soc in csoc:
        csoc[soc].send("done ".encode())
        for dist in distList:
          csoc[soc].send((str(dist)+" ").encode())
    else:
      for dist in distList:
        csoc[nameList[count%len(csoc)-1]].send((str(dist)+" ").encode())

    for soc in connDict:
      try:
        sDist = connDict[soc][0].recv(99)
        lDist = sDist.split()
      except:
        pass
      if(lDist[0]=="done"):
        lDist.remove("done")
        for dist in lDist:
          if(not (int(dist) in distList)):
            distList.append(int(dist))
        while(len(distList)<len(csoc)-1):
          try:
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
    count = count + 1
  return distList

def checkPaths(paths,i,f)
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
    except:
      pass

  return ret
