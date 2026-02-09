# token.py

class Token:
    def __init__(self, token_type, lexeme, line, column):
        self.token_type = token_type
        self.lexeme = lexeme
        self.line = line
        self.column = column

    def __repr__(self):
        return f"{self.token_type:<15} {self.lexeme:<25} (line {self.line}, col {self.column})"
