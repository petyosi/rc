export PATH="/opt/homebrew/bin:$PATH"
source /opt/homebrew/share/antigen/antigen.zsh
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

[ -f ~/.stream-env.zsh ] && source ~/.stream-env.zsh

export PATH="/opt/homebrew/opt/ruby/bin:/opt/homebrew/lib/ruby/gems/3.0.0/bin:$PATH"
export PATH=/opt/homebrew/opt/python@3.9/libexec/bin:$PATH
export LDFLAGS="-L/opt/homebrew/opt/ruby/lib"
export CPPFLAGS="-I/opt/homebrew/opt/ruby/include"
export PKG_CONFIG_PATH="/opt/homebrew/opt/ruby/lib/pkgconfig"


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
