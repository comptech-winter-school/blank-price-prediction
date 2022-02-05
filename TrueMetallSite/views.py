from django.shortcuts import render
from .models import Predicts
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import TrueMetall.settings as s
import io
import base64
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
    plt.figure(figsize=(14, 6))
    plt.title('Металлические заготовки', x=0.5, y=1.03, fontsize=18)
    plt.xlabel('День', labelpad=7, fontsize=14)
    plt.ylabel('Цена закрытия', labelpad=15, fontsize=14)
    plt.plot(closing_prices, label='Цена закрытия', c='g')
    plt.plot(bollinger_up, label='Верхняя Боллинджера', c='b', alpha=0.5)
    plt.plot(bollinger_down, label='Нижняя Боллинджера', c='b', alpha=0.5)
    plt.plot(sma, label='Средняя скользящая', c='#A66D00', alpha=0.5)
    plt.legend()
    img = io.BytesIO()
    plt.savefig(img, format='png')
    img.seek(0)
    plot_url = base64.b64encode(img.getvalue()).decode()
    plt.close()
    return render(request, 'TrueMetallSite/bollinger.html', context={'imagen': plot_url})
