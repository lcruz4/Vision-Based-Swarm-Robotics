from finalFuncs import *
import math

pnts = initialize()
connArch = {}
csocArch = {}
paths = {}
minPnt = [-1,-1]
loc = [-1,-1]
path = [None]
arrived = False
msg = ""
xdif = 0
ydif = 0
ackRemaining = 0

setTimeouts(0.001)	#timeouts for server sockets
minPnt = maxAvgDist(pnts,loc)
while(minPnt == [-1,-1]):
  loc = getLoc()
  for soc in connDict:
    try:
      msg = connDict[soc][0].recv(99)
      path = msg.split()
    except:
      pass
  if(path[0]=="i" and path[2]=="f"):
    i = path[1].split(",")
    i[0] = int(i[0])
    i[1] = int(i[1])
    f = path[3].split(",")
    f[0] = int(f[0])
    f[1] = int(f[1])
    path = [None]
    print(soc+" moving")#DEBUG
    pnts.remove(f)
    paths[soc] = [i,f]
    connArch[soc] = connDict.pop(soc)
    csocArch[soc] = csoc.pop(soc)
    print(soc+" socs archived")#DEBUG
    minPnt = maxAvgDist(pnts,loc)

if(len(paths) > 0):
  critPnts = checkPaths(paths,loc,minPnt)
  if(len(critPnts) > 0):
    for name in critPnts:
      msg = ("ackpnt "+str(critPnts[name][0])+","
		+str(critPnts[name][1])+" ")
      csocArch[name].send(msg.encode())
      print("requesting ack from "+name+" at:")#DEBUG
      print(critPnts[name])#DEBUG
      ackRemaining = ackRemaining + 1

for soc in csoc:
  msg = ("i "+str(loc[0])+","+str(loc[1])+" f "
	+str(minPnt[0])+","+str(minPnt[1])+" ")
  csoc[soc].send(msg.encode())	#i ix,iy f fx,fy

while(ackRemaining > 0):
  for name in connArch:
    try:
      msg = connArch[name][0].recv(99)
      msg = msg.split()
    except:
      pass
    if("ACK" in msg):
      print("received ACK from "+name)#DEBUG
      ackRemaining = ackRemaining - 1
    if("ackpnt" in msg):
      while(msg[0]!="ackpnt"):
        del msg[0]	#clean leftovers
      xy = msg[1].split(",")
      xy[0] = int(xy[0])
      xy[1] = int(xy[1])
      ackpnts[name] = xy
      print("ack request from "+name+" at:")#DEBUG
      print(xy)#DEBUG

while(not arrived):
  for name in connArch:
    try:
      msg = connArch[name][0].recv(99)
      msg = msg.split()
    except:
      pass
    if("ackpnt" in msg):
      while(msg[0]!="ackpnt"):
        del msg[0]	#clean leftovers
      xy = msg[1].split(",")
      xy[0] = int(xy[0])
      xy[1] = int(xy[1])
      ackpnts[name] = xy

  loc = getLoc()	#loc holds location from vision system
  dxDest = math.fabs(loc[0]-minPnt[0])
  dyDest = math.fabs(loc[1]-minPnt[1])
  for p in ackpnts:
    dxCrit = math.fabs(loc[0]-ackpnts[p][0])
    dyCrit = math.fabs(loc[1]-ackpnts[p][1])
    if(dxCrit < 20 and dyCrit < 20):
      csocArch[p].send("ACK ".encode())
      break
  del ackpnts[p]	#risky

  if(dxDest < 20 and dyDest < 20):
    goStop()
  else:
    goForward(40)
