Overview
========

A compiler from SIL (a simple imperative language) to x86-64 
assembly for linux written in Python 3.7.

The goal of the project is to learn how compilers work, so for 
simplicity SIL will have many missing parts.

Todo
====

Add:
  [+] Parser
  [+] Composite boolean operations (e.g. x <= 1 && x > -5)
  [+] Compound assignment (as syntactic sugar)
  [+] Add error handling to the parser	
  [+] Variable declarations
  [+] No variable is used before declaration
  [+] Block scoping
  [+] Correct handling of block scoping used symbol tables
  [+] Allow blocks to be inserted at arbitrary places
  [ ] Use a parser generator so that we can extend the parser more easily
  [ ] x++, x--, ++x, --x
  [ ] for loops
  [ ] Functions
  [ ] Arrays
  [ ] Pointers
  [ ] Structs
  [ ] Floating-point operations
  [ ] Type checker
  [ ] Cmd line arguments

SIL Syntax
==========

a in ArithExpr ::= var | lit | a1 aop a2
aop ::= + | - | * | / | %

b in BoolExpr ::= a1 bop a2 | not b | b1 and b2 | b1 or b2
bop ::= == | != | <= | < | > | >=

s in Stm ::= 
  | var = a           # assignment
  | var aop= a        # compound assignment
  | if b { ss1 } else { ss2 }
  | while b { ss }
  | print aexpr 
  | return b
 
ss := s*   # (possibly empty) statemenst list

Running the tests
=================

Unit tests:
```
$ make test
```

End to end tests:
```
$ make e2e
```

Running the code
================

```
$ python3 src/compile.py examples/ex0.sil
```
Prints the asm source code


```
$ ./scripts/compile.sh examples/ex0.sil 
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
