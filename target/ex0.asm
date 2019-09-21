visiing print
visiting arith lit
%include "std.asm"

section .data


section .text
    global _start

_start:
    push 1
    pop rax
    printint rax
    exit    
