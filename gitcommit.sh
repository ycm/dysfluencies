#!/bin/bash

for arg in "$@" 
do
  echo "adding: $arg"
  git add $arg
done
printf "commit message: "
read msg
git commit -m $msg
git push -u origin master

