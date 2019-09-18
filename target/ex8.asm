%include "std.asm"

section .data
  var_n dq 0
  var_x dq 0
  var_y dq 0

section .text
    global _start

_start:
    push 0
    pop rax
    mov [var_x], rax

    push 1
    pop rax
    mov [var_y], rax

    push 20
    pop rax
    mov [var_n], rax

_loop_while2:
    mov rax, [var_n]
    push rax
    push 0

    pop r11
    pop r10
    mov r9, 0
    cmp r10, r11
    jg _cmp_change1
    jmp _cmp_ret1
_cmp_change1:
    mov r9, 1
_cmp_ret1:
    push r9    
    pop rax
    cmp rax, 0
    je _while_ret2
    mov rax, [var_x]
    push rax
    pop rax
    printint rax

    mov rax, [var_x]
    push rax
    mov rax, [var_y]
    push rax
    pop r11
    pop r10
    add r10, r11
    push r10
    pop rax
    mov [var_y], rax

    mov rax, [var_y]
    push rax
    mov rax, [var_x]
    push rax
    pop r11
    pop r10
    sub r10, r11
    push r10
    pop rax
    mov [var_x], rax

    mov rax, [var_n]
    push rax
    push 1
    pop r11
    pop r10
    sub r10, r11
    push r10
    pop rax
    mov [var_n], rax
    jmp _loop_while2
_while_ret2:
    exit    
