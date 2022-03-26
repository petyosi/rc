#!/bin/sh
brew bundle install

# setup tmux
ln -sf $PWD/.tmux/.tmux.conf ~/.tmux.conf
ln -sf $PWD/.tmux.conf.local ~/.tmux.conf.local

# setup neovim
# neovim Plug
sh -c 'curl -fLo "${XDG_DATA_HOME:-$HOME/.local/share}"/nvim/site/autoload/plug.vim --create-dirs \
       https://raw.githubusercontent.com/junegunn/vim-plug/master/plug.vim'
mkdir -p ~/.config/nvim/backup
mkdir -p ~/.config/nvim/swp
mkdir -p ~/.config/nvim/undo
ln -sf $PWD/init.vim ~/.config/nvim/init.vim
ln -sf $PWD/coc-settings.json ~/.config/nvim/coc-settings.json

# zshell and git stuff
ln -sf $PWD/zshrc ~/.zshrc
ln -sf $PWD/gitconfig ~/.gitconfig
ln -sf $PWD/inputrc ~/.inputrc

touch ~/.hushlogin
tic -x ./tmux.terminfo
