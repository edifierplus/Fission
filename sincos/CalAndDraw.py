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
    aaaxxx.plot(x, y, label="$sin(x)$", color="red", linewidth=2)
    aaaxxx.plot(x, z, "b--", label="$cos(x^2)$")
    aaaxxx.set_ylim(-A, A)
    fig.savefig('sincos/images/test'+str(argument.id)+'.png')
    return