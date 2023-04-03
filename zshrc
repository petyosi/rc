export PATH="/opt/homebrew/bin:$PATH"

# if /opt/homebrew/ exists source antigen from there, if not, use /usr/local
if [ -d "/opt/homebrew/share/antigen" ]; then
  source /opt/homebrew/share/antigen/antigen.zsh
else
  source /usr/local/share/antigen/antigen.zsh
fi

export NVM_LAZY_LOAD=true
antigen bundle lukechilds/zsh-nvm
antigen apply

autoload -U colors && colors
autoload -U zmv
autoload -U compinit && compinit
autoload -Uz zcalc
autoload -U promptinit; promptinit

# prompt
eval "$(starship init zsh)"

# vi mode
bindkey -v
stty -ixon

# enable colored output from ls, etc
export CLICOLOR=1
export BAT_THEME=gruvbox-dark

# expand functions in the prompt
setopt prompt_subst

# ignore duplicate history entries
setopt histignoredups
setopt share_history
setopt APPEND_HISTORY
HISTSIZE=1000
SAVEHIST=1000
HISTFILE=~/.history

# 10ms for key sequences
KEYTIMEOUT=1

export FZF_DEFAULT_COMMAND='ag -g ""'
[ -f ~/.fzf.zsh ] && source ~/.fzf.zsh

alias tmux="tmux -2 -u"
export EDITOR='nvim'
export SUDO_EDITOR='nvim'
alias vim='nvim'
alias ivm='nvim'
alias g='git'
alias y='yarn'
alias p='pnpm'

alias ls='exa'
alias ll='exa -la --git --modified --header --group-directories-first'

export PATH="$HOME/.yarn/bin:$HOME/.config/yarn/global/node_modules/.bin:$PATH"

zstyle ':completion:*' matcher-list '' \
  'm:{a-z\-}={A-Z\_}' \
  'r:[^[:alpha:]]||[[:alpha:]]=** r:|=* m:{a-z\-}={A-Z\_}' \
  'r:|?=** m:{a-z\-}={A-Z\_}'

# tabtab source for packages
# uninstall by removing these lines
[[ -f ~/.config/tabtab/zsh/__tabtab.zsh ]] && . ~/.config/tabtab/zsh/__tabtab.zsh || true

# pnpm
# export PNPM_HOME="/Users/petyo/Library/pnpm"
# export PATH="$PNPM_HOME:$PATH"
# pnpm end

export GPG_TTY=$(tty)
alias p="pnpm"
