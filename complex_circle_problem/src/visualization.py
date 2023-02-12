import matplotlib.pyplot as plt
import math
import cmath

from matplotlib.patches import Arc
from matplotlib.axes import Axes
from . import complex_circle


_SUBPLOTS_PER_COL = 2
_FIGURE_SIZE = (10, 10)


def _configure_plot(axes: Axes, n: int, theta0: float):
    limit = 1 + 0.1
    axes.set_aspect("equal", adjustable="box")
    plt.axes(axes)
    plt.title(f"$n = {n}$  $\\theta_0 = {round(theta0, 4)}$")
    plt.xlim((-limit, limit))
    plt.ylim((-limit, limit))
    plt.ylabel("Imaginary")
    plt.xlabel("Real")


def _plot_circle(axes: Axes) -> None:
    axes.add_artist(plt.Circle((0, 0), 1, fill=False))


def _plot_complex_number(
    axes: Axes, z: complex, color: str, text: str = None, line_style="-"
) -> None:
    if text:
        axes.text(z.real, z.imag, text)
    axes.plot([0, z.real], [0, z.imag], color, ls=line_style)
    axes.plot([z.real], [z.imag], color, marker="x", markersize=10)


def _plot_angle(axes: Axes, z: complex, theta0: float) -> None:
    z_angle = cmath.polar(z)[1]
    angle = math.degrees(-theta0)
    while angle < 0:
        angle += 360

    theta2 = math.degrees(z_angle)
    while theta2 < 0:
        theta2 += 360

    theta1 = theta2 + angle

    # plot z with theta0 = 0
    z_0 = cmath.rect(1, z_angle - theta0)
    _plot_complex_number(axes, z_0, "grey", line_style="--")

    # plot theta0 arc
    arc = Arc(
        xy=(0, 0),
        width=1,
        height=1,
        angle=0,
        theta1=theta1,
        theta2=theta2,
        color="grey",
        ls="--",
    )
    axes.add_patch(arc)


def _plot_complex_circle(
    axes: Axes,
    complex_problem: complex_circle.ComplexCircle,
    show_angles: bool = False,
    show_result: bool = True,
) -> None:
    n = complex_problem.n
    theta0 = complex_problem.theta0
    z_list = complex_problem.get_z_list()
    result = complex_problem.complex_circle_reduced_formula()

    # plot unitary circle
    _plot_circle(axes)

    # plot z_list and angles
    for i, z in enumerate(z_list):
        _plot_complex_number(axes, z, "red", text=f"z{i+1}")
        if show_angles and theta0 != 0:
            _plot_angle(axes, z, theta0)

    # plot complex circle result
    if show_result:
        _plot_complex_number(axes, result, "blue")

    _configure_plot(axes, n, theta0)


def visualize(
    *complex_problem: complex_circle.ComplexCircle,
    show_angles: bool = False,
    show_result: bool = True,
) -> None:
    # figure, axes = plt.subplots(len(n_list))
    cols = _SUBPLOTS_PER_COL
    rows = math.ceil(len(complex_problem) / cols)
    figure, axes = plt.subplots(rows, cols, figsize=_FIGURE_SIZE)
    figure.tight_layout(pad=5.0)

    index = 0
    for row in range(rows):
        for col in range(cols):
            if rows > 1:
                axes_ = axes[row][col]
            else:
                axes_ = axes[index]

            #  last empty subplot
            if index > len(complex_problem) - 1:
                figure.delaxes(axes_)
                figure.tight_layout()
                return

            _plot_complex_circle(
                axes_, complex_problem[index], show_angles, show_result
            )
            index += 1
