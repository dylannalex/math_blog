import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as patches

from math import degrees
from matplotlib.lines import Line2D
from matplotlib.patches import Arc
from matplotlib.axes import Axes
from celluloid import Camera


A = 1
FONT_SIZE = 14
THETA_COLOR = "#1565C0"
TRIANGLE_COLOR = "#616161"
X_COLOR = "#F94949"


def _init():
    fig, ax = plt.subplots()
    plt.axes(ax)
    plt.rcParams["text.usetex"] = True
    plt.rcParams.update({"font.size": FONT_SIZE})
    plt.xlim((0, A))
    plt.ylim((0, A))
    plt.xticks([0], "")
    plt.yticks([0], "")
    return fig, ax


def _configure_axes(ax: Axes, theta: float):
    ax.set_aspect("equal", adjustable="box")
    angle = f"{round(degrees(theta), 2)}"
    degree = r"^{o}"
    ax.legend(
        [Line2D([0], [0], color=THETA_COLOR, lw=4, label="Line")],
        [f"$\\theta = {angle}{degree}$"],
    )
    # Add 'a' labels
    offset = A * 0.001 + FONT_SIZE * 3e-3
    ax.text(x=A / 2, y=-offset, s="$a$")
    ax.text(x=-offset, y=A / 2, s="$a$")


def _draw_squares(ax: Axes):
    square = patches.Rectangle([0, 0], A, A, fill=False, linewidth=1, alpha=0.5)
    ax.add_patch(square)


def _draw_triangle(ax: Axes, theta: int):
    ang = np.pi / 4 - theta / 2
    offset = A * (1 - np.tan(ang))
    ax.plot([0, A], [0, A - offset], TRIANGLE_COLOR)
    ax.plot([0, A - offset], [0, A], TRIANGLE_COLOR)
    ax.plot([A - offset, A], [A, A - offset], X_COLOR, linewidth=2)
    text_pos = A * 1.005 - offset / 2
    ax.text(x=text_pos, y=text_pos, s="$x$")


def _draw_theta(ax: Axes, theta: float):
    ang = np.pi / 4 - theta / 2
    arc = Arc(
        xy=(0, 0),
        width=A,
        height=A,
        angle=degrees(ang),
        theta1=0,
        theta2=degrees(theta),
        color=THETA_COLOR,
        ls="-",
        linewidth=3,
    )
    ax.add_patch(arc)


def triangle_problem_animation(
    frames: int,
    theta0: float = 0,
    theta1: float = np.pi / 2,
):
    fig, ax = _init()
    camera = Camera(fig)
    for theta in np.linspace(theta0, theta1, frames):
        _configure_axes(ax, theta)
        _draw_squares(ax)
        _draw_triangle(ax, theta)
        _draw_theta(ax, theta)
        camera.snap()
    animation = camera.animate()
    animation.save("animation.gif")


if __name__ == "__main__":
    triangle_problem_animation(frames=60)
