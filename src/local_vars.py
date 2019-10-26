class LocalVarsVisitor:
    def __init__(self):
        pass

    def visit_ArithLit(self, val):
        return []

    def visit_ArithVar(self, var):
        return []

    def visit_ArithUnaryop(self, op, a):
        return []

    def visit_ArithBinop(self, op, a1, a2):
        return []

    def visit_ArithAssign(self, var, a):
        return []

    def visit_BoolNeg(self, b):
        return []

    def visit_BoolArithCmp(self, op, a1, a2):
        return []

    def visit_StmExpr(self, a):
        return []

    def visit_StmIf(self, b, ss1, ss2):
        return self.visit_many(ss1) + self.visit_many(ss2)

    def visit_StmWhile(self, b, ss):
        return self.visit_many(ss)

    def visit_StmPrint(self, a):
        return []

    def visit_StmReturn(self, a):
        return []

    def visit_StmBreak(self):
        return []

    def visit_StmContinue(self):
        return []

    def visit_StmBlock(self, stms):
        return self.visit_many(stms)

    def visit_FunDecl(self, _type, name, params, body):
        return []

    def visit_FunCall(self, name, args):
        return []

    def visit_StmDecl(self, tp, var, a, kind):
        # a == None means that we only declare the var,
        # without initializing it
        return [var]

    def visit_many(self, stms):
        results = []
        for stm in stms:
            results += stm.accept(self)
        return results


def get_local_vars(stms):
    """
    Returns a list of all local variables defined by the
    given functions body.
    """
    return LocalVarsVisitor().visit_many(stms)
