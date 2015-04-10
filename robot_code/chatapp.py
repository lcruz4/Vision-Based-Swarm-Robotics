from connSetup import *
import sys


while(1):
  sendrecv=int(raw_input("0:send\n1:recv"))
  to = raw_input("'c','r1','r2', or 'r3'")
  if(sendrecv == 0):
    mesg = 234
    csoc[to].send(mesg)
  elif(sendrecv == 1):
    print(connDict[to][0].recv(4096))
  else:
    break


#while(1):
#  checkmessages()
#
#def checkmessages():
#  for soc in connDict:
#    buf[soc].append(connDict[soc][0].recv(4096))
