#########################
project "Forecasting prices for metal product"
#########################
Winter school CompTech 2022. The project was carried out jointly with company www.evraz.com

Objective of the project
=================

Based on the data accumulated over the past few years, build a predictive model to predict behavior
market prices for metal product.

Out results
=================

Prepared data:

- semantic analysis
- decomposition of data by meaning
- search for outliers
- filling in gaps
- generation of new features

Tried different models:

- linear regression
- random forest
- tree boosting
- fully connected neural networks
- recurrent neural networks

On the basis of a recurrent neural network, results of about 10% of MAPE were obtained.
An application has been created that processes new user data and returns a prediction for the next week.



Repository structure
=================

- preparcer: create many small tables of the usual format from the original large table, save them in tables/

- append_and_make_features: distributes new data across tables/, generates new features and dataframe-input for predictor models. It is important that tables/ exist and are non-empty!

- grid_lstm: training the lstm model on a grid of parameters in order to identify the optimal architecture

- lstm_predict: make a prediction of trained lstm


