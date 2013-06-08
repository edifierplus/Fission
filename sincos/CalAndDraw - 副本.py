"""
sincos/CalAndDraw.py
"""
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

def CD(argument):
    fig = plt.figure()
    aaaxxx = fig.add_subplot(111)
    k = float(argument.k)
    A = float(argument.A)
    phy = float(argument.phy)
    x = np.linspace(argument.x_min, argument.x_max, 10000)
    y = np.sin(k * x + phy) * A
    z = np.cos(k * x**2 - phy) * A / 2.0
    aaaxxx.plot(x, y, label="$Asin(kx+phy)$", color="red", linewidth=2)
    aaaxxx.plot(x, z, "b--", label="$\\frac{A}{2}cos(kx^2-phy)$")
    aaaxxx.set_ylim(-A, A)
    aaaxxx.grid()
    aaaxxx.legend()
    fig.xlabel("ffff")
    fig.savefig('sincos/images/test'+str(argument.id)+'.png')
    return