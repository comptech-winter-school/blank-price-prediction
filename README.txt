project' README.

preparcer: create many small tables of the usual format from the original large table, save them in tables/

append_and_make_features: distributes new data across tables/, generates dataframe-input for predictor models. 
It is important that tables/ exist and are non-empty!

final: training of the nn model

model_inference: making predictions of a trained nn

grid_lstm: training the lstm model on a grid of parameters in order to identify the optimal architecture

lstm_predict: make a prediction of trained lstm
