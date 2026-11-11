"""
main.py : entry point of the program

How to use:

    python main.py                                  opens the help/man page                      
    python main.py preset                           opens the preset "preset"
    python main.py --list                           shows all preset names
    python main.py --custom "f" "g"                 custom system of equation
    python main.py --help                           opens the help/man page 
    python main.py -h                               opens the help/man page
"""

import sys
from presets import PRESETS
from app import PhasePlaneApp



HELP = """
Phase Plane Plotter: draws the phase portrait of  x' = f(x,y),  y' = g(x,y)
 
USAGE
    python main.py <preset>                       open the preset called <preset>
    python main.py --list                         show all preset names
    python main.py --custom "f" "g"               your own system of equations
    python main.py --help                         show this help
 
EQUATIONS (for --custom)
    Write f and g in quotes, using x and y.
        python main.py --custom "y" "-sin(x) - b*y"
    Any other name (a, b, mu, ...) becomes a slider (range -5 to 5)
    Powers: x**2 or x^2
    Functions: sin cos tan exp log sqrt sinh cosh tanh abs   Constants: pi e

PHASE PROTRAIT
    The custom window is fixed at -5..5 on both axes
 
CONTROLS (in the window)
    left click        start a trajectory (forward in time)
    right click       start a trajectory (backward in time)
                      (traces the stable manifold of a saddle)
    sliders           change a parameter, everything redraws
    checkboxes        show/hide the vector field and the nullclines
    clear button      remove all trajectories
 
WHAT YOU SEE
    grey arrows       the vector field (direction of the flow)
    red dashed        nullcline (x' = 0) 
    blue dashed       nullcline (y' = 0)
    filled dot        stable fixed point    
    open dot          unstable fixed point
    side panel        type, trace, determinant and eigenvalues of each fixed point
"""


def main():
    args = sys.argv[1:]

    if not args or "--help" in args or "-h" in args:
        print(HELP)
        return

    if "--list" in args:
        print_presets()
        return

    # if custom system
    if "--custom" in args:
        i = args.index("--custom")

        if len(args) < i + 3:
            print('Error: --custom needs two equations, e.g. --custom "x^2" "-xy"\n')
            print(HELP)
            return

        preset = {
        "f": args[i + 1], 
        "g": args[i + 2], 
        "params": {}, # empty rn, but will parse f and g in system.py to find the parameters
        "xlim": (-5, 5), # limit x axis to [-5, 5]
        "ylim": (-5, 5), # limit x axis to [-5, 5]
        "starts": [], # start points
        "note": "custom"
        }


    else:
        name = args[0]
        if name not in PRESETS:
            print(f"Error: unknown preset '{name}'. Available presets:\n")
            print_presets()
            return

        preset = PRESETS[name] # load correct preset


    try:
        app = PhasePlaneApp(preset) # plot preset
    except ValueError as problem: # in case of a mistyped equation
        print("Error:", problem)
        return

    app.show() # show it as a window


def print_presets():
    for name, preset in PRESETS.items():
        print(f"{name:22s} {preset['note']}") # print the name of preset and any notes associated with it
        # limit name to always be 22 chars


if __name__ == "__main__":
    main()
