
import sys
import clang.cindex

fpTempFile='/Users/hungphan/git/COMS527/SampleCodes/prutor_no_error7.c'

class ForLoopItem:
    def __init__(self):
        self.loopId=-1
        self.setOfLines=[]
        self.currentMethodName=[]



class ForItemAnalysisWalker:
    def __init__(self, filename):
        self.filename = filename
        self.currentFuncDeclName=''
        self.stackForLoops=[]
        self.listForLoopsAfterVisits=[]

    def walkInForLoop(self, node,index):
        node_in_file =  bool(str(node.location.file) == self.filename)
        strNodeType = str(node.kind).replace('CursorKind.', '')
        # print(strNodeType)
        if node_in_file:
        #     print(f"node.spelling = {node.spelling:14}, node.kind = {node.kind}")
        #     if node.kind == clang.cindex.CursorKind.TEMPLATE_REF:
        #         print(f"node.get_num_template_arguments = {node.get_num_template_arguments()}")
            lstLine=[]
            for i in range(0,index):
                lstLine.append('\t')

            lstLine.append(' ')
            lstLine.append(str(node))
            lstLine.append(str(node.location.line))
            lstLine.append(' ')
            lstLine.append(str(node.kind))
            lstLine.append(' ')
            lstLine.append(str(node.spelling))
            strLine=''.join(lstLine)
            # print(strLine)
            if(strNodeType =='FUNCTION_DECL'):
                self.currentFuncDeclName=str(node.spelling)

            if(strNodeType == 'FOR_STMT'):
                itemFor=ForLoopItem()
                itemFor.loopId=len(self.listForLoopsAfterVisits)+1
                itemFor.setOfLines.append(node.location.line)
                itemFor.currentMethodName=self.currentFuncDeclName
                self.stackForLoops.append(itemFor)
                # print(strLine)
            elif len(self.stackForLoops)>0:
                itemFor=self.stackForLoops[len(self.stackForLoops)-1]
                itemFor.setOfLines.append(node.location.line)
            #     print(strLine)
            # print(strLine)

        for child in node.get_children():
            childIndex=index+1
            self.walkInForLoop(child,childIndex)
        if (strNodeType == 'FOR_STMT'):
            if(len(self.stackForLoops)>0):
                itemFor=self.stackForLoops.pop()
                bigValue=-10000*itemFor.setOfLines[len(itemFor.setOfLines)-1]
                itemFor.setOfLines.append(bigValue)
                itemFor.setOfLines=set(itemFor.setOfLines)
                # print('set {}'.format(itemFor.setOfLines))
                if not itemFor is None:
                    self.listForLoopsAfterVisits.append(itemFor)




#
# index = clang.cindex.Index.create()
# tu = index.parse(fpTempFile)
# print('{}'.format(tu))
# root = tu.cursor
# index=0
# indexOfForLoop=0
# walker = ForItemAnalysisWalker(fpTempFile)
# walker.walkInForLoop(root,index)
# print('{}\n{}'.format(len(walker.listForLoopsAfterVisits),len(walker.listForLoopsAfterVisits[0].setOfLines)))
# # print('size {} {} '.format(len(walker.listForLoops),walker.listForLoops[0].lineNumber))