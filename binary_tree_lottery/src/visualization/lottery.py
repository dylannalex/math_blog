import matplotlib.pyplot as plt
from matplotlib.axes import Axes
from celluloid import Camera
from collections import namedtuple

from .. import montecarlo


_EDGE_COLOR = "#767676"
_NODE_COLOR = "#5B81FF"
_NODE_SIZE = 0.2
_SELECTED_NODE_SIZE = 0.2
_CORRECT_NODE_COLOR = "#00C60D"
_INCORRECT_NODE_COLOR = "#E63D00"


Position = tuple[int, int]
Edge = tuple[Position, Position]
Level = namedtuple("Level", ["y", "x_list"])


def _find_pairs(list_: list[int]) -> list[tuple[int, int]]:
    pairs = []
    for i in range(0, len(list_), 2):
        pairs.append((list_[i], list_[i + 1]))
    return pairs


def tree(h: int) -> tuple[list[Level], list[Edge]]:
    levels: list[Level] = []
    edges: list[Edge] = []
    x_limit = 2 ** (h - 1)

    last_nodes = [x for x in range(-x_limit, x_limit + 1)]
    last_nodes.remove(0)
    levels.append(Level(h, last_nodes))
    for y in range(h - 1, -1, -1):
        pairs = _find_pairs(last_nodes)
        x_list = []
        for pair in pairs:
            x_value = (pair[0] + pair[1]) / 2
            x_list.append(x_value)
            edges.append(((x_value, y), (pair[0], y + 1)))
            edges.append(((x_value, y), (pair[1], y + 1)))
        levels.append(Level(y, x_list))
        last_nodes = x_list
    return levels, edges


def _configure_plot(ax: Axes, h: int):
    offset = 0.5
    x_limit = 2 ** (h - 1) + offset
    # General conf
    plt.axes(ax)
    plt.xlim((-x_limit, x_limit))
    plt.ylim((-h - offset, offset))
    plt.ylabel("Level")
    plt.xlabel("Node")

    # TODO: add legends without exponentially slow down the code.


def _plot_node(ax: Axes, x: int, h: int, color: str, fill: bool, size: float = 0.1):
    ax.add_patch(plt.Circle((x, h * -1), size, color=color, fill=fill))


def _plot_edge(ax: Axes, edge: Edge):
    x_list = (edge[0][0], edge[1][0])
    y_list = (-edge[0][1], -edge[1][1])
    ax.plot(x_list, y_list, color=_EDGE_COLOR, alpha=0.8)


def _find_node_pos(levels: list[Level], node_number: int) -> Position:
    node_level = montecarlo.node_level(node_number)
    for level in levels:
        if level.y == node_level:
            x_index = node_number - 2**node_level
            return (level.x_list[x_index], level.y)


def _plot_tree(
    ax: Axes,
    levels: list[Level],
    edges: list[Edge],
    nodes_to_ignore: list[Position] = [],
):
    # Plot edges
    for edge in edges:
        _plot_edge(ax, edge)

    # Plot nodes
    for level in levels:
        for x in level.x_list:
            if (x, level.y) in nodes_to_ignore:
                continue
            _plot_node(ax, x, level.y, _NODE_COLOR, True, _NODE_SIZE)


def _lottery_animation(
    ax: Axes,
    camera: Camera,
    levels: list[Level],
    edges: list[Edge],
    color: str,
    lottery_nodes: list[int],
    lottery_animation_frames: int,
):
    chosen_nodes = [
        _find_node_pos(levels, node_number) for node_number in lottery_nodes
    ]
    for _ in range(lottery_animation_frames):
        for node in chosen_nodes:
            _plot_tree(ax, levels, edges, chosen_nodes)
            _plot_node(
                ax,
                x=node[0],
                h=node[1],
                color=color,
                fill=True,
                size=_SELECTED_NODE_SIZE,
            )
        camera.snap()


def create_animation(
    h: int,
    k: int,
    simulation_iterations: int,
    total_lottery_animations: int,
    lottery_animation_frames: int,
    file_path: str,
):
    """Creates a Lottery Animation for a tree of height \
    `h` and choosing `k` nodes.

    Parameters
    ----------
    h : int
        Height of the tree.
    k : int
        Number of nodes to choose.
    simulation_iterations : int
        Number of iterations of the monte carlo simulation. 
    total_lottery_animations : int
        Number of lotteries animated.
    lottery_animation_frames : int
        Number of frames of each lottery animated.
    animation_file_name : str
        File name of the animation.
    """
    fig, ax = plt.subplots()
    _configure_plot(ax, h)
    camera = Camera(fig)

    levels, edges = tree(h)
    frames_per_lottery = round(simulation_iterations / total_lottery_animations)

    # Monte Carlo Simulation
    binary_tree = montecarlo.tree(h)
    wins = 0
    for i in range(simulation_iterations):
        lottery_nodes = montecarlo.lottery(binary_tree, k)
        has_win = montecarlo.check_winner(lottery_nodes)
        if has_win:
            wins += 1

        # Update lottery visualization
        if i % frames_per_lottery != 0:
            continue

        color = _CORRECT_NODE_COLOR if has_win else _INCORRECT_NODE_COLOR
        _lottery_animation(
            ax,
            camera,
            levels,
            edges,
            color,
            lottery_nodes,
            lottery_animation_frames,
        )

    animation = camera.animate()
    animation.save(file_path)
