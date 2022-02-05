from django.shortcuts import render
from .models import Predicts
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import TrueMetall.settings as s
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


def bollinger(request):
    templates = s.TEMPLATES[0]['DIRS'][0]
    df = pd.read_excel(templates / 'data.xlsx', skiprows=[0, 1])

    df = df[['Date', 'target']]
    df = df.dropna()

    df["Date"] = pd.to_datetime(df["Date"])
    df = df.sort_values(by='Date')
    df.index = np.arange(df.shape[0])
    closing_prices = df['target']

    sma = closing_prices.rolling(20).mean()
    std = closing_prices.rolling(20).std()
    bollinger_up = sma + std * 2
    bollinger_down = sma - std * 2

    # Plot the data
    plt.title('metall')
    plt.xlabel('Days')
    plt.ylabel('Closing Prices')
    plt.plot(closing_prices, label='Closing Prices')
    plt.plot(bollinger_up, label='Bollinger Up', c='g')
    plt.plot(bollinger_down, label='Bollinger Down', c='r')
    plt.plot(sma, label='Simple Moving Average', c='y')
    plt.legend()
    plt.savefig('TrueMetallSite/static/TrueMetallSite/images/foo.png')
    plt.clf()
    return render(request, 'TrueMetallSite/bollinger.html')
