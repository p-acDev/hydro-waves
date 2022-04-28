#!/usr/bin/env python
# coding: utf-8

# # Dispersion relationship
# 
# the relation lonks the wave lenght $\lambda$ with its period T and the water depth h. 
# 
# **In deeep water** the relation is simply: $\lambda = 1.56 * T^2$ 
# 
# The deep water condition is: $h > 0.5 * \lambda$
# 
# **In shallow water** the relation is simply: $\lambda = \sqrt{g * h} * T$
# 
# The shallow water condition is: $h < 0.05 * \lambda$
# 
# 
# **In general**, let's use the real relationship: $w^2 = k * g * tanh(k*h)$


import numpy as np
from scipy import optimize
from functools import partial


def find_lambda(t, h, l0, verbose=False):
    """
        find the wave lenght from period and depth

        :param t: wave period in s
        :param h: water depth in m
        :param l0: initialization of lambda
        :type t: float or numpy array
        :type h: float
        :type l0: float
        :return: lambda wave length
        :rtype: float or numpy array
    """


    g = 9.81 #  gravity parametr in m.s^-2

    def t_function(t):
        """
            definition of left member of equation
        """
        w = (2*np.pi) / t #  pulsation in rad.s^-1 
        return w**2

    def lambda_function(l, h):
        """
            definition of right member of equation

            :param l: wave lenght in m
            :param h: water depth in m
            :type l: float or numpy array
            :type h: float

        """
        k = (2*np.pi) / l #  wave number in rad.m^-1
        return  k * g * np.tanh(k * h)
    
    # once h is fixed, right member of equation 
    # only depends on l
    p = partial(lambda_function, h=h)

    def f(l): return p(l) - t_function(t)
    
    # find the lambda
    # for the init of Newtown resolution, we use the approx of shallow water
    try:
        _, info = optimize.newton(f, l0, full_output=True)

        if verbose:
            print(info, "\n")

        # compare with deep water hyp to check

            if info.converged:
                if h > 0.5 * info.root:
                    print("DEEP WATER CONDITION")
                    print("EXPECTED RESULT: LAMBDA = {} m".format(round(1.56*t**2,2)))
                elif h < 0.05 * info.root:
                    print("SHALLOW WATER CONDITION")
                    print("EXPECTED RESULT: LAMBDA = {} m".format(round(t * (g * h)**2, 2)))
                else:
                    print("INTERMEDIATE CONDITION")

        return info

    except RuntimeError as e:
        print("[-]", e)


if __name__ == "__main__":
    
    t = 0.5
    h = 0.190

    l0 = 500

    info = find_lambda(t=t, h=h, l0=l0, verbose=True)
