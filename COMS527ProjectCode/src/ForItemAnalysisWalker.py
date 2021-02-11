
import sys
import clang.cindex

fpTempFile='/home/hung/git/COMS527_data/SampleCodes/prutor_no_error7.c'

class ForLoopItem:
    def __init__(self):
        self.loopId=-1
        self.setOfLines=[]
        self.currentMethodName=[]
        self.listCodeContent=[]



class ForItemAnalysisWalker:
    def __init__(self, filename):
        self.filename = filename
        self.currentFuncDeclName=''
        self.stackForLoops=[]
        self.listForLoopsAfterVisits=[]
        f1 = open(filename, 'r')
        strF1 = f1.read()
        f1.close()
        self.arrCodes = strF1.split('\n')

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
            #print(strLine)

            if(strNodeType =='FUNCTION_DECL'):
                self.currentFuncDeclName=str(node.spelling)

            if(strNodeType == 'FOR_STMT'):
                itemFor=ForLoopItem()
                itemFor.loopId=len(self.listForLoopsAfterVisits)+1
                itemFor.currentMethodName = self.currentFuncDeclName
                if node.location.line not in itemFor.setOfLines:
                    itemFor.setOfLines.append(node.location.line)
                    itemFor.listCodeContent.append(self.arrCodes[node.location.line - 1])
                self.stackForLoops.append(itemFor)
                #print(strLine)
            elif len(self.stackForLoops)>0:
                itemFor=self.stackForLoops[len(self.stackForLoops)-1]
                if node.location.line not in itemFor.setOfLines:
                    itemFor.setOfLines.append(node.location.line)
                    itemFor.listCodeContent.append(self.arrCodes[node.location.line-1])
                #print('len stack {}'.format(len(self.stackForLoops)))

            #     print(strLine)
            # print(strLine)

        for child in node.get_children():
            childIndex=index+1
            self.walkInForLoop(child,childIndex)
        if (strNodeType == 'FOR_STMT'):
           # print('go here {}'.format(len(self.stackForLoops)))
            if(len(self.stackForLoops)>0):
                itemFor=self.stackForLoops.pop()
                '''
                bigValue=10000*itemFor.setOfLines[len(itemFor.setOfLines)-1]
                itemFor.setOfLines.append(bigValue)
                '''
                itemFor.setOfLines=sorted(set(itemFor.setOfLines))
                #print('set {}'.format(itemFor.setOfLines))
                if not itemFor is None:
                    self.listForLoopsAfterVisits.append(itemFor)
        elif (strNodeType == 'COMPOUND_STMT'):
            if (len(self.stackForLoops) > 0):
                itemFor = self.stackForLoops[len(self.stackForLoops) - 1]
                itemFor.listCodeContent.append('}')




#
index = clang.cindex.Index.create()
tu = index.parse(fpTempFile)
print('{}'.format(tu))
root = tu.cursor
index=0
indexOfForLoop=0
walker = ForItemAnalysisWalker(fpTempFile)
walker.walkInForLoop(root,index)
print('{}\n{}'.format(len(walker.listForLoopsAfterVisits),walker.listForLoopsAfterVisits[0].listCodeContent))
#print('size {} {} '.format(len(walker.listForLoops),walker.listForLoops[0].lineNumber))