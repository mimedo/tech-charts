import yfinance as yf
import mplfinance as mpf
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

data = yf.download('AAPL', start='2019-01-01', end='2024-04-09', interval='1d')

kwargs = dict(
    type='line',
    style='yahoo',
    xrotation=90,
    ylabel='Aktienpreis',
    xlabel='Zeitraum',
    xlim=('2024-01-01', '2024-04-09'),
    datetime_format='%Y',
)

fig, axlist = mpf.plot(
    data,
    **kwargs,
    returnfig=True
)

dataset = data.values
train_size = int(np.ceil(len(dataset) * .95))
train = data[:train_size]
valid = data[train_size:].copy()
predictions_df = pd.read_json('predicted_prices_apple.json')

predictions = pd.Series(predictions_df['Predictions'].values, index=pd.to_datetime(predictions_df['Date']))
valid.loc[:, 'Predictions'] = predictions

axStock = axlist[0]
axStock.legend(loc='lower right')
mpf.show()

# Gesamtansicht
plt.xlabel('Zeitraum', fontsize=11)
plt.ylabel('Aktienpreis', fontsize=11)
plt.plot(train['Close'])
plt.plot(valid[['Close', 'Predictions']])
plt.legend(['Trainingsdatensatz', 'Testdatensatz', 'Vorhersage'], loc='lower right')
plt.show()