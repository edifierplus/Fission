# -*- coding: UTF-8 -*-
"""
real/views.py
"""
from django.shortcuts import render, get_object_or_404
from django.utils import timezone
from real.models import Reactor, Stage
from decimal import Decimal
from real import CalAndDraw

#裂变产额 单位 比例
GAMA = {
    'U3': {'I': 0.04884, 'Xe': 0.01363, 'Pm': 0.0066},
    'U5': {'I': 0.06386, 'Xe': 0.00228, 'Pm': 0.0113},
    'Pu': {'I': 0.06100, 'Xe': 0.01087, 'Pm': 0.0119}}

#微观裂变截面 单位 b=10^-28m^2
SIGMAF = {'U3': 530.6, 'U5': 583.5, 'Pu': 744.0}

#微观吸收截面 单位 b=10^-28m^2
SIGMAA = {'U3': 579.6, 'U5': 680.9, 'Pu': 1011.2}

def index(request, erer = ""):
    latest_reactor = Reactor.objects.order_by('-id')[:100]
    output = {'latest_reactor': latest_reactor, 'erer': erer}
    return render(request, 'real/index.html', output)

def build_reactor(request):
    try:
        theV = Decimal(request.POST['V'])
        theN = Decimal(request.POST['N'])
        theelement = request.POST['element']
    except:
        return index(request, 'Please enter valid values.')
    else:
        if theelement == 'U-233':
            gamas = GAMA['U3']
            sf = SIGMAF['U3']
            sa = SIGMAA['U3']
        elif theelement == 'Pu-239':
            gamas = GAMA['Pu']
            sf = SIGMAF['Pu']
            sa = SIGMAA['Pu']
        else:
            gamas = GAMA['U5']
            sf = SIGMAF['U5']
            sa = SIGMAA['U5']

        new_reactor = Reactor(
            V = theV,
            N = theN,
            gamaI = gamas['I'],
            gamaXe = gamas['Xe'],
            gamaPm = gamas['Pm'],
            sigmaf = sf,
            sigmaa = sa,
            element = theelement,
            pub_date = timezone.now()
            )
        new_reactor.save()
        #Initiate the Reactor
        first_stage = CalAndDraw.initiate_reactor(new_reactor)

        return show_stage(request, new_reactor, first_stage, first_stage)

def cal_stage(request):
    try:
        reactor_id = int(request.POST['reactor_id'])
        next_power = Decimal(request.POST['next_power'])
        next_time = Decimal(request.POST['next_time'])
    except:
        reactor = get_object_or_404(Reactor, pk = reactor_id)
        next_stage = reactor.stage_set.all().order_by('-sn')[0]
        if next_stage.sn == 1:
            last_stage = next_stage
        else:
            last_stage = reactor.stage_set.all().order_by('-sn')[1]
        return show_stage(request, reactor, last_stage, next_stage, 'Please enter valid values.')
    else:
        reactor = get_object_or_404(Reactor, pk = reactor_id)
        last_stage = reactor.stage_set.all().order_by('-sn')[0]
        next_stage = CalAndDraw.create_next_stage(reactor, last_stage, 
            next_power, next_time)
        return show_stage(request, reactor, last_stage, next_stage)

def show_stage(request, reactor, last_stage, next_stage, erer = ''):
    output = {'last_stage': last_stage, 
        'next_stage': next_stage,
        'reactor': reactor,
        'erer': erer}

    output['last_stage'].phy = "%.4e" % output['last_stage'].phy
    output['last_stage'].dens_I = "%.4e" % output['last_stage'].dens_I
    output['last_stage'].dens_Xe = "%.4e" % output['last_stage'].dens_Xe
    output['last_stage'].dens_Pm = "%.4e" % output['last_stage'].dens_Pm
    output['last_stage'].dens_Sm = "%.4e" % output['last_stage'].dens_Sm
    if type(output['next_stage'].phy) != type("SB"):
        output['next_stage'].phy = "%.4e" % output['next_stage'].phy
        output['next_stage'].dens_I = "%.4e" % output['next_stage'].dens_I
        output['next_stage'].dens_Xe = "%.4e" % output['next_stage'].dens_Xe
        output['next_stage'].dens_Pm = "%.4e" % output['next_stage'].dens_Pm
        output['next_stage'].dens_Sm = "%.4e" % output['next_stage'].dens_Sm

    return render(request, 'real/stage.html', output)

def show_result(request, reactor_id):
    reactor = get_object_or_404(Reactor, pk = reactor_id)
    stages = reactor.stage_set.all()

    for st in stages:
        st.phy = "%.4e" % st.phy

    return render(request, 'real/result.html', {'reactor':reactor, 
        'stages':stages})