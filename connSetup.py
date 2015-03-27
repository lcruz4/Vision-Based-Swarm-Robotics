from socket import *
import string

f = open('./comm/ip','r')
f.readline()
myIP = f.readline()
start = string.find(myIP,'inet ')+5
end = string.find(myIP,'/')
myIP = myIP[start:end]
IPlist = [['10.159.202.190','c'],['10.159.157.88','r1'],['10.159.135.64','r2'],['10.159.9.3','r3']]#,IP4,IP5]
for ip in IPlist:
  if ip[0] == myIP:
    IPlist.remove(ip)
    break
iplen = len(IPlist)

Port = 6712
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
ssoc.settimeout(.001)
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
