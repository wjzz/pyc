"""
Interpreter for SIL. Used only as a sanity check.
"""

from collections import defaultdict
from ast import *

class InterpretVisitor:
    def __init__(self):
        self.state = defaultdict(int)

    def visit_ArithLit(self, val):
        return val

    def visit_ArithVar(self, var):
        return self.state[var]

    def visit_ArithBinop(self, op, a1, a2):
        v1 = a1.accept(self)
        v2 = a2.accept(self)
        if op == ArithOp.Add:
            return v1 + v2
        if op == ArithOp.Sub:
            return v1 - v2
        if op == ArithOp.Mul:
            return v1 * v2
        if op == ArithOp.Div:
            return v1 // v2
        if op == ArithOp.Mod:
            return v1 % v2

    def visit_BoolArithCmp(self, op, a1, a2):
        v1 = a1.accept(self)
        v2 = a2.accept(self)
        if op == ArithCmp.Eq:
            return v1 == v2
        if op == ArithCmp.Neq:
            return v1 != v2
        if op == ArithCmp.Leq:
            return v1 <= v2
        if op == ArithCmp.Lt:
            return v1 < v2
        if op == ArithCmp.Geq:
            return v1 >= v2
        if op == ArithCmp.Gt:
            return v1 > v2

    def visit_BoolNeg(self, b):
        return not (b.accept(self))

    def visit_BoolBinop(self, op, b1, b2):
        v1 = b1.accept(self)
        if op == BoolOp.Or:
            return v1 or b2.accept(self)
        elif op == BoolOp.And:
            return v1 and b2.accept(self)

    def visit_StmAssign(self, var, a):
        val = a.accept(self)
        self.state[var] = val

    def visit_StmIf(self, b, ss1, ss2):
        val = b.accept(self)
        if val:
            self.visit_many(ss1)
        else:
            self.visit_many(ss2)
    
    def visit_StmWhile(self, b, ss):
        while b.accept(self):
            self.visit_many(ss)

    def visit_StmPrint(self, a):
        val = a.accept(self)
        print(val)

    def visit_many(self, stms):
        for stm in stms:
            stm.accept(self)

def interpret_many(stms):
    InterpretVisitor().visit_many(stms)

#----------------------------------
#      Example programs in SIL
#----------------------------------

def example0():
    """
    print 15
    """
    
    return [
        StmPrint(ArithLit(15))
    ]


def example01():
    """
    print ((1 + 2) + (3 + 4))
    """
    return [
        StmPrint(
            ArithBinop(
                ArithOp.Add,
                ArithBinop(
                    ArithOp.Add,
                    ArithLit(1),
                    ArithLit(2),
                ),
                ArithBinop(
                    ArithOp.Add,
                    ArithLit(3),
                    ArithLit(4),
                ),
            )
        )
    ]

def example1():
    """
    x = 10
    print x
    """
    return [
        StmAssign("x", ArithLit(10)),
        StmPrint(ArithVar("x")),
    ]

def example2():
    """
    x = 10
    if x % 2 == 0:
        print 0
    else:
        print 1
    """
    return [
        StmAssign("x", ArithLit(10)),
        StmIf(
            BoolArithCmp(
                ArithCmp.Eq,
                ArithBinop(
                    ArithOp.Mod,
                    ArithVar("x"),
                    ArithLit(2)),
                ArithLit(0)),
            [
                StmPrint(ArithLit(0))
            ],
            [
                StmPrint(ArithLit(1))
            ]
        )
    ]

def example3():
    """
    # iterative fibonacci
    x = 0
    y = 1
    n = 20
    while n > 0:
      print x
      y = x + y
      x = y - x
      n = n -1
    """
    return [
        StmAssign("x", ArithLit(0)),
        StmAssign("y", ArithLit(1)),
        StmAssign("n", ArithLit(20)),
        StmWhile(
            BoolArithCmp(
                ArithCmp.Gt,
                ArithVar("n"),
                ArithLit(0)
            ),
            [
                StmPrint(ArithVar("x")),
                StmAssign("y", 
                    ArithBinop(
                        ArithOp.Add,
                        ArithVar("x"),
                        ArithVar("y")
                )),
                StmAssign("x", 
                    ArithBinop(
                        ArithOp.Sub,
                        ArithVar("y"),
                        ArithVar("x")
                )),
                StmAssign("n", 
                    ArithBinop(
                        ArithOp.Sub,
                        ArithVar("n"),
                        ArithLit(1)
                )),
            ]
        ),
    ]

# two ifs
def example4():
    """
    x = 10
    if x % 2 == 0:
        print 0
    else:
        print 1
    if x % 3 == 0:
        print 0
    else:
        print 1
    
    """
    return [
        StmAssign("x", ArithLit(10)),
        StmIf(
            BoolArithCmp(
                ArithCmp.Eq,
                ArithBinop(
                    ArithOp.Mod,
                    ArithVar("x"),
                    ArithLit(2)),
                ArithLit(0)),
            [
                StmPrint(ArithLit(0))
            ],
            [
                StmPrint(ArithLit(1))
            ]
        ),
        StmIf(
            BoolArithCmp(
                ArithCmp.Eq,
                ArithBinop(
                    ArithOp.Mod,
                    ArithVar("x"),
                    ArithLit(3)),
                ArithLit(0)),
            [
                StmPrint(ArithLit(0))
            ],
            [
                StmPrint(ArithLit(1))
            ]
        )
    ]

def example5():
    """
    x = 10
    if not (x % 2 == 0):
        print 0
    else:
        print 1
    """
    return [
        StmAssign("x", ArithLit(10)),
        StmIf(
            BoolNeg(
                BoolArithCmp(
                    ArithCmp.Eq,
                    ArithBinop(
                        ArithOp.Mod,
                        ArithVar("x"),
                        ArithLit(2)),
                    ArithLit(0))),
            [
                StmPrint(ArithLit(0))
            ],
            [
                StmPrint(ArithLit(1))
            ]
        )
    ]

def example6():
    """
    x = 10
    if x % 2 == 0 and x < 11:
        print 0
    """
    return [
        StmAssign("x", ArithLit(10)),
        StmIf(
            BoolBinop(
                BoolOp.And,
                BoolArithCmp(
                    ArithCmp.Eq,
                    ArithBinop(
                        ArithOp.Mod,
                        ArithVar("x"),
                        ArithLit(2)),
                    ArithLit(0)),
                BoolArithCmp(
                    ArithCmp.Lt,
                    ArithVar("x"),
                    ArithLit(11)
                )
            ),
            [
                StmPrint(ArithLit(0))
            ],
            [
            ]
        )
    ]

def example7():
    """
    x = 10
    if x % 2 == 1 or x < 11:
        print 0
    """
    return [
        StmAssign("x", ArithLit(10)),
        StmIf(
            BoolBinop(
                BoolOp.Or,
                BoolArithCmp(
                    ArithCmp.Eq,
                    ArithBinop(
                        ArithOp.Mod,
                        ArithVar("x"),
                        ArithLit(2)),
                    ArithLit(1)),
                BoolArithCmp(
                    ArithCmp.Lt,
                    ArithVar("x"),
                    ArithLit(11)
                )
            ),
            [
                StmPrint(ArithLit(0))
            ],
            [
            ]
        )
    ]

def example8_primes():
    """
    limit = 1000
    count = 0
    current = 2
    while current <= limit:
        is_prime = 1
        if current != 2 and current % 2 == 0:
            is_prime = 0
        candidate = 3
        while is_prime == 1 and candidate * candidate <= current:
            if current % candidate == 0:
                is_prime = 0
            candidate += 1
        if is_prime == 1:
            #print(current)
            count += 1
        current += 1
    print("Total =", count)
    """
    return [
        StmAssign("limit", ArithLit(1000)),
        StmAssign("count", ArithLit(0)),
        StmAssign("current", ArithLit(2)),
        StmWhile(
            BoolArithCmp(
                ArithCmp.Leq,
                ArithVar("current"),
                ArithVar("limit")    
            ),
            [
            StmAssign("is_prime", ArithLit(1)),
            StmIf(
                BoolBinop(
                    BoolOp.And,
                    BoolArithCmp(
                        ArithCmp.Neq,
                        ArithVar("current"),
                        ArithLit(2)
                    ),
                    BoolArithCmp(
                        ArithCmp.Eq,
                        ArithBinop(
                            ArithOp.Mod,
                            ArithVar("current"),
                            ArithLit(2)
                        ),
                        ArithLit(0)
                    ),
                ),
                [
                StmAssign("is_prime", ArithLit(0)),
                ],
                []
            ),
            StmAssign("candidate", ArithLit(3)),
            StmWhile(
                BoolBinop(
                    BoolOp.And,
                    BoolArithCmp(
                        ArithCmp.Eq,
                        ArithVar("is_prime"),
                        ArithLit(1)
                    ),
                    BoolArithCmp(
                        ArithCmp.Leq,
                        ArithBinop(
                            ArithOp.Mul,
                            ArithVar("candidate"),
                            ArithVar("candidate")
                        ),
                        ArithVar("current")
                    )   
                ),
                [
                StmIf(
                    BoolArithCmp(
                        ArithCmp.Eq,
                        ArithBinop(
                            ArithOp.Mod,
                            ArithVar("current"),
                            ArithVar("candidate")
                        ),
                        ArithLit(0)
                    ),
                    [
                        StmAssign("is_prime", ArithLit(0)),
                    ],
                    []
                ),
                StmAssign("candidate", 
                    ArithBinop(
                        ArithOp.Add,
                        ArithVar("candidate"),
                        ArithLit(1)
                    )
                )    
                ]
            ),
            # while is_prime
            StmIf(
                BoolArithCmp(
                    ArithCmp.Eq,
                    ArithVar("is_prime"),
                    ArithLit(1)
                ),
                [StmAssign("count", 
                    ArithBinop(
                        ArithOp.Add,
                        ArithVar("count"),
                        ArithLit(1)
                    )
                )],
                []
            ),
            # if is_prime
            StmAssign("current", 
                ArithBinop(
                    ArithOp.Add,
                    ArithVar("current"),
                    ArithLit(1)
                )
            ),
            ]
        ),
        StmPrint(
            ArithVar("count")
        ),
    ]

examples = [
    example0,
    example01,
    example1,
    example2,
    example3,
    example4,
    example5,
    example6,
    example7,
    example8_primes,
]

if __name__ == "__main__":
    for i, example in enumerate(examples):
        print("------------")
        print(f"example #{i}")
        print("------------")
        print(example.__doc__)
        print("------------")
        interpret_many(example())
