%include "std.asm"

section .text
    global _start

_start:
    mov r15, 0    ; count => r15
    mov r14, 2    ; current => r14
_main_loop:
    cmp r14, 1000000
    jg _end
    mov r13, 0    ; is_prime => r13
    cmp r14, 2
    je _if_ret5
    ; r14 != 2

    mov rax, r14
    and rax, 1
    
    ; rax = r14 % 2
    cmp rax, 0
    je _increment_current
    jne _if_ret5
_if_ret5:
    mov r12, 3     ; factor_candidate => r12
_inner_loop:
    cmp r13, 0
    jne _increment_current
    mov rax, r12
    mul rax
    cmp rax, r14
    jg _incr_count_if_prime   ; we didn't find any prime factors
    mov rax, r14
    mov rdx, 0
    div r12
    cmp rdx, 0
    je _increment_current
    inc r12
    jmp _inner_loop
_incr_count_if_prime:
    inc r15 ; count => r15
_increment_current:
    inc r14
    jmp _main_loop
_end:
    printint r15
    exit

