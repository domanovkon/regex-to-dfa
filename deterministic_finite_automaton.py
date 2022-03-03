from node import PosToSymbolMap, FollowPosMap
from utils import generate_syntax_tree


class DeterministicFiniteAutomaton:

    def __init__(self):
        self.start_state = None
        self.states = None
        self.state_transition_table = None
        self.all_symbols = None
        self.finite_states = None

    def build_automaton(self, marked_regexp):
        root = generate_syntax_tree(marked_regexp)
        root.compute()
        self.start_state = frozenset(root.firstpos)
        self.all_symbols = set(PosToSymbolMap.values()) - set("#")
        state_transition_table = dict()
        unmrkd_states = dict()
        unmrkd_states[self.start_state] = False

        while False in unmrkd_states.values():
            R = list(unmrkd_states.keys())[list(unmrkd_states.values()).index(False)]
            unmrkd_states[R] = True
            for a in self.all_symbols:
                S = set()
                for pos in [p for p in R if PosToSymbolMap[p] == a]:
                    S = S.union(FollowPosMap[pos])
                    if bool(S) and frozenset(S) not in unmrkd_states:
                        unmrkd_states[frozenset(S)] = False
                    if R not in state_transition_table:
                        state_transition_table[R] = dict()
                    state_transition_table[R][a] = S

        self.state_transition_table = state_transition_table
        self.states = list(unmrkd_states.keys())
        pos_of_last_symbol = list(PosToSymbolMap.keys())[list(PosToSymbolMap.values()).index("#")]
        self.finite_states = [state for state in self.states if pos_of_last_symbol in state]
        print("\nStates:")
        print(self.states)

        print("\nTransition table")
        for state, num in self.state_transition_table.items():
            print(state)
            for key in num:
                print(key + ':', num[key])

    def finite_automaton_modeling(self, s, state, trans_table):
        symbol_list = list(trans_table[state])
        for ch in s:
            if not symbol_list.__contains__(ch):
                return False
            state = frozenset(trans_table[state][ch])
        return state in self.finite_states
