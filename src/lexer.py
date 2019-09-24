from enum import Enum, auto
from collections import namedtuple

class AutoName(Enum):
    @staticmethod
    def _generate_next_value_(name, start, count, last_values):
        return name

class Token(AutoName):
    LPAREN = auto()
    RPAREN = auto()
    LBRACE = auto()
    RBRACE = auto()
    SEMI = auto()
    BANG = auto()
    AND = auto()
    OR = auto()
    EQUAL = auto()
    DBL_EQ = auto()
    NOT_EQ = auto()
    GREATER = auto()
    GREATER_EQ = auto()
    LESS = auto()
    LESS_EQ = auto()
    PLUS = auto()
    MINUS = auto()
    TIMES = auto()
    DIVIDE = auto()
    MOD = auto()
    PLUS_EQ = auto()
    MINUS_EQ = auto()
    TIMES_EQ = auto()
    DIVIDE_EQ = auto()
    MOD_EQ = auto()
    NUMBER = auto()
    PRINT = auto()
    WHILE = auto()
    IF = auto()
    ELSE = auto()
    ID = auto()
    EOF = auto()

# I always wanted to do this!!
all_tokens = list(Token)

TokenInfo = namedtuple('TokenInfo', 
    ['tag', 'value', 'line', 'offset'])

def tokenize(s):
    """Tokenize the given string s into a generator of tokens."""

    line_no = 1
    offset = 0

    def token_info(*, tag, value):
        nonlocal line_no
        nonlocal offset
        return TokenInfo(tag=tag, value=value, 
            line=line_no, offset=offset)

    def token(tag):
        return token_info(tag=tag, value=None)

    # TODO: move these helpers somewhere or hide inside a class?
    iterator = iter(s + " ")
    unchar_v = None

    def getchar():
        nonlocal unchar_v
        nonlocal offset
        if unchar_v is not None:
            char = unchar_v
            unchar_v = None
        else:
            offset += 1
            char = next(iterator)
        return char
            
    def unchar(char):
        nonlocal unchar_v
        unchar_v = char

    # start of the proper lexel
    
    simple_tokens = {
        "(": Token.LPAREN,
        ")": Token.RPAREN,
        "{": Token.LBRACE,
        "}": Token.RBRACE,
        "+": Token.PLUS,
        "-": Token.MINUS,
        "*": Token.TIMES,
        "/": Token.DIVIDE,
        "%": Token.MOD,
        ";": Token.SEMI,
    }

    # note: we add the sentinel at the end to make sure
    # the number will be consumed in full
    while True:
        try:
            char = getchar()
            
            if char.isdigit():
                number = 0
                while char.isdigit():
                    number *= 10
                    number += int(char)
                    char = getchar()
                assert(char is not None)
                unchar(char)
                yield token_info(tag = Token.NUMBER, value = number)
            elif char == "/":
                char2 = getchar()
                if char2 == "/":
                    while char != "\n":
                        char = getchar()
                    unchar(char)
                elif char2 == "=":
                    yield token(Token.DIVIDE_EQ)
                else:
                    yield token(simple_tokens["/"])
            elif char in "&|":
                char2 = getchar()
                if char == char2 == "&":
                    yield token(Token.AND)
                elif char == char2 == "|":
                    yield token(Token.OR)
            elif char in "+-*%":
                char2 = getchar()
                if char2 == "=":
                    mk_eq = {
                        "+": Token.PLUS_EQ,
                        "-": Token.MINUS_EQ,
                        "*": Token.TIMES_EQ,
                        "%": Token.MOD_EQ,
                    }
                    yield token(mk_eq[char])
                else:
                    unchar(char2)
                    yield token(simple_tokens[char])
            elif char in simple_tokens:
                yield token(simple_tokens[char])
            elif char == " " or char == "\n":
                if char == "\n":
                    line_no += 1
                    offset = 0
                continue
            elif char == "!":
                char2 = getchar()
                if char2 == "=":
                    yield token(Token.NOT_EQ)
                else:
                    unchar(char2)
                    yield token(Token.BANG)
            elif char == "=":
                char2 = getchar()
                if char2 == "=":
                    yield token(Token.DBL_EQ)
                else:
                    unchar(char2)
                    yield token(Token.EQUAL)
            elif char == ">":
                char2 = getchar()
                if char2 == "=":
                    yield token(Token.GREATER_EQ)
                else:
                    unchar(char2)
                    yield token(Token.GREATER)
            elif char == "<":
                char2 = getchar()
                if char2 == "=":
                    yield token(Token.LESS_EQ)
                else:
                    unchar(char2)
                    yield token(Token.LESS)
            elif char.isalnum() or char == "_":
                value = ""
                while char.isalnum() or char == "_":
                    value += char
                    char = getchar()
                assert(char is not None)
                unchar(char)
                if value == "while":
                    yield token(Token.WHILE)
                elif value == "if":
                    yield token(Token.IF)
                elif value == "else":
                    yield token(Token.ELSE)
                elif value == "print":
                    yield token(Token.PRINT)
                else:
                    yield token_info(tag = Token.ID, value = value)
            else:
                raise Exception(f"found unknown character while tokenizing: [{char}]")
        except StopIteration:
            break    
    yield token(Token.EOF)

def simplify(tokens):
    for (tag, value, _line, _offset) in tokens:
        name = tag.name
        if value is not None:
            yield name, value
        else:
            yield name

if __name__ == "__main__":
    example = "(1 + 11 * 22)"
    print(example)
    print(list(simplify(tokenize(example))))

    example2 = "let x := 1 in x + x end"
    print(example2)
    print(list(simplify(tokenize(example2))))
