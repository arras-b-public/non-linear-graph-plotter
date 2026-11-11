"""
presets.py : example systems taken from the book

Each preset is a dictionary:
    f, g      the equations as text
    params    {name: (start value, slider min, slider max)}
    xlim,ylim the window to show
    starts    a few trajectory start points drawn when the app opens
    note      where it is in the book / what to look for / general comments
"""

PRESETS = {
    "rabbits_vs_sheep": {
        "f": "x*(3 - x - 2*y)",
        "g": "y*(2 - x - y)",
        "params": {},
        "xlim": (-0.2, 4.0), "ylim": (-0.2, 3.0),
        "starts": [(0.1, 0.1), (1.0, 2.5), (2.5, 0.5), (0.5, 0.2), (3.5, 2.0)],
        "note": "Section 6.4. Saddle at (1,1); its stable manifold is the basin boundary.",
    },
    "double_well": {
        "f": "y",
        "g": "x - x**3",
        "params": {},
        "xlim": (-2.5, 2.5), "ylim": (-2.0, 2.0),
        "starts": [(0.5, 0.0), (-1.5, 0.0), (0.0, 0.8), (0.0, 1.0)],
        "note": "Example 6.5.2. Saddle at 0, centers at +-1, conservative system.",
    },
    "damped_pendulum": {
        "f": "y",
        "g": "-sin(x) - b*y",
        "params": {"b": (0.3, 0.0, 2.0)},
        "xlim": (-6.5, 6.5), "ylim": (-3.0, 3.0),
        "starts": [(1.0, 0.0), (-2.0, 1.0), (0.0, 2.8), (3.0, -1.0)],
        "note": "Section 6.7. Slide b to 0: spirals turn into centers.",
    },
    "van_der_pol": {
        "f": "y",
        "g": "-x - mu*(x**2 - 1)*y",
        "params": {"mu": (1.5, 0.0, 6.0)},
        "xlim": (-3.0, 3.0), "ylim": (-6.0, 6.0),
        "starts": [(0.2, 0.0), (2.5, 3.0), (-2.5, -3.0)],
        "note": "Section 7.1/7.5. Every start winds onto one limit cycle.",
    },
    "hopf_subcritical": {
        "f": "mu*x + y + x*y**2",
        "g": "-x + mu*y + y**3",
        "params": {"mu": (-0.2, -0.5, 0.5)},
        "xlim": (-2.0, 2.0), "ylim": (-2.0, 2.0),
        "starts": [(0.3, 0.0), (0.8, 0.0), (1.2, 0.0)],
        "note": "Example 8.2.1. Subcritical Hopf at mu = 0: look for the unstable cycle.",
    },
    "chemical_oscillator": {
        "f": "a - x - 4*x*y/(1 + x**2)",
        "g": "b*x*(1 - y/(1 + x**2))",
        "params": {"a": (10.0, 5.0, 15.0), "b": (3.0, 0.5, 8.0)},
        "xlim": (0.0, 5.0), "ylim": (0.0, 12.0),
        "starts": [(1.0, 1.0), (4.0, 10.0)],
        "note": "Section 8.3. Hopf at b = 3a/5 - 25/a: b below it gives a limit cycle.",
    },
    "linear_system": {
        "f": "a*x + b*y",
        "g": "c*x + d*y",
        "params": {"a": (1.0, -4.0, 4.0), "b": (1.0, -4.0, 4.0),
                   "c": (4.0, -4.0, 4.0), "d": (-2.0, -4.0, 4.0)},
        "xlim": (-3.0, 3.0), "ylim": (-3.0, 3.0),
        "starts": [(1.0, 1.0), (-1.0, 0.5), (0.5, -1.0), (-0.5, -1.0)],
        "note": "Chapter 5. Move the sliders and watch Figure 5.2.8 (tau, delta) come alive.",
    },
}
