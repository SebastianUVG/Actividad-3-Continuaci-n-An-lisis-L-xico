class SyntaxTreeNode:
    def __init__(self, value, left=None, right=None, position=None):
        self.value = value
        self.left = left
        self.right = right
        self.position = position

        self.nullable = False
        self.firstpos = set()
        self.lastpos = set()


class IdentifierRegexTree:
    def __init__(self):
        self.followpos = {}
        self.position_counter = 1
        self.leaves = {}
        self.root = None

    def new_leaf(self, symbol):
        pos = self.position_counter
        self.position_counter += 1

        node = SyntaxTreeNode(symbol, position=pos)
        node.nullable = False
        node.firstpos = {pos}
        node.lastpos = {pos}

        self.leaves[pos] = symbol
        self.followpos[pos] = set()
        return node

    def build_tree(self):
         # REGEX: [0-9]+(\.[0-9]+)? #

        digit1 = self.new_leaf("DIGIT")
        digit2 = self.new_leaf("DIGIT")

        digit_star1 = SyntaxTreeNode("*", left=digit2)

        integer_part = SyntaxTreeNode(".", left=digit1, right=digit_star1)

        dot = self.new_leaf("DOT")
        digit3 = self.new_leaf("DIGIT")
        digit4 = self.new_leaf("DIGIT")

        digit_star2 = SyntaxTreeNode("*", left=digit4)
        fractional_digits = SyntaxTreeNode(".", left=digit3, right=digit_star2)
        fractional_part = SyntaxTreeNode(".", left=dot, right=fractional_digits)

        epsilon = SyntaxTreeNode("ε")
        epsilon.nullable = True
        epsilon.firstpos = set()
        epsilon.lastpos = set()

        optional_fraction = SyntaxTreeNode("|", left=fractional_part, right=epsilon)

        full_number = SyntaxTreeNode(".", left=integer_part, right=optional_fraction)

        end = self.new_leaf("#")
        self.root = SyntaxTreeNode(".", left=full_number, right=end)

        return self.root

    def compute_nullable_first_last(self, node):
        if node is None:
            return

        # Postorden
        self.compute_nullable_first_last(node.left)
        self.compute_nullable_first_last(node.right)

        if node.position is not None:
            # Hoja
            node.nullable = False
            node.firstpos = {node.position}
            node.lastpos = {node.position}

        elif node.value == ".":
            node.nullable = node.left.nullable and node.right.nullable

            node.firstpos = (
                node.left.firstpos | node.right.firstpos
                if node.left.nullable else node.left.firstpos
            )

            node.lastpos = (
                node.left.lastpos | node.right.lastpos
                if node.right.nullable else node.right.lastpos
            )

        elif node.value == "*":
            node.nullable = True
            node.firstpos = node.left.firstpos
            node.lastpos = node.left.lastpos
        
        elif node.value == "|":
            node.nullable = node.left.nullable or node.right.nullable
            node.firstpos = node.left.firstpos | node.right.firstpos
            node.lastpos = node.left.lastpos | node.right.lastpos

    def compute_followpos(self, node):
        if node is None:
            return

        self.compute_followpos(node.left)
        self.compute_followpos(node.right)

        if node.value == ".":
            for i in node.left.lastpos:
                self.followpos[i] |= node.right.firstpos

        elif node.value == "*":
            for i in node.lastpos:
                self.followpos[i] |= node.firstpos

    def report(self):
        print("\n=== SYNTAX TREE POSITIONS ===")
        for pos, sym in self.leaves.items():
            print(f"Position {pos}: {sym}")

        print("\n=== FOLLOWPOS TABLE ===")
        for pos, f in self.followpos.items():
            print(f"followpos({pos}) = {f}")

        print("\nRoot nullable:", self.root.nullable)
        print("Root firstpos:", self.root.firstpos)
        print("Root lastpos:", self.root.lastpos)


def build_dfa_from_syntax_tree(tree: IdentifierRegexTree):
    print("\n-------------- DFA CONSTRUCTION -------------------")

    alphabet = set(tree.leaves.values())
    alphabet.discard("#")

    start_state = frozenset(tree.root.firstpos)
    states = [start_state]
    transitions = {}
    accepting_states = set()

    if any(tree.leaves[p] == "#" for p in start_state):
        accepting_states.add(start_state)

    i = 0
    while i < len(states):
        state = states[i]

        for symbol in alphabet:
            next_state = set()

            for pos in state:
                if tree.leaves[pos] == symbol:
                    next_state |= tree.followpos[pos]

            next_state = frozenset(next_state)

            if next_state:
                transitions[(state, symbol)] = next_state

                if next_state not in states:
                    states.append(next_state)
                    if any(tree.leaves[p] == "#" for p in next_state):
                        accepting_states.add(next_state)

        i += 1

    print("\nDFA States:")
    for s in states:
        print(s)

    print("\nDFA Transitions:")
    for k, v in transitions.items():
        print(f"{k} -> {v}")

    print("\nAccepting states:")
    for s in accepting_states:
        print(s)

    return {
        "states": states,
        "alphabet": alphabet,
        "transitions": transitions,
        "start": start_state,
        "accepting": accepting_states
    }
