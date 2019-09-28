BITS 64  ; enable 64 bit registers

section .data
	SYS_WRITE equ 1
	STDOUT equ 1
	SYS_EXIT equ 60
	EXIT_SUCCESS equ 0

	newline db 10,0

section .bss
	;; 18 digits for the number, 1 char for the sign
	;; 1 char for null
	;; 5 chars just in case
	__digits resb 25
	
;;; -------------------------------------------------------
;;; Macros
;;; -------------------------------------------------------
	
%macro print 1
	mov rax, %1
	call _puts
%endmacro

%macro println 1
	print %1
	print newline
%endmacro

%macro printint 1
	mov rax, %1
	call _int_to_string
	println __digits
%endmacro

%macro exit 1
        mov rdi, %1
	jmp _exit
%endmacro	
	
%macro exit_ok 0
        exit EXIT_SUCCESS
%endmacro

;;; -------------------------------------------------------
;;; Program start
;;; -------------------------------------------------------
	
section .text

;;; -------------------------------------------------------
;;; Puts
;;; -------------------------------------------------------
	
_puts:
	;; pre-cond: pointer to 0-terminated string in rax
	;; effect: string printed to stdout
	mov rsi, rax	; save the buffer to print
	mov rdx, 0	; length of the string (we don't count the '0)
_puts_loop:
	cmp byte [rax], 0	; check if '\0'
	jz _puts_ctd
	inc rdx
	inc rax
	jmp _puts_loop
_puts_ctd:
	;; we have the length calculated in r10 now
	;; we can make the syscall
	mov rax, SYS_WRITE
	mov rdi, STDOUT
	;; rsi has been already set up in the prologue
	;; rdx has the length already
	syscall
	ret

;;; -------------------------------------------------------
;;; Int to string
;;; -------------------------------------------------------

;;; pre-condition - argument (64-bit) in rax
;;; effect: __digits contains the characters
_int_to_string:
	push rbp
	mov rbp, rsp
	mov r8, rsp		; backup rsp
	mov r10, 0		; number of digits, dont count '-'
	mov r11, __digits
	;; special case - negative number
	cmp rax, 0
	jge _int_to_string_non_negative
	mov byte [r11], 45     	; ord('-') = 45
	inc r11
	neg rax			; make rax positive
	
_int_to_string_non_negative:
	;; special case - zero was passed
	cmp rax, 0
	jne _int_to_string_loop
	;; handle special case
	;; mov byte [r11], 48
	push 48
	;; inc r11
	inc r10
_int_to_string_loop:
	cmp rax, 0
	jz _int_to_string_ctd
	mov r9, 10
	mov rdx, 0		; division is performed on rdx:rax
	div r9			; rax % 10 goes to rdx
	add rdx, 48		; ord('0') = 48
	;; mov byte [r11], dl
	mov r9b, dl
	push r9
	;; inc r11
	inc r10
	jmp _int_to_string_loop
_int_to_string_ctd:
	;; reverse the string
	mov rcx, r10		; loop counter
_int_to_string_rev:
	pop r9
	mov byte [r11], r9b
	inc r11
	loop _int_to_string_rev

	;; terminate the string with '0'
	mov byte [r11], 0
	inc r11

	mov rsp, r8
	pop rbp
	ret

;;; -------------------------------------------------------
;;; Exit
;;; -------------------------------------------------------
	
_exit:
	mov rax, SYS_EXIT
	;; mov rdi, EXIT_SUCCESS
	syscall
