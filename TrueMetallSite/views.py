from django.shortcuts import render
from .models import Predicts
# Create your views here.


def index(request):
    return render(request, 'TrueMetallSite/index.html')


def predicts(request):
    predicts = Predicts.objects.order_by('datetime')
    context = {
        'predicts': predicts
    }
    return render(request, 'TrueMetallSite/predicts.html', context)


def current_predict(request):
    return render(request, 'TrueMetallSite/current_predict.html')
