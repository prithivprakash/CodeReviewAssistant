import ast

class pythonAnalyzer(ast.NodeVisitor):
    def __init__(self):
        self.loopCount = 0
        self.maxLoopDepth = 0
        self.currentLoopCount = 0
        self.recursiveCalls = False
        self.functionNames = set()
        self.usesGlobal = False
        self.usesEval = False
        self.functionLength = 0

    def visitFor(self, node):
        self._enterLoop()
        self.generic_visit(node)
        self._exitLoop()
    
    def visitWhile(self, node):
        self._enterLoop()
        self.generic_visit(node)
        self._exitLoop()
    
    def _enterLoop(self):
        self.loopCount += 1
        self.currentLoopDepth += 1
        self.maxLoopCount = max(self.maxLoopCount, self.currentLoopDepth)
    
    def _exitLoop(self):
        self.currentLoopDepth -= 1
    
    def visit_FunctionDef(self, node):
        self.functionNames.add(node.name)
        self.functionLength = max(self.functionLength, (node.end_lineno or node.lineno) - node.lineno + 1)
        self.generic_visit(node)

    def visit_Call(self, node):
        if isinstance(node.func, ast.Name):
            if node.func.id in self.functionNames:
                self.recursiveCalls = True
            if node.func.id in {"eval", "exec"}:
                self.usesEval = True
        self.generic_visit(node)

    def visit_Global(self, node):
        self.usesGlobal = True
        self.generic_visit(node)
    

def analyzeCode(code: str) -> dict:
    try:
        tree = ast.parse(code)
    except SyntaxError as e:
        return {
            "syntaxError" : True,
            "message" : str(e)
        }
    
    analyzer = pythonAnalyzer()
    analyzer.visit(tree)

    return {
        "syntaxError" : False,
        "loopCount" : analyzer.loopCount,
        "maxLoopDepth" : analyzer.maxLoopDepth,
        "hasNestedLoops" : analyzer.maxLoopDepth > 1,
        "usesRecursion" : analyzer.recursiveCalls,
        "usesGlobal" : analyzer.usesGlobal,
        "usesEval" : analyzer.usesEval,
        "maxFunctionLength" : analyzer.functionLength
    }

