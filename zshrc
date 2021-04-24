export PATH="/opt/homebrew/bin:$PATH"
fpath+=$HOME/.zsh/pure

autoload -U colors && colors
autoload -U zmv
autoload -U compinit && compinit
autoload -Uz zcalc
autoload -U promptinit; promptinit
prompt pure
zstyle ':prompt:pure:prompt:*' color green

# vi mode
bindkey -v
stty -ixon

# enable colored output from ls, etc
export CLICOLOR=1
export BAT_THEME=gruvbox-dark

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
# 10ms for key sequences
KEYTIMEOUT=1
setopt APPEND_HISTORY

export FZF_DEFAULT_COMMAND='ag -g ""'
[ -f ~/.fzf.zsh ] && source ~/.fzf.zsh

alias tmux="tmux -2 -u"
export EDITOR='nvim'
export SUDO_EDITOR='nvim'
alias vim='nvim'
alias g='git'
alias y='yarn'

alias ls='exa'
alias ll='exa -la --git --modified --header --group-directories-first'

export PUPPETEER_SKIP_CHROMIUM_DOWNLOAD=true
export PUPPETEER_EXECUTABLE_PATH=`which chromium`

[ -f ~/.stream-env.zsh ] && source ~/.stream-env.zsh
