from ast import *
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
        # currenly we keep all local variables in memory
        # this means that there can be name clashes
        # this dictionary tells us which occurence we are
        # currently using 
        self._var_occur_index = defaultdict(int)

        # ???
        self._vars_in_scope = set()
        
        # symbol table for parameters
        # we keep a separate stack for every variable
        self._var_addr = defaultdict(list)
        
        # a stack of function epilogue labels
        self._epilogues = []
        # a stack of loop end labels
        self._loop_labels = []

    # Function epilogue stack

    def push_epilogue(self, label):
        self._epilogues.append(label)
    
    @property
    def top_epilogue(self):
        return self._epilogues[-1]

    def pop_epilogue(self, label):
        assert(self.top_epilogue == label)
        self._epilogues.pop()

    # Loop end stack

    def push_loop_labels(self, labels):
        self._loop_labels.append(labels)
    
    @property
    def top_loop_start_label(self):
        return self._loop_labels[-1][0]

    @property
    def top_loop_end_label(self):
        return self._loop_labels[-1][1]

    def pop_loop_labels(self, labels):
        assert(self._loop_labels[-1] == labels)
        self._loop_labels.pop()

    # Variables in scope

    def add_variable_to_scope(self, var):
        self._vars_in_scope.add(var)
    
    @property
    def vars_in_scope(self):
        return self._vars_in_scope

    # Local variables and function parameters

    def add_occur_suffix(self, var):
        var_num = self._var_occur_index[var]
        if var_num > 1:
            # attach a suffix if more than one occurence
            return var + str(var_num)
        return var

    def global_var_addr(self, var):
        return mangle(self.add_occur_suffix(var))

    def is_parameter(self, var):
        """
        Checks if the given variable comes from
        binding the current functions formal parameters
        """
        return self._var_addr[var] != []

    def get_parameter_addr(self, var):
        return self._var_addr[var][-1]

    def get_var_addr(self, var):
        if self.is_parameter(var):
            return self.get_parameter_addr(var)
        else:
            return self.global_var_addr(var)

    def add_parameter(self, var, addr):
        self._var_addr[var].append(addr)

    def remove_parameter(self, var):
        self._var_addr[var].pop()

    def extend_environment(self, var):
        """
        Declares the given variable in the current environment.
        """
        self._var_occur_index[var] += 1

    def save_environment(self):
        return self._var_occur_index.copy()

    def restore_environment(self, env):
        self._var_occur_index = env
    
    # Code generation, case by case

    def visit_ArithLit(self, val):
        return f"""\
    push {val}\n"""

    def visit_Var(self, var):
        var_addr = self.get_var_addr(var)
        return f"""\
    mov rax, [{var_addr}]
    push rax\n\
"""

    # VERSION 1: we put all args on the stack
    # NOTE: we also have to pop them off
    # RETURN VALUE:
    #   all expressions leave the result on the top of the stack
    def visit_FunCall(self, name, args):
        # first prepare the arguments on the stack
        # we evaluate them right-to-left (seems natural here)
        arg_popping = ""
        cc = ""
        for arg in reversed(args):
            cc += arg.accept(self)   # we have implicit pushes over here
            arg_popping += "    pop r12\n"  # TODO: this can be replaced by a simple pointer arithm.
        # next - call the function
        funname = mangle_fun(name)
        cc += f"""\
    call {funname}
{arg_popping}
    push rax
"""
        return cc

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
        # a == None means that we only declare the var,
        # without initializing it

        self.extend_environment(var)
        self.add_variable_to_scope(self.add_occur_suffix(var))

        if a is not None:
            return self.visit_StmAssign(var, a)
        else:
            return ""

    def visit_StmAssign(self, var, a):
        c = a.accept(self)
        var_addr = self.global_var_addr(var)
        return c + f"""\
    pop rax
    mov [{var_addr}], rax\n"""

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
        label_id = CompileVisitor.fresh_id()
        while_start_lbl = f"_loop_while{label_id}"
        while_end_lbl = f"_while_ret{label_id}"
        labels = (while_start_lbl, while_end_lbl)
        bc = b.accept(self)
        
        self.push_loop_labels(labels)
        cc = self.visit_many(ss)
        self.pop_loop_labels(labels)

        return f"{while_start_lbl}:\n" + bc + f"""
    pop rax
    cmp rax, 0
    je {while_end_lbl}
{cc}\
    jmp {while_start_lbl}
{while_end_lbl}:\n\
"""

    def visit_StmPrint(self, a):
        cval = a.accept(self)
        cval += """\
    pop rax
    printint rax
"""
        return cval

    def visit_StmReturn(self, a):
        epilogue_lbl = self.top_epilogue
        cval = a.accept(self)
        cval += f"""\
    pop rax
    jmp {epilogue_lbl}
"""
        return cval

    def visit_StmBreak(self):
        loop_end_lbl = self.top_loop_end_label
        return f"jmp {loop_end_lbl}\n"

    def visit_StmContinue(self):
        loop_start_lbl = self.top_loop_start_label
        return f"jmp {loop_start_lbl}\n"

    def visit_StmBlock(self, stms):
        return self.visit_many(stms)

    def visit_many(self, stms):
        env = self.save_environment()
        ss = "\n".join([ stm.accept(self) for stm in stms ])
        self.restore_environment(env)
        return ss

    def visit_FunDecl(self, _type, name, params, body):
        funname = mangle_fun(name)
        # prepare the prologue
        # 
        # at this moment [rsp] contains the return address
        # [rsp] +  8 contains arg #1
        # [rsp] + 16 contains arg #2
        # etc
        # 
        # We store rsp in rbp at the very start of the prologue
        # so we can reference the vars using offsets of rbp.
        #
        # THIS ALSO MEANS THAT WE MUST ADD ANOTHER OFFSET OF 8!
        # The stack looks like this:
        # [rbp]      == value of rsp
        # [rbp +  8] == stored value of rbp
        # [rbp + 16] == arg #1
        # [rbp + 24] == arg #2
        # etc!
        # 
        # Note that the value of rsp changes as we change the stack.
        # rbp is a callee-save register, so we don't have to worry
        # about it being changed when calling other functions.

        # Bind the parameters
        word_len = 8
        for i, param in enumerate(params):
            var = param.var
            index = 2 + i
            # offset = word_len * index
            addr = f"rbp + {word_len} * {index}"
            self.add_parameter(var, addr)

        prologue = """
    push rbp
    mov rbp, rsp
"""
        # the epilogue label must be known here, because we need to jump here
        # if we find any return
        epilogue_lbl = f"{funname}_epilogue"

        self.push_epilogue(epilogue_lbl)

        # The main body of the function
        # the result of the function call is the content of the rax register
        body_code = self.visit_many(body)

        # we pass the label as a correctness check
        self.pop_epilogue(epilogue_lbl)

        # prepare the epilogue
        # NOTE: the parameters on the stack will be removed by the caller
        epilogue = """
    pop rbp
"""
        # remove the bindings for the params
        for param in params:
            self.remove_parameter(param.var)

        return f"""
{funname}:\
{prologue}\
{body_code}\
{epilogue_lbl}:\
{epilogue}\
    ret\
"""

    def visit_many_defs(self, defs):
        ss = "\n".join([ defn.accept(self) for defn in defs])
        return ss

# End of code generator cases

def mangle(var):
    return f"var_{var}"

def mangle_fun(name):
    return f"__{name}__"

def define_vars(vars):
    return "\n".join([ f"  {mangle(var)} dq 0" 
        for var in vars])

def compile_global_defs(defs):
    visitor = CompileVisitor()
    code = visitor.visit_many_defs(defs)
    vars = visitor.vars_in_scope
    return code, vars

def compile_file(defs):
    names = [defn.name for defn in defs]
    if "main" not in names:
        print("A program with function definition must have"
          " a 'main' function! Aborting...", file=sys.stderr)
        raise Exception("No main function")

    # TODO: check that all functions have different names

    global_defs, vars = compile_global_defs(defs)
    vars_decl = define_vars(vars)

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

    return template

def compile_top(decls):
    return compile_file(decls)
