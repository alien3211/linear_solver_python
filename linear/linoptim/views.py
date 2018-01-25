from collections import OrderedDict

from django.forms import formset_factory
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from scipy.optimize import linprog

from .forms import LinearForm


def result(request):
    data = request.session.get('_data')


    return render(request, 'linoptim/result.html',
                  {'data': data}
                  )


def index(request):
    """
    Allows a user to update their own profile.
    """

    # Create the formset, specifying the form and formset we want to use.
    LinkFormSet = formset_factory(LinearForm)

    if request.method == 'POST':

        link_formset = LinkFormSet(request.POST)

        if link_formset.is_valid():

            data_list = []
            for link_form in link_formset:
                row = list(map(lambda x: float(x), link_form.cleaned_data.get('row').split(';')))
                data_list.append(row)

            A = [list(map(lambda a: a*-1, x)) for x in data_list[:-1] ]
            c = data_list[-1]
            b = [x.pop() for x in A]

            linear_result = linear_optimalize(A,b,c)

            request.session['_data'] = {
                'linear_result': linear_result,
            }
            return HttpResponseRedirect(reverse('result'))

    else:
        link_formset = LinkFormSet()

    context = {
        'link_formset': link_formset,
    }

    return render(request, 'linoptim/logistic_optim.html', context)

def linear_optimalize(A,b,c):
    bounds = list(map(lambda _: (0,None), c))

    res = linprog(c, A_ub=A, b_ub=b, bounds=bounds)
    return list(res.x)