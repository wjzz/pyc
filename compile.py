from ast import *
from freevars import vars_many
import sys

class CompileVisitor:
    labelId = 0

    @staticmethod
    def fresh_id():
        CompileVisitor.labelId += 1
        return CompileVisitor.labelId

    def __init__(self):
        pass

    def visit_ArithLit(self, val):
        return f"""\
    push {val}\n"""

    def visit_ArithVar(self, var):
        var = mangle(var)
        return f"""\
    mov rax, [{var}]
    push rax\n\
"""

    def visit_ArithBinop(self, op, a1, a2):
        c1 = a1.accept(self)
        c2 = a2.accept(self)

        if op == ArithOp.Add:
            operation = "add r10, r11"
        if op == ArithOp.Sub:
            operation = "sub r10, r11"
        if op == ArithOp.Mul:
            operation = """
    mov rax, r10
    mul r11
    mov r10, rax
            """
        if op == ArithOp.Div:
            # TODO: we reset the rdx register here
            operation = """
    mov rax, r10
    xor rdx, rdx
    div r11
    mov r10, rax
            """
        if op == ArithOp.Mod:
            # TODO: we reset the rdx register here
            operation = """
    mov rax, r10
    xor rdx, rdx
    div r11
    mov r10, rdx
            """

        return c1 + c2 + f"""\
    pop r11
    pop r10
    {operation}
    push r10\n\
"""
        
    def visit_BoolBinop(self, op, a1, a2):
        c1 = a1.accept(self)
        c2 = a2.accept(self)

        label_id = CompileVisitor.fresh_id()
        label = f"_cmp_change{label_id}"

        if op == BoolOp.Eq:
            operator = "je"
        if op == BoolOp.Neq:
            operator = "jne"
        if op == BoolOp.Leq:
            operator = "jle"
        if op == BoolOp.Lt:
            operator = "jl"
            raise NotImplementedError
        if op == BoolOp.Geq:
            operator = "jge"
        if op == BoolOp.Gt:
            operator = "jg"

        return c1 + c2 + f"""
    pop r11
    pop r10
    mov r9, 0
    cmp r10, r11
    {operator} {label}
    jmp _cmp_ret{label_id}
{label}:
    mov r9, 1
_cmp_ret{label_id}:
    push r9\
    """

    def visit_BoolNeg(self, b):
        # trick:
        # given not 0 = 1
        #       not 1 = 0
        # we can implement not b as 1 - b = -(b - 1)
        c = b.accept(self)
        return c + """
    pop rax
    dec rax
    neg rax
    push rax\
"""

    def visit_StmAssign(self, var, a):
        c = a.accept(self)
        var = mangle(var)
        return c + f"""\
    pop rax
    mov [{var}], rax\n"""
        # self.state[var] = val

    def visit_StmIf(self, b, ss1, ss2):
        bc = b.accept(self)
        cc1 = self.visit_many(ss1)
        cc2 = self.visit_many(ss2)
        label_id = CompileVisitor.fresh_id()

        return bc + f"""
    pop rax
    cmp rax, 0
    je _if_false{label_id}
_if_true{label_id}:
{cc1}\
    jmp _if_ret{label_id}
_if_false{label_id}:
{cc2}\
_if_ret{label_id}:
"""
    
    def visit_StmWhile(self, b, ss):
        bc = b.accept(self)
        cc = self.visit_many(ss)
        label_id = CompileVisitor.fresh_id()
        return "_loop_while{label_id}:\n" + bc + f"""
    pop rax
    cmp rax, 0
    je _while_ret{label_id}
{cc}\
    jmp _loop_while{label_id}
_while_ret{label_id}:\n\
"""

    def visit_StmPrint(self, a):
        cval = a.accept(self)
        cval += """\
    pop rax
    printint rax
"""
        return cval

    def visit_many(self, stms):
        return "\n".join([ stm.accept(self) for stm in stms ])

def compile_many(stms):
    return CompileVisitor().visit_many(stms)

def compile_top(stms):
    free_vars = vars_many(stms)
    vars_decl = define_vars(free_vars)

    program = compile_many(stms)

    template = f"""\
%include "std.asm"

section .data
{vars_decl}

section .text
    global _start

_start:
{program}\
    exit\
    """

    return template

def mangle(var):
    return f"var_{var}"

def define_vars(vars):
    return "\n".join([ f"  {mangle(var)} dq 0" 
        for var in vars])

if __name__ == "__main__":
    if len(sys.argv) > 1:
        #print("got file name =", sys.argv[1])
        with open(sys.argv[1], "r") as f:
            lines = "\n".join(f.readlines())
            try:
                c = eval(lines)
                # print(c)
                free_vars = vars_many(c)
                # print(free_vars)
                result = compile_top(c)
                print(result)
            except Exception as e:
                print("Got lines", lines)
                print("Failed to parse the file", f=sys.stderr)
    else:
        result = compile_top([])
        print(result)
