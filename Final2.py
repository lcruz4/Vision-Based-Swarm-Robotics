from socket import *
import string

f = open('ip','r')
f.readline()
myIP = f.readline()
start = string.find(myIP,'inet ')+5
end = string.find(myIP,'/')
myIP = myIP[start:end]
IPlist = [['10.159.202.190','c'],['10.159.157.88','r1'],['10.159.135.64','r2'],['10.159.9.3','r3']]#,IP4,IP5]

Port = 6712
ssoc = socket(AF_INET, SOCK_STREAM)
csoc = {}
for i in range(3):
  csoc[IPlist[i][1]] = socket(AF_INET, SOCK_STREAM)
ssoc.bind((myIP,Port))
ssoc.listen(5)

for ip in IPlist:
  if ip[0] == myIP:
    IPlist.remove(ip)
    break
iplen = len(IPlist)

connectionList = []
connDict = {}
ssoc.settimeout(.001)
wait = True
for i in range(iplen):
  while(wait):
    try:
      csoc[IPlist[i][1]].connect((IPlist[i][0],Port))
      wait = False
    except:
      pass
  wait = True
while(len(connectionList)<iplen):
  try:
    connectionList.append(ssoc.accept())
  except:
    pass
i=0
while(i<iplen):
  if(IPlist[i][0] == connectionList[i][1][0]):
    conDict[IPlist[i][1]] = connectionList[i]
    i = i + 1
  else:
    connectionList.append(connectionList[i])
    connectionList.remove(connectionList[i])
print(IPlist)
print(connectionList)

'''
task = ssoc.recv(4096)
center = ssoc.recv(4096)
param = ssoc.recv(4096)

avgdist = magic(task,center,param)
connectionList[j+1].send(avgdist)'''
