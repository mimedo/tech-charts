import yfinance as yf
import mplfinance as mpf

stock_data = yf.download('AAPL', start='2019-01-01', end='2024-04-09', interval='1d')

stock_data['SMA'] = stock_data['Close'].rolling(window=1).mean()
stock_data['EMA'] = stock_data['Close'].ewm(span=1, adjust=False).mean()

stock_data.reset_index(inplace=True)
stock_data.set_index('Date', inplace=True)

kwargs = dict(
    type='candle',
    style='yahoo',
    xrotation=90,
    ylabel='Aktienpreis',
    xlabel='Zeitraum',
    figscale=1,
    xlim=('2024-01-01', '2024-04-09'),
    ylim=(165, 197),
    datetime_format='%b %d'
)

fig, axlist = mpf.plot(
    stock_data,
    **kwargs,
    mav=50,
    ema=100,
    returnfig=True
)

ax = axlist[0]
ax.plot(stock_data.index, stock_data['SMA'], label='SMA', color='#1f77b4')
ax.plot(stock_data.index, stock_data['EMA'], label='EMA', color='#ff7f0e')

ax.legend(loc='lower left')
mpf.show()
