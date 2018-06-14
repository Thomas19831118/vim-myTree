import vim
import os
import fileTree
import time
import threading
import imp
import subprocess

imp.reload(fileTree)

recentFileFileName = "C:\\.recentFile"

def recordRecentFile():
    fileName = vim.current.buffer.name
    if fileName.endswith("@my_tree") == False and fileName != recentFileFileName:
        saveFileNameToRecentFile(fileName)

def saveFileNameToRecentFile(fileName):
    maxRecentFileRecord = 10
    recentFiles = []
    try:
        with open(recentFileFileName) as f:
            recentFiles = f.readlines()
    except:
        pass

    with open(recentFileFileName,"w") as f:
        if fileName + "\n" in recentFiles:
            recentFiles.remove(fileName + "\n")
        else:
            if len(recentFiles) > maxRecentFileRecord:
                del recentFiles[-1]
        tmp = [fileName + "\n"]
        tmp.extend(recentFiles)
        recentFiles = tmp
        f.writelines(recentFiles)

def show():
    win = None
    if hasattr(vim,'win') :
        win = vim.win
    if win != None:
        try:
            vim.current.window = win
            vim.command("q!")
            return
        except vim.error as e:
            pass
    constructTreeView()
    mapKeyPresses()


def constructTreeView():
    fileName = vim.current.buffer.name
    vim.command("topleft vertical 40 new @my_tree")    
    vim.win = findWindow("@my_tree")
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
    vim.help_Infos = "=====???????????---------Help----------???????????=====\r\n"
    mapKeyPress('i',"expand or collapse the node")
    mapKeyPress("o",'open file or set folder as root')
    mapKeyPress("O",'open the selected file anyway and discarde the modification of the current file')
    mapKeyPress("a",'shrink width')
    mapKeyPress("A",'set width to default')
    mapKeyPress("p",'extend width')
    mapKeyPress("R",'show recent file list')
    mapKeyPress("P",'fix width with contents')
    mapKeyPress("r",'update contents of a selected folder')
    mapKeyPress("I",'popup folder explorer or popup file')
    mapKeyPress("T",'create a new tab and open selectted file')
    mapKeyPress("s",'hide the default key',False)
    mapKeyPress("x",'hide the default key',False)
    mapKeyPress("S",'hide the default key',False)
    mapKeyPress("X",'hide the default key',False)
    mapKeyPress("H",'print the help information')

def mapRecentViewKeyPresses():
    vim.help_Infos = "=====???????????---------Help----------???????????=====\r\n"
    mapKeyPress('i',"expand or collapse the node")
    mapKeyPress("o",'open file or set folder as root')
    mapKeyPress("O",'open the selected file anyway and discarde the modification of the current file')
    mapKeyPress("a",'shrink width')
    mapKeyPress("A",'set width to default')
    mapKeyPress("p",'extend width')
    mapKeyPress("R",'show recent file list')
    mapKeyPress("P",'fix width with contents')
    mapKeyPress("r",'update contents of a selected folder')
    mapKeyPress("I",'popup folder explorer or popup file')
    mapKeyPress("T",'create a new tab and open selectted file')
    mapKeyPress("s",'hide the default key',False)
    mapKeyPress("x",'hide the default key',False)
    mapKeyPress("S",'hide the default key',False)
    mapKeyPress("X",'hide the default key',False)
    mapKeyPress("H",'print the help information')



def mapKeyPress(key,info,info_visible=True):
    cmd = "nnoremap <silent> <buffer> key :call MyTree_KeyPress('key') <cr>" 
    cmd = cmd.replace("key",key,2)
    vim.command(cmd)
    if info_visible:
        vim.help_Infos += key + ': ' + info + '\r\n'

def FixWidthWithContent():
    maxLength = 0
    for item in vim.lineNodes:
        if maxLength < len(item[1]):
            maxLength = len(item[1])
    vim.win.width = maxLength + 4

def FixWidthWithBufferContent():
    maxLength = 0
    for line in vim.current.buffer:
        if maxLength < len(line):
            maxLength = len(line)
    vim.win.width = maxLength + 4

def processKeyPress(key):
    if vim.win.buffer.name.endswith("@my_tree"):
        processKeyPress_TreeMode(key)
    else:
        processKeyPress_RecentMode(key)


def processKeyPress_RecentMode(key):
    if key == 'H':
        print(vim.help_Infos)
    if key == 'p':
        vim.win.width += 1
    if key == 'a':
        vim.win.width -= 1
    if key == 'A':
        vim.win.width = 40
    if key == 'P':
        FixWidthWithBufferContent()
    if key == 'R':
        opencmd = "e! @my_tree"   
        vim.command(opencmd)
        refreshView()
        mapKeyPresses()   
    if key == 'o' or key == 'O':
        fileName = vim.current.line
        for win in vim.windows:
            if win != vim.win:
                vim.current.window = win
                opencmd = "e"
                if key == 'O':
                    opencmd += "!"
                opencmd += " " + fileName
                print(vim.current.line)
                try:
                    vim.command(opencmd)
                except vim.error as e :
                    print(e)
                    vim.current.window = vim.win
                break


def processKeyPress_TreeMode(key):
    if key == 'H':
        print(vim.help_Infos)
    if key == 'p':
        vim.win.width += 1
    if key == 'a':
        vim.win.width -= 1
    if key == 'A':
        vim.win.width = 40
    if key == 'P':
        FixWidthWithContent()
    if key == 'R':
        opencmd = "e! " + recentFileFileName   
        vim.command(opencmd)
        mapRecentViewKeyPresses()
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
        if key == 'o' or key == 'O':
            if currentNode.isDir:
                vim.tree.moveRootDownTo(currentNode)
                currentNode.isExpand = True
                if currentNode.isLoad == False:
                    vim.tree.loadNode(currentNode)
                needRefresh = True    
               #try:
               #    vim.command("cd " + currentNode.path())
               #except vim.error as e :
               #    print(e)
            else:
                for win in vim.windows:
                    if win != vim.win:
                        vim.current.window = win
                        opencmd = "e"
                        if key == 'O':
                            opencmd += "!"
                        opencmd += " " + currentNode.path()
                        try:
                            vim.command(opencmd)
                            vim.command("cd " + currentNode.parent.path())
                        except vim.error as e :
                            print(e)
                            vim.current.window = vim.win
                        break
        if key == 'I':
            current_dir = currentNode.path()
            if not currentNode.isDir:
                current_dir = currentNode.parent.path()       
            subprocess.call('explorer "' + current_dir + '"')
        if key == 'T':
            if not currentNode.isDir:
                current_dir = currentNode.path()
                vim.command("tabnew")
                vim.command('e ' + current_dir)
        if key == 'r':
            node = currentNode
            if not currentNode.isDir:
                node = currentNode.parent
            vim.tree.loadNode(node)
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
