from lexer import tokenize, Token, TokenInfo
import ast as E

# STM_TOP ::= <STM_LIST> EOF
# STM_LIST ::= <STM> | <STM> <STM_LIST>
# STM ::= PRINT ( <EXPR> ) SEMI
#       | VAR = <EXPR> SEMI
#       | WHILE ( <BOOL> ) <BLOCK>
#       | IF ( <BOOL> ) <BLOCK> (ELSE <BLOCK>)?

# BLOCK ::= 
#        | ;


# ARITH_CMP ::= == | != | > | >= | < | <=
# BOOL ::= <EXPR> <ARITH_CMP> <EXPR>

# EXPR_TOP ::= <EXPR> EOF
# EXPR ::= <FACTOR> | <FACTOR> [+-] <EXPR>
# FACTOR ::= <ATOM> | <ATOM> [*/%] <FACTOR>
# ATOM = NUM | ID ( <EXPR> )

class Parser:
    def __init__(self, tokens):
        self._tokens = tokens

    @property
    def get_token(self):
        return next(self._tokens)

    @property
    def peek(self):
        self._tokens = self.peekable(self._tokens)
        return next(self._tokens)

    def peekable(self, gen):
        val = next(gen)
        yield val
        yield val
        yield from gen

    def expect(self, *expected_tags):
        token = self.get_token
        assert(token.tag in expected_tags)

    #-----------------------------------
    # Statements

    def parse_stm_top(self):
        s = self.parse_stm_many()
        self.expect(Token.EOF)
        return s
    
    def parse_stm_many(self, end=Token.EOF):
        s = self.parse_stm()
        token = self.peek
        if token.tag != end:
            ss = self.parse_stm_many()
            return [s] + ss
        else:
            return [s]

    def parse_stm(self):
        token = self.get_token
        if token.tag == Token.PRINT:
            self.expect(Token.LPAREN)
            a = self.parse_expr()
            self.expect(Token.RPAREN)
            self.expect(Token.SEMI)
            return E.StmPrint(a)
        elif token.tag == Token.ID:
            var = token.value
            self.expect(Token.EQUAL)
            a = self.parse_expr()
            self.expect(Token.SEMI)
            return E.StmAssign(var, a)
        elif token.tag == Token.WHILE:
            self.expect(Token.LPAREN)
            b = self.parse_bool()
            self.expect(Token.RPAREN)
            ss = self.parse_block()
            return E.StmWhile(b, ss)
        elif token.tag == Token.IF:
            self.expect(Token.LPAREN)
            b = self.parse_bool()
            self.expect(Token.RPAREN)
            ss1 = self.parse_block()
            if self.peek.tag == Token.ELSE:
                self.expect(Token.ELSE)
                ss2 = self.parse_block()
            else:
                ss2 = []
            return E.StmIf(b, ss1, ss2)
        else:
            raise Exception(f"unexpected tag = {token.tag}")

    def parse_block(self):
        token = self.peek
        if token.tag == Token.LBRACE:
            self.expect(Token.LBRACE)
            ss = []
            while self.peek.tag != Token.RBRACE:
                ss.append(self.parse_stm())
            self.expect(Token.RBRACE)
            return ss
        else:
            return self.parse_stm()

    #-----------------------------------
    # Boolean Expressions

    def parse_bool_top(self):
        b = self.parse_bool()
        self.expect(Token.EOF)
        return b

    def parse_bool(self):
        operators = {
            Token.DBL_EQ : E.ArithCmp.Eq,
            Token.NOT_EQ : E.ArithCmp.Neq,
            Token.GREATER_EQ : E.ArithCmp.Geq,
            Token.GREATER : E.ArithCmp.Gt,
            Token.LESS_EQ : E.ArithCmp.Leq,
            Token.LESS : E.ArithCmp.Lt,
        }
        a1 = self.parse_expr()
        operator = self.get_token.tag
        assert (operator in operators.keys())
        a2 = self.parse_expr()
        return E.BoolArithCmp(
            operators[operator],
            a1,
            a2)

    #-----------------------------------
    # Arith Expressions

    def parse_expr_top(self):
        e = self.parse_expr()
        self.expect(Token.EOF)
        return e

    def parse_expr(self):
        factor = self.parse_factor()
        token = self.peek
        if token.tag not in [Token.PLUS, Token.MINUS]:
            return factor
        else:
            tags = {
                Token.PLUS : E.ArithOp.Add,
                Token.MINUS : E.ArithOp.Sub,
            }
            self.expect(Token.PLUS, Token.MINUS)
            expr = self.parse_expr()
            tag = tags[token.tag]
            return E.ArithBinop(tag, factor, expr)

    def parse_factor(self):
        atom = self.parse_atom()
        token = self.peek
        tags = {
            Token.TIMES : E.ArithOp.Mul,
            Token.DIVIDE : E.ArithOp.Div,
            Token.MOD : E.ArithOp.Mod,
        }

        if token.tag not in tags.keys():
            return atom
        else:
            self.expect(*tags.keys())
            factor = self.parse_factor()
            tag = tags[token.tag]
            return E.ArithBinop(tag, atom, factor)

    def parse_atom(self):
        token = self.get_token
        if token.tag == Token.LPAREN:
            e = self.parse_expr()
            self.expect(Token.RPAREN)
            return e
        elif token.tag == Token.NUMBER:
            return E.ArithLit(token.value)
        elif token.tag == Token.ID:
            return E.ArithVar(token.value)
        else:
            raise Exception(f"unexpected tag: {token.tag}")

def parse_expr(s):
    """
    Takes an input string and outputs an expr AST
    """
    tokens = tokenize(s)
    #print(list(tokenize(s)))
    return Parser(tokens).parse_expr_top()

def parse_bool(s):
    """
    Takes an input string and outputs a bool expr AST
    """
    tokens = tokenize(s)
    #print(list(tokenize(s)))
    return Parser(tokens).parse_bool_top()

def parse_stm(s):
    """
    Takes an input string and outputs a stm AST
    """
    tokens = tokenize(s)
    #print(list(tokenize(s)))
    return Parser(tokens).parse_stm_top()
