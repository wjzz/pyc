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
    je _cmp_change
    jmp _cmp_ret
_cmp_change:
    mov r9, 1
_cmp_ret:
    push r9    
    pop rax
    cmp rax, 0
    je _if_false
_if_true:
    push 0
    pop rax
    printint rax
    jmp _if_ret
_if_false:
    push 1
    pop rax
    printint rax
_if_ret:
    exit    
