function! MyTree()
python3<<EOP
import myTree
import imp
imp.reload(myTree)
myTree.show()
EOP
endfunction

function! MyTree_KeyPress(arg1)
python3<<EOP
import vim
import imp
import myTree
imp.reload(myTree)
myTree.processKeyPress(vim.eval("a:arg1"))
EOP
endfunction

command! -nargs=0 MyTree call MyTree() 
