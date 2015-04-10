from socket import *
import string
import random

XMAX=680
YMAX=480
myF = open('myip','r')
ipF = open('ips','r')
IPlist = []
tlist = []
for line in ipF:
  tlist.append(line[:-1])
  if(len(tlist)==2):
    IPlist.append(tlist)
    tlist = []


ipF.close()
myF.readline()
myIP = myF.readline()
myF.close()
start = string.find(myIP,'inet ')+5
end = string.find(myIP,'/')
myIP = myIP[start:end]
myName = ''

for ip in IPlist:
  if(ip[0]==myIP):
    IPlist.remove(ip)
    myName = ip[1]
    break


iplen = len(IPlist)

Port = 6702
ssoc = socket(AF_INET, SOCK_STREAM)
csoc = {}
for i in range(iplen): #IPlist[i][1] => 'c' or 'r1' or 'r2' etc
  csoc[IPlist[i][1]] = socket(AF_INET, SOCK_STREAM)

ssoc.bind((myIP,Port))
ssoc.listen(5)

connDict = {}
wait = True
for i in range(iplen):
  while(wait):
    try:
      csoc[IPlist[i][1]].connect((IPlist[i][0],Port))
      wait = False
    except:
      pass
  wait = True


connectionList = []
while(len(connectionList)<iplen):
  try:
    connectionList.append(ssoc.accept())
  except:
    pass


i=0
while(i<iplen):
  if(IPlist[i][0] == connectionList[i][1][0]):
    connDict[IPlist[i][1]] = connectionList[i]
    i = i + 1

  else:
    connectionList.append(connectionList[i])
    connectionList.remove(connectionList[i])


