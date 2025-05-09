#!/bin/sh
# brew bundle install

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
ln -sf "$PWD"/zed ~/.config/zed
