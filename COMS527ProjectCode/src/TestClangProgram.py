
import sys
import clang.cindex

fpTempFile='/Users/hungphan/git/COMS527/SampleCodes/prutor_no_error7.c'

class ForLocation:
    def __init__(self):
        self.lineNumber=-1
        self.funcName=''
        self.listChildrenFor=[]
        self.fatherNode=None

class Walker:
    def __init__(self, filename):
        self.filename = filename
        self.listForLoops=[]


    def walk(self, node,index):
        node_in_file =  bool(str(node.location.file) == self.filename)
        if node_in_file:
        #     print(f"node.spelling = {node.spelling:14}, node.kind = {node.kind}")
        #     if node.kind == clang.cindex.CursorKind.TEMPLATE_REF:
        #         print(f"node.get_num_template_arguments = {node.get_num_template_arguments()}")
            lstLine=[]
            for i in range(0,index):
                lstLine.append('\t')
            lstLine.append(str(node.location.line))
            lstLine.append(' ')
            lstLine.append(str(node.kind))
            lstLine.append(' ')
            lstLine.append(str(node.spelling))
            strLine=''.join(lstLine)
            print(strLine)
        for child in node.get_children():
            childIndex=index+1
            self.walk(child,childIndex)

index = clang.cindex.Index.create()
tu = index.parse(fpTempFile)
print('{}'.format(tu))
root = tu.cursor
index=0
walker = Walker(fpTempFile)
walker.walk(root,index)