from ast import *

class VarsVisitor:
    def __init__(self):
        self._vars = set()

    @property
    def vars(self):
        return self._vars

    def visit_ArithLit(self, val):
        pass

    def visit_ArithVar(self, var):
        self._vars.add(var)

    def visit_ArithBinop(self, op, a1, a2):
        a1.accept(self)
        a2.accept(self)

    def visit_BoolArithCmp(self, op, a1, a2):
        a1.accept(self)
        a2.accept(self)

    def visit_BoolNeg(self, b):
        b.accept(self)

    def visit_StmAssign(self, var, a):
        self._vars.add(var)
        # TODO: we check a just in case
        a.accept(self)

    def visit_StmIf(self, b, ss1, ss2):
        b.accept(self)
        self.visit_many(ss1)
        self.visit_many(ss2)
    
    def visit_StmWhile(self, b, ss):
        b.accept(self)
        self.visit_many(ss)

    def visit_StmPrint(self, a):
        val = a.accept(self)

    def visit_many(self, stms):
        for stm in stms:
            stm.accept(self)

def vars_many(stms):
    """
    Finds the names of all variables used in the program
    """
    visitor = VarsVisitor()
    visitor.visit_many(stms)
    return visitor.vars
