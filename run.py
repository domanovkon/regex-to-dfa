from deterministic_finite_automaton import DeterministicFiniteAutomaton

if __name__ == "__main__":
    regexp = "abaacabd"
    # regexp = "(a|b)*abb"
    marked_regexp = regexp + "#"
    print("Start regexp is " + regexp + "\n")
    print("Marked regexp is " + marked_regexp + "\n")
    automaton = DeterministicFiniteAutomaton()
    automaton.build_automaton(marked_regexp)

    check_string = "aabb"
    print("\nInput string: " + check_string)
    result = automaton.finite_automaton_modeling(check_string,
                                                 automaton.start_state,
                                                 automaton.state_transition_table,
                                                 automaton.finite_states)
    if not result:
        print("False")
    else:
        print("True")

    automaton.minimization()
