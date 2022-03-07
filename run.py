from deterministic_finite_automaton import DeterministicFiniteAutomaton

if __name__ == "__main__":
    # regexp = "abcbbd"
    regexp = "(a|b)*abb"
    marked_regexp = regexp + "#"
    print("Start regexp is " + regexp + "\n")
    print("Marked regexp is " + marked_regexp + "\n")
    automaton = DeterministicFiniteAutomaton()
    automaton.build_automaton(marked_regexp)
    automaton.minimization()
    check_string = "aaabb"
    print("\nInput string: " + check_string)
    result = automaton.finite_automaton_modeling(check_string,
                                                 automaton.start_state,
                                                 automaton.state_transition_table,
                                                 automaton.finite_states)
    if not result:
        print("not valid")
    else:
        print("valid")
