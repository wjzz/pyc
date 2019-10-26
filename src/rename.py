from ast import *
from collections import defaultdict


class RenameVarsVisitor:
    def __init__(self):
        self._var_counts = defaultdict(int)
        self._history = [self._var_counts.copy()]

    def push_variable(self, var):
        self._var_counts[var] += 1

    def mangle_var(self, var):
        count = self._var_counts[var]
        if count > 1:
            return var + str(count)
        else:
            return var

    def push_block(self):
        self._history.append(self._var_counts.copy())

    def pop_block(self):
        self._var_counts = self._history.pop()

    def visit_ArithLit(self, val):
        return ArithLit(val)

    def visit_Var(self, var):
        var1 = self.mangle_var(var)
        return Var(var1)

    def visit_ArithUnaryop(self, op, a):
        a1 = a.accept(self)
        return ArithUnaryop(op, a1)

    def visit_ArithBinop(self, op, a1, a2):
        a11 = a1.accept(self)
        a21 = a2.accept(self)
        return ArithBinop(op, a11, a21)

    def visit_BoolNeg(self, b):
        b1 = b.accept(self)
        return BoolNeg(b1)

    def visit_BoolArithCmp(self, op, a1, a2):
        a11 = a1.accept(self)
        a21 = a2.accept(self)
        return BoolArithCmp(op, a11, a21)

    def visit_BoolBinop(self, op, b1, b2):
        b11 = b1.accept(self)
        b21 = b2.accept(self)
        return BoolBinop(op, b11, b21)

    def visit_ArithAssign(self, lvalue, a):
        var = lvalue.loc
        var1 = self.mangle_var(var)
        lvalue1 = lvalue.rename(var1)
        a1 = a.accept(self)
        return ArithAssign(lvalue1, a1)

    def visit_StmExpr(self, a):
        a1 = a.accept(self)
        return StmExpr(a1)

    def visit_StmIf(self, b, ss1, ss2):
        b1 = b.accept(self)
        ss11 = self.visit_many(ss1)
        ss21 = self.visit_many(ss2)
        return StmIf(b1, ss11, ss21)

    def visit_StmWhile(self, b, ss):
        b1 = b.accept(self)
        ss1 = self.visit_many(ss)
        return StmWhile(b1, ss1)

    def visit_StmPrint(self, a):
        a1 = a.accept(self)
        return StmPrint(a1)

    def visit_StmReturn(self, a):
        a1 = a.accept(self)
        return StmReturn(a1)

    def visit_StmBreak(self):
        return StmBreak()

    def visit_StmContinue(self):
        return StmContinue()

    def visit_StmBlock(self, stms):
        return StmBlock(self.visit_many(stms))

    def visit_FunDecl(self, type, name, params, body):
        body1 = self.visit_many(body)
        return FunDecl(type, name, params, body1)

    def visit_FunCall(self, name, args):
        args1 = self.visit_many(args)
        return FunCall(name, args1)

    def visit_StmDecl(self, tp, var, a, kind):
        self.push_variable(var)
        var1 = self.mangle_var(var)
        a1 = a.accept(self) if a is not None else None
        return StmDecl(tp, var1, a1, kind)

    def visit_many(self, stms):
        self.push_block()
        stms1 = [stm.accept(self) for stm in stms]
        self.pop_block()
        return stms1


def rename_vars(stms):
    """
    Returns an equivalent program, but one where all
    variables are unique.
    """
    return RenameVarsVisitor().visit_many(stms)
