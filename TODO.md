# Todo

Features to add:
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
- [x] Include expressions in statements (so we can write `foo(n);`)
- [ ] Type checker
- - [x] Scope checker
- - [x] Function arg number checking
- - [ ] Achieve 100% code coverage for the type checker
- - [ ] Argument type checking
- [ ] BUG: fix the result of `!n`
- [ ] Start using registers in the code instead of pushing everything on the stack
- [ ] Add true and false
- [ ] x++, x--, ++x, --x
- [ ] for loops
- [ ] Arrays
- [ ] Structs
- [ ] Static variables
- [ ] Floating-point operations
- [ ] Function pointers
- [ ] Cmd line arguments
- [ ] Cstrings
- [ ] Use a parser generator so that we can extend the parser more easily

Make the compiler more modular:
- [ ] Use an IL (intermediate language)

Add more backends:
- [ ] WebAssembly
- [ ] ARM (Raspberry PI)
- [ ] Mac (PowerPC?)
- [ ] MIPS (use the SPIM emulator)
- - [x] SPIM installed

Tooling:
- [ ] Enable pydoc generation
