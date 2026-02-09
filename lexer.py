# lexer.py

from token import Token
from symbol_table import SymbolTable


class Lexer:
    KEYWORDS = {
        "public", "class", "static", "final", "void",
        "int", "double", "String", "if", "else",
        "return", "new", "private", "this"
    }

    OPERATORS = {
        "+", "-", "*", "/", "=",
        "<", ">", "<=", ">=", "==", "!=",
        "&&", "||"
    }

    PUNCTUATION = {
        "(", ")", "{", "}", "[", "]",
        ";", ",", "."
    }

    REGEX_PATTERNS = {
        "IDENTIFIER": r"[a-zA-Z_][a-zA-Z0-9_]*",
        "KEYWORD": r"(public|class|static|final|void|int|double|String|if|else|return|new|private|this)",
        "NUMBER": r"[0-9]+(\.[0-9]+)?",
        "OPERATOR": r"(\+|-|\*|/|==|!=|<=|>=|<|>|&&|\|\|)",
        "STRING": r"\".*?\"",
        "PUNCTUATION": r"[\(\)\{\}\[\];,\.]"
    }

    def __init__(self, source_code):
        self.source = source_code
        self.position = 0
        self.line = 1
        self.column = 1
        self.tokens = []
        self.symbol_table = SymbolTable()
        self.detected_lexeme_types = set()
        

    def peek(self):
        if self.position < len(self.source):
            return self.source[self.position]
        return None

    def _next_char(self):
        if self.position + 1 < len(self.source):
            return self.source[self.position + 1]
        return None

    def advance(self):
        char = self.peek()
        self.position += 1
        if char == "\n":
            self.line += 1
            self.column = 1
        else:
            self.column += 1
        return char

    def tokenize(self):
        self.detected_lexeme_types.add("OPERATOR")
        self.detected_lexeme_types.add("PUNCTUATION")

        while self.peek():
            char = self.peek()

            # Ignore whitespace
            if char.isspace():
                self.advance()
                continue

            # Line comment //
            if char == "/" and self._next_char() == "/":
                self._skip_line_comment()
                continue

            # Block comment /* */
            if char == "/" and self._next_char() == "*":
                self._skip_block_comment()
                continue

            # Identifiers / keywords
            if char.isalpha() or char == "_":
                self._tokenize_identifier()
                continue

            # Numbers
            if char.isdigit():
                self._tokenize_number()
                continue

            # Strings
            if char == '"':
                self._tokenize_string()
                self.detected_lexeme_types.add("STRING")

                continue

            two_char = char + (self._next_char() or "")
            if two_char in self.OPERATORS:
                start_col = self.column
                self.advance()
                self.advance()
                self.tokens.append(
                    Token("OPERATOR", two_char, self.line, start_col)
                )
                continue

            if char in self.OPERATORS:
                start_col = self.column
                self.tokens.append(
                    Token("OPERATOR", self.advance(), self.line, start_col)
                )
                continue

            if char in self.PUNCTUATION:
                start_col = self.column
                self.tokens.append(
                    Token("PUNCTUATION", self.advance(), self.line, start_col)
                )
                continue

            start_col = self.column
            self.tokens.append(
                Token("UNKNOWN", self.advance(), self.line, start_col)
                
            )

        return self.tokens

    def _tokenize_identifier(self):
        start_col = self.column
        
        lexeme = ""

        while self.peek() and (self.peek().isalnum() or self.peek() == "_"):
            lexeme += self.advance()

        if lexeme in self.KEYWORDS:
            token_type = "KEYWORD"
        else:
            token_type = "IDENTIFIER"
            self.symbol_table.add(lexeme, token_type)

        self.tokens.append(Token(token_type, lexeme, self.line, start_col))
        self.detected_lexeme_types.add(token_type)

    def _tokenize_number(self):
        start_col = self.column
        lexeme = ""
        dot_count = 0
        

        while self.peek() and (self.peek().isdigit() or self.peek() == "."):
            if self.peek() == ".":
                dot_count += 1
            lexeme += self.advance()

        self.detected_lexeme_types.add("NUMBER")
        self.tokens.append(Token("NUMBER", lexeme, self.line, start_col))

    def _tokenize_string(self):
        start_col = self.column
        lexeme = self.advance() 

        while self.peek() and self.peek() != '"':
            lexeme += self.advance()

        if self.peek() == '"':
            lexeme += self.advance()

        self.tokens.append(Token("STRING", lexeme, self.line, start_col))

    def _skip_line_comment(self):
        # Consume "//"
        self.advance()
        self.advance()

        while self.peek() and self.peek() != "\n":
            self.advance()

    def _skip_block_comment(self):
        # Consume "/*"
        self.advance()
        self.advance()

        while self.peek():
            if self.peek() == "*" and self._next_char() == "/":
                self.advance()  # *
                self.advance()  # /
                break
            else:
                self.advance()

    def report_lexeme_patterns(self):
        print("\n=== LEXEME TYPES AND REGULAR EXPRESSIONS ===")
        for lexeme_type in self.detected_lexeme_types:
            regex = self.REGEX_PATTERNS.get(lexeme_type, "No regex defined")
            print(f"{lexeme_type:<15} -> {regex}")

