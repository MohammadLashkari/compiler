from rply import ParserGenerator
from parse_tree import Number, Sub, Sum, Div, Mul, Exponent, Print


class Parser:
    def __init__(self):
        self.parser_generator = ParserGenerator(
            # fmt: off
            # A List Of All Token Names Accepted By The Parser
            ['FLOAT', 'INTEGER', 'STRING', 'IDENTIFIER',
             'PLUS', 'MINUS', 'TIMES', 'DIVIDE', 'MODULO','POWER',
             'AND', 'OR','INCREMENT', 'DECREMENT',
             'EQUALS', 'GREAT', 'LESS', 'GREATQ', 'LESSQ', 'NEQUAL', 'EQUAL',
             'IF', 'ELSE', 'FOR', 'SEMI_COLON', 'COMMA', 'COLON', 'PERIOD', 'LPAREN', 'RPAREN',
             'LBRACE', 'RBRACE', 'LBRACKET', 'RBRACKET', 'COMMENT', 'NEWLINE',
             'PRINT']
            # fmt: on
        )

    def parse(self):
        @self.parser_generator.production(
            "program : PRINT LPAREN expression RPAREN SEMI_COLON"
        )
        def program_parens(production):
            return Print(production[2])

        @self.parser_generator.production("expression : expression PLUS expression")
        @self.parser_generator.production("expression : expression MINUS expression")
        @self.parser_generator.production("expression : expression TIMES expression")
        @self.parser_generator.production("expression : expression DIVIDE expression")
        @self.parser_generator.production("expression : expression POWER expression")
        def expression_binop(production):
            left = production[0]
            right = production[2]
            operator = production[1]

            if operator.gettokentype() == "PLUS":
                return Sum(left, right)
            elif operator.gettokentype() == "MINUS":
                return Sub(left, right)
            elif operator.gettokentype() == "TIMES":
                return Mul(left, right)
            elif operator.gettokentype() == "DIVIDE":
                return Div(left, right)
            elif operator.gettokentype() == "POWER":
                return Exponent(left, right)

        @self.parser_generator.production("expression : INTEGER")
        def expression_number(production):
            return Number(production[0].value)

        @self.parser_generator.error
        def error_handle(token):
            raise ValueError(
                "Ran into a %s where it wasn't expected" % token.gettokentype()
            )

    def get_parser(self):
        return self.parser_generator.build()
