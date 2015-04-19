from finalFuncs import *
import math

pnts = initialize()
connArch = {}
csocArch = {}
paths = {}
ackpnts={}
minPnt = [-1,-1]
loc = [0,0]
loc[0],loc[1],angle = getLoc()
path = [None]
arrived = False
msg = ""
xdif = 0
ydif = 0
ackRemaining = 0

setTimeouts(0.001)	#timeouts for server sockets
#If robot has maxAvgDistance then this function returns the nearest point
#which is the point the robot should start moving to if possible.
minPnt = maxAvgDist(pnts,loc)
print(minPnt)#DEBUG
#This while loop happens as long as minPnt is not set, meaning the robot did
#not have the maximum average distance
while(minPnt == [-1,-1]):
  loc[0],loc[1],angle = getLoc()	#updates location
  #This for loop checks any messages received from the other robots
  #The only possible message at this point is a path of a moving robot
  for soc in connDict:
    try:
      msg = connDict[soc][0].recv(99)
      print("from "+soc+" received: "+msg)#DEBUG
      path = msg.split()
      if("i" in path and "f" in path):
        break
    except:
      pass
  #This checks that the message received was in fact a path and extracts the
  #necessary information
  if("i" in path and "f" in path):
    while(path[0]!="i"):
      print(path[0])
      del path[0]
    print("HERE")#DEBUG
    i = path[1].split(",")
    i[0] = int(i[0])	#i is the initial point of the moving robot
    i[1] = int(i[1])
    f = path[3].split(",")
    f[0] = int(f[0])	#f is the destination point of the moving robot
    f[1] = int(f[1])
    path = [None]
    print(soc+" moving")#DEBUG
    #point is already taken so it should be removed for the next iteration
    pnts.remove(f)
    paths[soc] = [i,f]	#updates path list
    #The next two lines archive the socket connections with the moving robot
    connArch[soc] = connDict.pop(soc)
    csocArch[soc] = csoc.pop(soc)
    print(soc+" socs archived")#DEBUG
    minPnt = maxAvgDist(pnts,loc)	#call maxAvgDist again and loop again

#Once outside the loop the robot has a destination point and must figure out
#whether it's okay to start moving or if it must wait for another robot
#The following if statement checks if there are any other moving robots
if(len(paths) > 0):
  #checkPaths checks for any intersections in the saved paths and returns
  #a list of the points of intersection (critical points)
  critPnts = checkPaths(paths,loc,minPnt)
  #if there is an intersection we must ask the intersecting robot for an ack
  if(len(critPnts) > 0):
    #The following for loop sends an ack request to every robot with a
    #path that will intersect with the current robot's path
    #The message also contains the critical point
    for name in critPnts:
      msg = ("ackpnt "+str(critPnts[name][0])+","
		+str(critPnts[name][1])+" ")
      csocArch[name].send(msg.encode())
      print("requesting ack from "+name+" at:")#DEBUG
      print(critPnts[name])#DEBUG
      ackRemaining = ackRemaining + 1

#after sending ack requests the robot must let all other robots know that it
#has a destination and will potentially start moving soon
for soc in csoc:	#sends its path to all robots that are not moving
  print("sent path to " + soc)#DEBUG
  print(loc)#DEBUG
  print(minPnt)#DEBUG
  msg = ("i "+str(loc[0])+","+str(loc[1])+" f "
	+str(minPnt[0])+","+str(minPnt[1])+" ")
  csoc[soc].send(msg.encode())	#i ix,iy f fx,fy

#Now the robot must wait for any acks that it requested before moving
while(ackRemaining > 0):
  for name in connArch:
    try:
      msg = connArch[name][0].recv(99)
      msg = msg.split()
    except:
      pass
    if("ACK" in msg):#if an ack is received ackRemaining will be decremented
      print("received ACK from "+name)#DEBUG
      ackRemaining = ackRemaining - 1
    if("ackpnt" in msg):#if an ack request is received it will be processed
      while(msg[0]!="ackpnt"):
        del msg[0]	#clean leftovers
      xy = msg[1].split(",")
      xy[0] = int(xy[0])
      xy[1] = int(xy[1])
      ackpnts[name] = xy#ackpoints are saved in a list
      print("ack request from "+name+" at:")#DEBUG
      print(xy)#DEBUG

#Once out of this loop the robot can start moving
while(not arrived):
  #this loop will check for messages for ack requests
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

  loc[0],loc[1],angle = getLoc()	#Gets location again
  dx = minPnt[0] - loc[0]
  dy = minPnt[1] - loc[1]
  theta = -(math.atan2(-dy,dx)*180/math.pi - 90)
  if(theta<0):
    theta = theta + 360
  desAngle = int(theta)

  if(math.fabs(desAngle-angle) < 10 or math.fabs(desAngle+360-angle) < 10
	or math.fabs(desAngle-(angle+360))):
    if(math.fabs(dx) < 20 and math.fabs(dy) < 20):
      goStop()
    else:
      goForward(40)
  elif(desAngle-angle < 0):
    pivotLeft(40)
  else:
    pivotRight(40)

  #This for loop checks if any ackpoints have passed
  for p in ackpnts:
    dxCrit = math.fabs(loc[0]-ackpnts[p][0])
    dyCrit = math.fabs(loc[1]-ackpnts[p][1])
    if(dxCrit < 20 and dyCrit < 20):
      csocArch[p].send("ACK ".encode())
      break
  if(len(ackpnts)!=0 and dxCrit < 20 and dyCrit < 20):
    del ackpnts[p]
