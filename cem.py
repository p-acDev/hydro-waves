import scipy.optimize as op
from functools import partial
import numpy as np
from dispersion import find_lambda

def u(vpeak, duration_time):
    """[summary]

    Args:
        vpeak (float): wind speed at 10 m 3 s
        duration_time (float): duration time in min

    Returns:
        float : wind speed at duration time
    """

    return vpeak * 0.8347 * duration_time ** (-0.056)

def tmin(fetch, wind_speed):
    """[summary]

    Args:
        fetch (float): fetch in m
        wind_speed (float): wind speed at desired duration time
    """

    return 77.23 * (fetch**0.67) / ((wind_speed ** 0.34) * (9.81 ** 0.33)) / 60

def solver_u_tmin(vpeak, fetch):
    """solves the non linear two equations system

    Args:
        vpeak (float): vpeak at 10m 3s
        fetch (float): fetch in m

    Returns:
        float, float: wind speed at duration time, duration time to be considered in Hs Tp calc
    """
    f1 = partial(u, vpeak)
    f2 = partial(tmin, fetch)

    def f(x):
        return [x[0] - f1(x[1]), x[1] - f2(x[0])]
    
    u_output, tmin_output = op.fsolve(f, (vpeak, 30.0))

    return u_output, tmin_output

def sea(vpeak, fetch, depth):

    u_tmin, tmin = solver_u_tmin(vpeak, fetch)
    
    uetoile = lambda x: x*np.sqrt(0.001*(1.1 + 0.035*x))

    hs = (0.0413 * (uetoile(u_tmin)**2) / 9.81) * np.sqrt((9.81*fetch) / (uetoile(u_tmin)**2))
    tp = 0.751 * (uetoile(u_tmin) / 9.81) * ((9.81*fetch) / (uetoile(u_tmin)**2)) ** (1/3)

    lp = find_lambda(tp, depth, 1.56 * tp ** 2).root

    hs2 = (3/4) * depth
    hs3 = lp * 0.142 * np.tanh(2 * np.pi * (depth / lp))

    return u_tmin, tmin, min([hs, hs2, hs3]), tp, lp


if __name__ == "__main__":
    
    vpeak = 35
    fetch = 500
    depth = 10

    u_tmin, tmin, hs, tp, lp = sea(vpeak, fetch, depth)

    print(tmin*60, u_tmin, hs, tp, "\n", lp)