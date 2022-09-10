from rply import LexerGenerator


class Lexer:
    def __init__(self):
        self.lexer = LexerGenerator()

    def add_tokens(self):
        # Functions
        self.lexer.add("PRINT", r"print")
        # # Logical Operators: && ||
        self.lexer.add("AND", r"\&\&")
        self.lexer.add("OR", r"\|\|")
        # Equality Operators == !=
        self.lexer.add("EQUAL", r"\=\=")
        self.lexer.add("NEQUAL", r"\!\=")
        # Relational Operators: = < > <= >=
        self.lexer.add("LESSQ", r"\<\=")
        self.lexer.add("GREATQ", r"\>\=")
        self.lexer.add("EQUALS", r"\=")
        self.lexer.add("GREAT", r"\>")
        self.lexer.add("LESS", r"\<")
        # Math Operators + - * / % **
        self.lexer.add("POWER", r"\*\*")
        self.lexer.add("PLUS", r"\+")
        self.lexer.add("MINUS", r"\-")
        self.lexer.add("TIMES", r"\*")
        self.lexer.add("DIVIDE", r"\/")
        self.lexer.add("MODULO", r"\%")
        # Primary Operators: ++ --
        self.lexer.add("INCREMENT", r"\+\+")
        self.lexer.add("DECREMENT", r"\-\-")
        # Data Types - Numbers
        self.lexer.add("FLOAT", r"-?\d+\.\d+")
        self.lexer.add("INTEGER", r"-?\d+")
        self.lexer.add("STRING", r'(".*")')
        # Identifiers
        self.lexer.add("IDENTIFIER", "[a-zA-Z_][a-zA-Z0-9_]*")
        # Delimiters: ( ) { } [ ] , . ; :
        self.lexer.add("LPAREN", r"\(")
        self.lexer.add("RPAREN", r"\)")
        self.lexer.add("LBRACE", r"\{")
        self.lexer.add("RBRACE", r"\}")
        self.lexer.add("LBRACKET", r"\[")
        self.lexer.add("RBRACKET", r"\]")
        self.lexer.add("PERIOD", r"\.")
        self.lexer.add("COMMA", r"\,")
        self.lexer.add("SEMI_COLON", r"\;")
        self.lexer.add("COLON", r"\:")
        # Others: \n #
        self.lexer.add("NEWLINE", r"\n+")
        self.lexer.add("COMMENT", r"\#")
        # Ignore White Spaces
        self.lexer.ignore("\s+")

    def get_lexer(self):
        self.add_tokens()
        return self.lexer.build()
