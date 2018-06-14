import os


class Node:
    def __init__(self,name,parent):
        self.name = name
        self.parent = parent
        self.children = []
        self.isLoad = False
        self.isExpand = False
        self.isDir = False

    def path(self):
        dir = self.name
        parent = self.parent
        while parent != None:
            if parent.name != "/":
                dir = parent.name + "/" + dir
            else:
                dir = "/" + dir
            parent = parent.parent
        return dir
            
    def level(self):
        lvl = 0
        parent = self.parent
        while parent != None:
            lvl += 1
            parent = parent.parent
        return lvl

    def isVisible(self):
        parent = self.parent
        while parent != None:
            if parent.isExpand == False:
                return False
            parent = parent.parent
        return True

    def forceVisible(self):
        parent = self.parent
        while parent != None:
            parent.isExpand = True
            parent = parent.parent

    def toString(self,baseLvl):
        dirChar = " "
        if self.isDir:
            if self.isExpand:
                dirChar = "-" #u"\u2193"
            else:
                dirChar = "+" #u"\u2192"
        lvl = self.level()-baseLvl
        name = self.name
        if lvl == 0:
            name = self.path()
        return "    "*lvl + dirChar + name
    
    def addChildren(self,node):
        name = node.name
        for child in self.children:
            if child.name == name:
                return
        self.children.append(node)
        self.children = sorted(self.children,key = lambda Node: str(not Node.isDir) + Node.name)

    def findChildNode(self,name):
        for child in self.children:
            if child.name == name:
                return child
        return None        

    
class fileTree:
    def __init__(self,filePath):
        self.root = None
        self.ultimate_root = None
        self.setCurrentFile(filePath)

    def getTreeLines(self):
        lines = []
        nodes = self.getAllChildrenNodes(self.root)
        if len(nodes) > 0:
            baseLvl = nodes[0].level()
            for node in nodes:
                if node.isVisible():
                    lines.append((node,node.toString(baseLvl)))
        return lines

    def getAllChildrenNodes(self,root):
        nodes = []
        nodes.append(root)
        nodeIndex = 0
        while nodeIndex < len(nodes):
            node = nodes[nodeIndex]
            nodeIndex += 1
            if len(node.children) > 0 :
                nodes[nodeIndex:nodeIndex] = node.children
        return nodes

    def loadNode(self,node):
        items = os.listdir(node.path())
        node.isLoad = True
        for it in items:
            newNode = Node(it,node)
            newNode.isDir = os.path.isdir(newNode.path())
            node.addChildren(newNode)

    def moveRootDownTo(self,node):
        self.root = node 

    def moveRootUpToParent(self):
        if self.root.name == "/":
            return
        if self.root.parent == None:
            parent,name = os.path.split(self.root.name)
            if name != "":
                self.root.name = name
                root = Node(parent,None)
                root.isDir = True
                root.isLoad = True
                root.isExpand = True
                self.root.parent = root
                root.children.append(self.root)
                self.loadNode(root)
        self.root = self.root.parent
            
    def setCurrentFile(self,filePath):
        self.constructUltimateRoot()
        parentDir = filePath
        if os.path.isdir(filePath) == False:
            parentDir,current = os.path.split(filePath)
        if parentDir != "/" and parentDir.endswith("/"):
            parentDir = parentDir[:-1]
        dirs = parentDir.split("/")
        del dirs[0]
        parentNode = self.ultimate_root
        for dir in dirs:
            tmpNode = parentNode.findChildNode(dir)
            if tmpNode == None:
                self.loadNode(parentNode)
            tmpNode = parentNode.findChildNode(dir)
            if tmpNode == None:
                self.root = parentNode
                return
            parentNode = tmpNode
        self.loadNode(parentNode)
        parentNode.isExpand = True
        self.root = parentNode   
        parentNode.forceVisible()
    
    def constructUltimateRoot(self):
        if self.ultimate_root != None:
            return
        self.ultimate_root = Node("/",None)
        self.ultimate_root.isDir = True
        self.loadNode(self.ultimate_root)
            

