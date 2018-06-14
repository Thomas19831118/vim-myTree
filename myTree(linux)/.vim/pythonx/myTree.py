import vim
import os
import fileTree
import time
import threading
import imp
imp.reload(fileTree)


def show():
    win = findWindow("/@my_tree")
    if win != None:
        vim.current.window = win
        vim.command("q!")
    else:
        constructTreeView()
        mapKeyPresses()


def constructTreeView():
    fileName = vim.current.buffer.name
    vim.command("topleft vertical 40 new @my_tree")    
    vim.win = findWindow("/@my_tree")
    if hasattr(vim,'tree')==False :
        vim.tree = fileTree.fileTree(fileName)
    else:
        vim.tree.setCurrentFile(fileName)
    refreshView(fileName)

def refreshView(fileName = ""):
    currentLine = vim.win.cursor[0]
    vim.current.buffer[:] = None
    vim.current.buffer[0] = "..."
    vim.lineNodes = vim.tree.getTreeLines()
    for item in vim.lineNodes:
        vim.current.buffer.append(item[1])
        if item[0].path() == fileName:
            currentLine = len(vim.current.buffer)
    if currentLine <= len(vim.lineNodes)+1:
        vim.win.cursor = (currentLine,0)

def mapKeyPresses():
    mapKeyPress('i')
    mapKeyPress("o")
    mapKeyPress("a")
    mapKeyPress("p")
    mapKeyPress("r")


def mapKeyPress(key):
    cmd = "nnoremap <silent> <buffer> key :call MyTree_KeyPress('key') <cr>" 
    cmd = cmd.replace("key",key,2)
    vim.command(cmd)


def processKeyPress(key):
    if key == 'p':
        vim.win.width += 1
    if key == 'a':
        vim.win.width -= 1
    currentLine = vim.current.range.start - 1
    needRefresh = False
    if currentLine >= 0:
        currentNode = vim.lineNodes[currentLine][0]
        if key == 'i':
            if currentNode.isDir:
                currentNode.isExpand = not currentNode.isExpand
                if currentNode.isExpand and currentNode.isLoad == False:
                    vim.tree.loadNode(currentNode)
                needRefresh = True
        if key == 'o':
            if currentNode.isDir:
                vim.tree.moveRootDownTo(currentNode)
                currentNode.isExpand = True
                if currentNode.isLoad == False:
                    vim.tree.loadNode(currentNode)
                needRefresh = True    
            else:
                for win in vim.windows:
                    if win != vim.win:
                        vim.current.window = win
                        opencmd = "e " + currentNode.path()
                        try:
                            vim.command(opencmd)
                        except vim.error as e :
                            print(e)
        if key == 'r':
            if currentNode.isDir:
                vim.tree.loadNode(currentNode)
                needRefresh = True
    else:
        if key == 'o':
            vim.tree.moveRootUpToParent()
            needRefresh = True
    
    if needRefresh:        
        refreshView()
    

def findWindow(name):
    for win in vim.windows:
        if win.buffer.name.endswith(name):
            return win
    return None

def refresh():
    vim.command("redraw")
