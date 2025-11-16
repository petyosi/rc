#!/bin/sh
brew bundle install

# Tmux
ln -sf "$PWD"/.tmux/.tmux.conf ~/.tmux.conf
ln -sf "$PWD"/.tmux.conf.local ~/.tmux.conf.local
tic -x ./tmux.terminfo

ln -sf "$PWD"/zshrc ~/.zshrc
ln -sf "$PWD"/inputrc ~/.inputrc
touch ~/.hushlogin

ln -sf "$PWD"/gitconfig ~/.gitconfig

mkdir -p ~/.config/ghostty
ln -sf "$PWD"/ghostty-config ~/.config/ghostty/config

mkdir -p ~/.claude

ln -sfn "$PWD"/PROFILE_CLAUDE.md ~/.claude/CLAUDE.md
ln -sfn "$PWD"/claude/skills ~/.claude/skills
ln -sfn "$PWD"/claude/settings.json ~/.claude/settings.json

ln -sfn "$PWD"/markdownlint.yaml ~/.markdownlint.yaml
