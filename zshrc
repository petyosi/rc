export PATH="/opt/homebrew/bin:$PATH"

# fpath+=$HOME/.zsh/pure

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

# use incremental search
# bindkey '^R' history-incremental-search-backward

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
alias ivm='nvim'
alias g='git'
alias y='yarn'

alias ls='exa'
alias ll='exa -la --git --modified --header --group-directories-first'

export PUPPETEER_SKIP_CHROMIUM_DOWNLOAD=true
export PUPPETEER_EXECUTABLE_PATH=`which chromium`

[ -f ~/.stream-env.zsh ] && source ~/.stream-env.zsh

export PATH="/opt/homebrew/opt/ruby/bin:/opt/homebrew/lib/ruby/gems/3.0.0/bin:$PATH"
export PATH=/opt/homebrew/opt/python@3.9/libexec/bin:$PATH
export LDFLAGS="-L/opt/homebrew/opt/ruby/lib"
export CPPFLAGS="-I/opt/homebrew/opt/ruby/include"
export PKG_CONFIG_PATH="/opt/homebrew/opt/ruby/lib/pkgconfig"

export NVM_DIR="$HOME/.nvm"
[ -s "/opt/homebrew/opt/nvm/nvm.sh" ] && . "/opt/homebrew/opt/nvm/nvm.sh"  # This loads nvm
[ -s "/opt/homebrew/opt/nvm/etc/bash_completion.d/nvm" ] && . "/opt/homebrew/opt/nvm/etc/bash_completion.d/nvm"  # This loads nvm bash_completion

# place this after nvm initialization!
autoload -U add-zsh-hook
load-nvmrc() {
  local node_version="$(nvm version)"
  local nvmrc_path="$(nvm_find_nvmrc)"

  if [ -n "$nvmrc_path" ]; then
    local nvmrc_node_version=$(nvm version "$(cat "${nvmrc_path}")")

    if [ "$nvmrc_node_version" = "N/A" ]; then
      nvm install
    elif [ "$nvmrc_node_version" != "$node_version" ]; then
      nvm use
    fi
  elif [ "$node_version" != "$(nvm version default)" ]; then
    echo "Reverting to nvm default version"
    nvm use default
  fi
}

add-zsh-hook chpwd load-nvmrc
load-nvmrc

export PATH="$HOME/.yarn/bin:$HOME/.config/yarn/global/node_modules/.bin:$PATH"

# android
export ANDROID_HOME=$HOME/Library/Android/sdk
export PATH=$PATH:$ANDROID_HOME/emulator
export PATH=$PATH:$ANDROID_HOME/tools
export PATH=$PATH:$ANDROID_HOME/tools/bin
export PATH=$PATH:$ANDROID_HOME/platform-tools

zstyle ':completion:*' matcher-list '' \
  'm:{a-z\-}={A-Z\_}' \
  'r:[^[:alpha:]]||[[:alpha:]]=** r:|=* m:{a-z\-}={A-Z\_}' \
  'r:|?=** m:{a-z\-}={A-Z\_}'

# tabtab source for packages
# uninstall by removing these lines
[[ -f ~/.config/tabtab/zsh/__tabtab.zsh ]] && . ~/.config/tabtab/zsh/__tabtab.zsh || true

# pnpm
export PNPM_HOME="/Users/petyo/Library/pnpm"
export PATH="$PNPM_HOME:$PATH"
# pnpm end