%include "std.asm"

section .data


section .text
    global _start

_start:
    push 1
    push 2
    pop r11
    pop r10
    add r10, r11
    push r10
    pop rax
    printint rax

    push 10
    push 1
    pop r11
    pop r10
    sub r10, r11
    push r10
    pop rax
    printint rax

    push 3
    push 3
    pop r11
    pop r10
    
            mov rax, r10
            mul r11
            mov r10, rax
            
    push r10
    pop rax
    printint rax

    push 100
    push 3
    pop r11
    pop r10
    
            mov rax, r10
            xor rdx, rdx
            div r11
            mov r10, rax
            
    push r10
    pop rax
    printint rax

    push 11
    push 3
    pop r11
    pop r10
    
            mov rax, r10
            xor rdx, rdx
            div r11
            mov r10, rdx
            
    push r10
    pop rax
    printint rax
    exit    
