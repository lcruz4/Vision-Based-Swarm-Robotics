#!/bin/sh
echo -n
read input

scp "$input" root@10.159.157.88:/root/
scp "$input" root@10.159.135.64:/root/
scp "$input" root@10.159.9.3:/root/
