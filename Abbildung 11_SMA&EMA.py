import yfinance as yf
import mplfinance as mpf

stock_data = yf.download('AAPL', start='2023-12-25', end='2024-03-10', interval='1d')

stock_data['SMA_40'] = stock_data['Close'].rolling(window=1).mean()
stock_data['EMA_40'] = stock_data['Close'].ewm(span=1, adjust=False).mean()

stock_data.reset_index(inplace=True)
stock_data.set_index('Date', inplace=True)

kwargs = dict(
    type='candle',
    style='yahoo',
    xrotation=90,
    ylabel='Aktienpreis',
    xlabel='Zeitraum',
    figscale=1,
    xlim=('2024-01-10', '2024-03-10'),
    datetime_format='%b %d'
)

fig, axlist = mpf.plot(
    stock_data,
    **kwargs,
    mav=9,
    ema=9,
    returnfig=True,
)

ax = axlist[0]
ax.plot(stock_data.index, stock_data['SMA_40'], label='SMA', color='#1f77b4')
ax.plot(stock_data.index, stock_data['EMA_40'], label='EMA', color='#ff7f0e')

ax.legend(loc='lower left')
mpf.show()
