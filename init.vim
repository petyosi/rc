" Basics
set hidden lazyredraw showmode novisualbell number ttyfast

set laststatus=3

" Whitespace configuration
set nowrap tabstop=2 shiftwidth=2 softtabstop=2 expandtab smartindent nofixendofline

set laststatus=3

" Menu stuff
set wildmode=list:full
set wildignore+=*.o,*.obj,.git,*.rbc,*.class,.svn,vendor/gems/*
set wildignore+=deploy/**,dist/**,release/**,*.min.js,*.js.map

" Search
set hlsearch incsearch ignorecase smartcase

" better colors
set termguicolors

" Use modeline overrides
set modeline modelines=10

set mouse=a

" Undo and backup
set undofile
set nobackup
set nowritebackup
set undodir=~/.config/nvim/undo
set backupdir=~/.config/nvim/backup
set directory=~/.config/nvim/swp

let mapleader=" "

set clipboard=unnamedplus

set diffopt=vertical,iwhiteall

" Smaller updatetime for CursorHold & CursorHoldI
set updatetime=300

" don't give |ins-completion-menu| messages.
set shortmess+=c

" always show signcolumns
set signcolumn=yes

autocmd FileType gitcommit setlocal tw=72 | set spell | set colorcolumn=50

call plug#begin('~/.config/nvim/plugged')

""""""""""""""""""""""""""""""""""""""
" general
""""""""""""""""""""""""""""""""""""""
Plug 'tpope/vim-sensible'
Plug 'tpope/vim-repeat'
Plug 'tpope/vim-surround'
Plug 'tpope/vim-unimpaired'
Plug 'tpope/vim-eunuch'
Plug 'tpope/vim-ragtag'
Plug 'wellle/targets.vim'

Plug 'tpope/vim-commentary'
Plug 'godlygeek/tabular'
Plug 'tpope/vim-markdown'
Plug 'iamcco/markdown-preview.nvim', { 'do': 'cd app & yarn install'  }
Plug 'jxnblk/vim-mdx-js'

""""""""""""""""""""""""""""""""""""""
" Rust/toml
""""""""""""""""""""""""""""""""""""""
Plug 'rust-lang/rust.vim'
Plug 'cespare/vim-toml'

""""""""""""""""""""""""""""""""""""""
" TypeScript / tsx
""""""""""""""""""""""""""""""""""""""
Plug 'leafgarland/typescript-vim'
Plug 'peitalin/vim-jsx-typescript'
Plug 'othree/yajs.vim'
Plug 'mxw/vim-jsx' 

""""""""""""""""""""""""""""""""""""""
" Git
""""""""""""""""""""""""""""""""""""""
Plug 'tpope/vim-git'
Plug 'tpope/vim-fugitive'
Plug 'tpope/vim-rhubarb'
Plug 'rhysd/git-messenger.vim'
" Plug 'airblade/vim-gitgutter'

""""""""""""""""""""""""""""""""""""""
" Ack
""""""""""""""""""""""""""""""""""""""
Plug 'mileszs/ack.vim'

""""""""""""""""""""""""""""""""""""""
" No idea who needs these
""""""""""""""""""""""""""""""""""""""
Plug 'ConradIrwin/vim-bracketed-paste'

""""""""""""""""""""""""""""""""""""""
" FZF
""""""""""""""""""""""""""""""""""""""
Plug 'junegunn/fzf', { 'dir': '~/.fzf', 'do': './install --all' }
Plug 'junegunn/fzf.vim'

""""""""""""""""""""""""""""""""""""""
" Airline
""""""""""""""""""""""""""""""""""""""
Plug 'vim-airline/vim-airline'
Plug 'vim-airline/vim-airline-themes'

""""""""""""""""""""""""""""""""""""""
" Misc stuff
""""""""""""""""""""""""""""""""""""""
Plug 'cakebaker/scss-syntax.vim'
Plug 'hail2u/vim-css3-syntax'
Plug 'othree/html5.vim'
Plug 'ap/vim-css-color'

Plug 'junegunn/goyo.vim'
Plug 'junegunn/limelight.vim'

Plug 'elzr/vim-json'
Plug 'neoclide/jsonc.vim'

Plug 'morhetz/gruvbox'
Plug 'rebelot/kanagawa.nvim'

Plug 'neoclide/coc.nvim', {'branch': 'release'}
Plug 'honza/vim-snippets'
Plug 'joaohkfaria/vim-jest-snippets'

Plug 'antoinemadec/coc-fzf'

Plug 'bfontaine/Brewfile.vim'
Plug 'evanleck/vim-svelte', {'branch': 'main'}
Plug 'nvim-treesitter/nvim-treesitter', {'do': ':TSUpdate'}
Plug 'ryanoasis/vim-devicons'
Plug 'kyazdani42/nvim-web-devicons'
Plug 'reedes/vim-pencil'

Plug 'nvim-lua/plenary.nvim'
Plug 'sindrets/diffview.nvim'
Plug 'github/copilot.vim'
Plug 'sainnhe/everforest'
call plug#end()

let g:fzf_layout = { 'window': { 'width': 0.9, 'height': 0.6 } }

if executable('ag')
  let g:ackprg = 'ag --vimgrep'
endif

let g:airline_powerline_fonts=1
let g:airline#extensions#tabline#enabled = 1
let g:airline#extensions#tabline#show_tabs = 1
let g:airline#extensions#tabline#show_tab_nr = 0
let g:airline#extensions#tabline#buffer_idx_mode = 1

nmap <leader>1 <Plug>AirlineSelectTab1
nmap <leader>2 <Plug>AirlineSelectTab2
nmap <leader>3 <Plug>AirlineSelectTab3
nmap <leader>4 <Plug>AirlineSelectTab4
nmap <leader>5 <Plug>AirlineSelectTab5
nmap <leader>6 <Plug>AirlineSelectTab6
nmap <leader>7 <Plug>AirlineSelectTab7
nmap <leader>8 <Plug>AirlineSelectTab8
nmap <leader>9 <Plug>AirlineSelectTab9

let $FZF_DEFAULT_COMMAND = 'ag -g ""'
nnoremap <leader>p :Files<CR>
nnoremap <leader>o :Buffers<CR>

map , <Plug>(easymotion-prefix)

let g:gruvbox_italic = 1
let g:gruvbox_contrast_dark = 'soft'
let g:everforest_background = 'soft'

set background=dark
colorscheme everforest
highlight Normal guibg=0 ctermbg=0

nnoremap <Leader>w :w!<CR>
nnoremap <Leader>ev :e $MYVIMRC<cr>
nnoremap <Leader>sv :so $MYVIMRC<cr>

cnoremap <C-n> <Up>

nnoremap <Tab> >>
nnoremap <S-Tab> <<
vnoremap <Tab> >gv
vnoremap <S-Tab> <gv

nnoremap <leader>d :bp<cr>:bd #<cr>
nnoremap <Leader>h :nohlsearch<CR>
nnoremap <Leader>s :setlocal spell! spell?<CR>

nnoremap <Leader>gs :0G<CR>
nnoremap <Leader>gd :Gvdiff<CR>

noremap <Leader>n :CocCommand explorer --sources file+,buffer+ --position right --width 80<CR>
noremap <M-j> :CocCommand explorer --sources file+,buffer+ --position right --width 80<CR>

noremap <Leader>rt :CocCommand tsserver.restart<CR>

nmap <Leader>er <Cmd>call CocAction('runCommand', 'explorer.doAction', 'closest', ['reveal:0'], [['relative', 0, 'file']])<CR>

let g:coc_global_extensions = [ 'coc-snippets', 'coc-json', 'coc-rls', 'coc-eslint', 'coc-tsserver', 'coc-css', 'coc-stylelintplus', 'coc-prettier', 'coc-git' , 'coc-explorer', 'coc-jest', 'coc-yank', 'coc-pairs' ]

function! s:check_back_space() abort
  let col = col('.') - 1
  return !col || getline('.')[col - 1]  =~# '\s'
endfunction

" Use <c-space> for trigger completion.
inoremap <silent><expr> <c-space> coc#refresh()

hi CocSearch ctermfg=12 guifg=#18A3FF
hi CocMenuSel ctermbg=109 guibg=#13354A

inoremap <silent><expr> <TAB>
      \ coc#pum#visible() ? coc#_select_confirm() :
      \ coc#expandableOrJumpable() ? "\<C-r>=coc#rpc#request('doKeymap', ['snippets-expand-jump',''])\<CR>" :
      \ CheckBackSpace() ? "\<TAB>" :
      \ coc#refresh()

function! CheckBackSpace() abort
  let col = col('.') - 1
  return !col || getline('.')[col - 1]  =~# '\s'
endfunction

inoremap <silent><expr> <CR> 
    \ coc#pum#visible() ? coc#pum#confirm() : 
    \ "\<C-g>u\<CR>"

inoremap <silent><expr> <C-x><C-z> coc#pum#visible() ? coc#pum#stop() : "\<C-x>\<C-z>"

" Use `[c` and `]c` for navigate diagnostics
nmap <silent> [c <Plug>(coc-diagnostic-prev)
nmap <silent> ]c <Plug>(coc-diagnostic-next)

" Remap keys for gotos
nmap <silent> gd <Plug>(coc-definition)
nmap <silent> gy <Plug>(coc-type-definition)
nmap <silent> gi <Plug>(coc-implementation)
nmap <silent> gr <Plug>(coc-references)

" Use K for show documentation in preview window
nnoremap <silent> K :call <SID>show_documentation()<CR>

function! s:show_documentation()
  if &filetype == 'vim'
    execute 'h '.expand('<cword>')
  else
    call CocAction('doHover')
  endif
endfunction

" Highlight symbol under cursor on CursorHold
autocmd CursorHold * silent call CocActionAsync('highlight')

" Remap for rename current word
nmap <leader>rn <Plug>(coc-rename)

" Remap for format selected region
vmap <leader>f <Plug>(coc-format-selected)
nmap <leader>f <Plug>(coc-format)

augroup mygroup
  autocmd!
  " Setup formatexpr specified filetype(s).
  autocmd FileType typescript,json setl formatexpr=CocAction('formatSelected')
  " Update signature help on jump placeholder
  autocmd User CocJumpPlaceholder call CocActionAsync('showSignatureHelp')
augroup end

" Remap for do codeAction of selected region, ex: `<leader>aap` for current paragraph
vmap <leader>a  <Plug>(coc-codeaction-selected)
vmap <M-k>  <Plug>(coc-codeaction-selected)
nmap <leader>a  <Plug>(coc-codeaction-selected)

" Remap for do codeAction of current line
nmap <leader>ac  <Plug>(coc-codeaction)
nmap <M-k>  <Plug>(coc-codeaction)
" Fix autofix problem of current line
nmap <leader>qf  <Plug>(coc-fix-current)

" Use `:Format` for format current buffer
command! -nargs=0 Format call CocAction('format')
command! -nargs=0 Prettier :CocCommand prettier.formatFile

" Use `:Fold` for fold current buffer
command! -nargs=? Fold :call     CocAction('fold', <f-args>)

" Show all diagnostics
nnoremap <silent> <space>a  :<C-u>CocFzfList diagnostics<cr>
" Manage extensions
nnoremap <silent> <space>e  :<C-u>CocFzfList extensions<cr>
" Find symbol of current document
nnoremap <silent> <space>l  :<C-u>CocFzfList outline<cr>
" Show commands
nnoremap <silent> <space>c  :<C-u>CocFzfList commands<cr>
" Search workspace symbols
nnoremap <silent> <space>s  :<C-u>CocFzfList symbols<cr>
" Do default action for next item.
nnoremap <silent> <space>j  :<C-u>CocNext<CR>
" Do default action for previous item.
nnoremap <silent> <space>k  :<C-u>CocPrev<CR>

" Use <C-l> for trigger snippet expand.
imap <C-l> <Plug>(coc-snippets-expand)

" Use <C-j> for select text for visual placeholder of snippet.
vmap <C-j> <Plug>(coc-snippets-select)

let g:coc_snippet_next = '<c-j>'

" Use <C-k> for jump to previous placeholder, it's default of coc.nvim
let g:coc_snippet_prev = '<c-k>'

" Use <C-j> for both expand and jump (make expand higher priority.)
imap <C-j> <Plug>(coc-snippets-expand-jump)


" Map function and class text objects
" NOTE: Requires 'textDocument.documentSymbol' support from the language server.
xmap if <Plug>(coc-funcobj-i)
omap if <Plug>(coc-funcobj-i)
xmap af <Plug>(coc-funcobj-a)
omap af <Plug>(coc-funcobj-a)
xmap ic <Plug>(coc-classobj-i)
omap ic <Plug>(coc-classobj-i)
xmap ac <Plug>(coc-classobj-a)
omap ac <Plug>(coc-classobj-a)

" Remap <C-f> and <C-b> for scroll float windows/popups.
if has('nvim-0.4.0') || has('patch-8.2.0750')
  nnoremap <silent><nowait><expr> <C-f> coc#float#has_scroll() ? coc#float#scroll(1) : "\<C-f>"
  nnoremap <silent><nowait><expr> <C-b> coc#float#has_scroll() ? coc#float#scroll(0) : "\<C-b>"
  inoremap <silent><nowait><expr> <C-f> coc#float#has_scroll() ? "\<c-r>=coc#float#scroll(1)\<cr>" : "\<Right>"
  inoremap <silent><nowait><expr> <C-b> coc#float#has_scroll() ? "\<c-r>=coc#float#scroll(0)\<cr>" : "\<Left>"
  vnoremap <silent><nowait><expr> <C-f> coc#float#has_scroll() ? coc#float#scroll(1) : "\<C-f>"
  vnoremap <silent><nowait><expr> <C-b> coc#float#has_scroll() ? coc#float#scroll(0) : "\<C-b>"
endif

let g:markdown_fenced_languages = ['ts=typescript', 'python', 'tsx=typescript', 'jsx=javascript.jsx']

function! s:goyo_enter()
  set noshowmode
  set noshowcmd
  set scrolloff=999
  Limelight
  SoftPencil
  set wrap
  set linebreak
  " ...
endfunction

let g:limelight_conceal_ctermfg = 100
let g:limelight_conceal_guifg = '#83a598'

function! s:goyo_leave()
  set showmode
  set showcmd
  set scrolloff=5
  Limelight!
  PencilOff
  set nowrap
  set nolinebreak
  " ...
endfunction

autocmd! User GoyoEnter nested call <SID>goyo_enter()
autocmd! User GoyoLeave nested call <SID>goyo_leave()

let g:goyo_width = 140
let g:goyo_height = 95

let g:rustfmt_autosave = 1

" navigate chunks of current buffer
nmap [g <Plug>(coc-git-prevchunk)
nmap ]g <Plug>(coc-git-nextchunk)
" show chunk diff at current position
nmap gs <Plug>(coc-git-chunkinfo)

lua <<EOF
require'nvim-treesitter.configs'.setup {
  ensure_installed = { "typescript", "tsx", "javascript", "json", "html", "css", "bash" },
  highlight = {
    enable = true,              -- false will disable the whole extension
  },
}
EOF

" Run jest for current project
command! -nargs=0 Jest :call  CocAction('runCommand', 'jest.projectTest')
" Run jest for current file
command! -nargs=0 JestCurrent :call  CocAction('runCommand', 'jest.fileTest', ['%'])
" Run jest for current test
nnoremap <leader>te :call CocAction('runCommand', 'jest.singleTest')<CR>

nnoremap <silent> <space>y  :<C-u>CocList -A --normal yank<cr>

" Hard time
let g:hardtime_default_on = 0

nnoremap <Leader>gy :.GBrowse!<CR>
xnoremap <Leader>gy :'<'>GBrowse!<CR>
autocmd FileType json setfiletype jsonc
autocmd BufRead,BufNewFile *.json set filetype=jsonc
xnoremap <Leader>gm <Plug>(git-messenger)

set cursorline 
set winblend=0
set pumblend=5

imap <M-i> <Plug>(copilot-next)
imap <M-u> <Plug>(copilot-previous)

" silence healthcheck warnings
let g:loaded_perl_provider = 0
let g:loaded_node_provider = 0
let g:loaded_ruby_provider = 0
