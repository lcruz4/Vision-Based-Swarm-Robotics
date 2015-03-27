import string

f = open('ip','r')
f.readline()
IP = f.readline()
start = string.find(IP,'inet ')+5
end = string.find(IP,'/')
IP = IP[start:end]

from socket import *
Port = 6712
ssoc = socket(AF_INET, SOCK_STREAM)
ssoc.bind((IP,Port))
