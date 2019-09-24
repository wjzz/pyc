"""
x86-64 architecture instructions
"""

from enum import Enum

class ITag(Enum):
    Label = "label"
    Mov = "mov"
    Push = "push"
    Pop = "pop"
    Cmp = "cmp"
    Jmp = "jmp"
    Je  = "je"
    Jne = "jne"
    Jg  = "jg"
    Jge = "jge"
    Jl  = "jl"
    Jle = "jle"
    Add = "add"
    Inc = "inc"
    Sub = "sub"
    Dec = "dec"
    Mul = "mul"
    Div = "div"
    Neg = "neg"
    Xor = "xor"
