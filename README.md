Overview
========

A compiler from SIL (a simple imperative language) to x86-64 
assembly for linux written in Python 3.7.

The goal of the project is to learn how compilers work, so for 
simplicity SIL will have many missing parts.

SIL Syntax
==========

a in ArithExpr ::= var | lit | a1 aop a2
aop ::= + | - | * | / | %

b in BoolExpr ::= a1 bop a2
bop ::= == | != | <= | < | > | >=

s in Stm ::= 
  | var = a           # assingment
  | var aop= a        # compound assignment
  | if b { ss1 } else { ss2 }
  | while b { ss }
  | print aexpr 
  | return b
 
ss := s*   # (possibly empty) statemenst list

Running the tests
=================

```
$ ./test_all.sh
```

Running the code
================

```
$ python3 compile.py examples/ex0.sil
```
Prints the asm source code


```
$ ./compile.sh examples/ex0.sil 
```

Yields:

```
filename = ex0.sil
base = ex0
Compiling the program... OK!
Running the assembler... OK!
Running the linker... OK!
Running the program... 
15
Return value = 1
```
