autoload -U colors && colors
autoload -U zmv
autoload -U compinit && compinit
autoload -Uz zcalc
autoload -U promptinit; promptinit
prompt pure

# vi mode
bindkey -v
stty -ixon

# enable colored output from ls, etc
export CLICOLOR=1

# expand functions in the prompt
setopt prompt_subst

# use incremental search
bindkey '^R' history-incremental-search-backward

# ignore duplicate history entries
setopt histignoredups
setopt share_history
HISTSIZE=1000
SAVEHIST=1000
HISTFILE=~/.history
setopt APPEND_HISTORY

export FZF_DEFAULT_COMMAND='ag -g ""'
[ -f ~/.fzf.zsh ] && source ~/.fzf.zsh

alias tmux="tmux -2 -u"
export EDITOR='nvim'
export SUDO_EDITOR='nvim'
alias vim='nvim'
alias g='git'
