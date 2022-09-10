from lexer import Lexer
from parser import Parser


if __name__ == "__main__":

    input_code = """
    print (4 + 2 * 300);
    """

    lexer = Lexer().get_lexer()
    tokens = lexer.lex(input_code)
    # for token in tokens:
    #     print(token)
    parser_generator = Parser()
    parser_generator.parse()
    parser = parser_generator.get_parser()
    parser.parse(tokens).eval()
