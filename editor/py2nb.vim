" Vim syntax file
" Language:             Python extended with special comments
" Repository:           https://github.com/Equaraphanus/py2nb/editor/py2nb.vim
" Last Change:          2022 Feb 13


" Quit when a syntax file was already loaded
if !exists("main_syntax")
  if exists("b:current_syntax")
    finish
  endif
  let main_syntax = 'py2nb'
endif

let s:cpo_save = &cpo
set cpo&vim



" The syntax is based on python
runtime! syntax/python.vim 
unlet b:current_syntax


" Override markdownLineStart to correctly handle headings, code blocks, etc
syn match markdownLineStart "\(^#: \)\@<=" nextgroup=@markdownBlock,htmlSpecialChar

syn match py2nbSpecialComment "^#\(: \|:$\|=\)" nextgroup=py2nbMarkdownContainer
syn match py2nbMarkdownContainer "\(^#: \)\@<=.*$" contains=@py2nbMarkdownBlock

syn include @py2nbMarkdownBlock $VIMRUNTIME/syntax/markdown.vim
unlet b:current_syntax
syn region py2nbMarkdownComment start="^#:\( \|$\)" end="$" keepend contains=py2nbSpecialComment,py2nbMarkdownContainer


hi link py2nbMarkdownComment Comment
hi link py2nbSpecialComment PreProc




let b:current_syntax = 'py2nb'

if main_syntax == 'py2nb'
  unlet main_syntax
endif

let &cpo = s:cpo_save
unlet s:cpo_save
