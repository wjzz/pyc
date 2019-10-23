2019/10/22
* implemented early jumps for `return`

`return` should jump to the function epilogue. We want the lexically closest one,
so keeping a stack of the epilogue labels is enough.

* implemented `break` and `continue`

This is very similar to `return`, but this time we look at loop labels instead of function labels.
Since `break` jumps to the loop_end label and `continue` jumps to the loop_start label we keep
a stack of loop [start, end] label pairs.

* tabs in source code are allowed

* removed the old syntax (python-like top-level statements instead of c-style main function)

* removed the old AST-based tests (there were used when there was no parser)

* removed many unused files, including a while-interpreter (I was not maintaining it anyways)

* BUG: my implementation of local variables was *very* naive and it's incorrect. Locals have to be put on the stack along with parameters - otherwise recursive functions won't work properly!

* implemented putting local variables on the stack.
I made the same mistake again - to allocate more memory we have to *substract* from rsp, not add - the stack grows downwards here!
Also it's important to always remember that we use a stack so if we allocate stuff, then we have to deallocate in the reverse order.

* implemented variable renaming - this way we get block scoping for free, without having to manage another stack for that

2019/10/23

* extended StmDecl with a flag to denote if the variable is local, global or static

* implemented global variables again. Static variables are not handled yet.
