Overview
========

A compiler from SIL (a simple imperative language) to x86-64 
assembly for linux written in Python 3.7.

The goal of the project is to learn how compilers work, so for 
simplicity SIL will have many missing parts.

Todo
====

Add:
- [x] Parser
- [x] Composite boolean operations (e.g. x <= 1 && x > -5)
- [x] Compound assignment (as syntactic sugar)
- [x] Add error handling to the parser	
- [x] Variable declarations
- [x] No variable is used before declaration
- [x] Block scoping
- [x] Correct handling of block scoping used symbol tables
- [x] Allow blocks to be inserted at arbitrary places
- [x] Functions
- [x] Make sure return returns early from the function
- [x] Implement break and continue
- [x] Support tabs
- [x] Put local variables on the stack
- [x] Support global variables again
- [x] Pointers (declaration, dereferencing and taking addresses)
- [x] Assignment using pointers
- [ ] Start using registers in the code instead of pushing everything on the stack
- [ ] Add true and false
- [ ] Include expressions in statements (now we can't write `foo(n)`)
- [ ] x++, x--, ++x, --x
- [ ] for loops
- [ ] Arrays
- [ ] Structs
- [ ] Static variables
- [ ] Floating-point operations
- [ ] Function pointers
- [ ] Type checker
- [ ] Cmd line arguments
- [ ] Use a parser generator so that we can extend the parser more easily

Make the compiler more modular:
- [ ] Use an IL (intermediate language)

Add more backends:
- [ ] WebAssembly
- [ ] ARM (Raspberry PI)
- [ ] Mac (PowerPC?)

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
$ python3 src/main.py examples/ex0.sil
```
Prints the asm source code

## Compile and run the code

```
$ ./scripts/compile.sh examples/ex0.sil
# OR
# c examples/ex0.sil           # I have an alias on my machine :-) 
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
