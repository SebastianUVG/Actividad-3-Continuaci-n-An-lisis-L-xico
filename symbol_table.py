# symbol_table.py

class SymbolTable:
    def __init__(self):
        self.symbols = {}

    def add(self, identifier, token_type):
        if identifier not in self.symbols:
            self.symbols[identifier] = token_type

    def __repr__(self):
        output = "\n=== SYMBOL TABLE ===\n"
        for name, ttype in self.symbols.items():
            output += f"{name:<25} {ttype}\n"
        return output
