export TBPATH=`dirname ${BASH_SOURCE[0]-$0}`

alias tbmux="tmux new-session -s tb -d zsh \
	&& tmux split-window -t tb:0.0 -h \
	&& tmux split-window -t tb:0.1 -v \
	&& tmux send-keys -t tb:0.1 \"printf '\033]2;%s\033\\' 'Frontend'\" C-m \
	&& tmux send-keys -t tb:0.2 \"printf '\033]2;%s\033\\' 'Backend api'\" C-m \
	&& tmux send-keys -t tb:0.1 'cd $TBPATH/front && npm run serve' C-m \
	&& tmux send-keys -t tb:0.2 'cd $TBPATH/api && source venv/bin/activate && python run.py --debug' C-m \
	&& tmux select-pane -t tb:0.0 \
	&& tmux a -t tb"

alias tbmux-quit="tmux kill-session -t tb"
