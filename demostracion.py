def simulate_dfa(dfa, lexeme, symbol_map):
    print("\n----------------- DFA SIMULATION ------------------------")
    current_state = dfa["start"]
    print(f"Start state: {current_state}")

    for i, char in enumerate(lexeme):
        symbol = symbol_map(char)
        print(f"\nStep {i + 1}")
        print(f"Read character: '{char}' -> symbol: {symbol}")

        transition_key = (current_state, symbol)

        if transition_key not in dfa["transitions"]:
            print("No transition found. Lexeme REJECTED.")
            return False

        next_state = dfa["transitions"][transition_key]
        print(f"Transition: {current_state} --{symbol}--> {next_state}")

        current_state = next_state

    print("\nEnd of input.")
    if current_state in dfa["accepting"]:
        print(f"Final state {current_state} is accepting. Lexeme ACCEPTED.")
        return True
    else:
        print(f"Final state {current_state} is NOT accepting. Lexeme REJECTED.")
        return False
