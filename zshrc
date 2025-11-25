export ZSH="$HOME/.oh-my-zsh"

VI_MODE_RESET_PROMPT_ON_MODE_CHANGE=true
VI_MODE_SET_CURSOR=true
KEYTIMEOUT=1

ZSH_THEME="robbyrussell"

zstyle ':omz:plugins:eza' 'dirs-first' yes
zstyle ':omz:plugins:eza' 'icons' yes
plugins=(git vi-mode eza gh nodenv starship zsh-autosuggestions)

#### pre sourcing the oh-my-zsh.sh 
source $ZSH/oh-my-zsh.sh

export EDITOR='nvim'
export SUDO_EDITOR='nvim'

alias tmux="tmux -2 -u"
alias vim='nvim'
alias ivm='nvim'
alias g='git'
alias y='yarn'
alias p='pnpm'
alias nr='npm run'
alias gotovo='say -v "Daria" готов си'

# uv
compdef '_files -g "*.py"' uv\ run
alias nbe='uv run nvim src/services/logfire-backend'
alias ndb='uv run nvim src/packages/logfire-db'
alias nfe='cd src/services/logfire-frontend && nvim .'
eval "$(uv generate-shell-completion zsh)"
# uv end

# pnpm
export PNPM_HOME="/Users/petyo/Library/pnpm"
case ":$PATH:" in
  *":$PNPM_HOME:"*) ;;
  *) export PATH="$PNPM_HOME:$PATH" ;;
esac
# pnpm end

[ -f ~/.llm-keys.sh ] && source ~/.llm-keys.sh

export PRE_COMMIT_ALLOW_NO_CONFIG=1 

# autosuggestions
bindkey '^ ' autosuggest-accept

# fnm
eval "$(fnm env --use-on-cd --version-file-strategy=recursive --resolve-engines --shell zsh)"
