from node_types import NodeType

PosToSymbolMap = dict()
FollowPosMap = dict()


class Node:
    def __init__(self):
        self.string = ""
        self.node_type = None
        self.left = None
        self.right = None
        self.pos = None
        self.nullable = None
        self.firstpos = []
        self.lastpos = []

    def assign_numbers_to_symbols(self, i):
        if self.string not in "*|.":
            self.pos = i + 1
            PosToSymbolMap[self.pos] = self.string
            return self.pos
        else:
            left_pos = self.left.assign_numbers_to_symbols(i)
            if self.string == "*":
                result = left_pos
            else:
                result = self.right.assign_numbers_to_symbols(left_pos)
            return result

    def compute_null_first_last(self):
        if self.pos is not None:
            self.nullable = False
            self.firstpos.append(self.pos)
            self.lastpos.append(self.pos)
        elif self.node_type == NodeType.Star:
            self.nullable = True
            self.left.compute_null_first_last()
            self.firstpos = self.left.firstpos
            self.lastpos = self.left.lastpos
        else:
            self.left.compute_null_first_last()
            self.right.compute_null_first_last()
            self.firstpos.extend(self.left.firstpos)
            self.lastpos.extend(self.right.lastpos)
            if self.node_type == NodeType.Or:
                self.nullable = self.left.nullable or self.right.nullable
                self.firstpos.extend(self.right.firstpos)
                self.lastpos.extend(self.left.lastpos)
            elif self.node_type == NodeType.Concatenation:
                self.nullable = self.left.nullable and self.right.nullable
                if self.left.nullable:
                    self.firstpos.extend(self.right.firstpos)
                if self.right.nullable:
                    self.lastpos.extend(self.left.lastpos)

    def compute_follow(self, i):
        result = []
        if self.node_type == NodeType.Concatenation and i in self.left.lastpos:
            result = self.right.firstpos
        elif self.node_type == NodeType.Star and i in self.lastpos:
            result = self.left.firstpos

        if self.left is not None:
            result.extend(self.left.compute_follow(i))
        if self.right is not None:
            result.extend(self.right.compute_follow(i))

        return set(result)

    def compute(self):
        self.assign_numbers_to_symbols(0)
        print("Numbers for each symbols in tree:")
        print(PosToSymbolMap)

        self.compute_null_first_last()
        for key in PosToSymbolMap.keys():
            FollowPosMap[key] = self.compute_follow(key)

        print("\nFollowpos:")
        print(FollowPosMap)
