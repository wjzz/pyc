%include "std.asm"

section .data


section .text
    global _start

_start:
    push 1
    push 2
    pop r10
    pop r11
    add r10, r11
    push r10
    push 3
    push 4
    pop r10
    pop r11
    add r10, r11
    push r10
    pop r10
    pop r11
    add r10, r11
    push r10
    pop rax
    printint rax
    exit    
