import time
from socket import *
timex = time.time()
count = 0
seq = []
maxerr = 0
while len(seq) < 10:
  #random delay times
  if(count%7==0):
    time.sleep(0.01)
  elif(count%13==0):
    time.sleep(0.02)
  elif(count%27==0):
    time.sleep(0.03)
  elif(count%59==0):
    time.sleep(0.025)
  else:
    time.sleep(0.005)
  #wait .5 second
  if(time.time() - timex > .5*(len(seq)+1)):
    seq.append(count)
    x = time.time() - timex
    print(x)
    x = x*10
    x = x%5
    if(maxerr < x):
      maxerr = x
  #initialize
  if(timex == 0):
    timex = time.time()
  #inc count
  count = count + 1

clientsocket = socket(AF_INET, SOCK_STREAM)
clientsocket.connect(('192.168.1.12',6712))
print('connected')
clientsocket.send(seq[0])
clientsocket.close()
print("maxerr: "+str(maxerr))
print("count: "+str(count))
print(seq)
