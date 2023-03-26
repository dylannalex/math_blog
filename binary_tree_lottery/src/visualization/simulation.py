import matplotlib.pyplot as plt
from matplotlib.lines import Line2D

from .. import montecarlo
from .. import analytic


def _montecarlo_scatter_plot(
    h: int,
    k: int,
    simulation_iterations: int,
    total_points: int,
    color: str,
    show_analytic_result: bool,
    analytic_result_color: str,
):
    """Scatter plot of monte carlo simulation.

    Parameters
    ----------
    h : int
        Height of the tree.
    k : int
        Number of nodes to choose.
    simulation_iterations : int
        Number of iterations of the monte carlo simulation.
    total_points : int
        Number of points plotted.
    color : str
        Points color.
    """
    iterations_per_point = simulation_iterations // total_points
    tree = montecarlo.tree(h)
    x, y = [], []
    wins = 0
    for iteration in range(1, simulation_iterations + 1):
        if montecarlo.check_winner(montecarlo.lottery(tree, k)):
            wins += 1
        if iteration % iterations_per_point == 0:
            x.append(iteration)
            y.append(wins / iteration)
    plt.scatter(x, y, color=color, s=0.9)

    # Analytic result
    if show_analytic_result:
        plt.plot(
            [0, simulation_iterations],
            [analytic.f(h, k)] * 2,
            color=analytic_result_color,
            alpha=1,
        )

    return wins / simulation_iterations


def simulation(
    h: int,
    k: int,
    simulation_iterations: int,
    total_points: int,
    color: str,
    show_analytic_result: bool,
    analytic_result_color: str,
):
    _montecarlo_scatter_plot(
        h,
        k,
        simulation_iterations,
        total_points,
        color,
        show_analytic_result,
        analytic_result_color,
    )

    # Labels
    plt.ylabel("P(A)")
    plt.xlabel("Iterations")

    # Legends
    legend_lines = [
        Line2D([1], [0], color=color, lw=4, label="Montecarlo Simulation"),
        Line2D([0], [0], color=analytic_result_color, lw=4, label="Analytic Result"),
    ]
    plt.legend(handles=legend_lines)
