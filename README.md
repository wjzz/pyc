# PyC 

## Overview

PyC (a pun on CPython) is a toy compiler from a (subset of) C to x86-64 assembly for linux written in Python 3.8. Being my first compiler it's extremely simple but extending it a great learning experience.

The project originally started as a compiler for a simple imperative language (SIL for short), which was based on the classic WHILE imperative language found in programming language theory or semantics textbooks. I slowly drifted into using the syntax and semantics of the C language.

## Goals

The goal of the project is to learn how compilers work, so for simplicity the source language will have many missing parts, although I'm slowly filling the gaps. For the current status of the project see `TODO.md` and the `examples` folder.

This project is also an excuse for me to play with many python tools and libraries, although at the time of writing no external libraries are required to compile the code. I'm slowly introducing some libraries for testing, linting etc.

## Requirements

I'm (ab)using a lot of f-strings and I intend to add typing annotations at some point, so python 3.7+ is required.

## Suported syntax

Check the examples in the `examples` directory to see which language features are currently supported.

## Running the tests

Unit tests:
```
$ make test
```

End to end tests:
```
$ make e2e
```

Check the coverage:
```
$ make cov-unit       # unit tests
$ make cov-e2e        # end to end tests
```

### Updating the example outputs for e2e tests

```
./scripts/generate_outputs.sh           # compiles all examples, runs them and writes their output
```

## Running the code

### Print the generated assembly

To print the asm source code:

```
$ python3 src/main.py examples/ex0.sil
```

### Compile and run the code

To compile and run the program:

```
$ ./scripts/compile.sh examples/ex0.sil
# OR
# c examples/ex0.sil           # I have an alias on my machine :-)
```

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

## Author

Wojciech Jedynak, 2019

