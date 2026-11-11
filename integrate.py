import numpy as np
from scipy.integrate import solve_ivp
 
 
def trajectory(system, x0, y0, t_max=30.0, backward=False, bound=50.0):
    # integrate from the start point (x0, y0).
 
    # backward=True runs time in reverse. That is how to draw the stable manifold of a saddle point
 
    # bound: if the trajectory leaves the box |x|,|y| < bound we stop
    # (otherwise a blow-up to infinity would run forever)
 
    # Returns two lists: all the x values and all the y values.
 

    # this function acts as an "event" trigger .
    # signals to solver to stop computing trajecory when system
    # is off screen (i.e. greater than the bound)
    def left_the_box(t, state): # state represent the current x and y position, t is the time
        size = max(abs(state[0]), abs(state[1]))
        if not np.isfinite(size): # overflowed to inf/nan, count as left the box
            # in certain ODE's, the value can shoot up very fast, so need to account for those
            size = 1e300 # so consider it as outside the box 
        return size - bound
 
    # scipy's solver checks if the function has an attirbute "terminal"
    # this tells it to stop when the event triggers
    left_the_box.terminal = True 
 
    t_end = -t_max if backward else t_max
 
    try: # try to solve the initial value problem
        solution = solve_ivp(
            system.rhs,             # the vector field 
                                    #(i.e. the function that computes the derivatives at any given point)
            (0.0, t_end),           # time interval
            [x0, y0],               # starting point
            events=left_the_box,    # even trigger
            method="LSODA",         # solver algorithm, it should handle all cases fine
                                    # (automatically switches strategies depending on the system)
            max_step=0.05,          # small steps so curves look smooth
            rtol=1e-8,              # relative and absolute error tolerances, so ensures mathematical correctness
            atol=1e-10,
        )
    except (ValueError, FloatingPointError, ZeroDivisionError, OverflowError):
        # on any erro, just return the starting point, so will draw nothing, but the app won't crash
        return np.array([x0]), np.array([y0])

    return solution.y[0], solution.y[1] # return list of all x and y points