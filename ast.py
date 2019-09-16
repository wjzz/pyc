from enum import Enum
from collections import namedtuple

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

class ArithVar(namedtuple('ArithVar', 'var')):
    def __str__(self):
        return self.var

    def accept(self, visitor):
        return visitor.visit_ArithVar(self.var)

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
# Statements
#-----------------------------------------

class StmAssign(namedtuple("StmAssign", "var a")):
    def __str__(self):
        return f"{self.var} = {self.a};"
    
    def accept(self, visitor):
        return visitor.visit_StmAssign(self.var, self.a)

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
        return f"print {self.a};"
    
    def accept(self, visitor):
        return visitor.visit_StmPrint(self.a)

class StmReturn(namedtuple("StmReturn", "a")):
    def __str__(self):
        return f"return {self.a};"

    def accept(self, visitor):
        return visitor.visit_StmReturn(self.a)


#-----------------------------------------
# Tests
#-----------------------------------------

if __name__ == "__main__":
    ops = list(ArithOp)
    print(ops) # uses repr
    print(list(map(str, ops)))

    bops = list(ArithCmp)
    print(list(map(str, bops)))

    var = ArithVar("x")
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
