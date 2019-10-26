"""
A generic visitor that all the others should inherit from.

This way we will know if some methods are missing even before we run the code.
"""

from abc import ABC, abstractmethod

class Visitor(ABC):

    @abstractmethod
    def visit_ArithLit(self, val):
        ...

    @abstractmethod
    def visit_Var(self, var):
        ...

    @abstractmethod
    def visit_FunCall(self, name, args):
        ...

    @abstractmethod
    def visit_ArithUnaryop(self, op, a):
        ...

    @abstractmethod
    def visit_ArithBinop(self, op, a1, a2):
        ...

    @abstractmethod
    def visit_BoolArithCmp(self, op, a1, a2):
        ...

    @abstractmethod
    def visit_BoolNeg(self, b):
        ...

    @abstractmethod
    def visit_BoolBinop(self, op, b1, b2):
        ...

    @abstractmethod
    def visit_ArithAssign(self, lvalue, a):
        ...

    @abstractmethod
    def visit_StmExpr(self, a):
        ...

    @abstractmethod
    def visit_StmDecl(self, tp, var, a, kind):
        ...

    @abstractmethod
    def visit_StmIf(self, b, ss1, ss2):
        ...

    @abstractmethod
    def visit_StmWhile(self, b, ss):
        ...

    @abstractmethod
    def visit_StmPrint(self, a):
        ...

    @abstractmethod
    def visit_StmReturn(self, a):
        ...

    @abstractmethod
    def visit_StmBreak(self):
        ...

    @abstractmethod
    def visit_StmContinue(self):
        ...

    @abstractmethod
    def visit_StmBlock(self, stms):
        ...

    @abstractmethod
    def visit_many(self, stms):
        ...

    @abstractmethod
    def visit_FunDecl(self, type, name, params, body):
        ...

    @abstractmethod
    def visit_many_defs(self, defs):
        ...
