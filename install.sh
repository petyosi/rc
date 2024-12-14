#!/bin/sh
# brew bundle install

# Tmux
ln -sf "$PWD"/.tmux/.tmux.conf ~/.tmux.conf
ln -sf "$PWD"/.tmux.conf.local ~/.tmux.conf.local
tic -x ./tmux.terminfo
tic -x -o ~/.terminfo ./wezterm.terminfo

ln -sf "$PWD"/zshrc ~/.zshrc
ln -sf "$PWD"/inputrc ~/.inputrc
touch ~/.hushlogin

ln -sf "$PWD"/gitconfig ~/.gitconfig
ln -sf "$PWD"/alacritty.toml ~/.alacritty.toml
