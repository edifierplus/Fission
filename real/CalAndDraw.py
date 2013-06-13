# -*- coding: UTF-8 -*-
"""
sincos/CalAndDraw.py
"""
from real.models import Reactor, Stage
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker

#beta衰变常数 单位 /s
LALA = {'I': 0.0000287, 'Xe': 0.0000209, 'Pm':0.00000358}

#微观吸收截面 单位 b=10^-28m^2
SIGMA_A = {'Xe': 2700000, 'Sm': 40800}

#计算宏观截面 单位 /m(b, 10^28m^-3)
def SIGMA(sigma, N):
    return sigma * N

#计算中子通量密度 单位 10^28m^-2s^-1(m^3, /m, MW)
def PHY(V, Sigmaf, P):
    return 3.12e-12 * P / V / Sigmaf

#计算I/Pm的变化
def get_y_I_Pm(x, A1, L1, N10):
    return A1 / L1 + (N10 - A1 / L1) * np.exp(- L1 * x)

#计算Xe的变化
def get_y_Xe(x, A1, A2, B2, L1, L2, N10, N20):
    c11 = (A1 + A2) / (L2 + B2)
    c22 = L1 * (N10 - A1 / L1) / (L2 + B2 - L1)
    c33 = N20 - c11 - c22

    return c11 + c22 * np.exp(- L1 * x) + c33 * np.exp(- (L2 + B2) * x)

#计算Sm的变化
def get_y_Sm(x, A3, B4, L3, N30, N40):
    if A3 == 0 and B4 == 0:
        ans_sm = N40 + N30 * (1 - np.exp(- L3 * x))
    else:
        c11 = A3 / B4
        c22 = L3 * (N30 - A3 / L3) / (B4 - L3)
        c33 = N40 - c11 - c22
        ans_sm = c11 + c22 * np.exp(- L3 * x) + c33 * np.exp(- B4 * x)

    return ans_sm

#计算rho
def get_rho(Ns, smallsigma, bigsigma):
    return (- Ns * smallsigma / bigsigma)


#计算得到所有的点
def wtf(reactor, last_stage, next_stage):
    usefulsf = SIGMA(float(reactor.sigmaf), float(reactor.N))#实用宏观裂变截面
    usefulsa = SIGMA(float(reactor.sigmaa), float(reactor.N))#实用宏观反应物吸收截面
    thephy = PHY(float(reactor.V), usefulsf, float(next_stage.power))

    A1 = float(reactor.gamaI) * usefulsf * thephy
    A2 = float(reactor.gamaXe) * usefulsf * thephy
    B2 = SIGMA_A['Xe'] * thephy
    A3 = float(reactor.gamaPm) * usefulsf * thephy
    B4 = SIGMA_A['Sm'] * thephy

    points = {'x': np.arange(0, float(next_stage.t) * 3600 + 1, 60), 
        'phy': thephy}
    points['I'] = get_y_I_Pm(points['x'], A1, LALA['I'], 
        float(last_stage.dens_I))
    points['Xe'] = get_y_Xe(points['x'], A1, A2, B2, LALA['I'], 
        LALA['Xe'], float(last_stage.dens_I), float(last_stage.dens_Xe))
    points['Pm'] = get_y_I_Pm(points['x'], A3, LALA['Pm'], 
        float(last_stage.dens_Pm))
    points['Sm'] = get_y_Sm(points['x'], A3, B4, LALA['Pm'], 
        float(last_stage.dens_Pm), float(last_stage.dens_Sm))
    points['I_Xe'] = get_rho(points['Xe'], SIGMA_A['Xe'], usefulsa)
    points['Pm_Sm'] = get_rho(points['Sm'], SIGMA_A['Sm'], usefulsa)
    points['ALL'] = points['I_Xe'] + points['Pm_Sm']
    return points

def initiate_reactor(reactor):
    first_stage = Stage(
        myreactor = reactor,
        reactor_id = reactor.id,
        sn = 1,
        t = 1.0,
        power = 0,
        phy = 0,
        dens_I = 0,
        dens_Xe = 0,
        dens_Sm = 0,
        dens_Pm = 0)
    first_stage.save()

    #画一个平的图
    thex = np.arange(0, float(first_stage.t) * 3600 + 1, 60)
    density1 = np.exp(thex / 360)
    density2 = np.exp(10-thex / 360)
    density3 = np.sin(thex / 360)
    density4 = np.cos(thex / 360)
    reactivity1 = np.sin(thex / 360)
    reactivity2 = np.sin(thex / 360+1)
    reactivity3 = reactivity1 + reactivity2

    thepoints = {
        'x': thex,
        'I': density1,
        'Xe': density2,
        'Pm': density3,
        'Sm': density4,
        'I_Xe': reactivity1,
        'Pm_Sm': reactivity2,
        'ALL': reactivity3}

    drawimage(thepoints, reactor.id, 1)

    return first_stage

def create_next_stage(reactor, last_stage, next_power, next_time):
    next_stage = Stage(
        myreactor = reactor,
        reactor_id = reactor.id,
        sn = last_stage.sn + 1,
        t = next_time,
        power = next_power,
        phy = 250,
        dens_I = -1,
        dens_Xe = -1,
        dens_Pm = -1,
        dens_Sm = -1)
    next_stage.save()

    thepoints = wtf(reactor, last_stage, next_stage)

    next_stage.dens_I = thepoints['I'][-1]
    next_stage.dens_Xe = thepoints['Xe'][-1]
    next_stage.dens_Pm = thepoints['Pm'][-1]
    next_stage.dens_Sm = thepoints['Sm'][-1]
    next_stage.phy = thepoints['phy']
    next_stage.save()

    drawimage(thepoints, reactor.id, next_stage.sn)

    return next_stage

def drawimage(points, rea, sta):
    points['x'] /= 3600
    fig = plt.figure(figsize=(8, 10))

    ax1 = fig.add_subplot(211)
    ax1.plot(points['x'], points['I'], 'b-')
    ax1.plot(points['x'], points['Xe'], 'b:')
    ax1.grid()
    ax1.set_title('Nuclear Density - Time Curve', family='serif')
    ax1.set_xlabel('time(h)', family='serif')
    ax1.set_ylabel('N$(10^{28}m^{-3})$', family='serif')
    ax1.yaxis.set_major_formatter(ticker.FormatStrFormatter('%.2e'))
    for label in ax1.get_yticklabels():
        label.set_fontsize('9')
        label.set_family('serif')
        label.set_color('b')

    for label in ax1.get_xticklabels():
        label.set_fontsize('9')
        label.set_family('serif')
    
    ax2 = ax1.twinx()
    ax2.plot([], [], 'b-')
    ax2.plot([], [], 'b:')
    ax2.plot(points['x'], points['Pm'], 'r-')
    ax2.plot(points['x'], points['Sm'], 'r:')
    ax2.yaxis.set_major_formatter(ticker.FormatStrFormatter('%.2e'))
    for label in ax2.get_yticklabels():
        label.set_fontsize('9')
        label.set_family('serif')
        label.set_color('r')

    ax3 = fig.add_subplot(212)
    ax3.plot(points['x'], points['I_Xe'], 'b-')
    ax3.plot(points['x'], points['Pm_Sm'], 'r-')
    ax3.plot(points['x'], points['ALL'], 'g-')
    ax3.grid()
    ax3.set_title('Delta Reactivity - Time Curve', family='serif')
    ax3.set_xlabel('time(h)', family='serif')
    ax3.set_ylabel('$\\Delta\\rho$', family='serif')
    for label in ax3.get_yticklabels():
        label.set_fontsize('9')
        label.set_family('serif')

    for label in ax3.get_xticklabels():
        label.set_fontsize('9')
        label.set_family('serif')

    leg1 = ax2.legend(("$^{135}I$", "$^{135}Xe$", "$^{149}Pm$", "$^{149}Sm$"),
           'upper right', shadow=True)
    for t in leg1.get_texts():
        t.set_fontsize('small')
    leg2 = ax3.legend(("$^{135}Xe$", "$^{149}Sm$", "$Total$"),
           'upper right', shadow=True)
    for t in leg2.get_texts():
        t.set_fontsize('small')

    plt.savefig('real/images/reactor'+str(rea)+'_stage'+str(sta)+'.png')
    return