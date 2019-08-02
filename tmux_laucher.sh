#!/bin/sh
#
# Setup a work space called `work` with two windows
# first window has 3 panes. 
# The first pane set at 65%, split horizontally, set to api root and running vim
# pane 2 is split at 25% and running redis-server 
# pane 3 is set to api root and bash prompt.
# note: `api` aliased to `cd ~/path/to/work`
#
source .venv/bin/activate
session="webchecker"

# set up tmux
tmux start-server

# create a new tmux session, starting vim from a saved session in the new window
tmux new-session -d -s $session

# Select pane 1, set dir to api, run vim
tmux selectp -t 1 
tmux send-keys "source .venv/bin/activate" C-m 
tmux send-keys "./manage.py runserver 0:8000" C-m 

tmux splitw -h -p 75
tmux send-keys "source .venv/bin/activate" C-m 
tmux send-keys "celery -A webapp  beat -l info --scheduler django_celery_beat.schedulers:DatabaseScheduler" C-m 

tmux selectp -t 2
tmux splitw -v -p 50
tmux send-keys "source .venv/bin/activate" C-m 
tmux send-keys "celery -A webapp worker -l info" C-m 

# Split pane 1 horizontal by 65%, start redis-server
tmux selectp -t 3
tmux splitw -v -p 50
tmux send-keys "source .venv/bin/activate" C-m 
tmux send-keys "./manage.py shell_plus" C-m 


# Select pane 1
tmux selectp -t 1

# # create a new window called scratch
# tmux new-window -t $session:1 -n scratch

# # return to main vim window
# tmux select-window -t $session:0

# Finished setup, attach to the tmux session!
tmux attach-session -t $session