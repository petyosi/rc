#!/bin/sh
brew bundle install

# oh-my-zsh installation
if [ ! -d "$HOME/.oh-my-zsh" ]; then
  echo "Installing oh-my-zsh..."
  sh -c "$(curl -fsSL https://raw.githubusercontent.com/ohmyzsh/ohmyzsh/master/tools/install.sh)" "" --unattended
else
  echo "oh-my-zsh already installed, skipping..."
fi

# zsh-autosuggestions plugin
ZSH_CUSTOM=${ZSH_CUSTOM:-$HOME/.oh-my-zsh/custom}
if [ ! -d "$ZSH_CUSTOM/plugins/zsh-autosuggestions" ]; then
  echo "Installing zsh-autosuggestions..."
  git clone https://github.com/zsh-users/zsh-autosuggestions "$ZSH_CUSTOM/plugins/zsh-autosuggestions"
else
  echo "zsh-autosuggestions already installed, skipping..."
fi

# ZSH
ln -sf "$PWD"/zshrc ~/.zshrc
ln -sf "$PWD"/inputrc ~/.inputrc
touch ~/.hushlogin

# Tmux
ln -sf "$PWD"/.tmux/.tmux.conf ~/.tmux.conf
ln -sf "$PWD"/.tmux.conf.local ~/.tmux.conf.local
tic -x ./tmux.terminfo

# Github
ln -sf "$PWD"/gitconfig ~/.gitconfig

# Ghostty
mkdir -p ~/.config/ghostty
ln -sf "$PWD"/ghostty-config ~/.config/ghostty/config

# Claude
mkdir -p ~/.claude
ln -sfn "$PWD"/PROFILE_CLAUDE.md ~/.claude/CLAUDE.md
ln -sfn "$PWD"/claude/skills ~/.claude/skills
ln -sfn "$PWD"/claude/settings.json ~/.claude/settings.json

# Markdownlint
ln -sfn "$PWD"/markdownlint.yaml ~/.markdownlint.yaml

# starship
ln -sfn "$PWD"/starship.toml ~/.config/starship.toml

# opencode
mkdir -p ~/.config/opencode
ln -sfn "$PWD"/opencode.json ~/.config/opencode/opencode.json
