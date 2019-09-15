%include "std.asm"

section .data


section .text
    global _start

_start:
    push 15
    pop rax
    printint rax
    exit    
