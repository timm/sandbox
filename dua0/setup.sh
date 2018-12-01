#!/usr/bin/env bash
HERE=$PWD
THERE=$(echo $PATH | gawk -F: '{print $1}')
sudo ln -sf $HERE/auk $THERE/auk
chmod +x auk

Var=$HERE/var
No=.gitignore
if [ ! -f $No ]; then
  echo $Var > $No; git add $No; 
fi
mkdir -p $Var


