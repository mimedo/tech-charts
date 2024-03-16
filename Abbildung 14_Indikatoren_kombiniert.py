import yfinance as yf
import pandas as pd
import mplfinance as mpf

stock_data = yf.download('AYX', start='2021-12-10', end='2024-03-17', interval='1wk')

# MACD
stock_data['EMA12'] = stock_data['Close'].ewm(span=12, min_periods=0, adjust=False).mean()
stock_data['EMA26'] = stock_data['Close'].ewm(span=26, min_periods=0, adjust=False).mean()
stock_data['MACD'] = stock_data['EMA12'] - stock_data['EMA26']
stock_data['Signal Line'] = stock_data['MACD'].ewm(span=9, min_periods=0, adjust=False).mean()

# RSI
delta = stock_data['Close'].diff()
gain = (delta.where(delta > 0, 0)).rolling(window=14).mean()
loss = (-delta.where(delta < 0, 0)).rolling(window=14).mean()
RS = gain / loss
stock_data['RSI'] = 100 - (100 / (1 + RS))

stock_data.reset_index(inplace=True)
stock_data['Date'] = pd.to_datetime(stock_data['Date'])
stock_data.set_index('Date', inplace=True)

ap1 = mpf.make_addplot(stock_data[['MACD']], panel=1, ylabel='MACD', color='#1f77b4', width=1.2, ylim=(-6, 3))
ap2 = mpf.make_addplot(stock_data[['Signal Line']], panel=1, color='#ff7f0e', width=1.2, ylim=(-6, 3))
ap3 = mpf.make_addplot(stock_data[['RSI']], panel=2, ylabel='RSI', color='lightblue')

kwargs = dict(
    type='candle',
    style='yahoo',
    xrotation=90,
    ylabel='Aktienpreis',
    xlabel='Zeitraum',
    figsize=(10, 6.1),
    xlim=('2023-01-12', '2024-01-10'),
    datetime_format='%b %d',
    addplot=[ap1, ap2, ap3],
    panel_ratios=(4, 2),
    mav=9
)

fig, axlist = mpf.plot(
    stock_data,
    **kwargs,
    returnfig=True
)

axStock = axlist[0]
axStock.plot(stock_data.index, stock_data['Close'], label='SMA', color='#1f77b4')

ax = axlist[3]
ax.plot(stock_data.index, stock_data['MACD'], label='MACD', color='#1f77b4')
ax.plot(stock_data.index, stock_data['Signal Line'], label='Signallinie', color='#ff7f0e')
ax_pos = ax.get_position()
ax.set_position([ax_pos.x0, ax_pos.y0 - 0.02, ax_pos.width, ax_pos.height])

axRsi = axlist[4]
axRsi.plot(stock_data.index, stock_data['RSI'], label='RSI', color='lightblue')
axRsiPos = axRsi.get_position()
axRsi.set_position([axRsiPos.x0, axRsiPos.y0 - 0.04, axRsiPos.width, axRsiPos.height])
axRsi.axhline(70, linestyle='--', color='#ff7f0e')
axRsi.axhline(30, linestyle='--', color='#ff7f0e')
axRsi.set_yticks([0, 30, 70, 100])

for ax in axlist:
    ax.tick_params(axis='both', labelsize=11)
    ax.set_xlabel(ax.get_xlabel(), fontsize=11)
    ax.set_ylabel(ax.get_ylabel(), fontsize=11)
    ax.legend(fontsize=11)

axlist[2].get_legend().remove()
axlist[3].legend(loc='upper right')
axlist[4].legend(loc='upper right')

mpf.show()
