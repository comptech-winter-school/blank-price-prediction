import pandas as pd
import numpy as np
import joblib
from keras.models import load_model
from TrueMetall.settings import TEMPLATES as TEMPLATES_LIST


def get_predict(scaler, model, df_train, df_test, shift):
    """
    scales the data using a scaler and makes a prediction using a model
    """
    scaler = scaler
    df_training_processed = df_train.iloc[:, :].values
    df_training_scaled = scaler.transform(df_training_processed)
    model = model

    # Let's create a sample for testing
    df_total = pd.concat((df_train, df_test), axis=0)
    test_inputs = df_total[len(df_total) - len(df_test) - shift:]
    test_inputs_processed = test_inputs.iloc[:, :].values
    test_inputs_scaled = scaler.transform(test_inputs_processed)
    test_features = []
    for i in range(shift, len(test_inputs_scaled)):
        test_features.append(test_inputs_scaled[i - shift:i, :])

    # Convert it again to an np array and make a format suitable for LSTM
    test_features = np.array(test_features)
    test_features = np.reshape(test_features, (test_features.shape[0], test_features.shape[1], test_features.shape[2]))

    predictions = model.predict(test_features)
    predictions = predictions.reshape(df_test.shape[0], )

    # We shove it into the intermediate matrix and invert it
    test_data_processed = (df_test.copy()).iloc[:].values
    test_data_processed[:, 0] = predictions
    test_data_processed = scaler.inverse_transform(test_data_processed)
    predictions = test_data_processed[:, 0]

    return predictions


def predict():
    templates_path = TEMPLATES_LIST[0]['DIRS'][0]
    file_name = 'data_for_lstm.csv'

    df = pd.read_csv(templates_path / file_name)
    df.drop(['timepoint'], axis=1, inplace=True)

    path = '/content/drive/MyDrive/metall/Прогноз металлические заготовки/cloud/'
    model = load_model(templates_path / 'lstm.hdf5')
    scaler = joblib.load(templates_path / 'scaler_lstm')
    len_ = df.shape[0]
    length_history = 8
    df_train = df.iloc[len_ - length_history - 1:len_ - 1, :].copy()
    df_test = df.iloc[len_ - 1:len_, :].copy()
    return get_predict(scaler=scaler, model=model, df_train=df_train.copy(), df_test=df_test.copy(), shift=length_history)
