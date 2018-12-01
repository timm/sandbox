#!/usr/bin/env bash
HERE=$PWD
THERE=$(echo $PATH | gawk -F: '{print $1}')
sudo ln -sf $HERE/auk $THERE/auk
chmod +x auk


Var=$HERE/var
No=.gitignore
if [ ! -f "$No" ]; then
  echo $Var > $No; git add $No; 
fi
mkdir -p $Var


pathadd() {
    if [ -d "$1" ] && [[ ":$PATH:" != *":$1:"* ]]; then
        PATH="${PATH:+"$PATH:"}$1"
    fi
}

pathadd $PWD

here() { cd $1; basename "$PWD"; }

Tag="Duo0"
_c1="\[\033[01;32m\]"
_c2="\[\033[01;34m\]"
_c3="\[\033[31m\]"
_c6="\033[33m"
_c5="\[\033[35m\]$"
_c0="\[\033[00m\]"
_c7="[\033]01;19\]"

PROMPT_COMMAND='echo -ne "${_c6}${Tag}> \033]0;$(here ../..)/$(here ..)/$(here .)\007";PS1="${_c1} $(here ../..)/$_c2$(here ..)/$_c3$(here .) ${_c6}\!>${_c0}\e[m "'

alias ll='ls -GF'
