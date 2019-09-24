import unittest
from lexer import tokenize, simplify
from parser import parse_stm, parse_bool, parse_expr
from ast import *

class Tests(unittest.TestCase):
    pass
    # def test_expr_str(self):
    #     n = NumberLit(11)
    #     m = NumberLit(22)
    #     self.assertEqual(str(n), "11")
    #     self.assertEqual(str(m), "22")
    #     x = Variable("x")
    #     self.assertEqual(str(x), "x")
    #     e1 = BinaryOp(n, Op.Plus, m)
    #     self.assertEqual(str(e1), "(11 + 22)")
    #     e2 = BinaryOp(n, Op.Mult, m)
    #     self.assertEqual(str(e2), "(11 * 22)")
    #     e3 = BinaryOp(e1, Op.Mult, e1)
    #     self.assertEqual(str(e3), "((11 + 22) * (11 + 22))")
    #     y = Variable("y")
    #     self.assertEqual(str(y), "y")
    #     e4 = BinaryOp(x, Op.Plus, y)
    #     self.assertEqual(str(e4), "(x + y)")
    #     e5 = LetIn("x", n, x)
    #     self.assertEqual(str(e5), "(let x := 11 in x)")
    #     e6 = LetIn("x", n, BinaryOp(x, Op.Plus, x))
    #     self.assertEqual(str(e6), "(let x := 11 in (x + x))")

    def test_lexer(self):
        e1 = "1"
        self.assertEqual(list(simplify(tokenize(e1))),
            [('NUMBER', 1), 'EOF'])
        
        input_str = "(1 + 11 * 22)"

        result = list(simplify(tokenize(input_str)))

        expected = ['LPAREN', ('NUMBER', 1), 'PLUS', ('NUMBER', 11), 
            'TIMES', ('NUMBER', 22), 'RPAREN', 'EOF']
        
        self.assertEqual(expected, result)

    def test_lexer_ident(self):
        inputs = [
            ("x", 
            [('ID', 'x'), 'EOF']),
            ("x123", 
            [('ID', 'x123'), 'EOF']),
            ("x_123", 
            [('ID', 'x_123'), 'EOF']),

        ]
        for (input, expected) in inputs:
            with self.subTest(input=input):
                self.assertEqual(
                    list(simplify(tokenize(input))),
                    expected)

    def test_lexer_ops(self):
        inputs = [
            ("x == 0", 
                [('ID', 'x'), 'DBL_EQ', ('NUMBER', 0), 'EOF']),
            ("x != 0", 
                [('ID', 'x'), 'NOT_EQ', ('NUMBER', 0), 'EOF']),
            ("x >= 0", 
                [('ID', 'x'), 'GREATER_EQ', ('NUMBER', 0), 'EOF']),
            ("x > 0", 
                [('ID', 'x'), 'GREATER', ('NUMBER', 0), 'EOF']),
            ("x <= 0", 
                [('ID', 'x'), 'LESS_EQ', ('NUMBER', 0), 'EOF']),
            ("x < 0", 
                [('ID', 'x'), 'LESS', ('NUMBER', 0), 'EOF']),
            ("! (x == 0)", 
                ['BANG', 'LPAREN', ('ID', 'x'), 'DBL_EQ', 
                    ('NUMBER', 0), 'RPAREN', 'EOF']),
            
        ]
        for (input, expected) in inputs:
            with self.subTest(input=input):
                self.assertEqual(
                    list(simplify(tokenize(input))),
                    expected)

    def test_lexer_while(self):
        input_str = "while (x > 0) { x = 10; } "

        result = list(simplify(tokenize(input_str)))

        expected = ['WHILE', 'LPAREN', ('ID', 'x'),
                   'GREATER', ('NUMBER', 0), 'RPAREN',
                   'LBRACE', ('ID', 'x'), 'EQUAL', ('NUMBER', 10),
                   'SEMI', 'RBRACE', 'EOF']
        
        self.assertEqual(expected, result)

    def test_lexer_if(self):
        input_str = "if (x > 0) { x = 10; } else { x = 5; }"

        result = list(simplify(tokenize(input_str)))

        expected = ['IF', 'LPAREN', ('ID', 'x'),
                   'GREATER', ('NUMBER', 0), 'RPAREN',
                   'LBRACE', ('ID', 'x'), 'EQUAL', ('NUMBER', 10),
                   'SEMI', 'RBRACE', 'ELSE', 
                   'LBRACE', ('ID', 'x'), 'EQUAL', ('NUMBER', 5),
                   'SEMI', 'RBRACE', 'EOF']
        
        self.assertEqual(expected, result)

    def test_lexer_print(self):
        input_str = "print(x);"

        result = list(simplify(tokenize(input_str)))

        expected = ['PRINT', 'LPAREN', ('ID', 'x'),
                   'RPAREN', 'SEMI', 'EOF']
        
        self.assertEqual(expected, result)

    def test_lexer_compound_assign(self):
        inputs = [
            ("x += 1", 
            [('ID', 'x'), 'PLUS_EQ', ('NUMBER', 1), 'EOF']),
            ("x -= 1", 
            [('ID', 'x'), 'MINUS_EQ', ('NUMBER', 1), 'EOF']),
            ("x *= 1", 
            [('ID', 'x'), 'TIMES_EQ', ('NUMBER', 1), 'EOF']),
            ("x /= 1", 
            [('ID', 'x'), 'DIVIDE_EQ', ('NUMBER', 1), 'EOF']),
            ("x %= 1", 
            [('ID', 'x'), 'MOD_EQ', ('NUMBER', 1), 'EOF']),
        ]

        for (input, expected) in inputs:
            with self.subTest(input=input):
                self.assertEqual(
                    list(simplify(tokenize(input))),
                    expected)

    def test_parser_expr(self):
        v1 = "x"
        self.assertEqual(parse_expr(v1), ArithVar("x"))

        v2 = "(x)"
        self.assertEqual(parse_expr(v2), ArithVar("x"))

        v3 = "thisisalongvariable"
        self.assertEqual(parse_expr(v3), ArithVar(v3))

        e1 = "1"
        self.assertEqual(parse_expr(e1), ArithLit(1))

        e2 = "(1)"
        self.assertEqual(parse_expr(e2), ArithLit(1))

        e3 = "((1))"
        self.assertEqual(parse_expr(e3), ArithLit(1))

        e4 = "(1 + 2)"
        r4 = ArithBinop(
                ArithOp.Add,
                ArithLit(1),
                ArithLit(2))
        self.assertEqual(parse_expr(e4), r4)

        e5 = "1 + 2"
        self.assertEqual(parse_expr(e5), r4)

        e6 = "(1 * 2)"
        r6 = ArithBinop(
                ArithOp.Mul,
                ArithLit(1),
                ArithLit(2))
        self.assertEqual(parse_expr(e6), r6)

        e7 = "1 * 2"
        self.assertEqual(parse_expr(e7), r6)

        e8 = "1 + 2 * 3"
        r8 = ArithBinop(
                ArithOp.Add,
                ArithLit(1),
                ArithBinop(
                    ArithOp.Mul,
                    ArithLit(2),
                    ArithLit(3)
                ))
        self.assertEqual(parse_expr(e8), r8)

        e9 = "(1 - 2)"
        r9 = ArithBinop(
                ArithOp.Sub,
                ArithLit(1),
                ArithLit(2))
        self.assertEqual(parse_expr(e9), r9)

        e10 = "(1 / 2)"
        r10 = ArithBinop(
                ArithOp.Div,
                ArithLit(1),
                ArithLit(2))
        self.assertEqual(parse_expr(e10), r10)

        e11 = "(1 % 2)"
        r11 = ArithBinop(
                ArithOp.Mod,
                ArithLit(1),
                ArithLit(2))
        self.assertEqual(parse_expr(e11), r11)

    def test_parser_bool(self):
        b1 = "x == 1"
        self.assertEqual(parse_bool(b1), 
            BoolArithCmp(
                ArithCmp.Eq,
                ArithVar("x"),
                ArithLit(1)))

        # b1a = "(x == 1)"
        # self.assertEqual(parse_bool(b1a), 
        #     BoolArithCmp(
        #         ArithCmp.Eq,
        #         ArithVar("x"),
        #         ArithLit(1)))

        b2 = "x != 1"
        self.assertEqual(parse_bool(b2), 
            BoolArithCmp(
                ArithCmp.Neq,
                ArithVar("x"),
                ArithLit(1)))

        b3 = "x > 1"
        self.assertEqual(parse_bool(b3), 
            BoolArithCmp(
                ArithCmp.Gt,
                ArithVar("x"),
                ArithLit(1)))

    def test_parser_stm(self):
        s1 = "print(x);"
        self.assertEqual(parse_stm(s1), 
            [StmPrint(ArithVar("x"))])

        s1a = "print(x_);"
        self.assertEqual(parse_stm(s1a), 
            [StmPrint(ArithVar("x_"))])


        s2 = "print(15);"
        self.assertEqual(parse_stm(s2), 
            [StmPrint(ArithLit(15))])

        s3 = "x = 1;"
        self.assertEqual(parse_stm(s3), 
            [StmAssign("x", ArithLit(1))])

        s3a = "x += 1;"
        self.assertEqual(parse_stm(s3a), 
            [StmAssign("x", 
                ArithBinop(
                    ArithOp.Add,
                    ArithVar("x"),
                    ArithLit(1)
                ))])

        s3b = "x -= 1;"
        self.assertEqual(parse_stm(s3b), 
            [StmAssign("x", 
                ArithBinop(
                    ArithOp.Sub,
                    ArithVar("x"),
                    ArithLit(1)
                ))])

        s3c = "x *= 1;"
        self.assertEqual(parse_stm(s3c), 
            [StmAssign("x", 
                ArithBinop(
                    ArithOp.Mul,
                    ArithVar("x"),
                    ArithLit(1)
                ))])

        s3d = "x /= 1;"
        self.assertEqual(parse_stm(s3d), 
            [StmAssign("x", 
                ArithBinop(
                    ArithOp.Div,
                    ArithVar("x"),
                    ArithLit(1)
                ))])

        s3d = "x %= 1;"
        self.assertEqual(parse_stm(s3d), 
            [StmAssign("x", 
                ArithBinop(
                    ArithOp.Mod,
                    ArithVar("x"),
                    ArithLit(1)
                ))])

        s4 = "while (x == 1) {}"
        self.assertEqual(parse_stm(s4), 
            [
                StmWhile(
                    BoolArithCmp(
                        ArithCmp.Eq,
                        ArithVar("x"),
                        ArithLit(1)
                    ),
                    [])
            ])

        s5 = "while (x == 1) { x = x + 1; }"
        self.assertEqual(parse_stm(s5), 
            [
                StmWhile(
                    BoolArithCmp(
                        ArithCmp.Eq,
                        ArithVar("x"),
                        ArithLit(1)
                    ),
                    [
                        StmAssign("x", 
                            ArithBinop(
                                ArithOp.Add,
                                ArithVar("x"),
                                ArithLit(1))
                            )
                    ])
            ])

        s6 = "if (x == 1) {}"
        self.assertEqual(parse_stm(s6), 
            [
                StmIf(
                    BoolArithCmp(
                        ArithCmp.Eq,
                        ArithVar("x"),
                        ArithLit(1)
                    ),
                    [],
                    [])
            ])

        s7 = "if (x == 1) {} else {}"
        self.assertEqual(parse_stm(s7), 
            [
                StmIf(
                    BoolArithCmp(
                        ArithCmp.Eq,
                        ArithVar("x"),
                        ArithLit(1)
                    ),
                    [],
                    [])
            ])
        
    # def test_evaluator(self):
    #     n = NumberLit(2)
    #     m = NumberLit(3)
    #     self.assertEqual(evaluate(n), 2)
    #     self.assertEqual(evaluate(m), 3)
    #     e1 = BinaryOp(n, Op.Plus, m)
    #     self.assertEqual(evaluate(e1), 5)
    #     e2 = BinaryOp(n, Op.Mult, m)
    #     self.assertEqual(evaluate(e2), 6)
    #     e3 = BinaryOp(e1, Op.Mult, e1)
    #     self.assertEqual(evaluate(e3), 25)

    # def test_everything_together(self):
    #     def test(a, b):
    #         self.assertEqual(ev(a), b)

    #     test("1", 1)
    #     test("1 + 1", 2)
    #     test("1+2+3+4", 10)
    #     test("1 + 1 + 1 + 1", 4)
    #     test("2 + 2 * 2", 6)
    #     test("(2 + 2) * 2", 8)
    #     test("2 * 2 + 2", 6)
    #     test("(2 + 2) * (2 + 2)", 16)
    #     test("2+2*2+2", 8)
    #     test("let x := 1 in x + x end", 2)
    #     test("let z := 2 in z * z end", 4)
    #     test("1 + let x := 1 in x + x end", 3)
    #     test("let x := 2 in (let y := 3 in x + y end) end", 5)

if __name__ == "__main__":
    unittest.main()
