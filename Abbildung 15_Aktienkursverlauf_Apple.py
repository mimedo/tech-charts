import yfinance as yf
import mplfinance as mpf
import matplotlib.pyplot as plt

data = yf.download('AAPL', start='2019-01-01', end='2024-04-09', interval='1d')

kwargs = dict(
    type='line',
    style='yahoo',
    xrotation=90,
    ylabel='Aktienpreis',
    xlabel='Zeitraum',
    xlim=('2019-01-01', '2024-04-09'),
    datetime_format='%Y',
)

fig, axlist = mpf.plot(
    data,
    **kwargs,
    returnfig=True
)

axStock = axlist[0]
axStock.legend(loc='lower right')
mpf.show()

# Gesamtansicht
plt.xlabel('Zeitraum', fontsize=11)
plt.ylabel('Aktienpreis', fontsize=11)
plt.plot(data['Close'])
plt.legend(['Aktienkursverlauf'], loc='lower right')
plt.show()