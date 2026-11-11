"""
app.py : the window the user interacts with

What is drawn on the phase plane:
    1. vector field      little arrows showing (x', y') at a grid of points
    2. nullclines        curves where x' = 0 (red) and y' = 0 (blue)
    3. fixed points      filled dot = stable, open dot = unstable, following the convention seen in class
    4. trajectories      the paths you start by clicking


Controls:
    left click    start a trajectory forward in time
    right click   start a trajectory backward in time (reveals saddle manifolds)
    sliders       one per parameter (other than x and y)
    checkboxes    show/hide vector field, nullclines, clear trajectories
"""

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider, CheckButtons, Button

from system import System
from integrate import trajectory
from analysis import find_fixed_points


def fmt_eig(e):
    """Show an eigenvalue as 2.41 for real ones, or 0.75+0.66i for complex ones."""
    if abs(e.imag) < 1e-9:
        return f"{e.real:.3g}"
    return f"{e.real:.2g}{e.imag:+.2g}i"


class PhasePlaneApp:
    def __init__(self, preset):
        self.preset = preset
        self.xlim = preset["xlim"]
        self.ylim = preset["ylim"]

        # Build the math object, using each parameter's start value
        start_values = {name: spec[0] for name, spec in preset["params"].items()}
        self.system = System(preset["f"], preset["g"], start_values)

        # Trajectories the user has started: list of (x0, y0, backward?)
        self.starts = [(px, py, False) for px, py in preset["starts"]]

        self.show_field = True
        self.show_nullclines = True

        self.make_window()
        self.redraw()

    # ------------------------------------------------------------ window
    def make_window(self):
        n_params = len(self.system.param_names)
        bottom = 0.08 + 0.05 * n_params           # leave room for sliders

        self.fig = plt.figure(figsize=(10, 7))
        self.ax = self.fig.add_axes([0.07, bottom + 0.05, 0.68, 0.88 - bottom])
        self.info = self.fig.text(0.77, 0.70, "", va="top", fontsize=8,
                                  family="monospace")

        # one slider per parameter
        self.sliders = []
        for i, name in enumerate(self.system.param_names):
            start, low, high = self.preset["params"].get(
                name, (1.0, -5.0, 5.0))
            slider_ax = self.fig.add_axes([0.12, 0.04 + 0.05 * i, 0.55, 0.03])
            slider = Slider(slider_ax, name, low, high, valinit=start)
            slider.on_changed(self.on_slider)
            self.sliders.append(slider)

        # checkboxes
        check_ax = self.fig.add_axes([0.77, 0.82, 0.21, 0.10])
        self.checks = CheckButtons(check_ax, ["vector field", "nullclines"],
                                   [True, True])
        self.checks.on_clicked(self.on_check)

        # clear button
        button_ax = self.fig.add_axes([0.77, 0.75, 0.21, 0.05])
        self.clear_button = Button(button_ax, "clear trajectories")
        self.clear_button.on_clicked(self.on_clear)

        self.fig.canvas.mpl_connect("button_press_event", self.on_click)

    # ------------------------------------------------------------ events
    def on_slider(self, _value):
        for slider in self.sliders:
            self.system.set_param(slider.label.get_text(), slider.val)
        self.redraw()

    def on_check(self, label):
        if label == "vector field":
            self.show_field = not self.show_field
        else:
            self.show_nullclines = not self.show_nullclines
        self.redraw()

    def on_clear(self, _event):
        self.starts = []
        self.redraw()

    def on_click(self, event):
        if event.inaxes != self.ax:
            return
        backward = (event.button == 3)            # 3 = right mouse button
        self.starts.append((event.xdata, event.ydata, backward))
        self.redraw()

    # ------------------------------------------------------------ drawing
    def redraw(self):
        ax = self.ax
        ax.clear()
        s = self.system

        # A grid of points covering the window
        gx = np.linspace(self.xlim[0], self.xlim[1], 400)
        gy = np.linspace(self.ylim[0], self.ylim[1], 400)
        GX, GY = np.meshgrid(gx, gy)

        # 1. Vector field (arrows all drawn the same length: only direction matters)
        if self.show_field:
            ax_x = np.linspace(self.xlim[0], self.xlim[1], 22)
            ax_y = np.linspace(self.ylim[0], self.ylim[1], 18)
            QX, QY = np.meshgrid(ax_x, ax_y)
            U, V = s.F(QX, QY), s.G(QX, QY)
            # normalize using the plot's own scale so arrows look right
            sx = (self.xlim[1] - self.xlim[0])
            sy = (self.ylim[1] - self.ylim[0])
            length = np.hypot(U / sx, V / sy)
            length[length == 0] = 1.0
            ax.quiver(QX, QY, U / sx / length, V / sy / length,
                      color="0.7", angles="xy", scale_units="xy",
                      scale=22 / sx * 1.6, width=0.002)

        # 2. Nullclines: contour lines where x' = 0 and y' = 0
        if self.show_nullclines:
            ax.contour(GX, GY, s.F(GX, GY), levels=[0], colors="tab:red",
                       linewidths=1.2, linestyles="--")
            ax.contour(GX, GY, s.G(GX, GY), levels=[0], colors="tab:blue",
                       linewidths=1.2, linestyles="--")

        # 4. Trajectories (drawn before the dots so the dots sit on top)
        for x0, y0, backward in self.starts:
            xs, ys = trajectory(s, x0, y0, t_max=40.0, backward=backward)
            ax.plot(xs, ys, color="tab:green" if backward else "black", lw=1.3)
            ax.plot(x0, y0, ".", color="tab:green" if backward else "black",
                    markersize=5)

        # 3. Fixed points
        points = find_fixed_points(s, self.xlim, self.ylim)
        lines = ["Fixed points", ""]
        for p in points:
            ax.plot(p.x, p.y, "o", markersize=9, markeredgecolor="black",
                    markeredgewidth=1.5,
                    markerfacecolor="black" if p.stable else "white",
                    zorder=5)
            note = "  (borderline!)" if p.borderline else ""
            lines.append(f"({p.x:.3g}, {p.y:.3g})")
            lines.append(f"  {p.kind}{note}")
            lines.append(f"  tau={p.tr:.3g}  delta={p.det:.3g}")
            lines.append("  lambda: " + ", ".join(fmt_eig(e) for e in p.eigenvalues))
            lines.append("")
        self.info.set_text("\n".join(lines))

        ax.set_xlim(self.xlim)
        ax.set_ylim(self.ylim)
        ax.set_xlabel("x")
        ax.set_ylabel("y")
        ax.set_title(f"x' = {s.f_text}     y' = {s.g_text}", fontsize=10)
        ax.grid(alpha=0.2)
        self.fig.canvas.draw_idle()

    def show(self):
        plt.show()
