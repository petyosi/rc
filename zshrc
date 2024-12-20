export PATH="/opt/homebrew/bin:$PATH"
export GPG_TTY=$(tty)
export EDITOR='nvim'
export SUDO_EDITOR='nvim'

autoload -U colors && colors
autoload -U zmv
autoload -U compinit && compinit
autoload -Uz zcalc
autoload -U promptinit; promptinit

# prompt
eval "$(starship init zsh)"

# vi mode
bindkey -v
bindkey "^R" history-incremental-search-backward
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

export FZF_DEFAULT_COMMAND='fd --type f --strip-cwd-prefix'
[ -f ~/.fzf.zsh ] && source ~/.fzf.zsh

alias tmux="tmux -2 -u"
alias vim='nvim'
alias ivm='nvim'
alias g='git'
alias y='yarn'
alias p='pnpm'
alias ls='eza --icons'
alias ll='eza -la --git --modified --header --group-directories-first --icons'
alias nr='npm run'
alias gotovo='say -v "Daria" готов си'

zstyle ':completion:*' matcher-list '' \
  'm:{a-z\-}={A-Z\_}' \
  'r:[^[:alpha:]]||[[:alpha:]]=** r:|=* m:{a-z\-}={A-Z\_}' \
  'r:|?=** m:{a-z\-}={A-Z\_}'
export PATH="/opt/homebrew/opt/postgresql@15/bin:$PATH"
export PATH="$(brew --prefix)/opt/python@3.12/libexec/bin:$PATH"

alias nbe='nvim src/services/logfire-backend'
alias ndb='nvim src/packages/logfire-db'
alias nfe='cd src/services/logfire-frontend && nvim .'
eval "$(fnm env --use-on-cd --version-file-strategy=recursive --resolve-engines --shell zsh)"
# This breaks FNM and does not work for the Python repo
# eval "$(direnv hook zsh)"

# Function to display a macOS notification
# Usage: notify "Message" "Title" "Subtitle"
notify() {
    local message="${1:-Notification}"
    local title="${2:-Notification}"
    local subtitle="${3:-}"

    # If no subtitle is provided, display notification without subtitle
    if [[ -z "$subtitle" ]]; then
        osascript -e "display notification \"$message\" with title \"$title\""
    else
        osascript -e "display notification \"$message\" with title \"$title\" subtitle \"$subtitle\""
    fi
}
