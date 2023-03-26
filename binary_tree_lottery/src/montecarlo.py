import random as _random
import math as _math

Tree = list[int]
Node = int
Nodes = list[Node]
Level = int


def tree(height: int) -> Tree:
    return [i for i in range(1, 2 ** (height + 1))]


def lottery(tree: Tree, k: int) -> Nodes:
    tree_ = tree[::]
    selected_nodes = []
    for _ in range(k):
        node = _random.choice(tree_)
        tree_.remove(node)
        selected_nodes.append(node)
    return selected_nodes


def node_level(node: Node) -> Level:
    return _math.floor(_math.log2(node))


def check_winner(nodes: Nodes) -> bool:
    level = node_level(nodes[0])
    for node in nodes[1:]:
        if node_level(node) != level:
            return False
    return True


def simulation(height: int, k: int, iterations: int = 1_000_000) -> float:
    binary_tree = tree(height)
    wins = 0
    for _ in range(iterations):
        if check_winner(lottery(binary_tree, k)):
            wins += 1
    return wins / iterations
