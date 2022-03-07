from node import PosToSymbolMap, FollowPosMap
from utils import generate_syntax_tree
import numpy as np


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
            print("State:", set(state))
            for key in num:
                print(key + ':', num[key])

    def finite_automaton_modeling(self, s, state, trans_table, finite_states):
        symbol_list = list(trans_table[state])
        i = 0
        for ch in s:
            if not symbol_list.__contains__(ch):
                return False
            if trans_table.__contains__(state):
                state = frozenset(trans_table[state][ch])
                try:
                    if self.finite_states.__contains__(state) and len(s) - 1 == i:
                        return True
                    else:
                        symbol_list = list(trans_table[state])
                except:
                    return False
            i += 1
        return state in finite_states

    def get_position(self, d):
        if len(d) == 0:
            # self.states.index(list(self.states)[len(self.states) - 1])
            return len(self.states) - 1
        return self.states.index(d)

    def minimization(self):
        n = len(self.states)
        min_matrix = np.zeros((n, n))
        subsets = [list(map(lambda s: self.get_position(set(s)), filter(lambda s: s not in self.finite_states, self.states))),
                   list(map(lambda s: self.get_position(set(s)), self.finite_states))]
        for a in subsets[0]:
            for b in subsets[1]:
                min_matrix[a, b] = 1
                min_matrix[b, a] = 1
        is_finished = False

        while not is_finished:
            copy_min_matrix = np.copy(min_matrix)
            k = 0
            for i in range(n):
                for j in range(n):
                    if min_matrix[i, j] < 1:
                        for e1 in list(list(self.state_transition_table.values())[i]):
                            for e2 in list(list(self.state_transition_table.values())[j]):
                                if e1 == e2 and min_matrix[
                                    self.get_position(list(self.state_transition_table.values())[i].get(e1)),
                                    self.get_position(list(self.state_transition_table.values())[j].get(e2))
                                ] > 0:
                                    copy_min_matrix[i, j], copy_min_matrix[j, i] = 2, 2
                                    k += 1

            newSubset = []
            for i in range(n):
                f = False
                newSubSubset = []
                for j in range(n):
                    if copy_min_matrix[i, j] == 0:
                        newSubSubset += [j]
                    if copy_min_matrix[i, j] == 2:
                        f = True
                newSubset += [newSubSubset]
                f = False
            newSubset = set(tuple(row) for row in newSubset)
            min_matrix = copy_min_matrix
            if k == 0:
                is_finished = True

        edges = []
        for e in newSubset:
            d = self.state_transition_table.get(self.states[e[0]])
            for k, v in d.items():
                if len(v) != 0:
                    edges.append({'Present state': e[0], 'Next state': self.get_position(v), 'Input': k})
        print("\nMinimized transition table")
        for edge in edges:
            print(edge)
