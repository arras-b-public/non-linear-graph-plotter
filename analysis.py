"""
analysis.py  :  find fixed points and say what kind they are.
--> chapter 5 and 6 of the book

--> close to fixed points, the non-linear system behaves like the linear system
(unless for centers, which require more analysis on the system)

The type of the fixed point depends only on two numbers from A:
        tr   = trace(A)
        det = det(A)
The eigenvalues  lambda = (tr +- sqrt(tr^2 - 4*det)) / 2.

    det < 0                      -> saddle
    det > 0, tr^2 - 4 det > 0 -> node    (stable if tr < 0)
    det > 0, tr^2 - 4 det < 0 -> spiral  (stable if tr < 0)
    det > 0, tr = 0             -> center (linear prediction only!)
    tr^2 - 4 det = 0            -> star / degenerate node
    det = 0                      -> not an isolated fixed point

Borderline cases (center, det = 0) are the ones where small nonlinear terms can change the answer
, so we mark them "borderline" 
"""

from dataclasses import dataclass
import numpy as np
from scipy.optimize import fsolve

EPS = 1e-6   # "close enough to zero" for classification


@dataclass
class FixedPoint:
    x: float
    y: float
    tr: float               # trace of the Jacobian
    det: float              # determinant of the Jacobian
    eigenvalues: np.ndarray
    kind: str               # "saddle", "stable spiral"
    stable: bool            # True only if both eigenvalues have negative real part
    borderline: bool        # True if linearization is not reliable


def classify(jac):
    # look at a 2x2 Jacobian and return (kind, stable, borderline, tr, det, eigenvalues)

    tr = float(np.trace(jac))
    det = float(np.linalg.det(jac))
    eigenvalues = np.linalg.eigvals(jac)

    discriminant = (tr ** 2) - (4 * det)

    stable = bool(np.all(eigenvalues.real < -EPS)) # if all negative, then stable, otw unstable
    borderline = False

    if det < -EPS:
        kind = "saddle"
    elif abs(det) <= EPS:
        kind = "non-isolated (det = 0)"
        borderline = True
    elif abs(tr) <= EPS:
        kind = "center (linear)"
        borderline = True
    elif abs(discriminant) <= EPS:
        kind = ("stable" if tr < 0 else "unstable") + " star/degenerate node"
        borderline = True
    elif discriminant > 0:
        kind = ("stable" if tr < 0 else "unstable") + " node"
    else:
        kind = ("stable" if tr < 0 else "unstable") + " spiral"

    return kind, stable, borderline, tr, det, eigenvalues


def find_fixed_points(system, xlim, ylim, seeds=9):
    # search the window xlim x ylim for fixed points.

    # Method: start a root-finder (fsolve) from a grid of guesses. Every guess
    # that converges to a true solution of f = g = 0 gives a fixed point.
    # Duplicates are removed afterwards.

    def equations(p):
        return [float(system.F(p[0], p[1])), float(system.G(p[0], p[1]))]

    found = []
    for sx in np.linspace(xlim[0], xlim[1], seeds):
        for sy in np.linspace(ylim[0], ylim[1], seeds):
            point, info, ok, _ = fsolve(equations, [sx, sy], full_output=True)
            if ok != 1:
                continue                                    # did not converge
            if max(abs(v) for v in equations(point)) > 1e-8:
                continue                                    # not a true root
            margin = 1e-6
            if not (xlim[0] - margin <= point[0] <= xlim[1] + margin and
                    ylim[0] - margin <= point[1] <= ylim[1] + margin):
                continue                                    # outside our window
            point = np.where(np.abs(point) < 1e-9, 0.0, point)   # clean -1e-17 -> 0
            if any(np.hypot(point[0] - q[0], point[1] - q[1]) < 1e-5 for q in found):
                continue                                    # already have it
            found.append(point)

    # Classify each one using its Jacobian
    result = []
    for px, py in found:
        kind, stable, borderline, tr, det, eig = classify(system.jacobian(px, py))
        result.append(FixedPoint(float(px), float(py), tr, det, eig,
                                 kind, stable, borderline))
    result.sort(key=lambda fp: (round(fp.x, 6), round(fp.y, 6)))
    return result
