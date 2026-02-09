# main.py

from lexer import Lexer

def main():
    with open("PotionBrever.java", "r", encoding="utf-8") as file:
        source_code = file.read()

    lexer = Lexer(source_code)
    tokens = lexer.tokenize()

    print("=== TOKENS ===")
    for token in tokens:
        print(token)

    print(lexer.symbol_table)

    # 👉 RESPUESTA AL EJERCICIO
    lexer.report_lexeme_patterns()

main()

