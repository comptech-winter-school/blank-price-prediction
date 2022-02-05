from django.shortcuts import render
from .models import Predicts
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import TrueMetall.settings as s
import io
import base64
from .predicts_handler import data_handler, model_handler
import datetime


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
    file = request.FILES['document'].file
    file.seek(0)
    data_handler.handle_data(file)
    data_handler.create_features()
    predictions = model_handler.predict_lstm()
    prediction = predictions[0]
    predictions = model_handler.predict_another().tolist()[0]

    now = datetime.datetime.today()
    preds1 = Predicts()
    preds2 = Predicts()
    preds1.set_datetime(now)
    preds1.set_one_week_predict(prediction)
    preds1.save()

    preds2.set_datetime(now)
    preds2.set_one_week_predict(predictions[0])
    preds2.set_two_weeks_predict(predictions[1])
    preds2.set_three_weeks_predict(predictions[2])
    preds2.set_four_weeks_predict(predictions[3])
    preds2.save()

    # Rounding the prediction
    prediction = round(prediction, 2)

    context = {"date": now,
               "predictions": processPredictions(predictions),
               "prediction": prediction}

    return render(request, 'TrueMetallSite/current_predict.html', context)


# Processing predictions and rounding it
def processPredictions(predictions):

    np_predictions = np.array(predictions)
    processed_predictions = []

    for np_prediction in np_predictions:
        np_prediction = round(np_prediction, 2)
        processed_predictions.append(np_prediction)

    predictions = processed_predictions

    return predictions


def bollinger(request):
    df = pd.read_excel(s.TEMPLATES[0]['DIRS'][0] / 'data.xlsx', skiprows=[0, 1])

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
    plt.figure(figsize=(13, 6))
    plt.title('Металлические заготовки', x=0.5, y=1.03, fontsize=18)
    plt.xlabel('День', labelpad=7, fontsize=14)
    plt.ylabel('Цена закрытия', labelpad=15, fontsize=14)
    plt.plot(closing_prices, label='Цена закрытия', c='#000', linewidth=1.3, zorder=10)
    plt.plot(bollinger_up, label='Верхняя Боллинджера', c='g', linewidth=1)
    plt.plot(bollinger_down, label='Нижняя Боллинджера', c='r', linewidth=1)
    plt.plot(sma, label='Средняя скользящая', c='#ffc800', linewidth=1)
    plt.legend()
    img = io.BytesIO()
    plt.savefig(img, format='png')
    img.seek(0)
    plot_url = base64.b64encode(img.getvalue()).decode()
    plt.close()
    return render(request, 'TrueMetallSite/bollinger.html', context={'imagen': plot_url})
