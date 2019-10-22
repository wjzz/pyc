2019/10/22
* implemented early jumps for `return`

`return` should jump to the function epilogue. We want the lexically closest one,
so keeping a stack of the epilogue labels is enough.

* implemented `break` and `continue`

This is very similar to `return`, but this time we look at loop labels instead of function labels.
Since `break` jumps to the loop_end label and `continue` jumps to the loop_start label we keep
a stack of loop [start, end] label pairs.

* tabs in source code are allowed
