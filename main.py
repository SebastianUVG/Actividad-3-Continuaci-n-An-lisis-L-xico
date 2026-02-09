from dfa import IdentifierRegexTree, build_dfa_from_syntax_tree
from lexer import Lexer
from minimizador_dfa import minimize_dfa
from demostracion import simulate_dfa

def number_symbol_map(char):
    if char.isdigit():
        return "DIGIT"
    elif char == ".":
        return "DOT"
    else:
        return None


def main():
    with open("PotionBrever.java", "r", encoding="utf-8") as file:
        source_code = file.read()

    lexer = Lexer(source_code)
    tokens = lexer.tokenize()

    print("=== TOKENS ===")
    for token in tokens:
        print(token)

    print(lexer.symbol_table)

    lexer.report_lexeme_patterns()

    

    print("\n DFA CONSTRUCTION (Number) ")
    tree = IdentifierRegexTree()
    root = tree.build_tree()

    tree.compute_nullable_first_last(root)
    tree.compute_followpos(root)
    
    tree.report()
    dfa = build_dfa_from_syntax_tree(tree)
    minimize_dfa(dfa)


    #lexema válido
    simulate_dfa(dfa, "12.34", number_symbol_map)

    #inválido
    simulate_dfa(dfa, "12.", number_symbol_map)
main()

