from node_types import NodeType
from node import Node


def generate_syntax_tree(regexp):
    root = None
    left_set = False
    for token in tokenize(regexp):
        if len(token) > 1:
            node = generate_syntax_tree(token)
        else:
            node = Node()
            node.string = token
            node.node_type = check_node_type(node, token)
        if root is None:
            root = node
        elif left_set:
            root.right = node
            left_set = False
        else:
            node.left = root
            if node.node_type != NodeType.Star:
                left_set = True
            root = node
    return root


def tokenize(regexp):
    tokens = []
    i = 0
    is_multiplier = False
    while i < len(regexp):
        ch = regexp[i]
        if ch == "(":
            token, i = process_brackets(regexp, i)
            if is_multiplier:
                tokens.append(".")
            tokens.append(token)
        else:
            if ch in "*|":
                tokens.append(ch)
            else:
                if is_multiplier:
                    tokens.append(".")
                tokens.append(ch)
        i += 1
        is_multiplier = ch != "|"
    return tokens


def process_brackets(regexp, i):
    brackets_counter = 1
    j = i
    while brackets_counter != 0 and j < len(regexp):
        j += 1
        ch = regexp[j]
        if ch == "(":
            brackets_counter += 1
        elif ch == ")":
            brackets_counter -= 1
    return regexp[i + 1:j], j


def check_node_type(node, token):
    if token == "*":
        node.node_type = NodeType.Star
    elif token == "|":
        node.node_type = NodeType.Or
    elif token == ".":
        node.node_type = NodeType.Concatenation
    else:
        node.node_type = NodeType.Symbol
    return node.node_type
