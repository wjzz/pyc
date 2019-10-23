from enum import Enum
from collections import namedtuple


#-----------------------------------------
# Types
#-----------------------------------------

class AtomType(Enum):
    Int = "int"
    Long = "long"
    Void = "void"
    Char = "char"

    def __str__(self):
        return self.value

class TypeKind(Enum):
    Normal = "normal"
    Pointer = "pointer"

    def __str__(self):
        return self.value

class CType(namedtuple("CType", "kind type")):
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

#-----------------------------------------
# Arithmetic operations
#-----------------------------------------

class ArithOp(Enum):
    Add = "+"
    Sub = "-"
    Mul = "*"
    Div = "/"
    Mod = "%"

    def __str__(self):
        return self.value

class Var(namedtuple('Var', 'var')):
    def __str__(self):
        return self.var

    def accept(self, visitor):
        return visitor.visit_Var(self.var)

class ArithLit(namedtuple('ArithLit', 'num')):
    def __str__(self):
        return str(self.num) 
    
    def accept(self, visitor):
        return visitor.visit_ArithLit(self.num)

class ArithBinop(namedtuple('ArithBinop', 'op a1 a2')):
    def __str__(self):
        [op, a1, a2] = [self.op, self.a1, self.a2]
        return f"({a1} {op} {a2})"

    def accept(self, visitor):
        return visitor.visit_ArithBinop(self.op, self.a1, self.a2)

#-----------------------------------------
# Boolean operations
#-----------------------------------------

class ArithCmp(Enum):
    Eq  = "=="
    Neq = "!="
    Leq = "<="
    Lt  = "<"
    Geq = ">="
    Gt  = ">"

    def __str__(self):
        return self.value

class BoolArithCmp(namedtuple("BoolArithCmp", "op a1 a2")):
    def __str__(self):
        [op, a1, a2] = [self.op, self.a1, self.a2]
        return f"({a1} {op} {a2})"

    def accept(self, visitor):
        return visitor.visit_BoolArithCmp(self.op, self.a1, self.a2)

class BoolNeg(namedtuple("BoolNeg", "b")):
    def __str__(self):
        return f"(not {self.b})"

    def accept(self, visitor):
        return visitor.visit_BoolNeg(self.b)

class BoolOp(Enum):
    And = "&&"
    Or  = "||"

    def __str__(self):
        return self.value

class BoolBinop(namedtuple("BoolBinop", "op b1 b2")):
    def __str__(self):
        [op, b1, b2] = [self.op, self.b1, self.b2]
        return f"({b1} {op} {b2})"

    def accept(self, visitor):
        return visitor.visit_BoolBinop(self.op, self.b1, self.b2)

#-----------------------------------------
# Other expressions
#-----------------------------------------

class FunCall(namedtuple("FunCall", "name args")):

    def __str__(self):
        args = ", ".join(map(str, self.args))
        return f"{self.name}({args})"

    def accept(self, visitor):
        return visitor.visit_FunCall(self.name, self.args)

#-----------------------------------------
# Statements
#-----------------------------------------

class StmDecl(namedtuple("StmDecl", "type var a kind", 
  defaults=(None, VarKind.Local))):
    def __str__(self):
        if self.a is not None:
            return f"{self.type} {self.var} = {self.a};"
        else: 
            return f"{self.type} {self.var};"
    
    def accept(self, visitor):
        return visitor.visit_StmDecl(
            self.type, self.var, self.a, self.kind)

class StmAssign(namedtuple("StmAssign", "var a")):
    def __str__(self):
        return f"{self.var} = {self.a};"
    
    def accept(self, visitor):
        return visitor.visit_StmAssign(self.var, self.a)

# TODO: at first we will include this as syntactic sugar only!
# 
# class StmAssignCompound(namedtuple("StmAssign", "var op a")):
#     def __str__(self):
#         return f"{self.var} {self.op}= {self.a};"
    
#     def accept(self, visitor):
#         return visitor.visit_StmAssignCompound(self.var, self.op, self.a)

class StmIf(namedtuple('StmIf', "b ss1 ss2")):
    def __str__(self):
        ss1 = "\n".join(map(str, self.ss1))
        ss2 = "\n".join(map(str, self.ss2))
        return f"if {self.b} {{\n\t{ss1}\n}} else {{\n\t{ss2}\n}}"

    def accept(self, visitor):
        return visitor.visit_StmIf(self.b, self.ss1, self.ss2)

class StmWhile(namedtuple('StmWhile', "b ss")):
    def __str__(self):
        ss = "\n".join(map(str, self.ss))
        return f"while {self.b} {{\n\t{ss}\n}}"

    def accept(self, visitor):
        return visitor.visit_StmWhile(self.b, self.ss)

class StmPrint(namedtuple("StmPrint", "a")):
    def __str__(self):
        return f"print({self.a});"
    
    def accept(self, visitor):
        return visitor.visit_StmPrint(self.a)

class StmReturn(namedtuple("StmReturn", "a")):
    def __str__(self):
        return f"return {self.a};"

    def accept(self, visitor):
        return visitor.visit_StmReturn(self.a)

class StmBreak(namedtuple("StmBreak", "")):
    def __str__(self):
        return f"break;"

    def accept(self, visitor):
        return visitor.visit_StmBreak()

class StmContinue(namedtuple("StmContinue", "")):
    def __str__(self):
        return f"continue;"

    def accept(self, visitor):
        return visitor.visit_StmContinue()

class StmBlock(namedtuple("StmBlock", "ss")):
    def __str__(self):
        ss = "\n".join(map(str, self.ss))
        return f"{{\n\t{ss}\n}}"
    
    def accept(self, visitor):
        return visitor.visit_StmBlock(self.ss)

#-----------------------------------------
# Top level declarations
#-----------------------------------------

class FunArg(namedtuple("FunArg", "type var")):
    def __str__(self):
        return f"{self.type} {self.var}"

class FunDecl(namedtuple("FunDecl", "type name params body")):
    def __str__(self):
        params = ", ".join(map(str, self.params))
        ss = "\n".join(map(str, self.body))
        return f"{self.type} {self.name}({params}) {{\n\t{ss}\n}}"

    def accept(self, visitor):
        return visitor.visit_FunDecl(self.type, self.name, self.params, self.body)

#-----------------------------------------
# Tests
#-----------------------------------------

if __name__ == "__main__":
    ops = list(ArithOp)
    print(ops) # uses repr
    print(list(map(str, ops)))

    bops = list(ArithCmp)
    print(list(map(str, bops)))

    var = Var("x")
    lit = ArithLit(123)
    abinop = ArithBinop(ArithOp.Add, var, lit)
    bex = BoolArithCmp(ArithCmp.Leq, var, lit)
    assignex = StmAssign("x", abinop)
    exprs = [
        var,
        lit,
        abinop,
        bex,
        BoolNeg(bex),
        BoolBinop(
            BoolOp.And,
            bex,
            BoolNeg(bex)
        ),
        BoolBinop(
            BoolOp.Or,
            bex,
            BoolNeg(bex)
        ),
        assignex,
        StmIf(bex, [assignex], [assignex]),
        StmWhile(bex, [assignex, assignex]),
        StmPrint(var),
        StmReturn(var),
    ]
    for e in exprs:
        print(e)
