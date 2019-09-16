%include "std.asm"

section .data


section .text
    global _start

_start:
    push 1
    push 0

    pop r11
    pop r10
    mov r9, 0
    cmp r10, r11
    je _cmp_change1
    jmp _cmp_ret1
_cmp_change1:
    mov r9, 1
_cmp_ret1:
    push r9    
    pop rax
    cmp rax, 0
    je _if_false2
_if_true2:
    push 0
    pop rax
    printint rax
    jmp _if_ret2
_if_false2:
    push 1
    pop rax
    printint rax
_if_ret2:
    exit    
