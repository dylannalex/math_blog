import matplotlib.pyplot as plt
import math
import cmath

from matplotlib.patches import Arc
from matplotlib.axes import Axes
from . import complex_circle


def _configure_plot():
    limit = 1 + 0.1
    plt.xlim((-limit, limit))
    plt.ylim((-limit, limit))
    plt.ylabel("Imaginary")
    plt.xlabel("Real")


def _plot_circle(axes: Axes) -> None:
    axes.add_artist(plt.Circle((0, 0), 1, fill=False))


def _plot_complex_number(
    z: complex, color: str, text: str = None, line_style="-"
) -> None:
    if text:
        plt.text(z.real, z.imag, text)
    plt.plot([0, z.real], [0, z.imag], color, ls=line_style)
    plt.plot([z.real], [z.imag], color, marker="x", markersize=10)


def _plot_angle(z: complex, theta0: float, axes: Axes) -> None:
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
    _plot_complex_number(z_0, "grey", line_style="--")

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


def plot_complex_circle_problem(
    n: int, theta0: float, show_angles: bool = False, show_result: bool = True
) -> None:
    figure, axes = plt.subplots()
    axes.set_aspect("equal", adjustable="box")

    z_list = complex_circle.get_z_list(n, theta0)
    _plot_circle(axes)

    # plot z_list and angles
    for i, z in enumerate(z_list):
        _plot_complex_number(z, "red", text=f"z{i+1}")
        if show_angles and theta0 != 0:
            _plot_angle(z, theta0, axes)

    # plot complex circle result
    if show_result:
        result = complex_circle.complex_circle_reduced_formula(n, theta0)
        _plot_complex_number(result, "blue")

    _configure_plot()
