#### STOCK PRICE PREDICTIONS

In ths notebook we try to implement stock amrket analysis and short ter prediction.

***Moving averages method***
Implementation based on the Mark Minervini Trend Template. Author had found that these conditions indicates that the stock is ready to potentially be bought and go on a massive run. It could be a good start point for trading.

Program evaluates and compares 52 week Low and High prices as well. 

As a baseline, we scraped and checked 95 tickers from Yahoo Finance. And got a recommendation to look deeper in theese tickers.

Tickers checked: 95

Recomendations for buying:

   Stock  50 Day MA  150 Day Ma  200 Day MA  52 Week Low  52 week High
0    CVX     166.38      140.56      130.26    91.491524    178.279999
1    XOM      87.66       75.49       70.69    50.938484     99.089996
2    OKE      67.08       63.01       61.08    47.143963     72.591393
3    WWE      61.14       55.87       55.67    46.839493     67.173523
4    OLN      58.65       55.37       53.79    40.311237     66.919998
5    PBR      13.05       10.96       10.18     6.629016     14.800000
6   ITUB       5.25        4.64        4.57     3.593598      5.851901
7    OXY      60.96       45.20       41.08    21.840628     70.726555
8     ET      11.21        9.78        9.61     7.875857     12.010000
9    KMI      18.98       17.32       17.01    14.782840     20.020000
10   GGB       5.84        5.21        5.04     4.023648      6.373935
11   PCG      12.22       12.03       11.53     8.290000     13.030000
12   SLB      41.93       37.40       35.47    26.035944     48.035000
13   RIG       4.19        3.71        3.70     2.760000      5.080000
14   BKR      34.72       29.58       28.13    19.117956     38.532143
15   AUY       5.54        4.76        4.60     3.751836      6.280000
16   MPC      90.88       76.48       72.41    49.268764    105.620003
17  CTRA      29.71       23.90       22.45    13.301115     35.520000



We selected one ticker from a given list and tried to go deeper.

In the notebook you will find great variety of different charts to know more about historical stock price and company's finaces.

We used LSTM Bidirectional model to predict future prices. Predicted period - 14 days.

model = Sequential()
model.add(Bidirectional(LSTM(64, activation='relu', return_sequences=True),  input_shape=(x_train.shape[1], 1)))
model.add(Dense(32, activation='relu'))
model.add(Bidirectional(LSTM(32)))
model.add(Dense(32, activation='relu'))
model.add(Dense(1))
model.compile(optimizer='adam', loss='mse')

model_path = 'LSTM_multivariate.h5'
early_stopings = tf.keras.callbacks.EarlyStopping(monitor='val_loss', min_delta=0, patience=5, mode='min') #,  
checkpoint =  tf.keras.callbacks.ModelCheckpoint(model_path, monitor='val_loss', save_best_only=True,  verbose=0, mode='min') 
callbacks=[early_stopings,checkpoint] 

#Train the model
history = model.fit(x_train, y_train, epochs=20, batch_size=64, steps_per_epoch=100, validation_split=0.05, verbose=1, callbacks=callbacks)

image.png



