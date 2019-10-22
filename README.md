Overview
========

A compiler from SIL (a simple imperative language) to x86-64 
assembly for linux written in Python 3.7.

The goal of the project is to learn how compilers work, so for 
simplicity SIL will have many missing parts.

Todo
====

Add:
* [+] Parser
* [+] Composite boolean operations (e.g. x <= 1 && x > -5)
* [+] Compound assignment (as syntactic sugar)
* [+] Add error handling to the parser	
* [+] Variable declarations
* [+] No variable is used before declaration
* [+] Block scoping
* [+] Correct handling of block scoping used symbol tables
* [+] Allow blocks to be inserted at arbitrary places
* [+] Functions
* [ ] Make sure return returns early from the function
* [ ] Put local variables on the stack
* [ ] x++, x--, ++x, --x
* [ ] for loops
* [ ] Arrays
* [ ] Pointers
* [ ] Structs
* [ ] Floating-point operations
* [ ] Type checker
* [ ] Cmd line arguments
* [ ] Use a parser generator so that we can extend the parser more easily

SIL Syntax
==========

Check the examples in the `examples` directory to see what is availabe.

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

Updating the tests
==================

```
./scripts/generate_outputs.sh           # compiles all examples, runs them and writes their output
```

Running the code
================

## Print the generated assembly

```
$ python3 src/compile.py examples/ex0.sil
```
Prints the asm source code


## Compile and run the code

```
$ ./scripts/compile.sh examples/ex0.sil 
```
Compiles and runs the program

Example output:

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
