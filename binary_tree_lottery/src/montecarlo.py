import random as _random
import math as _math

Tree = list[int]
Node = int
Nodes = list[Node]
Level = int
Simulation = dict[int, float]
IterationList = list[int]


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


def montecarlo_simulation(h: int, k: int, iteration_list: IterationList) -> Simulation:
    """Monte Carlo simulation of the Binary Tree \
    Lottery.

    Parameters
    ----------
    h : int
        Height of the tree.
    k : int
        Number of nodes selected in each round.
    iteration_list : list[int]
        List of positive integers containing the \
        iterations to be stored in the simulation. 

    Returns
    -------
    Simulation
        A dictionary where the keys represent the \
        iteration number and the values represent \
        the estimated probability of winning the \
        binary lottery game. 
    """
    binary_tree = tree(h)
    wins = 0
    simulation: Simulation = {}
    for iteration in range(1, max(iteration_list) + 1):
        if check_winner(lottery(binary_tree, k)):
            wins += 1
        if iteration in iteration_list:
            simulation[iteration] = wins / iteration
    return simulation
