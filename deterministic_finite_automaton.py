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
            print(state)
            for key in num:
                print(key + ':', num[key])

    def finite_automaton_modeling(self, s, state, trans_table, finite_states):
        symbol_list = list(trans_table[state])
        i = 0
        for ch in s:
            if not symbol_list.__contains__(ch):
                return False

            if (trans_table.__contains__(state)):
                state = frozenset(trans_table[state][ch])

                try:
                    if (self.finite_states.__contains__(state) and len(s)-1==i):
                        return True
                    else:
                        symbol_list = list(trans_table[state])
                except:
                    return False

            i += 1


        return state in finite_states

    def getPos(self, d):
        return self.states.index(d)

    def minimization(self):
        n = len(self.states)
        symb = list(self.all_symbols)

        min_matrix = np.zeros((n, n))

        subsets = [list(map(lambda s: self.getPos(set(s)), filter(lambda s: s not in self.finite_states,self.states))), list(map(lambda s: self.getPos(set(s)), self.finite_states))]
        for a in subsets[0]:
            for b in subsets[1]:
                min_matrix[a, b] = 1
                min_matrix[b, a] = 1

        isFinished = False

        while not isFinished:
            copyMin_matrix = np.copy(min_matrix)
            k = 0

            for i in range(n):
                for j in range(n):
                    if min_matrix[i, j] < 1:

                        for e1 in list(list(self.state_transition_table.values())[i]):
                            for e2 in list(list(self.state_transition_table.values())[j]):
                                if e1==e2 and min_matrix[
                                        self.getPos(list(self.state_transition_table.values())[i].get(e1)),
                                        self.getPos(list(self.state_transition_table.values())[j].get(e2))
                                    ] > 0:
                                    copyMin_matrix[i,j], copyMin_matrix[j,i] = 2, 2
                                    k+=1

            newSubset = []
            for i in range(n):
                f = False
                newSubSubset = []
                for j in range(n):
                    if(copyMin_matrix[i,j]==0):
                        newSubSubset += [j]
                    if(copyMin_matrix[i,j]==2):
                        f = True
                newSubset += [newSubSubset]
                f = False

            newSubset = set(tuple(row) for row in newSubset)


            min_matrix = copyMin_matrix
            if k==0:
                isFinished = True

        pass
        #for a in

        edges = []
        for e in newSubset:
            d = self.state_transition_table.get(self.states[e[0]])
            for k, v in d.items():
                edges.append({'srcNode': e[0], 'dstNode': self.getPos(v), 'data': k})
        print(edges)


    #     list_states = list()
    #     for i in range(len(self.states)):
    #         list_states.append((self.states[i]))
    #
    #     dop_state = frozenset()
    #     tr_tbl = self.state_transition_table
    #     tr_tbl[len(self.states)] = dop_state()
    #     print(self.state_transition_table[list_states[0]]['a'])

