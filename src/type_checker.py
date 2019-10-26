"""
Type checking of C programs.

We check that:
- all names are in scope
- there are no type errors
"""

from typing import List, Any

Stm = Any
SymbolTable = Any


class CTypeError(Exception):
    def __init__(self, msg):
        self.msg = msg

    def __str__(self):
        return f"{self.msg}"


def check(c: List[Stm]) -> SymbolTable:
    """
    Type checks the given program.

    Raises a CTypeError if there are some problems with the given input.
    """
    symbol_table = None
    return symbol_table
