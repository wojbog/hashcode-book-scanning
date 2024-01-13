#!/bin/bash

# Start tmux
tmux new-session -d

# Split the tmux window into 5 panes
tmux split-window -h
tmux split-window -h
tmux split-window -h
tmux split-window -h

# Run commands in each pane
tmux send-keys -t 1 "python main.py ./input/b_read_on.in ./output/b_read_on.txt" C-m
tmux send-keys -t 2 "python main.py ./input/c_incunabula.in ./output/c_incunabula.txt" C-m
tmux send-keys -t 3 "python main.py ./input/d_tough_choices.in ./output/d_tough_choices.txt" C-m
tmux send-keys -t 4 "python main.py ./input/e_so_many_books.in ./output/e_so_many_books.txt" C-m
tmux send-keys -t 5 "python main.py ./input/f_libraries_of_the_world.in ./output/f_libraries_of_the_world.txt" C-m

# Attach to the tmux session
tmux select-layout even-horizontal
# tmux select-layout tiled
tmux attach-session -d
