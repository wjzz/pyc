from __future__ import annotations

"""
Type checking of C programs.

We check that:
- all names are in scope
- there are no type errors
"""

from typing import Any, Optional, List, Dict

from visitor import Visitor
from ast import FunDecl, LValue, FunArg, FunType
import ast as AST


class CTypeError(Exception):
    def __init__(self, msg):
        self.msg = msg

    def __str__(self):
        return f"{self.msg}"


Stm = Any
Var = str
Tp = AST.CType
Params = List[FunArg]


class Env:
    env: Dict[Var, Tp] = {}

    def __contains__(self, var: Var):
        return var in self.env

    def add(self, var: Var, tp: Tp):
        self.env[var] = tp

    def get(self, var: Var) -> Tp:
        return self.env[var]

    def copy(self) -> Env:
        cp = Env()
        cp.env = self.env.copy()
        return cp

    def __str__(self):
        inside = "\n\t\t".join([f"{k}:{v}" for k, v in self.env.items()])
        return f"[\n\t\t{inside}\n\t]"


class SymbolTable:
    pass


class TypeCheckingVisitor(Visitor):
    symbol_table: SymbolTable = SymbolTable()
    env: Env = Env()

    # environment

    def add_binding(self, var: Var, tp: Tp):
        self.env.add(var, tp)

    def get_binding(self, var: Var) -> Tp:
        return self.env.get(var)

    def expect_bound_var(self, var: Var):
        if var not in self.env:
            raise CTypeError(f"name {var} is not defined in env: {self.env}")

    def expect_function_type(self, var: Var) -> FunType:
        self.expect_bound_var(var)
        c_type: AST.CType = self.get_binding(var)

        if c_type.kind == AST.TypeKind.Pointer:
            raise CTypeError(
                f"{var} should be a function, but it is a pointer type {c_type}"
            )
        assert c_type.kind == AST.TypeKind.Normal

        tp = c_type.type
        if not isinstance(tp, FunType):
            raise CTypeError(f"{var} should be a function, but found type {c_type}")

        assert isinstance(tp, FunType)
        return tp

    # type checking

    def __init__(self):
        pass

    def visit_ArithLit(self, val):
        pass

    def visit_Var(self, var: Var):
        self.expect_bound_var(var)

    def visit_FunCall(self, name: Var, args: List[Any]):
        # TODO: check if C has a different namespace for functions
        # TODO: check if the args have correct types

        fn_type = self.expect_function_type(name)

        expected_num = len(fn_type.args)
        given_num = len(args)
        if expected_num != given_num:
            raise CTypeError(
                f"function {name} got {given_num} args, "
                + "but {expected_num} args were expected"
            )

        self.visit_many(args)

    def visit_ArithUnaryop(self, op, a):
        a.accept(self)

    def visit_ArithBinop(self, op, a1, a2):
        a1.accept(self)
        a2.accept(self)

    def visit_BoolArithCmp(self, op, a1, a2):
        a1.accept(self)
        a2.accept(self)

    def visit_BoolNeg(self, b):
        b.accept(self)

    def visit_BoolBinop(self, op, b1, b2):
        b1.accept(self)
        b2.accept(self)

    def visit_ArithAssign(self, lvalue: LValue, a):
        var: Var = lvalue.loc
        self.expect_bound_var(var)
        a.accept(self)

    def visit_StmExpr(self, a):
        a.accept(self)

    def visit_StmDecl(self, tp: Tp, var: Var, a: Optional[Any], kind):
        if a is not None:
            a.accept(self)
        self.add_binding(var, tp)

    def visit_StmIf(self, b, ss1, ss2):
        b.accept(self)
        self.visit_StmBlock(ss1)
        self.visit_StmBlock(ss2)

    def visit_StmWhile(self, b, ss):
        b.accept(self)
        self.visit_StmBlock(ss)

    def visit_StmPrint(self, a):
        a.accept(self)

    def visit_StmReturn(self, a):
        a.accept(self)

    def visit_StmBreak(self):
        pass

    def visit_StmContinue(self):
        pass

    def visit_StmBlock(self, stms):
        env = self.env.copy()
        self.visit_many(stms)
        self.env = env

    def visit_many(self, stms):
        for stm in stms:
            stm.accept(self)

    def visit_FunDecl(self, tp: Tp, name: Var, params: Params, body: List[Stm]):
        args = [arg.type for arg in params]
        fn_type = AST.tp_normal(FunType(tp, args))

        self.add_binding(name, fn_type)

        env = self.env.copy()

        for funarg in params:
            self.add_binding(funarg.var, funarg.type)

        self.visit_many(body)

        self.env = env

    def visit_many_defs(self, defs):
        fun_names = [defn.name for defn in defs if isinstance(defn, FunDecl)]
        if "main" not in fun_names:
            msg = (
                "A program with function definition must have"
                + " a 'main' function! Aborting..."
            )
            raise CTypeError(msg)

        return self.visit_many(defs)


def check(defs: List[Stm]) -> SymbolTable:
    """
    Type checks the given program and returns a symbol table
    containing the type information for all nodes in the program.

    Raises a CTypeError if there are some problems with the given input.
    """
    visitor = TypeCheckingVisitor()
    visitor.visit_many_defs(defs)
    return visitor.symbol_table
