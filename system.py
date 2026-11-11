"""
system.py : describes ONE two-dimensional system:

        x' = f(x, y)
        y' = g(x, y)

You give it the equations as text, e.g.  "x*(3 - x - 2*y)".
Any name other than x and y (like r, mu, a, b) is treated as a PARAMETER
(a number you can change with a slider)
THUS WRITING MULTIPLICATION AS "xy" and not "x*y"  WILL RESULT IN "xy" BE TRATED AS A PARAMETER


the text is evaluated directly with Python's eval, using a small whitelist of math functions
the Jacobian is computed numerically with finite differences
"""

import numpy as np

# Functions and constants allowed inside equations
MATH = {
    "sin": np.sin, "cos": np.cos, "tan": np.tan,
    "exp": np.exp, "log": np.log, "sqrt": np.sqrt,
    "sinh": np.sinh, "cosh": np.cosh, "tanh": np.tanh,
    "abs": np.abs, "pi": np.pi, "e": np.e,
}


def find_names(text):
    # find all names used in an equaltion
    # example:
    # "mu*x - sin(y)" --> {"mu", "x", "sin", "y"}

    # can use python compile method to compile line into byte code into a placeholder named "<equation>"
    # the co_names attribute is a tuple of that compiled code contanint every single identifier name
    # that python encountered while reading the epression
    # in other other words, python will exactat each toekn for us

    return set(compile(text, "<equation>", "eval").co_names)


class System:
    def __init__(self, f_text, g_text, params_user=None):
        self.f_text = f_text
        self.g_text = g_text

        # '^' is accepted as a power sign, like "x^2"
        self.f_code = self._compile(f_text)
        self.g_code = self._compile(g_text)

        # parameters = every name that is not x, y or a math function/constant
        names = set(self.f_code.co_names) # extract parameters from f
        names |= set(self.g_code.co_names) # extract parameters from g
        names -= {"x", "y"} # remove x and y from sets
        names -= set(MATH) # remove all other symbols that are functions or constants

        # so names only contains paramters
        self.param_names = sorted(names)

        # a "name" made only of x's and y's (like xy) is almost surely a
        # forgotten multiplication, not a parameter. Say so throw error
        for name in self.param_names:
            if set(name) <= {"x", "y"}: # if an element is a subset of "x" "y"
                raise ValueError(f"'{name}' is read as one name. "
                                 f"Did you mean '{'*'.join(name)}'? Use * for multiplication.")


        # give a default value of 1 for all parameters. So we have a dict: {name: value}
        self.params = {name: 1.0 for name in self.param_names} 
        if params_user: # if the user specified some custom paramter values, update them
            self.params.update(params_user)


    @staticmethod
    def _compile(text):
        # turn equation text into code, with a readable error if it is malformed
        try:
            return compile(text.replace("^", "**"), "<equation>", "eval")
        except SyntaxError:
            raise ValueError(
                f"Could not read the equation '{text}'.Check the brackets, and use * for multiplication (2*x, not 2x)."
                )





    # sets a parameter value, or adds if it does not exist
    def set_param(self, name, value):
        self.params[name] = float(value)


    # evaluates the text
    # is the engine that actually calculates math equations using numbers or NumPy arrays
    def _evaluate(self, code, X, Y):
        """Run a compiled equation with x=X, y=Y (numbers or numpy arrays)."""
        X = np.asarray(X, dtype=float) # convert into NumPy arrays, if not already
        Y = np.asarray(Y, dtype=float)
        namespace = dict(MATH) # building the namespace of allowed words
        namespace.update(self.params) # include our parameter
        namespace["x"] = X # add X
        namespace["y"] = Y # add Y

        # the eval can only use our namespace, specify that builtin is empty, so don't use Python's
        # built-in functions, we only want our functions defined in the namepsace
        result = eval(code, {"__builtins__": {}}, namespace)
        result = result + 0.0 * X # if the result was a constant, convert it into an array
        # so force scalar result to be an array of 0's, so that it matches what the rest of code expects
        return result




    # FUNCTION FOR THE VERTOR FIELD"

    # F represents f(x,y), i.e. x' evaluated at (x, y)
    def F(self, X, Y):
        return self._evaluate(self.f_code, X, Y)


    # G represents g(x,y), i.e. x' evaluated at (x, y)
    def G(self, X, Y):
        return self._evaluate(self.g_code, X, Y)


    # represents the right-hand side in the form scipy's integrator need, i.e. : (t, [x, y])
    def rhs(self, t, state):
        px, py = state # extract the x and y points from the current state
        return [float(self.F(px, py)), float(self.G(px, py))]


    # computes the jacobian matrix at (x, y)
    # as seen in COMP 350, it uses central difference since it's error term decreases is O(h^2)
    # recall: df/dx  ~=  (f(x+h, y) - f(x-h, y)) / (2h)
    def jacobian(self, px, py, h=1e-6):
        fx = (self.F(px + h, py) - self.F(px - h, py)) / (2 * h)
        fy = (self.F(px, py + h) - self.F(px, py - h)) / (2 * h)
        gx = (self.G(px + h, py) - self.G(px - h, py)) / (2 * h)
        gy = (self.G(px, py + h) - self.G(px, py - h)) / (2 * h)
        return np.array([[fx, fy], [gx, gy]], dtype=float)