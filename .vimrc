set nu
colorscheme mycolor
syntax on
set autoindent
set cindent
set ruler
set tabstop=4
set softtabstop=4
set tabstop=4
set expandtab
filetype on
filetype plugin on
set shiftwidth=4
set wildmenu
set ignorecase
set hlsearch
hi search guibg=lightblue
map <silent> t :MyTree <cr>
map <silent> M :!make <cr>
map <silent> P :!python % <cr>
autocmd BufReadPre,FileReadPre * call MyTree_RecordRecentFile()
