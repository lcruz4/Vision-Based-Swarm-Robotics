import time

t= time.time()
print(t)
while(time.time()-t<.1):
  continue
t=time.time()
print(t)
