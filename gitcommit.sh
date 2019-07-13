#!/bin/bash

for arg in "$@" 
do
  git add $arg
done
printf "commit message: "
read msg
git commit -m $msg
git push -u origin master

