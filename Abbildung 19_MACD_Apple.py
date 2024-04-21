import yfinance as yf
import pandas as pd
import mplfinance as mpf

stock_data = yf.download('AAPL', start='2019-01-01', end='2024-04-09', interval='1d')

stock_data['EMA12'] = stock_data['Close'].ewm(span=12, min_periods=0, adjust=False).mean()
stock_data['EMA26'] = stock_data['Close'].ewm(span=26, min_periods=0, adjust=False).mean()
stock_data['MACD'] = stock_data['EMA12'] - stock_data['EMA26']
stock_data['Signal Line'] = stock_data['MACD'].ewm(span=9, min_periods=0, adjust=False).mean()

stock_data.reset_index(inplace=True)
stock_data['Date'] = pd.to_datetime(stock_data['Date'])
stock_data.set_index('Date', inplace=True)

ap1 = mpf.make_addplot(stock_data[['MACD']], panel=1, ylabel='MACD', color='#1f77b4', width=1.2, ylim=(-4.5, 1.5))
ap2 = mpf.make_addplot(stock_data[['Signal Line']], panel=1, color='#ff7f0e', width=1.2, ylim=(-4.5, 1.5))

kwargs = dict(
    type='candle',
    style='yahoo',
    xrotation=90,
    ylabel='Aktienpreis',
    xlabel='Zeitraum',
    figsize=(10, 5.2),
    xlim=('2024-01-01', '2024-04-09'),
    ylim=(168, 197),
    datetime_format='%b %d',
    addplot=[ap1, ap2],
    panel_ratios=(4, 2)
)

fig, axlist = mpf.plot(
    stock_data,
    **kwargs,
    returnfig=True
)

ax = axlist[2]
ax.plot(stock_data.index, stock_data['MACD'], label='MACD', color='#1f77b4')
ax.plot(stock_data.index, stock_data['Signal Line'], label='Signallinie', color='#ff7f0e')
ax_pos = ax.get_position()
ax.set_position([ax_pos.x0, ax_pos.y0 - 0.02, ax_pos.width, ax_pos.height])
ax.legend()

for ax in axlist:
    ax.tick_params(axis='both', labelsize=11)
    ax.set_xlabel(ax.get_xlabel(), fontsize=11)
    ax.set_ylabel(ax.get_ylabel(), fontsize=11)
    ax.legend(fontsize=11)

ax.get_legend().remove()
ax = axlist[0]
ax.get_legend().remove()

mpf.show()
