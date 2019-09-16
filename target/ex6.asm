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
    push 2
    pop r11
    pop r10
    
    mov rax, r10
    xor rdx, rdx
    div r11
    mov r10, rdx
            
    push r10
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
