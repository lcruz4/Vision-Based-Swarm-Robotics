#!/bin/sh
echo -n
read input

scp "$input" root@10.159.118.36:/root/
scp "$input" root@10.159.135.64:/root/
scp "$input" root@10.159.118.201:/root/
scp "$input" root@10.159.78.111:/root/
scp "$input" root@10.159.119.28:/root/
