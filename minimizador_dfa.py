def minimize_dfa(dfa):
    print("\n------------------ DFA MINIMIZATION -------------------")

    P = [
        set(dfa["accepting"]),
        set(dfa["states"]) - set(dfa["accepting"])
    ]

    print("\nInitial partition:")
    print(P)

    changed = True
    step = 1

    while changed:
        print(f"\n--- Refinement step {step} ---")
        changed = False
        new_P = []

        for group in P:
            blocks = {}

            for state in group:
                signature = []

                for symbol in dfa["alphabet"]:
                    target = dfa["transitions"].get((state, symbol))
                    for i, block in enumerate(P):
                        if target in block:
                            signature.append(i)
                            break
                    else:
                        signature.append(None)

                signature = tuple(signature)
                blocks.setdefault(signature, set()).add(state)

            if len(blocks) > 1:
                changed = True
                for b in blocks.values():
                    print("Split:", b)
                new_P.extend(blocks.values())
            else:
                new_P.append(group)

        P = new_P
        step += 1

    print("\nFinal partition:")
    print(P)
    return P
