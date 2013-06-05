"""
sincos/views.py
"""
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from sincos.models import Argument
from django.shortcuts import render, get_object_or_404
from decimal import Decimal
from django.utils import timezone
from sincos import CalAndDraw

def index(request, erer = ""):
    latest_argument = Argument.objects.order_by('-pub_date')[:100]
    output = {'latest_argument': latest_argument, 'erer': erer}
    return render(request, 'sincos/index.html', output)

def calculate(request):
    try:
        theA = Decimal(request.POST['A'])
        thek = Decimal(request.POST['k'])
        thephy = Decimal(request.POST['phy'])
    except:
        return index(request, 'Please enter decimals.')
    else:
        newidea = Argument(A = theA, k = thek, phy = thephy,
            x_min = -10.0, x_max = 10.0, y_min = -2.0, y_max = 2.0,
            delta_x = 0.01, pub_date = timezone.now()
        )
        newidea.save()
        new_id = str(newidea.id)
        #Do the calculation
        CalAndDraw.CD(newidea)
        return HttpResponseRedirect(
            reverse('sincos:result', kwargs={'argument_id': new_id}))

def result(request, argument_id):
    argument = get_object_or_404(Argument, pk = argument_id)
    return render(request, 'sincos/result.html', {'argument': argument})
