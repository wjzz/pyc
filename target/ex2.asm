%include "std.asm"

section .data
  var_x dq 0

section .text
    global _start

_start:
    push 10
    pop rax
    mov [var_x], rax

    mov rax, [var_x]
    push rax
    pop rax
    printint rax
    exit    
