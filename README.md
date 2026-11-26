# Non-Linear Systems Phase Plane Plotter 

An interactive tool for exploring two-dimensional systems of differential equations

```
x' = f(x, y)
y' = g(x, y)
```

It draws the phase portrait of the system, finds its fixed points, classifies them, and lets you click to start trajectories and use sliders to change parameters. I built it while studying nonlinear dynamics, and the built-in examples follow the textbook *Nonlinear Dynamics and Chaos* by Steven Strogatz.

This project is a work in progress.

![Damped pendulum phase portrait](docs/damped_pendulum.png)

The screenshot shows the damped pendulum preset (`x' = y`, `y' = -sin(x) - b*y`) with `b = 0.31`. The filled dots are stable spirals, the open dots are saddles, and the side panel lists the trace, determinant, and eigenvalues at each fixed point.

## Features

- **Vector field**: arrows showing the direction of the flow (all the same length, since only direction matters)
- **Nullclines**: red dashed curves where x' = 0 and blue dashed curves where y' = 0
- **Fixed points**: found numerically and classified from the linearization. Filled dots are stable and open dots are unstable
- **Trajectories**: left click to start one forward in time, right click to start one backward in time (useful for tracing the stable manifold of a saddle)
- **Parameter sliders**: any name in the equations other than `x` and `y` becomes a slider, and everything redraws as you move it
- **Presets**: several example systems from the book
- **Custom systems**: type your own equations on the command line

## Requirements

- Python 3.8+
- NumPy, SciPy, Matplotlib

## Usage

Run from the folder containing `main.py`:

```
python main.py --list                              # show all presets
python main.py damped_pendulum                     # open a preset
python main.py --custom "y" "-sin(x) - b*y"        # your own system
python main.py --help                              # show help
```

### Writing equations

- Use `x` and `y` for the variables, and write each equation in quotes.
- Any other name (`a`, `b`, `mu`, ...) becomes a parameter with a slider from -5 to 5, starting at 1.
- Multiplication must be explicit: write `x*y`, not `xy`. A name made only of x's and y's is rejected with a hint.
- Powers can be written `x**2` or `x^2`.
- Available functions: `sin cos tan exp log sqrt sinh cosh tanh abs`. Available constants: `pi e`.
- Custom systems use a fixed window of -5 to 5 on both axes.

### Controls

| Action | Effect |
|---|---|
| Left click | Start a trajectory forward in time |
| Right click | Start a trajectory backward in time |
| Sliders | Change a parameter |
| Checkboxes | Show or hide the vector field and the nullclines |
| Clear button | Remove all trajectories |

## Presets

| Name | Description |
|---|---|
| `rabbits_vs_sheep` | Competition model with a saddle whose stable manifold is the basin boundary |
| `double_well` | Conservative system with a saddle at the origin and centers at x = +-1 |
| `damped_pendulum` | Slide `b` toward 0 and the spirals turn into centers |
| `van_der_pol` | Every trajectory winds onto a single limit cycle |
| `hopf_subcritical` | Subcritical Hopf bifurcation, with an unstable cycle near mu = 0 |
| `chemical_oscillator` | Hopf bifurcation in a chemical reaction model, with parameters `a` and `b` |
| `linear_system` | General linear system with four sliders |

Presets are defined in `presets.py`, and adding one simply requires adding an entry with the equations, parameter ranges, window, and starting points.

## How it works

| File | Responsibility |
|---|---|
| `main.py` | Command line handling and help text |
| `app.py` | The matplotlib window, widgets, and drawing |
| `system.py` | Parses the equations and evaluates f, g, and the Jacobian |
| `analysis.py` | Finds and classifies fixed points |
| `integrate.py` | Integrates trajectories |
| `presets.py` | The example systems |


