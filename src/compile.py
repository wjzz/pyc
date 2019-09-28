from ast import *
import symbol_table
from optimize import optimize

from collections import defaultdict
import sys

class CompileVisitor:
    labelId = 0

    @staticmethod
    def fresh_id():
        CompileVisitor.labelId += 1
        return CompileVisitor.labelId

    def __init__(self):
        self._vars = defaultdict(int)
        self._vars_in_scope = set()
    
    def add_variable(self, var):
        self._vars_in_scope.add(var)
    
    @property
    def vars(self):
        return self._vars_in_scope

    def add_depth(self, var):
        var_num = self._vars[var]
        if var_num > 1:
            var = var + str(var_num)
        return var

    def visit_ArithLit(self, val):
        return f"""\
    push {val}\n"""

    def visit_Var(self, var):
        var = self.add_depth(var)
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
        
    def visit_BoolArithCmp(self, op, a1, a2):
        c1 = a1.accept(self)
        c2 = a2.accept(self)

        label_id = CompileVisitor.fresh_id()
        label = f"_cmp_change{label_id}"

        if op == ArithCmp.Eq:
            operator = "je"
        if op == ArithCmp.Neq:
            operator = "jne"
        if op == ArithCmp.Leq:
            operator = "jle"
        if op == ArithCmp.Lt:
            operator = "jl"
        if op == ArithCmp.Geq:
            operator = "jge"
        if op == ArithCmp.Gt:
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

    def visit_BoolBinop(self, op, b1, b2):
        c1 = b1.accept(self)
        c2 = b2.accept(self)
        label_id = CompileVisitor.fresh_id()

        if op == BoolOp.And:
            return c1 + f"""
    pop rax
    cmp rax, 0
    jne _and_right{label_id}
    push 0
    jmp _and_ret{label_id}
_and_right{label_id}:
{c2}
_and_ret{label_id}:
"""
        elif op == BoolOp.Or:
            return c1 + f"""
    pop rax
    cmp rax, 0
    je _or_right{label_id}
    push 1
    jmp _or_ret{label_id}
_or_right{label_id}:
{c2}
_or_ret{label_id}:
"""

    def visit_StmDecl(self, tp, var, a):
        # if a == None then we don't have to do anything

        self._vars[var] += 1
        self.add_variable(self.add_depth(var))

        if a is not None:
            return self.visit_StmAssign(var, a)
        else:
            return ""

    def visit_StmAssign(self, var, a):
        c = a.accept(self)
        var = self.add_depth(var)
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
        return f"_loop_while{label_id}:\n" + bc + f"""
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

    def visit_StmReturn(self, a):
        cval = a.accept(self)
        cval += """\
    pop rax
"""
        return cval

    def visit_StmBlock(self, stms):
        return self.visit_many(stms)

    def visit_many(self, stms):
        var_names = self._vars.copy()
        ss = "\n".join([ stm.accept(self) for stm in stms ])
        self._vars = var_names
        return ss

    def visit_FunDecl(self, _type, name, _args, body):
        funname = mangle_fun(name)
        ss = self.visit_many(body)
        return f"""
{funname}:
{ss}\
    ret\
        """

    def visit_many_defs(self, defs):
        ss = "\n".join ([ defn.accept(self) for defn in defs])
        return ss

def compile_many(stms):
    visitor = CompileVisitor()
    code = visitor.visit_many(stms)
    vars = visitor.vars
    return code, vars

def mangle(var):
    return f"var_{var}"

def mangle_fun(name):
    return f"__{name}__"

def define_vars(vars):
    return "\n".join([ f"  {mangle(var)} dq 0" 
        for var in vars])

def compile_stms(stms):
    _globals = symbol_table.build(stms)
    # print(symbols, file=sys.stderr)

    program, symbols = compile_many(stms)
    vars_decl = define_vars(symbols)

    template = f"""\
%include "asm/std.asm"

section .data
{vars_decl}

section .text
    global _start

_start:\
{program}\
    exit_ok\
    """

    return template

def compile_global_defs(defs):
    visitor = CompileVisitor()
    code = visitor.visit_many_defs(defs)
    # vars = visitor.vars
    return code #, vars

def compile_file(defs):
    print(f"found {len(defs)} declarations", file=sys.stderr, flush=True)
    names = [defn.name for defn in defs]
    if "main" not in names:
        print("A program with function definition must have"
          " a 'main' function! Aborting...", file=sys.stderr)
        raise Exception("No main function")

    # TODO: check that all functions have different names

    #_globals = symbol_table.build(stms)
    # print(symbols, file=sys.stderr)

    #program, symbols = compile_many(stms)
    #vars_decl = define_vars(symbols)
    vars_decl = ""
    global_defs = compile_global_defs(defs)

    template = f"""\
%include "asm/std.asm"

section .data
{vars_decl}

section .text
    global _start

_start:
    call __main__
    exit rax
{global_defs}\
    """

    print(template, flush=True, file=sys.stderr)
    return template
    #raise NotImplementedError

def compile_top(input):
    if input[0] == "STMS":
        stms = input[1]
        return compile_stms(stms)
    elif input[0] == "PRAGMA":
        decls = input[1]
        return compile_file(decls)

if __name__ == "__main__":
    if len(sys.argv) > 1:
        #print("got file name =", sys.argv[1])
        with open(sys.argv[1], "r") as f:
            lines = "\n".join(f.readlines())
            try:
                c = eval(lines)
                # print(c)
                result = compile_top(c)
                print(result)
                # print("--------------------------")
                # result2 = optimize(result)
                # print(result2)
            except Exception as e:
                print("Got lines", lines)
                print("Failed to parse the file", f=sys.stderr)
    else:
        result = compile_top([])
        print(result)
