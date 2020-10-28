from __future__ import annotations
from enum import Enum
from typing import Optional, Any
from dataclasses import dataclass

# -----------------------------------------
# Types
# -----------------------------------------

class Type:
    """Abstract Type class"""

class AtomType(Type, Enum):
    Int = "int"
    Long = "long"
    Void = "void"
    Char = "char"

    def __str__(self):
        return self.value


@dataclass(frozen=True)
class FunType(Type):
    ret: CType
    args: list[CType]

    def __str__(self):
        args = ",".join(map(str, self.args))
        return f"({args}) -> {self.ret}"


class TypeKind(Enum):
    Normal = "normal"
    Pointer = "pointer"

    def __str__(self):
        return self.value


@dataclass(frozen=True)
class CType():
    kind: TypeKind
    type: Type

    def __str__(self):
        stype = str(self.type)
        if self.kind == TypeKind.Normal:
            return stype
        elif self.kind == TypeKind.Pointer:
            return f"{stype}*"


def tp_normal(atomic):
    return CType(TypeKind.Normal, atomic)


def tp_pointer(atomic):
    return CType(TypeKind.Pointer, atomic)


class VarKind(Enum):
    Local = "local"
    Global = "global"
    Static = "static"

    def __str__(self):
        return self.value


# -----------------------------------------
# Arithmetic operations
# -----------------------------------------


class ArithUnaryOp(Enum):
    Deref = "*"
    Addr = "&"


class ArithOp(Enum):
    Add = "+"
    Sub = "-"
    Mul = "*"
    Div = "/"
    Mod = "%"

    def __str__(self):
        return self.value


class LValueKind(Enum):
    Var = "var"
    Pointer = "pointer"

    def __str__(self):
        return self.value


@dataclass(frozen=True)
class LValue:
    kind: LValueKind
    loc: str

    def __str__(self) -> str:
        s = str(self.loc)
        if self.kind == LValueKind.Pointer:
            return f"*{s}"
        else:
            return s

    def rename(self, var: str) -> LValue:
        if self.kind == LValueKind.Pointer:
            return lvalue_pointer(var)
        else:
            return lvalue_var(var)

    @property
    def expr(self) -> Arith:
        if self.kind == LValueKind.Var:
            return Var(self.loc)
        else:
            return ArithUnaryop(ArithUnaryOp.Deref, Var(self.loc))


def lvalue_var(var: str) -> LValue:
    return LValue(LValueKind.Var, var)


def lvalue_pointer(var: str) -> LValue:
    return LValue(LValueKind.Pointer, var)


class Expr:
    """Absract Expr class"""

class Arith(Expr):
    """Abstract Arith class"""


@dataclass(frozen=True)
class Var(Arith):
    var: str

    def __str__(self):
        return self.var

    def accept(self, visitor):
        return visitor.visit_Var(self.var)


@dataclass(frozen=True)
class ArithLit(Arith):
    num: int

    def __str__(self):
        return str(self.num)

    def accept(self, visitor):
        return visitor.visit_ArithLit(self.num)


@dataclass(frozen=True)
class ArithUnaryop(Arith):
    op: ArithUnaryOp
    a: Expr

    def __str__(self):
        [op, a] = [self.op, self.a]
        return f"({op} {a})"

    def accept(self, visitor):
        return visitor.visit_ArithUnaryop(self.op, self.a)


@dataclass(frozen=True)
class ArithBinop(Arith):
    op: ArithOp
    a1: Expr
    a2: Expr

    def __str__(self):
        [op, a1, a2] = [self.op, self.a1, self.a2]
        return f"({a1} {op} {a2})"

    def accept(self, visitor):
        return visitor.visit_ArithBinop(self.op, self.a1, self.a2)


@dataclass(frozen=True)
class ArithAssign(Arith):
    lvalue: LValue
    a: Expr

    def __str__(self):
        return f"{self.lvalue} = {self.a};"

    def accept(self, visitor):
        return visitor.visit_ArithAssign(self.lvalue, self.a)


# TODO: at first we will include this as syntactic sugar only!
#
# class StmAssignCompound(namedtuple("StmAssign", "var op a")):
#     def __str__(self):
#         return f"{self.var} {self.op}= {self.a};"

#     def accept(self, visitor):
#         return visitor.visit_StmAssignCompound(self.var, self.op, self.a)


# -----------------------------------------
# Boolean operations
# -----------------------------------------


class ArithCmp(Enum):
    Eq = "=="
    Neq = "!="
    Leq = "<="
    Lt = "<"
    Geq = ">="
    Gt = ">"

    def __str__(self):
        return self.value

class BoolExpr(Expr):
    """Abstract BoolExpr class"""

@dataclass(frozen=True)
class BoolArithCmp(BoolExpr):
    op: ArithCmp
    a1: Expr
    a2: Expr

    def __str__(self):
        [op, a1, a2] = [self.op, self.a1, self.a2]
        return f"({a1} {op} {a2})"

    def accept(self, visitor):
        return visitor.visit_BoolArithCmp(self.op, self.a1, self.a2)

@dataclass(frozen=True)
class BoolNeg(BoolExpr):
    b: Expr

    def __str__(self):
        return f"(not {self.b})"

    def accept(self, visitor):
        return visitor.visit_BoolNeg(self.b)


class BoolOp(Enum):
    And = "&&"
    Or = "||"

    def __str__(self):
        return self.value


@dataclass(frozen=True)
class BoolBinop(BoolExpr):
    op: BoolOp
    b1: Expr
    b2: Expr

    def __str__(self):
        [op, b1, b2] = [self.op, self.b1, self.b2]
        return f"({b1} {op} {b2})"

    def accept(self, visitor):
        return visitor.visit_BoolBinop(self.op, self.b1, self.b2)


# -----------------------------------------
# Other expressions
# -----------------------------------------


@dataclass(frozen=True)
class FunCall(Arith):
    name: str
    args: list[Any]

    def __str__(self):
        args = ", ".join(map(str, self.args))
        return f"{self.name}({args})"

    def accept(self, visitor):
        return visitor.visit_FunCall(self.name, self.args)


# -----------------------------------------
# Statements
# -----------------------------------------

class Decl:
    """Abstract declaration type"""

class Stm:
    """Abstract Statement class"""

@dataclass(frozen=True)
class StmExpr(Stm):
    a: Expr

    def __str__(self):
        return str(self.a)

    def accept(self, visitor):
        return visitor.visit_StmExpr(self.a)

@dataclass(frozen=True)
class StmDecl(Stm, Decl):
    type: CType
    var: str
    a: Optional[Expr]
    kind: VarKind = VarKind.Local

    def __str__(self):
        if self.a is not None:
            return f"{self.type} {self.var} = {self.a};"
        else:
            return f"{self.type} {self.var};"

    def accept(self, visitor):
        return visitor.visit_StmDecl(self.type, self.var, self.a, self.kind)

@dataclass(frozen=True)
class StmIf(Stm):
    b: Expr
    ss1: list[Stm]
    ss2: list[Stm]

    def __str__(self):
        ss1 = "\n".join(map(str, self.ss1))
        ss2 = "\n".join(map(str, self.ss2))
        return f"if {self.b} {{\n\t{ss1}\n}} else {{\n\t{ss2}\n}}"

    def accept(self, visitor):
        return visitor.visit_StmIf(self.b, self.ss1, self.ss2)

@dataclass(frozen=True)
class StmWhile(Stm):
    b: Expr
    ss: list[Stm]

    def __str__(self):
        ss = "\n".join(map(str, self.ss))
        return f"while {self.b} {{\n\t{ss}\n}}"

    def accept(self, visitor):
        return visitor.visit_StmWhile(self.b, self.ss)

@dataclass(frozen=True)
class StmPrint(Stm):
    a: Expr

    def __str__(self):
        return f"print({self.a});"

    def accept(self, visitor):
        return visitor.visit_StmPrint(self.a)


@dataclass(frozen=True)
class StmReturn(Stm):
    a: Expr

    def __str__(self):
        return f"return {self.a};"

    def accept(self, visitor):
        return visitor.visit_StmReturn(self.a)

@dataclass(frozen=True)
class StmBreak(Stm):
    def __str__(self):
        return "break;"

    def accept(self, visitor):
        return visitor.visit_StmBreak()

@dataclass(frozen=True)
class StmContinue(Stm):
    def __str__(self):
        return "continue;"

    def accept(self, visitor):
        return visitor.visit_StmContinue()

@dataclass(frozen=True)
class StmBlock(Stm):
    ss: list[Stm]

    def __str__(self):
        ss = "\n".join(map(str, self.ss))
        return f"{{\n\t{ss}\n}}"

    def accept(self, visitor):
        return visitor.visit_StmBlock(self.ss)


# -----------------------------------------
# Top level declarations
# -----------------------------------------

@dataclass(frozen=True)
class FunArg():
    type: CType
    var: str

    def __str__(self):
        return f"{self.type} {self.var}"

@dataclass(frozen=True)
class FunDecl(Decl):
    type: CType
    name: str
    params: list[FunArg]
    body: list[Stm]

    def __str__(self):
        params = ", ".join(map(str, self.params))
        ss = "\n".join(map(str, self.body))
        return f"{self.type} {self.name}({params}) {{\n\t{ss}\n}}"

    def accept(self, visitor):
        return visitor.visit_FunDecl(self.type, self.name, self.params, self.body)


# -----------------------------------------
# Tests
# -----------------------------------------

if __name__ == "__main__":
    ops = list(ArithOp)
    print(ops)  # uses repr
    print(list(map(str, ops)))

    bops = list(ArithCmp)
    print(list(map(str, bops)))

    var = Var("x")
    lit = ArithLit(123)
    abinop = ArithBinop(ArithOp.Add, var, lit)
    bex = BoolArithCmp(ArithCmp.Leq, var, lit)
    assignex = StmExpr(ArithAssign(lvalue_var("x"), abinop))
    exprs = [
        var,
        lit,
        abinop,
        bex,
        BoolNeg(bex),
        BoolBinop(BoolOp.And, bex, BoolNeg(bex)),
        BoolBinop(BoolOp.Or, bex, BoolNeg(bex)),
        assignex,
        StmIf(bex, [assignex], [assignex]),
        StmWhile(bex, [assignex, assignex]),
        StmPrint(var),
        StmReturn(var),
    ]
    for e in exprs:
        print(e)
