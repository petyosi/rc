eval "$(/opt/homebrew/bin/brew shellenv)"

source ~/.orbstack/shell/init.zsh 2>/dev/null || :

# rustup
export PATH="/opt/homebrew/opt/rustup/bin:$PATH"
