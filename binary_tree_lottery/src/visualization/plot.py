import matplotlib.pyplot as plt
from matplotlib.lines import Line2D

from ..montecarlo import Simulation


_SCATTER_PLOT_COLOR = "royalblue"
_ANALYTIC_RESULT_COLOR = "orange"


def _config_montecarlo_scatter_plot():
    # Labels
    plt.ylabel("P(A)")
    plt.xlabel("Iterations")

    # Legends
    legend_lines = [
        Line2D(
            [1], [0], color=_SCATTER_PLOT_COLOR, lw=4, label="Montecarlo Simulation"
        ),
        Line2D([0], [0], color=_ANALYTIC_RESULT_COLOR, lw=4, label="Analytic Result"),
    ]
    plt.legend(handles=legend_lines)


def montecarlo_scatter_plot(
    simulation: Simulation,
    smallest_iteration: int,
    analytic_result: float,
):
    """Scatter plot of monte carlo simulation.

    Parameters
    ----------
    simulation : Simulation
        A dictionary where the keys represent the \
        iteration number and the values represent \
        the estimated probability of winning the \
        binary lottery game.
    smallest_iteration : int
        Smallest iteration plotted. This prevents \
        outliers to be plotted.
    analytic_result : float or None
        The analytic result to compare with the \
        Monte Carlo simulation. If None, the \
        analytic result will not be plotted.
    """
    # Setup plot
    _config_montecarlo_scatter_plot()

    # Plot simulation
    x = [i for i in simulation.keys() if i >= smallest_iteration]
    y = [simulation[k] for k in x]
    plt.scatter(x, y, color=_SCATTER_PLOT_COLOR, s=0.9)

    # Analytic result line
    max_x = max(x)
    if analytic_result:
        plt.plot(
            [0, max_x],
            [analytic_result] * 2,
            color=_ANALYTIC_RESULT_COLOR,
            alpha=1,
        )


def montecarlo_table(simulation: Simulation, iteration_list: list[int]):
    """Plots a table for visualizing the estimated probability \
        of winning the binary lottery game at the given iterations \
        of the Monte Carlo simulation.

    Parameters
    ----------
    simulation : Simulation
        A dictionary where the keys represent the \
        iteration number and the values represent \
        the estimated probability of winning the \
        binary lottery game.
    iteration_list : list[int]
        The list of iterations to show on the table. \
        The iterations in `iteration_list` must also \
        be in `simulation`.
    """
    _, _ = plt.subplots(figsize=(7, 1))
    data = [(f"{i:,d}", simulation[i]) for i in iteration_list]
    plt.table(
        cellText=data,
        colLabels=["Iterations", "Estimated Probability"],
        cellLoc="center",
        loc="center",
        colColours=["#C0B6FF", "#C0B6FF"],
    )

    plt.axis("off")
    plt.axis("tight")
